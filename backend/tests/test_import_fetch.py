"""Link import fetcher and page reader: Development Plan §7.7 acceptance criteria 1-2.

No test touches the network: DNS is a fake resolver and HTTP a MockTransport
that records every address a connection was opened to.
"""

import asyncio
import json
import zlib
from collections.abc import AsyncIterator, Callable

import httpx
import pytest

from app.imports.fetch import BlockedURL, FetchError, FetchLimits, FetchResult, check_url, fetch
from app.imports.page import PageRecipe, PageUnusable, read_recipe_page, recipe_from_html

LIMITS = FetchLimits(max_bytes=3 * 1024 * 1024, deadline_s=2.0, max_redirects=3)
PUBLIC = "93.184.215.14"
PRIVATE_DNS = {"internal.example.org": ["10.0.0.5"], "meta.example.org": ["169.254.169.254"]}

RECIPE_HTML = """<html><head>
<script type="application/ld+json">{"@context": "https://schema.org", "@graph": [
 {"@type": "WebPage"},
 {"@type": ["Recipe"], "name": "Owsianka <b>z jabłkiem</b>", "recipeYield": ["2", "2 porcje"],
  "recipeIngredient": ["50 g płatków owsianych", "1 jabłko", "200 ml mleka"],
  "recipeInstructions": [{"@type": "HowToSection", "itemListElement": [
     {"@type": "HowToStep", "text": "Zagotuj mleko."},
     {"@type": "HowToStep", "text": "Dodaj płatki."}]}]}
]}</script></head><body>x</body></html>"""


class Recorder:
    """A fake resolver plus transport. ``connected`` lists every host a request went to."""

    def __init__(
        self,
        handler: Callable[[httpx.Request], httpx.Response],
        dns: dict[str, list[str]] | None = None,
    ):
        self.handler = handler
        self.dns = {
            "www.example.com": [PUBLIC],
            "example.com": [PUBLIC],
            **PRIVATE_DNS,
            **(dns or {}),
        }
        self.lookups: list[str] = []
        self.connected: list[str] = []
        self.transport = httpx.MockTransport(self._handle)

    async def resolve(self, host: str, port: int) -> list[str]:
        self.lookups.append(host)
        return self.dns.get(host, [PUBLIC])

    def _handle(self, request: httpx.Request) -> httpx.Response:
        self.connected.append(request.url.host)
        return self.handler(request)

    async def get(self, url: str) -> FetchResult:
        return await fetch(url, limits=LIMITS, resolver=self.resolve, transport=self.transport)


def html(body: str = "<p>hi</p>", **headers: str) -> httpx.Response:
    return httpx.Response(
        200, headers={"content-type": "text/html; charset=utf-8", **headers}, text=body
    )


@pytest.mark.parametrize(
    "url",
    [
        "file:///etc/passwd",
        "gopher://example.com/",
        "ftp://example.com/x",
        "data:text/html,hi",
        "http://2130706433/",
        "http://0x7f.1/",
        "http://127.1/",
        "http://0177.0.0.1/",
        "http://127.0.0.1/",
        "http://[::1]/",
        "http://[::ffff:169.254.169.254]/",
        "http://redis:6379",
        "http://redis/",
        "http://api/",
        "http://postgres/",
        "http://localhost/",
        "http://foo.localhost/",
        "http://user:pass@example.com/",
        "http://example.com:8080/",
        "https://donut.app/x",
        "https://api.donut.app/x",
    ],
)
async def test_blocked_urls_never_connect(url: str) -> None:
    rec = Recorder(lambda r: html())
    limits = FetchLimits(LIMITS.max_bytes, LIMITS.deadline_s, LIMITS.max_redirects, ("donut.app",))
    with pytest.raises(BlockedURL):
        await fetch(url, limits=limits, resolver=rec.resolve, transport=rec.transport)
    assert rec.connected == []


@pytest.mark.parametrize("host", ["internal.example.org", "meta.example.org"])
async def test_private_dns_answer_blocked(host: str) -> None:
    rec = Recorder(lambda r: html())
    with pytest.raises(BlockedURL):
        await rec.get(f"https://{host}/")
    assert rec.connected == []


