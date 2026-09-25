# FitMeal AI: brand name research

Maintained by the `brand-researcher` agent ([.claude/agents/brand-researcher.md](../../.claude/agents/brand-researcher.md)). Findings go to the `engineering-manager`. Choosing the brand requires Product Owner approval (CLAUDE.md). Nothing in this report is a naming decision, and nothing here is legal clearance.

"FitMeal AI" is the working title. This report looks for the product's public brand name.

**Status (2026-09-24): second research session done (international-first round). Live access is still limited.**

> **Product Owner feedback on session 1:** "Smakora is mostly a Polish name, like most of them." Eleven of the fourteen session-1 shortlisted names were Polish-rooted (Oskoma, Smakora, Smako, Doma, Akurat, Miska, Pora, Kredens, Zapas, Prepko, Yemo). The product launches in Poland and then expands internationally, so the brand must not read as a Polish word. Session 2 re-ran the naming international-first (§2.1) and rebuilt the shortlist (§6). Session-1 conclusions that this changes are marked **superseded**. They have not been deleted.

> **Live web access, sessions 1 and 2: partial.** Only **WebSearch** (a search engine) worked. At the start of session 2, each official source was retried once with a single plain request. Every one was still **blocked by the network egress proxy**: registry RDAP (.com, .app, the IANA bootstrap), the iTunes Search API, Google Play, EUIPO, TMview, UPRP, WIPO Brand DB, USPTO and UK IPO. Per the task, no workaround was attempted: no proxy probing, no `whois` or `dig` substitutes, no mirror sites. Details are in §5.1.
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

**Markets and languages.** Poland first, Polish and English from day one, EU hosting, iOS App Store launch (Plan §3, §9). Later English-speaking and other EU markets. **Session 2 (PO feedback): the brand itself must read as international, not Polish (§2.1).**

**Brand personality.** Practical, confident, food-positive, a little playful, and precise without being clinical. It should feel like a friend who is good with numbers and good in the kitchen. Never moralizing ("guilt-free", "cheat", "slim"), never medical (PRD §12, Plan §11 App Review risk), and never "the AI decides" (PRD §5 principle 10).

**Positioning statement (working).** For people in Poland who track what they eat but won't give up the food they love, [Brand] is the meal planner that makes any recipe fit your numbers, your budget and your prep day, and shows you exactly what it changed.

**Positioning statement, international version (session 2, working).** For people who track what they eat but won't give up the food they love, [Brand] is the meal planner that makes any recipe fit your numbers, your budget and your prep day, and shows you exactly what it changed.

---

## 2. Naming strategy

### 2.1 International-first (session 2, current)

**Why this changed.** The Product Owner's review of session 1: "Smakora is mostly a Polish name, like most of them." The launch is in Poland, but the plan is to expand internationally (PRD §3 wedge, PRD §13 roadmap, Plan §3 Polish + English from day one), so **the brand must not read as a Polish word.** Polish stays the first market to test the name in, not the language the name comes from.

**Rules for session 2:**
1. **Meaning and sound must not depend on Polish.** Allowed sources:
   - invented or coined words with no single-language root;
   - short tech-style brands;
   - Latin, Romance or pan-European roots that most Europeans recognise;
   - English-readable food, wellbeing or lifestyle words used in a new way.
2. **A Polish speaker must still say it right on first read.** Prefer letters that sound the same in Polish and English (a, e, i, o, u, b, d, f, g, k, l, m, n, p, r, s, t, z). Avoid c, j, w, y, ch, sz and cz. Session 2 found two more Polish reading traps:
   - In Polish, "si", "zi", "ni" and "ci" before a vowel are softened, so "Edesia" is read "e-DE-śa". Avoid those clusters.
   - Poles read English words with a silent "e" or a long "a" letter by letter ("plate", "taste", "staple", "savour"). Such words fail C2 unless the Polish reading is also acceptable.
3. **Form:** 4–8 characters, 1–2 syllables where practical, no diacritics, hyphens or numbers. The store title with a descriptor must fit 30 characters.
4. **Product principles:** no medical or "diet guilt" connotations (PRD §5, §12), nothing that suggests the AI decides (PRD §5 principle 10), and nothing close to the §3 competitors.
5. **No reuse** of names already in §4.1–§4.5.

**What session 2 learned (evidence in §3.4 and §5.3):**
- **Real Romance and English food words are now as crowded as English kitchen nouns were in session 1.** Same-category apps (meal planning, recipe import or macro tracking) exist for Sapora, Plendo, Modo, Adapto, Gramo, Melo, Metron, Trofi, Manna, Aldenté, Larder, Simmer, Skillet, Prato and Kulina. Several of them describe features very close to ours. Sapora imports social-media recipes with macros per portion, and Adapto "adapts the meals you already want".
- **A word that is descriptive or laudatory in any one EU language makes a weak EU trademark.** EUIPO assesses descriptiveness in every EU language. That counts against Portata (Italian for "a course of a meal") and Ottimo (Italian for "excellent"), and to some degree against any real word used for its own meaning.
- **"Apt-" reads as "apteka" (pharmacy) to Poles.** Both Aptelo and Aptimo turned up Polish pharmacy businesses (§5.3). Avoid the stem for the Polish market (C5).
- **"Por-" names sit next to Portio AI (§3.2) and PORTA (Italian ready meals sold in US retail).**
- **The cleanest openings were:** a metaphor from outside food (Tangram: pieces that always fit), arbitrary use of a known object or measure (Ramekin, Palmo), and new coinages built on pan-European roots (Sapimo).

**What still holds from session 1:** avoid "Fit-", "Meal-" and "AI" in the brand, and expect short English food words to be taken (§2.2).

### 2.2 Session-1 strategy (2026-09-24; partly superseded)

> **Superseded 2026-09-24 (PO feedback):** the session-1 conclusion that "the best openings are Polish-rooted words that an English speaker can read phonetically" no longer applies. §2.1 replaces it. The other session-1 findings below still hold. The text is kept as written.

**Directions explored (PO Phase 2):** (1) invented, distinctive words; (2) short tech-style brands; (3) food, nutrition and wellbeing words; (4) abstract lifestyle words; (5) international names that work in Polish and English, including Polish-rooted words that an English speaker can read.

**What the market research implies (§3):**
- **Avoid the "Fit-" prefix.** It is saturated in Poland (Fitatu, Fit Foczki, Fit-World, FitChoice, Fitia). The working title "FitMeal" falls into this crowded pattern and would be a weak mark (C1).
- **Avoid "Meal-" compounds** (Mealime, MealPrepPro, MealBoard, MealPreper, Mealll). They are descriptive and hard to register.
- **Avoid "AI" in the brand.** Store titles in this category already overuse it ("Fitatu Licznik Kalorii AI", "Portio AI", "Tamu"), and C7 rules it out.
- **Short English food words are heavily taken by recipe apps.** Morsel, Mise, Tavola, Paprika, Crouton, Pestle, Honeydew, Whisk and Gusta/Gustino were all found in use this session (§5.2).
- ~~**The best openings are Polish-rooted words that an English speaker can read phonetically, and distinctive coinages.**~~ *(Superseded by §2.1.)* Letters that sound the same in Polish and English: a, e, i, o, u, b, d, f, g, k, l, m, n, p, r, s, t, z. Avoid c, j, w, y, ch, sz, cz, rz, and anything with ł, ą or ę.

**Preferred form (from the PO brief):** 4–8 characters, one to three syllables, no diacritics, hyphens or numbers, a store title that fits the 30-character limit with a descriptor (for example "Smakora: Meal Planner" is 21 characters).

### 2.3 Naming criteria

