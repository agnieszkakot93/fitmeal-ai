# Data

## `foods/curated.yaml`

The hand-curated ingredient list: names (EN/PL), aliases, category, allergens,
culinary roles, portion weights, densities and package sizes. Nutrition values
come from USDA FoodData Central (FDC) or, for Polish products not in FDC, from a
product label (`nutrition:` block). See the header of the file for the format.

Everything in it is a **first draft that needs human review**, especially
portion weights, densities and FDC descriptions.

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
