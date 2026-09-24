# FitMeal AI: brand name research

Maintained by the `brand-researcher` agent ([.claude/agents/brand-researcher.md](../../.claude/agents/brand-researcher.md)). Findings go to the `engineering-manager`. Choosing the brand requires Product Owner approval (CLAUDE.md). Nothing in this report is a naming decision, and nothing here is legal clearance.

"FitMeal AI" is the working title. This report looks for the product's public brand name.

**Status (2026-09-24): first research session done, with limited live access.**

> **Live web access this session: partial.** Only **WebSearch** (a search engine) worked. Every authoritative source was **blocked by the network egress proxy** for both `curl` and WebFetch: registry RDAP (Verisign .com, Google Registry .app, NASK .pl, the IANA bootstrap), the iTunes Search API, apps.apple.com, Google Play, EUIPO, TMview, WIPO Brand DB, UPRP, USPTO, UK IPO, Instagram and TikTok. Per the task, no workaround was attempted: no proxy probing, no `whois` or `dig` substitutes, no mirror sites. Details are in §5.1.
>
> **What that means:** no name in this report has **Verified clear** or **Conflict** status for any store, domain, trademark or handle check. Every authoritative check is **Pending**. Search-engine findings are recorded separately as **Risk** (evidence of an existing, possibly conflicting use) or **Inconclusive** (no matching result found, which is **not** evidence of availability).

---

## Status legend

| Status | Meaning |
|---|---|
| **Verified clear** | Checked on an authoritative source (registry RDAP, official trademark register, official store search) on the stated date, with a link. No conflict found. |
| **Conflict** | An authoritative source shows the name taken, registered, or confusingly close to an existing mark, app or brand. |
| **Risk** | A partial or related conflict worth weighing. |
| **Inconclusive** | Checked, but the source was ambiguous, blocked or behind a login, or only a search engine answered. |
| **Pending** | Not checked yet, or live research was unavailable. |

A search engine result is never enough to call a name available. Domain and handle status changes: every finding is true only as of its check date. A clear trademark search is not a legal opinion, so attorney clearance is needed before adoption.

The Product Owner asked for four evidence categories. They map to the statuses like this:

| PO category | Status used here |
|---|---|
| Confirmed existing use (authoritative source) | **Conflict** (none this session, because authoritative sources were blocked) |
| Existing use seen only via a search engine / potentially conflicting name | **Risk** |
| No matching result found (search engine) | **Inconclusive** |
| Availability unverified (source not reached) | **Pending** |

---

## 1. Product positioning

Source documents: PRD §1–§5, §11–§13; Development Plan §3, §9; backend/README.md.

**Purpose.** Turn a recipe the user actually wants (from social media, a link, a PDF, or the catalog) into a version that fits their calories, macros, allergies, budget and meal-prep schedule. Then build a weekly plan and a shopping list around it (PRD §1, §8). Core promise: "Eat what you feel like eating, matched to your plan" (PRD §1).

**What it is not.** It is not a calorie counter (Fitatu, MyFitnessPal), not a recipe box (Paprika, ReciMe), not a diet-catering service (Dietly), and not a chatbot. It is a nutrition and optimization platform with an AI layer. The deterministic engine does the maths, and the AI only interprets and explains (PRD §1, §5 principle 2, §9).

**Differentiators** (the PRD §2 "ten problems as one system"):
1. Recipe transformation that preserves culinary intent (PRD §8.3).
2. Non-naive substitutions with a visible nutrition and cost delta for each swap (§8.4).
3. Swaps that rebalance the rest of the day automatically (§8.6).
4. Meal prep and Economy Mode as first-class features, including package-aware shopping (§5 principles 6–8, §8.7–8.8).
5. Explainability: the user approves every change, and the app says why it made it (§5 principles 4 and 10).

The backend already does PL/EN diacritics-insensitive ingredient search and unit-aware nutrition maths, including Polish kitchen units such as `łyżka` and `szklanka` (backend/README.md).

**Primary audience (go-to-market wedge).** 20–45-year-olds in Poland who already count calories and protein, take recipe inspiration from Instagram and TikTok, cook for themselves and prep for 2–3 days (PRD §3). Secondary personas: high-protein, cutting, bulking, vegetarian, athletes, budget-minded families, dietitian clients (PRD §3).

**User motivations** (drawn from PRD §2–§3):
- "I want to eat *that* recipe, not chicken and rice again."
- "I don't want to do the macro maths myself."
- "I want to spend less and waste less."
- "I cook once for several days."
- "I want control and to see what changed."

**Markets and languages.** Poland first, Polish and English from day one, EU hosting, iOS App Store launch (Plan §3, §9). Later English-speaking and other EU markets.

**Brand personality.** Practical, confident, food-positive, a little playful, and precise without being clinical. It should feel like a friend who is good with numbers and good in the kitchen. Never moralizing ("guilt-free", "cheat", "slim"), never medical (PRD §12, Plan §11 App Review risk), and never "the AI decides" (PRD §5 principle 10).

**Positioning statement (working).** For people in Poland who track what they eat but won't give up the food they love, [Brand] is the meal planner that makes any recipe fit your numbers, your budget and your prep day, and shows you exactly what it changed.

---

## 2. Naming strategy

**Directions explored (PO Phase 2):** (1) invented, distinctive words; (2) short tech-style brands; (3) food, nutrition and wellbeing words; (4) abstract lifestyle words; (5) international names that work in Polish and English, including Polish-rooted words that an English speaker can read.

**What the market research implies (§3):**
- **Avoid the "Fit-" prefix.** It is saturated in Poland (Fitatu, Fit Foczki, Fit-World, FitChoice, Fitia). The working title "FitMeal" falls into this crowded pattern and would be a weak mark (C1).
- **Avoid "Meal-" compounds** (Mealime, MealPrepPro, MealBoard, MealPreper, Mealll). They are descriptive and hard to register.
- **Avoid "AI" in the brand.** Store titles in this category already overuse it ("Fitatu Licznik Kalorii AI", "Portio AI", "Tamu"), and C7 rules it out.
- **Short English food words are heavily taken by recipe apps.** Morsel, Mise, Tavola, Paprika, Crouton, Pestle, Honeydew, Whisk and Gusta/Gustino were all found in use this session (§5.2).
- **The best openings are Polish-rooted words that an English speaker can read phonetically, and distinctive coinages.** Letters that sound the same in Polish and English: a, e, i, o, u, b, d, f, g, k, l, m, n, p, r, s, t, z. Avoid c, j, w, y, ch, sz, cz, rz, and anything with ł, ą or ę.

**Preferred form (from the PO brief):** 4–8 characters, one to three syllables, no diacritics, hyphens or numbers, a store title that fits the 30-character limit with a descriptor (for example "Smakora: Meal Planner" is 21 characters).

### Naming criteria

| # | Criterion | Why |
|---|---|---|
| C1 | Distinctive, not purely descriptive | Registrable as a trademark, stands out in the stores |
| C2 | Easy to say and spell in Polish and English, no diacritics | PL + EN from day one, word of mouth |
| C3 | No negative, rude or awkward meaning in PL, EN or other major EU languages | International use |
| C4 | Fits the positioning: personal, food you want, planning, economy, meal prep | PRD §1, §5 |
| C5 | No medical claims, no "diet guilt" language, doesn't suggest the AI decides nutrition | PRD §5, §12 |
| C6 | App name (with any descriptor) fits 30 characters; no Apple/Google trademarks | Store rules |
| C7 | Not tied to one feature, one diet or "AI" | Roadmap phases 2–4 (PRD §13) |
| C8 | .com or .app obtainable; consistent social handles possible | Brand consistency |
| C9 | No conflicting live trademarks in classes 9, 42, 44 (and 35, 41, 29/30) | Legal risk |

---

## 3. Competitor landscape

Checked 2026-09-24 via WebSearch only; competitor sites and store pages could not be opened (egress-blocked). Descriptions are what the search results showed, and they have not been verified against the stores.

### 3.1 Poland

