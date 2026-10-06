FitMeal takes a recipe someone actually wants to eat and fits it to their calories, protein, allergies, budget and cooking time. It then builds a week around it and writes the shopping list. The interface should feel like a calm kitchen notebook with a precise calculator inside: warm paper, confident numbers, and every change explained.

> **Your favorite food. Your macros. Less waste.**
> *Jedz to, na co masz ochotę — dopasowane do Twojego planu.*

## Principles the UI must show

1. **Numbers are the hero.** Kcal and protein are always visible, set in `numeral` / `numeral-xl` with tabular figures. Never hide a number behind a vague label like "healthy".
2. **Show what changed and why.** Anything FitMeal alters is tinted `paprika-soft` and can be explained with a `ChangeItem` list ("Reduced oil by 8 g — saves 72 kcal").
3. **Allergies are hard walls.** `danger` belongs only to allergies, destructive actions and errors. Options that conflict with an allergy or a strict intolerance are never offered. A recipe that contains one gets a blocking `Notice` naming the ingredient and the allergen, and it is never collapsed or hidden.
4. **Nothing changes until the user confirms.** Transformations, swaps, *I don't have this* and rebalances are proposals. Each change in *Why did FitMeal change this?* and each adjustment in a `RebalanceProposal` can be rejected on its own. Meals marked eaten or skipped are locked.
5. **Value before the paywall.** Show the real result first (`CompareCard`, `LockedPreview`), then ask for the upgrade.
6. **Food, not "AI".** Never lead with AI, sparkles or robots. The product is the plan.
7. **Safe by default.** Adults only (18+). There's a hard floor of 1,200 kcal a day for every target, plan and rebalance. The app makes no medical claims and asks for no medical conditions (see *Safety, privacy and consent*).

## Content fundamentals

- **Voice:** a capable friend who cooks. Plain, specific and brief. Use *you* for the user. FitMeal speaks as *we* only when it did something ("We found a simpler week").
- **Casing:** sentence case everywhere, including buttons and titles. `caption` section labels are the only uppercase.
- **Numbers:** always digits with units: *520 kcal*, *44 g protein*, *12.40 PLN*, *25 min*. Macro shorthand is `44 P · 52 C · 12 F`, always in that order and always after kcal. Use a true minus (−) and an explicit plus (+) in deltas. Put spaces before units. Polish locale: *199,99 zł*, decimal comma.
- **Buttons** are verbs naming the outcome: *Generate week*, *Use turkey breast*, *Adjust dinner −70 kcal*, *Unlock Economy Mode*. Never write *OK*, *Submit* or *Go Premium*.
- **Estimates are labelled** as estimates, with their basis: *Estimated from your plan, this week.* Never promise savings ("Save 200 PLN a month").
- **No medical claims.** Don't use "treat", "cure" or "detox". Sensitive profiles get the disclaimer in `footnote`.
- **No emoji** in UI copy. The one exception is post-meal feedback, which may use a fixed four-face scale.
- **Never moralize food or bodies.** Don't call foods "good" or "bad", don't say "cheat meal", and don't body-shame. Say what changed in numbers.
- **Name:** *FitMeal* is the working title (`docs/branding/NAME_RESEARCH.md`). Keep it set in plain type. No logo or wordmark exists until the Product Owner approves the final name; when that happens, the name, the cover and this book change together.
- **Languages:** Polish is the primary market and English ships from day one. Every string needs a PL version. Check Polish plural forms (1 posiłek, 2 posiłki, 5 posiłków) and allow about 30% extra length.

Real copy to match:

| Where | Copy |
| --- | --- |
| Rebalance | *Your day is 90 kcal over. Rebalance the meal you haven't eaten yet?* · *Dinner, portion −16%, −70 kcal* |
| Calorie floor | *FitMeal doesn't build plans below 1,200 kcal a day. Very low intakes need supervision from a doctor or dietitian.* |
| Allergen block | *Contains peanuts (peanut butter). Peanuts are your allergy. You can save this recipe, but we can't personalize or plan it until peanut butter is swapped or removed.* |
| No plan | *We couldn't build a 7-day plan. Too few breakfasts fit your exclusions and the 15-minute limit.* |
| Import | *Recipe detected · 1 cup cheese — Which cheese?* |
| Import fallback | *We can't read a recipe on this page. Paste the recipe text and we'll keep the link as the source.* |
| Where data lives | *Your profile stays on this phone and syncs to your private iCloud. We receive it only to build a plan or swap, and don't keep it.* |
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
- **Severity:** `danger` marks ALLERGY and allergen-block notices. `warning` marks INTOLERANCE, low-confidence imports, missed targets, plans that can't be built and an allergen check that can't run (no profile on the phone). Import fallbacks (*Paste recipe text*) are `info`. *Don't like* and *Prefer not* stay neutral.
- **Premium:** `premium` on `premium-soft` is for the Premium tier only.
- **Focus:** `focus-ring`, a solid 2px ring offset 2px, at least 5.8:1 on every surface in both themes.

