# Onboarding (web, first sprint of the client)

Platform: mobile-first responsive web / PWA (see README §Platform). "Browser (profile)" and "Browser (app state)" are defined in README §Where data lives; the accessibility baseline (WCAG 2.2 AA) in README applies to every step and is not repeated.

## Problem and requirement

A new user must get from install to a first plan with as little friction as possible, while Donut stays safe (18+, 1200 kcal floor, no medical claims) and lawful (separate GDPR Art. 9 consent). Serves PRD §6 (MVP onboarding), §7, §12.1, §12.2, §14 DoD step 1–3, and DEVELOPMENT_PLAN §7.1, D8, D9, S4.

Principles applied: Simple by default (every step after Consent has a pre-selected or skippable default, Advanced macros are opt-in), allergies are sacred (their own step, never collapsed, tiers explained), no account before value (Sign in with Apple only when the plan exists), the profile stays in the browser (IndexedDB, no server copy).

## Flow

1. **01 Welcome** → *Get started* (or *I already have an account* → restore path, see README map).
2. **02 Age confirmation** → *I'm 18 or older* → 03. *I'm under 18* → 02b stop (no way around).
3. **03 Consent & health notice** → tick the health-data box → *Continue*. Without it there is no path forward (only *Close Donut* info, see edge cases).
4. **04 Goal** → **05 Body data** (optional, with *Skip, I'll enter my own* as a first-class action; also shown after *Custom target*) → **06 Calories** → **07 Macros** → **08 Meals per day** → **09 Distribution** → **10 Allergies** → **11 Restrictions** → **12 Preferences** → **13 Budget** → **14 Meal prep & cooking** (with plan reminder card) → *Build my plan*.
5. **16 Create plan** (weekly-plan.md) → generation → **15 Sign in with Apple** sheet over the new plan → Today.

`OnboardingProgress` shows `step` / `total = 14` on screens 02–14. Welcome has no progress bar; Sign-in is not a numbered step.

States across onboarding:
- **Loading:** none; everything up to step 14 runs in the browser (suggested targets are calculated locally). Only free-text matching (step 11), Create plan and Sign-in call the server.
- **Offline:** steps 01–14 work fully offline. Create plan shows `state.offline.action.generate`; answers are kept.
- **Error:** only inline validation; server errors appear from Create plan onwards.
- **Resume:** on reload or a return visit, reopen at the last completed step with answers kept (Browser (app state) + Browser (profile)). Steps 02–03 must be complete before anything is written to the profile. Each step has its own URL (`/onboarding/<step>`); deep-linking past an incomplete required step redirects back to it.
- **Storage unavailable** (private window, blocked IndexedDB): stop at 03 with `data.no_storage` (README).

## Responsive layout

- `sm`: full-width column, gutter `space-5`, sticky primary at the bottom (`.fm-sticky`) with `scroll-padding-bottom` so focused fields are never hidden behind it.
- `md` / `lg`: one centred card (max 560 px, `surface-raised`, `radius-xl`) on `surface`; primary button at the end of the form, not sticky; `OnboardingProgress` above the card.
- Each question is a `<form>` with one `<fieldset>`/`<legend>` (the question) so Enter submits the step when valid.

## Shared layout

Every step 02–14: `NavBar` (inline, no title) with `OnboardingProgress` back button and bar; one question in `display-xl` (single display size per screen); optional one-line explanation in `body` `ink-muted`; the answer controls; a sticky primary `Button` (`.fm-sticky`, glass-prominent basil) at the bottom with content scrolling under a fade. Gutter `space-5`, sections `space-6`.

---

## 01 Welcome

**Purpose:** say what Donut does in one line and start without an account.

**Layout:** `surface` ground; brand line in `display-xl` (*Your favourite food. Your macros.*); `body` subline; three short value rows (icon + `callout`): import any recipe, fit to your calories and protein, plan and shop for the week. Primary `Button` *Get started*. Secondary text `Button` *I already have an account*. Language follows the browser (`navigator.language`); a small PL / EN switch sits in the footer of Welcome only.

**Fields:** none. **Stored:** nothing. **Metric:** not measured (installs come from App Store Connect).

**Accessibility:** value rows are a `<ul>`; icons `aria-hidden`. `<h1>` is the brand line. Both buttons ≥ 44 px and stack vertically on `sm`.

**Edge cases:** returning user with a profile in this browser never sees Welcome; `/` redirects to `/today`.

| Key | EN | PL |
|---|---|---|
| `onb.welcome.title` | Your favourite food. Your macros. | Twoje ulubione jedzenie. Twoje makro. |
| `onb.welcome.subtitle` | Bring any recipe. Donut fits it to your calories, protein, allergies and week. | Dodaj dowolny przepis. Donut dopasuje go do Twoich kalorii, białka, alergii i tygodnia. |
| `onb.welcome.point1` | Import recipes from links, PDFs or text | Importuj przepisy z linków, PDF-ów lub tekstu |
| `onb.welcome.point2` | Every meal fitted to your targets | Każdy posiłek dopasowany do Twoich celów |
| `onb.welcome.point3` | A weekly plan and shopping list | Plan na tydzień i lista zakupów |
| `onb.welcome.cta` | Get started | Zaczynamy |
| `onb.welcome.have_account` | I already have an account | Mam już konto |

---

## 02 Age confirmation (2/14)

**Purpose:** confirm 18+ (PRD §7, §12.1). No date of birth.

**Layout:** question *Are you 18 or older?*; `body`: *Donut is designed for adults.*; two **equal** `Button`s (same style, secondary, stacked full width): *I'm 18 or older*, *I'm under 18*. No sticky primary on this screen (the two answers are the actions). No default.

**Fields:** `age_18_plus: bool`. **Stored:** Browser (app state) as a pending consent `{type: age_18_plus, version, granted: true, answered_at}`; sent to Server (consent record) after sign-in. A *No* is not stored anywhere.

**02b Under-18 stop:** `display` title *Donut is for adults*; body explains kindly; no buttons except *Back* (in case of a mis-tap, returns to 02). No link to continue, no "ask a parent".

**Metric:** server `age_18_plus` consent records (after sign-in). Under-18 stops are not measured.

**Accessibility:** both buttons have the same style, size and DOM order; the question is the `<h1>`. On 02b, focus moves to its `<h1>`.

**Edge cases:** an age under 18 entered later in Body data shows 02b and clears the pending answers. On a new browser or device, 02 is asked again after sign-in (DEVELOPMENT_PLAN §7.1). Editing the URL cannot skip 02b: the stop state is kept in Browser (app state) for the session.

| Key | EN | PL |
|---|---|---|
| `onb.age.title` | Are you 18 or older? | Czy masz ukończone 18 lat? |
| `onb.age.body` | Donut is designed for adults. | Donut jest przeznaczony dla osób dorosłych. |
| `onb.age.yes` | I'm 18 or older | Mam 18 lat lub więcej |
| `onb.age.no` | I'm under 18 | Mam mniej niż 18 lat |
| `onb.age.stop.title` | Donut is for adults | Donut jest dla dorosłych |
| `onb.age.stop.body` | Nutrition needs change a lot while you're still growing, so Donut doesn't plan meals for people under 18. A doctor or dietitian can help you plan what's right for you. | W okresie dorastania potrzeby żywieniowe szybko się zmieniają, dlatego Donut nie układa planów dla osób poniżej 18 lat. Lekarz lub dietetyk pomoże dobrać to, co dla Ciebie najlepsze. |
| `onb.age.stop.back` | Back | Wróć |

---

## 03 Consent & health notice (3/14)

**Purpose:** explicit, separate, unticked Art. 9 consent; general health notice; where data lives (PRD §7, §12.2, DEVELOPMENT_PLAN §7.1).

**Layout (top to bottom):**
1. Title *Your health data*.
2. `body`: what counts as health data and why we need it.
3. `Checkbox` (unticked, full-row tap target) with the consent sentence. Link *Privacy policy* below it (opens in a new tab, `rel="noopener"`, announced as *opens in a new tab*).
4. `footnote` with `data.where` and `data.loss_warning` (README): the profile is saved in this browser, and clearing site data or switching device loses it.
5. `Notice tone="offline"` (neutral) *Not medical advice* with the health notice body and the list of who should talk to a doctor or dietitian first, as `items`.
6. Sticky *Continue*, **disabled until the checkbox is ticked**.

Never bundle terms of use here. Never pre-tick.

**Fields:** `health_data: bool` (must be true to continue). **Stored:** pending consent in Browser (app state) `{type: health_data, version: <consent text version>, granted: true, answered_at}`; POSTed after sign-in to Server (consent record). The health notice is not a consent and isn't recorded.

**Metric:** server `health_data` consent records = "profile started" proxy (PRD §4 Activation: profile completed). 

**Accessibility:** native `<input type="checkbox">` with the full consent sentence as its `<label>` (whole row clickable, Space toggles). *Continue* uses `aria-disabled` with `aria-describedby` → *Tick the consent above to continue*. Notice items are a `<ul>`.

**Edge cases:** user unticks after going back → steps 04+ stay reachable only after re-ticking; the profile already in the browser is kept but nothing is sent. User refuses → they stay here; a quiet line explains Donut can't build a personalised profile without it (no dark pattern, no nagging). Consent withdrawal later lives in Profile (leads to account deletion, specified later).

| Key | EN | PL |
|---|---|---|
| `onb.consent.title` | Your health data | Twoje dane o zdrowiu |
| `onb.consent.body` | To fit meals to you, Donut uses your allergies, intolerances, calorie and macro goals and, if you add it, your body data. The law treats this as health data, so we need your explicit consent. | Aby dopasować posiłki, Donut korzysta z Twoich alergii, nietolerancji, celów kalorycznych i makro oraz – jeśli je podasz – danych o ciele. Prawo traktuje je jako dane o zdrowiu, dlatego potrzebujemy Twojej wyraźnej zgody. |
| `onb.consent.checkbox` | I agree that Donut processes my health data (allergies, intolerances, body data and goals) to build my plans and recipes. | Wyrażam zgodę na przetwarzanie przez Donut moich danych o zdrowiu (alergie, nietolerancje, dane o ciele i cele) w celu układania planów i przepisów. |
| `onb.consent.where` | = `data.where` (README) | = `data.where` (README) |
| `onb.consent.loss` | = `data.loss_warning` (README) | = `data.loss_warning` (README) |
| `onb.consent.privacy_link` | Privacy policy | Polityka prywatności |
| `onb.consent.refused` | Without this consent Donut can't build a personal profile. You can change your mind anytime. | Bez tej zgody Donut nie może utworzyć Twojego profilu. W każdej chwili możesz zmienić zdanie. |
| `onb.health.title` | Not medical advice | To nie jest porada medyczna |
| `onb.health.body` | Donut gives general nutrition planning. Talk to a doctor or registered dietitian before using it if you: | Donut pomaga w ogólnym planowaniu posiłków. Zanim zaczniesz, skonsultuj się z lekarzem lub dietetykiem, jeśli: |
| `onb.health.item1` | are pregnant or breastfeeding | jesteś w ciąży lub karmisz piersią |
| `onb.health.item2` | have or have had an eating disorder | masz lub miałeś/-aś zaburzenia odżywiania |
| `onb.health.item3` | have kidney disease, diabetes or another medical condition | chorujesz na nerki, cukrzycę lub inną chorobę |
| `onb.health.item4` | follow a medically prescribed diet | stosujesz dietę zaleconą przez lekarza |
| `onb.health.footer` | Donut doesn't ask about or store any of these. | Donut nie pyta o te informacje i ich nie zapisuje. |
| `onb.consent.cta` | Continue | Dalej |
| `onb.consent.cta_hint_a11y` | Tick the consent above to continue | Zaznacz zgodę powyżej, aby przejść dalej |

Note: `onb.health.item2` uses the split form *miałeś/-aś*; see README open question 9. Alternative without gender: *masz lub w przeszłości występowały u Ciebie zaburzenia odżywiania*.

---

## 04 Goal (4/14)

**Purpose:** pick the direction that drives suggested targets.

**Layout:** title *What's your goal?*; four `SelectCard`s (single choice), *Custom target* last as the escape option. *Continue* enabled once a card is chosen; **default: Maintain** pre-selected (Simple by default).

| Option | Value | Description (what Donut does) |
|---|---|---|
| Lose fat | `cut` | We'll suggest about 500 kcal under your maintenance. |
| Maintain | `maintain` | We'll suggest your maintenance calories. |
| Build muscle | `bulk` | We'll suggest about 300 kcal over maintenance. |
| Custom target | `custom` | Enter your own calories and macros. |

**Stored:** Browser (profile) `goal`. **Metric:** not measured.

**Accessibility:** `SelectCard`s are native radio inputs in a `<fieldset>` (arrow keys move the choice); description linked via `aria-describedby`.

**Edge cases:** *Custom target* still goes through Body data (skippable) so the flow is linear; Calories then has no suggestion. Copy never says "lose weight" or comments on bodies.

| Key | EN | PL |
|---|---|---|
| `onb.goal.title` | What's your goal? | Jaki jest Twój cel? |
| `onb.goal.cut` | Lose fat | Redukcja tkanki tłuszczowej |
| `onb.goal.cut.desc` | We'll suggest about 500 kcal under your maintenance. | Zaproponujemy ok. 500 kcal poniżej Twojego zapotrzebowania. |
| `onb.goal.maintain` | Maintain | Utrzymanie |
| `onb.goal.maintain.desc` | We'll suggest your maintenance calories. | Zaproponujemy kalorie na poziomie Twojego zapotrzebowania. |
| `onb.goal.bulk` | Build muscle | Budowa masy mięśniowej |
| `onb.goal.bulk.desc` | We'll suggest about 300 kcal over maintenance. | Zaproponujemy ok. 300 kcal powyżej zapotrzebowania. |
| `onb.goal.custom` | Custom target | Własny cel |
| `onb.goal.custom.desc` | Enter your own calories and macros. | Wpisz własne kalorie i makroskładniki. |

---

## 05 Body data, optional (5/14)

**Purpose:** let the browser suggest calories and protein (PRD §7). Fully optional.

**Layout:** title *Want us to suggest your targets?*; `body`: *Calculated on this device. Skip if you already know your numbers.* Fields: `NumberField` age (*years*), `SegmentedControl` sex, `NumberField` weight (*kg*), `NumberField` height (*cm*), activity as five compact `SelectCard`s. Sticky primary *Calculate my targets*; secondary text button **above** it *Skip, I'll enter my own* (equal visibility, not hidden).

**Fields and validation:**

| Field | Range | Notes |
|---|---|---|
| Age | 18–100, integer | < 18 → 02b stop (PRD §7). > 100 → inline error. Not stored as a date. |
| Sex | Female · Male · Prefer not to say | *Prefer not to say* disables *Calculate* with hint *We need this for the calculation. You can skip and enter targets yourself.* (README open question 14) |
| Weight | 35–300 kg, one decimal | |
| Height | 120–230 cm, integer | |
| Activity | Mostly sitting · Lightly active · Active · Very active · Athlete | multipliers 1.2 / 1.375 / 1.55 / 1.725 / 1.9 |

Calculation (client-side in the browser, never on the server; `mobile-architect` owns the implementation): Mifflin-St Jeor × activity = maintenance; goal adjustment −500 / 0 / +300 kcal; **clamped to at least 1200**. Protein suggestion: 1.6 g/kg (cut and bulk) or 1.2 g/kg (maintain), rounded to 5 g. Results pre-fill 06 and 07 and are marked `suggested` in the profile.

**Stored:** Browser (profile) `body: {age, sex, weight_kg, height_cm, activity}` and `targets.source = suggested`. Never sent to the server (the snapshot only carries targets and exclusions).

**Metric:** not measured.

**Accessibility:** every `NumberField` is `<input inputmode="decimal|numeric">` with the unit in the accessible name (*Weight, kilograms*) and `autocomplete="off"`; errors shown on blur and on submit, linked by `aria-describedby`. Sex is a radio group; `SegmentedControl` wraps to a vertical list when it doesn't fit (narrow widths, 200% zoom).

**Edge cases:** partially filled form + *Skip* → body data discarded, nothing kept. Editing body data later in Profile re-suggests but never overwrites a user-entered target without asking.

| Key | EN | PL |
|---|---|---|
| `onb.body.title` | Want us to suggest your targets? | Zaproponować Ci cele? |
| `onb.body.subtitle` | Calculated on this phone. Skip if you already know your numbers. | Liczymy to na tym urządzeniu. Pomiń, jeśli znasz już swoje liczby. |
| `onb.body.age` | Age | Wiek |
| `onb.body.age.unit` | years | lat |
| `onb.body.age.error_max` | Enter an age up to 100. | Wpisz wiek do 100 lat. |
| `onb.body.sex` | Sex for the calculation | Płeć do obliczeń |
| `onb.body.sex.female` | Female | Kobieta |
| `onb.body.sex.male` | Male | Mężczyzna |
| `onb.body.sex.none` | Prefer not to say | Wolę nie podawać |
| `onb.body.sex.none_hint` | We need this for the calculation. You can skip and enter targets yourself. | Potrzebujemy tego do obliczeń. Możesz pominąć ten krok i wpisać cele samodzielnie. |
| `onb.body.weight` | Weight | Masa ciała |
| `onb.body.weight.error` | Enter a weight between 35 and 300 kg. | Wpisz wartość od 35 do 300 kg. |
| `onb.body.height` | Height | Wzrost |
| `onb.body.height.error` | Enter a height between 120 and 230 cm. | Wpisz wartość od 120 do 230 cm. |
| `onb.body.activity` | How active are you? | Jak bardzo jesteś aktywny/-a? |
| `onb.body.activity.1` | Mostly sitting | Głównie siedzę |
| `onb.body.activity.2` | Lightly active | Lekka aktywność |
| `onb.body.activity.3` | Active | Średnia aktywność |
| `onb.body.activity.4` | Very active | Duża aktywność |
| `onb.body.activity.5` | Athlete | Sport wyczynowy |
| `onb.body.cta` | Calculate my targets | Oblicz moje cele |
| `onb.body.skip` | Skip, I'll enter my own | Pomiń, wpiszę samodzielnie |

PL `onb.body.activity` alternative without gender: *Ile ruchu masz na co dzień?* (preferred, see open question 9).

---

## 06 Calories (6/14)

**Purpose:** set the daily kcal target; enforce the 1200 floor as a refusal (PRD §7, §12.1).

**Layout:** title *Your daily calories*; `NumberField large` with unit *kcal*, centred `numeral-xl`; hint under it. Sticky *Continue*.

**Validation:** integer, **1200–5000 kcal**. Below 1200 → `NumberField error` with the floor reason, *Continue* disabled. Above 5000 → error *Enter up to 5000 kcal.* Empty → *Continue* disabled. A suggested value below 1200 is pre-filled as 1200 and the hint says so.

**Stored:** Browser (profile) `targets.daily_kcal`, `targets.daily_kcal_source` (`suggested` / `user`). Maps to planner `Profile.daily_kcal` (≥ `KCAL_FLOOR` 1200).

**Metric:** not measured.

**Accessibility:** field label *Daily calories, kilocalories*; the error is read immediately (live region) when the value goes below 1200; the floor message is text, not colour only.

**Edge cases:** pasting non-digits strips them; leading zeros ignored; the field never auto-raises a typed value; user must fix it.

| Key | EN | PL |
|---|---|---|
| `onb.kcal.title` | Your daily calories | Twoje dzienne kalorie |
| `onb.kcal.hint.suggested` | Suggested from your body data. Change it anytime. | Propozycja na podstawie Twoich danych. Możesz ją zmienić w każdej chwili. |
| `onb.kcal.hint.clamped` | We set this to 1200 kcal, the lowest target Donut plans for. | Ustawiliśmy 1200 kcal – najniższy cel, dla którego Donut układa plany. |
| `onb.kcal.hint.manual` | Enter the number you're aiming for. | Wpisz liczbę, do której dążysz. |
| `onb.kcal.floor_error` | Donut doesn't build plans below 1,200 kcal a day. Very low intakes need supervision from a doctor or dietitian. | Donut nie układa planów poniżej 1200 kcal dziennie. Bardzo niska podaż energii wymaga opieki lekarza lub dietetyka. |
| `onb.kcal.max_error` | Enter up to 5,000 kcal. | Wpisz maksymalnie 5000 kcal. |
| `onb.kcal.a11y_label` | Daily calories, kilocalories | Dzienne kalorie, kilokalorie |

---

## 07 Macros: Simple / Advanced (7/14)

**Purpose:** set protein (hard minimum for the planner) and soft fat/carb targets (PRD §7, §8.5).

**Layout:** title *How do you want to split it?*; `SegmentedControl` *Simple* (default) / *Advanced*.

**Simple:** four `SelectCard`s with `meta` showing grams at the chosen kcal (e.g. *115 g protein*). Default **Standard**, or the body-data protein suggestion if present (shown as a hint *Protein suggested from your body data*).

| Preset | P / C / F share of kcal | Protein |
|---|---|---|
| Standard | 20 / 50 / 30 | minimum |
| Balanced | 25 / 45 / 30 | minimum |
| High protein | 30 / 40 / 30 | minimum |
| Lower carb | 30 / 25 / 45 | minimum |

(Pending dietitian sign-off, README open question 10.) Grams = share × kcal ÷ 4 (P, C) or ÷ 9 (F), rounded to 5 g.

**Advanced:** three `NumberField`s (*g*): Protein with a `Toggle` *Treat as minimum* (on by default), Fat, Carbs. Under them a `MacroLine` and a live line *These add up to 1,480 kcal* with a `Delta` vs the calorie target.

**Validation (Advanced):** protein 0–400 g, fat 0–300 g, carbs 0–800 g, integers. Implied energy (4P + 4C + 9F) **below 1200 kcal → refused** with the floor message, *Continue* disabled. If implied energy differs from the calorie target by more than 5%, show a `Notice tone="warning"` (not blocking) with two actions: *Use 1,480 kcal as my target* or *Keep 1,500 kcal* (then fat and carbs are soft targets and the planner fits calories first).

**Stored:** Browser (profile) `macros.mode` (`simple`/`advanced`), `macros.preset`, `protein_g`, `protein_is_min`, `fat_g`, `carbs_g`. Planner receives `protein_min_g` (backend requires ≥ 0). If *Treat as minimum* is off, protein is still sent as the minimum (the planner only supports a minimum) and the app says so in the hint.

**Metric:** not measured (README open question 8).

**Accessibility:** presets read *High protein, 115 grams protein, minimum*. The implied-kcal line is a live region, announced after editing stops.

**Edge cases:** switching Simple → Advanced pre-fills Advanced with the preset's grams; switching back keeps the Advanced numbers in memory until onboarding ends. Changing kcal on 06 afterwards recalculates Simple grams but never Advanced ones (shows the mismatch notice instead).

| Key | EN | PL |
|---|---|---|
| `onb.macros.title` | How do you want to split it? | Jak chcesz rozłożyć makro? |
| `onb.macros.simple` | Simple | Prosto |
| `onb.macros.advanced` | Advanced | Zaawansowane |
| `onb.macros.standard` | Standard | Standardowo |
| `onb.macros.balanced` | Balanced | Zrównoważone |
| `onb.macros.high_protein` | High protein | Dużo białka |
| `onb.macros.lower_carb` | Lower carb | Mniej węglowodanów |
| `onb.macros.meta_protein` | {g} g protein | {g} g białka |
| `onb.macros.protein` | Protein | Białko |
| `onb.macros.fat` | Fat | Tłuszcz |
| `onb.macros.carbs` | Carbs | Węglowodany |
| `onb.macros.protein_min` | Treat as minimum | Traktuj jako minimum |
| `onb.macros.protein_min_off_hint` | Donut plans protein as a minimum, so meals may have a little more. | Donut planuje białko jako minimum, więc posiłki mogą mieć go trochę więcej. |
| `onb.macros.implied` | These add up to {kcal} kcal | To razem {kcal} kcal |
| `onb.macros.mismatch.title` | Your macros and calories don't match | Makro i kalorie się nie zgadzają |
| `onb.macros.mismatch.use` | Use {kcal} kcal as my target | Ustaw {kcal} kcal jako cel |
| `onb.macros.mismatch.keep` | Keep {kcal} kcal | Zostaw {kcal} kcal |
| `onb.macros.floor_error` | These add up to less than 1,200 kcal a day. Donut doesn't build plans below that; very low intakes need supervision from a doctor or dietitian. | To razem mniej niż 1200 kcal dziennie. Donut nie układa planów poniżej tej wartości; bardzo niska podaż energii wymaga opieki lekarza lub dietetyka. |

---

## 08 Meals per day (8/14)

**Purpose:** number of meal slots (planner: 2–5 meals, unique names).

**Layout:** title *How many meals a day?*; four `SelectCard`s *2*, *3*, *4*, *5* with the slot names as description. **Default 3.**

| Count | Slots (name → `meal_type`) |
|---|---|
| 2 | Breakfast → breakfast · Dinner → dinner |
| 3 | Breakfast · Lunch · Dinner |
| 4 | Breakfast · Lunch · Snack → snack · Dinner |
| 5 | Breakfast · Snack 1 · Lunch · Snack 2 · Dinner |

"Lunch" is the main midday meal (PL *Obiad*), "Dinner" the evening meal (PL *Kolacja*), matching Polish eating habits.

**Stored:** Browser (profile) `meals[] {name, meal_type}`. **Metric:** not measured.

**Accessibility:** cards read *3 meals: breakfast, lunch, dinner*. Plural forms in PL.

| Key | EN | PL |
|---|---|---|
| `onb.meals.title` | How many meals a day? | Ile posiłków dziennie? |
| `onb.meals.count` | {n, plural, one {# meal} other {# meals}} | {n, plural, one {# posiłek} few {# posiłki} many {# posiłków} other {# posiłku}} |
| `meal.breakfast` | Breakfast | Śniadanie |
| `meal.lunch` | Lunch | Obiad |
| `meal.dinner` | Dinner | Kolacja |
| `meal.snack` | Snack | Przekąska |
| `meal.snack_n` | Snack {n} | Przekąska {n} |

---

## 09 Meal calorie distribution (9/14)

**Purpose:** each slot's share of daily kcal (planner: every share > 0, sum = 100% ± 1).

**Layout:** title *How should your calories split?*; `SegmentedControl` or `Chip` row of presets *Even* (default), *Large breakfast*, *Large lunch*, *Large dinner*, *Custom*; `DistributionEditor` with `kcal` = target and per-meal steppers (1% steps, last meal absorbs the difference); under each meal its kcal (*555 kcal*).

Presets (3 meals; other counts scale the same way, snacks fixed at 10% each when present):

| Preset | Breakfast / Lunch / Dinner |
|---|---|
| Even | 34 / 33 / 33 |
| Large breakfast | 40 / 30 / 30 |
| Large lunch | 30 / 40 / 30 |
| Large dinner | 30 / 30 / 40 |

Touching a stepper switches the preset to *Custom*.

**Validation:** each meal 5–70%; total 100% enforced by the editor. Any meal below 5% → stepper stops. *Continue* always enabled (the editor can't produce an invalid total).

**Stored:** Browser (profile) `meals[].kcal_share` (0–1). **Metric:** not measured.

**Accessibility:** each stepper is `<input type="number">` (or `role="spinbutton"`) with `aria-valuetext` *34 percent, 510 kilocalories*, labelled *Breakfast*; − / + buttons ≥ 44 px with names *Decrease breakfast* / *Increase breakfast*; arrow keys step 1%. The stacked bar is `aria-hidden` (steppers carry the numbers). The running total is a polite live region.

| Key | EN | PL |
|---|---|---|
| `onb.dist.title` | How should your calories split? | Jak rozłożyć kalorie w ciągu dnia? |
| `onb.dist.even` | Even | Równo |
| `onb.dist.big_breakfast` | Large breakfast | Duże śniadanie |
| `onb.dist.big_lunch` | Large lunch | Duży obiad |
| `onb.dist.big_dinner` | Large dinner | Duża kolacja |
| `onb.dist.custom` | Custom | Własny podział |
| `onb.dist.min_reached` | Each meal needs at least 5%. | Każdy posiłek musi mieć co najmniej 5%. |

---

## 10 Allergies (10/14)

**Purpose:** the 14 EU allergens with a severity tier each (PRD §7). Safety-critical.

**Layout:** title *Any allergies or intolerances?*; `body`: *Pick a level for anything you avoid. Allergies are never planned, including traces.* A tier legend (four `Badge`s with one-line meaning, always visible, not in a tooltip). Then 14 `ExclusionRow`s in the PRD order: cereals containing gluten, crustaceans, eggs, fish, peanuts, soybeans, milk, tree nuts, celery, mustard, sesame, sulphites, lupin, molluscs. Each row shows `examples` and four tier chips. Rows with *Intolerance* show `Toggle` *Avoid when possible*, off by default. Sticky *Continue* (label *I have none* while nothing is selected, then *Continue*).

**Fields:** per allergen `severity ∈ {allergy, intolerance, dislike, prefer_not, none}`, `relaxed` (intolerance only). Backend categories: `gluten, crustaceans, eggs, fish, peanuts, soy, milk, tree_nuts, celery, mustard, sesame, sulphites, lupin, molluscs`.

**Stored:** Browser (profile) `exclusions[] {category, severity, relaxed}`. Sent in every plan snapshot.

**Metric:** not measured (health data never leaves the browser except per request).

**Accessibility:** each `ExclusionRow` is a `<fieldset>` whose `<legend>` is the allergen name plus examples; the tiers are a radio group **with an explicit fifth option *None*** (instead of "tap again to clear", which is not discoverable by keyboard or screen reader). The selected tier's meaning is linked via `aria-describedby`. Colour is never the only signal; the tier name is always text. On `md`/`lg` rows sit in two columns, but DOM order stays alphabetical-by-PRD so tab order is predictable.

**Edge cases:** a user selects *Allergy* then switches to *Intolerance*: the row explains the difference immediately. Allergies cannot be "avoid when possible" (toggle not shown). Nothing is ever collapsed; at accessibility sizes the list just gets longer.

| Key | EN | PL |
|---|---|---|
| `onb.allergy.title` | Any allergies or intolerances? | Masz alergie lub nietolerancje? |
| `onb.allergy.body` | Pick a level for anything you avoid. Allergies are never planned, including traces. | Wybierz poziom dla tego, czego unikasz. Alergenów nigdy nie planujemy, także w śladowych ilościach. |
| `tier.allergy` | Allergy | Alergia |
| `tier.allergy.desc` | Never planned, including derived ingredients and "may contain" traces. | Nigdy w planie, również składniki pochodne i „może zawierać”. |
| `tier.intolerance` | Intolerance | Nietolerancja |
| `tier.intolerance.desc` | Never planned. Traces are allowed. | Nigdy w planie. Śladowe ilości są dopuszczalne. |
| `tier.intolerance.relax` | Avoid when possible | Unikaj, gdy to możliwe |
| `tier.intolerance.relax.desc` | Used only when nothing else fits, and always labelled. | Tylko gdy nic innego nie pasuje, zawsze z oznaczeniem. |
| `tier.dislike` | Don't like | Nie lubię |
| `tier.dislike.desc` | Rarely planned and never added as a swap. | Rzadko w planie, nigdy jako zamiennik. |
| `tier.prefer_not` | Prefer not | Wolę unikać |
| `tier.prefer_not.desc` | Planned a little less often. | Pojawia się w planie nieco rzadziej. |
| `onb.allergy.cta_none` | I have none | Nie mam żadnych |
| `allergen.gluten` | Cereals containing gluten | Zboża zawierające gluten |
| `allergen.crustaceans` | Crustaceans | Skorupiaki |
| `allergen.eggs` | Eggs | Jaja |
| `allergen.fish` | Fish | Ryby |
| `allergen.peanuts` | Peanuts | Orzeszki ziemne (arachidowe) |
| `allergen.soy` | Soybeans | Soja |
| `allergen.milk` | Milk | Mleko |
| `allergen.tree_nuts` | Tree nuts | Orzechy |
| `allergen.celery` | Celery | Seler |
| `allergen.mustard` | Mustard | Gorczyca |
| `allergen.sesame` | Sesame | Sezam |
| `allergen.sulphites` | Sulphites | Dwutlenek siarki i siarczyny |
| `allergen.lupin` | Lupin | Łubin |
| `allergen.molluscs` | Molluscs | Mięczaki |

(Allergen names follow the official PL wording of Regulation 1169/2011, Annex II.)

---

## 11 Restrictions (11/14)

**Purpose:** diet categories and free-text exclusions, with tiers (PRD §7).

**Layout:** title *Anything else you avoid?*; `SectionHeader` *Diet* with `ExclusionRow`s for the backend's broader groups: Meat (incl. poultry), Shellfish, Dairy, Nuts. `SectionHeader` *Something else* with a text field *Type a food, e.g. coriander* and *Add*. Each added term shows as an `ExclusionRow` with its match state. Sticky *Continue* / *I have none*.

**Free-text matching:** the term is matched against FoodItems/allergen groups. Needs the network (a food search, `GET /v1/foods/search`), so:
- Match found → row shows *Matched: coriander (fresh, seeds)* with a *Not this* link to pick another match from a sheet.
- Several matches → a sheet to pick one.
- No match → `Notice tone="warning"` inside the row: *We couldn't match "{term}" to a food, so we can't enforce it.* with *Pick a match* and *Remove*. Unmatched entries are kept but labelled *Not enforced*, and an ALLERGY tier on an unmatched entry is kept visible at the top of the list.
- Offline → the term is saved as *Not checked yet* and matched on the next connection; plan generation asks to resolve it first.

**Fields:** `exclusions[] {category: meat|shellfish|dairy|nuts|other, term?, severity, relaxed}` (`term` only for `other`).

**Stored:** Browser (profile). The free-text term goes to the server only as a food search query (no user link beyond the authenticated request; before sign-in, unauthenticated search).

**Metric:** not measured.

**Accessibility:** unmatched state announced as *Not enforced*. The search field has a clear button and *Add* ≥ 44 pt.

**Edge cases:** "vegetarian" as free text → suggest the *Meat* category or the Vegetarian preference on step 12. Duplicates of an allergen chosen on step 10 → show *Already in your allergies* and keep the stricter tier.

| Key | EN | PL |
|---|---|---|
| `onb.restr.title` | Anything else you avoid? | Czego jeszcze unikasz? |
| `onb.restr.diet` | Diet | Dieta |
| `excl.meat` | Meat (incl. poultry) | Mięso (w tym drób) |
| `excl.shellfish` | Shellfish | Owoce morza |
| `excl.dairy` | Dairy | Nabiał |
| `excl.nuts` | Nuts (incl. peanuts) | Orzechy (w tym arachidowe) |
| `onb.restr.other` | Something else | Coś innego |
| `onb.restr.other.placeholder` | Type a food, e.g. coriander | Wpisz produkt, np. kolendra |
| `onb.restr.other.add` | Add | Dodaj |
| `onb.restr.matched` | Matched: {food} | Dopasowano: {food} |
| `onb.restr.not_this` | Not this | To nie to |
| `onb.restr.unmatched` | We couldn't match "{term}" to a food, so we can't enforce it. | Nie udało się dopasować „{term}” do produktu, więc nie możemy tego egzekwować. |
| `onb.restr.pick_match` | Pick a match | Wybierz produkt |
| `onb.restr.remove` | Remove | Usuń |
| `onb.restr.not_enforced` | Not enforced | Nieegzekwowane |
| `onb.restr.not_checked` | Not checked yet | Jeszcze niesprawdzone |
| `onb.restr.duplicate` | Already in your allergies | Już na liście alergii |

---

## 12 Preferences (12/14)

**Purpose:** soft ranking inputs (PRD §7).

**Layout:** title *What do you like to eat?*; multi-select `Chip`s (wrap): High protein, Vegetarian, Vegan, Mediterranean, Quick meals, Sweet breakfast, Savoury breakfast, Meal-prep friendly, Low-cost. Optional; *Continue* enabled with none (*Skip*).

**Rules:** Vegetarian and Vegan are preferences (ranking) here. If the user wants a guarantee, a line under them says *Want no meat at all? Exclude it in the previous step.* with a link back. Sweet and Savoury breakfast are mutually exclusive.

**Stored:** Browser (profile) `preferences[]`. (Planner input to be added, README API need 5.) **Metric:** not measured.

**Accessibility:** chips are native checkboxes styled as `Chip` (Sweet/Savoury breakfast as a radio pair with a *No preference* option); they wrap at all widths.

| Key | EN | PL |
|---|---|---|
| `onb.pref.title` | What do you like to eat? | Co lubisz jeść? |
| `pref.high_protein` | High protein | Dużo białka |
| `pref.vegetarian` | Vegetarian | Wegetariańskie |
| `pref.vegan` | Vegan | Wegańskie |
| `pref.mediterranean` | Mediterranean | Śródziemnomorskie |
| `pref.quick` | Quick meals | Szybkie dania |
| `pref.sweet_breakfast` | Sweet breakfast | Słodkie śniadania |
| `pref.savoury_breakfast` | Savoury breakfast | Wytrawne śniadania |
| `pref.meal_prep` | Meal-prep friendly | Do przygotowania z wyprzedzeniem |
| `pref.low_cost` | Low-cost | Tanio |
| `onb.pref.meat_hint` | Want no meat at all? Exclude it in the previous step. | Nie chcesz mięsa wcale? Wyklucz je w poprzednim kroku. |
| `onb.pref.skip` | Skip | Pomiń |

---

## 13 Budget (13/14)

**Purpose:** budget tier for Economy Mode weighting (PRD §7, §8.8). **No amount** in the MVP.

**Layout:** title *How careful with spending?*; three `SelectCard`s (icon `wallet`). **Default Standard.**

| Tier | Description |
|---|---|
| Economy | Fewer different ingredients and more reuse across the week. |
| Standard | A balance of variety and simple shopping. |
| Flexible | More variety; ingredient count matters less. |

No prices, no "save X PLN" (brand book: estimates only, Phase 2).

**Stored:** Browser (profile) `budget_tier`. **Metric:** Economy Mode usage (PRD §4) once the tier travels in plan requests and the server counts aggregated plans by tier (no user link needed).

| Key | EN | PL |
|---|---|---|
| `onb.budget.title` | How careful with spending? | Jak bardzo chcesz oszczędzać? |
| `budget.economy` | Economy | Oszczędnie |
| `budget.economy.desc` | Fewer different ingredients and more reuse across the week. | Mniej różnych składników i więcej ich ponownego użycia w tygodniu. |
| `budget.standard` | Standard | Standardowo |
| `budget.standard.desc` | A balance of variety and simple shopping. | Równowaga między różnorodnością a prostymi zakupami. |
| `budget.flexible` | Flexible | Elastycznie |
| `budget.flexible.desc` | More variety; ingredient count matters less. | Więcej różnorodności; liczba składników ma mniejsze znaczenie. |

---

## 14 Meal prep & cooking (14/14)

**Purpose:** "cook once for N days", max cooking time, equipment, and the plan reminder (PRD §7, §8.7, §12.2).

**Layout:**
1. Title *How do you like to cook?*
2. *Cook once for* — `SegmentedControl` *1 day* · *2 days* · *3 days* (default **1**; description under it: *1 day means you cook every day.*). Maps to `prep_days` 1–3.
3. *Max cooking time* — `SegmentedControl` *15* · *30* · *45* · *60* · *60+ min* (default **45**). Maps to `max_minutes` 15/30/45/60/`null`.
4. *Equipment you have* — multi `Chip`s: Air fryer, Oven, Blender, Microwave, Thermomix, and *None of these* (exclusive). Default: Oven, Microwave pre-selected (common in PL kitchens; user can change). Pots, pans and baking trays are assumed (planner `BASIC_TOOLS`), stated in a `footnote`.
5. Plan reminder card (`surface-raised`, `radius-lg`): *Plan next week on Thursday?* `body` *One reminder a week. No marketing.* Buttons *Remind me on Thursdays* (calls `Notification.requestPermission()` and subscribes to Web Push) and *Not now*. Answering is not required to continue. **Shown only where Web Push is supported** (feature-detect `PushManager`; on iOS Safari only in an installed PWA). Elsewhere the card is omitted. Whether to keep this at all on web is README open question 5.
6. Sticky primary *Build my plan*.

**Stored:** Browser (profile) `prep_days`, `max_minutes`, `equipment[]`; Browser (app state) `plan_reminder` (mirrors the browser permission). The push subscription is sent to the server after sign-in (it's not health data); sending is server-side, later sprint.

**Metric:** meal-prep usage (PRD §4) from aggregated plans with `prep_days > 1`.

**Accessibility:** segmented controls are radio groups that wrap to vertical lists when they don't fit; *60+ min* has the accessible name *more than 60 minutes, no limit*. Equipment chips are checkboxes. The reminder card's buttons are both ≥ 44 px; *Not now* is a real button, not a dismiss X.

**Edge cases:** permission denied → card shows *Reminders are off. You can turn them on in your browser's site settings.* and never re-prompts (browsers block repeat prompts anyway). *None of these* deselects others.

| Key | EN | PL |
|---|---|---|
| `onb.cook.title` | How do you like to cook? | Jak lubisz gotować? |
| `onb.cook.prep` | Cook once for | Gotuj raz na |
| `onb.cook.prep_days` | {n, plural, one {# day} other {# days}} | {n, plural, one {# dzień} other {# dni}} |
| `onb.cook.prep_hint` | 1 day means you cook every day. | 1 dzień oznacza gotowanie codziennie. |
| `onb.cook.time` | Max cooking time | Maksymalny czas gotowania |
| `onb.cook.time_value` | {n} min | {n} min |
| `onb.cook.time_none` | 60+ min | 60+ min |
| `onb.cook.time_none_a11y` | More than 60 minutes, no limit | Ponad 60 minut, bez limitu |
| `onb.cook.equipment` | Equipment you have | Sprzęt, który masz |
| `equip.air_fryer` | Air fryer | Frytkownica beztłuszczowa |
| `equip.oven` | Oven | Piekarnik |
| `equip.blender` | Blender | Blender |
| `equip.microwave` | Microwave | Mikrofalówka |
| `equip.thermomix` | Thermomix | Thermomix |
| `equip.none` | None of these | Żadne z tych |
| `onb.cook.basic_tools` | We assume you have pots, pans and a baking tray. | Zakładamy, że masz garnki, patelnie i blachę do pieczenia. |
| `onb.reminder.title` | Plan next week on Thursday? | Planować kolejny tydzień w czwartek? |
| `onb.reminder.body` | One reminder a week. No marketing. | Jedno przypomnienie w tygodniu. Bez reklam. |
| `onb.reminder.yes` | Remind me on Thursdays | Przypominaj w czwartki |
| `onb.reminder.no` | Not now | Nie teraz |
| `onb.reminder.denied` | Reminders are off. You can turn them on in your browser's site settings. | Przypomnienia są wyłączone. Możesz je włączyć w ustawieniach witryny w przeglądarce. |
| `onb.cook.cta` | Build my plan | Ułóż mój plan |

---

## 15 Sign in with Apple (sheet)

**Purpose:** save and sync the first plan; record consents on the server (PRD §7; README open questions 1, 4 and 6).

**When:** after the first plan is generated (value first). Presented as a `<dialog>` over the new Weekly Plan: bottom sheet (`radius-sheet`, inset 8 px) on `sm`, centred modal (max 440 px) on `md`/`lg`.

**Provider:** Sign in with Apple via **Apple JS** (popup mode on desktop, redirect mode on mobile browsers where popups are blocked). Adding Google and/or an email magic link is **README open question 4**; the layout reserves a vertical stack of provider buttons so more can be added without redesign.

**Layout:** title `title-1` *Save your plan*; three short rows: *Plans and recipes are kept with your account.* / *Your profile stays in this browser.* / *We never see your Apple ID email if you hide it.*; Apple's official "Sign in with Apple" web button (black/white per theme, full width, per Apple's web button guidelines); `footnote` *By continuing you accept the Terms of use and Privacy policy.* with both as links; text button *Not now*.

**After success:**
1. Apple JS returns the `id_token` → `POST /v1/auth/apple` (web variant, README API need 8) → access token in memory, refresh token in an `HttpOnly` cookie. Nothing in `localStorage`.
2. `POST /v1/me/consents` with pending `age_18_plus`, `health_data` (versions as shown) and `terms_of_use`, `privacy_policy` (granted on this tap).
3. The plan is saved to the account; navigate to Today.

**Not now:** sheet closes; the plan stays as a read-only preview (no meal status, swap or shopping list). Any of those actions re-opens this sheet. The preview survives a reload in this browser only (IndexedDB).

**Errors:** Apple sign-in cancelled or popup closed → back to the sheet, no message. Popup blocked → fall back to redirect mode; after the redirect returns, reopen the plan with the sheet's success state. Network error → `state.error.generic` in the sheet with *Try again*; the plan is kept in the browser. Consent POST fails → retried silently in the background; the app does not use server features that need the consent until it succeeds.

**Stored:** Server (account data, consent records); refresh token as an `HttpOnly` cookie. After sign-in, a one-time `offline`-tone notice offers *Download my profile* (README §Where data lives).

**Metric:** Activation: *first plan generated* (server plan record) and *profile completed* (consent records present). Sign-in conversion = accounts created ÷ plans generated anonymously (if option 1 chosen).

**Accessibility:** native modal `<dialog>` with `aria-labelledby` the title; focus starts on the title, is trapped, `Esc` = *Not now*, and focus returns to the plan heading on close. The Apple button has the accessible name *Sign in with Apple*.

| Key | EN | PL |
|---|---|---|
| `signin.title` | Save your plan | Zapisz swój plan |
| `signin.row1` | Plans and recipes are kept with your account. | Plany i przepisy zapisujemy na Twoim koncie. |
| `signin.row2` | Your profile stays in this browser. | Twój profil zostaje w tej przeglądarce. |
| `signin.row3` | We never see your Apple ID email if you hide it. | Jeśli ukryjesz e-mail Apple ID, nigdy go nie zobaczymy. |
| `signin.legal` | By continuing you accept the {terms} and {privacy}. | Kontynuując, akceptujesz {terms} i {privacy}. |
| `signin.terms` | Terms of use | Regulamin |
| `signin.privacy` | Privacy policy | Politykę prywatności |
| `signin.not_now` | Not now | Nie teraz |
| `signin.preview_locked` | Sign in to save your plan and use it day to day. | Zaloguj się, aby zapisać plan i korzystać z niego na co dzień. |

---

## Onboarding edge cases (cross-screen)

- **Profile change after the plan exists** (from Profile, later spec): changes are saved in the browser; the current plan is not silently changed. Today shows *Your settings changed. Build a new plan?*
- **Reload / tab closed:** position and answers kept; pending consents kept until sent.
- **Two tabs open:** the profile is shared through IndexedDB; the second tab listens for changes (`BroadcastChannel`) and re-renders, last write wins.
- **New browser or device:** 02 and 03 asked again and recorded again (DEVELOPMENT_PLAN §7.1), then *Load a profile file* or set up again (README No profile state).
- **Site data cleared mid-onboarding:** restart at Welcome; nothing was sent to the server, so nothing to clean up.
- **Language switch** (footer switch or browser setting): answers kept; strings re-render.
- **Reading/focus order** on every step: progress (*Step 6 of 14*, `aria-label` on the progress bar, `aria-valuenow`) → `<h1>` question → explanation → controls → primary button.