| Brand | Category | What the search showed | Naming pattern | Relevance |
|---|---|---|---|---|
| **Fitatu** | Calorie/macro counter with AI and meal plans | Store title "Aplikacja Fitatu Licznik Kalorii AI", "10 million" users claimed, largest PL food database ([App Store PL](https://apps.apple.com/pl/app/fitatu-licznik-kalorii-ai/id1011095795?l=pl), [fitatu.com](https://www.fitatu.com/pl)) | Fit + invented suffix | Market leader the wedge users already have. "Fit-" names read as "another Fitatu". |
| **Luncher** (by Policzona Szama) | Meal-prep planner that adapts recipes to nutrition needs, with shopping lists | "Luncher – Twój planer zdrowych posiłków i meal prep by Policzona Szama" ([luncher.app](https://www.luncher.app/)) | Real English word + -er | **Closest PL functional competitor.** Its creator-led audience is the same wedge. |
| **Fit Foczki** | Recipes, meal plans, community | "Aplikacja Fit Foczki - Dieta i Przepisy - App Store" ([App Store PL](https://apps.apple.com/pl/app/fit-foczki-dieta-i-przepisy/id6478501038?l=pl)) | Fit + playful PL word | Influencer-led fit recipes |
| **Fit-World** | Diet plans, calorie diary, shopping list | "Fit-World: Dieta i Przepisy App - App Store" ([App Store PL](https://apps.apple.com/pl/app/fit-world-dieta-i-przepisy/id6468837358)) | Fit + EN word | Same pattern |
| **Dietly** | Comparison and ordering of diet catering (300 caterers) | "Aplikacja Dietly — App Store" ([App Store PL](https://apps.apple.com/pl/app/dietly/id1642713520?l=pl), [dietly.pl](https://dietly.pl/app)) | Diet + -ly | Adjacent: boxed diets replace cooking |
| **Vitalia** | Long-running diet platform with dietitian chat and shopping list | "Vitalia - dieta i motywacja on the App Store" ([App Store](https://apps.apple.com/us/app/vitalia-dieta-i-motywacja/id6443716283)) | Latinate vital- | Established diet-plan brand |
| **Smaker** (Interia) | Recipe app, 100k+ user recipes, planner | "Smaker - przepisy kulinarne on the App Store" ([App Store PL](https://apps.apple.com/pl/app/smaker-przepisy-kulinarne/id1189128951), [Google Play](https://play.google.com/store/apps/details?id=pl.interia.smaker&hl=en_US)) | PL "smak" (taste) + -er | **Matters for any "Smak-" name** (see Smako and Smakora) |
| **Kwestia Smaku** | Recipe portal, 639k Facebook followers per the search | [kwestiasmaku.com](https://www.kwestiasmaku.com/) | PL phrase ("a matter of taste") | Recipe inspiration source; uses the "smak" stem |
| **Kuchnia Lidla / LidloMix** | Retailer recipe portal; LidloMix app searches recipes by ingredients you have | [kuchnialidla.pl](https://kuchnialidla.pl/), [LidloMix article](https://cuisine-pratique.pl/blogs/robot-kuchenny-i-frytkownica-powietrzna-air-fryers/lidlomix-nowa-aplikacja-ktora-ulatwi-gotowanie-i-zakupy-w-lidlu) | Retailer brand | Pantry-style feature from a grocery giant |
| **Jadłonomia** | Plant-based blog and cookbook (Marta Dymek) | Search summary | PL coinage (jadło + -nomia) | Shows that PL coinages work, though this one has diacritics |
| **Przepisy.pl** | Recipe app, 9,000+ recipes | [Google Play](https://play.google.com/store/apps/details?id=pl.przepisy&hl=en_US) | Descriptive | Descriptive naming |
| **Foodsi** | Surplus-food marketplace | [foodsi.pl](https://foodsi.pl/) | Food + -si | Food-waste positioning overlap (Economy Mode) |
| **Rukola** | Diet catering app | "Aplikacja Rukola - App Store - Apple" ([App Store PL](https://apps.apple.com/pl/app/rukola/id6503609375?l=pl)) | Food word | Killed our "Rukola" candidate |
| **dietetycy.org.pl** | Dietitian portal ranking diet apps (Fitatu, Vitalia, FatSecret, MFP) | [dietetycy.org.pl/aplikacje-dietetyczne](https://dietetycy.org.pl/aplikacje-dietetyczne/) | Descriptive | A trust and review channel for the wedge |
| **Diet & Training by Ann, DietetykPro, dietetyk.ai** | Influencer and dietitian diet apps | [DietetykPro App Store](https://apps.apple.com/pl/app/dietetykpro-dieta-i-przepisy/id6479309416?l=pl), [dietetyk.ai](https://dietetyk.ai/jakie-sa-najlepsze-aplikacje-dietetyczne-online) | Person- or profession-led | Shows the "dietitian" framing used in the category |
| **Fitaid** | Not found as a Polish diet app | Search surfaced FitAid as a US recovery drink ([lifeaidbevco.com](https://www.lifeaidbevco.com/drinks/products/fitaid)) | — | **Inconclusive**: the PO's reference could not be matched |

### 3.2 International

| Brand | Category | What the search showed | Naming pattern |
|---|---|---|---|
| MyFitnessPal, Lose It!, FatSecret, Cal AI | Calorie trackers | Listed in 2026 roundups ([Fitia roundup](https://fitia.app/learn/article/top-12-nutrition-tracking-apps-2026/)) | Descriptive compounds |
| Yazio, Lifesum | Design-led trackers with diet plans (Lifesum: Sweden, 60M+ downloads per the search) | Same source | Coined (-io) / compound |
| MacroFactor, Cronometer | Adaptive macro coaching / micronutrient precision | Same source | Descriptive-technical |
| **Fitia** | Adaptive tracking plus meal planning | Same source | Fit + -ia |
| Foodvisor, Portio AI, SnapCalorie | Photo logging | [Portio AI App Store](https://apps.apple.com/us/app/portio-ai/id6754779401) | Compound / coined |
| **Eat This Much** | Auto meal plans for calorie, macro and budget targets | [Eat This Much blog](https://blog.eatthismuch.com/best-meal-planning-apps/) | Phrase | **Closest international functional competitor** |
| Mealime | Meal plans and grocery list; **shutting down 21 Oct 2026** per the search | [Pann article](https://www.pann-app.com/blog/is-mealime-shutting-down) | Meal + -ime |
| Samsung Food (formerly Whisk), Plan to Eat, Paprika | Recipe saving and planning | [comparison](https://blog.eatthismuch.com/best-meal-planning-apps/) | Food-tool words / phrase |
| ReciMe, Honeydew, Pestle, Crouton, Mela, Gustino, Tavola, Mob, Remy, Recipe Notes | Social-media recipe import | [Honeydew guide](https://honeydewcook.com/guides/best-recipe-apps), [Remy blog](https://www.remyapp.io/blog/the-best-apps-for-saving-recipes-from-tiktok-and-instagram), [Gustino](https://apps.apple.com/us/app/gustino-recipe-meal-planner/id6774185280), [Tavola](https://thetavola.ai/) | **Food and kitchen words dominate** |
| Noom | Behaviour-change weight program | [consumersadvocate.org](https://www.consumersadvocate.org/diet-plans/c/noom-diet-plans-review) | Abstract coinage |
| PlateJoy | **Closed 1 July 2025** per the search | [mealthinker.com](https://mealthinker.com/blog/platejoy-alternative) | Compound |
| Ollie | AI family meal planning | [App Store](https://apps.apple.com/us/app/ollie-for-meals-meal-planning/id6480014476) | Personal name |
| Gousto, HelloFresh | Meal kits (classes 29/30/35/43 overlap) | [Gousto Google Play](https://play.google.com/store/apps/details?id=uk.co.gousto.gousto&hl=en_GB) | Coined from "gusto" |

### 3.3 Takeaways for naming

1. The PL wedge knows Fitatu, Luncher/Policzona Szama, Fit Foczki and Smaker. **Anything "Fit-" or "Smak-er"-like will blend in.**
2. English food and kitchen nouns are the default naming move for recipe apps, and most short ones are taken.
3. Nobody in Poland owns a name that means "the food you feel like" or "fits your plan". Polish words about **craving, taste or portion** are the open semantic space, which is why Oskoma, Smakora, Porcio and Smako were tested.

---

## 4. Candidate names (longlist)

73 names generated on 2026-09-24. "Search" means a WebSearch screen was run that day (evidence in §5.2). "Judgment" means the name was screened out on linguistic or strategic grounds without a search. Such names are not claimed to be taken.

### 4.1 Invented, distinctive words

| # | Name | Idea behind it | Screen result |
|---|---|---|---|
| 1 | Porcio | "Portion" in PL (porcja), ES (porción) and Esperanto (porcio): your portion of the plan | **Shortlisted** (with Risk) |
| 2 | Smako | PL "smak" (taste) + a friendly -o | **Shortlisted** (with Risk) |
| 3 | Smakora | "smak" (taste) + a flowing ending; taste that fits | **Shortlisted** |
| 4 | Yemo | Phonetic "jem" / "jemy" (I eat / we eat) | **Shortlisted** (with Risk) |
| 5 | Prepko | Meal "prep" + the Polish diminutive -ko | **Shortlisted** (with Risk) |
| 6 | Remeal | Re-make the meal | Screened out (search): ReMeal surplus-food app, Malaysia; remeal.app in use |
| 7 | Menova | Menu + nova | Screened out (search): Menova menopause nutrition app; also a drug brand (C5) |
| 8 | Nutrova | Nutrition + nova | Screened out (judgment): "nutri-" is descriptive and supplement-like (C1/C5) |
| 9 | Kalio | From kaloria | Screened out (judgment): positions the product as a calorie counter (C4) |
| 10 | Tailo | Tailor | Screened out (judgment): Poles may read "ta-i-lo" and English speakers "tay-lo" (C2) |
| 11 | Mealo | Meal + o | Screened out (judgment): "meal" is descriptive (C1) |
| 12 | Fitlo | Fit + lo | Screened out (judgment): the "Fit-" prefix is saturated in PL (§3) |
| 13 | Tayst | "Taste" respelled | Screened out (judgment): the respelling breaks spelling from hearing (C2) |
| 14 | Macrolo | Macro + lo | Screened out (judgment): tied to macros (C7) |
| 15 | Talevo | Tale + evo | Screened out (search): Talevo story apps and an agency |
| 16 | Zestino | Zest + -ino: lively flavour | Screened out (judgment): "zest" is a crowded food-brand stem; PL readers may say "zes-TEE-no" or "dzes-" (C1/C2) |

### 4.2 Short, memorable tech brands

| # | Name | Idea behind it | Screen result |
|---|---|---|---|
| 17 | Tadam | "Ta-dam!": the reveal of your optimized recipe | **Shortlisted** (with Risk) |
| 18 | Takt | Rhythm or beat of the weekly loop | Screened out (search): many "Takt" apps (timer, time tracking, "Takt – an AI with taste"); "takt time" is a lean-manufacturing term |
| 19 | Loopa | The weekly planning loop | Screened out (search): Loop Nutrition, Food Loops; PL reads it as "lupa" (magnifier) |
| 20 | Mise | Mise en place | Screened out (search): several "Mise" recipe and meal-planner apps |
| 21 | Sous | Sous-chef | Screened out (judgment): PL pronunciation unclear; FR slang for money (C2/C3) |
| 22 | Whisk | Kitchen tool | Screened out (search): former name of Samsung Food |
| 23 | Prepd | Prepared | Screened out (search): "Preppd – Meal Prep & Planner" app; no vowel (C2) |
| 24 | Plato | Plate + philosopher | Screened out (judgment): generic, crowded |
| 25 | Tempo | Pace | Screened out (judgment): crowded, generic |
| 26 | Kova | Coined | Screened out (judgment): TR "bucket", FI "hard"; no concept |
| 27 | Gotu | From PL "gotuj" (cook) | Screened out (search): gotu kola, a medicinal herb (C5), and the GoToMeals app |
| 28 | Nomi | "Nom" (eat) + i | Screened out (judgment): likely crowded; not searched |

### 4.3 Food, nutrition and wellbeing

| # | Name | Idea behind it | Screen result |
|---|---|---|---|
| 29 | Ramekin | A small dish for one portion: your recipe, portioned for you | **Shortlisted** |
| 30 | Miska | PL "bowl" | **Shortlisted** (with Risk) |
| 31 | Kredens | PL kitchen dresser or cupboard: pantry and prep | **Shortlisted** (with Risk) |
| 32 | Morsel | A small bite | Screened out (search): three "Morsel" recipe apps on the App Store |
| 33 | Rukola | Arugula (PL/IT spelling) | Screened out (search): Polish diet-catering app "Rukola" |
| 34 | Tavola | IT "table" | Screened out (search): two "Tavola" meal-planner and recipe apps |
| 35 | Gusta | PL "gust" (taste) / ES "me gusta" | Screened out (search): Gusta recipe app, Gustino, and Gousto meal kits |
| 36 | Nuta | PL "nuta smaku" (a note of flavour) | Screened out (search): "Nuta – Smart Diet Tracker" app |
| 37 | Paprika | Spice | Screened out (search): Paprika recipe manager |
| 38 | Umami | Fifth taste | Screened out (judgment): crowded |
| 39 | Kale | Leafy green | Screened out (judgment): single ingredient or diet (C7) |
| 40 | Kasza | PL groats | Screened out (judgment): "sz" is hard for English speakers (C2) |
| 41 | Pestka | PL "pit" or "seed" | Screened out (judgment): English speakers read "pest" (C3) |
| 42 | Grub | EN slang for food | Screened out (judgment): PL "gruby" = fat (C3/C5) |
| 43 | Chow | EN slang for food | Screened out (judgment): PL "chów" = livestock breeding (C3) |
| 44 | Nosh | EN slang for food | Screened out (judgment): PL reads it as "nosz", an interjection used in mild swearing (C3) |
| 45 | Savora | Savour | Screened out (judgment): believed to be an existing French condiment brand (class 30); not searched |
| 46 | Kalibra | Calibrate the recipe | Screened out (search): Kalibra Diet app and Kalibra health app |
| 47 | Plateau | Plate + "plateau" | Screened out (judgment): "weight-loss plateau" connotation (C5) |
| 48 | Rabarbar | PL rhubarb; also the actors' crowd-noise word | Screened out (judgment): long, single ingredient (C7) |
| 49 | Kokilka | PL for ramekin | Screened out (judgment): hard for English speakers, diminutive, niche |

### 4.4 Abstract lifestyle

| # | Name | Idea behind it | Screen result |
|---|---|---|---|
| 50 | Doma | "At home" (PL dialect, CS, RU): home cooking | **Shortlisted** (with Risk) |
| 51 | Pora | PL "pora" = time or season ("pora obiadu", time for lunch) | **Shortlisted** (with Risk) |
| 52 | Lagom | Swedish "just the right amount" | Screened out (search): LAGOM school-nutrition app |
| 53 | Oreka | Basque "balance" | Screened out (search): Oreka food-waste app and a health-centre app with nutrition services |
| 54 | Tandem | Doing it together | Screened out (judgment): medical-device association (C5) |
| 55 | Balans | PL/SE/NL "balance" | Screened out (judgment): descriptive in PL (C1) |
| 56 | Rytmo | Rhythm | Screened out (judgment): the "y" is awkward in English (C2) |
| 57 | Juno | Goddess | Screened out (judgment): crowded |
| 58 | Sobota | PL Saturday (prep day) | Screened out (judgment): meaningless in English, weekday-specific (C2/C7) |
| 59 | Kompas | Compass | Screened out (judgment): crowded |

### 4.5 International names that work in Polish and English

| # | Name | Idea behind it | Screen result |
|---|---|---|---|
| 60 | Oskoma | Old PL word for craving or appetite ("mieć oskomę na…" = to crave something): eat what you feel like | **Shortlisted** |
| 61 | Akurat | PL "just right / exactly" | **Shortlisted** (with Risk) |
| 62 | Zapas | PL "na zapas" = made ahead or for later: meal prep | **Shortlisted** (with Risk) |
| 63 | Ochota | PL "mam ochotę na…" = I feel like eating… | Screened out (judgment): English speakers read "ch" as "tch" (C2); a Warsaw district; RU "okhota" = hunting |
| 64 | Jemy | PL "we eat" | Screened out (judgment): BrE "jemmy" = a burglar's crowbar (C3) |
| 65 | Mniam | PL "yum" | Screened out (judgment): unpronounceable for English speakers (C2) |
| 66 | Talia | Name-like | Screened out (judgment): PL "talia" = waist, a body focus (C5) |
| 67 | Forma | "W formie" (in shape) | Screened out (judgment): body-shape connotation (C5), crowded |
| 68 | Apetyt | PL appetite | Screened out (judgment): looks like a misspelling in English (C2) |
| 69 | Dania | PL "dishes" | Screened out (judgment): PL "Dania" also means Denmark |
| 70 | Pychota | PL "yummy!" | Screened out (judgment): "ch" (C2); "pycha" also means pride |
| 71 | Grosik | PL "little penny": economy | Screened out (judgment): English speakers see "gross" (C3) |
| 72 | Portio | Portion | Screened out (search + judgment): "Portio AI" calorie app; Latin anatomical term (C3) |
| 73 | Makrela | PL mackerel, a macro pun | Screened out (judgment): fish-specific (C7) |

Result: 14 names shortlisted (§6). The PO asked for 10–15.

---

## 5. Research findings and source links (evidence log)

All entries are dated **2026-09-24**.

### 5.1 Source access log

| Source (official) | Tool | Result | Consequence |
|---|---|---|---|
| `rdap.verisign.com` (.com RDAP) | curl, WebFetch | curl: `CONNECT tunnel failed, response 403` (proxy: `connect_rejected`). WebFetch: `EGRESS_BLOCKED … blocked by the network egress proxy` | All .com checks **Pending** |
| `pubapi.registry.google` (.app RDAP) | curl, WebFetch | Same two errors | All .app checks **Pending** |
| `data.iana.org` (RDAP bootstrap) | curl, WebFetch | Same | .io and .pl RDAP servers could not be looked up from the bootstrap |
| `rdap.dns.pl` (.pl RDAP) | WebFetch | `EGRESS_BLOCKED` | All .pl checks **Pending** |
| .io RDAP | not attempted | The bootstrap was unreachable, so the server URL could not be confirmed. Not guessed. | All .io checks **Pending** |
| `itunes.apple.com` (iTunes Search API) | curl, WebFetch | Blocked (as above) | App Store checks **Pending** |
| `apps.apple.com` | WebFetch | `EGRESS_BLOCKED` | App Store pages could not be opened |
| `play.google.com` | curl, WebFetch | Blocked | Google Play checks **Pending** |
| `euipo.europa.eu`, `www.tmdn.org`, `branddb.wipo.int`, `ewyszukiwarka.pue.uprp.gov.pl`, `tmsearch.uspto.gov`, `trademarks.ipo.gov.uk` | WebFetch | `EGRESS_BLOCKED` on each | All trademark checks **Pending** |
| `www.instagram.com`, `www.tiktok.com` | WebFetch | `EGRESS_BLOCKED` | Handle checks **Pending** |
| `www.fitatu.com` (a control, not a registry) | WebFetch | `EGRESS_BLOCKED` | WebFetch appears blocked for all hosts |
| WebSearch with `threads.net` domain filter | WebSearch | `400 … not accessible to our user agent` | Threads not searched |
| `whois` (port 43), `dig` | not used | Deliberately not used. They would sidestep the HTTPS egress block, which the task forbids. | — |
| **WebSearch** (general and domain-filtered) | WebSearch | **Worked** | Used for competitors, near-name screening and indicative store, domain and handle scans. Results are at most **Risk** or **Inconclusive**. |

### 5.2 Screening evidence (search engine; status at most Risk or Inconclusive)

Quoted text is the search result's title or snippet as returned.

| Name | Query | Status | What the search showed | Links |
|---|---|---|---|---|
| Remeal | `"Remeal" app` | Risk (screened out) | "ReMeal - Rescue Surplus Food - App Store - Apple"; "ReMeal - Rescue Surplus Food In Malaysia" at remeal.app | [App Store MY](https://apps.apple.com/my/app/remeal-rescue-surplus-food/id6499340832), [remeal.app](https://remeal.app/) |
| Gusta | `"Gusta" app recipes…` | Risk (screened out) | "Gusta on the App Store"; "Gustino: Recipe & Meal Planner - App Store" | [Gusta](https://apps.apple.com/ca/app/gusta/id6739286231), [Gustino](https://apps.apple.com/us/app/gustino-recipe-meal-planner/id6774185280) |
| Morsel | `"Morsel" app…` | Risk (screened out) | "Morsel: Recipe Manager App - App Store"; "Morsel: cook, share, eat - App Store"; getmorsel.com "a family recipe cookbook sharing app" | [1](https://apps.apple.com/us/app/morsel-recipe-manager/id6738929457), [2](https://apps.apple.com/us/app/morsel-cook-share-eat/id6756082004), [3](https://getmorsel.com/) |
| Menova | `"Menova" app OR brand` | Risk (screened out) | "Menova - App Store - Apple" (menopause meal-logging app); Menova drug-brand page | [App Store BR](https://apps.apple.com/br/app/menova/id6745178293), [medicinesfaq](https://www.medicinesfaq.com/brand/menova) |
| Loopa | `"Loopa" app food…` | Risk (screened out) | "Personalized Nutrition Services \| Loop Nutrition - Meal Planning"; "Food Loops App - App Store" | [loopnutrition.com](https://loopnutrition.com/meal-planning), [Food Loops](https://apps.apple.com/us/app/food-loops/id6742034552) |
| Nuta | `"Nuta" aplikacja…` | Risk (screened out) | "Nuta – Smart Diet Tracker - App Store - Apple" | [App Store](https://apps.apple.com/us/app/nuta-smart-diet-tracker/id1661970505) |
| Tavola | `"Tavola" app recipes…` | Risk (screened out) | "Tavola - Meal Planner App \| Weekly Meal Plans & Grocery Lists"; "Tavola — Your recipes deserve a home" | [thetavola.ai](https://thetavola.ai/), [tavolachef.app](https://tavolachef.app/) |
| Rukola | `"Rukola" app…` | Risk (screened out) | "Aplikacja Rukola - App Store - Apple" (diet catering); "Rukola - Apps on Google Play" | [App Store PL](https://apps.apple.com/pl/app/rukola/id6503609375?l=pl), [Play](https://play.google.com/store/apps/details?id=pl.rukola.app&hl=en_US) |
| Lagom | `"Lagom" app meal…` | Risk (screened out) | "Lagom - App Store - Apple" (school nutrition, meal plans) | [App Store](https://apps.apple.com/us/app/lagom/id6478700686) |
| Kalibra | `"Kalibra" app…` | Risk (screened out) | "Kalibra Diet - Apps on Google Play"; "Kalibra App - App Store"; "METODO KALIBRA®" | [Play](https://play.google.com/store/apps/details?id=eu.leonardoweb.kalibra&hl=en_US), [App Store](https://apps.apple.com/us/app/kalibra/id1569689807) |
| Gotu | `"Gotu" app cooking…` | Risk (screened out) | Gotu kola recipes; "GoToMeals - App Store - Apple" | [GoToMeals](https://apps.apple.com/us/app/gotomeals/id6749471193) |
| Takt | `Takt app` (store-filtered) | Risk (screened out) | "takt. App - App Store"; "Takt - Time Tracking"; "Takt - an AI with taste App" | [1](https://apps.apple.com/us/app/takt/id6756038807), [2](https://apps.apple.com/us/app/takt-an-ai-with-taste/id6755372259) |
| Oreka | `"Oreka" app OR brand…` | Risk (screened out) | "OREKA - Apps on Google Play" (food waste); "OREKA app" (health centre incl. nutrition) | [Play](https://play.google.com/store/apps/details?id=com.oreka.app&hl=en_US), [App Store](https://apps.apple.com/us/app/oreka-app/id6468587417) |
| Talevo | `"Smakora" OR "Talevo"…` | Risk (screened out) | "Talevo – Stories & Novels - App Store" | [App Store](https://apps.apple.com/us/app/talevo-stories-novels/id6756301257) |
| Mise | `"Miska" app meal…` (side result) | Risk (screened out) | "Mise - Recipes & AI Cooking - Apps on Google Play"; "Mise – Meal Planner & Recipe App" | [Play](https://play.google.com/store/apps/details?id=app.kineticloop.mise&hl=en_US), [mise.cooking](https://mise.cooking/) |
| Portio | `"Portio AI" OR "Portio"…` | Risk (screened out) | "Portio AI App - App Store" (photo calorie tracking); "Portio - App Store - Apple" | [1](https://apps.apple.com/us/app/portio-ai/id6754779401), [2](https://apps.apple.com/us/app/portio/id6736889954) |

The per-name evidence for the shortlist is in §6.3.

---

## 6. Shortlist

### 6.1 Check matrix (14 names)

Read each cell as **authoritative status (search-engine indication)**. "Pending" means the official source was blocked this session (§5.1). The indication in brackets is search-engine only.

| Name | 1 Competitors / similar | 2 App Store | 3 Google Play | 4 .com | 4 .app | 4 .io | 4 .pl | 5 Trademarks (EUIPO / TMview / UPRP / WIPO / USPTO / UKIPO) | 6 Language PL/EN | 7 Confusing similarity | 8 Social handles | E Search engine |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Ramekin** | Inconclusive | Pending (Inconclusive: no same-name app seen) | Pending (Inconclusive) | Pending | Pending | Pending | Pending | Pending (all six) | Inconclusive: no issue found; PL familiarity moderate | Inconclusive | Pending (Risk: generic word, heavy hashtag use) | Inconclusive |
| **Oskoma** | Risk: PL restaurants and cafés | Pending (Inconclusive) | Pending (Inconclusive) | Pending | Pending | Pending | Pending (Risk: appears listed for sale) | Pending | Risk: "-oma" medical ring (EN); RU "оскомина" | Risk: Restauracja Oskoma (PL, class 43) | Pending (Risk: @oskoma held by an individual) | Risk |
| **Smakora** | Risk: smakora.se recipe site (SE) | Pending (Inconclusive) | Pending (Inconclusive) | Pending | Pending | Pending | Pending | Pending | Inconclusive: EN "smack" echo | Risk: Smaker (PL recipe app), SMAKO™ | Pending | Risk |
| **Tadam** | Risk: non-food apps and brands | Pending (Risk: "Tadam" Mac timer, "Tadam – Easy Reports") | Pending (Risk: TaDam, TADAAM) | Pending | Pending | Pending | Pending | Pending | Inconclusive: no negative found | Risk: TADAM (FR menstrual products) | Pending (Risk: @wearetadam, @tadam_com in use) | Risk |
| **Smako** | Risk: SMAKO™ food personality test | Pending (Risk: SmakoBao restaurant app) | Pending (Risk: SmakoBao) | Pending | Pending | Pending | Pending | Pending | Inconclusive: "smack" echo | Risk: Smaker, SMAKO™, Smakoza | Pending (Risk: @smako.mp3, @smakoart in use) | Risk |
| **Porcio** | Risk: PorcioFOOD (HU healthy-meal delivery) | Pending (Risk: Portio AI near-identical) | Pending (Risk: "Porció" food delivery, HU) | Pending | Pending | Pending | Pending | Pending | Risk: porc/porco = pig (FR/IT/ES) | Risk: Portio AI (same category) | Pending (Risk: @porciofood) | Risk |
| **Yemo** | Risk: restaurant-ordering app, YeMo.ai | Pending (Risk: Yemmi food & macro tracker, similar) | Pending (Risk: "Yemo-Chat&video") | Pending | Pending | Pending | Pending | Pending | Risk: PL/EN readings differ | Risk: Yemmi | Pending (Risk: @yemo.dj etc.) | Risk |
| **Pora** | Risk: many "Pora" apps | Pending (Risk: Pora AI skin health, "Pora — Did I today?") | Pending (Risk: several) | Pending | Pending | Pending | Pending | Pending | Risk: PT "porra" near-homophone | Risk: "Pola" PL food app (sound) | Pending (Risk: @getpora in use) | Risk |
| **Miska** | Risk: Miskaa (recipe/meal-plan app), bowl restaurants | Pending (Risk: several "miska" apps) | Pending (Risk: Miska, МИСКА food app) | Pending | Pending | Pending | Pending | Pending | Risk: PL pet-bowl association | Risk: Miskaa | Pending (Risk: @miska.bowls etc.) | Risk |
| **Doma** | Risk: Doma (real estate), Doma.ai (proptech) | Pending (Risk: DonJoy DOMA, medical) | Pending (Risk: Doma property app) | Pending (Risk: doma.com in use by Doma) | Pending | Pending | Pending | Pending | Risk: US "DOMA" political acronym | Risk | Pending (Risk: @domaofficial 125K, @doma.official) | Risk |
| **Akurat** | Risk: Akurat.co (ID news), PL band Akurat | Pending (Risk: news apps) | Pending (Risk: "Akurat.co") | Pending | Pending | Pending | Pending (Risk: akurat.pl = band site) | Pending | Risk: EN ending "-rat" | Risk | Pending (Risk: @akuratco 154K) | Risk |
| **Zapas** | Risk: Zapas SRL apps, Za-Pas Knives (PL) | Pending (Risk: "Zapas SRL" developer) | Pending (Risk: "Apps by Zapas") | Pending (Risk: listed for sale by a broker) | Pending (Risk: zapas.app in use) | Pending | Pending | Pending | Risk: ES slang "zapas" = sneakers | Risk | Pending (Risk: @zapas.flash, FB zapasapp) | Risk |
| **Kredens** | Risk: many PL restaurants named Kredens | Pending (Risk: "Kredens Pizza Italiana") | Pending (Inconclusive) | Pending | Pending | Pending | Pending (Risk: kredens.pl in use) | Pending | Inconclusive: EN hears "credence" | Risk | Pending (Risk: @restauracjakredens etc.) | Risk |
| **Prepko** | Risk: Prepko (PrepKosher) meal-kit service, US | Pending (Inconclusive) | Pending (Risk: "Prepko - Анатомия") | Pending | Pending | Pending | Pending | Pending | Inconclusive | Risk: same-name meal kit | Pending (Risk: @prepkosher, youtube @Prepko) | Risk |

### 6.2 Scores (C1–C7) and ranking

Scores run from 1 (poor) to 5 (strong). They are the reviewer's assessment from the evidence above. **C8 (domains and handles) and C9 (trademarks) are Pending for every name** and are not scored. "Evidence weight" summarizes the search-engine Risk findings. It is a triage signal, not a legal assessment.

| Rank | Name | C1 | C2 | C3 | C4 | C5 | C6 | C7 | Sum /35 | Evidence weight (SE) | Further investigation? |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **Ramekin** | 4 | 3 | 5 | 4 | 5 | 5 | 5 | 31 | Low: no same-name app or company in the category seen | **Yes, top 3** |
| 2 | **Oskoma** | 4 | 4 | 3 | 5 | 4 | 5 | 5 | 30 | Medium: PL restaurants and cafés (class 43) | **Yes, top 3** |
| 3 | **Smakora** | 4 | 4 | 4 | 5 | 5 | 5 | 5 | 32 | Medium-high: same-name Swedish recipe site; "smak-" neighbours | **Yes, top 3** |
| 4 | Tadam | 3 | 5 | 4 | 3 | 5 | 5 | 5 | 30 | Medium: same-name apps in class 9 (non-food); FR consumer brand | Yes, alternate |
| 5 | Smako | 3 | 4 | 4 | 5 | 5 | 5 | 5 | 31 | High: SMAKO™ food-taste product | Only if Smakora fails |
| 6 | Yemo | 3 | 3 | 4 | 4 | 5 | 5 | 5 | 29 | Medium-high | No |
| 7 | Doma | 3 | 4 | 3 | 3 | 5 | 5 | 5 | 28 | Medium-high (large namesake brands, handles taken) | No |
| 8 | Akurat | 3 | 3 | 3 | 4 | 5 | 5 | 5 | 28 | Medium-high (well-known PL band) | No |
| 9 | Miska | 2 | 4 | 3 | 4 | 5 | 5 | 5 | 28 | High (Miskaa) | No |
| 10 | Prepko | 3 | 4 | 4 | 4 | 5 | 5 | 3 | 28 | High (same-name meal kit) | No |
| 11 | Pora | 2 | 4 | 3 | 3 | 5 | 5 | 5 | 27 | High (crowded; Pora AI health) | No |
| 12 | Kredens | 3 | 3 | 4 | 3 | 5 | 5 | 4 | 27 | Medium | No |
| 13 | Porcio | 3 | 3 | 2 | 4 | 4 | 5 | 5 | 26 | High (Portio AI; pig connotation) | No |
| 14 | Zapas | 3 | 3 | 3 | 4 | 5 | 5 | 3 | 26 | Medium (domain brokered) | No |

**Trade-offs in brief:**
- **Ramekin** is the cleanest in search, is instantly visual (a small individual dish makes a strong app icon) and fits "your portion, your plan". But it is an English kitchen word that fewer Poles know. It is also descriptive for tableware (class 21, not our class) and may read as a recipe-category word ("ramekin recipes") in class 41 content.
- **Oskoma** has the best fit with the core promise ("craving") and is spelled phonetically in both languages. But it is archaic Polish, it is used by several Polish food businesses, and to English ears the "-oma" ending sounds medical.
- **Smakora** is a coinage that is easy in both languages and carries "taste" across PL and the Nordic languages. But an identical Swedish recipe publication exists, and in Poland it sits near Smaker (Interia) and Kwestia Smaku.

### 6.3 Per-name evidence

All checks are dated 2026-09-24. Store, domain, trademark and handle checks are **Pending** for every name because the official sources were egress-blocked (§5.1). They are listed once per name in the tables rather than in every row.

---

#### `Ramekin`

- **Concept:** A ramekin is the small dish that holds one portion. The name says "your recipe, portioned and fitted to you" without saying diet, and it leaves room for pantry, family and dietitian phases.
- **Pronunciation:** EN /ˈræmɪkɪn/ "RAM-ih-kin". PL [ˈramɛkin] "RA-me-kin". A Pole reads it close to the English. English speakers spell it after one hearing; Polish speakers who don't know the word may write "ramekin" or "ramkin".
- **Meaning and connotations:** EN: an individual baking or serving dish (from FR "ramequin"). PL: a known loanword in recipes; the native term is "kokilka". No rude or negative meanings known in EN, PL, DE, FR, ES or IT (reviewer assessment; a native-speaker check is pending).
- **Brand positioning:** "Every recipe, in your portion." Warm and domestic, with a design-led look.
- **Visual identity:** a simple round dish silhouette works well as a monochrome app icon.
- **Main risks:** C1 is weaker if the mark is read as descriptive for recipe content. Moderate PL familiarity. Three syllables.

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Inconclusive | 2026-09-24 | [search](https://www.zoominfo.com/c/ramekin-llc/411222819) | "Ramekin LLC", LA, "Information & Document Management", 1–4 employees; ramekintech.com described as "parked free, courtesy of GoDaddy.com". No food or nutrition app seen. |
| 2 App Store (PL/US/GB) | Pending (SE: Inconclusive) | 2026-09-24 | iTunes API blocked; SE filtered to apps.apple.com | Nearest titles returned were "Ramain", "Ramin", "Kinton Ramen". No "Ramekin" app shown. |
| 3 Google Play | Pending (SE: Inconclusive) | 2026-09-24 | Play blocked; SE filtered to play.google.com | No "Ramekin" app shown. |
| 4 Domains .com/.app/.io/.pl | Pending | 2026-09-24 | RDAP blocked | A search for "ramekin.com / .app / .io" returned no site at those domains. That is not evidence of availability. |
| 5 Trademarks | Pending | 2026-09-24 | Registries blocked | Search `"Ramekin" trademark software OR app` returned no Ramekin mark. **Not a clearance.** |
| 6 Language | Inconclusive | 2026-09-24 | Reviewer assessment | See above. A native-speaker check is pending. |
| 7 Confusing similarity | Inconclusive | 2026-09-24 | SE | Nothing close found in the category. "Rameking" (kitchen organisation products) is a minor look-alike in class 21 ([rameking.com](https://www.rameking.com/about-us)). |
| 8 Social handles | Pending (SE: Risk) | 2026-09-24 | Instagram and TikTok blocked; SE filtered | Results are generic ramekin content (TikTok "How to Use A Ramekin"). The exact handles are unknown. Expect to need `ramekinapp` / `getramekin`. |

---

#### `Oskoma`

- **Concept:** An old Polish word for a craving or appetite for a particular food ("mieć oskomę na coś"). It is the core promise in one word: eat what you feel like, fitted to your plan.
- **Pronunciation:** PL [ɔsˈkɔma] "os-KO-ma". EN /ɒsˈkoʊmə/ "oss-KOH-muh". It is spelled phonetically in both languages, so it is easy to write after one hearing.
- **Meaning and connotations:** PL (search result summarising PWN): "dawne: 1) chęć zjedzenia lub wypicia czegoś, 2) wielka ochota na coś" (archaic: the wish to eat or drink something; a great desire for something). It is also colloquially "cierpnięcie, drętwienie zębów" (teeth on edge) ([PWN](https://sjp.pwn.pl/sjp/oskoma;2496435.html), [Wikisource etymology](https://pl.wikisource.org/wiki/S%C5%82ownik_etymologiczny_j%C4%99zyka_polskiego/oskoma)). RU/UA (reviewer knowledge): "оскомина" is the sour teeth-on-edge feeling, and "набить оскомину" means "to become tiresome", a mild negative. EN: no meaning, but the **"-oma" ending recalls medical terms** (carcinoma, glaucoma), a C5 risk. The black-metal band "Oskoma" is a minor association.
- **Brand positioning:** "Masz oskomę? Dopasujemy." ("Craving it? We'll make it fit.") A smart revival of an old word, with editorial charm for the PL market.
- **Visual identity:** a rounded "O" works well as the icon.
- **Main risks:** existing Polish food businesses with the same name; the medical-sounding ending; many Polish users won't know the archaic word (that can also be a storytelling asset).

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk | 2026-09-24 | [Tripadvisor](https://www.tripadvisor.com/Restaurant_Review-g19110773-d9763309-Reviews-Oskoma-Trzaskowo_Czerwonak_Greater_Poland_Province_Central_Poland.html), [Instagram (via SE)](https://www.instagram.com/oskoma_restaurant/), [Facebook (via SE)](https://www.facebook.com/p/Oskoma-Brunch-Coffee-100083654134202/) | "OSKOMA, Trzaskowo - Restaurant Reviews"; "Restauracja Oskoma (@oskoma_restaurant)"; "Oskoma - Brunch & Coffee" (Opole); "Oskoma Chybie" café. These are services (class 43), not software. |
| 2 App Store | Pending (SE: Inconclusive) | 2026-09-24 | SE filtered to apps.apple.com | No "Oskoma" app. Nearest: "OSMA", "Osmows". |
| 3 Google Play | Pending (SE: Inconclusive) | 2026-09-24 | SE filtered | No "Oskoma" app. |
| 4 Domains | Pending (SE: Risk for .pl) | 2026-09-24 | [oskoma.pl](http://oskoma.pl/) via SE | The search summary said "oskoma.pl - This domain appears to be for sale". Unverified: RDAP is needed. Nothing found for .com, .app or .io. |
| 5 Trademarks | Pending | 2026-09-24 | Registries blocked | Owner search needed (§8). |
| 6 Language | Risk | 2026-09-24 | PWN, Wikisource (above) | Archaic PL meaning confirmed by dictionary results; RU/EN connotations as noted. |
| 7 Confusing similarity | Risk | 2026-09-24 | as row 1 | An identical name used by a PL restaurant run by a "Top Chef finalist" (per SE), in an adjacent field. |
| 8 Social handles | Pending (SE: Risk) | 2026-09-24 | [Instagram @oskoma (via SE)](https://www.instagram.com/oskoma/?hl=en), [X @OskomaOfficial (via SE)](https://x.com/OskomaOfficial) | "Lisa Oskoma (@oskoma)" and "Anatoliy Oskoma (@OskomaOfficial)" suggest both exact handles are held by individuals. Variants like `oskoma.app` or `getoskoma` would be needed. |

---

#### `Smakora`

- **Concept:** "Smak" (taste) with an open, melodic ending: food that tastes like what you wanted, fitted to your numbers.
- **Pronunciation:** PL [smaˈkɔra] "sma-KO-ra". EN /sməˈkɔːrə/ "smuh-KOR-uh". Spelled phonetically, so it is easy to write after one hearing.
- **Meaning and connotations** (reviewer assessment; native check pending): "smak" means taste in PL and in Swedish and Norwegian. UA "смак" means taste and RU "смак" means relish. "-kora" reads in PL as "kora" (bark, cortex), which is neutral. EN risk: a "SMACK-ora" reading echoes "smack" (a hit; slang for heroin). That is mild, since stress falls on "-KOR-".
- **Brand positioning:** "Taste first, then the plan." Food-positive, a coined name with a Polish root and European reach.
- **Visual identity:** a lowercase "s" or a spoon mark.
- **Main risks:** the identical-name Swedish recipe publication (matters for any Nordic launch and for EU-wide rights if it holds a mark); crowding around the "smak" stem in Poland (Smaker, Kwestia Smaku, SMAKO™). The stem is descriptive in Polish, so protection rests on the whole coined word.

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk | 2026-09-24 | [smakora.se](https://smakora.se/asiatisk-kycklingfars-soja-ingefara/) | "Asiatisk kycklingfärs – underbart god, 25 min \| Smakora"; the search summary describes it as a food publication with recipes (Sweden). |
| 2 App Store | Pending (SE: Inconclusive) | 2026-09-24 | SE filtered | No "Smakora" app. Nearest: "SmakoBao", "Smak". |
| 3 Google Play | Pending (SE: Inconclusive) | 2026-09-24 | SE filtered | No "Smakora" app. |
| 4 Domains | Pending | 2026-09-24 | RDAP blocked | SE found **smakora.se in use**. Nothing found for .com, .app, .pl or .io, which is not evidence of availability. |
| 5 Trademarks | Pending | 2026-09-24 | Registries blocked | Owner search needed. Include the Swedish office in TMview. |
| 6 Language | Inconclusive | 2026-09-24 | Reviewer assessment | See above. |
| 7 Confusing similarity | Risk | 2026-09-24 | [Smaker App Store PL](https://apps.apple.com/pl/app/smaker-przepisy-kulinarne/id1189128951), [smakotest.com](https://www.smakotest.com/) | "Smaker - przepisy kulinarne" (Interia, PL recipe app) shares the "smak" stem; "SMAKO™ — 64 Flavour Characters" is a food-taste quiz. |
| 8 Social handles | Pending (SE: Inconclusive) | 2026-09-24 | SE filtered | Only "smakor" / "@smakor2" accounts surfaced, not "smakora". The exact handles are unverified. |

---

#### `Tadam` (alternate)

- **Concept:** "Ta-dam!" is the reveal when your recipe comes back fitted to your plan. It maps to the value-first paywall moment ("optimized version found", PRD §11).
- **Pronunciation:** PL [taˈdam]. EN /təˈdæm/. Instantly spellable in PL, EN and FR.
- **Meaning:** an interjection (PL/FR). No negatives known (reviewer assessment).
- **Main risks:** a common interjection, so distinctiveness is moderate. Same-name software exists in class 9. There is a French consumer brand (@tadam_com, menstrual products per the SE summary).

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk | 2026-09-24 | [Tadam! jewellery](https://notjustalabel.com/tadam), [Tadam Software](https://www.tadamsoft.com/) | Several unrelated "Tadam" companies and brands |
| 2 App Store | Pending (SE: Risk) | 2026-09-24 | [Tadam Mac](https://apps.apple.com/us/app/tadam/id531349534?mt=12), [Tadam Easy Reports](https://apps.apple.com/us/app/tadam/id1462515520) | "Tadam on the Mac App Store" (focus timer); "Tadam - Easy Reports App" |
| 3 Google Play | Pending (SE: Risk) | 2026-09-24 | [TADAAM](https://play.google.com/store/apps/details?id=be.tadaam&hl=en_US), [TaDam](https://play.google.com/store/apps/details?id=com.Easytech.Tadam&hl=en_US) | "TADAAM" (Belgian TV), "TaDam תאדם" |
| 4 Domains | Pending | 2026-09-24 | RDAP blocked | Nothing found for tadam.pl by SE (not evidence of availability) |
| 5 Trademarks | Pending | 2026-09-24 | Registries blocked | — |
| 6 Language | Inconclusive | 2026-09-24 | Reviewer | No issue found |
| 7 Confusing similarity | Risk | 2026-09-24 | as above | Identical names in software |
| 8 Social handles | Pending (SE: Risk) | 2026-09-24 | [@wearetadam (via SE)](https://www.instagram.com/wearetadam/), [@tadam_com (via SE)](https://www.instagram.com/tadam_com/?hl=en) | Both appear to be in use |

---

#### `Smako`

- **Concept:** "Smak" (taste) + -o. **Pronunciation:** PL [ˈsmakɔ]; EN /ˈsmɑːkoʊ/ (may be said "SMACK-o").
- **Main risks:** SMAKO™ is an active food-taste product; SmakoBao is a Polish restaurant app; smako.store has negative reviews (reputational noise).

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk | 2026-09-24 | [smakotest.com](https://www.smakotest.com/) | "SMAKO™ — 64 Flavour Characters. Which One Are You? \| Food Personality Test" |
| 2 App Store | Pending (SE: Risk) | 2026-09-24 | [SmakoBao](https://apps.apple.com/uy/app/smakobao/id1642325729) | "SmakoBao on the App Store" (restaurant in Opole) |
| 3 Google Play | Pending (SE: Risk) | 2026-09-24 | [SmakoBao Play](https://play.google.com/store/apps/details?id=com.restaumatic.smakobao_production&hl=en) | "SmakoBao - Apps on Google Play" |
| 4 Domains | Pending | 2026-09-24 | RDAP blocked | SE: [smako.store](https://au.trustpilot.com/review/smako.store) in use; "Smako Group" at smakogroup.com |
| 5 Trademarks | Pending | 2026-09-24 | — | "™" claimed by SMAKO™ (registration status unknown) |
| 6 Language | Inconclusive | 2026-09-24 | Reviewer | "smack" echo in EN |
| 7 Similarity | Risk | 2026-09-24 | as above; [Smakoza](https://smakoza.pl/) | Smaker, SMAKO™, Smakoza (PL restaurant ordering) |
| 8 Handles | Pending (SE: Risk) | 2026-09-24 | [@smako.mp3 (via SE)](https://www.instagram.com/smako.mp3/), [@smakoart (via SE)](https://www.instagram.com/smakoart/) | Exact and near handles in use |

---

#### `Porcio`

- **Concept:** "Portion" across PL, ES and Esperanto. **Pronunciation:** PL [ˈpɔrt͡sjɔ]; EN "POR-see-oh" or "POR-shee-oh"; an Italian reader says "POR-cho". The spelling-to-sound mismatch hurts C2.
- **Language risk:** FR/CA "porc" and IT "porco" (pig; also part of common Italian blasphemies), ES "porcino". A pig association in a food and body context is unfortunate (C3).

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk | 2026-09-24 | [PorcioFOOD Instagram (via SE)](https://www.instagram.com/porciofood/), [Porció Élelmiszeripari (via SE)](https://www.facebook.com/PorcioEK/?locale=hu_HU) | Hungarian healthy-meal delivery "PorcioFOOD"; a Hungarian meat processor |
| 2 App Store | Pending (SE: Risk) | 2026-09-24 | [Portio AI](https://apps.apple.com/us/app/portio-ai/id6754779401) | "Portio AI App" (photo calorie tracker): one letter apart, same category |
| 3 Google Play | Pending (SE: Risk) | 2026-09-24 | [Porció](https://play.google.com/store/apps/details?id=hu.porciobp&gl=US) | "Porció - Apps on Google Play" (Budapest food delivery) |
| 4 Domains | Pending | 2026-09-24 | RDAP blocked | SE: nothing for porcio.com / .app / .pl / .io (not evidence of availability) |
| 5 Trademarks | Pending | 2026-09-24 | — | — |
| 6 Language | Risk | 2026-09-24 | [Wiktionary (via SE)](https://en.wiktionary.org/wiki/porcio) | Esperanto "porcio"; pig connotations as above |
| 7 Similarity | Risk | 2026-09-24 | as row 2 | Portio / Portio AI |
| 8 Handles | Pending (SE: Risk) | 2026-09-24 | as row 1 | @porciofood |

---

#### `Yemo`

- **Concept:** "Jem / jemy" (I eat / we eat), spelled for English readers. **Pronunciation:** EN "YEH-moh"; a Pole who hears it will write "jemo", which is ambiguous.

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk | 2026-09-24 | [yemo.ai](https://yemo.ai/) | "YeMo.ai"; a Yemo restaurant-ordering app (per the SE summary) |
| 2 App Store | Pending (SE: Risk) | 2026-09-24 | [Yemmi](https://apps.apple.com/us/app/yemmi-food-macro-tracker/id6749887396) | "Yemmi: Food & Macro Tracker": similar sound, same category |
| 3 Google Play | Pending (SE: Risk) | 2026-09-24 | [Yemo-Chat](https://play.google.com/store/apps/details?id=com.yemo.chat&hl=en) | "Yemo-Chat&video" |
| 4 Domains | Pending | 2026-09-24 | RDAP blocked | yemo.ai in use (SE) |
| 5 Trademarks | Pending | 2026-09-24 | — | — |
| 6 Language | Risk | 2026-09-24 | Reviewer | PL/EN spelling mismatch; faint "Yemen" echo |
| 7 Similarity | Risk | 2026-09-24 | as row 2 | Yemmi |
| 8 Handles | Pending (SE: Risk) | 2026-09-24 | [@yemo.dj (via SE)](https://www.instagram.com/yemo.dj/) | Several Yemo accounts in use |

---

#### `Pora`

- **Concept:** PL "pora" = time or season ("pora obiadu", lunchtime; "pora na plan", time to plan). **Pronunciation:** PL [ˈpɔra]; EN "POR-uh".
- **Language risk:** PT "porra" (vulgar interjection) is a near-homophone. In Poland, it sounds close to "Pola", a well-known Polish food-origin app.

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk | 2026-09-24 | [palta.com/pora](https://palta.com/pora), [poraapp.com](https://www.poraapp.com/) | Pora.ai skin-health app (Palta); Pora diaspora networking app |
| 2 App Store | Pending (SE: Risk) | 2026-09-24 | [Pora](https://apps.apple.com/us/app/pora/id1589757343), [Pora — Did I today?](https://apps.apple.com/us/app/pora-did-i-today/id6768423829) | Several "Pora" apps |
| 3 Google Play | Pending (SE: Risk) | 2026-09-24 | [Pora video chat](https://play.google.com/store/apps/details?id=com.live.streamer.online.app.video&hl=en_US) | "Video Chat & Video Call - Pora" |
| 4 Domains | Pending | 2026-09-24 | RDAP blocked | — |
| 5 Trademarks | Pending | 2026-09-24 | — | — |
| 6 Language | Risk | 2026-09-24 | Reviewer | as above |
| 7 Similarity | Risk | 2026-09-24 | [Pola article](https://www.portalspozywczy.pl/handel/wiadomosci/aplikacja-quot-pola-quot-wprowadzi-wlasny-znak-towarowy-dla-polskiej-zywnosci,161623.html) | "Aplikacja 'Pola' wprowadzi własny znak towarowy dla polskiej żywności" |
| 8 Handles | Pending (SE: Risk) | 2026-09-24 | [@getpora (via SE)](https://www.instagram.com/getpora/) | "Pora App (@getpora)" |

---

#### `Miska`

- **Concept:** PL "bowl". **Pronunciation:** PL [ˈmiska]; EN "MISS-kuh".
- **Language risk:** in Polish, "miska" strongly suggests a pet bowl ("miska dla psa").

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk | 2026-09-24 | [Miskaa Play](https://play.google.com/store/apps/details?id=com.miskaa.recipes&hl=en_US&gl=US), [Miska Gastro Bowls (via SE)](https://www.instagram.com/p/DJER4_5NXTW/) | "Miskaa - Live Cooking Class, Meal Plan & Recipes"; PL bowl restaurants |
| 2 App Store | Pending (SE: Risk) | 2026-09-24 | [miska](https://apps.apple.com/kz/app/miska/id6443659195) | "miska - App Store" |
| 3 Google Play | Pending (SE: Risk) | 2026-09-24 | [Miska](https://play.google.com/store/apps/details?id=com.nikolai.miska&hl=en), [МИСКА](https://play.google.com/store/apps/details?id=ru.foodapp.loyalty.miska&hl=en_US) | Several, including a food-delivery loyalty app |
| 4 Domains | Pending | 2026-09-24 | RDAP blocked | — |
| 5 Trademarks | Pending | 2026-09-24 | — | — |
| 6 Language | Risk | 2026-09-24 | Reviewer | Pet-bowl association |
| 7 Similarity | Risk | 2026-09-24 | as row 1 | Miskaa (one letter apart, same category) |
| 8 Handles | Pending (SE: Risk) | 2026-09-24 | [@miska.bowls (via SE)](https://www.instagram.com/miska.bowls/) | Bowl restaurants hold the variants |

---

#### `Doma`

- **Concept:** "At home": home cooking. **Pronunciation:** PL [ˈdɔma]; EN "DOH-muh". **Language risk:** in US English, "DOMA" is the Defense of Marriage Act acronym, which is politically charged.

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk | 2026-09-24 | [Doma.ai LinkedIn (via SE)](https://www.linkedin.com/company/domaai) | Doma (real estate, doma.com), Doma.ai (proptech) |
| 2 App Store | Pending (SE: Risk) | 2026-09-24 | [DonJoy DOMA](https://apps.apple.com/us/app/donjoy-doma/id6446365115) | Medical ordering app, among others |
| 3 Google Play | Pending (SE: Risk) | 2026-09-24 | [Doma](https://play.google.com/store/apps/details?id=ai.doma.client&hl=en_US) | Property-management app |
| 4 Domains | Pending (SE: Risk) | 2026-09-24 | SE summary | "Doma's official website is www.doma.com" |
| 5 Trademarks | Pending | 2026-09-24 | — | — |
| 6 Language | Risk | 2026-09-24 | Reviewer | DOMA acronym |
| 7 Similarity | Risk | 2026-09-24 | as above | Large namesakes |
| 8 Handles | Pending (SE: Risk) | 2026-09-24 | [@domaofficial (via SE)](https://www.instagram.com/domaofficial/), [TikTok @doma.official (via SE)](https://www.tiktok.com/@doma.official) | "DOMA (@domaofficial)" 125K per the SE summary |

---

#### `Akurat`

- **Concept:** PL "just right / exactly". **Pronunciation:** PL [aˈkurat]; EN "ACK-yoo-rat" (ends in "rat").
- **Main risk:** in Poland it strongly suggests the band Akurat.

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk | 2026-09-24 | [Akurat.co Play](https://play.google.com/store/apps/details?id=com.promedia.akurat&hl=en), [Akurat Lighting](https://www.akurat.lighting/pl/), [ALEO](https://aleo.com/int/company/v4bg-spolka-z-ograniczona-odpowiedzialnoscia) | Indonesian news app; film lighting brand; "AKURAT SPÓŁKA Z O.O., WARSZAWA … Restaurants" |
| 2 App Store | Pending (SE: Risk) | 2026-09-24 | [Akurat Kompas](https://apps.apple.com/id/app/akurat-kompas/id1069599397?l=id) | Several "Akurat" utilities |
| 3 Google Play | Pending (SE: Risk) | 2026-09-24 | as row 1 | "Akurat.co - Apps on Google Play" |
| 4 Domains | Pending (SE: Risk) | 2026-09-24 | SE summary | "akurat.pl is the official website for Akurat, a Polish band" |
| 5 Trademarks | Pending | 2026-09-24 | — | — |
| 6 Language | Risk | 2026-09-24 | Reviewer | "-rat" in EN |
| 7 Similarity | Risk | 2026-09-24 | [Wikipedia (via SE)](https://en.wikipedia.org/wiki/Akurat) | Band |
| 8 Handles | Pending (SE: Risk) | 2026-09-24 | [@akuratco (via SE)](https://www.instagram.com/akuratco/) | 154K per the SE summary |

---

#### `Zapas`

- **Concept:** PL "na zapas" = made ahead or for later, the meal-prep idea. **Pronunciation:** PL [ˈzapas]; EN "ZAP-us". **Language risk:** Spanish colloquial "zapas" = sneakers.

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk | 2026-09-24 | [Za-Pas Knives](https://www.zapas-knives.pl/en_US/index) | PL knife brand; Spanish espadrille brand |
| 2 App Store | Pending (SE: Risk) | 2026-09-24 | [Zapas SRL](https://apps.apple.com/gb/developer/zapas-srl/id1844048861) | Developer "Zapas SRL" |
| 3 Google Play | Pending (SE: Risk) | 2026-09-24 | [Apps by Zapas](https://play.google.com/store/apps/developer?id=Zapas) | Developer "Zapas" |
| 4 Domains | Pending (SE: Risk) | 2026-09-24 | [zapas.com](https://zapas.com/), [zapas.app](https://zapas.app/) | "ZAPAS.COM \| Strategic-Grade domain names…" (broker listing); zapas.app is a live JS application |
| 5 Trademarks | Pending | 2026-09-24 | — | — |
| 6 Language | Risk | 2026-09-24 | Reviewer | ES slang |
| 7 Similarity | Risk | 2026-09-24 | as above | — |
| 8 Handles | Pending (SE: Risk) | 2026-09-24 | [FB zapasapp (via SE)](https://www.facebook.com/zapasapp/) | "Zapas app" page exists |

---

#### `Kredens`

- **Concept:** PL kitchen dresser or cupboard: pantry and planning. **Pronunciation:** PL [ˈkrɛdɛns]; EN hears "credence".

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk | 2026-09-24 | [@restauracjakredens (via SE)](https://www.instagram.com/restauracjakredens/), [@krynicki_kredens (via SE)](https://www.instagram.com/krynicki_kredens/) | Many PL restaurants named Kredens |
| 2 App Store | Pending (SE: Risk) | 2026-09-24 | [Kredens Pizza Italiana](https://apps.apple.com/se/app/kredens-pizza-italiana/id6443875226) | Restaurant ordering app |
| 3 Google Play | Pending (SE: Inconclusive) | 2026-09-24 | SE filtered | No exact match shown |
| 4 Domains | Pending (SE: Risk) | 2026-09-24 | [kredens.pl](https://www.kredens.pl/) | "Strona domeny kredens.pl" (in use) |
| 5 Trademarks | Pending | 2026-09-24 | — | — |
| 6 Language | Inconclusive | 2026-09-24 | Reviewer | "credence" / "credit" echo |
| 7 Similarity | Risk | 2026-09-24 | as row 1 | — |
| 8 Handles | Pending (SE: Risk) | 2026-09-24 | as row 1 | Variants held by restaurants |

---

#### `Prepko`

- **Concept:** Prep + PL diminutive -ko. **Pronunciation:** PL [ˈprɛpkɔ]; EN "PREP-koh". Tied to meal prep (C7).

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk | 2026-09-24 | [Jewish Journal](https://jewishjournal.com/community/237730/prepko-kosher-version-blue-apron/) | "Prepko: The Kosher Version of Blue Apron" (US meal-kit service; current activity unknown) |
| 2 App Store | Pending (SE: Inconclusive) | 2026-09-24 | SE filtered | Nearest: "PrepOK", "The Prep Kitchen" |
| 3 Google Play | Pending (SE: Risk) | 2026-09-24 | [Prepko - Анатомия](https://play.google.com/store/apps/details?id=boyanov.prepko2&hl=lv&gl=US) | Anatomy study app with the exact name |
| 4 Domains | Pending | 2026-09-24 | RDAP blocked | — |
| 5 Trademarks | Pending | 2026-09-24 | — | — |
| 6 Language | Inconclusive | 2026-09-24 | Reviewer | No issue found |
| 7 Similarity | Risk | 2026-09-24 | as row 1 | Same-name meal kit (classes 29/30/35) |
| 8 Handles | Pending (SE: Risk) | 2026-09-24 | [@prepkosher (via SE)](https://www.instagram.com/prepkosher/), [YouTube @Prepko (via SE)](https://www.youtube.com/@Prepko) | Held by the meal kit |

---

## 7. Risks and unresolved checks

**Session-level limits**
1. **No authoritative check could run.** Every store, domain, trademark and handle status is Pending (§5.1). Rankings rest on search-engine evidence, which can miss registered marks, unlaunched apps, and parked or reserved domains.
2. **Absence is not availability.** Where the search found nothing (for example Ramekin in the app stores, or Smakora and Oskoma for .com/.app), the status is Inconclusive. It must not be read as "free".
3. **Language checks are the reviewer's own assessment.** Native-speaker checks are pending for PL, EN (UK and US), DE, FR, ES, IT, PT, SV, CS and UK/RU, the languages where issues were flagged.
4. **Trademark reality.** Common-word names (Tadam, Pora, Doma, Miska, Akurat, Zapas, Kredens) are likely to have several registrations across classes. Coined or archaic names (Smakora, Oskoma) and arbitrary-use words (Ramekin) are likely stronger, but only a registry search and an attorney can say.

**Name-specific risks (top 3 and alternate)**

| Name | Main remaining risk | What would resolve it |
|---|---|---|
| Ramekin | Possible descriptiveness for recipe content; moderate PL familiarity; .com very likely registered (unverified) | Registry TM search in classes 9/42/44/41; RDAP for ramekin.com/.app/.pl/.io; a 5–10 person PL comprehension test |
| Oskoma | Polish restaurants use the name (class 43); "-oma" sounds medical to English ears; RU "fed up" idiom; oskoma.pl may be brokered | UPRP and EUIPO search in classes 43, 35 and 9/42; RDAP for oskoma.pl; EN listener test |
| Smakora | Identical Swedish recipe publication; neighbours on the "smak" stem (Smaker, SMAKO™) | TMview including the Swedish office; an EUIPO phonetic search for SMAK*; attorney view on coexistence with Smaker |
| Tadam (alternate) | Same-name class 9 software and consumer brands; weak distinctiveness | EUIPO/UPRP search; attorney view |

**Open checks per shortlisted name:** App Store (iTunes API PL/US/GB), Google Play (PL/US), RDAP for .com, .app, .io and .pl, EUIPO, TMview (EM + PL + SE), UPRP, WIPO, USPTO, UK IPO, and handles on Instagram, TikTok, Facebook, YouTube, X, Threads and LinkedIn. All are Pending.

---

## 8. Next verification steps

### 8.1 Re-run on a network with registry access (agent, next session)

Run these for Ramekin, Oskoma, Smakora and Tadam first, then the rest of §6. Replace `<n>` with the lowercase name.

- App Store: `https://itunes.apple.com/search?term=<n>&entity=software&country=pl` (then `us`, `gb`)
- Google Play: `https://play.google.com/store/search?q=<n>&c=apps&gl=PL` (then `gl=US`)
- .com: `https://rdap.verisign.com/com/v1/domain/<n>.com`
- .app: `https://pubapi.registry.google/rdap/domain/<n>.app`
- .pl and .io: get the RDAP base URL for `pl` and `io` from `https://data.iana.org/rdap/dns.json`, then `<base>/domain/<n>.pl` and `<base>/domain/<n>.io`

### 8.2 Owner actions (need an account, or are the owner's call)

1. **Trademark searches** until the agent can reach the registries. Search each name as an exact word, then with a wildcard and phonetically:
   - **EUIPO eSearch plus** (https://euipo.europa.eu/eSearch/): Trade marks, "Word" = `RAMEKIN` (then `OSKOMA`, `SMAKORA`, `TADAM`). Nice classes 9, 29, 30, 35, 41, 42, 43, 44. Status: all, then filed and registered only. Repeat with `SMAK*` and `OSKOM*`.
   - **TMview** (https://www.tmdn.org/tmview/): the same terms. Offices: EM, PL, SE, DE, FR, ES, IT, WO. Same classes. Note live and dead status, owner and filing date.
   - **UPRP e-Wyszukiwarka** (https://ewyszukiwarka.pue.uprp.gov.pl/): "Znaki towarowe", word element `ramekin` / `oskoma` / `smakora` / `tadam`, plus `smak*` and `oskom*`.
   - **WIPO Global Brand Database** (https://branddb.wipo.int/): Brand = the name, Nice classes as above, designations PL/EU/US/GB.
   - **USPTO** (https://tmsearch.uspto.gov/) and **UK IPO** (https://trademarks.ipo.gov.uk/): exact and phonetic, classes 9, 42 and 44.
2. **App Store Connect name check:** needs the owner's Apple Developer account. Try reserving the app name only when ready to commit, since Apple holds reservations for a limited time.
3. **Google Play Console check:** needs the owner's developer account.
4. **Trademark attorney clearance** in at least the EU (EUIPO) and Poland (UPRP), plus the US and UK if English-speaking launches are planned, **before adoption**. Nothing here is a legal opinion.
5. **Social handles:** only signing up confirms a handle is free. The owner decides whether to sign up for `<name>`, `<name>app`, `get<name>` and `<name>.pl` on Instagram, TikTok, Facebook, YouTube, X, Threads and LinkedIn.
6. **Domain purchase decisions:** the owner buys; the agent never does. Decide whether to accept a variant domain (`get<name>.com`, `<name>.app`) or pay broker prices (zapas.com appears broker-listed; oskoma.pl appears for sale, both unverified).
7. **Native-speaker and audience test:** 5–10 people from the PL wedge plus 3–5 native English speakers. Test pronunciation after hearing each name once, spelling, associations and appeal for Ramekin, Oskoma, Smakora and Tadam.

**Do not** rename application identifiers, bundle IDs, packages, domains or assets until the Product Owner approves a final name (CLAUDE.md).

---

## 9. Official sources

| Check | Source |
|---|---|
| EU trademarks | EUIPO eSearch plus: https://euipo.europa.eu/eSearch/ |
| EU + national trademarks (incl. Poland) | TMview: https://www.tmdn.org/tmview/ |
| Polish trademarks | UPRP e-Wyszukiwarka: https://ewyszukiwarka.pue.uprp.gov.pl/ |
| International trademarks | WIPO Global Brand Database: https://branddb.wipo.int/ |
| US trademarks | USPTO: https://tmsearch.uspto.gov/ |
| UK trademarks | UK IPO: https://trademarks.ipo.gov.uk/ |
| .com registration | Verisign RDAP: `https://rdap.verisign.com/com/v1/domain/<name>.com` |
| .app registration | Google Registry RDAP: `https://pubapi.registry.google/rdap/domain/<name>.app` |
| Other TLDs | IANA RDAP bootstrap: https://data.iana.org/rdap/dns.json |
| App Store | iTunes Search API: `https://itunes.apple.com/search?term=<name>&entity=software&country=pl` |
| Google Play | `https://play.google.com/store/search?q=<name>&c=apps&gl=PL` |

---

## 10. Changelog

| Date | Change |
|---|---|
| 2026-09-24 | Report created with the brief, criteria and templates. No research run yet. |
| 2026-09-24 | First research session (brand-researcher). Only WebSearch was available; all registry, store, trademark and social sources were egress-blocked (§5.1), so every authoritative check is Pending. Added: product positioning (§1), naming strategy (§2), competitor landscape for PL and international (§3), a 73-name longlist with screen results (§4), a dated evidence log (§5), a 14-name shortlist with check matrix, scores and per-name evidence (§6), risks (§7) and next steps with owner actions (§8). Recommended for further investigation, not selected: Ramekin, Oskoma, Smakora (alternate: Tadam). No earlier findings existed, so nothing was superseded. |