Every text token's usage note names the grounds it passes 4.5:1 on in both themes. Control borders (`line-strong`) and icons meet 3:1.

## Liquid Glass (iOS 26)

FitMeal follows Apple's Liquid Glass design language, in its light and clear form. Content (meals, numbers, recipes) sits on warm solid paper. Navigation and controls float above it as clear glass: half-transparent, lit from the top by a soft sheen, with a crisp 1px rim and barely any shadow. The colour of whatever scrolls underneath glows through. There are two layers and never more.

- **What is glass:** the three-tab bar and its Add button, the bottom accessory, NavBar back and trailing buttons (grouped into one capsule), floating CTAs over a hero or scrolling list, partial-height sheets, context menus and the cooking-mode toolbar.
- **What is never glass:** cards, list groups, ingredient rows, macro visuals and any content. Glass on glass is not allowed. Inside a glass container, controls are plain (`.fm-glass-group .fm-iconbtn`).
- **Recipe:** a `glass-sheen` → transparent gradient (top 55%) over `glass-fill` (controls) or `glass-fill-strong` (sheets and menus), plus a backdrop `blur(glass-blur) saturate(glass-saturation)` (20px, 200%), plus `shadow-glass` (a crisp specular rim, a hairline and a wide, faint float shadow). Tinted glass uses the weaker `glass-sheen-tint`. In SwiftUI, use `.glassEffect()` / `.glassEffect(.regular.tint(...))` inside a `GlassEffectContainer`, and `.buttonStyle(.glass)` / `.glassProminent`.
- **Tints:** `glass-tint-basil` is the one prominent floating action on a screen. `glass-tint-paprika` is only for the Add button. Everything else is untinted, and colour comes from the content underneath.
- **Text on glass** is `ink` or `basil` only, never `ink-muted`. Ink stays at 5:1 or better over every brand fill in both themes. The one tighter case is a large solid light fill directly under dark glass (4.1:1), which the blur softens. The selected tab uses bold `basil` on the `glass-selected` lens: a bright, lifted pill in light and a pressed-in pill in dark (`shadow-lens`). That lens keeps the label at 4.8:1 or better whatever scrolls underneath.
- **Keep it light:** don't raise glass opacity to fix legibility. Move the text off the glass or onto a lens instead. Dims behind sheets use the light `scrim`, so the screen underneath stays visible.
- **Shape:** capsules and circles. All buttons are capsules (`radius-pill`). Floating sheets inset 8px use `radius-sheet` (40), concentric with the iPhone's display corners.
- **Behaviour:** the tab bar shrinks to the active tab plus Add while scrolling down, and the accessory moves inline (`.tabBarMinimizeBehavior(.onScrollDown)`). Glass elements morph into each other when they appear or disappear (`glassEffectID`). A long-press lifts a card and shows a glass menu.
- **Accessibility:** with Reduce Transparency, every glass element becomes solid `surface-raised` (built into `bundle.css` via `prefers-reduced-transparency`). With Increase Contrast, add a `line-strong` edge. With Reduce Motion, glass cross-fades instead of morphing.

## Safety, privacy and consent

- **Adults only.** Onboarding step 2 asks *Are you 18 or older?* with two equal buttons. *I'm under 18* ends onboarding on a kind stop screen, and there is no way around it. No date of birth is stored.
- **Health-data consent (GDPR Art. 9)** has its own screen: a plain explanation, a **separate, unticked** checkbox and a Privacy link. It is never bundled with the terms. *Continue* stays disabled until it's ticked. Its footnote says where the profile lives (next point). This is the only consent in the app. Consent can be withdrawn in Profile › Privacy & health, which leads to account deletion.
- **Where data lives.** Say it the same way everywhere (03, 05, 15, 37b, 38):
  - *On this phone:* the nutrition profile (targets, exclusions with their tiers, optional body data). It syncs through the user's private iCloud, on by default and switchable in Profile; we can't read it. The server receives it with each plan, transform, swap and rebalance request and keeps nothing. The suggested-targets calculator runs on the phone.
  - *On our servers in the EU:* account, plans, meal status, saved and imported recipes, shopping lists, consent records.
  - *Never collected:* medical conditions, date of birth, device or advertising identifiers, PDF files.
  - Never say the profile is "stored in the EU" or "on our servers". Recipe text goes to *our AI provider in the EU*; the profile never goes to AI.
