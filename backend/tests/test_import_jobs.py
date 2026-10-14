"""Import jobs API and worker against Postgres, with the curated foods and FDC snapshot.

The arq task runs in-process (``worker.run_import``), without Redis. Link
imports use the fake resolver and transport from ``test_import_fetch``; nothing
touches the network.
"""

from __future__ import annotations

import uuid
from collections.abc import AsyncIterator, Iterator
from typing import Any

import httpx
import pytest
from httpx import AsyncClient
from sqlalchemy import func, select, text, update

from app.core.db import get_sessionmaker
from app.foods import importer
from app.foods.curated import load_curated
from app.foods.fdc import load_fdc_dirs
from app.importjobs import worker
from app.importjobs.config import get_import_settings
from app.importjobs.models import ImportCacheEntry, ImportJob
from app.importjobs.queue import ArqQueue, get_queue
from app.main import app
from app.recipes.models import Recipe, RecipeIngredient, RecipeSource
from tests.test_auth import FakeApple, apple, apple_key, bearer, client, login
from tests.test_foods_db import CURATED
from tests.test_import_fetch import LIMITS, Recorder, html
from tests.test_planner_catalog import SNAPSHOT

__all__ = ["apple", "apple_key", "client"]  # fixtures shared with test_auth

Json = dict[str, Any]

TEXT = """Owsianka z bananem
Porcje: 2
Składniki:
1 1/2 szklanki mleka
1 banan
1 łyżka miodu
kawałek czegoś słodkiego
Przygotowanie:
1. Zagotuj mleko.
2. Dodaj banana i miód.
"""
SWEET = 3  # the line that must ask

PAGE = """<html><head><script type="application/ld+json">
{"@context": "https://schema.org", "@type": "Recipe", "name": "Peanut eggs",
 "recipeYield": "2 servings", "inLanguage": "en",
 "recipeIngredient": ["3 eggs", "2 tbsp peanut butter", "1 cup cheese"],
 "recipeInstructions": [{"@type": "HowToStep", "text": "Mix."}]}
</script></head><body>x</body></html>"""
URL = "https://www.example.com/recipes/peanut-eggs?id=7&utm_source=ig&fbclid=abc"
CLEAN_URL = "https://www.example.com/recipes/peanut-eggs?id=7"  # stored and fetched
CHEESE = 2


class FakeQueue:
    def __init__(self) -> None:
        self.ids: list[uuid.UUID] = []
        self.down = False

    async def enqueue(self, import_id: uuid.UUID) -> None:
        if self.down:
            raise ConnectionError("redis down")
        self.ids.append(import_id)


@pytest.fixture(scope="module")
async def foods(migrated_db: None) -> AsyncIterator[None]:
    async with get_sessionmaker()() as session:
        await session.execute(text("TRUNCATE food_items, recipe_sources CASCADE"))
        report = importer.resolve(load_curated(CURATED), load_fdc_dirs([SNAPSHOT]))
        await importer.apply(session, report.resolved)
        await session.commit()
    yield


@pytest.fixture
def queue() -> Iterator[FakeQueue]:
    fake = FakeQueue()
    app.dependency_overrides[get_queue] = lambda: fake
    yield fake
    app.dependency_overrides.pop(get_queue, None)


@pytest.fixture
async def api(foods: None, client: AsyncClient, queue: FakeQueue) -> AsyncClient:
    return client


def site(page: str = PAGE) -> Recorder:
    def handle(request: httpx.Request) -> httpx.Response:
        if request.url.path in ("/robots.txt", "/.well-known/tdmrep.json"):
            return httpx.Response(404)
        return html(page)

    return Recorder(handle)


async def submit(c: AsyncClient, pair: Json, **body: Any) -> httpx.Response:
    return await c.post("/v1/imports", json=body, headers=bearer(pair))


async def run(job_id: str, recorder: Recorder | None = None) -> None:
    ctx: dict[str, Any] = {}
    if recorder is not None:
        ctx = {"resolver": recorder.resolve, "transport": recorder.transport}
        ctx["fetch_limits"] = LIMITS
    await worker.run_import(ctx, job_id)


