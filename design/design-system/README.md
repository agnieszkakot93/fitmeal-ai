FitMeal takes a recipe someone actually wants to eat and fits it to their calories, protein, allergies, budget and cooking time. It then builds a week around it and writes the shopping list. The interface should feel like a calm kitchen notebook with a precise calculator inside: warm paper, confident numbers, and every change explained.

> **Your favorite food. Your macros. Less waste.**
> *Jedz to, na co masz ochotę — dopasowane do Twojego planu.*

## Principles the UI must show

1. **Numbers are the hero.** Kcal and protein are always visible, set in `numeral` / `numeral-xl` with tabular figures. Never hide a number behind a vague label like "healthy".
2. **Show what changed and why.** Anything FitMeal alters is tinted `paprika-soft` and can be explained with a `ChangeItem` list ("Reduced oil by 8 g — saves 72 kcal").
3. **Allergies are hard walls.** `danger` belongs only to allergies, destructive actions and errors. A blocked option stays visible with its reason (`SwapOption blocked`), so people learn why.
4. **The user approves.** Rebalancing, swaps and imports propose a change and wait for a tap (*Adjust dinner −70 kcal*, *Keep as is*). Nothing is applied silently.
5. **Value before the paywall.** Show the real result first (`CompareCard`, `LockedPreview`), then ask for the upgrade.
6. **Food, not "AI".** Never lead with AI, sparkles or robots. The product is the plan.

## Content fundamentals

- **Voice:** a capable friend who cooks. Plain, specific and brief. Use *you* for the user. FitMeal speaks as *we* only when it did something ("We found a simpler week").
- **Casing:** sentence case everywhere, including buttons and titles. `caption` section labels are the only uppercase.
- **Numbers:** always digits with units: *520 kcal*, *44 g protein*, *12.40 PLN*, *25 min*. Macro shorthand is `44 P · 52 C · 12 F`, always in that order and always after kcal. Use a true minus (−) and an explicit plus (+) in deltas. Put spaces before units. Polish locale: *199,99 zł*, decimal comma.
- **Buttons** are verbs naming the outcome: *Generate week*, *Use turkey breast*, *Adjust dinner −70 kcal*, *Unlock Economy Mode*. Never write *OK*, *Submit* or *Go Premium*.
- **Estimates are labelled** as estimates, with their basis: *Estimated from your plan, this week.* Never promise savings ("Save 200 PLN a month").
- **No medical claims.** Don't use "treat", "cure" or "detox". Sensitive profiles get the disclaimer in `footnote`.
- **No emoji** in UI copy. The one exception is post-meal feedback, which may use a fixed four-face scale.

Real copy to match:

| Where | Copy |
| --- | --- |
| Rebalance | *Your day is 70 kcal over. Make dinner 8% smaller to land back on target.* |
| Import | *Recipe detected · 1 cup cheese — Which cheese?* |
| Swap | *Amounts are converted by protein, not 1:1* |
| Paywall | *Economy version found · 34 → 23 unique items · same calories, same protein target* |
| Meal prep | *Cook today: lunch and dinner cover Wed + Thu.* |

## Colour

The palette is basil green, paprika and warm paper, with three macro colours. All colour comes from tokens. There are two themes, `light` (the default) and `dark`.

- **Grounds:** screens sit on `surface`. Cards, sheets and list groups use `surface-raised`. Wells and tracks use `surface-sunken`. Separate them with a `line` hairline, not shadows (`shadow-card` stays faint).
- **Text:** use `ink` for everything that matters and `ink-muted` for units and metadata. `ink-faint` is for disabled text and placeholders only, because it fails 4.5:1 on purpose.
- **Brand:** `basil` is the primary action, the selected state, success and "on target". Text on a basil fill is `on-basil`, which turns dark in the dark theme. Selected fills use `basil-soft` with `basil-ink` text.
- **Accent:** `paprika` means *FitMeal changed this* and *Add*. It covers change tints (`paprika-soft` / `paprika-ink`), the Add tab button and the import CTA. Text on a paprika fill is always `on-paprika`, never white. Paprika is never used for errors.
- **Macros:** `macro-protein` (terracotta), `macro-carbs` (amber) and `macro-fat` (blue), on a `macro-track`. Carbs is the lightest and protein the darkest in light mode. Fat is blue, so no pair relies on a red–green split. A macro colour never appears without its letter or word (P / C / F).
- **Severity:** `danger` marks ALLERGY, `warning` marks INTOLERANCE and low-confidence imports, and *Don't like* / *Prefer not* stay neutral.
- **Premium:** `premium` on `premium-soft` is for the Premium tier only.
- **Focus:** `focus-ring`, a solid 2px ring offset 2px, at least 5.8:1 on every surface in both themes.

Every text token's usage note names the grounds it passes 4.5:1 on in both themes. Control borders (`line-strong`) and icons meet 3:1.

## Typography

