"""Guarded HTTP fetching for link import (Development Plan §7.7, URL fetching and limits).

Every URL we fetch for an import, the page itself and its ``robots.txt`` and
TDMRep lookups, goes through ``fetch``:

- only ``http``/``https`` on ports 80/443, no credentials, no raw IP hosts in
  any spelling, no single-label hosts (Docker service names) and none of our
  own domains;
- the host is resolved once, every address must be ``is_global``, and the
  connection goes to that checked address (no second lookup, so DNS rebinding
  cannot swap it);
- redirects are followed by hand, each hop checked again;
- one deadline covers the whole fetch, and the body is capped after
  decompression, so a drip-feeding server or a gzip bomb both stop early.

Error messages never contain the URL: it may carry personal data.
"""

from __future__ import annotations

import asyncio
import ipaddress
import logging
import re
import socket
from collections.abc import Awaitable, Callable, Collection
from dataclasses import dataclass

import httpx

from app.core.config import get_settings

# these log full URLs (§7.2)
for _name in ("httpx", "httpcore"):
    logging.getLogger(_name).setLevel(logging.WARNING)

USER_AGENT = "DonutBot/0.1 (+recipe link import)"
HTML_TYPES = frozenset({"text/html", "application/xhtml+xml", "application/ld+json"})
_PORTS = {"http": 80, "https": 443}
_REDIRECTS = {301, 302, 303, 307, 308}
# WHATWG: a host whose last label is a number is an IPv4 address ("2130706433",
# "0x7f.1", "127.1", "0177.0.0.1")
_NUMERIC_LABEL = re.compile(r"^(?:0x[0-9a-f]*|[0-9]+)$", re.IGNORECASE)

Resolver = Callable[[str, int], Awaitable[list[str]]]


class FetchError(Exception):
    """A fetch we refused or that failed. ``reason`` is a stable code for the API."""

    def __init__(self, reason: str, detail: str = "") -> None:
        super().__init__(f"{reason}: {detail}" if detail else reason)
        self.reason = reason


class BlockedURL(FetchError):
    def __init__(self, detail: str) -> None:
        super().__init__("blocked_url", detail)


@dataclass(frozen=True, slots=True)
class FetchLimits:
    max_bytes: int
    deadline_s: float
    max_redirects: int
    blocked_domains: tuple[str, ...] = ()

    @classmethod
    def from_settings(cls) -> FetchLimits:
        s = get_settings()
        return cls(
            max_bytes=s.import_max_bytes,
            deadline_s=s.import_deadline_s,
            max_redirects=s.import_max_redirects,
            blocked_domains=tuple(d.lower().strip(".") for d in s.import_blocked_domains),
        )


@dataclass(frozen=True, slots=True)
class FetchResult:
    url: str  # the final URL, after redirects
    status: int
    content_type: str  # lower case, without parameters
    headers: httpx.Headers
    body: bytes

    def text(self) -> str:
        charset = None
        for part in self.headers.get("content-type", "").split(";")[1:]:
            key, _, value = part.strip().partition("=")
            if key.lower() == "charset":
                charset = value.strip("\"' ")
        try:
            return self.body.decode(charset or "utf-8", errors="replace")
        except LookupError:
            return self.body.decode("utf-8", errors="replace")


async def system_resolver(host: str, port: int) -> list[str]:
    loop = asyncio.get_running_loop()
    infos = await loop.getaddrinfo(host, port, type=socket.SOCK_STREAM)
    return list(dict.fromkeys(str(info[4][0]) for info in infos))


def check_url(url: str | httpx.URL, blocked_domains: Collection[str] = ()) -> httpx.URL:
    """Reject a URL we must never fetch, before any DNS lookup. Returns it parsed."""
    try:
        parsed = url if isinstance(url, httpx.URL) else httpx.URL(url)
    except (httpx.InvalidURL, ValueError, TypeError) as e:
        raise BlockedURL("not a valid URL") from e
    if parsed.scheme not in _PORTS:
        raise BlockedURL("scheme")
    if parsed.userinfo:
        raise BlockedURL("credentials in URL")
    if parsed.port is not None and parsed.port not in _PORTS.values():
        raise BlockedURL("port")
    host = parsed.host.lower().rstrip(".")
    if not host:
        raise BlockedURL("no host")
    if ":" in host:
        raise BlockedURL("IP address host")
    try:
        ipaddress.ip_address(host)
    except ValueError:
        pass
    else:
        raise BlockedURL("IP address host")
    labels = host.split(".")
    if _NUMERIC_LABEL.match(labels[-1]):
        raise BlockedURL("IP address host")
    if len(labels) < 2:  # "redis", "api", "postgres", "localhost"
        raise BlockedURL("single-label host")
    if labels[-1] in {"localhost", "local", "internal", "localdomain"}:
        raise BlockedURL("local host")
    for domain in blocked_domains:
        if host == domain or host.endswith("." + domain):
            raise BlockedURL("own domain")
    return parsed


