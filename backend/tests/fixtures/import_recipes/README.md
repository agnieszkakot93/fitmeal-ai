# Full-recipe import golden set

About 50 recipes, written for Donut as realistic rewrites (no text copied from
real sites, PRD §8.1), run by `app/imports/evaluate.py` and gated in
`tests/test_import_eval.py`.

One YAML file per recipe:

```yaml
title: "Placki z cukinii z parmezanem"
language: pl            # pl | en
source: blog            # blog | caption | cookbook
servings: 3
html: pl-placki-z-cukinii.html   # optional: lines are read from the page's JSON-LD
expected_per_serving: {kcal: 268, protein_g: 13.8}
lines:
  - {line: "2 cukinie (ok. 600 g)", slug: zucchini, grams: 600}
  - {line: "sól, pieprz", slug: null}   # must go to a clarification prompt
```

- `line` is the raw ingredient line as people write it. For an `html` recipe it
  must equal, in order, what `recipe_from_html` extracts from the page.
- `slug`/`grams` are the hand-checked truth: a food from `data/foods/curated.yaml`
  that has nutrition, and its weight. Portion and volume weights follow the
  curated entry (e.g. 1 onion = 110 g, 1 tbsp olive oil = 15 ml × 0.91).
  A weight stated in the line ("ok. 600 g", "28 oz") wins over the portion.
- `slug: null` when the line can't be answered from the text and the food data:
  a food Donut doesn't have, no amount for a non-seasoning ("olej do smażenia"),
  several foods in one line, or an ambiguous amount. "Do smaku" on salt, pepper
  or a spice means one pinch.
- `expected_per_serving` follows from the lines with a slug (must-ask lines are
  answered by the user, so they're in neither number). After editing lines,
  `test_expected_macros_match_expected_lines` tells you the new values.
