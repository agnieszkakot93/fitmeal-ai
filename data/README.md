# Data

## `foods/curated.yaml`

The hand-curated ingredient list: names (EN/PL), aliases, category, allergens,
culinary roles, portion weights, densities and package sizes. Nutrition values
come from USDA FoodData Central (FDC) or, for Polish products not in FDC, from a
product label (`nutrition:` block). See the header of the file for the format.

### Provenance: review and trace status

Every entry states its own provenance, written out explicitly even where it
equals the default, so the status of each food is visible where it is edited:

```yaml
traces: {status: unknown}          # unknown | none_declared | declared
review: {status: draft}            # draft | auto_checked | verified
```

- **`review`**: `draft` (default) → `auto_checked` (passed automated checks,
  no human sign-off) → `verified`. `verified` needs `by` (the reviewer's
  initials, 2–4 capital letters) and `date` (`YYYY-MM-DD`), and **only a named
  person sets it, never an agent or script**. It covers the whole entry,
  including portion weights, densities, package sizes and FDC descriptions.
  The importer sets `food_items.reviewed` only for `verified`.
- **`traces`** says whether `may_contain` is known:
  - `unknown` (default): nobody has checked. This is **not** "none": a user
    with an ALLERGY exclusion never gets a food with unknown traces (for any
    allergen category; free-text and `meat` exclusions are unaffected).
    No `source`, empty `may_contain`.
  - `none_declared`: checked, and the source declares no traces. Needs a
    `source`, empty `may_contain`.
  - `declared`: checked, `may_contain` lists the traces. Needs a `source` and a
    non-empty `may_contain`.

  `source` is `{type: label, ref: "<brand, product>"}` for a product label or
  `{type: policy, ref: "TRACE_POLICY.md#<rule-id>"}` for a rule of the generic
  food policy in [docs/data/TRACE_POLICY.md](../docs/data/TRACE_POLICY.md)
  (approved 2026-09-25). A test checks that every `policy` ref names a rule
  of that policy.

  Trace status is inherited through `derived_from`: if a food or anything it
  is derived from is `unknown`, the food's effective status is `unknown`.

Today all entries are `review: draft`. Generic foods covered by a rule of the
trace policy cite it; everything else is `traces: unknown`.

### Allergen lint

`fitmeal-admin foods import` (also with `--dry-run`) refuses to write when an
entry clearly contradicts its allergens: a `dairy`/`egg`/`fish`/`shellfish`
origin without milk/eggs/fish/crustaceans or molluscs, or a name or alias that
names an allergen source ("wheat", "pszenne", "tahini", "tofu", "almond" ...)
without that allergen. The rules live in `backend/app/foods/lint.py` and only
list words that always mean the allergen.

## Loading foods into the database

1. Download two CSV datasets from <https://fdc.nal.usda.gov/download-datasets>
   (free, public domain):
   - **SR Legacy** — CSV
   - **Foundation Foods** — CSV
2. Unzip both into `data/fdc/` (git-ignored), e.g.
   `data/fdc/sr_legacy/` and `data/fdc/foundation/`. Each folder must contain
   `food.csv` and `food_nutrient.csv`.
3. Check the matches first. Nothing is written:

   ```bash
   cd backend
   uv run fitmeal-admin foods import \
     --fdc-dir ../data/fdc/sr_legacy --fdc-dir ../data/fdc/foundation --dry-run
   ```

   The report lists:
   - **unmatched**: the `fdc.description` in `curated.yaml` doesn't exist in
     FDC. The closest FDC descriptions are shown under each entry (`?`). Copy the
     right one into the YAML, or use `fdc: {fdc_id: 12345}` instead.
   - **pending**: foods with no nutrition source yet (e.g. skyr, twaróg). Add a
     `nutrition:` block from a product label.
   - **energy/macro mismatches**: kcal doesn't fit the macros. Worth a look.
   - **allergen contradictions**: see "Allergen lint" above. The command exits
     with an error and writes nothing until they are fixed.
4. Run the same command without `--dry-run` to write to the database. It is
   safe to re-run; existing foods are updated in place.

With Docker Compose instead of a local Python:

```bash
docker compose -f infra/docker-compose.yml run --rm api \
  fitmeal-admin foods import --fdc-dir /app/data/fdc/sr_legacy --fdc-dir /app/data/fdc/foundation
```

## Conventions

- Nutrition is **per 100 g** of the food as weighed (raw unless the name says otherwise).
- `carbs_g` is **available carbohydrate, excluding fiber** (EU label style).
  FDC's "carbohydrate by difference" includes fiber, so the importer subtracts it.
- Allergens are the EU 14. `derived_from` makes a food inherit its parents'
  allergens (whey protein → skim milk → milk).
- `may_contain` lists "may contain" / trace declarations, kept apart from
  `allergens`, and needs `traces: {status: declared, ...}`. Traces are
  inherited through `derived_from` too; an allergen a food already contains is
  not also listed as a trace.