@pytest.mark.parametrize(
    "address",
    [
        "::1",
        "fe80::1",
        "fc00::1",
        "::ffff:10.0.0.1",
        "64:ff9b::a00:1",
        "2002:a00:1::",
        "100.64.0.1",
        "0.0.0.0",
    ],
)
async def test_any_private_address_in_answer_blocks(address: str) -> None:
    rec = Recorder(lambda r: html(), dns={"mixed.example.com": [PUBLIC, address]})
    with pytest.raises(BlockedURL):
        await rec.get("https://mixed.example.com/")
    assert rec.connected == []


async def test_connects_to_checked_ip_with_host_header() -> None:
    seen: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        seen.append(r)
        return html()

    rec = Recorder(handler)
    res = await rec.get("https://www.example.com/r?id=1")
    assert rec.connected == [PUBLIC]
    assert seen[0].headers["host"] == "www.example.com"
    assert seen[0].extensions["sni_hostname"] == "www.example.com"
    assert res.url == "https://www.example.com/r?id=1"


async def test_dns_rebinding_resolves_once() -> None:
    answers = iter([[PUBLIC], ["127.0.0.1"]])
    rec = Recorder(lambda r: html())

    async def rebinding(host: str, port: int) -> list[str]:
        rec.lookups.append(host)
        return next(answers)

    await fetch(
        "https://rebind.example.com/", limits=LIMITS, resolver=rebinding, transport=rec.transport
    )
    assert rec.lookups == ["rebind.example.com"]
    assert rec.connected == [PUBLIC]


async def test_redirect_to_private_blocked() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        return httpx.Response(302, headers={"location": "http://169.254.169.254/latest/meta-data/"})

    rec = Recorder(handler)
    with pytest.raises(BlockedURL):
        await rec.get("https://www.example.com/")
    assert rec.connected == [PUBLIC]


async def test_redirect_to_private_hostname_blocked() -> None:
    rec = Recorder(
        lambda r: httpx.Response(301, headers={"location": "https://internal.example.org/"})
    )
    with pytest.raises(BlockedURL):
        await rec.get("https://www.example.com/")
    assert rec.connected == [PUBLIC]


async def test_redirect_limit() -> None:
    rec = Recorder(lambda r: httpx.Response(302, headers={"location": "/again"}))
    with pytest.raises(FetchError) as e:
        await rec.get("https://www.example.com/")
    assert e.value.reason == "too_many_redirects"
    assert len(rec.connected) == LIMITS.max_redirects + 1


async def test_follows_public_redirect() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.url.path == "/old":
            return httpx.Response(301, headers={"location": "https://example.com/new"})
        return html()

    res = await Recorder(handler).get("https://www.example.com/old")
    assert res.url == "https://example.com/new"


async def test_gzip_bomb_stops_at_byte_cap() -> None:
    comp = zlib.compressobj(9, zlib.DEFLATED, 31)  # gzip
    chunk = b"\0" * (1 << 20)
    bomb = b"".join(comp.compress(chunk) for _ in range(256)) + comp.flush()  # 256 MB inflated
    assert len(bomb) < 512 * 1024
    rec = Recorder(
        lambda r: httpx.Response(
            200, headers={"content-type": "text/html", "content-encoding": "gzip"}, content=bomb
        )
    )
    with pytest.raises(FetchError) as e:
        await rec.get("https://www.example.com/")
    assert e.value.reason == "too_large"


async def test_declared_length_over_cap() -> None:
    rec = Recorder(
        lambda r: httpx.Response(
            200, headers={"content-type": "text/html"}, content=b"x" * (LIMITS.max_bytes + 1)
        )
    )
    with pytest.raises(FetchError) as e:
        await rec.get("https://www.example.com/")
    assert e.value.reason == "too_large"


async def test_drip_feed_hits_deadline() -> None:
    class Drip(httpx.AsyncByteStream):
        async def __aiter__(self) -> AsyncIterator[bytes]:
            while True:
                await asyncio.sleep(0.05)
                yield b"x"

    rec = Recorder(
        lambda r: httpx.Response(200, headers={"content-type": "text/html"}, stream=Drip())
    )
    limits = FetchLimits(LIMITS.max_bytes, 0.5, 3)
    loop = asyncio.get_running_loop()
    start = loop.time()
    with pytest.raises(FetchError) as e:
        await fetch(
            "https://www.example.com/", limits=limits, resolver=rec.resolve, transport=rec.transport
        )
    assert e.value.reason == "timeout"
    assert loop.time() - start < 1.5


async def test_image_rejected() -> None:
    rec = Recorder(
        lambda r: httpx.Response(200, headers={"content-type": "image/png"}, content=b"\x89PNG")
    )
    with pytest.raises(FetchError) as e:
        await rec.get("https://www.example.com/")
    assert e.value.reason == "bad_content_type"


