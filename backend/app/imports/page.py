"""Reading a recipe from a web page link (Development Plan §3, §7.3, §7.7).

Link import reads only schema.org ``Recipe`` JSON-LD. Before the page is
fetched we check ``robots.txt`` and the site's TDMRep file; after, the
``tdm-reservation`` header and meta tag. A site that opts out of text and data
mining, or a page without recipe data, raises ``PageUnusable`` and the app asks
the user to paste the recipe text instead.

All three lookups go through ``app.imports.fetch``. The page HTML is scanned
with the standard library parser for ``<script type="application/ld+json">``
and ``<meta name="tdm-reservation">`` only; nothing else in it is kept.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Any
from urllib.robotparser import RobotFileParser

import httpx

from app.imports.fetch import (
    FetchError,
    FetchLimits,
    Resolver,
    check_url,
    fetch,
    system_resolver,
)

ROBOTS_AGENT = "DonutBot"
MAX_JSONLD_BYTES = 512 * 1024  # per script block
MAX_JSONLD_DEPTH = 20
MAX_LINES = 200  # ingredients and steps, each
MAX_LINE_CHARS = 1000
MAX_NAME_CHARS = 300
_META_BYTES = 256 * 1024  # robots.txt, tdmrep.json


class PageUnusable(Exception):
    """The link can't be imported; the app offers "paste the recipe text"."""

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = (
            reason  # "tdm_opt_out", "robots_disallowed", "no_recipe", or a FetchError code
        )


@dataclass(frozen=True, slots=True)
class PageRecipe:
    source_url: str  # kept as attribution (§7.3)
    name: str | None
    ingredients: list[str]
    instructions: list[str]
    servings: str | None = None
    language: str | None = None


# --- opt-out checks --------------------------------------------------------


def _origin(url: httpx.URL) -> str:
    return f"{url.scheme}://{url.netloc.decode('ascii')}"


async def _robots_allows(url: httpx.URL, **kw: Any) -> bool:
    try:
        res = await fetch(_origin(url) + "/robots.txt", allowed_types=None, **kw)
    except FetchError as e:
        if e.reason == "too_large":
            return False
        raise
    if res.status in (401, 403):
        return False
    if res.status >= 400:  # no robots.txt: no restriction
        return True
    parser = RobotFileParser()
    parser.parse(res.text().splitlines())
    return parser.can_fetch(ROBOTS_AGENT, str(url))


def _tdmrep_reserved(rules: Any, path: str) -> bool:
    """TDMRep ``/.well-known/tdmrep.json``: a list of {location, tdm-reservation}."""
    if not isinstance(rules, list):
        return False
    best: tuple[int, bool] | None = None
    for rule in rules[:1000]:
        if not isinstance(rule, dict):
            continue
        location = str(rule.get("location", ""))
        prefix = location.rstrip("*")
        if not path.startswith(prefix or "/"):
            continue
        reserved = str(rule.get("tdm-reservation", "0")) == "1"
        if best is None or len(prefix) > best[0]:  # the most specific rule wins
            best = (len(prefix), reserved)
    return best is not None and best[1]


async def _tdmrep_reserves(url: httpx.URL, **kw: Any) -> bool:
    res = await fetch(_origin(url) + "/.well-known/tdmrep.json", allowed_types=None, **kw)
    if res.status >= 400 or not res.body:
        return False
    try:
        rules = json.loads(res.body[:_META_BYTES])
    except ValueError:
        return False
    return _tdmrep_reserved(rules, url.path)


# --- HTML and JSON-LD -----------------------------------------------------


