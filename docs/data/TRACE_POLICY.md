# Trace policy for generic foods

Approved by the product owner on 2026-09-25, including the answers to the
open questions of the draft (see "Decisions" below).

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
  The reviewer spot-checks the rule against current Polish retail labels and
  records a `label` source instead wherever a label says otherwise.
- Anything not covered by a rule stays `traces: {status: unknown}`. When in
  doubt whether a food fits a rule, leave it `unknown`.

## Rules: declared traces

| Rule id | Applies to | `may_contain` (minus what the food contains) |
|---|---|---|
| `gluten-free-grains` | Rice, buckwheat, millet, quinoa (grains, groats, flakes, flour) and plain rice cakes | gluten |
| `tree-nuts` | Whole or chopped tree nuts (almonds, walnuts, hazelnuts, cashews, pistachios ...) | peanuts (every other tree nut is already covered by the `tree_nuts` allergen) |
| `seeds` | Whole seeds (sunflower, pumpkin, chia, flax, sesame) | peanuts, tree_nuts, sesame |
| `peanuts` | Peanuts and 100 % peanut butter | tree_nuts |
| `ground-spices` | Dried ground or whole single spices (pepper, paprika, cinnamon, cumin ...), not salt or spice blends with other ingredients | celery, mustard, gluten, sesame |
| `raw-fish-seafood` | Raw, unprocessed, unseasoned fish, crustaceans and molluscs (not canned, smoked or marinated) | fish, crustaceans, molluscs |

Oats: EU Regulation 1169/2011 lists oats as a cereal containing gluten, so our
oat entries already *contain* gluten and need no trace rule. Oats sold as
gluten-free take their status from the label.

## Rules: none declared

These decide how many foods stay available to users with an allergy.

| Rule id | Applies to | Status |
|---|---|---|
| `fresh-produce` | Whole, raw fruit, vegetables and mushrooms with no added ingredient (not canned, frozen, juices, purées or pastes) | none_declared |
| `raw-meat-eggs` | Raw, unprocessed, unseasoned meat and poultry (whole cuts or plain mince), and shell eggs | none_declared |
| `plain-dairy` | Plain, unflavoured milk, cream, butter, yogurt, kefir, skyr, twaróg and cheese with no ingredient beyond milk, cultures, rennet, salt and enzymes | none_declared |

Not covered by `plain-dairy`: flavoured or sweetened products (fruit yogurts,
desserts), and cheeses that may contain egg lysozyme (e.g. Grana Padano). Those
stay `unknown` until a label is recorded.

## Decisions

The product owner's answers to the open questions of the draft (2026-09-25):

1. **Rice and rice cakes** declare gluten: rice joins `gluten-free-grains`.
2. **Ground spices** declare celery, mustard, gluten and sesame: new rule
   `ground-spices`.
3. **Raw fish and seafood** declare crustaceans and molluscs as traces, and
   shellfish declare fish: new rule `raw-fish-seafood` instead of
   `raw-meat-eggs`.
4. **Seeds** also declare sesame.
5. **Plain dairy** is `none_declared`; flavoured dairy stays `unknown`: new
   rule `plain-dairy`.

The `fresh-produce` and `raw-meat-eggs` rules were approved as drafted.