def test_error_messages_do_not_contain_url() -> None:
    with pytest.raises(BlockedURL) as e:
        check_url("http://anna.kowalska%40mail.pl:x@example.com/")
    assert "kowalska" not in str(e.value)


# --- page reader ----------------------------------------------------------


def site(page: httpx.Response, robots: str | None = None, tdmrep: object = None) -> Recorder:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.url.path == "/robots.txt":
            return httpx.Response(200, text=robots) if robots is not None else httpx.Response(404)
        if r.url.path == "/.well-known/tdmrep.json":
            if tdmrep is None:
                return httpx.Response(404)
            return httpx.Response(
                200, headers={"content-type": "application/json"}, text=json.dumps(tdmrep)
            )
        return page

    return Recorder(handler)


async def read(rec: Recorder, url: str = "https://www.example.com/przepis/owsianka") -> PageRecipe:
    return await read_recipe_page(url, limits=LIMITS, resolver=rec.resolve, transport=rec.transport)


async def test_reads_recipe_from_jsonld() -> None:
    recipe = await read(site(html(RECIPE_HTML)))
    assert recipe.name == "Owsianka z jabłkiem"
    assert recipe.ingredients == ["50 g płatków owsianych", "1 jabłko", "200 ml mleka"]
    assert recipe.instructions == ["Zagotuj mleko.", "Dodaj płatki."]
    assert recipe.servings == "2"
    assert recipe.source_url == "https://www.example.com/przepis/owsianka"


async def test_robots_disallow_means_no_page_fetch() -> None:
    rec = site(html(RECIPE_HTML), robots="User-agent: DonutBot\nDisallow: /przepis/\n")
    with pytest.raises(PageUnusable) as e:
        await read(rec)
    assert e.value.reason == "robots_disallowed"
    assert len(rec.connected) == 1  # robots.txt only


async def test_tdmrep_reservation_means_no_page_fetch() -> None:
    rec = site(html(RECIPE_HTML), tdmrep=[{"location": "/*", "tdm-reservation": 1}])
    with pytest.raises(PageUnusable) as e:
        await read(rec)
    assert e.value.reason == "tdm_opt_out"
    assert len(rec.connected) == 2


async def test_tdmrep_more_specific_rule_wins() -> None:
    rules = [
        {"location": "/*", "tdm-reservation": 1},
        {"location": "/przepis/*", "tdm-reservation": 0},
    ]
    assert (await read(site(html(RECIPE_HTML), tdmrep=rules))).ingredients


async def test_tdm_header_and_meta_opt_out() -> None:
    with pytest.raises(PageUnusable, match="tdm_opt_out"):
        await read(site(html(RECIPE_HTML, **{"tdm-reservation": "1"})))
    meta = RECIPE_HTML.replace("<head>", '<head><meta name="tdm-reservation" content="1">')
    with pytest.raises(PageUnusable, match="tdm_opt_out"):
        await read(site(html(meta)))


async def test_page_without_recipe() -> None:
    with pytest.raises(PageUnusable, match="no_recipe"):
        await read(site(html("<p>Just a blog post</p>")))


async def test_blocked_url_is_not_paste_text() -> None:
    with pytest.raises(BlockedURL):
        await read(site(html(RECIPE_HTML)), "http://127.0.0.1/")


def test_deep_jsonld_ignored() -> None:
    deep = "[" * 50 + "]" * 50
    page = f'<script type="application/ld+json">{deep}</script>' + RECIPE_HTML
    assert recipe_from_html(page, "https://x.example.com/") is not None


def test_oversize_jsonld_block_ignored() -> None:
    big = json.dumps({"@type": "Recipe", "recipeIngredient": ["x" * 600_000]})
    assert recipe_from_html(f'<script type="application/ld+json">{big}</script>', "u") is None


def test_plain_string_instructions_and_limits() -> None:
    data = {
        "@type": "Recipe",
        "recipeIngredient": ["a" * 5000] + ["1 egg"] * 500,
        "recipeInstructions": "Mix.\nBake.",
    }
    r = recipe_from_html(f'<script type="application/ld+json">{json.dumps(data)}</script>', "u")
    assert r is not None
    assert len(r.ingredients) == 200 and len(r.ingredients[0]) == 1000
    assert r.instructions == ["Mix.", "Bake."]