class _Scan(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.blocks: list[str] = []
        self.tdm_reserved = False
        self._in_jsonld = False
        self._buf: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = {k.lower(): (v or "") for k, v in attrs}
        if (
            tag == "script"
            and a.get("type", "").split(";")[0].strip().lower() == "application/ld+json"
        ):
            self._in_jsonld, self._buf = True, []
        elif tag == "meta" and a.get("name", "").lower() == "tdm-reservation":
            self.tdm_reserved = self.tdm_reserved or a.get("content", "").strip() == "1"

    def handle_data(self, data: str) -> None:
        if self._in_jsonld:
            self._buf.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._in_jsonld:
            self._in_jsonld = False
            block = "".join(self._buf)
            if len(block.encode()) <= MAX_JSONLD_BYTES:
                self.blocks.append(block)


def _depth_ok(value: Any) -> bool:
    stack: list[tuple[Any, int]] = [(value, 1)]
    while stack:
        item, depth = stack.pop()
        if depth > MAX_JSONLD_DEPTH:
            return False
        if isinstance(item, dict):
            stack.extend((v, depth + 1) for v in item.values())
        elif isinstance(item, list):
            stack.extend((v, depth + 1) for v in item)
    return True


def _is_recipe(node: dict[str, Any]) -> bool:
    types = node.get("@type")
    types = types if isinstance(types, list) else [types]
    return any(isinstance(t, str) and t.rsplit("/", 1)[-1] == "Recipe" for t in types)


def _find_recipe(data: Any) -> dict[str, Any] | None:
    stack = [data]
    while stack:
        node = stack.pop(0)
        if isinstance(node, list):
            stack.extend(node)
        elif isinstance(node, dict):
            if _is_recipe(node):
                return node
            for key in ("@graph", "mainEntity", "mainEntityOfPage"):
                if key in node:
                    stack.append(node[key])
    return None


def _clean(value: Any, limit: int = MAX_LINE_CHARS) -> str | None:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        value = str(value)
    if not isinstance(value, str):
        return None
    if "<" in value:  # some sites put HTML in JSON-LD strings
        scan = _Text()
        scan.feed(value)
        value = " ".join(scan.parts)
    text = " ".join(value.split())
    return text[:limit] or None


class _Text(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def _steps(value: Any, out: list[str]) -> None:
    if len(out) >= MAX_LINES:
        return
    if isinstance(value, list):
        for v in value:
            _steps(v, out)
    elif isinstance(value, dict):
        if "itemListElement" in value:  # HowToSection
            _steps(value["itemListElement"], out)
        else:  # HowToStep
            text = _clean(value.get("text") or value.get("name"))
            if text:
                out.append(text)
    elif isinstance(value, str):
        out.extend(t for t in (_clean(line) for line in value.splitlines()) if t)


def _first(value: Any) -> Any:
    return value[0] if isinstance(value, list) and value else value


def recipe_from_html(html: str, source_url: str) -> PageRecipe | None:
    """The first schema.org Recipe in the page's JSON-LD, or None."""
    scan = _Scan()
    scan.feed(html)
    scan.close()
    return _recipe_from_blocks(scan.blocks, source_url)


def _recipe_from_blocks(blocks: list[str], source_url: str) -> PageRecipe | None:
    for block in blocks:
        try:
            data = json.loads(block)
        except (ValueError, RecursionError):
            continue
        if not _depth_ok(data):
            continue
        node = _find_recipe(data)
        if node is None:
            continue
        raw_ingredients = node.get("recipeIngredient") or node.get("ingredients") or []
        if not isinstance(raw_ingredients, list):
            raw_ingredients = [raw_ingredients]
        ingredients = [s for s in (_clean(v) for v in raw_ingredients[:MAX_LINES]) if s]
        if not ingredients:
            continue
        steps: list[str] = []
        _steps(node.get("recipeInstructions"), steps)
        return PageRecipe(
            source_url=source_url,
            name=_clean(_first(node.get("name")), MAX_NAME_CHARS),
            ingredients=ingredients,
            instructions=steps[:MAX_LINES],
            servings=_clean(_first(node.get("recipeYield")), MAX_NAME_CHARS),
            language=_clean(node.get("inLanguage"), 35),
        )
    return None


# --- the whole read --------------------------------------------------------


async def read_recipe_page(
    url: str,
    *,
    limits: FetchLimits | None = None,
    resolver: Resolver = system_resolver,
    transport: httpx.AsyncBaseTransport | None = None,
) -> PageRecipe:
    """Check opt-outs, fetch the page and return its recipe data.

    Raises ``FetchError`` for a URL we refuse (``blocked_url``) and
    ``PageUnusable`` for everything that should end in "paste the text".
    """
    kw: dict[str, Any] = {"limits": limits, "resolver": resolver, "transport": transport}
    parsed = check_url(url, (limits or FetchLimits.from_settings()).blocked_domains)
    try:
        if not await _robots_allows(parsed, **kw):
            raise PageUnusable("robots_disallowed")
        if await _tdmrep_reserves(parsed, **kw):
            raise PageUnusable("tdm_opt_out")
        page = await fetch(str(parsed), **kw)
    except FetchError as e:
        if e.reason == "blocked_url":
            raise
        raise PageUnusable(e.reason) from e
    if page.status >= 400:
        raise PageUnusable("http_error")
    if page.headers.get("tdm-reservation", "").strip() == "1":
        raise PageUnusable("tdm_opt_out")
    if page.content_type == "application/ld+json":
        blocks, reserved = [page.text()], False
    else:
        scan = _Scan()
        scan.feed(page.text())
        scan.close()
        blocks, reserved = scan.blocks, scan.tdm_reserved
    if reserved:
        raise PageUnusable("tdm_opt_out")
    recipe = _recipe_from_blocks(blocks, page.url)
    if recipe is None:
        raise PageUnusable("no_recipe")
    return recipe