C1–C9 are unchanged from session 1. C10 was added in session 2 after the PO feedback.

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
| **C10** | **International neutrality:** meaning and sound don't depend on one language, and no bad meaning is known in DE, FR, ES, IT, PT, NL or SV. Scored 1–5: 5 = coined or understood the same way across Europe; 3 = a real word from one non-Polish language that reads as foreign-but-friendly elsewhere; 1 = only makes sense in Polish. | PO feedback, session 2 |

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
| **Eat This Much** | Auto meal plans for calorie, macro and budget targets | [Eat This Much blog](https://blog.eatthismuch.com/best-meal-planning-apps/) | Phrase. **Closest international functional competitor** |
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

> **Superseded in part (2026-09-24, PO feedback):** takeaway 3 pointed session 1 towards Polish words. Session 2 looks for the same meanings (craving, taste, portion, fit) in international forms (§2.1). See §3.4 for the same-category apps found in session 2.

### 3.4 Same-category apps found in session 2

Checked 2026-09-24 via WebSearch only. These apps surfaced while screening the session-2 candidates. None of the pages could be opened (egress-blocked), so the descriptions are the search results' titles and summaries, not verified store data.

| Brand | What the search showed | Link | Relevance |
|---|---|---|---|
| **Sapora** | "Sapora — Stop scrubbing videos. Start cooking." The summary says it reads TikTok, Instagram and YouTube recipes and gives "macros per portion", and it can "plan your week" | [sapora.app](https://sapora.app/) | **Very close to PRD §8.1 and §8.3** (social import plus per-portion macros) |
| **Adapto** | "Make the Meals You Already Want… Better. \| The meal adaptation app for real-life kitchens" | [studio.com](https://studio.com/apps/jeremy/adapo) | **Same core promise** as PRD §1 |
| **MODL** | "MODL - Hit your macros with real food": a week of recipes that add up to your targets, plus a grocery list | [joinmodl.app](https://www.joinmodl.app/) | Close to PRD §8.5 and §8.10 |
| BonApp! | "BonApp! Recipes & Meal Planner": social recipe import, macro targets, nutrition breakdown, meal planner | [bonapp.recipes](https://bonapp.recipes/) | Close functional overlap |
| Plendo | "Plendo — Fuel, refined.": personalised sports-nutrition meal plans | [plendo.app](https://plendo.app/) | Adaptive plans |
| Modo | "Modo \| Digital Nutritionist App" | [getmodo.io](https://www.getmodo.io/) | AI diet plans |
| Melo AI | "Melo AI \| Your Adaptive Diet Coach" | [meloai.app](https://www.meloai.app/) | Adaptive diet plans |
| Manna AI | "Manna AI — AI-Powered Meal Planner": weekly plan, shopping list, pantry | [mannaaiinc.com](https://mannaaiinc.com/) | Planner with pantry |
| Aldenté | "Aldenté Cookbook, Recipe Saver App": TikTok and Instagram import, weekly plan, grocery list | [aldente.kitchen](https://aldente.kitchen/) | Recipe import |
| Potto | "Potto: Meal Planner & Recipes": budget-based weekly plans | [App Store](https://apps.apple.com/us/app/potto-meal-planner-recipes/id6778760884) | Planner with a budget angle (cf. PRD §8.8) |
| Simmerly | "Simmerly: Meal planning for great dinners all week" ("make-ahead prep, planned leftovers") | [simmerly.app](https://simmerly.app/) | Meal-prep angle |
| Larder / The Larder | Several meal-planner and recipe apps with this name | [thelarder.app](https://www.thelarder.app/), [cookwithlarder.com](https://www.cookwithlarder.com/) | Planner |
| Sabora | "Sabora: Recipes & Meal Planner" | [Google Play](https://play.google.com/store/apps/details?id=com.sabora.ai&hl=fil) | Planner |
| Culina | "Culina - Your Personal Meal Planning Assistant" | [culina.food](https://www.culina.food/) | Planner |
| Tera | "AI Dietitian & Meal Plans:Tera" | [App Store](https://apps.apple.com/us/app/ai-dietitian-meal-plans-tera/id1608429635) | AI diet plans |
| Gramo, Metron, trofi foods, Eato | AI or photo macro trackers | [gramo.space](https://gramo.space/), [metronapp.xyz](https://www.metronapp.xyz/marketing), [trofi foods](https://apps.apple.com/us/app/trofi-foods/id6502950424), [Eato](https://play.google.com/store/apps/details?id=com.eato.caloriecounter.weight.loss&hl=en_US) | Trackers |
| saviMon | "saviMon: Food & Supplements App": food, medication and vitamin tracker | [App Store](https://apps.apple.com/us/app/savimon/id6760576803) | Tracker (health) |

**Takeaway.** The international "import a recipe, fit it to your macros, plan the week" space is filling quickly, and several apps (Sapora, Adapto, MODL, BonApp!) are close to PRD §1. The brand can't rely on a food word to explain the product: the store descriptor ("…: Meal Planner") and the product have to do that. The name's job is to be **distinctive and ownable**.

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

Result (session 1): 14 names shortlisted. The PO asked for 10–15. *(Superseded 2026-09-24: the shortlist was rebuilt international-first in session 2; see §4.6 and §6.)*

### 4.6 Session 2: international-first longlist (74–160)

87 new names were generated on 2026-09-24 under the §2.1 rules. None of them is in §4.1–§4.5. "Search" means a WebSearch screen was run that day (evidence in §5.3). "Judgment" means the name was screened out on linguistic, strategic or reviewer-knowledge grounds; where reviewer knowledge was used, it says so and the name was not searched. A name screened out by judgment is not claimed to be taken.

#### 4.6.1 Invented or coined words (no single-language root)

| # | Name | Idea behind it | Screen result |
|---|---|---|---|
| 74 | Sapimo | Latin *sapor* (taste), alive in IT *sapore*, ES/PT *sabor*, FR *saveur*, with an open "-imo" ending: taste first | **Shortlisted** |
| 75 | Savimo | "Savour" / FR *saveur* / "savvy": tasty and smart | **Shortlisted** (with Risk) |
| 76 | Aptimo | Latin *aptus* (fitting) + *optimum*: it fits, optimally | Screened out (search): aptimo.pl is a Polish online pharmacy ("AptimO.pl Dla zdrowia"); to Poles "apt-" reads as "apteka" (pharmacy) (C5); an "Aptimo." developer on Google Play; visually near Aprimo (marketing software) |
| 77 | Aptelo | apt + "-elo" | Screened out (search): Aptelo sp. z o.o. with the Facebook page @namierzamyleki ("we track down medicines"), the same apteka echo (C5); aptelo.com listed for sale |
| 78 | Sapora | *sapor* + "-a" | Screened out (search): Sapora, a recipe-import app with per-portion macros (sapora.app), plus a Sapora spice brand (sapora.com) |
| 79 | Plendo | Plenty + blend | Screened out (search): Plendo, a sports-nutrition meal-planning app (plendo.app) |
| 80 | Mezura | Blend of IT *misura* / FR *mesure* / EN "measure" | Screened out (search): "Mezura" cut-planning app on the App Store |
| 81 | Tomalo | Tomato + ES *tómalo* ("take it") | Screened out (search): "Tómalo" retail app; Tomalo Radio |
| 82 | Melo | Melon / melody / mellow | Screened out (search): Melo AI adaptive diet coach; Melo AI family organizer (meal plans) |
| 83 | Gramo | Gram + "-o" (also ES "gram") | Screened out (search): Gramo AI macro tracker (gramo.space); also frames the product as a tracker (C4) |
| 84 | Adapto | "I adapt" (ES/IT/PT) | Screened out (search): a "meal adaptation app" with the same core promise |
| 85 | Tavelo | IT *tavola* (table) + "-elo" | Screened out (search): Tavelo bikes; weak idea |
| 86 | Tavimo | IT *tavola* + "-imo" | Screened out (judgment): no clear idea behind it (a grouped search found nothing, which is Inconclusive) |
| 87 | Bonimo | FR/IT *bon/buono* + "-imo" | Screened out (search): "Bonimo: Gutscheine sofort" voucher app (DE) |
| 88 | Fornelo | IT *fornello* (stove) | Screened out (search): "Fornello" apps (retail, fast food) |
| 89 | Kaldo | *Caldo* (broth, warm) spelled with a K | Screened out (search): Kaldo pub app; Kaldo's restaurant app |
| 90 | Nomeo | "Nom" (eat) + "-eo" | Screened out (search): Nomeo, a digital-nomad community app |
| 91 | Sumisura | IT *su misura* (made to measure) | Screened out (search): Sumisura resume-tailoring tool and a bespoke-shirt maker; 4 syllables |
| 92 | Menora | Menu + "-ora" | Screened out (judgment): reads as "menorah" |
| 93 | Tadora | Coined | Screened out (judgment): believed to be a tadalafil drug brand (reviewer knowledge, not searched) (C5) |
| 94 | Alimo | Latin *alimentum* (food) | Screened out (judgment): Polish "alimenty" means child-support payments (C3) |
| 95 | Apetto | Appetite + IT "-etto" | Screened out (judgment): too close to apetito AG, the German frozen-meals company (seen in §5.3 results for "Etto") |

#### 4.6.2 Short tech-style brands

| # | Name | Idea behind it | Screen result |
|---|---|---|---|
| 96 | Tangram | The seven-piece puzzle whose pieces always fit into one shape: your recipes, macros, budget and prep day fitted into a plan | **Shortlisted** (with Risk) |
| 97 | Palmo | Handspan in IT/ES/PT, echoing EN "palm": portions judged by hand, and a plan in the palm of your hand | **Shortlisted** (with Risk) |
| 98 | Apto | "Suitable, fit" (ES/PT/IT; EN "apt") | Screened out (search): "Apto" health app (Latin America) combining diet with medical records; Apto commercial real-estate software (apto.com); in Spanish food labelling "apto para…" is descriptive |
| 99 | Modo | "Way, mode" (IT/ES/PT) | Screened out (search): "Modo \| Digital Nutritionist App" |
| 100 | Ritmo | "Rhythm" (IT/ES/PT) | Screened out (search): "Ritmo" routine-tracker app on Google Play |
| 101 | Etto | IT hectogram (100 g) | Screened out (search): sounds close to "Eato", a calorie counter |
| 102 | Listo | ES "ready" | Screened out (search): "Listo - Delivery App" (Food & Drink) |
| 103 | Ponto | PT *no ponto* (cooked just right) | Screened out (search): close to "Potto: Meal Planner & Recipes"; "Dieta dos Pontos" app |
| 104 | Rumo | PT "heading, course" | Screened out (search): "Rumo: Saúde, Dieta e Treino" (BR diet and training app) |
| 105 | Tondo | IT "round" | Screened out (search + judgment): results dominated by Tondo, a district of Manila |
| 106 | Faro | "Lighthouse"; sounds like farro grain | Screened out (search): FARAH meal-plan app sounds close; also FARO Technologies in measurement software (reviewer knowledge, not searched) |
| 107 | Seta | ES "mushroom" / IT "silk" | Screened out (search): SETA Organic superfood blends; weak idea |
| 108 | Riff | "A riff on a recipe" | Screened out (search): Riff meal kits (Daniel Humm, sold at Target); riff.kitchen recipe generator |
| 109 | Doppio | IT "double": cook once, eat twice | Screened out (search): Doppio Games, Doppio Lab (app agency), Doppio Group; strong coffee association |
| 110 | Metron | Greek "measure" (*pan metron ariston*) | Screened out (search): Metron photo food and macro app |
| 111 | Trofi | Greek *trofi* (food) | Screened out (search): "trofi foods" app; Trofi Life meal shakes |
| 112 | Tenzo | The head cook in a Zen monastery | Screened out (search): Tenzo restaurant-operations platform; Tenzo matcha tea |

#### 4.6.3 Latin, Romance or pan-European roots

| # | Name | Idea behind it | Screen result |
|---|---|---|---|
| 113 | Portata | IT "a course of a meal"; *a portata di mano* = within reach | **Shortlisted** (with Risk) |
| 114 | Sarto | IT "tailor" (Latin *sartor*): recipes tailored to you | **Shortlisted** (with Risk) |
| 115 | Mestolo | IT "ladle": the tool that serves one portion | **Shortlisted** (with Risk) |
| 116 | Pomona | Roman goddess of fruit and orchards | Screened out (search): Groupe Pomona, a French food-distribution group (Pomona EpiSaveurs, Pomona Iberia); pomona.pl, a Polish maker of food-packaging absorbent pads; pomona.io listed for sale |
| 117 | Annona | Roman goddess of the grain supply: provisions for the week | Screened out (search): "anona diet", a meal-subscription app; several Annona food brands |
| 118 | Prato | PT "plate, dish" | Screened out (search): "Prato", a meal-tracking and calorie app on Google Play |
| 119 | Kulina | Latin *culina* (kitchen) | Screened out (search): two "Kulina" food apps (a Norwegian recipe community and an office food-delivery app) |
| 120 | Merenda | IT/PT afternoon snack | Screened out (search): Merenda, the leading Greek chocolate spread; Merenda Foods (Dutch organic snacks); Brazilian "merenda escolar" apps |
| 121 | Semana | ES/PT "week": the weekly plan | Screened out (judgment): descriptive in Spanish and Portuguese; also the name of news magazines (reviewer knowledge) |
| 122 | Bona | Latin "good"; Queen Bona, who brought Italian vegetables to Poland | Screened out (search): sounds like "BonApp!" and "Bon App" meal planners |
| 123 | Olla | ES cooking pot | Screened out (search): the query returned "Ollie for Meals" (meal planner); weak idea |
| 124 | Menta | "Mint" (IT/ES/PT) | Screened out (search + judgment): "Menta Healthy Food & Coffee" café; generic |
| 125 | Dimora | IT "home, dwelling" | Screened out (search + judgment): DiMoRa restaurant; weak link to the product |
| 126 | Aldente | *Al dente*: cooked just right | Screened out (search): "Aldenté" recipe-saver and meal-planner app |
| 127 | Aposto | IT *a posto* ("all set") | Screened out (search): Aposto media app (TR) with a food publication; PT *aposto* = "I bet" |
| 128 | Avanti | IT "forward": cook ahead | Screened out (search): crowded (nutritionists, restaurants) |
| 129 | Apetit | "Appetite" (CZ/SK; DE/SV *Appetit*) | Screened out (search): "Časopis Apetit", a Czech food-magazine app |
| 130 | Pepita | ES pumpkin seed / nugget | Screened out (search): pepita.com, a large marketplace operating in Poland (pepita.com/pl); Pépito biscuits (LU, Mondelēz); Pepita Catering |
| 131 | Ottimo | IT "excellent, optimal" | Screened out (search + judgment): laudatory in Italian (weak EU mark); an Ottimo food mark (India) and Ottimo PRO food-storage products |
| 132 | Pranzo | IT "lunch" | Screened out (search + judgment): descriptive in Italian; restaurants |
| 133 | Tessera | A mosaic tile: small pieces make the whole | Screened out (search): Tessera Foods (B2B food ingredients); near "Tera" AI dietitian app |
| 134 | Vesper | Latin "evening"; DE/AT *Vesper* = light meal | Screened out (search): the search summary described a "Vesper" women's-health app with nutrition content (no titled store link returned); Vesper cocktail |
| 135 | Misura | IT *su misura* (made to measure) | Screened out (judgment): believed to be an Italian biscuit and cracker brand (reviewer knowledge, not searched) |
| 136 | Marmita | BR PT packed lunch; ES cooking pot | Screened out (judgment): too close to Marmite (UK spread) |
| 137 | Hestia | Greek goddess of the hearth | Screened out (judgment): Ergo Hestia, a major Polish insurer (reviewer knowledge) |
| 138 | Edesia | Roman goddess of banquets | Screened out (judgment): Polish reads "si" as "ś" (C2); believed to be the name of a therapeutic-food non-profit (reviewer knowledge, not searched) |
| 139 | Libra | Balance, scales | Screened out (judgment): weight connotation (C5); crowded (reviewer knowledge) |
| 140 | Presto | IT "quickly" | Screened out (judgment): believed to be a US kitchen-appliance brand (reviewer knowledge, not searched) |

#### 4.6.4 English-readable food, wellbeing and lifestyle words used in a new way

| # | Name | Idea behind it | Screen result |
|---|---|---|---|
| 141 | Tiffin | Indian and British lunch box: meal prep | Screened out (search): "Healthy Tiffin: Meals & More" app and tiffin meal services |
| 142 | Larder | Pantry | Screened out (search): several "Larder" meal-planner apps |
| 143 | Simmer | Slow cooking, calm | Screened out (search): Simmerly and four or more "Simmer" recipe apps |
| 144 | Skillet | Frying pan | Screened out (search): "Skillet – Recipe Keeper" app |
| 145 | Platter | A serving dish for sharing | Screened out (search): "Platter" restaurant-management and POS apps; a UK wholesale-food SaaS |
| 146 | Manna | Food from heaven; PL *kasza manna* | Screened out (search): "Manna AI - Weekly Meal Planner"; "Manna Cooking" |
| 147 | Hopla | Pan-European "hoppla!" when something lands right | Screened out (search): "Hopla Food" food-truck app; a Hoplà cream product |
| 148 | Meze | Small shared plates | Screened out (search): Meze Audio (Romanian headphone brand with EU filings, class 9); Meze restaurant marks; tied to one cuisine (C7) |
| 149 | Ponzu | Citrus soy sauce | Screened out (search): several Ponzu restaurant apps; one sauce (C7) |
| 150 | Tanoa | Fijian kava bowl, like Ramekin | Screened out (search + judgment): kava bowls and Tanoa Hotels; kava is a psychoactive drink (C5) |
| 151 | Fika | Swedish coffee break | Screened out (judgment): sounds like IT *fica*, which is vulgar (C3) |
| 152 | Sprig | A sprig of herbs | Screened out (judgment): believed to be a UX-research software brand (reviewer knowledge, not searched) |
| 153 | Nutmeg | Spice | Screened out (judgment): believed to be a UK investment app (reviewer knowledge, not searched) |
| 154 | Sorted | British "sorted!" (all done) | Screened out (judgment): SORTEDfood, a UK food media brand (reviewer knowledge); "-ed" is awkward in Polish |
| 155 | Estro | IT "flair, inspiration" | Screened out (judgment): EN "estrogen" and "estrus" echoes (C3/C5) |
| 156 | Olio | IT "oil" | Screened out (judgment): OLIO food-sharing app (UK) (reviewer knowledge) |
| 157 | Frugo | Frugal | Screened out (judgment): Frugo is a Polish drink brand (reviewer knowledge) |
| 158 | Envie | FR *avoir envie de* (to feel like eating) | Screened out (judgment): one-language word; EN "envy" (C3) |
| 159 | Lust | DE *Lust auf* (to feel like) | Screened out (judgment): EN "lust" (C3) |
| 160 | Zin | NL *zin in* (to feel like) | Screened out (judgment): one-language word; three letters |

Result: **7 new international names shortlisted** (Tangram, Palmo, Sapimo, Savimo, Portata, Sarto, Mestolo). Together with Ramekin and Tadam from session 1, that makes 9 international names, plus 2 Polish-flavoured alternatives (§6).

---

## 5. Research findings and source links (evidence log)

All entries are dated **2026-09-24** (sessions 1 and 2 ran on the same day).

### 5.1 Source access log

#### Session 1 (2026-09-24)

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

#### Session 2 retry (2026-09-24)

At the start of session 2, each official source got **one plain request**, as the task asked. `curl` was run once for every source. WebFetch was also tried once on the RDAP, IANA, iTunes, Play and TMview URLs. The test name was `ramekin`.

| Source (official) | Request | Tool | Result |
|---|---|---|---|
| `rdap.verisign.com` (.com RDAP) | `/com/v1/domain/ramekin.com` | curl; WebFetch | curl: `curl: (56) CONNECT tunnel failed, response 403`. WebFetch: `EGRESS_BLOCKED … Access to rdap.verisign.com is blocked by the network egress proxy.` |
| `pubapi.registry.google` (.app RDAP) | `/rdap/domain/ramekin.app` | curl; WebFetch | Same two errors |
| `data.iana.org` (RDAP bootstrap) | `/rdap/dns.json` | curl; WebFetch | Same two errors, so the .pl and .io RDAP servers still can't be looked up |
| `itunes.apple.com` (iTunes Search API) | `/search?term=ramekin&entity=software&country=pl` | curl; WebFetch | Same two errors |
| `play.google.com` | `/store/search?q=ramekin&c=apps&gl=PL` | curl; WebFetch | Same two errors |
| `www.tmdn.org` (TMview) | `/tmview/` | curl; WebFetch | Same two errors |
| `euipo.europa.eu`, `ewyszukiwarka.pue.uprp.gov.pl`, `branddb.wipo.int`, `tmsearch.uspto.gov`, `trademarks.ipo.gov.uk` | landing page | curl | `CONNECT tunnel failed, response 403` on each |
| **WebSearch** | — | WebSearch | **Worked.** Used for every session-2 screen and per-name check (§5.3, §6.3) |

**Consequence:** the access situation is unchanged from session 1. Every store, domain, trademark and handle check for every name stays **Pending**. No workaround was attempted.

### 5.2 Session 1 screening evidence (search engine; status at most Risk or Inconclusive)

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

### 5.3 Session 2 screening evidence (search engine; status at most Risk or Inconclusive)

All entries are dated **2026-09-24**. Quoted text is the search result's title, or its snippet or summary, as returned. None of the linked pages could be opened (egress-blocked). The per-name evidence for the new shortlist is in §6.3.

| Name | Query | Status | What the search showed | Links |
|---|---|---|---|---|
| Sapora | `"Sapora" app OR food OR recipes` | Risk (screened out) | "Sapora — Stop scrubbing videos. Start cooking."; summary: imports TikTok and Instagram recipes with "macros per portion"; sapora.com sells spices | [sapora.app](https://sapora.app/), [sapora.com](https://sapora.com/) |
| Plendo | `"Plendo" app OR brand` | Risk (screened out) | "Plendo — Fuel, refined."; summary: "sports-nutrition meal-planning app" | [plendo.app](https://plendo.app/) |
| Adapto | `"Adapto" app meal OR recipes OR nutrition` | Risk (screened out) | "Make the Meals You Already Want… Better. \| The meal adaptation app for real-life kitchens" | [studio.com](https://studio.com/apps/jeremy/adapo) |
| Modo | `"Modo" app meal OR nutrition OR recipes` | Risk (screened out) | "Modo \| Digital Nutritionist App"; "MODL - Hit your macros with real food" | [getmodo.io](https://www.getmodo.io/), [joinmodl.app](https://www.joinmodl.app/) |
| Melo | `"Melo" app food OR recipes OR meal OR nutrition` | Risk (screened out) | "Melo AI \| Your Adaptive Diet Coach"; "Melo: AI Family Organizer - App Store" | [meloai.app](https://www.meloai.app/), [App Store](https://apps.apple.com/us/app/melo-ai-family-organizer/id6752846683) |
| Gramo | `"Gramo" app food OR nutrition OR recipes` | Risk (screened out) | summary: "an AI-powered macro tracker" at gramo.space | [gramo.space](https://gramo.space/) |
| Metron | `"Metron" app nutrition OR food OR meal` | Risk (screened out) | summary: photograph a meal, get "energy and macros" | [metronapp.xyz](https://www.metronapp.xyz/marketing) |
| Trofi | `"Trofi" app OR brand food OR nutrition` | Risk (screened out) | "trofi foods App - App Store"; "Trofi Life: Fuel Better \| Plant-Based Meal Replacement" | [App Store](https://apps.apple.com/us/app/trofi-foods/id6502950424), [trofilife.com](https://trofilife.com/) |
| Manna | `"Manna" app meal planner OR nutrition OR recipes` | Risk (screened out) | "Manna AI - Weekly Meal Planner - Apps on Google Play"; "Manna Cooking App - App Store" | [Play](https://play.google.com/store/apps/details?id=com.mannaai.appv), [App Store](https://apps.apple.com/us/app/manna-cooking/id1493581046) |
| Aldente | `"Aldente" app recipes OR meal planner` | Risk (screened out) | "Aldenté Cookbook, Recipe Saver App - App Store"; "Recipe Organizer & Meal Planner with Grocery List \| Aldenté" | [App Store](https://apps.apple.com/us/app/aldent%C3%A9/id6748151276), [aldente.kitchen](https://aldente.kitchen/) |
| Larder | `"Larder" app pantry OR recipes OR meal planner` | Risk (screened out) | "Meal Planner & Recipes: Larder - Apps on Google Play"; "The Larder — Recipe Vault & Meal Planner" | [Play](https://play.google.com/store/apps/details?id=app.meal.planner.recipes&hl=en_US), [thelarder.app](https://www.thelarder.app/) |
| Simmer | `"Simmer" app recipes OR meal planner` | Risk (screened out) | "Simmerly: Meal Planner App - App Store"; "Simmer - Recipes & Cooking - App Store"; "Simmer AI – Recipe Generator" | [Simmerly](https://apps.apple.com/us/app/simmerly-meal-planner/id6754786986), [Simmer](https://apps.apple.com/us/app/simmer-recipes-cooking/id1559086783) |
| Skillet | `"Skillet" app recipes OR meal planning` | Risk (screened out) | "Skillet – Recipe Keeper - App Store - Apple" | [App Store](https://apps.apple.com/us/app/skillet-recipe-keeper/id6789624043) |
| Tiffin | `"Tiffin" app meal prep OR meal planner OR nutrition` | Risk (screened out) | "Healthy Tiffin: Meals & More App - App Store" | [App Store](https://apps.apple.com/us/app/healthy-tiffin-meals-more/id6753857177) |
| Platter | store-filtered `Platter`; `"Platter" brand OR company app food startup` | Risk (screened out) | "Platter: Restaurant Management - App Store"; "Platter Restaurant POS"; "British wholesale food platform Platter raises €411k" | [App Store](https://apps.apple.com/us/app/platter-restaurant-management/id6446100338), [EU-Startups](https://www.eu-startups.com/2025/05/british-wholesale-food-platform-platter-raises-e411k-to-reduce-inefficiency-food-waste/) |
| Prato | `"Prato" app recipes OR meal planner OR nutrition` | Risk (screened out) | "Prato - Apps on Google Play" (summary: meal tracking and calorie counting); "Potto: Meal Planner & Recipes" | [Play](https://play.google.com/store/apps/details?id=com.prato.prato_app&hl=en_US) |
| Kulina | `"Kulina" app OR brand food OR recipes` | Risk (screened out) | "Kulina - Apps on Google Play" (Norwegian recipe community); "Kulina - Office Food Delivery - App Store" | [Play](https://play.google.com/store/apps/details?id=no.kulina&gl=US), [App Store](https://apps.apple.com/us/app/kulina-office-food-delivery/id1442192909) |
| Merenda | store-filtered `Merenda`; `"Merenda" brand OR company food products` | Risk (screened out) | "What Is Merenda? Greece's Answer to Nutella Explained"; "Organic private label snacks - Merenda Foods"; "Merenda Escolar - Apps on Google Play" | [Honest Cooking](https://honestcooking.com/merenda-is-greek-for-nutella/), [merendafoods.com](https://merendafoods.com/en/), [Play](https://play.google.com/store/apps/details?id=br.com.etibrasil.merendaescolar) |
| Pomona | store-filtered `Pomona`; `"Pomona" marka OR firma…`; `"pomona.com" OR…` | Risk (screened out) | "Pomona Iberia - Aplicaciones en Google Play" (food distribution); "GROUPE POMONA for iPhone"; "Strona główna - POMONA COMPANY" (absorbent pads for food packaging, Żyrardów); "pomona.io - Domain Name For Sale \| Dan.com" | [Play](https://play.google.com/store/apps/details?id=com.uve.pomonaiberia&hl=en_US), [App Store developer](https://apps.apple.com/kg/developer/groupe-pomona/id1524920753), [pomona.pl](https://pomona.pl/en/), [pomona.io](https://pomona.io/) |
| Annona | `"Annona" app OR brand food` | Risk (screened out) | "anona diet App - App Store" (meal selection and "weight management") | [App Store](https://apps.apple.com/us/app/anona-diet/id1661103386) |
| Pepita | store-filtered `Pepita`; `"pepita.com" OR…`; `"Pepito" biscuits…` | Risk (screened out) | "Rodzinny sklep internetowy 9 241 718 produkt \| Pepita.com" (a marketplace operating in PL); "Pepita Catering"; the summary says Pepito is a LU brand owned by Mondelēz | [pepita.com/pl](https://pepita.com/pl), [Pepita Catering](https://pepitacatering.com/conference-services), [LU (Wikipedia)](https://en.wikipedia.org/wiki/LU_(biscuits)) |
| Apto | `"Apto" app meal…`; store-filtered `Apto app`; `"Apto" company…` | Risk (screened out) | "App Apto - App Store" (summary: combines "dietary habits and physical activity with laboratory tests and health history"); Apto commercial real-estate software at apto.com | [App Store AR](https://apps.apple.com/ar/app/apto/id1458389608), [broker.apto.com](https://broker.apto.com/) |
| Aptelo | `"Aptelo"` | Risk (screened out) | "Aptelo (@namierzamyleki)"; "APTELO \| Rejestr.io"; "The domain name Aptelo.com is for sale" | [Facebook](https://www.facebook.com/namierzamyleki/), [rejestr.io](https://rejestr.io/krs/491621/aptelo), [aptelo.com](https://www.aptelo.com/) |
| Aptimo | `"Aptimo" app OR brand…`; store-filtered; `"aptimo.com" OR…` | Risk (screened out) | "AptimO.pl Dla zdrowia" (summary: online pharmacy in Mikstat); "Android Apps by Aptimo. on Google Play" (engineering calculators) | [aptimo.pl](https://www.aptimo.pl/search), [Play developer](https://play.google.com/store/apps/developer?id=Aptimo.&hl=en_US) |
| Faro | `"Faro" app meal planner OR nutrition OR recipes` | Risk (screened out) | "Weekly Meal Plan: FARAH" (a sound-alike meal-plan app); no Faro app | [getfarah.app](https://getfarah.app/meal-plan) |
| Seta | `"Seta" app food OR nutrition OR recipes` | Risk (screened out) | "Superfood powder blends for smoothies & recipes \| Seta Organic" | [setaorganic.com](https://setaorganic.com/en/pages/accueil) |
| Ritmo | `"Ritmo" app nutrition OR meal OR diet` | Risk (screened out) | "Ritmo - Apps on Google Play" (routine tracker) | [Play](https://play.google.com/store/apps/details?id=com.rutinapp.app&hl=en) |
| Etto | `"Etto" app food OR nutrition OR brand` | Risk (screened out) | No Etto app; "Eato®: Calorie Counter - Apps on Google Play" sounds close | [Play](https://play.google.com/store/apps/details?id=com.eato.caloriecounter.weight.loss&hl=en_US) |
| Listo | `"Listo" app meal OR food OR recipes` | Risk (screened out) | "Listo - Delivery App - App Store - Apple" | [App Store](https://apps.apple.com/us/app/listo-delivery-app/id6469943534) |
| Ponto | `"Ponto" app nutrition OR meal OR recipes` | Risk (screened out) | "Potto: Meal Planner & Recipes - App Store"; "Nutrieduc - Dieta dos Pontos" | [Potto](https://apps.apple.com/us/app/potto-meal-planner-recipes/id6778760884) |
| Rumo | `"Rumo" app food OR nutrition OR recipes` | Risk (screened out) | "Rumo: Saúde, Dieta e Treino – Apps on Google Play" | [Play](https://play.google.com/store/apps/details?id=com.bussoladigital.rumo&hl=en_IN) |
| Tondo | `"Tondo" app food OR recipes OR nutrition` | Risk (screened out) | Results dominated by food trips in Tondo, Manila | [The Peach Kitchen](https://www.thepeachkitchen.com/2025/03/ugbo-tondo-food-trip-2025/) |
| Riff | `"Riff" app recipes OR cooking OR meal` | Risk (screened out) | "Daniel Humm Launches Riff Meal Kits at Target"; "Recipe Generator From the Ingredients You Already Have \| Riff.kitchen" | [eatriff.com](https://eatriff.com/), [riff.kitchen](https://riff.kitchen/) |
| Doppio | `"Doppio" brand OR app OR company` | Risk (screened out) | Doppio Games; "Doppio Lab - Premium Mobile App Development"; Doppio Group | [doppio-lab.com](https://doppio-lab.com/), [Dealroom](https://app.dealroom.co/companies/doppio) |
| Tenzo | `"Tenzo" app OR brand food` | Risk (screened out) | "Tenzo - Restaurant PerformanceOps"; "Tenzo - App Store - Apple"; Tenzo Tea (matcha) | [App Store](https://apps.apple.com/us/app/tenzo/id6748526081), [LinkedIn](https://www.linkedin.com/company/tenzo-tea) |
| Mezura | `"Mezura" OR "Sarto app" OR "Portata app"` | Risk (screened out) | "Mezura on the App Store" (cut planning for woodwork and LED strips) | [App Store](https://apps.apple.com/gb/app/mezura/id1585338510) |
| Tomalo | `"Tomalo" app OR brand` | Risk (screened out) | "Tómalo – Apps on Google Play" (retail); "TOMALO RADIO HD" | [Play](https://play.google.com/store/apps/details?id=com.innref.tomalo&hl=en_IE) |
| Tavelo / Aptelo | `"Tavelo" OR "Aptelo" app OR brand` | Risk (Tavelo, screened out) | "Unleash the Power \| Tavelo Bikes" | [tavelo.cc](https://tavelo.cc/) |
| Nomeo / Sapimo / Delumo | `"Nomeo" OR "Sapimo" OR "Delumo" app OR brand` | Risk (Nomeo); Inconclusive (Sapimo) | Nomeo, a digital-nomad community; Delumo AB, an agency; nothing for Sapimo | [LinkedIn Nomeo](https://www.linkedin.com/company/nomeoio) |
| Bonimo / Tavimo | `"Bonimo" OR "Tavimo" app OR brand` | Risk (Bonimo); Inconclusive (Tavimo) | "Bonimo: Gutscheine sofort - Apps on Google Play"; nothing for Tavimo | [Play](https://play.google.com/store/apps/details?id=com.monet.bonimo&hl=en_US) |
| Fornelo | `"Fornelo" app OR brand` | Risk (screened out) | "Fornello - App Store - Apple" (retail ordering) | [App Store](https://apps.apple.com/us/app/fornello/id1624454498) |
| Kaldo | `"Kaldo" app OR brand food` | Risk (screened out) | "Kaldo - Apps on Google Play" (pub); "Kaldo's - Apps on Google Play" (restaurant) | [Play](https://play.google.com/store/apps/details?id=com.errevi2.kaldo&hl=en) |
| Sumisura | `"Sumisura" app OR brand` | Risk (screened out) | Sumisura, an "AI resume tailoring" project; "suMisura - Apps on Google Play" | [GitHub](https://github.com/gio-del/sumisura), [Play](https://play.google.com/store/apps/details?id=com.peels.sumisura&hl=en_US) |
| Bona | `"Bona" app meal OR nutrition OR recipes` | Risk (screened out) | "BonApp! Recipes & Meal Planner App - App Store"; "Bon App \| Weekly balanced meal plans and shopping lists" | [App Store](https://apps.apple.com/us/app/bonapp-recipes-meal-planner/id6739699218), [bonapp.menu](https://www.bonapp.menu/en/) |
| Olla | `"Olla" app recipes OR meal planner OR cooking` | Risk (screened out) | The query returned "Ollie for Meals: Meal Planning" | [App Store](https://apps.apple.com/us/app/ollie-for-meals-meal-planning/id6480014476) |
| Menta | `"Menta" app nutrition OR recipes OR meal` | Inconclusive (screened out on judgment) | "Menta Healthy Food & Coffee" (Jerez); no Menta app | [TikTok](https://www.tiktok.com/@bur25/video/7387115167462542624) |
| Dimora | `"Dimora" app food OR recipes OR brand` | Inconclusive (screened out on judgment) | "DiMoRa", a restaurant | [dimora.co.in](https://www.dimora.co.in/) |
| Semana | `"Semana" meal planner app` | Inconclusive (screened out on judgment) | No Semana app; generic meal-planner results | — |
| Tessera | `"Tessera" app food OR nutrition OR meal` | Risk (screened out) | "Tessera Foods \| Premium Quality Food Products & Ingredients"; "AI Dietitian & Meal Plans:Tera" | [tesserafoods.com](https://www.tesserafoods.com/), [App Store](https://apps.apple.com/us/app/ai-dietitian-meal-plans-tera/id1608429635) |
| Meze | `"Meze" app…`; `"Meze" brand trademark…` | Risk (screened out) | No Meze app; Meze Audio (Baia Mare, Romania); "MEZE AUDIO ARTA Trademark … European Union" | [Wikipedia](https://en.wikipedia.org/wiki/Meze_Audio), [Trademarkia EU](https://www.trademarkia.eu/en/trademark-detail/meze-audio-arta-019278421) |
| Ponzu | `"Ponzu" app OR brand -sauce` | Risk (screened out) | "Ponzu Restaurant - Apps on Google Play"; "Ponzu Sushi - Apps on Google Play" | [Play](https://play.google.com/store/apps/details?id=com.masdelivery.ponzusushi&hl=en_US) |
| Tanoa | `"Tanoa" app OR brand food` | Risk (screened out) | Kava bowls; "Tanoa Hotels Logo & Brand Assets" | [Brandfetch](https://brandfetch.com/tanoahotels.com) |
| Hopla | `"Hopla" app OR brand food` | Risk (screened out) | "Download Hopla Food app for iPhone and iPad"; "HOPLA TO BE ASSEMBLED ALREADY SUGARED 500 ML" | [hopla-food](https://hopla-food.appstor.io/), [ABC Foodservice](https://www.abcfoodservice.it/en/prepared-for-dessert/hopla-to-be-assembled-already-sugared-500-ml) |
| Apetit | `"Apetit" app OR magazine OR brand food` | Risk (screened out) | "Časopis Apetit – Apps on Google Play" | [Play](https://play.google.com/store/apps/details?id=cz.burdadigital.apetit&hl=en_IN) |
| Avanti | `"Avanti" app meal prep OR recipes OR nutrition` | Risk (screened out) | Nutritionists and restaurants named Avanti | [christineavanti.com](https://www.christineavanti.com/) |
| Aposto | `"Aposto" app OR brand` | Risk (screened out) | "Aposto - Apps on Google Play"; "Aposto Brands" (includes a food publication) | [Play](https://play.google.com/store/apps/details?id=com.aposto.android&hl=en_US), [Aposto Brands](https://about.aposto.com/en/brands) |
| Ottimo | `"Ottimo" app food…`; `"Ottimo" brand OR trademark…` | Risk (screened out) | "Ottimo Trademark by Ottimo Foods & Ingredients" (summary: food classes, India); "Home - Ottimo PRO" (food preparation and storage products) | [trademarKing.in](https://trademarking.in/details/Ottimo-2212680.html), [ottimopro.com](https://ottimopro.com/en/) |
| Vesper | `"Vesper" app food OR meal OR recipes OR nutrition` | Risk (screened out; weak evidence) | The summary described a "Vesper" 30-day women's-health app with nutrition content, but no titled store link was returned. Other results: Vesper martini recipes | — |
| Pranzo | `"Pranzo" app meal OR food OR recipes` | Inconclusive (screened out on judgment) | Italian meal structure; Caffe Pranzo restaurants; no Pranzo app | — |
| Savimo, Sapimo, Tangram, Palmo, Portata, Sarto, Mestolo | see §6.3 | — | Shortlisted; full per-name evidence in §6.3 | — |

---

## 6. Shortlist

> **Rebuilt in session 2 (2026-09-24), international-first.** The shortlist now has **9 international names** (§6.1–§6.3) and **2 Polish-flavoured alternatives** (§6.4), which are not recommended as the main brand for international expansion. The other session-1 names were removed; their evidence is kept in §6.5. The session-1 check matrix and ranking are kept in §6.6 and marked superseded.

### 6.1 Check matrix (session 2: 9 international names)

Read each cell as **authoritative status (search-engine indication)**. "Pending" means the official source was blocked (§5.1); the bracketed indication comes from the search engine only. **N** is C10 international neutrality (1–5, §2.3), a reviewer assessment.

| Name | Type | 1 Competitors / similar | 2 App Store | 3 Google Play | 4 .com | 4 .app | 4 .io | 4 .pl | 5 Trademarks (EUIPO / TMview / UPRP / WIPO / USPTO / UKIPO) | 6 Language PL/EN | 7 Confusing similarity | 8 Social handles | N |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Tangram** | Known puzzle word, used arbitrarily | Risk: software firms (tangram.dev, tangram.co, Tangram Vision); no food use seen | Pending (Risk: many "Tangram" puzzle games) | Pending (Risk: puzzle games; "TANGRAM Center") | Pending (Inconclusive) | Pending (Inconclusive) | Pending (Inconclusive) | Pending (Inconclusive) | Pending (Risk: US TANGRAM and TANGRAM FLEX software marks on third-party sites) | Inconclusive: no negatives found; same word across Europe | Risk: exact name common in class 9 games | Pending (Risk: @tangrambr, 15K) | 5 |
| **Ramekin** *(session 1)* | EN/FR kitchen word, used arbitrarily | Inconclusive | Pending (Inconclusive) | Pending (Inconclusive) | Pending | Pending | Pending | Pending | Pending | Inconclusive: moderate PL familiarity | Inconclusive | Pending (Risk: generic word) | 4 |
| **Palmo** | IT/ES/PT word, used arbitrarily | Risk: Palmo creative studio, The Palmo Company (media); no food use seen | Pending (Risk: "Palmo: Paycheck Budget Tracker") | Pending (Risk: "Palmo: Chat & Message Analyzer") | Pending (Inconclusive) | Pending (Inconclusive) | Pending (Inconclusive) | Pending (Inconclusive) | Pending (Risk: PALMO CALIFORNIA, US, class 14, on a third-party site) | Inconclusive: remote ES slang echo ("palmar" = to die) | Risk: exact-name class-9 apps outside food | Pending (Risk: many @palmo… accounts) | 4 |
| **Sapimo** | Coinage | Inconclusive: only small personal accounts | Pending (Inconclusive) | Pending (Inconclusive: nearest "SAPINO", a game) | Pending (Inconclusive) | Pending (Inconclusive) | Pending | Pending (Inconclusive) | Pending (Inconclusive) | Risk (mild): EN "sap"; PL "sapie" (puffs, wheezes); ID "sapi" = cow | Risk (low): shares "Sap-" and the "taste" root with Sapora (recipe app) | Pending (Risk: @sa.pi.mo, a small personal account) | 4 |
| **Tadam** *(session 1)* | Interjection | Risk: non-food apps and brands | Pending (Risk) | Pending (Risk) | Pending | Pending | Pending | Pending | Pending | Inconclusive: no negatives found | Risk: TADAM (FR consumer brand) | Pending (Risk) | 5 |
| **Savimo** | Coinage | Risk: SAVIMO fashion brand; Savimo SA (Tunis) | Pending (Risk: "saviMon: Food & Supplements App") | Pending (Risk: "saviMon: Food, Meds & Vitamins") | Pending (Risk: savimo.com shows a security-check page) | Pending | Pending | Pending | Pending (Inconclusive) | Inconclusive: no negatives found | **Risk (high): saviMon, same category, one letter longer** | Pending (Risk: @savimo_brand) | 5 |
| **Sarto** | IT word | Risk: Sarto&Food (IT food retail app), Sarto Pasta (Leeds), Sarto restaurants | Pending (Risk: "SARTO" booking app; "Sarto: Resume Builder & Tailor"; "SARTO PASTICCERIA") | Pending (Risk: "Il Tuo Sarto"; a tailor game) | Pending (Inconclusive) | Pending | Pending | Pending (Inconclusive) | Pending (Risk: FRANCO SARTO US marks; other Sarto marks) | Inconclusive: no negatives found | Risk: crowded, including food uses | Pending (Risk: @sartopasta, @sartoframes, others) | 3 |
| **Portata** | IT word | Risk: portata.dev ("AI host for independent restaurants") | Pending (Inconclusive: only apps using the IT phrase) | Pending (Inconclusive) | Pending (Inconclusive) | Pending | Pending | Pending | Pending (Inconclusive), plus a descriptiveness risk in IT | Inconclusive: no negatives found | Risk: PORTA (IT ready meals, US retail); Portio AI | Pending (Inconclusive) | 3 |
| **Mestolo** | IT word | Risk (low): restaurants in Siena and Bremen | Pending (Inconclusive) | Pending (Inconclusive) | Pending (Risk: mestolo.com is a German cooking blog, per a third-party SEO page) | Pending | Pending | Pending | Pending | Inconclusive: 3 syllables; stress unclear in EN | Risk (low): class 43 restaurants | Pending (Risk: @mestolo.de, @mestolo_bremen) | 3 |

### 6.2 Scores (C1–C7, C10) and ranking

Scores run from 1 (poor) to 5 (strong) and are the reviewer's assessment of the evidence above. **C8 (domains and handles) and C9 (trademarks) are Pending for every name** and are not scored. "Evidence weight" summarises the search-engine Risk findings; it is a triage signal, not a legal assessment. **The rank weighs the C1–C7 score, C10 and the evidence weight together**, so a higher sum does not always mean a higher rank.

| Rank | Name | C1 | C2 | C3 | C4 | C5 | C6 | C7 | Sum /35 | C10 /5 | Evidence weight (SE) | Further investigation? |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **Tangram** | 4 | 5 | 5 | 4 | 5 | 5 | 5 | 33 | 5 | Medium: the exact name is common for puzzle apps (class 9) and some software firms; no food or nutrition use seen | **Yes, top 3** |
| 2 | **Ramekin** | 4 | 3 | 5 | 4 | 5 | 5 | 5 | 31 | 4 | Low: no same-name app or company in the category seen (session 1) | **Yes, top 3** |
| 3 | **Palmo** | 4 | 4 | 4 | 4 | 5 | 5 | 5 | 31 | 4 | Medium: two exact-name class-9 apps outside food (budget, chat analyser); a US jewellery mark | **Yes, top 3** |
| 4 | Sapimo | 5 | 4 | 3 | 3 | 5 | 5 | 5 | 30 | 4 | Low: only small personal accounts seen | Yes, alternate (the coined option) |
| 5 | Tadam | 3 | 5 | 4 | 3 | 5 | 5 | 5 | 30 | 5 | Medium: same-name apps in class 9 (non-food); FR consumer brand (session 1) | Yes, alternate |
| 6 | Savimo | 5 | 4 | 5 | 4 | 5 | 5 | 5 | 33 | 5 | **High:** "saviMon", a food and medication tracker, is near-identical in the same category | Only if an attorney sees no conflict with saviMon |
| 7 | Sarto | 3 | 5 | 5 | 4 | 5 | 5 | 5 | 32 | 3 | High: many Sarto marks and food uses (IT food retail, UK fresh pasta) | No |
| 8 | Portata | 3 | 4 | 5 | 4 | 5 | 5 | 5 | 31 | 3 | Medium-high: descriptive in Italian; near PORTA (ready meals) and Portio AI | No |
| 9 | Mestolo | 4 | 3 | 4 | 3 | 5 | 5 | 5 | 29 | 3 | Medium: restaurants; the .com is a cooking blog | No |

**Trade-offs in brief:**
- **Tangram** has the strongest international profile. The word is the same in PL, EN, DE, FR, ES and IT, it is spelled phonetically, and the metaphor (seven pieces that always make a whole) fits the product exactly: recipes, macros, budget and prep day fitted into one plan (PRD §1, §8.6). It doesn't say "diet", and it leaves room for PRD §13 phases 2–4. The cost: in the stores, "tangram" means puzzle games, so the brand needs a descriptor ("Tangram: Meal Planner", 21 characters) and won't own the bare search term. It is also a common noun in class 9 for games, and some US software marks exist (unverified). Registrability for nutrition software is plausible but needs an attorney's view.
- **Ramekin** is still the cleanest in search, visual and warm, and it is an international kitchen word (EN, and FR *ramequin*). But fewer Poles know it, it has three syllables, and it may read as descriptive for recipe content (session 1, §6.3).
- **Palmo** is short (5 letters, 2 syllables), friendly and neutral. It says "portion" (the handspan and hand-portion idea) and "mobile" (in the palm of your hand) without saying diet. The cost: two unrelated class-9 apps already use the exact name, and many social handles are taken.
- **Sapimo** (alternate) is the only coinage with a nearly empty search footprint, and it should be the easiest to register. But its meaning is only half-visible ("sapore/sabor"), it has three syllables, and its echoes (EN "sap", PL "sapie") need a listener test.
- **Tadam** (alternate) is fun and universal, but it is an interjection with same-name software already in class 9.
- **Savimo** would score at the top on language, but "saviMon" (food and meds tracker) is too close in the same category for it to be a first choice.
- **Sarto, Portata and Mestolo** show that Italian words read as "international" to most Europeans, but each is a real Italian word. They are weak in Italy (and Portata is descriptive there), and the category is crowded around them. They are kept for completeness, not recommended.

### 6.3 Per-name evidence (international shortlist)

All session-2 checks are dated **2026-09-24**. Store, domain, trademark and handle checks are **Pending** for every name because the official sources were egress-blocked (§5.1). The bracketed search-engine indication is given in the "What the source showed" column. "SE" means a WebSearch result that could not be opened.

---

#### `Tangram` (top 3)

- **Concept:** A tangram is the seven-piece puzzle whose pieces always come together into one shape. The app does the same with the pieces the user already has (the recipe they want, their calories and macros, allergies, budget and prep day) and fits them into a plan that works. It suggests the optimisation without saying "diet", and it isn't tied to one feature.
- **Pronunciation:** PL [ˈtaŋɡram] "TAN-gram". The word is already used in Polish for the puzzle ("tangram – chińska układanka"). EN /ˈtæŋɡræm/ "TANG-gram". It is spelled phonetically in both languages, so people can write it after hearing it once.
- **Meaning and connotations:** The puzzle is known by the same name in DE, FR, ES, IT, NL, SV and PL (reviewer knowledge). Associations: play, logic, geometry, "everything fits". No rude or negative meanings are known in PL, EN, DE, FR, ES, IT, PT, NL or SV (reviewer assessment; native check pending). Nothing medical or moralising (C5).
- **Brand positioning:** "Every piece fits." / "Twój przepis. Twój plan. Wszystko pasuje." ("Your recipe. Your plan. It all fits.")
- **Visual identity:** seven flat geometric pieces forming a bowl or a plate. The icon is simple, monochrome-friendly and recognisable.
- **Main risks:** the bare word is used by many puzzle games (class 9), so store search returns puzzles, and the app title needs a descriptor. The US has TANGRAM software marks (seen only on third-party sites). The exact social handles are probably taken.

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk | 2026-09-24 | [tangram.dev](https://www.tangram.dev/), [tangram.co](https://www.tangram.co/), [Tangram Vision ToS](https://www.tangramvision.com/tos) | SE: "Tangram is a build system and package manager"; tangram.co is described as an API-first no-code platform; "Tangram Robotics, Inc. Terms Of Service". Query `"Tangram" app meal OR nutrition OR recipes OR food` returned **no** Tangram food, recipe or nutrition product (Inconclusive for the category). |
| 2 App Store (PL/US/GB) | Pending (SE: Risk) | 2026-09-24 | [Tayasui Tangram](https://apps.apple.com/us/app/tayasui-tangram/id765385885), [Osmo Tangram](https://apps.apple.com/us/app/osmo-tangram/id1539533255), [Tangram King](https://apps.apple.com/us/app/tangram-king/id1124017784), [Tangram: Logic Shape Puzzles](https://apps.apple.com/us/app/tangram-logic-shape-puzzles/id1568474294) | Store-filtered SE: every result was a puzzle game. The iTunes API is blocked, so App Store Connect availability is an owner action. |
| 3 Google Play | Pending (SE: Risk) | 2026-09-24 | [Tangram - Puzzle Game](https://play.google.com/store/apps/details?id=studio.onepixel.tangrambee), [Tangram (Magma Mobile)](https://play.google.com/store/apps/details?id=com.magmamobile.game.Tangram&hl=en_US), [TANGRAM Center](https://play.google.com/store/apps/details?id=com.cmacgm.tangram&hl=en_SG) | Puzzle games and a corporate "TANGRAM Center" app. No food app. |
| 4 Domains .com/.app/.io/.pl | Pending (SE: Inconclusive) | 2026-09-24 | RDAP blocked; SE for `"tangram.com" OR "tangram.app" OR "tangram.io"` | No site at tangram.com, .app or .io surfaced. tangram.dev, tangram.co and tangramio.com are in use. **Not evidence of availability**; a short dictionary word's .com is very likely registered. |
| 5 Trademarks | Pending (SE: Risk) | 2026-09-24 | [Trademark Elite: TANGRAM 88473186](https://www.trademarkelite.com/trademark/trademark-detail/88473186/TANGRAM), [Justia: TANGRAM FLEX](https://trademarks.justia.com/886/84/tangramflex-88684720.html), [Justia: TANGRAM 73635102](https://trademarks.justia.com/736/35/tangram-73635102.html) | Third-party (unofficial) pages: "TANGRAM Trademark of Tangram, LLC. Serial Number: 88473186" (goods not shown in the snippet); TANGRAM FLEX software, registered per the summary; a 1986 TANGRAM registration (1454723) "cancelled on 1994-02-28". The registries were blocked; the owner or an attorney must search USPTO, EUIPO, TMview and UPRP. |
| 6 Language | Inconclusive | 2026-09-24 | Reviewer assessment | See above. A native-speaker check is pending. |
| 7 Confusing similarity | Risk | 2026-09-24 | as rows 2–3 | Identical name widely used for puzzle games in class 9. No nutrition or meal-planning use seen. |
| 8 Social handles | Pending (SE: Risk) | 2026-09-24 | [@tangrambr (via SE)](https://www.instagram.com/tangrambr/) | "Tangram: Jogue, aprenda e enriqueça. (@tangrambr)", a Brazilian financial-education app (15K per the SE summary). The exact @tangram was not seen. Expect to need `tangramapp`, `gettangram` or `tangram.pl`. |

---

#### `Palmo` (top 3)

- **Concept:** "Palmo" is the handspan in Italian, Spanish and Portuguese (*palmo a palmo* = inch by inch), and it echoes English "palm". Two ideas in one word: portions you can judge with your hand (the familiar "palm-sized protein" method), and a plan that sits in the palm of your hand. It isn't tied to one diet or feature.
- **Pronunciation:** PL [ˈpalmɔ] "PAL-mo". EN /ˈpælmoʊ/ "PAL-moh"; some speakers may say "PAHL-moh". Unlike in "palm", the "l" is spoken. Easy to spell after one hearing.
- **Meaning and connotations:** IT/ES/PT: a span, an old unit of length. PL: no meaning ("palma" is a palm tree). ES colloquial verb *palmar(la)* means "to die". "Palmo" as a first-person form of that verb is rare, so the risk is low but should be tested with Spanish speakers. No negatives known in DE, FR, NL or SV (reviewer assessment).
- **Brand positioning:** "Your plan, in the palm of your hand." / "Twój plan na wyciągnięcie dłoni." ("Your plan within hand's reach.")
- **Visual identity:** an open palm holding a small bowl.
- **Main risks:** exact-name apps in class 9 (a budget tracker and a chat analyser); many social accounts; a minor visual echo of "Palmolive" (class 3).

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk | 2026-09-24 | [The Palmo Company](https://www.palmocompany.com/), [palmo.inc](https://palmo.inc/), [ZoomInfo](https://www.zoominfo.com/c/palmo/451628663) | SE: "a holding company building media businesses in New York City"; "Palmo - Global Creative Studio"; per the summary, a Palmo packaging manufacturer in Thessaloniki. Query `"Palmo" app food OR nutrition OR recipes` returned **no** Palmo food app. |
| 2 App Store | Pending (SE: Risk) | 2026-09-24 | [Palmo: Paycheck Budget Tracker](https://apps.apple.com/us/app/palmo-paycheck-budget-tracker/id6443496808) | "Palmo: Paycheck Budget Tracker App - App Store" (JLApp LLC). Finance, not food. |
| 3 Google Play | Pending (SE: Risk) | 2026-09-24 | [Palmo: Chat & Message Analyzer](https://play.google.com/store/apps/details?id=com.palmo.palmo) | "Palmo: Chat & Message Analyzer - Apps on Google Play". |
| 4 Domains | Pending (SE: Inconclusive) | 2026-09-24 | RDAP blocked; SE for `"palmo.com" OR "palmo.app" OR "palmo.io" OR "palmo.pl"` | No page at those domains surfaced. Not evidence of availability. |
| 5 Trademarks | Pending (SE: Risk) | 2026-09-24 | [Trademark Elite: PALMO CALIFORNIA](https://www.trademarkelite.com/trademark/trademark-detail/88121694/PALMO-CALIFORNIA) | "PALMO CALIFORNIA … Registration Number 5767646 … International Class 014" (jewellery), from a third-party page. No software or food mark surfaced. Registries were blocked. |
| 6 Language | Inconclusive | 2026-09-24 | Reviewer assessment | See above. |
| 7 Confusing similarity | Risk | 2026-09-24 | as rows 2–3 | Identical name on two class-9 apps in other fields. Nothing in nutrition or recipes. |
| 8 Social handles | Pending (SE: Risk) | 2026-09-24 | [@palmodesigns](https://www.instagram.com/palmodesigns/), [@palmo_germany](https://www.instagram.com/palmo_germany/), [@palmogoods](https://www.instagram.com/palmogoods/) (all via SE) | Many "Palmo" accounts are in use. The exact @palmo was not seen. Expect `palmoapp`, `getpalmo` or `palmo.pl`. |

---

#### `Sapimo` (alternate: the coined option)

- **Concept:** Coined from Latin *sapor* (taste), which lives on in IT *sapore*, ES/PT *sabor* and FR *saveur*, with an open, friendly "-imo" ending. "Taste first" in a form most Europeans half-recognise, without belonging to any one language.
- **Pronunciation:** PL [saˈpimɔ] "sa-PI-mo". EN /səˈpiːmoʊ/ "suh-PEE-moh". Spelled phonetically, so it is easy to write after one hearing.
- **Meaning and connotations:** No dictionary meaning found. Possible echoes: EN "sap" (plant sap; slang for a fool); PL "sapie", from *sapać* (to puff or wheeze); Indonesian *sapi* = cow (the TikTok tag "#sapimo" is cow content); the Neapolitan song "Madonna nui sapimo" ("we know"). None is strong, but a listener test should cover them (C3).
- **Brand positioning:** "Taste first. Then the numbers." / "Najpierw smak. Potem liczby."
- **Main risks:** the meaning is not obvious; three syllables; the echoes above; a shared "Sap-" start with Sapora, a recipe-import app (§3.4).

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Inconclusive | 2026-09-24 | [@sa.pi.mo (via SE)](https://www.instagram.com/sa.pi.mo/), [Linktree SapiMo](https://linktr.ee/SapiMo), [Apple Music](https://music.apple.com/us/song/madonna-nul-sapimo/1519083381) | `"Sapimo"` returned only a small personal Instagram account ("13 followers" per the summary), a Linktree, a DeviantArt user and the song "Madonna nul sapimo". No company or product. |
| 2 App Store | Pending (SE: Inconclusive) | 2026-09-24 | Store-filtered SE | No Sapimo app returned. |
| 3 Google Play | Pending (SE: Inconclusive) | 2026-09-24 | [SAPINO](https://play.google.com/store/apps/details?id=appinventor.ai_bmindsapps.SAPINO&hl=en_US) | Nearest match: "SAPINO", a name-guessing game. |
| 4 Domains | Pending (SE: Inconclusive) | 2026-09-24 | RDAP blocked | SE for `"sapimo.com" OR "sapimo.app" OR "sapimo.pl"` returned no site. Not evidence of availability. |
| 5 Trademarks | Pending (SE: Inconclusive) | 2026-09-24 | Registries blocked | No mark surfaced. **Not a clearance.** |
| 6 Language | Risk (mild) | 2026-09-24 | Reviewer assessment; [TikTok #sapimo (via SE)](https://www.tiktok.com/tag/sapimo%F0%9F%90%AE) | Echoes as above. |
| 7 Confusing similarity | Risk (low) | 2026-09-24 | [sapora.app](https://sapora.app/) | Sapora (recipe import with macros) shares "Sap-" and the taste root. The words differ in ending and length. |
| 8 Social handles | Pending (SE: Risk) | 2026-09-24 | [@sa.pi.mo (via SE)](https://www.instagram.com/sa.pi.mo/), [Facebook "Sapimo" (via SE)](https://www.facebook.com/sapimo.sapimo.96/) | Small personal accounts only. The exact @sapimo was not seen. |

---

#### `Savimo` (not recommended unless saviMon is cleared)

- **Concept:** Coined from EN "savour", FR *saveur*/*savoir* and "savvy": food that tastes good, planned smartly.
- **Pronunciation:** PL [saˈvimɔ] "sa-VI-mo". EN /səˈviːmoʊ/ "suh-VEE-moh" (some may say "SAV-ih-moh").
- **Meaning and connotations:** no dictionary meaning; IT *savi* = wise (plural). No negatives known in the languages checked (reviewer assessment).
- **Main risk:** "saviMon", a food, medication and vitamin tracker, is one letter away, in the same category, and health-flavoured (C5 by association).

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk | 2026-09-24 | [savimobrand.com](https://savimobrand.com/), [D&B: Savimo SA](https://www.dnb.com/business-directory/company-profiles.savimo_sa.a27c9cba1308fcb1de1d4c5015abcba4.html) | "SAVIMO BRAND" (women's luxury wear); Savimo SA (Tunis). |
| 2 App Store | Pending (SE: Risk) | 2026-09-24 | [saviMon](https://apps.apple.com/us/app/savimon/id6760576803) | "saviMon: Food & Supplements App - App Store". |
| 3 Google Play | Pending (SE: Risk) | 2026-09-24 | [saviMon](https://play.google.com/store/apps/details?id=ai.tachyonhq.savimon&hl=en_US) | "saviMon: Food, Meds & Vitamins - Apps on Google Play". |
| 4 Domains | Pending (SE: Risk) | 2026-09-24 | [savimo.com](http://www.savimo.com/) | The SE summary described savimo.com as a captcha or security-check page with a customer-care number: registered and possibly parked (unverified). Nothing surfaced for .app, .pl or .io. |
| 5 Trademarks | Pending (SE: Inconclusive) | 2026-09-24 | Registries blocked | No mark surfaced. |
| 6 Language | Inconclusive | 2026-09-24 | Reviewer assessment | No issue found. |
| 7 Confusing similarity | Risk (high) | 2026-09-24 | as rows 2–3 | saviMon. |
| 8 Social handles | Pending (SE: Risk) | 2026-09-24 | [@savimo_brand (via SE)](https://www.instagram.com/savimo_brand/) | About 4.4K followers per the SE summary. |

---

#### `Sarto`

- **Concept:** IT *sarto* = tailor (Latin *sartor*): recipes tailored to your numbers.
- **Pronunciation:** PL [ˈsartɔ]; EN /ˈsɑːrtoʊ/ "SAR-toh". Easy in both languages.
- **Meaning and connotations:** also an Italian surname (the painter Andrea del Sarto). No negatives known (reviewer assessment).
- **Main risk:** crowding. Many Sarto marks and businesses exist, including food uses.

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk | 2026-09-24 | [SARTO PASTICCERIA (Sarto&Food)](https://apps.apple.com/ie/app/sarto-pasticceria/id6755481786), [D&B: SARTO SRL](https://www.dnb.com/business-directory/company-profiles.sarto_srl.672477bb3d31115ab2c0e7b947def370.html), [@sartopasta (via SE)](https://www.instagram.com/sartopasta/?hl=en) | Sarto&Food loyalty app ("authentic taste", IT); SARTO SRL, described in the summary as a specialty food retailer (Porto Viro); "Fresh, handmade pasta in Leeds"; Sarto restaurants in Providence and Denver. |
| 2 App Store | Pending (SE: Risk) | 2026-09-24 | [SARTO](https://apps.apple.com/us/app/sarto/id1436294235), [Sarto: Resume Builder & Tailor](https://apps.apple.com/ie/app/sarto-resume-builder-tailor/id6790501360) | "SARTO on the App Store" (appointment booking); a resume "tailor" app. |
| 3 Google Play | Pending (SE: Risk) | 2026-09-24 | [Il Tuo Sarto](https://play.google.com/store/apps/details?id=yuss.iltuosarto&hl=it&gl=US), [sarto game](https://play.google.com/store/apps/details?id=com.YovoGames.tailor&hl=en_US) | A tailoring service app and a children's tailor game. |
| 4 Domains | Pending (SE: Inconclusive) | 2026-09-24 | [sartobikes.com](https://www.sartobikes.com/en), [sartohome.com](https://www.sartohome.com/) | Nothing surfaced for sarto.com; related domains are in use. |
| 5 Trademarks | Pending (SE: Risk) | 2026-09-24 | [Trademarkia: FRANCO SARTO](https://www.trademarkia.com/franco-sarto-85076996) | FRANCO SARTO (US, Caleres). The summary also says "Sarto is a registered trademark of Fatih Ev Tekstil" (home textiles). Third-party sources only. |
| 6 Language | Inconclusive | 2026-09-24 | Reviewer assessment | No issue found. |
| 7 Confusing similarity | Risk | 2026-09-24 | as rows 1–3 | Crowded, including food retail and pasta. |
| 8 Social handles | Pending (SE: Risk) | 2026-09-24 | [@sartoframes](https://www.instagram.com/sartoframes/), [@sarto__official](https://www.instagram.com/sarto__official/) (via SE) | Many Sarto accounts are in use. |

---

#### `Portata`

- **Concept:** IT *portata* = a course of a meal (*prima portata*), and *a portata di mano* = within reach. The plan puts the food you want within reach.
- **Pronunciation:** PL [pɔrˈtata] "por-TA-ta"; EN /pɔːrˈtɑːtə/ "por-TAH-tuh". Three syllables.
- **Meaning and connotations:** IT also means "flow rate" or "capacity". ES *portada* (a cover) is a different word. No negatives known (reviewer assessment).
- **Main risks:** descriptive for meals in Italian, and EUIPO assesses every EU language (C1/C9); a very common Italian phrase, so the brand would not own search; sounds near PORTA (Italian ready meals) and Portio AI.

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk | 2026-09-24 | [portata.dev](https://portata.dev/), [Kimball: Portata](https://www.kimballinternational.com/product/portata.html) | "Portata · The AI host for independent restaurants"; a seating collection. |
| 2 App Store | Pending (SE: Inconclusive) | 2026-09-24 | Store-filtered SE | Only Italian apps using the phrase "a portata di mano". No Portata app. |
| 3 Google Play | Pending (SE: Inconclusive) | 2026-09-24 | [Misuratore di portata](https://play.google.com/store/apps/details?id=brisinua.flowratemeter&hl=en_US) | A flow-rate calculator. |
| 4 Domains | Pending (SE: Inconclusive) | 2026-09-24 | RDAP blocked | Nothing surfaced for portata.com, .app or .io. |
| 5 Trademarks | Pending (SE: Inconclusive) | 2026-09-24 | Registries blocked | No mark surfaced. Descriptiveness in Italian is a separate risk. |
| 6 Language | Inconclusive | 2026-09-24 | Reviewer assessment | See above. |
| 7 Confusing similarity | Risk | 2026-09-24 | [@eatporta (via SE)](https://www.instagram.com/eatporta/?hl=en), Portio AI (§5.2) | PORTA: "traditional Italian food handmade by chefs … available at Whole Foods, Sprouts, Sobeys" (summary). |
| 8 Social handles | Pending (SE: Inconclusive) | 2026-09-24 | SE filtered to Instagram and TikTok | No exact @portata surfaced. |

---

#### `Mestolo`

- **Concept:** IT *mestolo* = ladle: the tool that serves one portion. It is the Italian cousin of Ramekin.
- **Pronunciation:** PL [mɛsˈtɔlɔ] "mes-TO-lo"; EN /mɛˈstoʊloʊ/ "meh-STOH-loh". English speakers may put the stress elsewhere.
- **Meaning and connotations:** no negatives known. For Czech, Slovak or Slovene readers, "mesto" (town) is a harmless echo.
- **Main risks:** three syllables; the meaning is only clear to Italian speakers; restaurants and a cooking blog on the .com.

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk (low) | 2026-09-24 | [@ristoranteilmestolosiena](https://www.instagram.com/ristoranteilmestolosiena/), [@mestolo_bremen](https://www.instagram.com/mestolo_bremen/) (via SE) | "Il Mestolo" (Siena) and "Restaurant Mestolo" (Bremen). |
| 2 App Store | Pending (SE: Inconclusive) | 2026-09-24 | Store-filtered SE | No Mestolo app. |
| 3 Google Play | Pending (SE: Inconclusive) | 2026-09-24 | Store-filtered SE | No Mestolo app. The nearest result was "Mesto.rest", a restaurant loyalty app. |
| 4 Domains | Pending (SE: Risk) | 2026-09-24 | [SEOceros: mestolo.com](https://seoceros.com/pl/mestolo.com) | The summary calls mestolo.com "a vegetarian cooking blog (DAS vegetarische Kochblog)", so it is registered and in use (unverified). |
| 5 Trademarks | Pending | 2026-09-24 | Registries blocked | — |
| 6 Language | Inconclusive | 2026-09-24 | Reviewer assessment | See above. |
| 7 Confusing similarity | Risk (low) | 2026-09-24 | as row 1 | Restaurants (class 43). |
| 8 Social handles | Pending (SE: Risk) | 2026-09-24 | [@mestolo.de (via SE)](https://www.instagram.com/mestolo.de/) | "mestolo.de - Maria Fratini". |

---

#### Session-1 names retained on the international shortlist: `Ramekin` and `Tadam`

Their session-1 evidence (2026-09-24) follows unchanged. Session 2 re-ran no checks on them, because the official sources were still blocked and the search-engine evidence is from the same day.

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

**Session 2 note (2026-09-24):** Ramekin stays on the international shortlist and is now ranked 2 (top 3). No new evidence. C10 = 4: it is an English kitchen word with a French root (*ramequin*) and is used in cooking across Europe, but it is less familiar to Polish home cooks than to English ones.

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

**Session 2 note (2026-09-24):** Tadam stays on the international shortlist as an alternate (rank 5). No new evidence. C10 = 5: "ta-dam!" (PL, FR) and "ta-da!" (EN) are understood across Europe.

---

### 6.4 Polish-flavoured alternatives (not recommended as the main brand for international expansion)

> **Superseded as main-brand candidates, 2026-09-24 (PO feedback).** In session 1, Oskoma and Smakora were in the top 3. They are kept here as the best two Polish-rooted names, with all their session-1 evidence (dated 2026-09-24). They could still work in Poland as a sub-brand, a campaign line or a feature name (for example, a "cravings" feature for Oskoma). They are not recommended as the international brand.

| Name | Session-1 sum /35 | C10 /5 | Why it is kept | Why it is not the main brand |
|---|---|---|---|---|
| **Oskoma** | 30 | 1 | The best fit to the core promise ("eat what you feel like", PRD §1). Spelled phonetically in PL and EN. | The meaning only exists in (archaic) Polish; the "-oma" ending sounds medical in English; Polish restaurants and cafés use the name. |
| **Smakora** | 32 | 2 | The highest session-1 score. Easy in PL and EN. | It reads as Polish ("smak"); the same name is used by a Swedish recipe site; neighbours such as Smaker and SMAKO™ share the stem. |

Session-1 matrix rows (unchanged):

| Name | 1 Competitors / similar | 2 App Store | 3 Google Play | 4 .com | 4 .app | 4 .io | 4 .pl | 5 Trademarks | 6 Language PL/EN | 7 Confusing similarity | 8 Social handles | E Search engine |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Oskoma** | Risk: PL restaurants and cafés | Pending (Inconclusive) | Pending (Inconclusive) | Pending | Pending | Pending | Pending (Risk: appears listed for sale) | Pending | Risk: "-oma" medical ring (EN); RU "оскомина" | Risk: Restauracja Oskoma (PL, class 43) | Pending (Risk: @oskoma held by an individual) | Risk |
| **Smakora** | Risk: smakora.se recipe site (SE) | Pending (Inconclusive) | Pending (Inconclusive) | Pending | Pending | Pending | Pending | Pending | Inconclusive: EN "smack" echo | Risk: Smaker (PL recipe app), SMAKO™ | Pending | Risk |

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

### 6.5 Session-1 names removed from the shortlist (evidence retained)

> **Superseded 2026-09-24.** In session 2 these ten names were taken off the shortlist. Smako, Yemo, Pora, Miska, Doma, Akurat, Zapas, Kredens and Prepko are Polish-rooted (PO feedback), and they are weaker than Oskoma and Smakora. Porcio is not Polish-rooted, but it was dropped on its own session-1 evidence: the pig connotation in FR/IT/ES and Portio AI. Their session-1 evidence (all dated 2026-09-24) is kept below, unchanged.

Session-1 note, kept as written: All checks are dated 2026-09-24. Store, domain, trademark and handle checks are **Pending** for every name because the official sources were egress-blocked (§5.1). They are listed once per name in the tables rather than in every row.

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

### 6.6 Session-1 check matrix and ranking (superseded 2026-09-24)

> **Superseded by §6.1–§6.4 (PO feedback, 2026-09-24).** Kept as written in session 1. The session-1 recommendation (top 3: Ramekin, Oskoma, Smakora; alternate: Tadam) is replaced by the session-2 recommendation in §6.2 (top 3: Tangram, Ramekin, Palmo; alternates: Sapimo, Tadam).

#### Session-1 check matrix (14 names)

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

#### Session-1 scores (C1–C7) and ranking

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

---

## 7. Risks and unresolved checks

### 7.1 Session-level limits (updated 2026-09-24)

1. **No authoritative check could run in either session.** Every store, domain, trademark and handle status is Pending (§5.1). Rankings rest on search-engine evidence, which can miss registered marks, unlaunched apps, and parked or reserved domains.
2. **Absence is not availability.** Where the search found nothing (for example Sapimo anywhere, or Tangram and Palmo in food), the status is Inconclusive. It must not be read as "free".
3. **Language checks are the reviewer's own assessment.** C10 raises the bar: native-speaker checks are now needed in PL, EN (UK and US), DE, FR, ES, IT, PT, NL and SV for the top 3 and the alternates. They are pending.
4. **Trademark reality.** Real words used arbitrarily (Tangram, Palmo, Ramekin, Tadam) will have registrations in other classes, and Tangram is a common noun for puzzle games in class 9. Coinages (Sapimo) are likely stronger but carry less meaning. Italian words (Sarto, Portata, Mestolo) are weak in Italy, and Portata may be descriptive there. Only a registry search and an attorney can settle this.
5. **The category is filling fast.** Session 2 found more than fifteen same-category apps that weren't in the session-1 landscape (§3.4). A name that is Inconclusive today can have a competitor next month, so re-check at decision time.

### 7.2 Name-specific risks (session 2: top 3 and alternates)

| Name | Main remaining risk | What would resolve it |
|---|---|---|
| **Tangram** | Exact name widely used by puzzle apps (class 9), so store search returns puzzles; US TANGRAM software marks seen on third-party sites (goods unknown); the .com is very likely registered; exact handles are probably taken | EUIPO, TMview (EM, PL), UPRP, WIPO and USPTO in classes 9, 42, 44 (and 35, 41), including the goods of US serial 88473186; an attorney's view on registering a common puzzle noun for nutrition software; RDAP for .com, .app, .pl and .io; a store title with a descriptor ("Tangram: Meal Planner") |
| **Ramekin** | Possible descriptiveness for recipe content; moderate PL familiarity; the .com is very likely registered (unverified); three syllables | As in session 1 (§7.3), plus a PL comprehension test |
| **Palmo** | Two exact-name class-9 apps (a budget tracker and a chat analyser); PALMO CALIFORNIA (US, class 14); many handles in use; a remote ES slang echo | Registry searches in 9, 42, 44 and 35; RDAP; handle variants (`palmoapp`, `getpalmo`); a Spanish-speaker listener check |
| Sapimo (alternate) | Meaning not obvious; EN "sap" and PL "sapie" echoes; shares "Sap-" with Sapora (a recipe app) | Listener test in PL and EN; an attorney's view on Sapora; RDAP |
| Tadam (alternate) | Same-name class-9 software and consumer brands; weak distinctiveness | As in session 1 (§7.3) |

**Open checks per shortlisted name:** App Store (iTunes API PL/US/GB), Google Play (PL/US), RDAP for .com, .app, .io and .pl, EUIPO, TMview (EM + PL, plus IT for the Italian words and SE for Smakora), UPRP, WIPO, USPTO, UK IPO, and handles on Instagram, TikTok, Facebook, YouTube, X, Threads and LinkedIn. All are Pending.

### 7.3 Session-1 name-specific risks (superseded 2026-09-24)

> Kept as written in session 1. Oskoma and Smakora are now Polish-flavoured alternatives (§6.4), and the Ramekin and Tadam rows remain valid.

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

Run these for **Tangram, Ramekin and Palmo** first, then **Sapimo and Tadam**, then the rest of §6.1 and the §6.4 alternatives. Replace `<n>` with the lowercase name.

- App Store: `https://itunes.apple.com/search?term=<n>&entity=software&country=pl` (then `us`, `gb`)
- Google Play: `https://play.google.com/store/search?q=<n>&c=apps&gl=PL` (then `gl=US`)
- .com: `https://rdap.verisign.com/com/v1/domain/<n>.com`
- .app: `https://pubapi.registry.google/rdap/domain/<n>.app`
- .pl and .io: get the RDAP base URL for `pl` and `io` from `https://data.iana.org/rdap/dns.json`, then `<base>/domain/<n>.pl` and `<base>/domain/<n>.io`
- Also re-check the near-conflicts found in session 2: "saviMon" (for Savimo), "Sapora" (for Sapimo), PORTA and "portata.dev" (for Portata), and the US TANGRAM serial 88473186 (for Tangram).

### 8.2 Owner actions (need an account, or are the owner's call)

1. **Trademark searches**, until the agent can reach the registries. Search each name as an exact word, then with a wildcard and phonetically:
   - **EUIPO eSearch plus** (https://euipo.europa.eu/eSearch/): Trade marks, "Word" = `TANGRAM`, then `RAMEKIN`, `PALMO`, `SAPIMO`, `TADAM`. Nice classes 9, 29, 30, 35, 41, 42, 43, 44. Status: all, then filed and registered only. Repeat with `TANGRAM*`, `PALM*`, `SAPI*` and `SAVIM*`.
   - **TMview** (https://www.tmdn.org/tmview/): the same terms. Offices: EM, PL, DE, FR, ES, IT, SE, WO. Same classes. Record live or dead status, owner and filing date.
   - **UPRP e-Wyszukiwarka** (https://ewyszukiwarka.pue.uprp.gov.pl/): "Znaki towarowe", word element `tangram` / `ramekin` / `palmo` / `sapimo` / `tadam`.
   - **WIPO Global Brand Database** (https://branddb.wipo.int/): Brand = the name, Nice classes as above, designations PL, EU, US, GB.
   - **USPTO** (https://tmsearch.uspto.gov/): `TANGRAM` (open serial 88473186 and TANGRAM FLEX and record their goods), `PALMO`, `RAMEKIN`, `SAPIMO`, `TADAM`; classes 9, 42, 44. **UK IPO** (https://trademarks.ipo.gov.uk/): the same.
2. **App Store Connect name check** for "Tangram", "Palmo" and "Ramekin" with a descriptor (for example "Tangram: Meal Planner"). This needs the owner's Apple Developer account. Reserve a name only when ready to commit, because Apple holds reservations for a limited time.
3. **Google Play Console check:** needs the owner's developer account.
4. **Trademark attorney clearance** before adoption, in at least the EU (EUIPO) and Poland (UPRP), plus the US and UK if English-speaking launches are planned. Ask specifically about: Tangram as a common puzzle noun in class 9; Palmo's coexistence with the class-9 apps; and Sapimo against Sapora. Nothing here is a legal opinion.
5. **Social handles:** only signing up confirms a handle is free. The owner decides whether to sign up for `<name>`, `<name>app`, `get<name>` and `<name>.pl` on Instagram, TikTok, Facebook, YouTube, X, Threads and LinkedIn.
6. **Domain purchase decisions:** the owner buys; the agent never does. Short dictionary words (Tangram, Palmo, Ramekin) very likely have a registered .com, so decide early whether a variant (`get<name>.com`, `<name>.app`) is acceptable.
7. **Audience and native-speaker test (international):** 5–10 people from the PL wedge (PRD §3), 3–5 native English speakers, and 2–3 each for DE, ES and IT. Test the top 3 and alternates for pronunciation after hearing each name once, spelling, associations and appeal. For Palmo, include Spanish slang; for Sapimo, the "sap" and "sapie" echoes.

### 8.3 Decisions for the Product Owner

1. **Real word or coinage.** Tangram, Palmo and Ramekin carry meaning but share their word with others. Sapimo is more ownable but explains less. Which trade-off does the PO prefer?
2. **Do Italian-word names count as "international"?** Sarto, Portata and Mestolo read as foreign-but-friendly in Poland and most of Europe, but they are ordinary words in Italy. They are shown in §6 but not recommended.
3. **Second market.** Naming the first expansion market (for example the UK, DACH or Spain) would focus the language tests and the trademark offices to search.
4. **Polish-flavoured names.** Keep Oskoma or Smakora for a PL-only sub-brand or feature, or drop them.

**Do not** rename application identifiers, bundle IDs, packages, domains or assets until the Product Owner approves a final name (CLAUDE.md).

### 8.4 Session-1 next steps (superseded 2026-09-24)

> Replaced by §8.1–§8.3. Kept as written in session 1, where the priority names were Ramekin, Oskoma, Smakora and Tadam.

#### Session-1 8.1 Re-run on a network with registry access

Run these for Ramekin, Oskoma, Smakora and Tadam first, then the rest of §6. Replace `<n>` with the lowercase name.

- App Store: `https://itunes.apple.com/search?term=<n>&entity=software&country=pl` (then `us`, `gb`)
- Google Play: `https://play.google.com/store/search?q=<n>&c=apps&gl=PL` (then `gl=US`)
- .com: `https://rdap.verisign.com/com/v1/domain/<n>.com`
- .app: `https://pubapi.registry.google/rdap/domain/<n>.app`
- .pl and .io: get the RDAP base URL for `pl` and `io` from `https://data.iana.org/rdap/dns.json`, then `<base>/domain/<n>.pl` and `<base>/domain/<n>.io`

#### Session-1 8.2 Owner actions

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
| 2026-09-24 | **Second research session (brand-researcher): international-first round.** It responds to the Product Owner's feedback on session 1: "Smakora is mostly a Polish name, like most of them." (11 of 14 shortlisted names were Polish-rooted.) At the start, each official source was retried once with a plain request (curl for all; WebFetch also for the RDAP, IANA, iTunes, Play and TMview URLs). All were still egress-blocked (§5.1), so every authoritative check remains **Pending**, and screening used WebSearch only. **Added:** the international-first strategy with the PO feedback, and the new criterion C10 (international neutrality) (§2.1, §2.3); an international positioning statement (§1); same-category apps found in session 2 (§3.4); 87 new candidates, #74–#160 (§4.6); the session-2 access log and screening evidence (§5.1, §5.3); a rebuilt shortlist of **9 international names** (Tangram, Ramekin, Palmo, Sapimo, Tadam, Savimo, Sarto, Portata, Mestolo) with a check matrix including C10, scores and per-name evidence (§6.1–§6.3); new risks (§7.1–§7.2) and next steps with owner decisions (§8.1–§8.3). **Superseded, not deleted:** the session-1 conclusion that Polish-rooted names were the best opening (§2.2, §3.3); the session-1 shortlist, matrix and ranking (§6.6); session-1 risks and next steps (§7.3, §8.4). Oskoma and Smakora moved to "Polish-flavoured alternatives (not recommended as the main brand for international expansion)" (§6.4). The other session-1 names moved to §6.5 with their evidence. **Top 3 for further investigation** changed from Ramekin, Oskoma, Smakora to **Tangram, Ramekin, Palmo** (alternates: Sapimo, Tadam). No name was selected. |