- **No analytics and no device identifiers.** There is no analytics SDK, so there is no analytics consent, toggle or banner anywhere. Don't add one.
- **No marketing.** No marketing email or push at launch, so no marketing opt-in. The only notification is the Thursday *plan next week* reminder, offered on the cooking step (14) through the iOS permission prompt with *Not now*, and managed in Profile › *Plan reminder · Thursdays*.
- **Imports** are private, never feed a public catalog, and send only recipe text: PDFs are read on the phone, link import uses only schema.org recipe data, and shares send only the caption. The import notice sits next to every import action.
- **Health notice:** a neutral `Notice` in onboarding says the app is general planning, not medical advice, and names who should talk to a doctor or dietitian first. It stays available in Profile. The app never asks about or stores medical conditions.
- **1,200 kcal floor:** a refusal, not a warning. `NumberField` shows the error and the reason, *Continue* is disabled, and a suggested value is clamped to 1,200.
- **Allergens:** the checklist is the 14 EU allergens, diet categories, and free text that must be matched to a food and confirmed. An unmatched entry says it can't be enforced. `ExclusionRow` states what each tier does. *Allergy* also excludes derived ingredients and "may contain" traces. An *Intolerance* can be relaxed to *avoid when possible*. Unclear imported ingredients count as possible allergens until clarified. With no profile on the phone, the allergen check can't run: Import Preview is blocked (`warning`), and plans and swaps wait for the profile.
- **Export and deletion** cover both places. *Export my data* combines the profile from this phone with the data from our servers. *Delete account* names what goes: account, plans and private imports on our servers, and the profile on this phone and in iCloud (if iCloud can't be reached, it says the profile may stay there and how to remove it). Consent records are kept only as long as the law requires. It also says the App Store subscription must be cancelled with Apple.

## MVP scope in the UI

The MVP ships Free + Standard, with Premium shown as *Coming soon*. Don't design Phase 2 features into MVP screens:

- **No prices:** no PLN on swaps, recipes or the shopping list, and no *estimated saved*. Economy Mode v1 compares unique ingredients at the same calories and protein.
- **No Pantry Mode:** no "at home" amounts and no *Cook from what I have*.
- **No waste statistics.**
- **Plans:** 3, 5 or 7 days (Free is limited to 3). Meal prep is *cook once for* 1–3 days. Budget is a tier (Economy, Standard or Flexible), with no amount.

These components already support the Phase 2 versions (`Delta` with `PLN`, `ShoppingItem` `pantry` / `price`, premium `LockedPreview`), so the screens can switch them on later.

## Typography

- **Display — Bricolage Grotesque** (700/650): screen titles, meal and recipe names, and every large numeral. It's friendly, a little editorial, and its figures read well big.
- **Text — Figtree** (400–700): everything else. On iOS, ship both as bundled fonts registered with Dynamic Type through `UIFontMetrics`. SF Pro is the fallback.
- **Scale:** `display-xl` 40 (onboarding questions, paywall hero) · `display` 32 (tab roots) · `title-1` 24 (recipe, sheet titles) · `title-2` 19 (cards) · `numeral-xl` 44 · `numeral` 22 · `headline` 17 · `body` 16 · `callout` 15 · `subhead` 14 · `footnote` 13 · `caption` 12 (UPPERCASE, +0.06em) · `micro` 11 (tab labels).
- **Numerals** are always tabular (`font-variant-numeric: tabular-nums`; `.monospacedDigit()` in SwiftUI), so totals don't jitter while rebalancing.
- Use one `display-xl` or `display` per screen. Don't stack two display sizes.

## Space, shape, elevation

- **4 pt grid:** `space-1` 4 … `space-12` 48. The screen gutter is `space-5` (20). Card padding is `space-4` (16). Sections are separated by `space-6` (24).
- **Radii** get softer as things get bigger: `radius-xs` 6 (checkbox) → `radius-sm` 10 (fields) → `radius-md` 14 (options, groups) → `radius-lg` 20 (meal and plan cards) → `radius-xl` 28 (hero bottom, full sheets) → `radius-sheet` 40 (floating sheets). `radius-pill` is for every button, chip, badge, segmented control and glass control.
- **Elevation:** content cards use a `line` border plus a faint `shadow-card`. Only glass gets `shadow-glass`. Full-height sheets sit over `scrim`.
- **Hit targets** are at least `size-tap` (44). Row-level controls make the whole row tappable.

## Layout patterns

- **Onboarding** has 14 steps, each with one question and one sticky primary: welcome, 18+, consent and health notice, goal, body data (optional, *Skip, I'll enter my own*), calories, macros (Simple by default, Advanced opt-in), meals per day, distribution, allergens, diet and other exclusions, preferences, budget, and meal prep with cooking. No account is needed. Step 14 (cooking) also offers the Thursday plan reminder as a card with *Remind me on Thursdays* (the iOS prompt) and *Not now*; it is not a separate step. *Sign in with Apple* is asked when the first plan is generated, as a sheet over the new plan (whether to show the plan first is an open decision in the PRD). The sheet says plans and recipes are kept with the account and the profile stays on this phone; it offers no iCloud choice. Use Apple's own `SignInWithAppleButton` in the app.
- **New phone:** *I already have an account* → Sign in with Apple → 18+ and consent again → **01b Restore profile** from iCloud (the normal path: a summary of calories, protein and exclusions to check, *Restore my profile* / *Set up again*) or, when sync was off or iCloud can't be reached, **01c No profile on this phone** (plans are back; plans, swaps and the import allergen check are paused until the profile is set up in steps 04–14 or restored).
- **Tab roots** (Today, Plan, Shopping) use a `NavBar large` title plus subtitle, the user's `Avatar` at the top right, content scrolling under a floating glass `TabBar` with three tabs, and a separate round Add button that opens Add Recipe. A `BottomAccessory` shows what's next: *Up next · Lunch 13:30* on Today, *Cook today · 2 recipes* on Plan, basket progress on Shopping.
- **Profile** is not a tab. Tapping the `Avatar` opens it as a page sheet over the current tab, with a glass-prominent check (Done) at the top right. It holds stats, targets (calories, exclusions, meal prep), subscription, and Privacy & health: *Nutrition profile · On this phone* (opens *Where your data lives*), *Sync with iCloud*, *Plan reminder · Thursdays* (mirrors the iOS permission, with *Open Settings* when it's off), the health notice, the consent, data export and account deletion.
- **Decisions** (swap meal, swap ingredient, *I don't have this*) open a floating glass sheet (inset 8px, `radius-sheet`). It holds ranked `SwapOption`s with their `Delta`, the effect on the day (*Your day after the swap*), and one primary button naming the result, with *Nothing changes until you confirm*.
- **Rebalance proposal:** after a confirmed swap that leaves the day outside tolerance, a `RebalanceProposal` lists each adjustment (±20% at most) with its own checkbox. Eaten, skipped and earlier meals are shown as locked, and *Keep day as is* is always available. When the target can't be restored, it switches to the unreachable variant.
- **Meal status:** every `MealCard` on Today and Plan can be marked cooked, eaten or skipped in one tap, including offline. Prepped meals show *cook Wed · eat by Thu*.
- **States:** *No plan possible* explains the blocker in plain words and lists concrete changes (never relaxing an allergy). A plan built by relaxing a soft goal says which goal. Offline shows what still works and what needs a connection. All three use `Notice`.
- **Import:** Add recipe offers *Paste link* (recipe pages and blogs), *Choose a PDF* (selectable text, read on the phone), *Paste recipe text* and *Enter manually*, with the import notice next to them. A PDF opens a picker of the recipes found with their pages; each ticked recipe is one import and the picker shows what's left. When a source can't be read (a scanned PDF, a page without recipe data, a site that opts out of text and data mining, an Instagram or TikTok link), an `info` `Notice` offers *Paste recipe text* first and the URL stays as the source. The Share Extension shows the caption it will use and the source URL, which is never opened. The allergen block sits at the top of Import Preview; with no profile on the phone, a `warning` block asks to set it up, and the recipe can still be saved. Unclear lines open a Clarification prompt that blocks planning until answered. *Your version* shows the source's own nutrition figure for comparison only. A missed target is shown as missed, with options. Never lead with AI and never design OCR or link fetching for Instagram or TikTok.
- **Shopping list:** sections follow the backend's store-walk order (vegetables, fruit, meat & fish, dairy & eggs …). Package counts are shown. A checked item that grew shows *+200 g more to buy*.
- **Recipes** open with an edge-to-edge `RecipeHero` (the macro plate) under a glass `NavBar overlay`, then the name, `MacroLine lg`, badges (time, portions, cost, storage), a paprika *Fitted to your lunch · N changes* link, and ingredient rows with changes tinted. The bottom has a glass *Cook* button and a glass-prominent *Mark as cooked*.
- **Cooking mode** shows one big step per screen, with a glass toolbar (previous, *Next step*, timers) and the running timer in a `BottomAccessory`.
- **Motion:** use the standard iOS springs. Totals count up or down over about 250 ms after a rebalance. Glass morphs between states. Respect Reduce Motion.

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
| cloud (iCloud sync) | `icloud` | | |

Icons are single-ink and take the text colour of their row. No emoji or illustrated food icons in the UI chrome. Recipe imagery comes later and never reuses a source's photos.

## Components

The React bundle is `window.FitMeal` (React 18). It is the visual reference for the SwiftUI `DesignSystem` package: each component maps to one SwiftUI view with the same name and props. Groups:

- **Actions:** `Button` (including `glass` / `glass-prominent`), `IconButton` (including `glass`)
- **Inputs:** `Chip`, `SegmentedControl`, `SelectCard`, `Toggle`, `Checkbox`, `NumberField`, `ExclusionRow`, `DistributionEditor`
- **Nutrition:** `MacroRing`, `MacroBar`, `MacroLine`, `Delta`
- **Meals:** `MealCard`, `DayStrip`, `RebalanceProposal`, `StatTile`
- **Recipes:** `RecipeHero`, `IngredientRow`, `SwapOption`, `ChangeItem`, `CompareCard`, `ConfidencePrompt`
- **Shopping:** `ShoppingItem`
- **Status:** `Badge`, `Notice`
- **Monetization:** `PlanCard`, `LockedPreview`
- **Navigation:** `SectionHeader`, `NavBar`, `Avatar`, `OnboardingProgress`, `TabBar`, `BottomAccessory`
- **Layout:** `PhoneFrame`, for showcase pages only

Helper classes in `bundle.css`: `.fm-glass` (the glass material), `.fm-glass-group` (toolbar capsule), `.fm-group` (inset list container), `.fm-changes` (ChangeItem list), `.fm-sheet` / `.fm-scrim` (floating glass sheet), `.fm-sticky` (bottom CTA over a fade), `.fm-cap` (caption label).

## App screens

The **Screens** group lays out the MVP flow of the PRD (after the review decisions) on iPhone frames:

- **Onboarding (01–15):** welcome, restore profile on a new phone (01b) and no profile on this phone (01c), 18+ confirmation and the under-18 stop, consent and health notice (profile on this phone), goal, body data (calculated on the phone), suggested calories and the 1,200 kcal floor, macros, meals and distribution, the 14 EU allergens with severity tiers, diet and free-text exclusions, preferences, budget and meal prep with the plan reminder, and *Sign in with Apple* to save the first plan.
- **Plan and Today (16–19):** create plan (3, 5 or 7 days), weekly plan with cook and eat-by days, Today with meal statuses, and swap meal with its effect on the day.
- **Rebalance and recipe (20–24):** rebalance proposal, the can't-restore case, recipe, *Why did FitMeal change this?* with keep and undo per change, and ingredient swap.
- **Import (25–30):** add recipe with the import notice, PDF recipe picker (25b), fallbacks to *Paste recipe text* for a scanned PDF (25c), a page without recipe data (25d), a site that opts out of text and data mining (25e) and an Instagram or TikTok link (25f), the Share Extension with and without a caption (25g), Import Preview with an allergen block (shared-caption source line), Import Preview with no profile on this phone (26b), clarification prompt, your version with source nutrition, target missed, and *I don't have this*.
- **Plan states (31–33):** no plan possible, a plan with a relaxed goal, and offline.
- **Shopping, paywall and profile (34–38):** shopping list, Economy Mode v1 preview, paywall, Profile with Privacy & health (profile on this phone, iCloud sync, plan reminder, export), *Where your data lives* (37b), and delete account (with the iCloud-not-reachable case).
- A dark-theme set (including 01c, an import fallback, the no-profile block and 37b) and a Liquid Glass page.

Together they cover every step of the MVP Definition of Done.
