# Trace policy for generic foods

> **DRAFT – awaiting product owner approval.**
> No rule below may be applied to `data/foods/curated.yaml` until the product
> owner approves it and this banner is removed. A test enforces this: while the
> banner is here, no curated entry may use `source: {type: policy}`.

## Why

A generic (unbranded) food such as "buckwheat groats" has no single label to
copy a "may contain" statement from. Without a rule its trace status stays
`unknown`, and for a user with any ALLERGY exclusion an unknown food is
**excluded** (PRD §7, §9: unknown is treated like an unresolved ingredient).
This policy lets a reviewer give generic foods a trace status that reflects
what Polish retail labels for that kind of product typically declare.

## How a rule is applied

- Only to generic foods. A food with a product label (a `nutrition:` block or
  a specific brand) takes its traces from that label: `source: {type: label, ref: "<brand, product>"}`.
  A label always beats this policy.
- An entry that follows a rule records it:

  ```yaml
  may_contain: [gluten]
  traces: {status: declared, source: {type: policy, ref: "TRACE_POLICY.md#gluten-free-grains"}}
  ```

- A rule can only add traces or confirm `none_declared`; it never removes an
  allergen the food contains. Allergens already in `allergens` (or inherited
  through `derived_from`) are not repeated as traces.
- Applying a rule does not make an entry `verified`. Only a named person sets
  `review: {status: verified, by: <initials>, date: ...}` after checking it.
- Anything not covered by a rule stays `traces: {status: unknown}`.

## Proposed rules: declared traces

| Rule id | Applies to | `may_contain` | Curated foods today |
|---|---|---|---|
| `gluten-free-grains` | Buckwheat, millet, quinoa (groats, flakes, flour) | gluten | buckwheat-groats, millet-dry, quinoa-dry |
| `tree-nuts` | Whole or chopped tree nuts (almonds, walnuts, hazelnuts, cashews, pistachios ...) | peanuts, and every other tree nut is already covered by the `tree_nuts` allergen | almonds, walnuts |
| `seeds` | Whole seeds (sunflower, pumpkin, chia, flax, sesame) | peanuts, tree_nuts | chia-seeds, sunflower-seeds, sesame-seeds |
| `peanuts` | Peanuts and 100 % peanut butter | tree_nuts | peanut-butter |

Oats: EU Regulation 1169/2011 lists oats as a cereal containing gluten, so our
oat entries already *contain* gluten and need no trace rule. Oats sold as
gluten-free take their status from the label.

## Proposed rules: none declared

These decide how many foods stay available to users with an allergy, so they
need an explicit decision.

| Rule id | Applies to | Status | Curated foods today (approx.) |
|---|---|---|---|
| `fresh-produce` | Whole, raw fruit, vegetables and mushrooms with no added ingredient (not canned, frozen mixes, juices or pastes) | none_declared | about 30 |
| `raw-meat-eggs` | Raw, unprocessed, unseasoned meat, poultry and shell eggs | none_declared | about 8 |

## Open questions for the product owner

1. Rice and rice cakes: many Polish packs say "może zawierać gluten". Add rice
   to `gluten-free-grains`?
2. Ground spices: labels often declare celery, mustard, gluten and sesame.
   Declare these for all ground spices, or leave spices `unknown` until
   labelled?
3. Raw fish and seafood: include in `raw-meat-eggs`, or declare crustaceans and
   molluscs as traces for fish?
4. Seeds: should non-sesame seeds also declare sesame?
5. Plain dairy (milk, yogurt, cheese): leave `unknown` until labelled, or a
   `none_declared` rule?