- **Display — Bricolage Grotesque** (700/650): screen titles, meal and recipe names, and every large numeral. It's friendly, a little editorial, and its figures read well big.
- **Text — Figtree** (400–700): everything else. On iOS, ship both as bundled fonts registered with Dynamic Type through `UIFontMetrics`. SF Pro is the fallback.
- **Scale:** `display-xl` 40 (onboarding questions, paywall hero) · `display` 32 (tab roots) · `title-1` 24 (recipe, sheet titles) · `title-2` 19 (cards) · `numeral-xl` 44 · `numeral` 22 · `headline` 17 · `body` 16 · `callout` 15 · `subhead` 14 · `footnote` 13 · `caption` 12 (UPPERCASE, +0.06em) · `micro` 11 (tab labels).
- **Numerals** are always tabular (`font-variant-numeric: tabular-nums`; `.monospacedDigit()` in SwiftUI), so totals don't jitter while rebalancing.
- Use one `display-xl` or `display` per screen. Don't stack two display sizes.

## Space, shape, elevation

- **4 pt grid:** `space-1` 4 … `space-12` 48. The screen gutter is `space-5` (20). Card padding is `space-4` (16). Sections are separated by `space-6` (24).
- **Radii** get softer as things get bigger: `radius-xs` 6 (checkbox) → `radius-sm` 10 (fields, segments) → `radius-md` 14 (buttons, options, groups) → `radius-lg` 20 (meal and plan cards) → `radius-xl` 28 (sheets). Pills (`radius-pill`) are for chips, badges and day pills.
- **Elevation:** cards use a `line` border plus a faint `shadow-card`. Only bottom sheets and the sticky CTA get `shadow-sheet`. Sheets sit over `scrim`.
- **Hit targets** are at least `size-tap` (44). Row-level controls make the whole row tappable.

## Layout patterns

- **Tab roots** (Today, Plan, Shopping, Profile) use a `NavBar large` title plus subtitle, scrolling content and the `TabBar`. Add is a paprika button that opens the Add Recipe screen.
- **Onboarding** uses `OnboardingProgress` (11 steps), one `display-xl` question, options as `SelectCard` / `SegmentedControl` / `Chip`, and one sticky primary *Continue*. Simple mode is the default and Advanced is opt-in.
- **Decisions** (swap meal, swap ingredient, *I don't have this*) open a bottom sheet with ranked `SwapOption`s, each showing its `Delta`, and one primary button naming the result.
- **Recipes** show the name, `MacroLine lg`, badges (time, portions, cost, storage), a paprika *Fitted to your lunch — N changes. Why?* link, and ingredient rows with changes tinted.
- **Motion:** use the standard iOS springs. Totals count up or down over about 250 ms after a rebalance. Respect Reduce Motion.

## Iconography

The iOS app uses **SF Symbols** (regular weight, 22 pt in rows, 24 pt in the tab bar). The `Icon` component is a matching 24px line set (1.75 stroke, round caps) for web previews and Android parity. Name mapping:

| Icon | SF Symbol | Icon | SF Symbol |
| --- | --- | --- | --- |
| today | `sun.max` | swap | `arrow.left.arrow.right` |
| plan | `calendar` | repeat (meal prep) | `arrow.2.squarepath` |
| plus (Add) | `plus` | lock | `lock` |
| cart | `bag` | fridge (pantry) | `refrigerator` |
| user | `person` | box (package) | `shippingbox` |
| flame | `flame` | alert | `exclamationmark.triangle` |
| clock | `clock` | leaf (waste) | `leaf` |
| target | `scope` | wallet (budget) | `creditcard` |

Icons are single-ink and take the text colour of their row. No emoji or illustrated food icons in the UI chrome. Recipe imagery comes later and never reuses a source's photos.

## Components

The React bundle is `window.FitMeal` (React 18). It is the visual reference for the SwiftUI `DesignSystem` package: each component maps to one SwiftUI view with the same name and props. Groups:

- **Actions:** `Button`, `IconButton`
- **Inputs:** `Chip`, `SegmentedControl`, `SelectCard`, `Toggle`, `Checkbox`, `NumberField`, `ExclusionRow`, `DistributionEditor`
- **Nutrition:** `MacroRing`, `MacroBar`, `MacroLine`, `Delta`
- **Meals:** `MealCard`, `DayStrip`, `RebalanceBanner`, `StatTile`
- **Recipes:** `IngredientRow`, `SwapOption`, `ChangeItem`, `CompareCard`, `ConfidencePrompt`
- **Shopping:** `ShoppingItem`
- **Status:** `Badge`
- **Monetization:** `PlanCard`, `LockedPreview`
- **Navigation:** `SectionHeader`, `NavBar`, `OnboardingProgress`, `TabBar`
- **Layout:** `PhoneFrame`, for showcase pages only

Helper classes in `bundle.css`: `.fm-group` (inset list container), `.fm-changes` (ChangeItem list), `.fm-sheet` / `.fm-scrim` (bottom sheet), `.fm-sticky` (bottom CTA), `.fm-cap` (caption label).

## App screens

The **Screens** group lays out the MVP flow from the PRD on iPhone frames: onboarding (Welcome → Goal → Calories → Macros → Meals and distribution → Exclusions → Preferences → Cooking and budget), Create plan, Weekly plan, Today, Swap meal, Rebalance, Recipe, *Why did FitMeal change this?*, Ingredient swap, Add recipe, Import preview, Your version, *I don't have this*, Shopping list, Economy Mode preview, Paywall, Profile, and a dark-theme set. Together they cover all 12 steps of the MVP Definition of Done.