async def imported(
    c: AsyncClient, pair: Json, recorder: Recorder | None = None, **body: Any
) -> Json:
    res = await submit(c, pair, **body)
    assert res.status_code == 202, res.text
    await run(res.json()["id"], recorder)
    got = await c.get(f"/v1/imports/{res.json()['id']}", headers=bearer(pair))
    assert got.status_code == 200, got.text
    out: Json = got.json()
    return out


async def stored(job_id: str) -> ImportJob:
    async with get_sessionmaker()() as session:
        job = await session.get(ImportJob, uuid.UUID(job_id))
        assert job is not None
        return job


# --- submission ----------------------------------------------------------------


async def test_sign_in_required(api: AsyncClient) -> None:
    some = uuid.uuid4()
    assert (await api.post("/v1/imports", json={"type": "text"})).status_code == 401
    assert (await api.get(f"/v1/imports/{some}")).status_code == 401
    assert (await api.post(f"/v1/imports/{some}/confirm", json={})).status_code == 401


@pytest.mark.parametrize(
    "body",
    [
        {"type": "link", "origin": "paste"},  # no url
        {"type": "link", "origin": "paste", "url": URL, "text": "x"},
        {"type": "link", "origin": "pdf", "url": URL},  # PDF text is a text import
        {"type": "text", "origin": "paste", "text": "   "},
        {"type": "text", "origin": "paste", "text": "ą" * 150_000},  # 300 KB as UTF-8
        {"type": "text", "origin": "fax", "text": "x"},
        {"type": "text", "origin": "paste", "text": "x", "public": True},
        {"type": "link", "origin": "paste", "url": "https://www.example.com/a\u0000b"},
    ],
)
async def test_bad_bodies_are_refused_without_echo(
    api: AsyncClient, apple: FakeApple, queue: FakeQueue, body: Json
) -> None:
    pair = await login(api, apple)
    res = await submit(api, pair, **body)
    assert res.status_code == 422
    assert "ąąą" not in res.text and URL not in res.text
    assert queue.ids == []


@pytest.mark.parametrize(
    "url", ["http://127.0.0.1/x", "http://redis:6379/", "file:///etc/passwd", "http://0x7f.1/"]
)
async def test_blocked_links_fail_before_queueing(
    api: AsyncClient, apple: FakeApple, queue: FakeQueue, url: str
) -> None:
    pair = await login(api, apple)
    res = await submit(api, pair, type="link", origin="paste", url=url)
    assert (res.status_code, res.json()["detail"]) == (422, "blocked_url")
    assert queue.ids == []


@pytest.mark.parametrize(
    "url", ["https://www.instagram.com/p/abc/", "https://vm.tiktok.com/x", "https://x.com/a/1"]
)
async def test_social_posts_are_never_fetched(
    api: AsyncClient, apple: FakeApple, queue: FakeQueue, url: str
) -> None:
    pair = await login(api, apple)
    res = await submit(api, pair, type="link", origin="share", url=url)
    assert (res.status_code, res.json()["detail"]) == (422, "platform_link")
    assert queue.ids == []


async def test_nul_and_controls_never_reach_the_database_or_logs(
    api: AsyncClient, apple: FakeApple, caplog: pytest.LogCaptureFixture
) -> None:
    pair = await login(api, apple)
    canary = "Anna Kowalska CANARY-7731"
    out = await imported(
        api, pair, type="text", origin="pdf", text=TEXT.replace("Porcje", f"{canary}\x00\x0cPorcje")
    )
    assert out["status"] == "ready"
    res = await api.post(
        f"/v1/imports/{out['id']}/confirm",
        json={"title": f"{canary}\u0000", "answers": [{"position": SWEET, "skip": True}]},
        headers=bearer(pair),
    )
    assert res.status_code == 422 and canary not in res.text
    assert canary not in caplog.text


async def test_oversized_declared_body_is_413(api: AsyncClient, apple: FakeApple) -> None:
    pair = await login(api, apple)
    res = await api.post(
        "/v1/imports",
        content=b"{" + b" " * 500_000 + b"}",
        headers={**bearer(pair), "content-type": "application/json"},
    )
    assert res.status_code == 413


