"""Admin commands.

``donut-admin foods import [--fdc-dir ...] [--dry-run]`` (default: the committed snapshot)
``donut-admin foods snapshot --fdc-dir ...`` (refresh data/foods/fdc_snapshot from a download)
``donut-admin recipes import [--dry-run]`` (run after the food import)
``donut-admin recipes report`` (per-serving nutrition with plausibility flags)
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

from app.core.db import get_sessionmaker
from app.foods import importer
from app.foods.curated import load_curated
from app.foods.fdc import load_fdc_dirs, write_snapshot
from app.recipes import catalog, report

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
DEFAULT_CURATED = DATA_DIR / "foods" / "curated.yaml"
DEFAULT_CATALOG = DATA_DIR / "recipes" / "catalog.yaml"
# the FDC records the curated list uses, committed so imports work without the download
DEFAULT_SNAPSHOT = DATA_DIR / "foods" / "fdc_snapshot"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="donut-admin")
    sub = parser.add_subparsers(dest="group", required=True)
    foods = sub.add_parser("foods").add_subparsers(dest="command", required=True)

    imp = foods.add_parser("import", help="load curated foods with USDA FDC nutrition")
    imp.add_argument("--curated", type=Path, default=DEFAULT_CURATED)
    imp.add_argument(
        "--fdc-dir",
        type=Path,
        action="append",
        default=[],
        help="unzipped FDC CSV directory (repeat for Foundation and SR Legacy)",
    )
    imp.add_argument("--dry-run", action="store_true", help="report matches, write nothing")

    recipes = sub.add_parser("recipes").add_subparsers(dest="command", required=True)
    rec = recipes.add_parser("import", help="load the recipe catalog (foods must be imported)")
    rec.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    rec.add_argument("--curated", type=Path, default=DEFAULT_CURATED)
    rec.add_argument("--dry-run", action="store_true", help="validate only, write nothing")

    recipes.add_parser("report", help="per-serving nutrition of stored recipes, with flags")

    snap = foods.add_parser("snapshot", help="save the FDC records the curated list uses")
    snap.add_argument("--curated", type=Path, default=DEFAULT_CURATED)
    snap.add_argument("--fdc-dir", type=Path, action="append", required=True)
    snap.add_argument("--out", type=Path, default=DEFAULT_SNAPSHOT)

    args = parser.parse_args(argv)
    if args.group == "foods" and args.command == "import":
        fdc_dirs = args.fdc_dir
        if not fdc_dirs and DEFAULT_SNAPSHOT.is_dir():
            print(f"using the committed FDC snapshot: {DEFAULT_SNAPSHOT}", file=sys.stderr)
            fdc_dirs = [DEFAULT_SNAPSHOT]
        return asyncio.run(_import(args.curated, fdc_dirs, args.dry_run))
    if args.group == "foods" and args.command == "snapshot":
        return _snapshot(args.curated, args.fdc_dir, args.out)
    if args.group == "recipes" and args.command == "import":
        return asyncio.run(_import_recipes(args.catalog, args.curated, args.dry_run))
    if args.group == "recipes" and args.command == "report":
        return asyncio.run(_report())
    return 2


async def _import(curated_path: Path, fdc_dirs: list[Path], dry_run: bool) -> int:
    curated = load_curated(curated_path)
    index = load_fdc_dirs(fdc_dirs) if fdc_dirs else None
    if index is None:
        print("no --fdc-dir given: only label-sourced foods will be imported", file=sys.stderr)
    report = importer.resolve(curated, index)
    print(report.summary())
    if report.allergen_problems:
        print("allergen contradictions found: nothing written", file=sys.stderr)
        return 1
    if dry_run:
        return 0
    async with get_sessionmaker()() as session, session.begin():
        await importer.apply(session, report.resolved)
    print(f"written: {len(report.resolved)} foods")
    return 0


def _snapshot(curated_path: Path, fdc_dirs: list[Path], out: Path) -> int:
    index = load_fdc_dirs(fdc_dirs)
    report = importer.resolve(load_curated(curated_path), index)
    if report.unmatched:
        print(report.summary(), file=sys.stderr)
        print("fix the unmatched foods first: nothing written", file=sys.stderr)
        return 1
    ids = {int(r.source_ref) for r in report.resolved if r.source == "usda_fdc"}
    written = write_snapshot((index.by_id[i] for i in ids), out)
    print(f"snapshot: {written} FDC records written to {out}")
    return 0


async def _import_recipes(catalog_path: Path, curated_path: Path, dry_run: bool) -> int:
    recipes = catalog.load_catalog(catalog_path)
    problems = catalog.check_against_foods(recipes, load_curated(curated_path))
    if problems:
        print("\n".join(problems), file=sys.stderr)
        return 1
    print(f"catalog ok: {len(recipes.recipes)} recipes")
    if dry_run:
        return 0
    async with get_sessionmaker()() as session, session.begin():
        report = await catalog.apply(session, recipes)
    print(report.summary())
    return 0


async def _report() -> int:
    async with get_sessionmaker()() as session:
        rows = await report.build(session)
    if not rows:
        print("no catalog recipes in the database: run `donut-admin recipes import` first")
        return 1
    print(report.render(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