def check_address(address: str) -> ipaddress.IPv4Address | ipaddress.IPv6Address:
    ip = ipaddress.ip_address(address.split("%", 1)[0])
    if isinstance(ip, ipaddress.IPv6Address):
        mapped = ip.ipv4_mapped or ip.sixtofour
        if mapped is not None and not mapped.is_global:
            raise BlockedURL("non-public address")
        if ip in ipaddress.ip_network("64:ff9b::/96") or ip in ipaddress.ip_network(
            "64:ff9b:1::/48"
        ):
            raise BlockedURL("non-public address")
    if not ip.is_global or ip.is_multicast:
        raise BlockedURL("non-public address")
    return ip


async def _resolve_checked(url: httpx.URL, resolver: Resolver) -> str:
    port = url.port or _PORTS[url.scheme]
    try:
        addresses = await resolver(url.host, port)
    except OSError as e:
        raise FetchError("dns_failed") from e
    if not addresses:
        raise FetchError("dns_failed")
    checked = [check_address(a) for a in addresses]  # every answer must be public
    return str(checked[0])


async def _get_once(
    client: httpx.AsyncClient, url: httpx.URL, address: str, max_bytes: int
) -> FetchResult:
    target = url.copy_with(host=address)  # connect to the checked address
    host_header = url.netloc.decode("ascii")
    request = client.build_request(
        "GET",
        target,
        headers={"Host": host_header},
        # TLS: SNI and certificate check use the real host name, not the IP
        extensions={"sni_hostname": url.host} if url.scheme == "https" else {},
    )
    response = await client.send(request, stream=True)
    try:
        content_type = response.headers.get("content-type", "").split(";")[0].strip().lower()
        body = b""
        if response.status_code not in _REDIRECTS:
            declared = response.headers.get("content-length")
            if declared and declared.isdigit() and int(declared) > max_bytes:
                raise FetchError("too_large")
            chunks: list[bytes] = []
            size = 0
            async for chunk in response.aiter_bytes():  # decompressed
                size += len(chunk)
                if size > max_bytes:
                    raise FetchError("too_large")
                chunks.append(chunk)
            body = b"".join(chunks)
        return FetchResult(str(url), response.status_code, content_type, response.headers, body)
    finally:
        await response.aclose()


async def fetch(
    url: str,
    *,
    limits: FetchLimits | None = None,
    allowed_types: Collection[str] | None = HTML_TYPES,
    resolver: Resolver = system_resolver,
    transport: httpx.AsyncBaseTransport | None = None,
) -> FetchResult:
    """GET ``url`` under the import guard. ``allowed_types=None`` accepts any type."""
    limits = limits or FetchLimits.from_settings()
    current = check_url(url, limits.blocked_domains)
    async with httpx.AsyncClient(
        transport=transport,
        trust_env=False,  # no proxy or netrc from the environment
        follow_redirects=False,
        timeout=httpx.Timeout(limits.deadline_s),
        headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml"},
    ) as client:
        try:
            async with asyncio.timeout(limits.deadline_s):
                for _hop in range(limits.max_redirects + 1):
                    address = await _resolve_checked(current, resolver)
                    result = await _get_once(client, current, address, limits.max_bytes)
                    if result.status not in _REDIRECTS:
                        break
                    location = result.headers.get("location")
                    if not location:
                        raise FetchError("bad_redirect")
                    current = check_url(current.join(location), limits.blocked_domains)
                else:
                    raise FetchError("too_many_redirects")
        except TimeoutError as e:
            raise FetchError("timeout") from e
        except httpx.HTTPError as e:
            raise FetchError("network_error", type(e).__name__) from e
    if (
        allowed_types is not None
        and result.status < 400
        and result.content_type not in allowed_types
    ):
        raise FetchError("bad_content_type")
    return result