async def test_the_queue_gets_only_the_id(
    api: AsyncClient, apple: FakeApple, queue: FakeQueue
) -> None:
    pair = await login(api, apple)
    res = await submit(api, pair, type="text", origin="paste", text=TEXT)
    assert res.status_code == 202
    body = res.json()
    assert (body["status"], body["preview"]) == ("queued", None)
    assert queue.ids == [uuid.UUID(body["id"])]


async def test_arq_payload_is_the_id_only() -> None:
    calls: list[tuple[Any, ...]] = []

    class Pool:
        async def enqueue_job(self, *args: Any, **kwargs: Any) -> None:
            calls.append((args, kwargs))

    q = ArqQueue()
    q._pool = Pool()  # type: ignore[assignment]
    job_id = uuid.uuid4()
    await q.enqueue(job_id)
    assert calls == [(("run_import", str(job_id)), {"_job_id": f"import:{job_id}"})]
    assert worker.WorkerSettings.keep_result == 0


async def test_queue_down_is_503_and_costs_no_quota(
    api: AsyncClient, apple: FakeApple, queue: FakeQueue
) -> None:
    pair = await login(api, apple)
    queue.down = True
    res = await submit(api, pair, type="text", origin="paste", text=TEXT)
    assert res.status_code == 503
    async with get_sessionmaker()() as session:
        assert await session.scalar(select(func.count()).select_from(ImportJob)) == 0


async def test_daily_quota(
    api: AsyncClient, apple: FakeApple, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(get_import_settings(), "import_daily_quota", 2)
    pair = await login(api, apple)
    for _ in range(2):
        assert (await submit(api, pair, type="text", origin="paste", text=TEXT)).status_code == 202
    res = await submit(api, pair, type="text", origin="paste", text=TEXT)
    assert res.status_code == 429
    # yesterday's imports don't count; another user has their own quota
    other = await login(api, apple, sub="apple-sub-2")
    assert (await submit(api, other, type="text", origin="paste", text=TEXT)).status_code == 202
    async with get_sessionmaker()() as session:
        await session.execute(
            update(ImportJob).values(created_at=func.now() - text("interval '25 hours'"))
        )
        await session.commit()
    assert (await submit(api, pair, type="text", origin="paste", text=TEXT)).status_code == 202


# --- the worker -----------------------------------------------------------------


async def test_text_import_previews_matches_and_questions(
    api: AsyncClient, apple: FakeApple
) -> None:
    pair = await login(api, apple)
    out = await imported(api, pair, type="text", origin="paste", text=TEXT)
    assert (out["status"], out["error"], out["cached"]) == ("ready", None, False)
    preview = out["preview"]
    assert (preview["title"], preview["servings"], preview["language"]) == (
        "Owsianka z bananem",
        2,
        "pl",
    )
    assert preview["instructions"] == ["Zagotuj mleko.", "Dodaj banana i miód."]
    lines = preview["ingredients"]
    assert [line["food"]["slug"] for line in lines[:SWEET]] == ["milk-2", "banana", "honey"]
    assert lines[SWEET]["needs_clarification"]  # a best guess at most, never taken unasked
    assert lines[0]["grams"] == pytest.approx(386, rel=0.05)
    assert all(not line["needs_clarification"] for line in lines[:SWEET])
    assert [(q["kind"], q["position"]) for q in preview["clarifications"]] == [
        ("ingredient", SWEET)
    ]
    assert preview["confidence"] == lines[SWEET]["confidence"] < 0.7
    # the raw text is gone once parsing ends
    assert (await stored(out["id"])).input_text is None


async def test_pdf_text_is_a_text_import(api: AsyncClient, apple: FakeApple) -> None:
    pair = await login(api, apple)
    out = await imported(api, pair, type="text", origin="pdf", text=TEXT)
    assert (out["origin"], out["status"]) == ("pdf", "ready")


async def test_link_import_reads_json_ld(api: AsyncClient, apple: FakeApple) -> None:
    pair = await login(api, apple)
    rec = site()
    out = await imported(api, pair, rec, type="link", origin="share", url=URL)
    assert out["status"] == "ready", out
    preview = out["preview"]
    assert (preview["title"], preview["servings"], preview["source_url"]) == (
        "Peanut eggs",
        2,
        CLEAN_URL,
    )
    lines = preview["ingredients"]
    assert lines[0]["food"]["slug"] == "egg-whole-raw"
    assert lines[1]["food"]["slug"] == "peanut-butter"
    assert [q["position"] for q in preview["clarifications"]] == [CHEESE]
    assert rec.connected and set(rec.connected) == {"93.184.215.14"}


async def test_link_without_recipe_data_fails_with_a_reason(
    api: AsyncClient, apple: FakeApple
) -> None:
    pair = await login(api, apple)
    out = await imported(api, pair, site("<p>no recipe</p>"), type="link", origin="paste", url=URL)
    assert (out["status"], out["error"], out["preview"]) == ("failed", "no_recipe", None)


async def test_link_resolving_to_a_private_address_is_blocked(
    api: AsyncClient, apple: FakeApple
) -> None:
    pair = await login(api, apple)
    rec = site()
    url = "https://internal.example.org/recipe"  # the fake DNS answers 10.0.0.5
    out = await imported(api, pair, rec, type="link", origin="paste", url=url)
    assert (out["status"], out["error"]) == ("failed", "blocked_url")
    assert rec.connected == []


async def test_a_job_runs_once(api: AsyncClient, apple: FakeApple) -> None:
    pair = await login(api, apple)
    out = await imported(api, pair, type="text", origin="paste", text=TEXT)
    await run(out["id"])  # arq delivering it again changes nothing
    again = await api.get(f"/v1/imports/{out['id']}", headers=bearer(pair))
    assert again.json() == out


# --- cache ----------------------------------------------------------------------


async def test_link_cache_is_shared_and_keyed_by_the_submitted_url(
    api: AsyncClient, apple: FakeApple
) -> None:
    first = await login(api, apple)
    await imported(api, first, site(), type="link", origin="paste", url=URL)
    second = await login(api, apple, sub="apple-sub-2")
    rec = site()
    same = "HTTPS://WWW.EXAMPLE.COM/recipes/peanut-eggs?id=7&utm_medium=x#steps"
    out = await imported(api, second, rec, type="link", origin="paste", url=same)
    assert (out["status"], out["cached"]) == ("ready", True)
    assert rec.connected == []  # no fetch at all
    # the path and query keep their case: another page
    other = await imported(
        api, second, site(), type="link", origin="paste", url=URL.replace("id=7", "ID=7")
    )
    assert other["cached"] is False


async def test_text_cache_is_per_user(api: AsyncClient, apple: FakeApple) -> None:
    pair = await login(api, apple)
    await imported(api, pair, type="text", origin="paste", text=TEXT)
    again = await imported(api, pair, type="text", origin="share", text=TEXT.replace("\n", "\n  "))
    assert (again["status"], again["cached"]) == ("ready", True)
    other = await login(api, apple, sub="apple-sub-2")
    theirs = await imported(api, other, type="text", origin="paste", text=TEXT)
    assert theirs["cached"] is False
    async with get_sessionmaker()() as session:
        owners = (await session.scalars(select(ImportCacheEntry.user_id))).all()
    assert None not in owners and len(set(owners)) == 2


async def test_shared_caption_url_never_keys_the_shared_cache(
    api: AsyncClient, apple: FakeApple
) -> None:
    pair = await login(api, apple)
    out = await imported(
        api, pair, type="text", origin="share", text=TEXT, url="https://www.instagram.com/p/abc/"
    )
    assert out["preview"]["source_url"] == "https://www.instagram.com/p/abc/"
    async with get_sessionmaker()() as session:
        entries = (await session.scalars(select(ImportCacheEntry))).all()
    assert [e.user_id for e in entries] != [None] and all(
        e.key.startswith("text:") for e in entries
    )


# --- ownership, expiry --------------------------------------------------------


async def test_only_the_owner_can_read_or_confirm(api: AsyncClient, apple: FakeApple) -> None:
    owner = await login(api, apple)
    out = await imported(api, owner, type="text", origin="paste", text=TEXT)
    other = await login(api, apple, sub="apple-sub-2")
    assert (await api.get(f"/v1/imports/{out['id']}", headers=bearer(other))).status_code == 404
    res = await api.post(
        f"/v1/imports/{out['id']}/confirm",
        json={"answers": [{"position": SWEET, "skip": True}]},
        headers=bearer(other),
    )
    assert res.status_code == 404
    assert (await stored(out["id"])).status == "ready"


async def test_expired_previews_are_gone(api: AsyncClient, apple: FakeApple) -> None:
    pair = await login(api, apple)
    out = await imported(api, pair, type="text", origin="paste", text=TEXT)
    async with get_sessionmaker()() as session:
        await session.execute(
            update(ImportJob).values(expires_at=func.now() - text("interval '1 minute'"))
        )
        await session.commit()
    assert (await api.get(f"/v1/imports/{out['id']}", headers=bearer(pair))).status_code == 404
    await worker.purge_expired({})
    async with get_sessionmaker()() as session:
        assert await session.get(ImportJob, uuid.UUID(out["id"])) is None


# --- confirm ----------------------------------------------------------------------


async def test_confirm_needs_every_answer(api: AsyncClient, apple: FakeApple) -> None:
    pair = await login(api, apple)
    out = await imported(api, pair, rec := site(), type="link", origin="paste", url=URL)
    assert rec.connected
    res = await api.post(f"/v1/imports/{out['id']}/confirm", json={}, headers=bearer(pair))
    assert res.status_code == 422
    assert (res.json()["positions"], res.json()["missing"]) == ([CHEESE], [])


@pytest.mark.parametrize(
    "answer",
    [
        {"position": CHEESE, "food_slug": "no-such-food", "grams": 50},
        {"position": 99, "skip": True},
        {"position": CHEESE, "skip": True, "grams": 5},
        {"position": CHEESE, "food_slug": "parmesan", "grams": -1},
    ],
)
async def test_confirm_rejects_bad_answers(
    api: AsyncClient, apple: FakeApple, answer: Json
) -> None:
    pair = await login(api, apple)
    out = await imported(api, pair, site(), type="link", origin="paste", url=URL)
    res = await api.post(
        f"/v1/imports/{out['id']}/confirm", json={"answers": [answer]}, headers=bearer(pair)
    )
    assert res.status_code == 422
    assert (await stored(out["id"])).status == "ready"


async def test_confirm_stores_a_private_recipe(api: AsyncClient, apple: FakeApple) -> None:
    pair = await login(api, apple)
    out = await imported(api, pair, site(), type="link", origin="paste", url=URL)
    body = {"answers": [{"position": CHEESE, "food_slug": "parmesan", "grams": 40}]}
    res = await api.post(f"/v1/imports/{out['id']}/confirm", json=body, headers=bearer(pair))
    assert res.status_code == 201, res.text
    recipe = res.json()["recipe"]
    assert (recipe["title_en"], recipe["servings"], recipe["slug"]) == ("Peanut eggs", 2, None)
    assert recipe["per_serving"]["kcal"] > 0
    assert {"eggs", "peanuts", "milk"} <= set(recipe["allergens"])

    async with get_sessionmaker()() as session:
        row = await session.get(Recipe, uuid.UUID(recipe["id"]))
        assert row is not None
        source = await session.get(RecipeSource, row.source_id)
        assert source is not None
        me = (await api.get("/v1/me", headers=bearer(pair))).json()
        assert str(row.owner_user_id) == me["id"]
        assert (source.type, source.public_usage_status, source.reference) == (
            "link",
            "private_only",
            CLEAN_URL,
        )
    job = await stored(out["id"])
    assert (job.status, job.preview, str(job.recipe_id)) == ("confirmed", None, recipe["id"])
    # never in the public catalogue
    catalogue = (await api.get("/v1/recipes")).json()
    assert recipe["id"] not in {r["id"] for r in catalogue["items"]}
    assert (await api.get(f"/v1/recipes/{recipe['id']}")).status_code == 404
    # confirmed once only
    again = await api.post(f"/v1/imports/{out['id']}/confirm", json=body, headers=bearer(pair))
    assert again.status_code == 409
    assert (await api.get(f"/v1/imports/{out['id']}", headers=bearer(pair))).json()[
        "recipe_id"
    ] == recipe["id"]


async def test_confirm_text_with_a_skip_and_new_title(api: AsyncClient, apple: FakeApple) -> None:
    pair = await login(api, apple)
    out = await imported(api, pair, type="text", origin="pdf", text=TEXT)
    body = {
        "title": "Moja owsianka",
        "servings": 1,
        "answers": [
            {"position": SWEET, "skip": True},
            {"position": 1, "grams": 200},  # more banana than the line said
        ],
    }
    res = await api.post(f"/v1/imports/{out['id']}/confirm", json=body, headers=bearer(pair))
    assert res.status_code == 201, res.text
    recipe = res.json()["recipe"]
    assert (recipe["title_pl"], recipe["title_en"], recipe["servings"]) == (
        "Moja owsianka",
        None,
        1,
    )
    async with get_sessionmaker()() as session:
        row = await session.get(Recipe, uuid.UUID(recipe["id"]))
        assert row is not None
        source = await session.get(RecipeSource, row.source_id)
        assert source is not None and (source.type, source.reference) == ("pdf", None)
        grams = await session.scalars(
            select(RecipeIngredient.amount_g)
            .where(RecipeIngredient.recipe_id == row.id)
            .order_by(RecipeIngredient.position)
        )
        assert list(grams) == [pytest.approx(386, rel=0.05), 200, pytest.approx(21.3, rel=0.05)]
        assert row.instructions_pl == ["Zagotuj mleko.", "Dodaj banana i miód."]


async def test_confirm_asks_for_servings_when_unknown(api: AsyncClient, apple: FakeApple) -> None:
    pair = await login(api, apple)
    out = await imported(api, pair, type="text", origin="paste", text="Placki\n3 jajka\n1 banan")
    kinds = [q["kind"] for q in out["preview"]["clarifications"]]
    assert kinds == ["servings"]
    res = await api.post(f"/v1/imports/{out['id']}/confirm", json={}, headers=bearer(pair))
    assert (res.status_code, res.json()["missing"]) == (422, ["servings"])
    res = await api.post(
        f"/v1/imports/{out['id']}/confirm", json={"servings": 2}, headers=bearer(pair)
    )
    assert res.status_code == 201, res.text


async def test_account_erasure_removes_imports(api: AsyncClient, apple: FakeApple) -> None:
    pair = await login(api, apple)
    await imported(api, pair, type="text", origin="paste", text=TEXT)
    assert (await api.delete("/v1/me", headers=bearer(pair))).status_code == 204
    async with get_sessionmaker()() as session:
        assert await session.scalar(select(func.count()).select_from(ImportJob)) == 0
        assert await session.scalar(select(func.count()).select_from(ImportCacheEntry)) == 0


async def test_personal_data_is_cut_from_steps(api: AsyncClient, apple: FakeApple) -> None:
    pair = await login(api, apple)
    note = "Klientka: tel. 600 123 456, anna.k@example.com, https://example.com/plan?u=1"
    out = await imported(api, pair, type="text", origin="paste", text=TEXT + note + "\n")
    steps = " ".join(out["preview"]["instructions"])
    assert "600" not in steps and "@" not in steps and "https" not in steps
    assert "Zagotuj mleko." in steps


async def test_shared_link_entries_hold_no_steps(api: AsyncClient, apple: FakeApple) -> None:
    pair = await login(api, apple)
    out = await imported(api, pair, site(), type="link", origin="paste", url=URL)
    assert out["preview"]["instructions"] == ["Mix."]
    async with get_sessionmaker()() as session:
        entry = await session.scalar(select(ImportCacheEntry))
        assert entry is not None and entry.user_id is None
        assert entry.recipe["instructions"] == []
        assert entry.recipe["ingredients"] == ["3 eggs", "2 tbsp peanut butter", "1 cup cheese"]


async def test_stale_jobs_fail_and_lose_their_text(api: AsyncClient, apple: FakeApple) -> None:
    pair = await login(api, apple)
    res = await submit(api, pair, type="text", origin="paste", text=TEXT)
    job_id = res.json()["id"]
    async with get_sessionmaker()() as session:
        await session.execute(
            update(ImportJob).values(
                status="running", created_at=func.now() - text("interval '20 minutes'")
            )
        )
        await session.commit()
    await worker.purge_expired({})
    job = await stored(job_id)
    assert (job.status, job.error, job.input_text) == ("failed", "timeout", None)
