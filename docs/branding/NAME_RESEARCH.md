# FitMeal AI: brand name research

Maintained by the `brand-researcher` agent ([.claude/agents/brand-researcher.md](../../.claude/agents/brand-researcher.md)). Findings go to the `engineering-manager`. Choosing the brand requires Product Owner approval (CLAUDE.md). Nothing in this report is a naming decision, and nothing here is legal clearance.

"FitMeal AI" is the working title. This report looks for the product's public brand name.

**Status (2026-09-25): fourth research session done (short real English food-word round). Live access is still limited.**

> **Product Owner feedback on session 3:** "nothing from proposals". This rejects the whole session-3 shortlist (Zubo, Kazu, Dozo, Nimbo, Gobo, Bibim, Zumo, Kumo, Panko, Gumbo, Mogu, Pappa). **PO style questionnaire (2026-09-25):** preferred style = **short real English word** (the way Bolt, Lime, Oura, Notion or Headspace are real words), not coined sounds and not foreign words; food hint = **clearly** (people should guess it is a food or meal app from the name alone); no example brands given. Session 4 generated 129 real English food, cooking and kitchen words (§4.8), screened them (§5.5), and built a new current shortlist of 13 names (§6.8). The session-3 shortlist and top 3 are marked **superseded (PO: "nothing from proposals")**. They have not been deleted.
>
> **Current recommendation for further investigation (not a selection):** top 3 **Salsa, Pretzel, Donut**; alternates **Pickle, Handful** (§6.8.2).
>
> **Key session-4 finding:** every example word in the brief (Ladle, Pinch, Crumb, Pantry, Spoonful, Zest), plus Forkful, Spoon, Basil, Supper, Stir, Savor and Lemon, is already the name of a meal-planning, recipe or nutrition app, several of them with social-recipe import and macros (§3.6). Real English food words are the most crowded naming space found in four sessions.

> **Product Owner feedback on session 2 (verbatim):** "i dont like those names they are too long and not catchy". This covers the whole session-2 shortlist (Tangram, Ramekin, Palmo, Sapimo, Tadam, Savimo, Sarto, Portata, Mestolo). Session 3 re-ran the naming for **3–5 letters, 1–2 syllables, catchy and international** (§2.4), screened 111 new candidates (§4.7, §5.4) and built a new current shortlist of 12 names (§6.7). The session-2 shortlist and top 3 are marked **superseded (PO: too long, not catchy)**. They have not been deleted.
>
> *(Superseded 2026-09-25, PO: "nothing from proposals".)* ~~**Current recommendation for further investigation (not a selection):** top 3 **Zubo, Kazu, Dozo**; alternates **Nimbo, Gobo** (§6.7.2).~~

> **Product Owner feedback on session 1:** "Smakora is mostly a Polish name, like most of them." Eleven of the fourteen session-1 shortlisted names were Polish-rooted (Oskoma, Smakora, Smako, Doma, Akurat, Miska, Pora, Kredens, Zapas, Prepko, Yemo). The product launches in Poland and then expands internationally, so the brand must not read as a Polish word. Session 2 re-ran the naming international-first (§2.1) and rebuilt the shortlist (§6). Session-1 conclusions that this changes are marked **superseded**. They have not been deleted.

> **Live web access, sessions 1, 2, 3 and 4: partial.** Only **WebSearch** (a search engine) worked. At the start of sessions 2, 3 and 4, each official source was retried once with a single plain request. Every one was still **blocked by the network egress proxy**: registry RDAP (.com, .app, the IANA bootstrap), the iTunes Search API, Google Play, EUIPO, TMview, UPRP, WIPO Brand DB, USPTO and UK IPO. Per the task, no workaround was attempted: no proxy probing, no `whois` or `dig` substitutes, no mirror sites. Details are in §5.1.
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

**Session 3 addition (2026-09-25, PO feedback).** The name itself has to carry the "a little playful" part of the personality: short, punchy and fun to say, the way Noom, Uber, Zoom, Yuka, Bolt or Kiwi are. The store descriptor ("…: Meal Planner") and the product carry the explanation (§3.4 takeaway), so the name does not need to describe anything.

**Session 4 addition (2026-09-25, PO questionnaire).** The name should be a **short real English word with a clear food hint**, so that someone hearing it guesses "food or meal app" without the descriptor. The name now carries some of the explaining that §2.4 left to the descriptor, but it must still suggest rather than describe (PRD §5 principles still apply: food-positive, never moralizing, never medical).

**Positioning statement (working).** For people in Poland who track what they eat but won't give up the food they love, [Brand] is the meal planner that makes any recipe fit your numbers, your budget and your prep day, and shows you exactly what it changed.

**Positioning statement, international version (session 2, working).** For people who track what they eat but won't give up the food they love, [Brand] is the meal planner that makes any recipe fit your numbers, your budget and your prep day, and shows you exactly what it changed.

---

## 2. Naming strategy

> **Current strategy: §2.5 (session 4), placed first below.** It is numbered 2.5 so that existing references to §2.1–§2.4 still point to the right text. §2.4 (session 3), §2.1 (session 2) and §2.2 (session 1) are kept for history.

### 2.5 Session 4: short real English food words (current, 2026-09-25)

**Why this changed.** The Product Owner's review of session 3: "nothing from proposals". The PO then answered a style questionnaire (2026-09-25):
- **Preferred style:** a **short real English word**, in the way Bolt, Lime, Oura, Notion or Headspace are real words. Not coined sounds (Zubo, Nimbo) and not foreign words (Kazu, Dozo, Gobo).
- **Food hint:** **clearly**. People should guess it is a food or meal app from the name alone.
- **Example brands:** none given.

**Rules for session 4** (these replace the §2.4 form rules; the §2.1 international rules and C1–C11 still apply where not contradicted):
1. **A real English word**, single word, 3–8 letters, 1–2 syllables. A two-word compound only if it reads as one word ("Forkful", "Mealbox"). Loanwords that are in English dictionaries (pesto, salsa, tapas, nacho) count, and are flagged as such.
2. **Clearly food, eating, cooking or kitchen:** ingredients, dishes, utensils, cooking actions, tastes, portions, pantry and prep words.
3. **Suggestive, not generic.** The name of the service ("Meal Planner", "Diet", "Recipes", "Nutrition") is unregistrable. Each candidate is marked **D/S**: **S** = suggestive or arbitrary for nutrition software (names a specific food or tool, so it evokes food without describing the service); **B** = borderline (a portion, meal or prep word that could be read as describing a feature, e.g. Handful, Batch, Lunchbox); **D** = descriptive (Snack, Mealbox).
4. **Easy for Poles** with basic English (PRD §3 wedge). Flagged: "th", "w", silent letters, "ch" (Poles read [x]), soft "g", "ea"/"oa"/"ay"/"au" spellings and silent final "e" (Poles read letter by letter, §2.1). No Polish-rude or awkward echoes (PL "pan" = Mr, "pot" = sweat).
5. **No diet guilt, body or medical meaning** (Lean, Slim, Skinny, Cheat, Guilt and similar were excluded without listing). PRD §5, §12.
6. **No reuse** of names screened out as taken in §4 and §5 (Whisk, Mise, Morsel, Paprika, Plum, Miso, Nori, Bento, Crouton, Pestle, Honeydew, Umami, Kale, Grub, Chow, Nosh, Fig, Dill, Zing, Gulp, Nibs, Larder, Simmer, Skillet, Platter, Tiffin, Sprig, Nutmeg, Olio, Manna, Riff, Gumbo, Panko). No session-1 word was revisited.
7. **Store title:** the name plus a descriptor must fit 30 characters. The reference descriptor is ": Meal Planner & Macros" (23 characters), so the name can have at most 7 letters in that form ("Pretzel: Meal Planner & Macros" is exactly 30). Longer names need the shorter ": Meal Planner" (14 characters).

**Evidence rule for ranking (task instruction).** English food words are crowded, so a same-name use is weighed by *where* it is: **serious** if it is a food, recipe, nutrition or meal-planning app or service; **lighter** if it is elsewhere (dance, comics, fintech, HR software). Search-engine evidence is at most Risk or Inconclusive (§5.5).

**What session 4 learned (evidence in §3.6 and §5.5):**
- **Real English food words are the most crowded space in four sessions.** Of the 111 words screened by search, **43 are already the exact name of a recipe, meal-planning or nutrition app or service**, and about 14 more have a near-identical name in the category, often with the same features as PRD §8 (social-recipe import, macros per portion, weekly plan, allergens, budget). Examples: **Ladle** (four apps), **Pinch**, **Crumb/Crumbs**, **Pantry**, **Spoonful**, **Forkful**, **Spoon**, **Basil**, **Supper**, **Stir**, **Savor**, **Lemon**, **Garlic**, **Clove**, **Carrot**, **Mango**, **Peach**, **Munch**, **Feast**, **Sprout**, **Harvest**, **Sizzle**, **Sumac**, **Saffron**, **Fennel**, **Tofu**, **Sesame**, **Lentil**, **Olive**, **Pepper**, **Scoop**, **Dollop**, **Nibble**, **Yum**, **Apron**, **Picnic**, **Maple**, **Tidbit**.
- **Every example word in the brief is taken in the category:** Ladle, Pinch, Crumb, Pantry, Spoonful (§5.5) and Zest (§5.4, "Zest: Meal Planner & Recipes").
- **Portion and utensil words are gone first** (Pinch, Crumb, Scoop, Dollop, Spoonful, Forkful, Spoon, Ladle, Spatula, Nibble). **Specific dishes and snacks** (Pretzel, Donut, Salsa, Nacho, Bagel) are the least used by nutrition apps, because they don't sound "healthy". Their namesakes are mostly restaurants and unrelated software, which is the lighter kind of conflict.
- **"Clearly food" and "suggestive, not generic" pull against each other.** The clearer the food hint, the more likely the word is either taken in the category or reads as describing a feature (Snack, Brunch, Supper, Lunchbox, Batch, Portion, Handful).
- **Polish traps specific to English food words:** Pan (PL "Mr/sir"), Pot (PL "sweat"), Curry (PL "kury", hens), Nacho (Poles read "ch" as [x]), Bagel (Poles read "BA-gel"), Gravy (Poles read "GRA-vy"), Ginger (Poles read a hard "g"), and every "oa"/"ea"/"ay" word (Toast, Loaf, Roast, Oats, Feast, Tray).
- **Other-language trap:** DE *Pickel* = pimple (Pickle).

### 2.4 Session 3: short and catchy (superseded 2026-09-25)

> **Superseded 2026-09-25 (PO: "nothing from proposals").** The session-3 rules (3–5 letters, coined or foreign sounds, the name need not describe anything) are replaced by §2.5 (real English word with a clear food hint). The findings below (crowding of short names, the Japanese-word cluster, Polish ear traps) remain valid as evidence. The text is kept as written.

**Why this changed.** The Product Owner's review of session 2, verbatim: "i dont like those names they are too long and not catchy". The session-2 shortlist had names of 5–7 letters and up to three syllables (Tangram, Ramekin, Sapimo, Portata, Mestolo), several of them real words chosen for their meaning. The PO had already rejected the mostly Polish-rooted session-1 names. So the brand has to be **short and catchy**, and still **international**.

**Rules for session 3** (these tighten §2.1; everything in §2.1 that is not contradicted still applies):
1. **Length:** 3–5 letters (6 only if exceptionally good), 1–2 syllables. Ideally one stressed syllable, or a bouncy two-syllable CV-CV pattern (Zu-bo, Ka-zu).
2. **Catchy:** punchy, rhythmic, fun to say, remembered after one hearing, and good as a one-word icon or wordmark. Reference points: Noom, Uber, Zoom, Hinge, Yuka, Bolt, Lime, Oura, Kiwi, Mela, Zego. A strong consonant, a clear vowel, often a repeated sound. Scored as the new criterion **C11** (§2.3).
3. **International:** no Polish word or Polish root as the concept. A Polish speaker must still read it correctly on first sight, so use letters that sound the same in PL and EN (a, e, i, o, u, b, d, f, g, k, l, m, n, p, r, s, t, z). Avoid c, j, w, y, ch, sz, cz, th, and "ee"/"oo" spellings that Poles misread ("Noom" reads "no-om" in Polish).
4. **No** diacritics, hyphens or numbers. **No** medical, diet-guilt or body connotations (PRD §5, §12). **Nothing close** to the §3 competitors, especially Fitatu, Fitia, Yazio, Yuka, Noom, Mealime, Mela, Portio and Sapora.
5. **No reuse** of names already in §4.1–§4.6.

**What session 3 learned (evidence in §3.5 and §5.4):**
- **Short names are far more crowded than long ones, and the category is the most crowded of all.** Of 111 candidates, about 45 hit a same-category app (meal planning, recipes, macro or calorie tracking, food ordering) on the first search. Examples: Nomo (NomNom, noms), Tasto, Plum, Miso, Nori, Bento, Momo, Lumo, Numo, Nubo, Paku, Miam, Pasto (Plento Pasto), Tamo (Tomo), Tuki (Tucki), Zesto, Zing.
- **Every 4-letter CV-CV name is used by someone.** None of the shortlisted names is free of same-name apps. The test that still separates them is **whether the same-name uses are in food, nutrition or health**. The shortlist keeps names whose same-name uses are in other fields (ride-hailing, radio, real estate, marketplaces), and flags the ones that touch food or health.
- **Food words from Japanese and Korean read as international, catchy and easy for Poles** (Kazu, Dozo, Gobo, Kumo, Mogu, Panko, Bibim), because Japanese and Korean romanisation uses the same vowels as Polish. But the popular ones (Miso, Nori, Umai, Mizu, Bento, Momo) are already taken in the category.
- **Polish ear traps found this round:** "Kazu" sounds close to "Kaziu", the familiar form of the name Kazimierz; "Dozo" echoes "doza" / "dozować" (dose, to dispense); "Mogu" is Russian for "I can"; "Panko" is also a Polish pest-monitoring brand. These are recorded against each name in §6.7.3.
- **Slang and body traps screened out without searching:** Sumo, Kilo, Gula (ES gluttony), Pica (an eating disorder), Nudo (IT naked), Kapo, Suka, Nuda, Pipa, Bimbo, Zizi, Popo, Kuku, Zaza (§4.7.5).

### 2.1 International-first (session 2; superseded in part 2026-09-25)

> **Superseded in part, 2026-09-25 (PO: too long, not catchy).** The session-2 form rule (4–8 characters, 1–2 syllables "where practical") and the conclusion that "the cleanest openings were" real-word metaphors such as Tangram, Ramekin and Palmo are replaced by §2.4. The international rules below (no Polish root, letters that read the same in PL and EN, the "si/zi/ni/ci" and silent-"e" traps, C10) still apply. The text is kept as written.

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

C1–C9 are unchanged from session 1. C10 was added in session 2 after the PO feedback. C11 was added in session 3 after the PO feedback on session 2.

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
| **C11** | **Catchiness:** short (3–5 letters, 1–2 syllables), punchy, rhythmic, fun to say, remembered after one hearing, strong as a one-word icon. Scored 1–5: 5 = a strong consonant onset, clear vowels and a bounce or repeated sound, instantly repeatable (Zoom, Kiwi); 3 = short and easy but flat or ordinary; 1 = long or hard to repeat. Reviewer assessment until a listener test is run. | PO feedback, session 2 ("too long and not catchy") |

**Session 4 note (2026-09-25).** For real English words, C11 is scored on the same 1–5 scale but with the §2.5 length (3–8 letters, 1–2 syllables); a 6–7 letter word is not penalised for length alone. Two extra columns are shown in §6.8 but not scored as criteria: **Food hint** (clear / moderate / weak, the PO questionnaire answer) and **D/S** (suggestive / borderline / descriptive, §2.5 rule 3).

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

### 3.5 Same-category apps found in session 3

Checked 2026-09-25 via WebSearch only. These apps surfaced while screening the session-3 short names. None of the pages could be opened (egress-blocked), so the descriptions are the search results' titles and summaries, not verified store data. The most relevant ones for PRD §1 and §8 are listed first.

| Brand | What the search showed | Link | Relevance |
|---|---|---|---|
| **Tasto** | "Tasto: Recipe Manager"; summary: saves recipes from Instagram, TikTok and YouTube, "full nutritional breakdown… calories, protein, carbs, and fats", weekly plan, AI ingredient swaps, allergen highlights | [App Store](https://apps.apple.com/us/app/tasto-recipe-manager/id6760462265), [tastoapp.com](https://tastoapp.com/) | **Very close to PRD §8.1–§8.4** (social import, macros, swaps, allergens) |
| **Miso / Miso Cook** | "Miso - Recipe Keeper" (social import, nutrition, "cost per serving"); "Miso Cook: Meal Planner" (calorie goal 1200–4000 kcal, weekly plan); misoapp.ca (calorie and macro targets, budget, pantry) | [Miso](https://apps.apple.com/us/app/miso-recipe-keeper/id6756516262), [Miso Cook](https://apps.apple.com/us/app/miso-cook-meal-planner/id6757978247), [misoapp.ca](https://misoapp.ca/) | **Very close** (import, calories, cost, pantry) |
| **Plum Recipes** | Summary: downloads Instagram, TikTok and YouTube recipes; "can estimate calories and macros"; suggests meals for the week | [plumrecipes.app](https://www.plumrecipes.app/) | Close (import plus macros) |
| **noms / NomNom** | "noms - AI recipe & meal plan" (turns a video link into a structured recipe with nutrition); "NomNom: Meal Planner & Recipes" (week of cheap dinners, "set your budget") | [noms](https://apps.apple.com/us/app/noms-ai-recipe-meal-plan/id6748933312), [NomNom](https://apps.apple.com/us/app/nomnom-meal-planner-recipes/id6788049718) | Close (import; budget planning, cf. PRD §8.8) |
| **Tomo** | "Tomo - Diet & Calories"; summary: recipes "based on your tastes, budget and needs", grocery lists | [App Store](https://apps.apple.com/us/app/tomo-diet-calories/id6793031588) | Close (budget plus calories) |
| **Plento Pasto** | "Plento Pasto: Meal Planner"; summary: plans "around your grocery budget and what's already in your kitchen", allergy-aware | [plentopasto.com](https://plentopasto.com/) | Close (budget, pantry, allergies) |
| **Makros** | "Makros: Meal Plan & Grocery"; summary: fitness goals "without breaking the bank", macro tracker, weekly planner | [Google Play](https://play.google.com/store/apps/details?id=com.ivandiettracker.makros.makros_app&hl=en_US) | Close (macros plus budget) |
| Zesto | "Cooking Assistant AI - Zesto": AI recipes, meal planner, nutrition | [App Store](https://apps.apple.com/us/app/cooking-assistant-ai-zesto/id6584520256) | Recipe AI |
| Nori | "Nori - Family AI": allergy-aware weekly menus, grocery lists | [heynori.com](https://heynori.com/ai-powered-meal-planning) | Family planner (PRD §13 family phase) |
| Lumo | "Lumo - AI Chef": meal planning, pantry, nutrition insights | [App Store](https://apps.apple.com/ca/app/lumo-ai-chef/id6746675356) | Planner with pantry |
| Bento (several) | "Bento Box: Meal plans now easy" (import, plan, grocery lists); "Bento" meal planner (Quartz) | [App Store](https://apps.apple.com/us/app/bento-box-meal-plans-now-easy/id6758401088) | Meal-prep planner |
| Tucki, Tami Meal / TamiTales, Pomelo | Family and weekly meal-plan apps | [Tucki](https://apps.apple.com/us/app/tucki/id6503348465), [Tami Meal](https://tami-meal.com/), [Pomelo](https://apps.apple.com/us/app/pomelo-nutrition-meal-plans/id6763051623) | Planners |
| Momo, Paku, Numo, Nubo, Bimi, Bite AI, Umai | AI photo or chat nutrition trackers and recipe apps | [Momo](https://trymomo.app/), [Paku](https://apps.apple.com/us/app/paku-ai-calorie-counter-pet/id6752853273), [Numo](https://play.google.com/store/apps/details?id=com.astertechltda.numo), [Nubo](https://apps.apple.com/vn/app/nubo-body-and-nutrition/id1492780477), [Bimi](https://apps.apple.com/us/app/bimi-eat-better/id6756016601) | Trackers (the short-name space is dense here) |

**Takeaway.** Social-recipe import with macros, which session 2 found at Sapora and BonApp!, is now common (Tasto, Miso, Plum, noms). Budget-aware planning (PRD §8.8) is also appearing (NomNom, Tomo, Plento Pasto, Makros). Short, cute names are the default in this category, so a short name alone will not stand out: it has to avoid the food and nutrition apps above and be ownable.

### 3.6 Same-category apps found in session 4

Checked 2026-09-25 via WebSearch only. These apps surfaced while screening the session-4 English food words. None of the pages could be opened (egress-blocked), so the descriptions are the search results' titles and summaries, not verified store data. The most relevant ones for PRD §1 and §8 are listed first.

| Brand | What the search showed | Link | Relevance |
|---|---|---|---|
| **Savor** | "Savor - Meal Planner"; summary: tell it your "diet, allergies, budget, and household size", get "seven dinners… priced against your local supermarket", photo calorie logging, import from TikTok, YouTube and Instagram | [App Store](https://apps.apple.com/us/app/savor-meal-planner/id6615086643), [savoreat.co](https://savoreat.co/) | **Closest to PRD §1 + §8.8 found so far** (allergies, budget, supermarket pricing, social import) |
| **Ladle** (four apps) | "Ladle: Recipes & Meal Plan" (paste a TikTok or Instagram link; "protein, carb, fat, and calorie breakdowns per recipe and per day"); "useLadle: Meal Planner" (allergen exclusions); "Ladle - Recipes and Cooking"; ladle.cooking (AI sous-chef for women in midlife) | [App Store](https://apps.apple.com/us/app/ladle-recipes-meal-plan/id6760197380), [Play](https://play.google.com/store/apps/details?id=com.useladle.app&hl=en_US), [useladle.com](https://www.useladle.com/blog/meal-planning-app-dietary-restrictions) | **Very close to PRD §8.1–§8.4** |
| **Forkful** | "Forkful: Recipe Meal Planner" / "Forkful - Reels to meals": AI import from video links, weekly plan, grocery list, "automatic calories and macros for every recipe" | [App Store](https://apps.apple.com/us/app/forkful-recipe-meal-planner/id6760579706), [forkful.food](https://forkful.food/) | Very close (import plus macros) |
| **Supper** | "Supper: Recipes & Meal Planner": import from Instagram, TikTok, YouTube; household meal prep; "nutrition and macros information for every recipe" | [Play](https://play.google.com/store/apps/details?id=com.nabustudio.supper) | Very close (import, prep, macros) |
| **Basil** | "Basil: Recipes & Meal Planner": import incl. TikTok and Instagram; allergens; "calculate calories, protein, carbs, and fats for any recipe"; "Chef Basil" (7-day plan, weekly macros) | [App Store](https://apps.apple.com/us/app/basil-recipes-meal-planner/id6740829669), [Chef Basil](https://apps.apple.com/gh/app/chef-basil/id6761494168) | Very close |
| **Stir** | "Stir - Your Recipe Assistant": import from Instagram and TikTok, "tracks 7 nutrients per serving", weekly plan; "Stir & Store" recipe manager | [App Store](https://apps.apple.com/gb/app/stir-your-recipe-assistant/id6760202603), [stir-it.app](https://stir-it.app/download) | Very close |
| **Lemon** (EU) | "Lemon: Nutrition Made Simple": natural-language and photo logging, recipe import with "full breakdown per portion", meal plans | [App Store](https://apps.apple.com/us/app/lemon-nutrition-made-simple/id6618148167), [lemonnutrition.eu](https://lemonnutrition.eu/) | Close (EU nutrition app) |
| **Munchi** and other "Munch" apps | "Munchi: Meal Planner & Recipes" (calorie and macro targets, allergies); "Munched: Nutrition Scanner"; "MUNCH: AI Lifestyle Planner"; "Munch Metrics" | [Munchi](https://apps.apple.com/us/app/munchi-meal-planner-recipes/id6783936727), [Munched](https://apps.apple.com/us/app/munched-nutrition-scanner/id6740371125) | Close |
| **Crumb / Crumbs** | "Crumb: Recipe & Dinner Ideas" (fridge and pantry AI recipes); "Crumbs Meal Plans & Recipes" (YouTube and Instagram import); getcrumbapp.com | [Crumb](https://apps.apple.com/us/app/crumb-recipe-dinner-ideas/id6475651024), [Crumbs](https://apps.apple.com/us/app/crumbs-meal-plans-recipes/id6740446268) | Close |
| **Pesto** (on the **Polish** App Store) | "Pesto - Recipe App": "all-in-one recipe organizer, shopping list, and meal planner" | [App Store PL](https://apps.apple.com/pl/app/pesto-recipe-app/id6504192769) | Same category, **in the launch market** |
| MealPrepPro (developer **Nibble Apps**) | "MealPrepPro Meal Planner" by Nibble Apps: plans "automatically adapted to your calorie and macro needs" | [Play](https://play.google.com/store/apps/details?id=com.nibbleapps.meal_prep_pro), [nibbleapps.com](https://nibbleapps.com/) | Established macro meal-prep planner |
| Herbi | "Herbi: Meal Planner + Recipes": weekly dinner plan "based on your budget, dietary needs…", macros | [App Store](https://apps.apple.com/gb/app/herbi-meal-planner-recipes/id6777230233) | Budget planner (PRD §8.8) |
| Garlic, Clove, Spoon, Sumac, Saffron, Fennel, Sizzle, Spatula, Pepper, Apron, Harvest, Maple, Yum AI, Carrot AI | Recipe keepers and meal planners named after food and kitchen words (Clove and Garlic plan around the pantry; Maple "will sunset on December 31, 2026" per the summary) | [Garlic](https://apps.apple.com/us/app/garlic-recipe-keeper-planner/id6758080753), [Clove](https://apps.apple.com/us/app/clove-import-share-recipes/id6741995783), [Spoon](https://apps.apple.com/us/app/spoon-recipe-meal-planner/id6759272641), [Sumac](https://apps.apple.com/us/app/sumac-recipe-manager/id6753876940), [Saffron](https://apps.apple.com/us/app/saffron-your-digital-cookbook/id1438683531) | Planners and recipe keepers |
| Pantry, Scoop, Feast, Mango Bites, Mango AI, Peach, Lentil, Sesame, Olive, Spoonful, Tidbit, Crunch | Trackers, food scanners and nutrition coaches ("Pantry: macros from receipts"; "Scoop: Healthy Eating Out"; "Feast: Nutrition Coach"; "Peach: AI Calorie Tracker"; "Spoonful: Diet & Food Scanner"; "Tidbit … GLP-1 tracking") | [Pantry](https://getpantry.app/), [Scoop](https://apps.apple.com/us/app/scoop-healthy-eating-out/id6757786715), [Feast](https://apps.apple.com/us/app/feast-nutrition-coach/id6740829087), [Peach](https://apps.apple.com/us/app/peach-ai-calorie-tracker/id6748237403), [Spoonful](https://apps.apple.com/us/app/spoonful-diet-food-scanner/id1481914232) | Trackers |
| **Picnic** | "Picnic: Supermarket & Recipes": online supermarket with recipes and a meal planner (NL, DE, FR), "over 7 million downloads" per the summary | [App Store](https://apps.apple.com/us/app/picnic-supermarket-recipes/id1018175041) | Large EU grocer in the adjacent space |

**Takeaway.** In session 4 the category is even denser than in session 3: most short English food words that sound "healthy" or "kitchen-y" already name an app that does part of PRD §8. Savor is worth adding to the competitor watch list next to Sapora, Tasto and Adapto, because it combines allergies, budget and supermarket pricing with social import. The only real English food words still open in the category are **indulgent or specific dishes and snacks** (Pretzel, Donut, Salsa, Nacho, Bagel), whose namesakes are restaurants and unrelated software.

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

Result: **7 new international names shortlisted** (Tangram, Palmo, Sapimo, Savimo, Portata, Sarto, Mestolo). Together with Ramekin and Tadam from session 1, that makes 9 international names, plus 2 Polish-flavoured alternatives (§6). *(Superseded 2026-09-25, PO: too long, not catchy. See §4.7 and §6.7.)*

### 4.7 Session 3: short-and-catchy longlist (161–271)

111 new names were generated on 2026-09-25 under the §2.4 rules. None of them is in §4.1–§4.6. **S/L** = syllables / letters. "Search" means a WebSearch screen was run that day (evidence in §5.4). "Judgment" means the name was screened out on linguistic, strategic or reviewer-knowledge grounds; where reviewer knowledge was used, it says so and the name was not searched. A name screened out by judgment is not claimed to be taken. A loose link to food, taste, fit, ease or a bite is enough for the idea; catchiness matters more.

#### 4.7.1 Coined sounds (CV-CV and CV-CCV)

| # | Name | S/L | Idea behind it | Screen result |
|---|---|---|---|---|
| 161 | Zubo | 2/4 | A punchy "Z" and a round "-bo": sounds like something you'd happily grab, with no dictionary meaning to box it in | **Shortlisted, top 3** |
| 162 | Nimbo | 2/5 | Nimbus, nimble: light, quick plans (PT *nimbo* = rain cloud) | **Shortlisted, alternate** |
| 163 | Nomo | 2/4 | "Nom" (the eating sound) + "-o" | Screened out (search): "noms – AI recipe & meal plan", "NomNom: Meal Planner & Recipes" |
| 164 | Bito | 2/4 | "Bite" + "-o" | Screened out (search): many "Bite" nutrition apps sound the same (Bite AI, BiteRite, BiteTracker) |
| 165 | Bimo | 2/4 | Coined | Screened out (search): Bimo biscuits (ES); "Bimi – Eat Better" nutrition app |
| 166 | Tuki | 2/4 | Coined, bouncy | Screened out (search): "Tucki: Family Meal Planner" sounds identical |
| 167 | Tamo | 2/4 | Coined | Screened out (search): "Tomo – Diet & Calories" is one letter away |
| 168 | Dabo | 2/4 | Coined | Screened out (search): "Just Dabao" food-saving app; dabo kolo (Ethiopian snack) |
| 169 | Zumi | 2/4 | Coined | Screened out (search): Zumi Foods (nutrition shakes); "zumi" pet-nutrition app |
| 170 | Temi | 2/4 | Coined | Screened out (search): Tami Meal / TamiTales meal planners sound close |
| 171 | Numo | 2/4 | "Num" (yum) + "-o"; the form the PO gave as an example | Screened out (search): "Numo: Contador de calorias" (BR); "Numo World" meal delivery |
| 172 | Nubo | 2/4 | Coined | Screened out (search): "Nubo – Body and Nutrition" app; NuBo Wellness |
| 173 | Mubo | 2/4 | Coined | Screened out (judgment): no idea behind it; a grouped search found nothing (Inconclusive) |
| 174 | Zelo | 2/4 | IT *zelo* (zeal) | Screened out (search): "Zelo Delivery" grocery app; the query also returned ZOE nutrition |
| 175 | Zembo | 2/5 | Coined | Screened out (search): Zembo is the developer name of the "Circle Diet For Life" diet app |
| 176 | Nomba | 2/5 | "Nom" + "-ba" | Screened out (search): Nomba, a large Nigerian fintech (nomba.com, @nomba on X) |
| 177 | Zanko | 2/5 | Coined | Screened out (judgment): weak idea; the search surfaced Zankou Chicken |
| 178 | Deko | 2/4 | Coined | Screened out (judgment): DE *Deko* = decoration; no food idea (search Inconclusive) |
| 179 | Lumbo | 2/5 | Coined | Screened out (judgment): echoes "lumbar" (C5); the search surfaced Bumbo Foods and Slimbo meal plans |
| 180 | Pingo | 2/5 | Coined, bouncy | Screened out (search): "Pingo" restaurant-discovery app |
| 181 | Bibo | 2/4 | Latin *bibo* (I drink) | Screened out (search): "BIBO" restaurant-ordering app |
| 182 | Mixo | 2/4 | Mix + "-o" | Screened out (search): Mixo, a food-video social platform |
| 183 | Maku | 2/4 | Clipped "macro" | Screened out (search): "Makro" and "Makros" macro apps |
| 184 | Zesto | 2/5 | Zest + "-o" | Screened out (search): "Cooking Assistant AI – Zesto" recipe app |
| 185 | Tasto | 2/5 | Taste + "-o" (IT *tasto* = key) | Screened out (search): "Tasto: Recipe Manager" (social import plus macros) |
| 186 | Tosto | 2/5 | IT *tosto* (soon; toast) | Screened out (search): one letter from Tasto |
| 187 | Savo | 2/4 | Clipped "savour" | Screened out (judgment): too close to Savora and Savimo (§4); not searched |
| 188 | Prota | 2/5 | Clipped "protein" | Screened out (judgment): ties the brand to protein (C7) and is descriptive (C1) |
| 189 | Snak | 1/4 | "Snack" respelled | Screened out (judgment): a misspelt descriptive word (C1, C2) |
| 190 | Kombo | 2/5 | "Combo" with a K | Screened out (search): Kombo healthy meal boxes with macros (Serbia); "Kombo" ordering app |

#### 4.7.2 Playful doubled sounds and eating onomatopoeia

| # | Name | S/L | Idea behind it | Screen result |
|---|---|---|---|---|
| 191 | Mogu | 2/4 | JP *mogu-mogu* = "munch munch" | **Shortlisted (not recommended)** |
| 192 | Paku | 2/4 | JP *paku-paku* = eating in big bites (the root of "Pac-Man") | Screened out (search): "Paku: AI Calorie Counter Pet" |
| 193 | Zuzu | 2/4 | Doubled "zu" | Screened out (search): ZuZu restaurants and food delivery |
| 194 | Bimbam | 2/6 | "Bim-bam" bells | Screened out (judgment): echoes "bimbo" in EN; 6 letters (search Inconclusive) |
| 195 | Pompom | 2/6 | Doubled, bouncy | Screened out (judgment): cheerleading association; no food link (search Inconclusive) |
| 196 | Tamtam | 2/6 | The tam-tam drum | Screened out (search): TamTam, a Russian messenger app; TamiMeal |
| 197 | Happa | 2/5 | DE child word *happa-happa* (eat); JP *happa* (leaf) | Screened out (search): Happa Foods (baby food, IN); "h" reads as [x] in Polish |
| 198 | Miam | 1/4 | FR *miam!* (yum) | Screened out (search): "Miam" recipe and meal-plan app; MiamPlan; MIAM nutrition bars |
| 199 | Mums | 1/4 | SV *mums!* (yum) | Screened out (search + judgment): in UK English "mums" means mothers; mum-nutrition apps dominate |
| 200 | Nuum | 1/4 | The form the PO gave as an example | Screened out (judgment): an English speaker reads it exactly like Noom (§3 competitor) |
| 201 | Kiki | 2/4 | Doubled | Screened out (judgment): slang meanings in EN and FR (C3) |
| 202 | Zizi | 2/4 | Doubled | Screened out (judgment): FR child word for penis (C3) |
| 203 | Popo | 2/4 | Doubled | Screened out (judgment): colloquial "bottom" in DE and PL (C3) |
| 204 | Kuku | 2/4 | Doubled | Screened out (judgment): PL *kuku* = crazy (C3) |
| 205 | Zaza | 2/4 | Doubled | Screened out (judgment): US slang for cannabis (C3, C5) |
| 206 | Didi | 2/4 | Doubled | Screened out (judgment): DiDi ride-hailing (reviewer knowledge) |
| 207 | Pappa | 2/5 | IT *pappa* = grub, "food's ready" | **Shortlisted (not recommended)** |

#### 4.7.3 Short words from other languages, used arbitrarily

| # | Name | S/L | Idea behind it | Screen result |
|---|---|---|---|---|
| 208 | Kazu | 2/4 | JP *kazu* = number: it does the numbers so you don't have to | **Shortlisted, top 3** |
| 209 | Dozo | 2/4 | JP *dōzo* = "please, help yourself", said when offering food | **Shortlisted, top 3** |
| 210 | Gobo | 2/4 | JP *gobō* (burdock root); also a stage-light stencil that projects a shape | **Shortlisted, alternate** |
| 211 | Bibim | 2/5 | KR *bibim* = mixed (as in bibimbap): mix what you love with what you need | **Shortlisted** |
| 212 | Zumo | 2/4 | ES *zumo* = juice: the good stuff, squeezed in | **Shortlisted (not recommended)** |
| 213 | Kumo | 2/4 | JP *kumo* = cloud: light, always with you | **Shortlisted (not recommended)** |
| 214 | Panko | 2/5 | JP breadcrumbs: crunchy, playful, food-positive | **Shortlisted (not recommended)** |
| 215 | Gumbo | 2/5 | The Louisiana stew, and EN "a gumbo of…" (a mix) | **Shortlisted (not recommended)** |
| 216 | Kibo | 2/4 | JP *kibō* = hope | Screened out (search): Kibo Foods (protein chips, "complete meal kit", recipes) |
| 217 | Pepo | 2/4 | Botanical term for a squash-type fruit | Screened out (search): the "PEP: Diet" meal-plan app family; Peppo food app |
| 218 | Pomo | 2/4 | IT *pomo* (apple) | Screened out (search): "Pomelo – Nutrition Meal Plans"; POMO restaurant rewards |
| 219 | Tembo | 2/5 | Swahili "elephant" | Screened out (search): Tembo Money savings app (UK), Tembo (Postgres), Tembo Connect |
| 220 | Bento | 2/5 | JP lunch box: meal prep | Screened out (search): several "Bento" meal planners |
| 221 | Momo | 2/4 | Dumplings; doubled | Screened out (search): "Momo — Eat better", an AI nutrition app |
| 222 | Nori | 2/4 | Seaweed | Screened out (search): "Nori – Family AI" meal planner; "Nori" nutrition tracker |
| 223 | Miso | 2/4 | Soybean paste | Screened out (search): "Miso – Recipe Keeper"; "Miso Cook: Meal Planner" |
| 224 | Umai | 2/4 | JP "tasty" | Screened out (search): "Umai: Recipes with a spark" |
| 225 | Mizu | 2/4 | JP "water" | Screened out (search): "Mizu – Your CKD companion" (kidney-disease nutrition app; C5) |
| 226 | Mola | 2/4 | ES slang *¡mola!* ("it's cool") | Screened out (search + judgment): Mola Foods (sauces); "mola" is also a medical term (molar pregnancy) (C5) |
| 227 | Kudu | 2/4 | Antelope | Screened out (search): Kudu, a Saudi restaurant chain app |
| 228 | Lulo | 2/4 | Andean fruit | Screened out (search): Lulo, a WIC food-benefits app |
| 229 | Dango | 2/5 | JP rice dumpling | Screened out (search): "Dango: Food Delivery & More" |
| 230 | Mirin | 2/5 | JP rice wine | Screened out (judgment): an alcohol-based ingredient; near "Miri AI" nutrition app (search) |
| 231 | Kanzo | 2/5 | JP licorice root | Screened out (judgment): licorice root is sold as a herbal remedy (C5); weak idea |
| 232 | Posto | 2/5 | IT *a posto* (all sorted) | Screened out (judgment): sounds near Potto (meal planner, §3.4); PT *posto* = petrol station (search Inconclusive) |
| 233 | Rumbo | 2/5 | ES "heading, course" | Screened out (search): "Rumbo Fitness" app (calorie tracking); Rumbo.es travel |
| 234 | Tombo | 2/5 | JP "dragonfly" | Screened out (judgment): believed to be close to Tombow pens (reviewer knowledge); search Inconclusive |
| 235 | Tenko | 2/5 | A crisp JP-sounding word (JP *tenko* = roll call) | Screened out (search + judgment): restaurants; *tenko* (roll call) is also known as the title of a British TV drama about a WW2 prison camp (reviewer knowledge; C3) |
| 236 | Morso | 2/5 | IT "a bite" | Screened out (search): "Morso – Visual food journal"; a Morso AI recipe app |
| 237 | Kanpai | 2/6 | JP "cheers!" | Screened out (search): Kanpai Foods (candy); ordering apps; an alcohol toast |
| 238 | Pasto | 2/5 | IT "meal" | Screened out (search): "Plento Pasto: Meal Planner"; descriptive in IT |
| 239 | Mako | 2/4 | Shark | Screened out (search): MAKO bakery app; "Makros" meal-plan app |
| 240 | Mozo | 2/4 | ES "waiter" | Screened out (search): Mozo restaurant order-taking and payments platforms |
| 241 | Remo | 2/4 | IT/ES "oar" | Screened out (search): sounds like "Remi" and "Remy" recipe apps |
| 242 | Rumi | 2/4 | Name-like | Screened out (judgment): crowded (the poet); near Remy/Remi (search Inconclusive) |
| 243 | Pinta | 2/5 | ES *tiene buena pinta* ("looks tasty") | Screened out (judgment): believed to be a Polish craft brewery, Browar PINTA (reviewer knowledge, not searched) |
| 244 | Mimo | 2/4 | Coined-looking | Screened out (judgment): Mimo coding app (reviewer knowledge); PL *mimo* = "despite" (a Polish word) |

#### 4.7.4 Short English words used arbitrarily

| # | Name | S/L | Idea behind it | Screen result |
|---|---|---|---|---|
| 245 | Plum | 1/4 | Fruit; "a plum job" | Screened out (search): "Plum Recipe Saver", "Plum: Recipe Keeper" (import plus macros) |
| 246 | Fig | 1/3 | Fruit | Screened out (search): "Fig: Food Scanner & Recipes" (diet and allergy app) |
| 247 | Dill | 1/4 | Herb | Screened out (search): "Dill" campus food ordering, "dill Till" restaurant platform, "Dill Kitchen"; AU slang "dill" = fool (C3) |
| 248 | Zing | 1/4 | Zest, energy | Screened out (search): "Zing Wellbeing" (recipes, meal plans); Zing Coach |
| 249 | Gulp | 1/4 | Eating sound | Screened out (search + judgment): "Gulp Note" meal diary; "gulping food" is off-message |
| 250 | Nibs | 1/4 | Cocoa nibs; nibble | Screened out (search): "Nibbly" recipe and meal-scanner apps |

#### 4.7.5 Screened out on meaning or known brands alone (judgment unless stated)

| # | Name | S/L | Why screened out |
|---|---|---|---|
| 251 | Sumo | 2/4 | Body-weight connotation (C5) |
| 252 | Kilo | 2/4 | Weight unit (C5) |
| 253 | Gula | 2/4 | ES "gluttony" (C5) |
| 254 | Pica | 2/4 | The name of an eating disorder (C5) |
| 255 | Nudo | 2/4 | IT "naked" (C3) |
| 256 | Kapo | 2/4 | A concentration-camp prisoner functionary (C3) |
| 257 | Suka | 2/4 | PL and RU vulgar insult (C3) |
| 258 | Nuda | 2/4 | PL "boredom", and a Polish word (C3) |
| 259 | Pipa | 2/4 | PL vulgar slang (C3) |
| 260 | Bimbo | 2/5 | EN insult; Grupo Bimbo bakeries (class 30) (reviewer knowledge) |
| 261 | Zumba | 2/5 | Zumba fitness brand (reviewer knowledge) |
| 262 | Bozo | 2/4 | EN insult (C3) |
| 263 | Kobo | 2/4 | Rakuten Kobo e-readers (class 9) (reviewer knowledge) |
| 264 | Tazo | 2/4 | Tazo tea (class 30) (reviewer knowledge) |
| 265 | Numi | 2/4 | Numi organic tea (class 30) (reviewer knowledge); "NuMi" by Nutrisystem appeared in the Numo search |
| 266 | Lomi | 2/4 | Lomi kitchen composter (reviewer knowledge) |
| 267 | Olo | 2/3 | Olo restaurant-ordering platform (reviewer knowledge) |
| 268 | Orzo | 2/4 | Poles read "rz" as "ż" (C2) |
| 269 | Bimi | 2/4 | Search: "Bimi – Eat Better" nutrition app (seen in the Bimo search) |
| 270 | Zoe | 2/3 | Search: ZOE personalised-nutrition app (seen in the Zelo search) |
| 271 | Yuzu | 2/4 | Uses "y"; search: "Yuzu: Healthy Recipes App" (seen in the Mizu search) |

Result: **12 names shortlisted** (§6.7): Zubo, Kazu, Dozo, Nimbo, Gobo, Bibim, Zumo, Kumo, Panko, Gumbo, Mogu, Pappa. All are 4–5 letters and 2 syllables. The last six are kept for comparison and are not recommended (§6.7.2). *(Superseded 2026-09-25, PO: "nothing from proposals". See §4.8 and §6.8.)*

### 4.8 Session 4: short real English food words (272–400)

129 real English words were generated on 2026-09-25 under the §2.5 rules. None of them is in §4.1–§4.7. **L/S** = letters / syllables. **D/S** (§2.5 rule 3): **S** = suggestive or arbitrary for nutrition software; **B** = borderline (could be read as describing a portion, meal or prep feature); **D** = descriptive. **PL** = how a Polish speaker with basic English reads it (OK, or the trap). "Search" means a WebSearch screen was run that day (evidence in §5.5). "Judgment" means the name was screened out on linguistic, strategic or reviewer-knowledge grounds; where reviewer knowledge was used, it says so. A name screened out by judgment is not claimed to be taken. Loanwords (pesto, salsa, tapas, nacho, tahini, tofu, taco) are included because they are in English dictionaries and are used as ordinary English words. Diet-guilt and body words (Lean, Slim, Skinny, Cheat, Guilt and similar) were excluded before listing (§2.5 rule 5).

#### 4.8.1 Ingredients, herbs and produce

| # | Name | L/S | Idea behind it | D/S | PL | Screen result |
|---|---|---|---|---|---|---|
| 272 | Salsa | 5/2 | A lively mix: the recipe you love blended with what you need; also the dance, the rhythm of your week | S (in ES/IT/PT *salsa* = "sauce") | OK, identical | **Shortlisted, top 3** |
| 273 | Pesto | 5/2 | A few good things ground together: your recipe plus your numbers | S | OK, identical | **Shortlisted (not recommended):** "Pesto - Recipe App" on the Polish App Store |
| 274 | Pickle | 6/2 | Pickling is preparing ahead, like meal prep; the app gets you out of a pickle | S | OK ("PI-kel"; PL *pikle*) | **Shortlisted, alternate** |
| 275 | Caper | 5/2 | A small bud of big flavour; "a caper" is also a playful adventure | S | Misread: PL "KA-per", EN "KAY-per" | **Shortlisted (not recommended):** Instacart Caper AI grocery carts |
| 276 | Melon | 5/2 | Round, fresh, friendly | S | OK, identical | **Shortlisted (not recommended)** |
| 277 | Basil | 5/2 | A fresh herb | S | OK | Screened out (search): "Basil: Recipes & Meal Planner"; "Chef Basil" |
| 278 | Saffron | 7/2 | A precious spice | S | OK | Screened out (search): "Saffron: Your Digital Cookbook" |
| 279 | Sumac | 5/2 | A tangy spice | S | OK | Screened out (search): "Sumac Recipe Manager" |
| 280 | Fennel | 6/2 | Crisp, fresh vegetable | S | OK | Screened out (search): a "Fennel" recipe-import app; "Fennel: Invest your way" |
| 281 | Olive | 5/2 | Mediterranean staple | S | Silent final "e": PL "o-LI-ve" | Screened out (search): "Olive" food-scanner app |
| 282 | Pepper | 6/2 | A kick of flavour | S | OK | Screened out (search): "Pepper - Recipe Organizer"; Pepperplate |
| 283 | Chili | 5/2 | Heat and energy | S | "ch" | Screened out (search): "Chilli food" app |
| 284 | Tofu | 4/2 | Adapts to any flavour | S (one diet, C7) | OK | Screened out (search): "Tofu - Vegan Recipes" (macros) |
| 285 | Sesame | 6/3 | "Open sesame" | S | OK | Screened out (search): "Sesame: Healthy Food Scanner"; 3 syllables; an allergen |
| 286 | Lentil | 6/2 | Cheap, high-protein staple | S | OK | Screened out (search): "Lentil - Food Insights" |
| 287 | Radish | 6/2 | Crunchy, bright | S | Word little known in PL (*rzodkiewka*) | Screened out (search): Radish Health (telehealth, C5), Radish Fiction, Radish Kitchen |
| 288 | Mango | 5/2 | Sweet, sunny | S | OK | Screened out (search): "Mango Bites" and "Mango AI" calorie trackers |
| 289 | Lemon | 5/2 | Fresh, zesty | S | OK | Screened out (search): "Lemon: Nutrition Made Simple" (EU) |
| 290 | Peach | 5/1 | "A peach" = something great | S | "ea": PL "pe-ach" | Screened out (search): "Peach: AI Calorie Tracker" |
| 291 | Garlic | 6/2 | Every recipe starts with it | S | OK | Screened out (search): "Garlic Recipe Keeper & Planner" |
| 292 | Carrot | 6/2 | Carrot, not stick | S | OK | Screened out (search): Carrot AI, "Carrot: Calorie Counter & AI", Carroty, Purple Carrot |
| 293 | Clove | 5/1 | A small spice | S | Silent final "e" | Screened out (search): "Clove" AI meal planner and recipe app |
| 294 | Maple | 5/2 | Sweet, natural | S | "a" = "ey", silent "e" | Screened out (search): Maple family meal planner |
| 295 | Honey | 5/2 | Sweet, warm | S | "ey" | Screened out (search): Honeydew recipe app is near (§4.1); PayPal Honey (reviewer knowledge) |
| 296 | Oats | 4/1 | Breakfast staple | S | "oa" | Screened out (search): "Oatsy" nutrition app is near; C2 |
| 297 | Tahini | 6/3 | Sesame paste | S | OK | Screened out (judgment): 3 syllables; search Inconclusive |
| 298 | Ginger | 6/2 | Zing | S | Soft "g": Poles say a hard "g" | Screened out (judgment): C2; also sold as a remedy (C5); search Inconclusive |
| 299 | Cress | 5/1 | A sprinkle of green | S | Little known in PL | Screened out (judgment): weak for the wedge; search Inconclusive |
| 300 | Almond | 6/2 | Wholesome snack | S | Silent "l" | Screened out (judgment): C2; a tree-nut allergen, awkward for an allergy-aware app; search Inconclusive |
| 301 | Cocoa | 5/2 | Comfort | S | "oa" | Screened out (judgment): Cocoa is Apple's developer-framework name (C6); search Inconclusive |
| 302 | Cherry | 6/2 | "The cherry on top" | S | "ch" | Screened out (judgment): C2; the grouped search returned only "Peach" apps |
| 303 | Berry | 5/2 | Small, bright | S | OK | Screened out (judgment): weak and generic; search Inconclusive |
| 304 | Jam | 3/1 | Sweet; also a jam session | S | "j" read as "y" (PL *dżem*) | Screened out (judgment): C2; "traffic jam"; search Inconclusive |
| 305 | Truffle | 7/2 | Rare and special | S | OK | Screened out (search + judgment): "Truffle Blog" food app; luxury and fungus associations |
| 306 | Onion | 5/2 | Layers | S | "o" = "u" in EN | Screened out (judgment): The Onion (satire) and Tor ".onion" (reviewer knowledge); the grouped search returned only "Garlic" apps |
| 307 | Butter | 6/2 | Smooth | S | "u" | Screened out (judgment): weak; fat focus; grouped search Inconclusive |

#### 4.8.2 Dishes, breads and snacks

| # | Name | L/S | Idea behind it | D/S | PL | Screen result |
|---|---|---|---|---|---|---|
| 308 | Pretzel | 7/2 | A twist that holds together: the app twists your recipe until it fits your plan | S | OK ("PRET-zel"; PL *precel*) | **Shortlisted, top 3** |
| 309 | Donut | 5/2 | The food you'd feel guilty about elsewhere fits your plan here (PRD §1) | S | OK (PL *donat*) | **Shortlisted, top 3** |
| 310 | Nacho | 5/2 | "Nacho average meal plan"; a sharing plate | S | "ch": Poles read [x] ("NA-ho") | **Shortlisted (not recommended)** |
| 311 | Bagel | 5/2 | A round classic | S | Misread: PL "BA-gel", EN "BAY-gel" | **Shortlisted (not recommended)** |
| 312 | Tapas | 5/2 | Small plates, lots of variety: your week in portions | S/B (descriptive for food service in ES) | OK, identical | **Shortlisted (not recommended)** |
| 313 | Gravy | 5/2 | "It's all gravy" = all good; the extra that makes a meal | S | Misread: PL "GRA-vy", EN "GRAY-vee" | **Shortlisted (not recommended)** |
| 314 | Taco | 4/2 | Fold anything in | S | OK | Screened out (judgment): one cuisine, fast food (C7); Taco Bell (reviewer knowledge); search Inconclusive |
| 315 | Muffin | 6/2 | Homely bake | S | OK | Screened out (judgment): "muffin top" is a belly-fat term (C5); search Inconclusive |
| 316 | Dumpling | 8/2 | Everything wrapped in one | S | OK | Screened out (judgment): EN "dump" echo (C3); search Inconclusive |
| 317 | Noodle | 6/2 | "Use your noodle" | S | "oo" | Screened out (search): ekilu, formerly "Nooddle", a recipe and meal-plan app |
| 318 | Toast | 5/1 | A toast to good food | S | "oa" (PL *tost*) | Screened out (search): "Toast - Local Restaurants" (Toast Inc., restaurant platform); "you're toast" = doomed |
| 319 | Crumble | 7/2 | Comfort pudding | S | OK | Screened out (search): "Crumbs Meal Plans & Recipes" and "Crumb" are near |
| 320 | Crust | 5/1 | The good edge | S | OK | Screened out (judgment): weak food hint (pizza or bread only); search Inconclusive |
| 321 | Loaf | 4/1 | A loaf for the week | S | "oa" | Screened out (judgment): C2; EN "to loaf" = to laze about; search Inconclusive |
| 322 | Nugget | 6/2 | A small valuable piece | S | OK | Screened out (search): Nugget Markets (US grocer) publishes meal planning; "chicken nugget" |
| 323 | Brunch | 6/1 | Relaxed weekend meal | B | OK (PL *brancz*) | Screened out (search + judgment): "Brunch Bites" recipe app; names one meal (C1, C7) |
| 324 | Snack | 5/1 | Small bite | D | OK | Screened out (judgment): descriptive (C1) |
| 325 | Wedge | 5/1 | A piece of the whole | S | "dg" | Screened out (judgment): weak food hint; grouped search Inconclusive |
| 326 | Slice | 5/1 | Your slice | B | Silent "e" | Screened out (judgment): Slice pizza-ordering app (reviewer knowledge); grouped search Inconclusive |

#### 4.8.3 Utensils and kitchen objects

| # | Name | L/S | Idea behind it | D/S | PL | Screen result |
|---|---|---|---|---|---|---|
| 327 | Kettle | 6/2 | The kitchen's heartbeat; a nod to kettlebells | S | Word little known (PL *czajnik*); reads "KET-tle" | **Shortlisted (only if the top 5 fail)** |
| 328 | Ladle | 5/2 | Serves one portion (PO's example) | S | Silent "e"; not known to the wedge (PL *chochla*) | Screened out (search): four "Ladle" recipe and meal-planner apps (§3.6) |
| 329 | Spoon | 5/1 | Everyday eating | S | "oo" | Screened out (search): "Spoon: Recipe & Meal Planner"; "Spoon: Smart Calorie Tracker"; spoonacular |
| 330 | Fork | 4/1 | Everyday eating | S | OK | Screened out (search): "Forks Meal Planner" (Forks Over Knives), "Forked AI", Forkful |
| 331 | Spatula | 7/3 | Flip it | S | OK | Screened out (search): "Spatula" recipe box; 3 syllables |
| 332 | Oven | 4/2 | Warm home cooking | S | OK | Screened out (search): BigOven recipes and meal planner |
| 333 | Wok | 3/1 | Fast, hot, simple | S | "w" (PL [v]) | Screened out (search + judgment): "WokTheWeek" meal planner; C2; one cuisine |
| 334 | Jar | 3/1 | Meal prep in jars | S | "j" | Screened out (search): "MealJar" meal planner; C2 |
| 335 | Apron | 5/2 | Ready to cook | S | "A-pron" vs "AY-pron" | Screened out (search): "Apron: Recipes & Grocery Lists"; Blue Apron meal kits |
| 336 | Grill | 5/1 | Direct heat | S/B | OK | Screened out (search + judgment): "Grill'd" restaurant app; generic |
| 337 | Tray | 4/1 | Traybake meal prep | B | "ay" | Screened out (judgment): C2; search Inconclusive |
| 338 | Pan | 3/1 | One-pan meals | S | **PL *pan* = Mr/sir** | Screened out (judgment): C3 in PL |
| 339 | Pot | 3/1 | One-pot meals | S | **PL *pot* = sweat**; EN slang for cannabis | Screened out (judgment): C3, C5 |
| 340 | Mortar | 6/2 | Grinding flavours together | S | OK | Screened out (judgment): the building-material sense dominates; search Inconclusive |
| 341 | Tongs | 5/1 | Grab what you want | S | OK | Screened out (judgment): weak and flat; search Inconclusive |
| 342 | Grater | 6/2 | Fine detail | S | "a" = "ey"; sounds like "greater" | Screened out (judgment): C2; search Inconclusive |
| 343 | Skewer | 6/2 | Everything lined up | S | "ew" | Screened out (judgment): C2; "to skewer" = to criticise harshly |
| 344 | Galley | 6/2 | A compact working kitchen | S | OK | Screened out (search): Galley Solutions, culinary resource-planning SaaS (class 42) |

#### 4.8.4 Cooking actions and tastes

| # | Name | L/S | Idea behind it | D/S | PL | Screen result |
|---|---|---|---|---|---|---|
| 345 | Stir | 4/1 | Mix things up | S | OK | Screened out (search): "Stir - Your Recipe Assistant"; "Stir & Store" |
| 346 | Sear | 4/1 | Lock in flavour | S | "ea" | Screened out (judgment): C2; search Inconclusive |
| 347 | Braise | 6/1 | Slow, patient cooking | S | "ai" + silent "e" | Screened out (judgment): C2; search Inconclusive |
| 348 | Roast | 5/1 | Sunday roast | S | "oa" | Screened out (judgment): C2; "a roast" = mockery; search Inconclusive |
| 349 | Glaze | 5/1 | The finishing touch | S | Silent "e" | Screened out (search + judgment): "Deglaze" recipe app is near; C2 |
| 350 | Sizzle | 6/2 | Excitement in the pan | S | "zz" | Screened out (search): two "Sizzle" recipe and meal-planner apps |
| 351 | Drizzle | 7/2 | A light finishing touch | S | OK | Screened out (search): "Drizzle Me Skinny" Weight Watchers recipe app ("skinny", C5 by association) |
| 352 | Crisp | 5/1 | Fresh and sharp | S | OK | Screened out (search): "Crisp supermarkt" (NL online grocer); "CRISP & GREEN" healthy-restaurant app; Crisp chat SaaS |
| 353 | Crunch | 6/1 | "Crunch the numbers" | S | "u" | Screened out (search): "Crunch: Voice & AI Calorie Log"; Crunch Fitness |
| 354 | Munch | 5/1 | Happy eating | S | "u" | Screened out (search): Munchi, Munched, MUNCH, munch, Munch Metrics |
| 355 | Nibble | 6/2 | Small bites | S | OK | Screened out (search): Nibble Apps (the MealPrepPro developer), "Nibble AI - Calorie Tracker", Nibbly |
| 356 | Savor | 5/2 | Enjoy every bite | S | "a" = "ey" | Screened out (search): Savor meal planner (§3.6), Savour, savori |
| 357 | Yum | 3/1 | Pure delight | S | "u" | Screened out (search): "Yum AI", "Yum: Easy & Tasty Recipes", Wholesome Yum, Yummly; Yum! Brands (reviewer knowledge) |
| 358 | Feast | 5/1 | Abundance | S | "ea" | Screened out (search): "Feast: Nutrition Coach" |

#### 4.8.5 Portions, pantry and meal words

| # | Name | L/S | Idea behind it | D/S | PL | Screen result |
|---|---|---|---|---|---|---|
| 359 | Handful | 7/2 | Portions measured by hand; plans that feel manageable | B (a portion word) | OK ("HAND-ful") | **Shortlisted, alternate** |
| 360 | Pinch | 5/1 | A pinch of this (PO's example) | B | OK | Screened out (search): "Pinch It! Recipe Box"; "Pinch: Follow. Cook. Share." |
| 361 | Crumb | 5/1 | Small piece (PO's example) | S | Silent "b" | Screened out (search): "Crumb: Recipe & Dinner Ideas"; "Crumbs Meal Plans & Recipes" |
| 362 | Scoop | 5/1 | A portion; "the scoop" = the inside story | B | "oo" | Screened out (search): "Scoop: Healthy Eating Out" (AI nutrition coach) |
| 363 | Dollop | 6/2 | A generous spoonful | B | OK | Screened out (search): "Dollop — Dinner, Decided" recipe discovery |
| 364 | Spoonful | 8/2 | One portion (PO's example) | B | "oo" | Screened out (search): "Spoonful: Diet & Food Scanner" |
| 365 | Forkful | 7/2 | One bite | B | OK | Screened out (search): "Forkful: Recipe Meal Planner" |
| 366 | Mouthful | 8/2 | A bite | B | "th" | Screened out (judgment): C2; search Inconclusive |
| 367 | Plateful | 8/2 | A full plate | B | Silent "e" | Screened out (search): "PlateFul" menu software (senior living); "Plateful Nutrition" |
| 368 | Tidbit | 6/2 | A tasty morsel | S | OK | Screened out (search): "Tidbit" nutrition and GLP-1 tracker (C5 neighbour) |
| 369 | Smidge | 6/1 | A tiny amount | B | "dge"; unknown to the wedge | Screened out (judgment): C2; search Inconclusive |
| 370 | Helping | 7/2 | "A second helping" | B | OK | Screened out (judgment): reads as the verb "helping"; search Inconclusive |
| 371 | Pantry | 6/2 | Your stocked kitchen (PO's example) | S | OK | Screened out (search): "Pantry: macros from receipts" |
| 372 | Supper | 6/2 | Evening meal | B | "u" | Screened out (search): "Supper: Recipes & Meal Planner"; Supperhero |
| 373 | Picnic | 6/2 | Food made to share | S | OK (PL *piknik*) | Screened out (search): Picnic online supermarket with recipes and a meal planner |
| 374 | Harvest | 7/2 | Fresh from the field | S | OK | Screened out (search): "Harvest — Meal Planning App"; Daily Harvest |
| 375 | Basket | 6/2 | Your shopping, sorted | S | OK | Screened out (judgment): generic shopping term; grouped search returned Harvest apps |
| 376 | Batch | 5/1 | Batch cooking | B/D | "tch" | Screened out (judgment): describes meal prep (C1); search Inconclusive |
| 377 | Lunchbox | 8/2 | Meal prep to go | B | OK | Screened out (search + judgment): LaLa Lunchbox, Little Lunches; describes meal prep (C1) |
| 378 | Bistro | 6/2 | Casual good food | S | OK | Screened out (search): "Bistro: Food in minutes" (Blinkit, IN), Bistro.sk; bistroMD diet-meal delivery (reviewer knowledge) |
| 379 | Herb | 4/1 | Fresh flavour | S | "h" silent in US English | Screened out (search): "Herbi: Meal Planner + Recipes" |
| 380 | Sprout | 6/1 | Growth | S | "ou" | Screened out (search): "Sprout AI - Healthy Recipes", Sproutly, Sprout Cooking |
| 381 | Spice | 5/1 | Variety | S | "i" = "ai" + silent "e" | Screened out (judgment): C2; "Spice" is a street name for synthetic cannabis (C5) |
| 382 | Kernel | 6/2 | The core | S | OK | Screened out (judgment): reads as a computing term; weak food hint; search Inconclusive |
| 383 | Mealbox | 7/2 | Meal prep box | D | "ea" | Screened out (judgment): descriptive (C1); not searched |

#### 4.8.6 Screened out on spelling, meaning or known brands alone (judgment; not searched)

| # | Name | L/S | Why screened out |
|---|---|---|---|
| 384 | Thyme | 5/1 | "th" and a silent "h" (C2) |
| 385 | Knead | 5/1 | Silent "k"; sounds like "need" (C2) |
| 386 | Dough | 5/1 | "gh"; Poles read "doug-h" (C2); "dough" = money slang |
| 387 | Broth | 5/1 | "th" (C2) |
| 388 | Yolk | 4/1 | Silent "l" (C2) |
| 389 | Chive | 5/1 | "ch" read as [x] in PL (C2) |
| 390 | Sieve | 5/1 | "ie" and "ve" (C2) |
| 391 | Tasty | 5/2 | BuzzFeed's "Tasty" recipe app (reviewer knowledge) |
| 392 | Lime | 4/1 | Lime scooters (reviewer knowledge) |
| 393 | Mint | 4/1 | Intuit's former "Mint" finance app (reviewer knowledge); "mint" = money |
| 394 | Sage | 4/1 | Sage Group accounting software (reviewer knowledge) |
| 395 | Fudge | 5/1 | "To fudge the numbers" = to falsify figures (C3), bad for an app that does the maths |
| 396 | Cracker | 7/2 | A US racial slur (C3) |
| 397 | Cumin | 5/2 | EN "cum" echo (C3) |
| 398 | Anise | 5/2 | EN "anus" echo (C3) |
| 399 | Curry | 5/2 | PL *kury* (hens); one cuisine (C7) |
| 400 | Sauce | 5/1 | "au" misread by Poles (C2); "saucy" = cheeky |

Result: **13 names shortlisted** (§6.8): Salsa, Pretzel, Donut (top 3), Pickle, Handful (alternates), Kettle, Tapas, Nacho, Melon, Bagel, Pesto, Caper, Gravy. All are 5–7 letters and 2 syllables. The last eight are kept so the PO can see why obvious catchy food words were not recommended (§6.8.2).

---

## 5. Research findings and source links (evidence log)

Sessions 1 and 2 are dated **2026-09-24**; sessions 3 and 4 are dated **2026-09-25**.

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

#### Session 3 retry (2026-09-25)

At the start of session 3, each official source got **one plain request**, as the task asked. `curl` was run once for every source (HTTP status only, 20-second timeout). WebFetch was also tried once on the .com RDAP, iTunes, Google Play and TMview URLs. The test name was `zumo`.

| Source (official) | Request | Tool | Result |
|---|---|---|---|
| `rdap.verisign.com` (.com RDAP) | `/com/v1/domain/zumo.com` | curl; WebFetch | curl: `curl: (56) CONNECT tunnel failed, response 403`. WebFetch: `EGRESS_BLOCKED … Access to rdap.verisign.com is blocked by the network egress proxy.` |
| `pubapi.registry.google` (.app RDAP) | `/rdap/domain/zumo.app` | curl | `CONNECT tunnel failed, response 403` |
| `data.iana.org` (RDAP bootstrap) | `/rdap/dns.json` | curl | `CONNECT tunnel failed, response 403`, so the .pl and .io RDAP servers still can't be looked up |
| `itunes.apple.com` (iTunes Search API) | `/search?term=zumo&entity=software&country=pl` | curl; WebFetch | curl: `CONNECT tunnel failed, response 403`. WebFetch: `EGRESS_BLOCKED … Access to itunes.apple.com is blocked` |
| `play.google.com` | `/store/search?q=zumo&c=apps&gl=PL` | curl; WebFetch | curl: `CONNECT tunnel failed, response 403`. WebFetch: `EGRESS_BLOCKED … Access to play.google.com is blocked` |
| `www.tmdn.org` (TMview) | `/tmview/` | curl; WebFetch | curl: `CONNECT tunnel failed, response 403`. WebFetch: `EGRESS_BLOCKED … Access to www.tmdn.org is blocked` |
| `euipo.europa.eu/eSearch/`, `ewyszukiwarka.pue.uprp.gov.pl`, `branddb.wipo.int`, `tmsearch.uspto.gov`, `trademarks.ipo.gov.uk` | landing page | curl | `CONNECT tunnel failed, response 403` on each |
| **WebSearch** | — | WebSearch | **Worked.** Used for every session-3 screen and per-name check (§5.4, §6.7.3). Domain-filtered searches on apps.apple.com, play.google.com, instagram.com and tiktok.com also worked. |

**Consequence:** unchanged for the third session running. Every store, domain, trademark and handle check for every session-3 name is **Pending**. No workaround was attempted.

#### Session 4 retry (2026-09-25)

At the start of session 4, each official source got **one plain request**, as the task asked. `curl` was run once for every source (HTTP status only, 20-second timeout). WebFetch was also tried once on the .com RDAP, iTunes, Google Play and TMview URLs. The test name was `ladle`.

| Source (official) | Request | Tool | Result |
|---|---|---|---|
| `rdap.verisign.com` (.com RDAP) | `/com/v1/domain/ladle.com` | curl; WebFetch | curl: `curl: (56) CONNECT tunnel failed, response 403`. WebFetch: `EGRESS_BLOCKED … Access to rdap.verisign.com is blocked by the network egress proxy.` |
| `pubapi.registry.google` (.app RDAP) | `/rdap/domain/ladle.app` | curl | `curl: (56) CONNECT tunnel failed, response 403` |
| `data.iana.org` (RDAP bootstrap) | `/rdap/dns.json` | curl | `CONNECT tunnel failed, response 403`, so the .pl and .io RDAP servers still can't be looked up |
| `itunes.apple.com` (iTunes Search API) | `/search?term=ladle&entity=software&country=pl` | curl; WebFetch | curl: `CONNECT tunnel failed, response 403`. WebFetch: `EGRESS_BLOCKED … Access to itunes.apple.com is blocked by the network egress proxy.` |
| `play.google.com` | `/store/search?q=ladle&c=apps&gl=PL` | curl; WebFetch | curl: `CONNECT tunnel failed, response 403`. WebFetch: `EGRESS_BLOCKED … Access to play.google.com is blocked by the network egress proxy.` |
| `www.tmdn.org` (TMview) | `/tmview/` | curl; WebFetch | curl: `CONNECT tunnel failed, response 403`. WebFetch: `EGRESS_BLOCKED … Access to www.tmdn.org is blocked by the network egress proxy.` |
| `euipo.europa.eu/eSearch/`, `ewyszukiwarka.pue.uprp.gov.pl`, `branddb.wipo.int`, `tmsearch.uspto.gov`, `trademarks.ipo.gov.uk` | landing page | curl | `CONNECT tunnel failed, response 403` on each |
| **WebSearch** | — | WebSearch | **Worked.** Used for every session-4 screen and per-name check (§5.5, §6.8.3). Domain-filtered searches on apps.apple.com, play.google.com, instagram.com, tiktok.com and on third-party trademark mirrors (trademarkia.com, trademarks.justia.com, uspto.report) also worked. |

**Consequence:** unchanged for the fourth session running. Every store, domain, trademark and handle check for every session-4 name is **Pending**. Trademark findings in §6.8.3 come from third-party mirror sites seen through the search engine; they are indications only (Risk or Inconclusive), not registry results. No workaround was attempted.

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

### 5.4 Session 3 screening evidence (search engine; status at most Risk or Inconclusive)

All entries are dated **2026-09-25**. Quoted text is the search result's title, or its snippet or summary, as returned. None of the linked pages could be opened (egress-blocked). Unless stated, the query was `"<Name>" app food OR meal OR nutrition OR recipes` (or the close variant shown). The per-name evidence for the shortlist is in §6.7.3.

| Name | Query (variant) | Status | What the search showed | Links |
|---|---|---|---|---|
| Nomo | standard | Risk (screened out) | No Nomo app; "noms - AI recipe & meal plan"; "NomNom: Meal Planner & Recipes" (summary: "set your budget"); "Nom Nom: Organize Recipes Plan" | [noms](https://apps.apple.com/us/app/noms-ai-recipe-meal-plan/id6748933312), [NomNom](https://apps.apple.com/us/app/nomnom-meal-planner-recipes/id6788049718) |
| Bito | standard | Risk (screened out) | No Bito app; "Bite AI: Meal Calorie Tracker"; "BiteRite \| Calorie controlled, meal plan app"; "BiteTracker: Plan & Track Food" | [Bite AI](https://apps.apple.com/us/app/bite-ai-calorie-counter/id6736922373), [biterite.app](https://biterite.app/) |
| Kibo | standard | Risk (screened out) | "Collections – Kibo Foods" (complete meal kit); "5 Tips for Sustainable Meal Planning and Prep" on kibofoods.us | [kibofoods.us](https://kibofoods.us/products/complete-meal-kit) |
| Bimo | standard | Risk (screened out) | Bimo biscuits in Fitia's Spanish database; "Bimi - Eat Better - App Store" | [Bimi](https://apps.apple.com/us/app/bimi-eat-better/id6756016601) |
| Tuki | standard | Risk (screened out) | "Tucki: Family Meal Planner - App Store"; "Tuki - Apps on Google Play" (a residents' super-app with food delivery) | [Tucki](https://apps.apple.com/us/app/tucki/id6503348465), [Tuki](https://play.google.com/store/apps/details?id=asia.tuki.twa&hl=en_US) |
| Zesto | `"Zesto" app OR brand food OR meal OR recipes` | Risk (screened out) | "Cooking Assistant AI - Zesto App - App Store"; "Zest: Meal Planner & Recipes"; "Zesto \| Buddy" | [Zesto](https://apps.apple.com/us/app/cooking-assistant-ai-zesto/id6584520256), [Zest](https://apps.apple.com/gb/app/zest-meal-planner-recipes/id1595938390) |
| Pepo | `"Pepo" app OR brand food OR meal OR nutrition` | Risk (screened out) | "PEP: Diet - Healthy meal plan" and related PEP apps; "Peppo - Apps on Google Play" (Italian food ordering) | [PEP](https://apps.apple.com/us/app/pep-diet-healthy-meal-plan/id1530408366), [Peppo](https://play.google.com/store/apps/details?id=com.dishop.peppo&hl=en_US) |
| Tasto | standard | Risk (screened out) | "Tasto: Recipe Manager - App Store"; "Tasto: From Social to Kitchen" | [App Store](https://apps.apple.com/us/app/tasto-recipe-manager/id6760462265), [tastoapp.com](https://tastoapp.com/) |
| Pasto | `"Pasto" app meal planner OR nutrition OR recipes` | Risk (screened out) | "Plento Pasto: Meal Planner - App Store"; "Plento Pasto — Plenty + meal, for the everyday family" | [App Store](https://apps.apple.com/us/app/plento-pasto-meal-planner/id6773336713), [plentopasto.com](https://plentopasto.com/) |
| Mako | standard | Risk (screened out) | "MAKO - Apps on Google Play" (bakery); "Makros: Meal Plan & Grocery" | [MAKO](https://play.google.com/store/apps/details?id=com.mako.app), [Makros](https://play.google.com/store/apps/details?id=com.ivandiettracker.makros.makros_app&hl=en_US) |
| Maku | `"Maku" app food OR meal OR nutrition OR macros` | Risk (screened out) | "Food Macro Calculator: Makro - App Store"; "Makros: Meal Plan & Grocery" | [Makro](https://apps.apple.com/us/app/food-macro-calculator-makro/id6477851684) |
| Bento | `"Bento" app meal prep OR meal planner OR nutrition` | Risk (screened out) | "Bento Box: Meal plans now easy App - App Store"; "Bento - Apps on Google Play" (meal planner); "Bento - Meal Planner, AI Recipe Generator, Calorie Tracker" | [App Store](https://apps.apple.com/us/app/bento-box-meal-plans-now-easy/id6758401088), [Play](https://play.google.com/store/apps/details?id=io.quartz.app&hl=en) |
| Momo | `"Momo" app meal planner OR nutrition OR recipes` | Risk (screened out) | "Momo — Eat better. Feel your best." (AI meal-photo nutrition) | [trymomo.app](https://trymomo.app/) |
| Plum | `"Plum" app meal planner OR nutrition OR recipes` | Risk (screened out) | "Plum Recipe Saver on the App Store"; "Plum: Recipe Keeper"; "Plum Recipes - A delightful, free recipe organizer" | [App Store](https://apps.apple.com/us/app/plum-recipe-saver/id6496861616), [plumrecipes.app](https://www.plumrecipes.app/) |
| Fig | `"Fig" app food OR nutrition OR meal planner` | Risk (screened out) | "Fig: Food Scanner & Recipes App - App Store" | [App Store](https://apps.apple.com/us/app/fig-food-scanner-recipes/id1564434726) |
| Dill | `"Dill" app meal planner OR recipes OR nutrition`; store-filtered `Dill app` | Inconclusive, then Risk (screened out) | Category query: no Dill app. Store-filtered: "Dill - App Store" (campus food ordering); "dill Till App"; "Dill Kitchen on the App Store"; "What's The Dill" | [Dill](https://apps.apple.com/us/app/dill/id1462397948), [dill Till](https://apps.apple.com/us/app/dill-till/id6461347364), [Dill Kitchen](https://apps.apple.com/us/app/dill-kitchen/id1624644757) |
| Zing | `"Zing" app meal planner OR nutrition OR recipes OR food` | Risk (screened out) | "Zing Wellbeing - App Store - Apple" (recipes and meal plans); "Nutrition Guide – Zing Coach Help Center" | [App Store](https://apps.apple.com/us/app/zing-wellbeing/id6743520200) |
| Nori | `"Nori" app meal planner OR nutrition OR recipes` | Risk (screened out) | "Nori - Family AI App - App Store"; "Nori AI: Your Health Advisor"; "Nori - Nutrition Tracker" (Microsoft Store) | [App Store](https://apps.apple.com/us/app/nori-family-ai/id6753757891), [heynori.com](https://heynori.com/ai-powered-meal-planning) |
| Miso | `"Miso" app meal planner OR nutrition OR recipes` | Risk (screened out) | "Miso - Recipe Keeper"; "Miso Cook: Meal Planner"; "Miso \| Meal Planning, Pantry, Groceries, and Nutrition" | [Miso](https://apps.apple.com/us/app/miso-recipe-keeper/id6756516262), [Miso Cook](https://apps.apple.com/us/app/miso-cook-meal-planner/id6757978247), [misoapp.ca](https://misoapp.ca/) |
| Mola | standard | Risk (screened out) | "Mola Foods - App on Amazon Appstore" (vegan sauces); "Mola - Food Menu" (restaurant) | [Amazon](https://www.amazon.com/Mola-Foods-Inc/dp/B07FXQ2GZS) |
| Remo | standard | Risk (screened out) | No Remo app; "Remi: Recipes & Cooking"; "Remy - Recipes & Meal Planner"; ReciMe | [Remi](https://apps.apple.com/us/app/remi-recipes-cooking/id6504444134), [Remy](https://apps.apple.com/us/app/remy-recipes-meal-planner/id6738160281) |
| Kombo | standard | Risk (screened out) | "Your food. Your day. - Kombo" (meal boxes; summary: calorie values and macronutrient proportions per box); "Kombo App - App Store" (food ordering) | [kombomeals.rs](https://kombomeals.rs/en/home/), [App Store](https://apps.apple.com/us/app/kombo/id1553081211) |
| Tembo | standard; `"Gobo" OR "Zubo" OR "Tembo" app OR company software` | Inconclusive (food), Risk (software; screened out) | No Tembo food app; "New Version Of Tembo App Is Here!" (Tembo Money); "Tembo \| LinkedIn" (Postgres company); "Tembo Connect - Apps on Google Play" | [Tembo Money](https://www.tembomoney.com/learn/introducing-the-new-version-of-tembo-app), [Tembo Connect](https://play.google.com/store/apps/details?id=nl.speakap.tembo&hl=en_US) |
| Nubo / Mubo | `"Mubo" OR "Nubo" app OR brand food OR nutrition` | Risk (Nubo, screened out); Inconclusive (Mubo) | "Nubo - Body and Nutrition - App Store"; "NUBO WEIGHT LOSS \| NuBo Wellness"; nothing for Mubo | [App Store](https://apps.apple.com/vn/app/nubo-body-and-nutrition/id1492780477), [nubowellness.com](https://www.nubowellness.com/) |
| Pomo | standard | Risk (screened out) | "Pomelo - Nutrition Meal Plans - App Store"; "POMO Network" (restaurant rewards) | [Pomelo](https://apps.apple.com/us/app/pomelo-nutrition-meal-plans/id6763051623), [pomo.network](https://pomo.network/) |
| Tamo | `"Tamo" app OR brand food OR meal OR nutrition` | Risk (screened out) | "Tomo - Diet & Calories App - App Store"; TAMO Bistro + Bar | [Tomo](https://apps.apple.com/us/app/tomo-diet-calories/id6793031588) |
| Dabo | `"Dabo" app OR brand food OR meal OR nutrition` | Risk (screened out) | "Just Dabao: Food Saving App - Apps on Google Play"; "Dabo kolo" (Wikipedia) | [Play](https://play.google.com/store/apps/details?id=com.dabo.food_delivery_app) |
| Zumi | `"Zumi" app OR brand food OR meal OR nutrition` | Risk (screened out) | "ZUMI FOODS \| LinkedIn" (milkshakes); "zumi - pet care - Apps on Google Play" (pet weight and nutrition) | [Facebook](https://www.facebook.com/zumifoods/), [Play](https://play.google.com/store/apps/details?id=com.zumi.app.zumi_app&hl=en_US) |
| Lulo | `"Lulo" app OR brand food OR meal OR nutrition` | Risk (screened out) | "Lulo" (a WIC food-benefits app, New York) | [hellolulo.com](https://www.hellolulo.com/) |
| Zuzu | `"Zuzu" app OR brand food OR meal OR nutrition` | Risk (screened out) | "ZuZu Handmade Mexican Food - Apps on Google Play"; "ZuZu Foods - Home" | [Play](https://play.google.com/store/apps/details?id=com.chownow.zuzuhandmademexicanfood&hl=en), [zuzu.food](https://zuzu.food/) |
| Umai | standard | Risk (screened out) | "Umai: Recipes with a spark - Apps on Google Play" | [Play](https://play.google.com/store/apps/details?id=com.ndokholyan.umai) |
| Tamtam | `"Tamtam" OR "Tam Tam" app food…` | Risk (screened out) | "TamTam (app)" (Wikipedia; a messenger); "TamiMeal - App Store" | [Wikipedia](https://en.wikipedia.org/wiki/TamTam_(app)), [TamiMeal](https://apps.apple.com/us/app/tamimeal/id6745157267) |
| Kanpai | `"Kanpai" app OR brand food OR meal OR nutrition` | Risk (screened out) | "Kanpai Foodz \| Freeze Dried Candy Store"; "Kanpai - Apps on Google Play" (ordering) | [kanpaifoods.com](https://kanpaifoods.com/), [Play](https://play.google.com/store/apps/details?id=com.owner.kanpai&hl=en) |
| Mizu | standard | Risk (screened out; C5) | "Mizu - Your CKD companion - App Store - Apple" (kidney-disease food diary) | [App Store](https://apps.apple.com/us/app/mizu-your-ckd-companion/id1536328825) |
| Zelo | `"Zelo" app OR brand food OR meal OR nutrition` | Risk (screened out) | "Zelo Delivery - Apps on Google Play" (grocery quick commerce); "ZOE: Personalized Nutrition - App Store" | [Zelo](https://play.google.com/store/apps/details?id=com.abs.zelo&hl=en_US), [ZOE](https://apps.apple.com/gb/app/zoe-personalized-nutrition/id1471632228) |
| Rumbo / Tombo | `"Rumbo" OR "Tombo" app food OR meal planner OR nutrition`; store-filtered `Rumbo app` | Inconclusive (category), then Risk (Rumbo, screened out) | Category query: nothing for either. Store-filtered: "Rumbo Fitness - App Store - Apple" (calorie counting on Apple Watch); "Rumbo.es - vuelos baratos" | [Rumbo Fitness](https://apps.apple.com/us/app/rumbo-fitness/id6475088608), [Rumbo.es](https://apps.apple.com/us/app/rumbo-es-vuelos-baratos/id535128140) |
| Kudu | standard | Risk (screened out) | "Kudu Restaurant - Saudi Arabia - Apps on Google Play" | [Play](https://play.google.com/store/apps/details?id=com.kudu.androidapp&hl=en) |
| Temi | standard | Risk (screened out) | No Temi app; "Tami Meal - The meal planner for what's next"; "TamiTales: Weekly Meal Plan" | [tami-meal.com](https://tami-meal.com/), [Play](https://play.google.com/store/apps/details?id=com.tamimeal&hl=en_US) |
| Posto | `"Posto" app food OR meal OR recipes OR nutrition` | Inconclusive (screened out on judgment) | No Posto app; "Posto Nutrition" (poppy seeds, Bengali cooking); "Potto: Meal Planner & Recipes" | [SnapCalorie](https://www.snapcalorie.com/nutrition/posto_nutrition.html) |
| Gulp | standard | Risk (screened out) | "Gulp Note - Meal/Dining Diary – Apps bei Google Play" | [Play](https://play.google.com/store/apps/details?id=com.onnz.app.android.gulpnote&hl=en_US) |
| Nibs | standard | Risk (screened out) | "Recipe Manager - Nibbly - App Store"; "Meal Scanner Fun: Nibbly" | [App Store](https://apps.apple.com/us/app/recipe-manager-nibbly/id6747835183) |
| Miam | `"Miam" app food OR meal OR recipes OR nutrition` | Risk (screened out) | "Miam - Apps on Google Play" (recipes, weekly planning); "MiamPlan : Meal Plan & Recipe"; "MiaM, the complete breakfast" (nutrition bars) | [Play](https://play.google.com/store/apps/details?id=cloud.miam&hl=en), [miam-nutri.com](https://www.miam-nutri.com/en-US) |
| Tenko / Zanko | `"Tenko" OR "Zanko" app food OR meal OR nutrition` | Inconclusive (screened out on judgment) | "Order Tenko Japan - Cary" (restaurant); "Zankou Chicken" | [Uber Eats](https://www.ubereats.com/store/tenko-japan-cary/_OsyD1_SWM6R36PKIjahBg) |
| Mozo | `"Mozo" app OR brand food OR kitchen OR meal` | Risk (screened out) | "Mozo · The order-taking app for restaurants"; "Mozo, The New Generation Ordering & Payments Infrastructure" | [buho.la](https://buho.la/productos/mozo), [trymozo.com](https://www.trymozo.com/) |
| Tosto | `"Tosto" app OR brand food OR meal OR recipes` | Risk (screened out) | No Tosto app; "Tasto: Recipe Manager" returned first | — |
| Bimbam / Pompom | `"Bimbam" OR "Pompom" app food OR meal OR recipes` | Inconclusive (screened out on judgment) | Only bibimbap recipes and "Bibimbox" | — |
| Deko / Kazu | `"Deko" OR "Kazu" app food OR meal planner OR nutrition` | Inconclusive | No app named Deko or Kazu in the category results | — |
| Numo | standard | Risk (screened out) | "Numo: Contador de calorias - Apps on Google Play"; "Numo World App - App Store" (nutritious meal delivery) | [Play](https://play.google.com/store/apps/details?id=com.astertechltda.numo), [App Store](https://apps.apple.com/in/app/numo-world/id6447801011) |
| Lumo | standard | Risk (screened out) | "Lumo - AI Chef App - App Store"; "Lumo - Know What You Buy"; "Lumo - Nutrition care that keeps moving between visits" | [App Store](https://apps.apple.com/ca/app/lumo-ai-chef/id6746675356), [lumomeals.com](https://lumomeals.com/) |
| Morso | `"Morso" app OR brand food OR meal OR recipes` | Risk (screened out) | "Morso - Visual food journal App - App Store"; "Morso - App Store - Apple" (AI recipe creator, per summary); "Morso Burger" | [Journal](https://apps.apple.com/sg/app/morso-visual-food-journal/id6758254422), [Morso](https://apps.apple.com/de/app/morso/id6774290724?l=en-GB) |
| Bibo / Pingo | `"Bibo" OR "Pingo" app food OR meal OR nutrition` | Risk (screened out) | "BIBO - Apps on Google Play" (restaurant ordering); "Pingo - Food & Drink App" (restaurant discovery) | [BIBO](https://play.google.com/store/apps/details?id=mcom.com.mcom.bibo&hl=en), [Pingo](https://mwm.ai/apps/pingo/6446988156) |
| Rumi / Kibu | `"Rumi" OR "Kibu" app meal planner OR nutrition OR recipes` | Inconclusive | Only Remy, ReciMe and generic planners | — |
| Dango | `"Dango" app food OR meal planner OR nutrition OR recipes` | Risk (screened out) | "Dango : Food Delivery & More - Apps on Google Play" | [Play](https://play.google.com/store/apps/details?id=com.dango.user.app&hl=en_US) |
| Mirin / Kanzo | `"Mirin" OR "Kanzo" app meal planner OR nutrition OR recipes` | Inconclusive (screened out on judgment) | Mirin recipes; "Miri AI" nutrition companion | [Miri AI](https://apps.apple.com/mo/app/miri-ai/id6478316446) |
| Mixo | standard | Risk (screened out) | "Mixo, a Video-First Social Media Platform Built for Food Content, Launches in the App Store" | [GlobeNewswire](https://www.globenewswire.com/news-release/2022/06/01/2454219/0/en/Mixo-a-Video-First-Social-Media-Platform-Built-for-Food-Content-Launches-in-the-App-Store.html) |
| Paku | standard | Risk (screened out) | "Paku: AI Calorie Counter Pet - App Store - Apple"; same on Google Play | [App Store](https://apps.apple.com/us/app/paku-ai-calorie-counter-pet/id6752853273) |
| Happa | `"Happa" app OR brand food OR meal OR nutrition` | Risk (screened out) | "About Us \| Happa" (organic baby food, Mumbai); "Happa - App Store - Apple" | [happafoods.com](https://happafoods.com/pages/about-us), [App Store](https://apps.apple.com/us/app/happa/id6495164638) |
| Mums | `"Mums" app food OR meal OR recipes OR nutrition` | Risk (screened out) | "Healthy Mummy App - App Store" and other apps for mothers | [App Store](https://apps.apple.com/au/app/healthy-mummy/id1411902609) |
| Nomba / Zembo | `"Nomba" OR "Zembo" app OR brand food OR nutrition`; `"nomba.com" OR …` | Risk (both screened out) | "Circle Diet For Life - Apps on Google Play" (developer id com.zembo); "Nomba \| Business Banking & Payments"; "Nomba Support (@nomba) / X" | [Circle Diet](https://play.google.com/store/apps/details?id=com.zembo.cdfl), [nomba.com](https://nomba.com/) |
| Lumbo / Dembo | `"Lumbo" OR "Dembo" app OR brand food OR meal` | Inconclusive (screened out on judgment) | Nothing for either; "Bumbo Foods" recipe app; "Slimbo" meal plans | [Slimbo](https://slimbo.app/en/) |
| Zubo, Kazu, Dozo, Nimbo, Gobo, Bibim, Zumo, Kumo, Panko, Gumbo, Mogu, Pappa | see §6.7.3 | — | Shortlisted; full per-name evidence in §6.7.3 | — |

### 5.5 Session 4 screening evidence (search engine; status at most Risk or Inconclusive)

All entries are dated **2026-09-25**. Quoted text is the search result's title, or its snippet or summary, as returned. None of the linked pages could be opened (egress-blocked). Unless stated, the query was `"<Name>" app recipes OR "meal planner" OR nutrition` (or a close variant with "macros"); **store** means the query `<Name> app` restricted to apps.apple.com and play.google.com. **Weight** says whether the same-name use is in a food, recipe, nutrition or meal-planning app or service (**serious**) or elsewhere (**lighter**), per the §2.5 evidence rule. The per-name evidence for the shortlist is in §6.8.3.

**Tally.** 111 of the 129 session-4 words were screened by search (the rest by judgment, §4.8.6). **43 are already the exact name of a recipe, meal-planning or nutrition app or service**, and about 14 more have a near-identical name in the category (Honeydew, Oatsy, Nooddle, BigOven, MealJar, WokTheWeek, Crumbs, Herbi, Deglaze, Drizzle Me Skinny, LaLa Lunchbox, Brunch Bites, PlateFul, Nugget Markets).

| Name | Query (variant) | Status | Weight | What the search showed | Links |
|---|---|---|---|---|---|
| Ladle | standard | Risk (screened out) | Serious | "Ladle: Recipe & Meal Planner - Apps on Google Play"; "Ladle: Recipes & Meal Plan - App Store"; "useLadle: Meal Planner"; "Ladle - Recipes and Cooking"; "Ladle I AI-powered sous chef for women in midlife"; "Ladle - Your Recipe Book, Reimagined" (getladle.app) | [Play](https://play.google.com/store/apps/details?id=com.ladle.app&hl=en_US), [App Store](https://apps.apple.com/us/app/ladle-recipes-meal-plan/id6760197380), [useLadle](https://play.google.com/store/apps/details?id=com.useladle.app&hl=en_US), [getladle.app](https://getladle.app/) |
| Pinch | standard, then `"Pinch" recipe app App Store cooking` | Inconclusive, then Risk (screened out) | Serious | "Pinch It! Recipe Box" (Just A Pinch; "build custom meal plans"); "Pinch: Follow. Cook. Share." (social recipe network) | [Pinch It!](https://apps.apple.com/us/app/pinch-it-recipe-box/id1451513406), [Pinch](https://apps.apple.com/us/app/pinch-follow-cook-share/id6761978337) |
| Crumb | standard | Risk (screened out) | Serious | "Crumbs Meal Plans & Recipes"; "Crumb: Recipe & Dinner Ideas"; "Fridge Recipe Generator: Crumb"; "Crumb — Plan your meals, simplify your week" | [Crumbs](https://apps.apple.com/us/app/crumbs-meal-plans-recipes/id6740446268), [Crumb](https://apps.apple.com/us/app/crumb-recipe-dinner-ideas/id6475651024), [getcrumbapp.com](https://getcrumbapp.com/) |
| Spoonful | standard | Risk (screened out) | Serious | "Spoonful: Diet & Food Scanner" (IBS, celiac, allergies; recipes; nutrition logging) | [App Store](https://apps.apple.com/us/app/spoonful-diet-food-scanner/id1481914232), [spoonfulapp.com](https://spoonfulapp.com/) |
| Forkful | standard | Risk (screened out) | Serious | "Forkful: Recipe Meal Planner"; "Forkful - Reels to meals"; "Forkful \| Recipes, Meal Plans, Grocery Lists & Nutrition Tracking" | [App Store](https://apps.apple.com/us/app/forkful-recipe-meal-planner/id6760579706), [forkful.food](https://forkful.food/) |
| Pantry | `"Pantry" app "meal planner" OR recipes OR macros` | Risk (screened out) | Serious | "Pantry: macros from receipts" (photo calories and macros, receipt scanning) | [getpantry.app](https://getpantry.app/) |
| Scoop | standard + macros | Risk (screened out) | Serious | "Scoop: Healthy Eating Out" ("an AI nutrition coach that knows the menu… your allergies, your macros") | [App Store](https://apps.apple.com/us/app/scoop-healthy-eating-out/id6757786715) |
| Dollop | `"Dollop" app recipes OR "meal planner" OR food` | Risk (screened out) | Serious | "Dollop — Dinner, Decided. Personalized Recipe Discovery" | [dolloponline.com](https://dolloponline.com/) |
| Sumac | standard + food | Risk (screened out) | Serious | "Sumac Recipe Manager App - App Store" (recipes, meal-plan calendar, shopping lists) | [App Store](https://apps.apple.com/us/app/sumac-recipe-manager/id6753876940) |
| Saffron | standard | Risk (screened out) | Serious | "Saffron: Your Digital Cookbook" (recipe manager, meal planner, nutrition estimates) | [App Store](https://apps.apple.com/us/app/saffron-your-digital-cookbook/id1438683531) |
| Basil | standard + App Store | Risk (screened out) | Serious | "Basil: Recipes & Meal Planner" (import incl. TikTok and Instagram, allergens, calories and macros); "Chef Basil" | [App Store](https://apps.apple.com/us/app/basil-recipes-meal-planner/id6740829669), [Chef Basil](https://apps.apple.com/gh/app/chef-basil/id6761494168) |
| Fennel | standard; store | Inconclusive, then Risk (screened out) | Serious | Category query: recipes only. Store: "Fennel: Invest your way"; the summary describes a "Fennel Recipe App" (import by URL, shopping lists); "Fennel Restaurant" | [Fennel invest](https://apps.apple.com/us/app/fennel-invest-your-way/id6443565903), [Fennel](https://apps.apple.com/za/app/fennel/id6759586338) |
| Tahini | standard | Inconclusive (screened out on judgment) | — | Only tahini recipes; no Tahini app | — |
| Lentil | standard | Risk (screened out) | Serious | "Lentil - Food Insights App" (meal and menu scans, AI nutrition coach) | [App Store](https://apps.apple.com/us/app/lentil-food-insights/id6756281742) |
| Olive | standard + macros | Risk (screened out) | Serious | "Olive: Your Holistic Health Companion" (food scanner with lab-tested contaminant data) | [oliveapp.com](https://www.oliveapp.com/blogs/best-food-scanner-app-for-healthier-eating) |
| Pepper | `"Pepper" app recipes cooking social OR "meal planner"` | Risk (screened out) | Serious | "Pepper - Recipe Organizer" (social cookbook, import from Instagram and TikTok); "Pepperplate" planner | [App Store](https://apps.apple.com/us/app/pepper-recipe-organizer/id1583947369), [peppertheapp.com](https://peppertheapp.com/) |
| Chili | `"Chili" OR "Chilli" app …` | Risk (screened out) | Serious | "Chilli food App - App Store" | [App Store](https://apps.apple.com/us/app/chilli-food/id6458737266) |
| Tofu | standard + macros | Risk (screened out) | Serious | "Tofu - Vegan Recipes" ("300+ plant-based recipes… macros on each"); "Tasty Tofu Recipes" | [App Store](https://apps.apple.com/us/app/tofu-vegan-recipes/id6761143218), [gettofu.app](https://gettofu.app/) |
| Sesame | standard | Risk (screened out) | Serious | "Sesame: Healthy Food Scanner" (made "with clinical nutrition experts") | [App Store](https://apps.apple.com/us/app/sesame-healthy-food-scanner/id6471442567) |
| Radish | standard + food; store | Risk (screened out) | Lighter (food: a restaurant); C5 neighbour | "Radish Kitchen" (salad restaurant ordering); store: "Radish Health" (doctor access, prescriptions), "Radish Mobile" (radiology community), "Radish Fiction" | [Radish Health](https://apps.apple.com/us/app/radish-health/id1556054938), [Radish Fiction](https://apps.apple.com/ca/app/radish-fiction/id1076491465) |
| Stir | standard + cooking | Risk (screened out) | Serious | "Stir - Your Recipe Assistant" (Instagram and TikTok import, "tracks 7 nutrients per serving", weekly plan); "Stir & Store" | [App Store](https://apps.apple.com/gb/app/stir-your-recipe-assistant/id6760202603), [Stir & Store](https://apps.apple.com/us/app/stir-store/id6760269255) |
| Sear / Braise | `"Sear" OR "Braise" app …` | Inconclusive (screened out on judgment) | — | Generic meal-planner results only | — |
| Batch | `"Batch" app "meal prep" OR …` | Inconclusive (screened out on judgment) | — | Batch-cooking articles and MealPrepPro, Mob; no Batch app | — |
| Supper | standard | Risk (screened out) | Serious | "Supper: Recipes & Meal Planner" (social import, meal prep, "nutrition and macros information for every recipe"); "Supperhero – AI meal planner"; supperapp.io | [Play](https://play.google.com/store/apps/details?id=com.nabustudio.supper), [Supperhero](https://apps.apple.com/us/app/supperhero-ai-meal-planner/id6738939154) |
| Galley | `"Galley" app recipes OR "meal planner" OR food` | Risk (screened out) | Serious (culinary software) | "Galley Solutions: Culinary Resource Planning for Every Kitchen" | [galleysolutions.com](https://www.galleysolutions.com/) |
| Kettle | `"Kettle" app …`; store | Inconclusive (category), then Risk | Lighter, with a health neighbour | See §6.8.3 | — |
| Mango | standard + macros | Risk (screened out) | Serious | "Mango Bites - Food Tracker"; "Mango AI - Calorie Tracker" | [Mango Bites](https://apps.apple.com/us/app/mango-bites-food-tracker/id6743328271), [Mango AI](https://apps.apple.com/lt/app/mango-ai-calorie-tracker/id6742989225) |
| Munch | standard + macros | Risk (screened out) | Serious | "Munched: Nutrition Scanner"; "MUNCH: AI Lifestyle Planner"; "Munchi: Meal Planner & Recipes"; "munch - eat out healthy"; "Munch: Simple Food Diary"; "Munch Metrics" | [Munchi](https://apps.apple.com/us/app/munchi-meal-planner-recipes/id6783936727), [MUNCH](https://apps.apple.com/gb/app/munch-ai-lifestyle-planner/id6760965644) |
| Crunch | standard | Risk (screened out) | Serious | "crunch - App Store"; "Crunch: Voice & AI Calorie Log"; "Crunch+ Workout & Fitness Plan" (Crunch Fitness) | [Play](https://play.google.com/store/apps/details?id=com.crunchai.app&hl=en_US) |
| Spoon | standard + macros | Risk (screened out) | Serious | "Spoon: Recipe & Meal Planner"; "Spoon: Smart Calorie Tracker"; "spoonacular food companion" | [App Store](https://apps.apple.com/us/app/spoon-recipe-meal-planner/id6759272641), [Play](https://play.google.com/store/apps/details?id=com.oumlah.spoonapp&hl=en_US) |
| Oven | standard | Risk (screened out) | Serious (near) | "BigOven Recipes & Meal Planner" | [Play](https://play.google.com/store/apps/details?id=com.bigoven.android&hl=en_US&gl=US) |
| Pickle | see §6.8.3 | — | — | Shortlisted | — |
| Lemon | standard + macros | Risk (screened out) | Serious | "Lemon: Nutrition Made Simple" (recipes, import, per-portion breakdown, meal plans); lemonnutrition.eu | [App Store](https://apps.apple.com/us/app/lemon-nutrition-made-simple/id6618148167), [lemonnutrition.eu](https://lemonnutrition.eu/) |
| Jar | `"Jar" OR "Jars" app …` | Risk (screened out) | Serious (near) | "MealJar - Meal Planner App for iOS" | [mealjar.app](https://mealjar.app/) |
| Wok | standard | Risk (screened out) | Serious (near) | "WokTheWeek – Weekly Meal Planner for Households" | [woktheweek.com](https://woktheweek.com/) |
| Fork | standard + macros | Risk (screened out) | Serious | "Forks Meal Planner" (Forks Over Knives); Forkful; "Forked AI" | [App Store](https://apps.apple.com/us/app/forks-meal-planner/id1484372198) |
| Grill | `"Grill" OR "Griddle" app …` | Risk (screened out) | Lighter (restaurant) | "Grill'd - Apps on Google Play" (restaurant with nutrition info) | [Play](https://play.google.com/store/apps/details?id=com.grilld.grilld&hl=en_US) |
| Feast | standard + macros | Risk (screened out) | Serious | "Feast: Nutrition Coach"; "Feast - Caloric Intelligence" | [App Store](https://apps.apple.com/us/app/feast-nutrition-coach/id6740829087) |
| Savor | `"Savor" OR "Savour" app …` | Risk (screened out) | Serious | "Savor - Meal Planner" (diet, allergies, budget, supermarket pricing, social import); "Savour App"; "savori - meal plan & groceries" | [App Store](https://apps.apple.com/us/app/savor-meal-planner/id6615086643), [savori](https://play.google.com/store/apps/details?id=com.savori&hl=en_US) |
| Nacho / Taco | `"Nacho" OR "Taco" app …` | Inconclusive (Taco screened out on judgment; Nacho shortlisted) | — | Recipes only; no Nacho or Taco meal-planner app | — |
| Noodle | standard | Risk (screened out) | Serious (near) | "ekilu - healthy recipes & plan" (package `es.nooddle`); summary: "previously known as Nooddle" | [Play](https://play.google.com/store/apps/details?id=es.nooddle&hl=en_US&gl=US) |
| Sprout | standard | Risk (screened out) | Serious | "Sprout AI - Healthy Recipes"; "Sproutly \| AI Meal Planner & Smart Pantry Tracker"; "Sprout Cooking — Any Recipe, Made for You" | [App Store](https://apps.apple.com/us/app/sprout-ai-healthy-recipes/id6744351406), [sproutcooking.app](https://sproutcooking.app/) |
| Kernel | standard + food | Inconclusive (screened out on judgment) | — | No Kernel app | — |
| Brunch / Snack | `"Brunch" OR "Snack" app …` | Risk (screened out) | Serious (small) | "Brunch Bites" (recipes, grocery lists, macros) | [App Store](https://apps.apple.com/us/app/-/id1529171760) |
| Picnic | `"Picnic" app groceries OR recipes OR "meal planner"` | Risk (screened out) | Serious | "Picnic: Supermarket & Recipes" ("supermarket, planner, shopping list and recipes in one"); "Picnic: order, cook, eat" | [App Store](https://apps.apple.com/us/app/picnic-supermarket-recipes/id1018175041), [Play](https://play.google.com/store/apps/details?id=com.picnic.android&hl=en) |
| Crust / Loaf | `"Crust" OR "Loaf" app …` | Inconclusive (screened out on judgment) | — | No Crust or Loaf app | — |
| Harvest / Basket | `"Harvest" OR "Basket" app …` | Risk (Harvest, screened out) | Serious | "Harvest — Meal Planning App" (myharvest.app); "Daily Harvest App" | [myharvest.app](https://myharvest.app/), [Daily Harvest](https://apps.apple.com/us/app/daily-harvest/id1437836101) |
| Spice / Herb | `"Spice" OR "Herb" app …` | Risk (Herb, screened out) | Serious (near) | "Herbi: Meal Planner + Recipes" (budget, dietary needs, macros); "Food Now Spice Guide" | [App Store](https://apps.apple.com/gb/app/herbi-meal-planner-recipes/id6777230233) |
| Apron | standard | Risk (screened out) | Serious | "Apron: Recipes & Grocery Lists" (pantry tracking, meal planning); "Blue Apron: Meal Kit Delivery" | [App Store](https://apps.apple.com/app/id6736772028), [Blue Apron](https://apps.apple.com/us/app/blue-apron-meal-kits/id976642810) |
| Toast / Yum | `"Toast" OR "Yum" app …`; store `Toast app` | Risk (both screened out) | Serious (Yum); lighter but heavy (Toast) | "Yum AI: Recipes & Meal Planner"; "Yum: Easy & Tasty Recipes"; Wholesome Yum; Yummly. Store: "Toast - Local Restaurants" (Toast Local), "Toast Now", "MyToast" | [Yum AI](https://apps.apple.com/ca/app/yum-ai-recipes-meal-planner/id6739822998), [Toast Local](https://apps.apple.com/us/app/toast-local-restaurants/id1362180579) |
| Honey / Butter | `"Honey" OR "Butter" app …` | Risk (Honey, screened out on the near name) | Serious (near) | "Honeydew - Recipe Capture & Meal Planning App"; no Honey or Butter app | [honeydewcook.com](https://honeydewcook.com/) |
| Maple | standard | Risk (screened out) | Serious | "Maple Meal Planner \| Take stress off your plate"; "Maple has been acquired by Wander and will sunset on December 31, 2026" | [growmaple.com](https://www.growmaple.com/meal-planner) |
| Ginger | standard | Inconclusive (screened out on judgment) | — | No Ginger meal-planner app | — |
| Cumin / Clove | `"Cumin" OR "Clove" app …` | Risk (Clove, screened out) | Serious | "Clove \| Free AI Weekly Meal Planner"; "Clove: Import & Share Recipes" | [clove.kitchen](https://clove.kitchen/meal-plan), [App Store](https://apps.apple.com/us/app/clove-import-share-recipes/id6741995783) |
| Oats / Cress | `"Oats" OR "Cress" app …` | Risk (Oats, near); Inconclusive (Cress) | Serious (near) | "Oatsy Calorie Deficit Calculator \| Best Free Nutrition App" | [oatsyapp.com](https://www.oatsyapp.com/) |
| Tidbit / Smidge | `"Tidbit" OR "Smidge" app …` | Risk (Tidbit); Inconclusive (Smidge) | Serious | "Tidbit — Clean nutrition and GLP-1 tracking for iPhone" | [tidbitfood.app](https://tidbitfood.app/) |
| Handful | see §6.8.3 | — | — | Shortlisted | — |
| Spatula / Skewer | `"Spatula" OR "Skewer" app …` | Risk (Spatula, screened out) | Serious | Spatula "smart and social recipe box" | [App Store](https://apps.apple.com/mx/app/spatula/id1090496189) |
| Truffle / Crumble | `"Truffle" OR "Crumble" app …` | Risk (both screened out) | Serious (Crumbs near); lighter (Truffle Blog) | "Truffle Blog" food-content app; "Crumbs Meal Plans & Recipes" | [Truffle Blog](https://apps.apple.com/hn/app/truffle-blog/id6746181470) |
| Nugget | standard + food | Risk (screened out) | Serious (grocer) | "Meal Planning 101 - Nugget Markets Daily Dish" | [nuggetmarket.com](https://www.nuggetmarket.com/articles/2885/meal-planning-101/) |
| Wedge / Slice | `"Wedge" OR "Slice" app …` | Inconclusive (screened out on judgment) | — | No Wedge or Slice meal-planner app | — |
| Bagel / Muffin | `"Bagel" OR "Muffin" app …`; store `Bagel app` | Inconclusive (category), then Risk (Bagel, shortlisted) | — | See §6.8.3 | — |
| Dumpling | standard | Inconclusive (screened out on judgment) | — | No Dumpling app | — |
| Garlic / Onion | `"Garlic" OR "Onion" app … App Store` | Risk (Garlic, screened out) | Serious | "Garlic Recipe Keeper & Planner" (weekly plans, estimated nutrition, pantry) | [App Store](https://apps.apple.com/us/app/garlic-recipe-keeper-planner/id6758080753) |
| Carrot | standard | Risk (screened out) | Serious | "Carrot AI - Your Complete Kitchen Assistant \| AI Meal Planner"; "Carrot: Calorie Counter & AI"; "Carroty - Grocery Lists & Meal Plans"; "Purple Carrot" | [carrotai.app](https://www.carrotai.app/), [App Store](https://apps.apple.com/gb/app/carrot-calorie-counter-ai/id6747942538) |
| Almond / Cocoa | `"Almond" OR "Cocoa" app …` | Inconclusive (screened out on judgment) | — | Recipes only | — |
| Peach / Cherry | `"Peach" OR "Cherry" app …` | Risk (Peach, screened out) | Serious | "Peach: AI Calorie Tracker" (macro tracker, AI meal planner) | [App Store](https://apps.apple.com/us/app/peach-ai-calorie-tracker/id6748237403) |
| Nibble | standard + macros | Risk (screened out) | Serious | "MealPrepPro Meal Planner" by **Nibble Apps**; "Nibble: Find Safer Foods"; "Nibble AI - Calorie Tracker"; "Recipe Manager - Nibbly" | [nibbleapps.com](https://nibbleapps.com/), [Nibble AI](https://apps.apple.com/us/app/nibble-ai/id6756195763) |
| Mouthful / Plateful | `"Mouthful" OR "Plateful" app …` | Risk (Plateful); Inconclusive (Mouthful) | Serious (menu and nutrient software) | "PlateFul \| Senior Living Menu Management Software" (nutrient analysis); "Plateful Nutrition" | [diningrd.com](https://www.diningrd.com/plateful.html) |
| Tray / Pan | `"Tray" OR "Pan" app …` | Inconclusive (screened out on judgment) | — | No Tray or Pan app | — |
| Roast / Glaze | `"Roast" OR "Glaze" app …` | Risk (Glaze, near) | Serious (near) | "Deglaze: Cooking, Simplified" recipe app | [App Store](https://apps.apple.com/us/app/deglaze-cooking-simplified/id6443578246) |
| Mortar / Tongs / Grater | `"Mortar" OR "Tongs" OR "Grater" app …` | Inconclusive (screened out on judgment) | — | Kitchen-equipment pages only | — |
| Jam / Berry | `"Jam" OR "Berry" app …` | Inconclusive (screened out on judgment) | — | Jam recipes only | — |
| Tapas | `"Tapas" app …`; store | Inconclusive (category), then Risk (shortlisted) | — | See §6.8.3 | — |
| Crisp | `"Crisp" app …`; store | Risk (screened out) | Serious (grocer, healthy restaurant) | "CRISP & GREEN" app (healthy restaurant, recipes, nutrition); store: "Crisp supermarkt" / "Crisp - online supermarkt" (NL); "Crisp" customer-chat SaaS; "Crisp - AI Photo Enhancer" | [Crisp supermarkt](https://apps.apple.com/us/app/crisp-supermarkt/id1416625210), [CRISP & GREEN](https://apps.apple.com/us/app/crisp-green/id1180644340), [Crisp chat](https://apps.apple.com/us/app/crisp/id1085770229) |
| Drizzle / Sizzle | `"Drizzle" OR "Sizzle" app …` | Risk (both screened out) | Serious | "Drizzle Me Skinny - Healthy Recipes and Meals" (Weight Watchers points); "Sizzle App" recipe manager and meal planner; sizzle-app.com | [Amazon](https://www.amazon.com/Drizzle-Me-Skinny-Healthy-Recipes/dp/B01BPZTJ96), [Sizzle](https://apps.apple.com/app/sizzle-app/id6743368861) |
| Lunchbox | standard + "meal prep" | Risk (screened out) | Serious | "LaLa Lunchbox" (kids' meal planning); "Little Lunches: Kids Meals"; "Athlete Lunchbox" meal prep | [LaLa Lunchbox](https://apps.apple.com/us/app/lala-lunchbox/id519037961) |
| Bistro | standard; store | Inconclusive (category), then Risk (screened out) | Serious (food delivery) | Store: "Bistro: Food in minutes" (Blinkit Foods, IN); "Bistro.sk" (2,400+ restaurants); "Hello Bistro"; the Bagel search also surfaced a bistromd.com nutrition blog (bistroMD is a diet-meal delivery service, reviewer knowledge) | [Bistro](https://apps.apple.com/in/app/bistro-food-in-minutes/id6670203019), [Bistro.sk](https://apps.apple.com/us/app/bistro-sk/id828925849) |
| Helping | `"Helping" app food …` | Inconclusive (screened out on judgment) | — | Generic meal-planner results only | — |
| PL-market check for the top 3 | `aplikacja "Salsa" OR "Pretzel" OR "Donut" dieta przepisy kalorie` | Inconclusive | — | Polish diet-app roundups (Fitatu, Fit-World, Cal AI, Dine4Fit) and donut calorie pages; the summary: "the specific applications 'Salsa,' 'Pretzel,' and 'Donut' were not found as dedicated diet applications" | [dietetycy.org.pl](https://dietetycy.org.pl/aplikacje-dietetyczne/) |
| Salsa, Pretzel, Donut, Pickle, Handful, Kettle, Tapas, Nacho, Melon, Bagel, Pesto, Caper, Gravy | see §6.8.3 | — | — | Shortlisted; full per-name evidence in §6.8.3 | — |

---

## 6. Shortlist

> **Current shortlist: §6.8 (session 4, 2026-09-25), placed first below.** It is numbered 6.8 so that existing references to §6.1–§6.7 still point to the right text. The session-3 shortlist (§6.7) and its top 3 (Zubo, Kazu, Dozo; alternates Nimbo, Gobo) are **superseded (PO: "nothing from proposals")**. The session-2 shortlist (§6.1–§6.3) and top 3 (Tangram, Ramekin, Palmo) are **superseded (PO: too long, not catchy)**. Both are kept below with all their evidence.

### 6.8 Session 4: short real English food-word shortlist (current)

Thirteen names, all real English words (four are dictionary loanwords: Salsa, Tapas, Nacho, Pesto), 5–7 letters and 2 syllables. All checks are dated **2026-09-25**. Store, domain, trademark and handle checks are **Pending** for every name because the official sources were egress-blocked (§5.1). The bracketed text is the search-engine indication only. **Food** = food hint (PO questionnaire); **D/S** = suggestive / borderline (§2.5 rule 3); **N** = C10 international neutrality; **Catch** = C11 catchiness (§2.3). All are reviewer assessments.

#### 6.8.1 Check matrix

| Name | L/S | Food | D/S | 1 Competitors / similar | 2 App Store | 3 Google Play | 4 .com | 4 .app | 4 .io | 4 .pl | 5 Trademarks (EUIPO / TMview / UPRP / WIPO / USPTO / UKIPO) | 6 Language PL/EN | 7 Confusing similarity | 8 Social handles | N | Catch |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Salsa** | 5/2 | Clear | S | Inconclusive in food apps; Risk in software: Salsa Labs (nonprofit SaaS), salsa.dev (payroll API), SALSA UK food-safety scheme | Pending (Risk, lighter: dance-event and dance-lesson "Salsa App"s) | Pending (Risk, lighter: dance events; "Salsa Live Stream & Video Chat") | Pending (not searched; very likely registered) | Pending (Inconclusive) | Pending (Risk: salsapp.io / salsaapp.io used by the dance app) | Pending (Inconclusive) | Pending (**Risk: UK SALSA reg. UK00003937773, SALSA Scheme Ltd, software for "food safety compliance"**; SALSA SYSTEMS, US) | Inconclusive: identical in PL/EN; ES/IT/PT *salsa* = "sauce" | Risk (medium): UK food-safety software mark | Pending (Risk: live-streaming "Salsa App" holds @salsa.appoficial, @salsalatam, @salsa.usa) | 4 | 5 |
| **Pretzel** | 7/2 | Clear | S | Risk, lighter: pretzel-chain apps; Pretzel AI, GetPretzel (software) | Pending (Risk, lighter: "Pretzel Rated", chain ordering apps) | Pending (Risk, lighter: "Pretzel POS" hospitality, chains) | Pending (Inconclusive) | Pending (Inconclusive) | Pending (Risk: an Instagram @pretzel.io shopping app; domain unverified) | Pending (Inconclusive) | Pending (**Risk: US PRETZEL reg. 5312372, language-learning software, class 9**; PRETZEL THERAPEUTICS, class 5) | Inconclusive: PL hears *precel* (same sound, PL spelling) | Risk (medium): same-name class-9 software outside food | Pending (Risk: @pretzel.app = Pretzel Rated) | 4 | 4 |
| **Donut** | 5/2 | Clear | S | Risk: Donut for Slack (donut.com, 20,000+ companies); donut shops | Pending (Risk: "I Deserve a Donut" weight-loss devotional app; games; Dunkin') | Pending (Risk, lighter: a delivery-driver app; shop apps) | Pending (Risk: donut.com = Donut for Slack) | Pending (Inconclusive) | Pending (Risk: app.donut.io = Donut dashboard) | Pending (Inconclusive) | Pending (Risk: DONUT LAB application, vehicle software, class 9; DONUT (Donut Media), class 41; DONUTS (domain registry)) | Risk (mild): UK "you donut"; donut/doughnut spelling | Risk (medium-high): identical well-known SaaS name in 9/42 | Pending (Risk: @donut_app, @donut.ai, @donutmedia) | 4 | 5 |
| **Pickle** | 6/2 | Clear | S | **Risk, serious: Pickle.ph healthy meal-plan delivery with calorie calculator and macro-balanced plans (PH)** | Pending (Risk, lighter: fashion rental, pickleball) | Pending (Risk, lighter: money, notes, reels) | Pending (Inconclusive) | Pending (Inconclusive) | Pending (Risk: a cloud platform per a summary, unverified) | Pending (Inconclusive) | Pending (Risk: PICKLE (Pickle, Inc.), PICKLEPAY, DESIGN PICKLE, PICKLEGRAM in 9/42) | Risk: DE *Pickel* = pimple; "in a pickle" | Risk (medium-high) | Pending (Risk: @getpickle, @getpickle.ai) | 3 | 5 |
| **Handful** | 7/2 | Moderate | B | Risk, lighter: handful.com sports-bra brand; Healthy Handfuls kids' snacks | Pending (Risk, lighter: "Handful: Daily Gratitude") | Pending (Inconclusive) | Pending (Risk: handful.com in use, sports bras) | Pending (Inconclusive) | Pending (Inconclusive) | Pending (Inconclusive) | Pending (Inconclusive: no HANDFUL mark surfaced) | Risk (mild): "a handful" = hard to manage; bra-brand innuendo | Risk (low-medium) | Pending (Risk: @handful = sports-bra brand, 43K) | 3 | 3 |
| **Kettle** | 6/2 | Moderate (kitchen) | S | Risk: Kettle Brand chips, Kettle & Fire (class 29) | Pending (Risk: "Kettle: AI Fitness Coach", KettlePay) | Pending (Risk, lighter: networking app, café ordering) | Pending (Inconclusive) | Pending (Inconclusive) | Pending (Risk: kettle.io agency) | Pending (Inconclusive) | Pending (Risk: KETTLE BRAND, KETTLE & FIRE, class 29) | Inconclusive: word little known in PL | Risk (medium): fitness-coach app | Pending (Risk: @kettle = Kettle Pay) | 3 | 3 |
| Tapas | 5/2 | Clear | S/B | Risk, heavy: Tapas comics (Tapas Media) | Pending (Risk, heavy: "Tapas – Comics and Novels") | Pending (Risk, heavy: same) | Pending | Pending | Pending | Pending | Pending (Risk: US TAPAS reg., social networking and comics) | Risk: descriptive in ES | Risk (high) | Pending | 3 | 4 |
| Nacho | 5/2 | Clear | S | Risk, lighter: restaurants; NachoNacho SaaS | Pending (Risk, lighter: restaurant apps) | Pending (Risk: a Spaces wallet app) | Pending (Inconclusive) | Pending (Inconclusive) | Pending (Inconclusive) | Pending | Pending (Risk, low: NACHO MAMAS, classes 30 and 42) | Risk: PL reads "ch" as [x] | Risk (medium) | Pending (Risk: @nacho, 15M personal) | 3 | 5 |
| Melon | 5/2 | Clear | S | **Risk, serious: a MELON filing for a weight-loss-habit tracking app**; near Mela and Melo AI | Pending (Risk: several Melon apps) | Pending (Risk, heavy: Kakao's Melon music) | Pending | Pending | Pending | Pending | Pending (Risk: Melon Innovations LLC app filing) | Risk: slang "melons" (breasts), UK "melon" (head) | Risk (high) | Pending | 4 | 4 |
| Bagel | 5/2 | Clear | S | Risk, heavy: Coffee Meets Bagel dating app | Pending (Risk: CMB, bagel chains) | Pending (Risk: CMB) | Pending | Pending | Pending | Pending | Pending | Risk: PL "BA-gel" vs EN "BAY-gel" | Risk (medium-high) | Pending | 4 | 4 |
| Pesto | 5/2 | Clear | S | **Risk, serious: "Pesto - Recipe App" (organiser, weekly meal planner, shopping list) on the Polish App Store** | Pending (Risk, serious) | Pending (Risk: "pesto", Pesto Assistant) | Pending | Pending | Pending | Pending | Pending | Inconclusive: IT descriptive | Risk (high) | Pending | 4 | 5 |
| Caper | 5/2 | Clear | S | **Risk, serious-adjacent: Instacart Caper AI grocery carts (caper.ai)** | Pending (Risk: Capper betting app) | Pending (Risk: Caper logistics apps) | Pending | Pending | Pending | Pending | Pending | Risk: PL "KA-per" vs EN "KAY-per" | Risk (high) | Pending | 3 | 4 |
| Gravy | 5/2 | Clear | S | **Risk, reputational: Gravy Analytics, FTC order on selling sensitive location data (2025)** | Pending (Risk: fintech "Gravy" apps) | Pending (Risk: Gravy, All Gravy) | Pending | Pending | Pending | Pending | Pending | Risk: PL "GRA-vy"; "gravy train" | Risk (medium-high) | Pending | 3 | 4 |

#### 6.8.2 Scores (C1–C7, C10, C11) and ranking

Scores run from 1 (poor) to 5 (strong) and are the reviewer's assessment of the evidence above. **C8 (domains and handles) and C9 (trademarks) are Pending for every name** and are not scored. "Evidence weight" summarises the search-engine Risk findings using the §2.5 rule (same-name use in food, recipe, nutrition or meal-planning apps is serious; elsewhere is lighter); it is a triage signal, not a legal assessment. The rank weighs the C1–C7 sum, C10, C11, the food hint and the evidence weight together, so a higher sum does not always mean a higher rank. **This is a recommendation for further investigation, not a selection.**

| Rank | Name | L/S | C1 | C2 | C3 | C4 | C5 | C6 | C7 | Sum /35 | C10 /5 | C11 /5 | Food | Evidence weight (SE) | Further investigation? |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **Salsa** | 5/2 | 3 | 5 | 5 | 3 | 5 | 5 | 4 | 30 | 4 | 5 | Clear | **Medium:** no food or nutrition app of this name seen; store search owned by dance and live-streaming apps; software namesakes (Salsa Labs, salsa.dev); a UK SALSA mark for food-safety compliance software | **Yes, top 3** |
| 2 | **Pretzel** | 7/2 | 4 | 4 | 5 | 4 | 5 | 5 | 5 | 32 | 4 | 4 | Clear | **Medium:** pretzel chains' ordering apps and a hospitality POS (lighter); a US PRETZEL registration for language-learning software (class 9); @pretzel.app taken | **Yes, top 3** |
| 3 | **Donut** | 5/2 | 3 | 4 | 4 | 4 | 4 | 5 | 5 | 29 | 4 | 5 | Clear | **Medium-high:** Donut for Slack is a well-known SaaS in 9/42 (lighter category, but a strong brand); a weight-loss devotional app "I Deserve a Donut"; donut.com and app.donut.io in use | **Yes, top 3** |
| 4 | **Pickle** | 6/2 | 3 | 4 | 3 | 4 | 5 | 5 | 5 | 29 | 3 | 5 | Clear | **Medium-high:** Pickle.ph, a healthy meal-plan delivery service with macros (serious, PH market); several PICKLE software marks; DE *Pickel* = pimple | Yes, alternate |
| 5 | **Handful** | 7/2 | 4 | 4 | 3 | 4 | 4 | 5 | 5 | 29 | 3 | 3 | Moderate | **Medium:** nothing in food or nutrition apps; handful.com sports-bra brand and @handful; a gratitude app; borderline descriptive for portions | Yes, alternate |
| 6 | Kettle | 6/2 | 4 | 3 | 4 | 3 | 5 | 5 | 5 | 29 | 3 | 3 | Moderate | Medium-high: "Kettle: AI Fitness Coach" (health-adjacent class 9); food marks in class 29; @kettle taken | Only if the top 5 all fail |
| 7 | Tapas | 5/2 | 3 | 5 | 5 | 4 | 5 | 5 | 4 | 31 | 3 | 4 | Clear | **High:** Tapas (comics) by Tapas Media, a major class-9/41 app with a US TAPAS registration; descriptive for food service in ES | No |
| 8 | Pesto | 5/2 | 3 | 5 | 5 | 3 | 5 | 5 | 4 | 30 | 4 | 5 | Clear | **High:** "Pesto - Recipe App", a recipe organiser and meal planner, on the Polish App Store | No |
| 9 | Melon | 5/2 | 3 | 5 | 3 | 2 | 4 | 5 | 5 | 27 | 4 | 4 | Clear | **High:** a MELON filing for a weight-loss tracking app; Kakao's Melon music; near Mela and Melo AI; slang | No |
| 10 | Caper | 5/2 | 3 | 3 | 4 | 3 | 5 | 5 | 5 | 28 | 3 | 4 | Clear | **High:** Instacart's Caper AI grocery carts (grocery tech next to our shopping list) | No |
| 11 | Bagel | 5/2 | 3 | 3 | 5 | 2 | 5 | 5 | 4 | 27 | 4 | 4 | Clear | Medium-high: Coffee Meets Bagel; bagel chains; PL/EN pronunciation split | No |
| 12 | Nacho | 5/2 | 3 | 3 | 4 | 3 | 4 | 5 | 4 | 26 | 3 | 5 | Clear | Medium: restaurants and small software; but Poles read "ch" as [x] and the pun only works in English | No |
| 13 | Gravy | 5/2 | 3 | 3 | 3 | 3 | 4 | 5 | 5 | 26 | 3 | 4 | Clear | **High (reputational):** Gravy Analytics, subject of a 2025 FTC order on selling sensitive location data | No |

**Catchiness in one line each (C11):**
- **Salsa (5):** two bright "a" vowels and a doubled "s", with a dance built into the word; the same sound in PL and EN.
- **Pretzel (4):** a crisp "pr-tz" snap and a strong icon (the knot); one consonant cluster too many for a 5.
- **Donut (5):** round, soft and cheerful; the logo draws itself.
- **Pickle (5):** bouncy, a little silly, instantly memorable.
- **Handful (3):** friendly but flat, and three consonants in the middle.
- **Kettle (3):** homely rather than punchy.
- **Tapas (4), Nacho (5), Melon (4), Bagel (4), Pesto (5), Caper (4), Gravy (4):** all easy and fun; their problems are evidence and language, not sound.

**Trade-offs in brief:**
- **Salsa** fits the PO's answers best on sound and language: a real word everyone in PL and EN already knows, identical in both, clearly food, lively and catchy, with a built-in story (mix what you love with what you need; the rhythm of the week). The cost: the store search term belongs to dance and live-streaming apps, so the descriptor must do the work in search ("Salsa: Meal Planner & Macros", 28 characters). There are several SALSA software marks, and the nearest is a UK registration for food-safety compliance software. In Spanish, Italian and Portuguese *salsa* just means "sauce", which weakens the mark there.
- **Pretzel** scores highest on the criteria: clearly food, arbitrary for software (so the strongest trademark footing of the three), known across Europe (PL *precel*, DE *Brezel*), with the best product metaphor: the app twists a recipe until it fits your plan (PRD §8.3–§8.6). The costs: a US PRETZEL registration for language-learning software (class 9) needs an attorney's view; the long store title is exactly at 30 characters; @pretzel.app is taken; and a Pole who hears it may spell it "precel".
- **Donut** carries the core promise most directly: "yes, even this fits" (PRD §1), without moralizing (PRD §5). It is the catchiest and most iconic of the three. The costs: Donut for Slack is a well-known software brand with the identical name in 9/42, and naming a nutrition platform after a treat is a positioning bet that the PO should make on purpose (it could read as playful to the wedge and as flippant to dietitians, PRD §3).
- **Pickle** (alternate) has the best meal-prep meaning (pickling is making ahead, PRD §5) and top catchiness, but a Manila meal-plan service with macros uses the exact name, and in German *Pickel* means pimple.
- **Handful** (alternate) is the only portion word left that is not taken by a food app, and it matches the hand-portion idea. But its food hint is only moderate (the PO asked for "clearly"), it sits on the descriptive side for portion features, and handful.com is a sports-bra brand that plays on the word.
- **Tapas, Pesto, Melon, Caper and Gravy** are shown because they are the obvious catchy food words the PO might think of. Each has a high-weight problem: a major comics app (Tapas), a same-category recipe app in the Polish store (Pesto), a weight-loss app filing and slang (Melon), Instacart's grocery carts (Caper), and a data-privacy scandal (Gravy).

#### 6.8.3 Per-name evidence (session 4)

All checks are dated **2026-09-25**. "SE" means a WebSearch result that could not be opened. Domains: RDAP was blocked for every TLD, so every domain status is **Pending**. A 5–7 letter dictionary .com is almost always registered, so each block lists realistic variants to check first (`<name>.app`, `get<name>.com`, `eat<name>.com`, `<name>app.com`, `<name>.pl`). They are unverified and must be checked by RDAP before any decision. Trademark indications come from third-party mirror sites (Trademarkia, Justia, uspto.report) seen through the search engine, not from the registries. Handles on Facebook, YouTube, X, Threads and LinkedIn could not be checked and are **Pending** unless noted. Store titles use the reference descriptor ": Meal Planner & Macros"; a Polish-store alternative is ": Planer posiłków" (the descriptor may use diacritics; the brand does not).

---

##### `Salsa` (top 3)

- **Concept:** Salsa is what you get when you chop up good things and mix them into something you want to eat, which is what the app does with a recipe and your numbers. It is also the dance: rhythm, energy, the weekly loop. Food-positive and lively, never about restriction (PRD §5).
- **Pronunciation:** PL [ˈsalsa] "SAL-sa". EN UK /ˈsælsə/ "SAL-suh", US /ˈsɑːlsə/ "SAHL-suh". Everyone in the wedge already knows the word, and it is spelled the same after one hearing in both languages.
- **Meaning and connotations:** EN (a dictionary loanword) and PL: a spicy sauce or dip, and the Latin dance. ES, IT, PT: *salsa* = "sauce" in general. No rude, body or medical meanings known in PL, EN, DE, FR, ES, IT, PT, NL or SV (reviewer assessment). A mild Latin-American cuisine flavour (C7).
- **Positioning line:** "Salsa. The recipe you love, mixed to your numbers." / "Salsa – przepis, który lubisz, w Twoich makro."
- **Store title:** "Salsa: Meal Planner & Macros" (28 characters). PL: "Salsa: Planer posiłków i makro" (30).
- **Food hint / D/S:** clear / suggestive.
- **Catchiness:** 5/5.
- **Distinctiveness note (classes 9, 42, 44):** "salsa" names a food, not the service, so for nutrition and meal-planning software it is suggestive in EN and PL. EUIPO assesses meaning in every EU language: in ES, IT and PT *salsa* is the ordinary word for "sauce", so an examiner could call it descriptive of recipe content (publications, class 41/16) and allusive for nutrition advice (44). That weakens protection in those markets without obviously blocking registration for software. Several SALSA marks already exist in 9/42, so expect to rely on coexistence. An attorney's view is needed.
- **Main risks:** the UK SALSA registration covering food-safety compliance software; dance and live-streaming apps own the store search term; the exact .com and the main handles are very likely taken.

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Inconclusive (food) / Risk (software) | 2026-09-25 | [salsafood.co.uk](https://www.salsafood.co.uk/), [Salsa Labs (Wikipedia)](https://en.wikipedia.org/wiki/Salsa_Labs), [salsa.dev](https://www.salsa.dev/) | Category query `"Salsa" app recipes OR "meal planner" OR nutrition -dance` returned no Salsa recipe, meal-planning or nutrition app (only salsa recipes and "Salsarita's Nutrition Calculator", a restaurant). Software namesakes: Salsa Labs, a "SaaS company that provides donor management… to more than 3,000 nonprofit organizations"; Salsa, "embedded payroll solutions" (salsa.dev). SALSA = "Safe and Local Supplier Approval", a UK food-safety certification scheme run by SALSA Scheme Ltd ("a non-profit joint venture between FDF, NFU and UK Hospitality"). |
| 2 App Store (PL/US/GB) | Pending (SE: Risk, lighter) | 2026-09-25 | [Salsa App](https://apps.apple.com/us/app/salsa-app/id1601246909), [Salsa App](https://apps.apple.com/us/app/salsa-app/id6745124781), [Pocket Salsa](https://apps.apple.com/us/app/pocket-salsa/id371402545), [Salsa Rhythm](https://apps.apple.com/us/app/salsa-rhythm/id379868541) | Store-filtered SE: dance-event finders, dance lessons and a rhythm trainer. No food app. The iTunes API is blocked; App Store Connect availability is an owner action. |
| 3 Google Play | Pending (SE: Risk, lighter) | 2026-09-25 | [Salsa App](https://play.google.com/store/apps/details?id=com.salsapp), [Salsa Live Stream & Video Chat](https://play.google.com/store/apps/details?id=app.salsayou.android&hl=en_US) | Dance events; per the summary "a social streaming app built for India's digital content creators". No food app. |
| 4 Domains .com / .app / .io / .pl | Pending (SE: Risk for variants) | 2026-09-25 | RDAP blocked; [salsapp.io](https://salsapp.io/), [salsaapp.io](https://salsaapp.io/) | salsapp.io and salsaapp.io are used by the dance "Salsa App". Query `"salsa.app" OR "getsalsa.com" OR "salsa.io" OR "salsaapp.com"` showed nothing at those four. salsa.com was not searched; a 5-letter dictionary .com is very likely registered (unverified). **Not evidence of availability.** Check first: salsa.app, getsalsa.com, eatsalsa.com, salsa.pl. |
| 5 Trademarks | Pending (SE: Risk) | 2026-09-25 | [Trademarkia: SALSA UK00003937773](https://www.trademarkia.com/salsa-UK00003937773), [uspto.report: SALSA SYSTEMS 78026010](https://uspto.report/TM/78026010), [Justia: SALSA AND 97709873](https://trademarks.justia.com/977/09/salsa-and-97709873.html) | Third-party summary: SALSA, SALSA Scheme Ltd, UK, filed 2023-07-25, registered 2024-08-08, covering "computer software for use in collecting, compiling, storing, registering… and collaborating" and software design "relating to health and safety assessments, audits, accreditations and food safety compliance". SALSA SYSTEMS (Salsa Systems, Inc., US; goods not shown). Registries blocked. |
| 6 Language | Inconclusive (no negatives found) | 2026-09-25 | Reviewer assessment | As above. A listener test should confirm that PL and EN listeners hear "food" before "dance". |
| 7 Confusing similarity | Risk (medium) | 2026-09-25 | rows 1, 5 | The UK SALSA food-safety software mark is the nearest in goods (software touching food). Dance, streaming, nonprofit CRM and payroll uses are lighter. |
| 8 Social handles | Pending (SE: Risk) | 2026-09-25 | [@salsa.appoficial](https://www.instagram.com/salsa.appoficial/), [@salsalatam](https://www.instagram.com/salsalatam/), [@salsalive.app](https://www.instagram.com/salsalive.app/), [@salsaapp.asia](https://www.instagram.com/salsaapp.asia/) (all via SE) | The live-streaming "Salsa App" holds many regional handles (@salsa.appoficial with 9,052 followers, @salsalatam, @salsa.usa, @salsaapp.asia). The exact @salsa was not seen. Try `getsalsa`, `salsa.pl`, `eatsalsa`. |

---

##### `Pretzel` (top 3)

- **Concept:** A pretzel is dough twisted until it holds its shape. The app twists your recipe (swaps, portions, rebalancing, PRD §8.3–§8.6) until it fits your plan, and shows every turn it made (PRD §5 principle 10). Playful and a little indulgent, and the knot is a strong icon.
- **Pronunciation:** PL [ˈprɛtsɛl] "PRET-sel", the same sound as the Polish word *precel*. EN /ˈprɛtsəl/ "PRET-sul". A Pole who hears it may write "precel"; an English speaker writes "pretzel".
- **Meaning and connotations:** the baked knot, known across Europe (DE *Brezel*, FR *bretzel*, PL *precel*). "Twisted into a pretzel" = contorted (mild). No rude, body or medical meanings known (reviewer assessment).
- **Positioning line:** "Pretzel. We twist your recipe until it fits." / "Pretzel – przepis skręcony pod Twoje makro."
- **Store title:** "Pretzel: Meal Planner & Macros" (30 characters, at the limit) or "Pretzel: Meal Planner" (21).
- **Food hint / D/S:** clear / suggestive (arbitrary for software).
- **Catchiness:** 4/5.
- **Distinctiveness note (classes 9, 42, 44):** arbitrary for nutrition software and advice; descriptive only for bakery goods (30) and bakery or restaurant services (43). Of the three, it has the strongest footing. A US PRETZEL registration covers downloadable language-learning software (class 9); both are "downloadable software", so an attorney should judge whether the different purposes allow coexistence.
- **Main risks:** the US PRETZEL software registration; pretzel chains own the store search term; @pretzel.app is taken; the long store title uses all 30 characters.

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk (lighter) | 2026-09-25 | [Wetzel's Pretzels](https://apps.apple.com/us/app/wetzels-pretzels/id1637424029), [Auntie Anne's Rewards](https://play.google.com/store/apps/details?id=com.auntieannes.pretzelperks&hl=en_US), [Pretzel AI (GitHub)](https://github.com/pretzelai/pretzelai), [GetPretzel (GitHub)](https://github.com/GetPretzel/Pretzel) | Category query `"Pretzel" app "meal planner" OR nutrition OR recipes OR macros`: the summary says the results "don't appear to contain any information about an app specifically called 'Pretzel'". Food uses are pretzel chains (Wetzel's, Auntie Anne's, Philly Pretzel Factory, Ben's). Software: Pretzel AI ("modern replacement for Jupyter Notebooks"), GetPretzel ("stock take application"), a Mac shortcuts app. |
| 2 App Store (PL/US/GB) | Pending (SE: Risk, lighter) | 2026-09-25 | [Pretzel Rated](https://apps.apple.com/us/app/pretzel-rated/id6758898111), [Philly Pretzel Factory](https://apps.apple.com/us/app/philly-pretzel-factory/id1185574639), [Ben's Pretzels](https://apps.apple.com/us/app/bens-pretzels/id1181066695) | A movie and TV rating social app; chain ordering and rewards apps. No nutrition app. |
| 3 Google Play | Pending (SE: Risk, lighter) | 2026-09-25 | [Pretzel POS](https://play.google.com/store/apps/details?id=au.com.swifti&hl=en_US), [Wetzel's Pretzels](https://play.google.com/store/apps/details?id=com.wetzels.app&hl=en_US) | "Pretzel POS – A complete hospitality point-of-sale system for cafes, restaurants and food trucks"; chains; a game. |
| 4 Domains | Pending (SE: Risk for variants) | 2026-09-25 | RDAP blocked; [@pretzel.io (via SE)](https://www.instagram.com/pretzel.io/) | Query `"pretzel.app" OR "getpretzel.com" OR "pretzel.io" OR "pretzel.com"`: pretzelai.app is in use by Pretzel AI (per the summary); an Instagram account @pretzel.io describes a shopping app (whether it uses the pretzel.io domain is unverified); a GitHub organisation "GetPretzel" exists (getpretzel.com itself was not seen). Nothing for pretzel.com or pretzel.app. Check first: pretzel.app, getpretzel.com, eatpretzel.com, pretzel.pl. |
| 5 Trademarks | Pending (SE: Risk) | 2026-09-25 | [Justia: PRETZEL 86953904](https://trademarks.justia.com/869/53/pretzel-86953904.html), [Justia: PRETZEL THERAPEUTICS 88856373](https://trademarks.justia.com/888/56/pretzel-88856373.html) | Third-party summary: PRETZEL, Pretzel, Inc., "filed in March 2016 and registered in October 2017" (reg. 5312372), "covering downloadable software for skill improvement and skill sharing, particularly for practicing foreign languages". PRETZEL THERAPEUTICS (engineered proteins, class 5). Registries blocked. |
| 6 Language | Inconclusive (no negatives found) | 2026-09-25 | Reviewer assessment | The PL spelling split (*precel*). |
| 7 Confusing similarity | Risk (medium) | 2026-09-25 | rows 3, 5 | Same-name class-9 software in language learning and a hospitality POS. Nothing in nutrition. |
| 8 Social handles | Pending (SE: Risk) | 2026-09-25 | [@pretzel.app](https://www.instagram.com/pretzel.app/), [@pretzel.io](https://www.instagram.com/pretzel.io/), [@pretzelized](https://www.instagram.com/pretzelized/) (via SE) | "Pretzel Rated (@pretzel.app)" holds that variant; @pretzel.io is a shopping app; many snack brands. The exact @pretzel was not seen. Try `getpretzel`, `pretzel.pl`, `eatpretzel`. |

---

##### `Donut` (top 3)

- **Concept:** The PRD promise is "eat what you feel like eating, matched to your plan" (PRD §1). A donut is the food a diet app forbids; here it fits. The name says "no guilt" without ever saying guilt (PRD §5, no moralizing). Round, cheerful and instantly drawable.
- **Pronunciation:** PL [ˈdɔnut] "DO-nut" (the everyday Polish word is *donat*). EN /ˈdoʊnʌt/ "DOH-nut". Spellable after one hearing; British English also writes "doughnut".
- **Meaning and connotations:** EN: the fried ring; UK slang "you donut" = a mild "you silly"; "doing donuts" (car stunts). PL: known as *donat* or *donut*. No medical meaning (reviewer assessment).
- **Positioning line:** "Donut. Yes, it fits." / "Donut – tak, to też się zmieści."
- **Store title:** "Donut: Meal Planner & Macros" (28 characters).
- **Food hint / D/S:** clear / suggestive (arbitrary for software).
- **Catchiness:** 5/5.
- **Distinctiveness note (classes 9, 42, 44):** arbitrary for nutrition software, so strong in principle. But "Donut" is already a well-known software brand in 9/42 (Donut for Slack, used by "20,000+ companies"), and DONUT marks exist in class 9 (a vehicle-software application) and 41 (Donut Media). An attorney must assess whether "software" goods with different purposes are similar enough to block.
- **Main risks:** Donut for Slack (donut.com, app.donut.io); the positioning bet of naming a nutrition platform after a treat (the PO's call, §8.6.3); "I Deserve a Donut", a weight-loss devotional app; the donut/doughnut spelling split.

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk (lighter category, strong brand) | 2026-09-25 | [donut.com](https://www.donut.com/), [Slack Marketplace](https://app.slack.com/apps/A11MJ51SR-donut) | "Donut is an employee experience platform that helps you automate and scale people programs, right in Slack"; "used by 20,000+ companies"; "raised $12 million from Accel and the Slack Fund". Category query `"Donut" app "meal planner" OR recipes OR nutrition`: the summary says "there doesn't appear to be a specific app called 'Donut'". |
| 2 App Store (PL/US/GB) | Pending (SE: Risk) | 2026-09-25 | [Donut Inc.](https://apps.apple.com/us/app/donut-inc/id1666146982), [I Deserve a Donut](https://apps.apple.com/us/app/i-deserve-a-donut/id529567174), [Dunkin'](https://apps.apple.com/us/app/dunkin/id1056813463) | A shop-simulation game; "I Deserve a Donut" (per the summary, "a weight loss support app containing 32 sets of questions and 150+ Bible verses", a small nutrition-adjacent namesake); donut-shop apps. |
| 3 Google Play | Pending (SE: Risk, lighter) | 2026-09-25 | [DONUT](https://play.google.com/store/apps/details?id=com.tiongnam.donut_flutter&hl=en_US), [Donut Time](https://play.google.com/store/apps/details?id=com.storefrontconsumer.donut.time&hl=en_US) | A delivery-driver management app; shop ordering apps. |
| 4 Domains | Pending (SE: Risk) | 2026-09-25 | [donut.com](https://www.donut.com/), [app.donut.io](https://app.donut.io/), [getdonut.ai](https://getdonut.ai/) | donut.com = Donut for Slack; app.donut.io = its web dashboard; getdonut.ai = a trading tool. Nothing surfaced for donut.app, getdonut.com or donut.pl. Check first: donut.app, eatdonut.com, donutapp.com, donut.pl. |
| 5 Trademarks | Pending (SE: Risk) | 2026-09-25 | [Justia: DONUT LAB 98936152](https://trademarks.justia.com/989/36/donut-98936152.html), [Justia: DONUT 87441489](https://trademarks.justia.com/874/41/donut-87441489.html), [Justia: DONUTS 85801950](https://trademarks.justia.com/858/01/donuts-85801950.html) | DONUT LAB, Donut Lab Development OÜ, filed 2025-01-03, "downloadable software for vehicle operation, control, diagnostic, and communication"; DONUT, Donut Media (reg. 5390018), entertainment; DONUTS, Donuts Inc. (reg. 4502837), domain-name registration. The Slack company's own marks did not surface. Registries blocked. |
| 6 Language | Risk (mild) | 2026-09-25 | Reviewer assessment | UK "you donut"; donut/doughnut spelling. |
| 7 Confusing similarity | Risk (medium-high) | 2026-09-25 | rows 1, 5 | A well-known SaaS with the identical name in 9/42; a weight-loss devotional app. |
| 8 Social handles | Pending (SE: Risk) | 2026-09-25 | [@donut_app](https://www.instagram.com/donut_app/), [@donut.ai](https://www.instagram.com/donut.ai/), [@donutmedia](https://www.instagram.com/donutmedia/), [@donut_lab](https://www.instagram.com/donut_lab/) (via SE) | @donut_app, @donut.ai (the Slack company), @donutmedia (2M, cars), @donut_lab. The exact @donut was not seen. Try `donut.pl`, `eatdonut`, `donutplanner`. |

---

##### `Pickle` (alternate)

- **Concept:** Pickling is the original meal prep: make it once, eat it all week (PRD §5, meal prep as a first-class feature). And the app gets you out of a pickle when a recipe doesn't fit your numbers.
- **Pronunciation:** PL [ˈpiklɛ] "PI-kle" (Poles know *pikle*). EN /ˈpɪkəl/ "PIK-ul". Spellable after one hearing.
- **Meaning and connotations:** EN "in a pickle" = in trouble; "pickled" = drunk (slang). **DE *Pickel* = pimple** (a skin and body word, C3/C5, mild). App stores are full of pickleball. Also a Python serialisation module (reviewer knowledge).
- **Store title:** "Pickle: Meal Planner & Macros" (29 characters).
- **Food hint / D/S:** clear / suggestive. **Catchiness:** 5/5.
- **Distinctiveness note:** arbitrary for software but diluted: several PICKLE marks already exist in 9/42.
- **Main risks:** Pickle.ph (a healthy meal-plan service with calorie-controlled, macro-balanced plans); the DE meaning; crowded software marks.

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk (serious) | 2026-09-25 | [pickle.ph](https://pickle.ph/), [pickle.ph meal plans](https://pickle.ph/meal-plans/) | "Since 2015, Pickle Healthy Food Delivery has been redefining nutrition with its chef-prepared, nutritionist-approved meal plans"; "Every meal is calorie-controlled, macro-balanced"; plans named "Signature", "Lean and Clean", "Performance"; a calorie calculator (Metro Manila). The category query found no Pickle meal-planner app. |
| 2 App Store | Pending (SE: Risk, lighter) | 2026-09-25 | [Pickle: Rent & Lend Fashion](https://apps.apple.com/us/app/pickle-rent-lend-fashion/id1551736097), [Play Pickle](https://apps.apple.com/us/app/play-pickle/id6738210884), [Pickle Pro](https://apps.apple.com/us/app/pickle-pro/id6744969406) | Fashion rental; pickleball. |
| 3 Google Play | Pending (SE: Risk, lighter) | 2026-09-25 | [Pickle](https://play.google.com/store/apps/details?id=com.pickle_app), [Pickle - A simple note](https://play.google.com/store/apps/details?id=com.afn.pickle&hl=en), [Chicken N Pickle](https://play.google.com/store/apps/details?id=com.thanx.chickennpickle&hl=en_US) | A money-management app, a notes app, an AI reel maker, pickleball venues. |
| 4 Domains | Pending (SE: Risk for variants) | 2026-09-25 | [app.getpickle.ai](https://app.getpickle.ai/home), [shoponpickle.com](https://help.shoponpickle.com/en/articles/14442965-app-feature-faqs) | getpickle.ai (AI avatars) and shoponpickle.com (fashion) are in use. The summary said pickle.io is "a flexible cloud management platform" (no URL shown; unverified). Check first: pickle.app, getpickle.com, eatpickle.com, pickle.pl. |
| 5 Trademarks | Pending (SE: Risk) | 2026-09-25 | [uspto.report: PICKLE 99448059](https://uspto.report/TM/99448059), [Justia: PICKLEPAY 90380383](https://trademarks.justia.com/903/80/picklepay-90380383.html), [Justia: DESIGN PICKLE 90222910](https://trademarks.justia.com/902/22/design-90222910.html) | PICKLE (Pickle, Inc.): "online non-downloadable software for generating and utilizing virtual avatars"; PICKLEPAY: downloadable payment software; DESIGN PICKLE: PaaS for design services; PICKLEGRAM (Computer & Software Products). Registries blocked. |
| 6 Language | Risk | 2026-09-25 | Reviewer assessment | DE *Pickel*; "in a pickle"; "pickled". |
| 7 Confusing similarity | Risk (medium-high) | 2026-09-25 | rows 1, 5 | A same-category meal-plan service and several software marks. |
| 8 Social handles | Pending (SE: Risk) | 2026-09-25 | [@getpickle](https://www.instagram.com/getpickle/), [@getpickle.ai](https://www.instagram.com/getpickle.ai/), [@pickle__com](https://www.instagram.com/pickle__com/) (via SE) | @getpickle is a farm-to-jar pickles brand; @getpickle.ai (Instagram and TikTok) is Pickle AI. The exact @pickle was not seen. Try `pickle.pl`, `eatpickle`, `pickleplanner`. |

---

##### `Handful` (alternate)

- **Concept:** A handful is the oldest portion guide there is (palm, fist, handful). The app turns any recipe into portions you can picture, and keeps weekly planning manageable. It is the only shortlisted word about portions rather than a specific food.
- **Pronunciation:** PL [ˈxantful] "HAND-ful" with a Polish [x] for "h". EN /ˈhændfʊl/ "HAND-fool". A Pole might write "hendful" after hearing it.
- **Meaning and connotations:** EN "a handful" = a small amount; "he's a handful" = hard to manage (mild negative); handful.com is a sports-bra brand that plays on the word (a body innuendo in EN, mild C3/C5). PL: no meaning.
- **Store title:** "Handful: Meal Planner & Macros" (30 characters, at the limit).
- **Food hint / D/S:** moderate / borderline. **Catchiness:** 3/5.
- **Distinctiveness note:** borderline. For nutrition advice (44) and portion-aware software (9), "handful" alludes to portion size, so an examiner could see it as describing a feature. Weaker than a specific food name.
- **Main risks:** the food hint is weaker than the PO asked for; the sports-bra brand and @handful; borderline descriptiveness.

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk (lighter) | 2026-09-25 | [handful.com](https://handful.com/pages/faq), [Healthy Handfuls](https://www.foodprocessing.com/new-food-products/product/11358088/healthy-handfuls-llc) | handful.com: per the summary, "a private, direct-to-consumer women's activewear brand founded in 2006" (sports bras). "Healthy Handfuls", organic kids' snacks. The category query found no Handful meal or nutrition app. |
| 2 App Store | Pending (SE: Risk, lighter) | 2026-09-25 | [Handful: Daily Gratitude](https://apps.apple.com/fr/app/handful-daily-gratitude/id6761936798) | A gratitude-journal app (developer "Beech Hill Fitness Inc." per the summary). No food app. |
| 3 Google Play | Pending (SE: Inconclusive) | 2026-09-25 | — | Only unrelated near names (Handly, Handy). **Not evidence of availability.** |
| 4 Domains | Pending (SE: Risk for .com) | 2026-09-25 | [handful.com](https://handful.com/pages/contact) | handful.com is in use (sports bras). Nothing surfaced for handful.app, gethandful.com or handful.io. Check first: handful.app, gethandful.com, handfulapp.com, handful.pl. |
| 5 Trademarks | Pending (SE: Inconclusive) | 2026-09-25 | — | The mirror-site search returned no HANDFUL mark. The sports-bra brand may hold one (unverified). **Not a clearance.** |
| 6 Language | Risk (mild) | 2026-09-25 | Reviewer assessment | "A handful" (hard to manage); the bra-brand innuendo. |
| 7 Confusing similarity | Risk (low-medium) | 2026-09-25 | rows 1–2 | Activewear (class 25) and a gratitude app (class 9). Nothing in nutrition software. |
| 8 Social handles | Pending (SE: Risk) | 2026-09-25 | [@handful](https://www.instagram.com/handful/), [@handfulenglish](https://www.instagram.com/handfulenglish/) (via SE) | @handful is the sports-bra brand (43K). Try `handful.app`, `gethandful`, `handful.pl`. |

---

##### `Kettle` (only if the top 5 all fail)

- **Concept:** The kettle starts every kitchen routine, and it nods to kettlebells, which suits the fitness-minded wedge (PRD §3).
- **Pronunciation:** PL [ˈkɛtlɛ] "KET-le"; the word is not everyday Polish (PL *czajnik*). EN /ˈkɛtəl/ "KET-ul".
- **Meaning and connotations:** "a different kettle of fish"; "the pot calling the kettle black". No negatives known in PL, DE, FR, ES or IT (reviewer assessment).
- **Store title:** "Kettle: Meal Planner & Macros" (29). **Food hint / D/S:** moderate (a kitchen object, not a food) / suggestive. **Catchiness:** 3/5.
- **Distinctiveness note:** arbitrary for software; KETTLE is crowded in food (class 29).
- **Main risks:** "Kettle: AI Fitness Coach" (health-adjacent class 9); KettlePay holds @kettle; food marks in class 29.

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk | 2026-09-25 | [Justia: KETTLE BRAND 86975998](https://trademarks.justia.com/869/75/kettle-86975998.html), [TikTok @kettlebrand](https://www.tiktok.com/@kettlebrand?lang=en) | Kettle Brand chips (Snyder's-Lance), Kettle & Fire broth, Kettle Studio air-fried chips (Mumbai). The category query found no Kettle meal-planner app. |
| 2 App Store | Pending (SE: Risk) | 2026-09-25 | [Kettle: AI Fitness Coach](https://apps.apple.com/gb/app/kettle-ai-fitness-coach/id6762473970), [KettlePay](https://apps.apple.com/us/app/kettlepay/id6747727129) | An AI workout coach (health and fitness, adjacent); crypto payments; kettlebell planners. |
| 3 Google Play | Pending (SE: Risk, lighter) | 2026-09-25 | [Kettle – Connect.Heatup.Meet](https://play.google.com/store/apps/details?id=com.kettleweb.app&hl=en_US), [The Kettle To Go](https://play.google.com/store/apps/details?id=com.owner.thekettle&hl=en_GB) | Professional networking; café ordering. |
| 4 Domains | Pending (SE: Risk) | 2026-09-25 | [kettle.io](https://kettle.io/), [app.ourkettle.com](https://app.ourkettle.com/) | kettle.io = a development and design agency; ourkettle.com = a login app. Nothing for kettle.com, kettle.app or getkettle.com. Check first: kettle.app, getkettle.com, kettle.pl. |
| 5 Trademarks | Pending (SE: Risk, food classes) | 2026-09-25 | [Justia: KETTLE BRAND](https://trademarks.justia.com/869/75/kettle-86975998.html), [uspto.report: KETTLE & FIRE 88712175](https://uspto.report/TM/88712175) | KETTLE BRAND (chips); KETTLE & FIRE ("Meats and Processed Food Products"); KETTLE COLLECTION (Kerry Group). No software mark surfaced. |
| 6 Language | Inconclusive | 2026-09-25 | Reviewer assessment | Low PL familiarity. |
| 7 Confusing similarity | Risk (medium) | 2026-09-25 | rows 2, 5 | A fitness-coach app and food marks. |
| 8 Social handles | Pending (SE: Risk) | 2026-09-25 | [@kettle](https://www.instagram.com/kettle/) (via SE) | "Kettle Pay (@kettle)". Try `getkettle`, `kettle.pl`. |

---

##### `Tapas` (not recommended)

- **Concept:** Small plates and lots of variety: your week in portions. **Pronunciation:** PL [ˈtapas]; EN /ˈtæpəs/ "TAP-us". **Store title:** "Tapas: Meal Planner & Macros" (28). **Catchiness:** 4/5. **Food hint / D/S:** clear / suggestive, but descriptive for food service in ES.
- **Distinctiveness note:** descriptive in Spanish for restaurant services (43) and arguably allusive to small portions (44); a major TAPAS brand exists in 9/41/45.
- **Main risk:** Tapas (comics and novels) by Tapas Media, a major app with a US TAPAS registration.

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk (heavy, outside food) | 2026-09-25 | [Tapas – Comics and Novels](https://apps.apple.com/us/app/tapas-comics-and-novels/id578836126), [MealTap](https://play.google.com/store/apps/details?id=com.meeltap.app&hl=en) | "Over 75,000 talented creators… publish their work on Tapas". Category query: no Tapas meal app; "MealTap" and "TapThePlate" meal planners sound close. |
| 2 App Store | Pending (SE: Risk) | 2026-09-25 | as row 1 | Tapas comics; "La Prensa Tacos & Tapas", "Riserva Bar & Tapas". |
| 3 Google Play | Pending (SE: Risk) | 2026-09-25 | [Tapas](https://play.google.com/store/apps/details?id=com.tapastic&hl=en_US), [Trending Tapas](https://play.google.com/store/apps/details?id=com.foodbooking.ttapas&hl=en_US) | Comics; restaurant ordering. |
| 4 Domains | Pending | 2026-09-25 | — | Not searched this session. |
| 5 Trademarks | Pending (SE: Risk) | 2026-09-25 | [uspto.report: TAPAS 88453377](https://uspto.report/TM/88453377), [Trademarkia: Tapas Media](https://www.trademarkia.com/owners/tapas-media-inc) | TAPAS covers "on-line social networking services… in the field of literature and comics"; Tapas Media also holds TAPASTRY and TAPAS STORIES YOU CRAVE. |
| 6 Language | Risk | 2026-09-25 | Reviewer assessment | Descriptive in ES. |
| 7 Confusing similarity | Risk (high) | 2026-09-25 | rows 1, 5 | A major same-name app. |
| 8 Social handles | Pending | 2026-09-25 | — | Not searched. |

---

##### `Nacho` (not recommended)

- **Concept:** "Nacho average meal plan"; a sharing plate. **Pronunciation:** PL [ˈnaxɔ] if read as Polish, [ˈnatʃɔ] if known; EN /ˈnɑːtʃoʊ/ "NAH-cho". **Store title:** "Nacho: Meal Planner & Macros" (28). **Catchiness:** 5/5. **Food hint / D/S:** clear / suggestive.
- **Distinctiveness note:** arbitrary for software; also a common Spanish nickname (Ignacio).
- **Main risks:** Poles read "ch" as [x]; the pun works only in English; tied to Tex-Mex junk food (C4, C7); @nacho is a 15M personal account.

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk (lighter) | 2026-09-25 | [Nacho Shack](https://apps.apple.com/us/app/nacho-shack/id6476187840), [NachoNacho](https://connect.nachonacho.com/) | Restaurant apps; NachoNacho (a software marketplace); Nacho King (Tex-Mex manufacturer, PH). No Nacho meal app. |
| 2 App Store | Pending (SE: Risk, lighter) | 2026-09-25 | as row 1 | Nacho Shack, Restaurant Nacho's, Nacho Daddy, Tio Nacho, Nacho Map. |
| 3 Google Play | Pending (SE: Risk) | 2026-09-25 | [Nacho (wallet)](https://play.google.com/store/apps/details?id=com.impervious.nacho), [Movie Nachos](https://play.google.com/store/apps/details?id=com.alexpournaras.nachos) | A "non-custodial wallet" for Spaces handles; a movie app. |
| 4 Domains | Pending (SE: Inconclusive) | 2026-09-25 | [nachoapps.dev](https://www.nachoapps.dev/) | nachoapps.dev and nachonacho.com in use; nothing for nacho.app, getnacho.com, nacho.io or nacho.com. |
| 5 Trademarks | Pending (SE: Risk, low) | 2026-09-25 | [Trademarkia: Nacho Mamas Inc.](https://www.trademarkia.com/owners/nacho-mamas-inc) | NACHO MAMAS in class 030 and class 042. |
| 6 Language | Risk | 2026-09-25 | Reviewer assessment | PL "ch" = [x]. |
| 7 Confusing similarity | Risk (medium) | 2026-09-25 | rows 1–3 | Restaurants and small software. |
| 8 Social handles | Pending (SE: Risk) | 2026-09-25 | [@nacho](https://www.instagram.com/nacho/), [TikTok @nacho_official](https://www.tiktok.com/@nacho_official) | "Nacho 'Miguelito' Mendoza (@nacho)", 15M followers. |

---

##### `Melon` (not recommended)

- **Concept:** Round, fresh, friendly. **Pronunciation:** PL [ˈmɛlɔn]; EN /ˈmɛlən/ "MEL-un". **Store title:** "Melon: Meal Planner & Macros" (28). **Catchiness:** 4/5. **Food hint / D/S:** clear / suggestive.
- **Distinctiveness note:** arbitrary for software, but a MELON filing already covers a weight-loss tracking app.
- **Main risks:** that filing; Kakao's Melon music platform; near Mela (recipe app, §3.2) and Melo AI (diet coach, §3.4); slang ("melons" = breasts; UK "melon" = head).

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk (serious) | 2026-09-25 | [Justia: Melon Innovations LLC](https://trademark.justia.com/owners/melon-innovations-llc-5086829/) | Per the summary, Melon Innovations LLC "filed a trademark for downloadable mobile application featuring software for recommending and tracking user weight loss habits". The category query found no Melon meal-planner app. |
| 2 App Store | Pending (SE: Risk) | 2026-09-25 | [Melon: Sandbox](https://apps.apple.com/us/app/melon-sandbox/id1610874732), [Melon - Business Travel](https://apps.apple.com/us/app/melon-business-travel/id1569321067), [Melon Music](https://apps.apple.com/us/app/melon-music/id6767312118) | A game, business travel, a music player. |
| 3 Google Play | Pending (SE: Risk, heavy) | 2026-09-25 | [멜론 (Melon)](https://play.google.com/store/apps/details?id=com.iloen.melon&hl=en_US) | Kakao's Melon music platform (KR); several other Melon apps. |
| 4 Domains | Pending | 2026-09-25 | — | Not searched. |
| 5 Trademarks | Pending (SE: Risk) | 2026-09-25 | as row 1; [Trademarkia: Kakao Entertainment](https://www.trademarkia.com/owners/kakao-entertainment-corp) | The weight-loss app filing; Kakao Entertainment's 13 marks (whether MELON is among them was not shown). |
| 6 Language | Risk | 2026-09-25 | Reviewer assessment | Slang as above (C3). |
| 7 Confusing similarity | Risk (high) | 2026-09-25 | rows 1, 3 | Same-category filing; near Mela and Melo AI. |
| 8 Social handles | Pending | 2026-09-25 | — | Not searched. |

---

##### `Bagel` (not recommended)

- **Concept:** A round classic. **Pronunciation:** PL [ˈbaɡɛl] (PL *bajgiel*); EN /ˈbeɪɡəl/ "BAY-gul". **Store title:** "Bagel: Meal Planner & Macros" (28). **Catchiness:** 4/5. **Food hint / D/S:** clear / suggestive.
- **Distinctiveness note:** arbitrary for software, but "Bagel" is the distinctive half of a well-known dating brand.
- **Main risks:** Coffee Meets Bagel; the PL/EN pronunciation split; a weak product metaphor (C4).

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk (heavy, outside food) | 2026-09-25 | [Coffee Meets Bagel](https://apps.apple.com/us/app/coffee-meets-bagel-dating-app/id6502307144) | A major dating app ("over 150 million matches" per the summary); bagel chains. The category query found no Bagel meal app. |
| 2 App Store | Pending (SE: Risk) | 2026-09-25 | [Einstein Bros Bagels](https://apps.apple.com/us/app/einstein-bros-bagels/id1405128897) | CMB; Einstein Bros, Brooklyn Bagel, Old School Bagel, Bagel Market NY. |
| 3 Google Play | Pending (SE: Risk) | 2026-09-25 | [Coffee Meets Bagel](https://play.google.com/store/apps/details?id=io.cmbus.app&hl=en_US), [B Bagel](https://play.google.com/store/apps/details?id=com.bbagel.app&hl=en_US) | CMB; bagel shops. |
| 4 Domains | Pending | 2026-09-25 | — | Not searched. |
| 5 Trademarks | Pending | 2026-09-25 | — | Not searched. |
| 6 Language | Risk | 2026-09-25 | Reviewer assessment | Pronunciation split. |
| 7 Confusing similarity | Risk (medium-high) | 2026-09-25 | row 1 | CMB. |
| 8 Social handles | Pending | 2026-09-25 | — | Not searched. |

---

##### `Pesto` (not recommended)

- **Concept:** A few good things ground together: your recipe plus your numbers. **Pronunciation:** PL [ˈpɛstɔ]; EN /ˈpɛstoʊ/ "PES-toh". **Store title:** "Pesto: Meal Planner & Macros" (28). **Catchiness:** 5/5. **Food hint / D/S:** clear / suggestive.
- **Distinctiveness note:** arbitrary for software in EN and PL; descriptive in IT (a sauce).
- **Main risk:** a same-category recipe and meal-planner app of the same name on the Polish App Store.

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk (serious) | 2026-09-25 | [Pesto - Recipe App (App Store PL)](https://apps.apple.com/pl/app/pesto-recipe-app/id6504192769) | "Pesto is an all-in-one recipe organizer, shopping list, and meal planner" with "an integrated weekly meal planner" and unit conversion. |
| 2 App Store | Pending (SE: Risk, serious) | 2026-09-25 | as row 1; [Pesto Restaurant](https://apps.apple.com/us/app/pesto-restaurant/id6761471614), [Pesto Family](https://apps.apple.com/us/app/pesto-family/id1574466794) | The recipe app (PL store); restaurant and delivery apps; "Pesto Kitchen". |
| 3 Google Play | Pending (SE: Risk) | 2026-09-25 | [pesto](https://play.google.com/store/apps/details?id=com.brenqo.pesto), [Pesto Assistant](https://play.google.com/store/apps/details?id=com.useappility.pesto&hl=en_US) | An app named "pesto" (category not shown); a Greek voice assistant. |
| 4 Domains | Pending | 2026-09-25 | — | Not searched. |
| 5 Trademarks | Pending | 2026-09-25 | — | Not searched. |
| 6 Language | Inconclusive | 2026-09-25 | Reviewer assessment | Descriptive in IT. |
| 7 Confusing similarity | Risk (high) | 2026-09-25 | row 1 | Identical name, same category, same launch market. |
| 8 Social handles | Pending | 2026-09-25 | — | Not searched. |

---

##### `Caper` (not recommended)

- **Concept:** A small bud with big flavour; "a caper" is also a playful adventure. **Pronunciation:** PL [ˈkapɛr] "KA-per"; EN /ˈkeɪpər/ "KAY-per". **Store title:** "Caper: Meal Planner & Macros" (28). **Catchiness:** 4/5. **Food hint / D/S:** clear / suggestive.
- **Distinctiveness note:** arbitrary for software, but Instacart's Caper is a known grocery-technology brand.
- **Main risks:** Instacart Caper Carts (grocery shopping tech sits next to our shopping list, PRD §8); the PL/EN pronunciation split; "caper" = heist.

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk (serious-adjacent) | 2026-09-25 | [caper.ai](https://www.caper.ai/), [Instacart Caper Carts](https://company.instacart.com/enterprise-platform/connected-stores/caper-carts) | "Caper Carts are high-tech, AI-enabled grocery carts"; "more than 100 cities across 15 states", Coles in Australia, "Morrisons in the UK coming later this year". |
| 2 App Store | Pending (SE: Risk) | 2026-09-25 | [Capper App](https://apps.apple.com/us/app/capper-app/id6756785474) | A sports-betting "capper" app; mystery games. |
| 3 Google Play | Pending (SE: Risk) | 2026-09-25 | [Caper App Store](https://play.google.com/store/apps/details?id=com.caper_cloud_app&hl=en_US), [Caper Xpresion](https://play.google.com/store/apps/details?id=com.caper_store&hl=en) | Logistics and courier apps. |
| 4 Domains | Pending (SE: Risk) | 2026-09-25 | [caper.ai](https://www.caper.ai/) | caper.ai is in use (Instacart). Others not searched. |
| 5 Trademarks | Pending | 2026-09-25 | — | Not searched. |
| 6 Language | Risk | 2026-09-25 | Reviewer assessment | Pronunciation split; "caper" = heist. |
| 7 Confusing similarity | Risk (high) | 2026-09-25 | row 1 | Grocery technology. |
| 8 Social handles | Pending | 2026-09-25 | — | Not searched. |

---

##### `Gravy` (not recommended)

- **Concept:** "It's all gravy" = all good; the extra that makes a meal. **Pronunciation:** PL [ˈɡravɨ] "GRA-vy"; EN /ˈɡreɪvi/ "GRAY-vee". **Store title:** "Gravy: Meal Planner & Macros" (28). **Catchiness:** 4/5. **Food hint / D/S:** clear / suggestive.
- **Distinctiveness note:** arbitrary for software; crowded in fintech.
- **Main risk:** Gravy Analytics, subject of a 2025 FTC order on selling sensitive location data including visits to health locations. A privacy-scandal namesake is a poor fit for an app that holds health-adjacent data.

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk (reputational) | 2026-09-25 | [FTC press release](https://www.ftc.gov/news-events/news/press-releases/2025/01/ftc-finalizes-order-prohibiting-gravy-analytics-venntel-selling-sensitive-location-data), [Gravy Analytics (Wikipedia)](https://en.wikipedia.org/wiki/Gravy_Analytics) | "FTC Finalizes Order Prohibiting Gravy Analytics, Venntel from Selling Sensitive Location Data", including "visits to health-related locations" (finalised 2025-01-14 per the summary). |
| 2 App Store | Pending (SE: Risk) | 2026-09-25 | [Gravy: Homebuying for renters](https://apps.apple.com/us/app/gravy-homebuying-for-renters/id1572896190), [Gravy Rewards](https://apps.apple.com/us/app/gravy-rewards/id6742050220), [GravyWork](https://apps.apple.com/us/app/gravywork/id1576705364) | Fintech and gig-work apps. |
| 3 Google Play | Pending (SE: Risk) | 2026-09-25 | [Gravy](https://play.google.com/store/apps/details?id=com.gravy&hl=en_US), [All Gravy](https://play.google.com/store/apps/details?id=com.buttersolutions.butter&hl=en_US) | The same homebuying app; an employee app. |
| 4 Domains | Pending | 2026-09-25 | — | Not searched. |
| 5 Trademarks | Pending | 2026-09-25 | — | Not searched. |
| 6 Language | Risk | 2026-09-25 | Reviewer assessment | PL reading; "gravy train" (easy money). |
| 7 Confusing similarity | Risk (medium-high) | 2026-09-25 | rows 1–3 | Data-broker namesake; fintech apps. |
| 8 Social handles | Pending | 2026-09-25 | — | Not searched. |

#### 6.8.4 Domain strategy for real-word names

A 5–7 letter dictionary .com is almost always registered, and for the top names the search engine already found other businesses on related domains (salsapp.io, salsaapp.io, pretzelai.app, donut.com, app.donut.io, getpickle.ai, handful.com). Real food words also make natural "verb + noun" domains, which are often still open. Once RDAP is reachable, check these in this order, then decide with the owner (§8.6.2):

| Name | 1st | 2nd | 3rd | 4th (PL market) |
|---|---|---|---|---|
| Salsa | salsa.app | getsalsa.com | eatsalsa.com | salsa.pl |
| Pretzel | pretzel.app | getpretzel.com | eatpretzel.com | pretzel.pl |
| Donut | donut.app | eatdonut.com | donutapp.com | donut.pl |
| Pickle | pickle.app | getpickle.com | eatpickle.com | pickle.pl |
| Handful | handful.app | gethandful.com | handfulapp.com | handful.pl |

All are **Pending**; none has been checked on a registry. Remember that .app requires HTTPS (HSTS preloaded), that a registry 404 does not guarantee a standard price (short dictionary words are often premium-priced), and that the .com of a dictionary word may be for sale at a broker price.

### 6.7 Session 3: short-and-catchy shortlist (superseded 2026-09-25, PO: "nothing from proposals")

> **Superseded 2026-09-25 (PO: "nothing from proposals").** §6.7.1–§6.7.4 below are kept exactly as written, with all their evidence. The session-3 top 3 (Zubo, Kazu, Dozo) and alternates (Nimbo, Gobo) are no longer recommended. They are replaced by §6.8. Where §6.7 says "current", read "current as of session 3".

Twelve names, all 4–5 letters and 2 syllables. All checks are dated **2026-09-25**. Store, domain, trademark and handle checks are **Pending** for every name because the official sources were egress-blocked (§5.1). The bracketed text is the search-engine indication only. **N** = C10 international neutrality and **Catch** = C11 catchiness (§2.3), both reviewer assessments.

#### 6.7.1 Check matrix

| Name | S/L | Type | 1 Competitors / similar | 2 App Store | 3 Google Play | 4 .com | 4 .app | 4 .io | 4 .pl | 5 Trademarks (EUIPO / TMview / UPRP / WIPO / USPTO / UKIPO) | 6 Language PL/EN | 7 Confusing similarity | 8 Social handles | N | Catch |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Zubo** | 2/4 | Coinage | Inconclusive: no food, nutrition or recipe use seen; non-food uses (2008 EA game, child-tracking app, a Filipino restaurant) | Pending (Risk: ride-hailing "Zubo", "Zubo: Learn to Read for Kids", "Zubo! Driver") | Pending (Risk: Zubo ride-hailing, Zubo Conductor, Zubo pasajero) | Pending (Inconclusive) | Pending (Inconclusive) | Pending (Inconclusive) | Pending (Inconclusive) | Pending (Risk, low: US ZUBO abandoned; US ZUBO footwear application, 2024) | Risk (mild): *zub* = tooth in CS, SK, HR, SR, RU, UK | Risk: exact-name class-9 apps in mobility and kids' education; none in food | Pending (Risk: Instagram @zubo.app is in use) | 4 | 4 |
| **Kazu** | 2/4 | JP word | Risk (low): restaurants, a "Kazu" spice brand, recipe channels | Pending (Risk: KAZU Public Radio, "Kazu", "Kazu: Positive Affirmations", Sushi Kazu) | Pending (Risk: KAZU real estate, Kazu Bot) | Pending (Inconclusive) | Pending (Inconclusive) | Pending | Pending | Pending (Risk, low: KRAZY FOR KAZU'S, US food mark) | Risk: Poles may hear "Kaziu" (familiar form of Kazimierz); EN "kazoo" | Risk: exact-name class-9 apps outside food | Pending (Risk: @kazu held by an individual) | 3 | 4 |
| **Dozo** | 2/4 | JP word | Risk: Dozo Food Products (IN, instant grain meals); DOZO dog food (JP); restaurants | Pending (Risk: "dozo" (JP); Dozo LLP developer) | Pending (Risk: Dozo Marketplace, Dozo Live, dōzo gift, Dozo (Bhutan), Dozo Izakaya) | Pending (Inconclusive) | Pending (Risk: dozo.app in use) | Pending | Pending (Inconclusive) | Pending (Risk: US DOZO, classes 5 and 34, hemp gummies and vaporizers; DOZO PERKS application, classes 25 and 5) | Risk: PL *doza* / *dozować* (dose, to dispense); EN "doze" | Risk: supplement and hemp marks in class 5 | Pending (Risk: @dozobrands; X @dozoapp) | 4 | 4 |
| **Nimbo** | 2/5 | Coinage (PT *nimbo*) | Risk: restaurant loyalty app, ERP apps, satellite maps; a search summary mentioned a patient-management system (unverified) | Pending (Risk: Nimbo Labs developer) | Pending (Risk: NIMBO restaurant app, Nimbo Móvil, Nimbo Yazılım) | Pending (Inconclusive) | Pending (Inconclusive) | Pending (Inconclusive) | Pending (Inconclusive) | Pending (Inconclusive: no exact mark seen; NIMBOO, NIMBAO near) | Inconclusive: PT "rain cloud"; EN rhymes "bimbo", "nimby" | Risk (medium): possible health-software namesake (unverified) | Pending (Risk: @nimbo_oficial, @therealnimbo and others) | 4 | 4 |
| **Gobo** | 2/4 | JP word / EN lighting term | Risk: "Gobo: Order & Sell Local" (restaurants and markets, NI); @gobo.sa healthy food delivery (Jeddah) | Pending (Risk: Gobo: Order & Sell Local, Gobo Box Office, Omino Gobo) | Pending (Risk: Gobo, Gobo Carrier, GOBO Inventory) | Pending (Risk: gobo.com shows a page titled "Gobo") | Pending (Inconclusive) | Pending (Risk: gobo.io in use) | Pending (Inconclusive) | Pending (Risk: GOBO application in India, class 42, third-party site) | Inconclusive: EN "gob" (slang for mouth) | Risk (medium-high): food-ordering and healthy-food uses | Pending (Risk: @wearegobo, @its.gobo, @gobo.sa) | 4 | 4 |
| **Bibim** | 2/5 | KR word | Risk: many Korean restaurants (class 43) | Pending (Risk: BiBim student-community app; Bibimbox) | Pending (Risk: BiBim) | Pending (Inconclusive) | Pending (Risk: bibim.app in use) | Pending | Pending | Pending (Risk, low: US BIBIM class 43 cancelled 2022; BIBIMBOWL class 43 live) | Inconclusive: reads as "the bibimbap word" | Risk (low): restaurants | Pending (Risk: restaurant accounts) | 3 | 3 |
| **Zumo** | 2/4 | ES word | Risk: Zumo juice and smoothie bar chain across Europe | Pending (Risk: Zumo, Zumo Thai, zūmo Radar (Garmin)) | Pending (Risk: Zumo, Zumo crypto wallet, Zumo car rental, ZumoDO) | Pending (Inconclusive) | Pending (Inconclusive) | Pending | Pending (Inconclusive) | Pending (Risk, high: an EU ZUMO mark for payment software per a search summary; US ZUMO applications and registrations) | Risk: ES "juice"; Spaniards say "THOO-mo" | Risk (high): EU class-9 mark; ZUMO vape brand | Pending (Risk: @zumo in use) | 3 | 5 |
| **Kumo** | 2/4 | JP word | Risk: KumoHealth app; sushi restaurants | Pending (Risk: Kumo – Offline Friend, Mitsubishi "kumo cloud", Kumo AI Video) | Pending (Risk: Comfort by Mitsubishi Electric (kumo cloud), KumoHealth) | Pending (Inconclusive) | Pending | Pending | Pending | Pending (Risk: KUMO STATION, Mitsubishi Electric US) | Inconclusive: no negatives found | Risk (high): Mitsubishi "kumo cloud" in class 9; kumo.ai | Pending (Risk: many) | 4 | 4 |
| **Panko** | 2/5 | JP food word | Risk: Panko, a Polish maker of pest-monitoring products; breadcrumb brands | Pending (Risk: Panko Alerts, Hot Sauce and Panko, Panko and Sushi) | Pending (Risk: Panko, Panko Easy) | Pending (Inconclusive) | Pending | Pending | Pending (Inconclusive) | Pending (Risk: PANKO CONCEPT EU filing, goods unknown) | Risk: the PL pest-control brand; an ingredient word | Risk (medium): PL namesake | Pending (Risk) | 3 | 4 |
| **Gumbo** | 2/5 | EN food word | Risk: Gumbo, a digital-health company; restaurants | Pending (Risk: Gumbo App, Gumbo 94.9, Gumbo King) | Pending (Risk: Gumbo (health), GUMBO off-road (PL), Gumbo social) | Pending (Risk: gumbo.com in use) | Pending | Pending | Pending | Pending (Inconclusive) | Risk: PL says "GOOM-bo", EN "GUM-bo"; a "Gumbo Brands" account selling "Disposables" (product type not shown) | Risk (high): same-name digital-health app | Pending (Risk: @gumbo_app taken) | 3 | 4 |
| **Mogu** | 2/4 | JP onomatopoeia | Risk: Mogu Mogu drinks; MÓGU Mushrooms supplements | Pending (Risk: "Mogu Exercise", a chewing tracker for meals; MÓGŪ restaurant) | Pending (Risk: MOGU, MOGU Tours) | Pending (Risk: mogu.com used by MOGU Inc., per a search summary) | Pending | Pending | Pending | Pending (Risk: US MOGU, MÓGU MUSHROOMS (supplements), MOGU MOGU (drinks)) | Risk: RU *могу* = "I can", which Poles recognise | Risk (high): chewing tracker in the eating space | Pending (Risk: many) | 2 | 5 |
| **Pappa** | 2/5 | IT word | Risk: pizza restaurants, Pappa Pastificio | Pending (Risk: Pappa Pizza, Pappa AB developer, Papa Care) | Pending (Risk: Pappa.ai, Papa Care) | Pending (Inconclusive) | Pending | Pending | Pending | Pending (Inconclusive) | Risk: IT baby food, *pappa pronta* ("spoon-fed"); SV/NO "dad" | Risk (medium): "Papa" senior-care apps sound identical | Pending (Risk: @pappa in use) | 3 | 3 |

#### 6.7.2 Scores (C1–C7, C10, C11) and ranking

Scores run from 1 (poor) to 5 (strong) and are the reviewer's assessment of the evidence above. **C8 (domains and handles) and C9 (trademarks) are Pending for every name** and are not scored. "Evidence weight" summarises the search-engine Risk findings; it is a triage signal, not a legal assessment. The rank weighs the C1–C7 sum, C10, C11 and the evidence weight together, so a higher sum does not always mean a higher rank. **This is a recommendation for further investigation, not a selection.**

| Rank | Name | S/L | C1 | C2 | C3 | C4 | C5 | C6 | C7 | Sum /35 | C10 /5 | C11 /5 | Evidence weight (SE) | Further investigation? |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **Zubo** | 2/4 | 5 | 5 | 4 | 3 | 5 | 5 | 5 | 32 | 4 | 4 | **Medium:** exact-name apps in ride-hailing and kids' reading (class 9); Instagram @zubo.app in use; **no food, nutrition or health use seen** | **Yes, top 3** |
| 2 | **Kazu** | 2/4 | 4 | 4 | 4 | 4 | 5 | 5 | 5 | 31 | 3 | 4 | **Medium:** exact-name apps in radio, real estate and affirmations; food uses limited to restaurants and a spice brand; @kazu taken; the PL "Kaziu" echo | **Yes, top 3** |
| 3 | **Dozo** | 2/4 | 4 | 4 | 3 | 5 | 4 | 5 | 5 | 30 | 4 | 4 | **Medium-high:** US DOZO marks for hemp gummies and vaporizers and a supplements application (class 5); dozo.app in use; many Japanese apps; a dog-food brand | **Yes, top 3** |
| 4 | **Nimbo** | 2/5 | 4 | 5 | 4 | 3 | 5 | 5 | 5 | 31 | 4 | 4 | **Medium:** restaurant-loyalty and ERP apps; one unverified health-software mention | Yes, alternate |
| 5 | **Gobo** | 2/4 | 4 | 5 | 4 | 3 | 5 | 5 | 5 | 31 | 4 | 4 | **Medium-high:** a food-ordering super-app and a healthy-food delivery service use the exact name; gobo.com and gobo.io in use | Yes, alternate |
| 6 | Bibim | 2/5 | 3 | 4 | 5 | 4 | 5 | 5 | 4 | 30 | 3 | 3 | Medium: restaurants (class 43), a student app, bibim.app in use | Only if the top 5 all fail |
| 7 | Kumo | 2/4 | 3 | 5 | 5 | 3 | 5 | 5 | 5 | 31 | 4 | 4 | **High:** Mitsubishi Electric "kumo cloud" app and KUMO STATION mark (class 9); KumoHealth | No |
| 8 | Zumo | 2/4 | 3 | 5 | 4 | 3 | 4 | 5 | 4 | 28 | 3 | 5 | **High:** an EU ZUMO class-9 software mark (per a search summary); a European juice-bar chain; a vape brand | No |
| 9 | Mogu | 2/4 | 3 | 4 | 3 | 5 | 4 | 5 | 5 | 29 | 2 | 5 | **High:** "Mogu Exercise" chewing tracker; MÓGU MUSHROOMS supplements mark; MOGU Inc. (listed company) | No |
| 10 | Panko | 2/5 | 3 | 4 | 3 | 4 | 5 | 5 | 4 | 28 | 3 | 4 | Medium-high: a Polish pest-monitoring brand called Panko; an EU "PANKO CONCEPT" filing | No |
| 11 | Pappa | 2/5 | 3 | 4 | 3 | 3 | 5 | 5 | 5 | 28 | 3 | 3 | Medium: "Papa" senior-care apps; baby-food meaning in IT | No |
| 12 | Gumbo | 2/5 | 3 | 3 | 4 | 4 | 4 | 5 | 4 | 27 | 3 | 4 | **High:** a same-name digital-health app; a "Gumbo Brands" disposables account (product type not shown) | No |

**Catchiness in one line each (C11):**
- **Zubo (4):** a buzzy "Z" into two round vowels; says itself after one hearing; looks bold as a four-letter icon. Not a 5 only because it carries no hook or image.
- **Kazu (4):** crisp K-Z contrast and an open "-zu" ending; "kazoo" makes it playful in English.
- **Dozo (4):** mirrored "o-o" vowels give it bounce, and it invites you in ("help yourself").
- **Nimbo (4):** soft and light; "-mbo" gives it rhythm. One consonant more than the others.
- **Gobo (4):** repeated "o" and a "go" start, friendly and toy-like.
- **Bibim (3):** fun doubled "bi", but the closed "-im" ending lands flat, and people may stumble over the stress.
- **Zumo (5):** the punchiest: "zoom" plus "-o", with an energy-drink feel.
- **Kumo (4):** smooth and calm rather than punchy.
- **Mogu (5):** *mogu-mogu* is literally "munch-munch"; cute and memorable.
- **Panko (4):** crunchy "-nk-" in the middle; playful.
- **Pappa (3):** doubled but ordinary, and reads as "papa".
- **Gumbo (4):** fun and bouncy, but a little clumsy ("gum").

**Trade-offs in brief:**
- **Zubo** is the cleanest short name found: coined, spelled and said the same way in PL and EN ("ZOO-boh"), with no food, nutrition or health namesake in any search. The cost: it means nothing, so the store descriptor and brand work must carry the product ("Zubo: Meal Planner", 18 characters). Same-name apps exist in ride-hailing and kids' reading, and the Instagram handle @zubo.app is already in use. A mild tooth echo (*zub*) exists in Czech, Slovak, BCS and Russian. For a food app that is about chewing, not medicine, but a listener test should confirm it.
- **Kazu** has a hidden hook: *kazu* is Japanese for "number", which fits "we do the maths, you cook" without saying diet. It is crisp and easy in PL and EN. The cost: many exact-name apps in other fields, and to Polish ears it can sound like **"Kaziu"**, the familiar form of the old-fashioned name Kazimierz. Given the PO's rejection of Polish-sounding names, **this needs a PL listener test before going further.**
- **Dozo** has the warmest meaning (*dōzo*, "please, help yourself", said when offering food), which matches "eat what you feel like" (PRD §1). The cost: US DOZO marks cover hemp gummies and vaporizers, and a "DOZO PERKS" application covers dietary supplements (class 5). That is an unwelcome neighbour for a nutrition app (C5). dozo.app is in use. PL *doza* (dose) is a mild medical echo.
- **Nimbo** (alternate) is soft and neutral, with no food namesake. But one search summary mentioned a patient-management system called Nimbo (unverified), and it has no meaning hook.
- **Gobo** (alternate) is very easy and friendly, but the exact name is used by a local food-ordering super-app and by a healthy-food delivery account. That is close to our category.
- **Zumo and Mogu** are the catchiest (5), but both have high-weight conflicts: an EU software mark and a juice-bar chain for Zumo; a meal-chewing tracker and a supplements mark for Mogu. They are shown because the PO asked for catchiness, not recommended.
- **A pattern to note:** six of the twelve are Japanese words (Kazu, Dozo, Gobo, Kumo, Panko, Mogu). Japanese romanisation reads the same in PL and EN, which is why they pass C2. If two of them reach the final, the PO may want to decide whether a Japanese flavour suits a Polish-launched nutrition brand (§8.5.3).

#### 6.7.3 Per-name evidence (session 3)

All checks are dated **2026-09-25**. "SE" means a WebSearch result that could not be opened. Domains: RDAP was blocked for every TLD, so every domain status is **Pending**. A 4-letter .com is almost always registered, so each block lists realistic variants to check first (`get<name>.com`, `<name>.app`, `<name>app.com`, `<name>.pl`). They are unverified and must be checked by RDAP before any decision. Handles on Facebook, YouTube, X, Threads and LinkedIn could not be checked (no filtered search returned them, and Threads was not searchable in session 1) and are **Pending**, unless noted.

---

##### `Zubo` (top 3)

- **Concept:** A coined sound, not a word. A buzzy "Z" and a round, friendly "-bo" make it something you'd grab without thinking. It doesn't say diet, meal or AI, so it stretches to pantry, family and dietitian phases (PRD §13). The meaning comes from the product and the descriptor.
- **Pronunciation:** PL [ˈzubɔ] "ZU-bo". EN /ˈzuːboʊ/ "ZOO-boh". The same in both, and people can spell it after one hearing (a Pole writes "zubo"; an English speaker might try "zoobo", so the wordmark matters).
- **Meaning and connotations:** no dictionary meaning in PL, EN, DE, FR, ES, IT, PT, NL or SV (reviewer assessment). Echo: *zub* = tooth in Czech, Slovak, Croatian, Serbian, Russian and Ukrainian (Polish is *ząb*). That fits eating, but should be listener-tested. No slang found. Nothing medical or moralising (C5).
- **Positioning line:** "Your recipe. Your numbers. Zubo." / "Jedz, co lubisz. Zubo dopasuje resztę." ("Eat what you like. Zubo fits the rest.")
- **Store title:** "Zubo: Meal Planner" (18 characters).
- **Catchiness:** 4/5 (see §6.7.2).
- **Main risks:** exact-name apps in ride-hailing, driver and kids' reading (class 9); Instagram @zubo.app is in use; the tooth echo in some Slavic languages.

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Inconclusive | 2026-09-25 | [Zubo game (Fandom)](https://zubo.fandom.com/wiki/Zubo_(Game)), [zubogo.com](https://zubogo.com/), [@zubo.to (via SE)](https://www.instagram.com/zubo.to/), [zuno.fit](https://zuno.fit/) | SE: "Zubo (Game) \| Zubo Wiki" (EA, Nintendo DS, 2008); "Zubo: Smart App for Child Tracking and Safety"; "ZUBO.TO", a Filipino restaurant. Query `"Zubo" app OR brand food OR meal OR nutrition` returned **no** Zubo food or nutrition product; the nearest were Zuno (a fitness and nutrition app) and Zumub (sports-nutrition shop). |
| 2 App Store (PL/US/GB) | Pending (SE: Risk) | 2026-09-25 | [Zubo App](https://apps.apple.com/gh/app/zubo/id6742074745), [Zubo: Learn to Read for Kids](https://apps.apple.com/us/app/zubo-learn-to-read-for-kids/id6747403776), [Zubo! Driver](https://apps.apple.com/us/app/zubo-driver/id6749956894) | Store-filtered SE: a ride-hailing app, a kids' AI reading tutor, a driver app. No food app. The iTunes API is blocked; App Store Connect availability is an owner action. |
| 3 Google Play | Pending (SE: Risk) | 2026-09-25 | [Zubo](https://play.google.com/store/apps/details?id=com.zubo.ride), [Zubo Conductor](https://play.google.com/store/apps/details?id=zubo.io), [Zubo pasajero](https://play.google.com/store/apps/details?id=zubocliente.app.io&hl=en_US) | Ride-hailing and taxi apps. No food app. |
| 4 Domains .com / .app / .io / .pl | Pending (SE: Inconclusive) | 2026-09-25 | RDAP blocked; SE `"zubo.com" OR "zubo.app" OR "zubo.io" OR "zubo.pl"` | No site at those four surfaced; "zubo.io" appeared only as a Play package ID. zubogo.com is in use. **Not evidence of availability.** Check first: getzubo.com, zubo.app, zuboapp.com, zubo.pl. |
| 5 Trademarks | Pending (SE: Risk, low) | 2026-09-25 | [Trademarkia: ZUBO 77462177](https://www.trademarkia.com/zubo-77462177), [Justia: ZUBO 98431784](https://trademarks.justia.com/984/31/zubo-98431784.html) | Third-party pages: EA's US ZUBO (filed 2008-04-30) "ABANDONED - NO STATEMENT OF USE FILED"; a new US ZUBO application filed 2024-03-04 "for sneakers and footwear kits". No software, food or nutrition mark surfaced. Registries blocked. |
| 6 Language | Risk (mild) | 2026-09-25 | Reviewer assessment | The Slavic tooth echo as above. A native-speaker check is pending. |
| 7 Confusing similarity | Risk | 2026-09-25 | as rows 2–3 | Identical name on class-9 apps in mobility and education. Nothing in food or nutrition. "Zuno" (fitness and nutrition) is a sound-neighbour, low. |
| 8 Social handles | Pending (SE: Risk) | 2026-09-25 | [@zubo.app](https://www.instagram.com/zubo.app/), [@zubo.store](https://www.instagram.com/zubo.store/), [@zubo_zb](https://www.instagram.com/zubo_zb/), [TikTok @zubo.hr](https://www.tiktok.com/@zubo.hr) (all via SE) | **"Zubo (@zubo.app)" is in use on Instagram**, so that variant is gone. "Z U B O (@zubo_zb)" is a fashion account (41K per the SE summary). The exact @zubo was not seen. Try `getzubo`, `zubo.pl`, `zuboplanner`. |

---

##### `Kazu` (top 3)

- **Concept:** *Kazu* (数) is Japanese for "number". The app does the numbers (calories, macros, cost per portion) so you can cook what you want. The meaning is a hidden bonus. Most users will hear a short, crisp, friendly name.
- **Pronunciation:** PL [ˈkazu] "KA-zu". EN /ˈkɑːzuː/ "KAH-zoo". Spellable after one hearing, though English speakers may write "Kazoo".
- **Meaning and connotations:** JP "number"; also a common Japanese given-name element (Kazuo, Kazuki). EN: echoes "kazoo" (a toy instrument), which is playful. **PL: close to "Kaziu", the familiar vocative of Kazimierz** (an old-fashioned name); the "zi" is softer, but the resemblance is audible. No rude meanings found in the languages checked (reviewer assessment).
- **Positioning line:** "You cook. Kazu does the numbers." / "Ty gotujesz, Kazu liczy."
- **Store title:** "Kazu: Meal Planner" (18 characters).
- **Catchiness:** 4/5.
- **Main risks:** the "Kaziu" echo for the first market; many exact-name apps (radio, real estate, affirmations, a sushi bar); @kazu is held by an individual.

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk (low) | 2026-09-25 | [Kazu Authentic recipes](https://kazuauthentic.com/recipes/), [Kazu restaurant](https://kazu.restaurants-info.com/menu), [Kazu Recipes (YouTube)](https://www.youtube.com/channel/UCQLfZpJhJ6BVGPxyUCgIvFQ) | SE: "Kazu \| Recipes" (a spice and seasoning brand); a Kazu restaurant in Montreal; "Kazu Recipes" cooking channels. **No** Kazu food, nutrition or meal-planning app. |
| 2 App Store | Pending (SE: Risk) | 2026-09-25 | [KAZU Public Radio](https://apps.apple.com/us/app/kazu-public-radio-app/id979422850), [Kazu](https://apps.apple.com/us/app/kazu/id6756679772), [Kazu: Positive Affirmations](https://apps.apple.com/my/app/kazu-positive-affirmations/id6760725778), [Sushi Kazu](https://apps.apple.com/us/app/sushi-kazu/id6744416017) | Radio, an app whose category did not show, an AI affirmations app, a sushi-restaurant ordering app (Bad Nauheim, DE). |
| 3 Google Play | Pending (SE: Risk) | 2026-09-25 | [KAZU](https://play.google.com/store/apps/details?id=com.kazurealestate.kazu&hl=en_US), [Kazu Bot](https://play.google.com/store/apps/details?id=net.klymora.velnato.kazu.bot) | Real estate (El Salvador); a game. |
| 4 Domains | Pending (SE: Inconclusive) | 2026-09-25 | RDAP blocked; [kazu.org](https://www.kazu.org/contact) | kazu.org (public radio) is in use. The SE summary said kazu.com and kazu.app belong to the real-estate platform, **but no URL at those domains was shown**, so that is unverified. Check first: getkazu.com, kazu.app, kazuapp.com, kazu.pl. |
| 5 Trademarks | Pending (SE: Risk, low) | 2026-09-25 | [Trademarkia: KRAZY FOR KAZU'S](https://www.trademarkia.com/krazy-for-kazu-s-85278533) | "KRAZY FOR KAZU'S is a registered trademark (Registration #4298723)", described as food-related (CT, US). The SE also returned KAZOO (software), "Dead/Cancelled". No exact KAZU software mark surfaced. Registries blocked. |
| 6 Language | Risk | 2026-09-25 | Reviewer assessment | The "Kaziu" echo (PL). A PL listener test is needed. |
| 7 Confusing similarity | Risk | 2026-09-25 | as rows 2–3 | Identical name on several class-9 apps outside food. |
| 8 Social handles | Pending (SE: Risk) | 2026-09-25 | [@kazu](https://www.instagram.com/kazu/), [@kazu.makino](https://www.instagram.com/kazu.makino/?hl=en), [@kazu_official_](https://www.instagram.com/kazu_official_/) (via SE) | "KAZU \| Sander (@kazu)" holds the exact Instagram handle. Try `getkazu`, `kazu.app`, `kazu.pl`. |

---

##### `Dozo` (top 3)

- **Concept:** *Dōzo* (どうぞ) is what you say in Japanese when offering food: "please, go ahead, help yourself". The app says the same about the recipe you wanted: go ahead, it fits your plan. That is the core promise (PRD §1) in two syllables, and it is hospitable rather than preachy (PRD §5).
- **Pronunciation:** PL [ˈdɔzɔ] "DO-zo". EN /ˈdoʊzoʊ/ "DOH-zoh" (JP [doːzo]). Spellable after one hearing in both languages.
- **Meaning and connotations:** JP "please / go ahead / help yourself". EN: the first syllable echoes "doze" (sleepy), mild. **PL: echoes *doza* (a dose) and *dozować* (to dose or dispense)**, as in "doza leku" (a dose of medicine) and "dozownik" (a dispenser). The portion sense fits; the medicine sense is a mild C5 flag. No rude meanings found (reviewer assessment).
- **Positioning line:** "Dozo. Help yourself." / "Dozo – częstuj się."
- **Store title:** "Dozo: Meal Planner" (18 characters).
- **Catchiness:** 4/5.
- **Main risks:** US DOZO marks for hemp gummies and vaporizers, and a DOZO PERKS application for dietary supplements, both class 5 (an unwelcome neighbour for a nutrition app); dozo.app is in use; many Japanese "dozo" apps and restaurants; a Japanese dog-food brand.

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk | 2026-09-25 | [Dozo Food Products](https://dozofoodproducts.com/about/), [@dozo20_dogs (via SE)](https://www.instagram.com/dozo20_dogs/), [@dozodozonyc (via SE)](https://www.instagram.com/dozodozonyc/) | "Dozo Food Products" (Mumbai, since 1987): "2-minute nutritious meals" from ragi, jowar and amaranth. "DOZO(ドーゾ)", a low-allergen dog-food brand. Several Japanese restaurants (Charlotte, NYC, Toulouse). |
| 2 App Store | Pending (SE: Risk) | 2026-09-25 | [dozo（ドーゾ）](https://apps.apple.com/jp/app/dozo-%E3%83%89%E3%83%BC%E3%82%BE/id6708591529?l=en-US), [Dozo LLP developer](https://apps.apple.com/ci/developer/dozo-llp/id917205893?l=en) | A Japanese souvenir-shop app; a developer named Dozo LLP. |
| 3 Google Play | Pending (SE: Risk) | 2026-09-25 | [Dozo Marketplace](https://play.google.com/store/apps/details?id=com.dozo_app.dozo&hl=en_US), [Dozo Live](https://play.google.com/store/apps/details?id=com.dozo.live&hl=en_US), [dōzo gift](https://play.google.com/store/apps/details?id=li.yapp.app05A23784), [Dozo (Bhutan)](https://play.google.com/store/apps/details?id=bt.dcpl.dozo&hl=en_IN), [Dozo Izakaya](https://play.google.com/store/apps/details?id=com.chownow.dozoizakaya&hl=en_US) | A Japanese marketplace, a live-chat app, a gift service, Bhutan's "all-in-one" ride-hailing and delivery app, a restaurant. |
| 4 Domains | Pending (SE: Risk for .app) | 2026-09-25 | [GitHub: dozo.app](https://github.com/dozo-app), [X @dozoapp](https://x.com/dozoapp) | "dozo.app · GitHub" and "dozo.app (@dozoapp) / X"; the SE summary says dozo.app "is designed to help students stay focused" in class, so **dozo.app appears to be registered and in use** (unverified). Nothing surfaced for dozo.com, .io or .pl (the SE mixed in the DOZ.pl pharmacy app). Check first: getdozo.com, dozoapp.com, dozo.pl. |
| 5 Trademarks | Pending (SE: Risk) | 2026-09-25 | [uspto.report: DOZO 97460033](https://uspto.report/TM/97460033/APP20220618112443/), [Justia: DOZO PERKS 98725477](https://trademark.justia.com/987/25/dozo-98725477.html) | Third-party summaries: "DOZO is registered by LATRO INC." in class 005 ("herbal gummy supplements exclusively for use with Hemp…") and class 034 ("disposable oral vaporizers…"). "DOZO PERKS" filed 2024-08-29, classes 025 and 005 ("dietary and nutritional supplements"). None in 9, 29, 30, 42 per the summary. Registries blocked. |
| 6 Language | Risk (mild) | 2026-09-25 | Reviewer assessment | The *doza* and "doze" echoes above. |
| 7 Confusing similarity | Risk | 2026-09-25 | as rows 1, 3, 5 | Hemp and supplement marks (class 5) and Indian instant-meal products; many unrelated apps. |
| 8 Social handles | Pending (SE: Risk) | 2026-09-25 | [@dozobrands](https://www.instagram.com/dozobrands/), [@dozoclt](https://www.instagram.com/dozoclt/), [@thisisdozo_](https://www.instagram.com/thisisdozo_/) (via SE); X @dozoapp (row 4) | Many Dozo accounts; X `@dozoapp` is in use. The exact Instagram @dozo was not seen. |

---

##### `Nimbo` (alternate)

- **Concept:** From *nimbus* (a cloud, a halo) and "nimble": light, quick plans that move with you. Soft and friendly, with no diet or body meaning.
- **Pronunciation:** PL [ˈnimbɔ] "NIM-bo". EN /ˈnɪmboʊ/ "NIM-boh". Spellable after one hearing.
- **Meaning and connotations:** PT *nimbo* = a rain cloud (poetic). EN rhymes: "bimbo", and the "nimby" echo; both mild. No negatives found in PL, DE, FR, ES or IT (reviewer assessment).
- **Positioning line:** "Nimbo. Plans that keep up with you."
- **Store title:** "Nimbo: Meal Planner" (19 characters).
- **Catchiness:** 4/5.
- **Main risks:** many Nimbo businesses (ERP, telecom, satellite maps, a restaurant-loyalty app); one unverified mention of a Nimbo patient-management system for doctors (health, class 9/44).

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk | 2026-09-25 | [NIMBO (restaurant app)](https://play.google.com/store/apps/details?id=com.remarked.nimbo.app&hl=en_US), [nimbo.earth](https://nimbo.earth/earth-online/about-nimbo/) | "NIMBO … an app for three restaurants" (loyalty); Nimbo satellite basemaps (Kermap, FR). The Instagram-filtered SE summary also mentioned "a digital patient management system used by over 20,000 doctors" named Nimbo, **with no titled link** (weak evidence). |
| 2 App Store | Pending (SE: Risk) | 2026-09-25 | [Nimbo Labs developer](https://apps.apple.com/us/developer/nimbo-labs/id427868910) | A developer called Nimbo Labs (GPS-tracking apps); a "NIMBO AI" chatbot per the summary. |
| 3 Google Play | Pending (SE: Risk) | 2026-09-25 | [Nimbo Móvil](https://play.google.com/store/apps/details?id=com.avathartech.nimbomovil), [Nimbo Yazılım](https://play.google.com/store/apps/details?id=com.nimboyazilim) | ERP and business apps; the NIMBO restaurant app (row 1). |
| 4 Domains | Pending (SE: Inconclusive) | 2026-09-25 | RDAP blocked; [app.nimbo-x.com](https://app.nimbo-x.com/) | Nothing surfaced at nimbo.com, .app, .io or .pl; nimbo-x.com, nimbo.earth and nimbosync.com are in use. Check first: getnimbo.com, nimbo.app, nimbo.pl. |
| 5 Trademarks | Pending (SE: Inconclusive) | 2026-09-25 | [Justia: NIMBOO](https://trademarks.justia.com/982/00/nimboo-98200027.html), [Trademarkia: NIMBAO](https://www.trademarkia.com/nimbao-99498595) | No exact NIMBO mark surfaced. Near: NIMBOO (US application; luggage, furniture, toys), NIMBAO (US; clothing). **Not a clearance.** |
| 6 Language | Inconclusive | 2026-09-25 | Reviewer assessment | As above. |
| 7 Confusing similarity | Risk (medium) | 2026-09-25 | row 1 | Resolve whether a health-software "Nimbo" exists (registry and store search). |
| 8 Social handles | Pending (SE: Risk) | 2026-09-25 | [@therealnimbo](https://www.instagram.com/therealnimbo/?hl=en), [@nimbo_oficial](https://www.instagram.com/nimbo_oficial/), [@nimbomovil](https://www.instagram.com/nimbomovil/), [@nimboberlin](https://www.instagram.com/nimboberlin/) (via SE) | Many Nimbo accounts; the exact @nimbo was not seen. |

---

##### `Gobo` (alternate)

- **Concept:** Two things at once: *gobō* is Japanese burdock root (a real food), and a gobo is the stencil that makes a spotlight project a shape. The app puts your food in the spotlight and shapes it to your plan. Mostly it is just a happy, toy-like sound.
- **Pronunciation:** PL [ˈɡɔbɔ] "GO-bo". EN /ˈɡoʊboʊ/ "GOH-boh". Spellable after one hearing.
- **Meaning and connotations:** as above. EN: "gob" is slang for mouth (and "to gob" = to spit, BrE); mild. Gobo is also a Fraggle Rock character (reviewer knowledge, not searched). No negatives known in PL, DE, FR, ES or IT (reviewer assessment).
- **Positioning line:** "Gobo. Your food, in the spotlight."
- **Store title:** "Gobo: Meal Planner" (18 characters).
- **Catchiness:** 4/5.
- **Main risks:** "Gobo: Order & Sell Local" is a food-ordering super-app (restaurants, markets); @gobo.sa is a healthy-food delivery service; gobo.com and gobo.io are in use; a GOBO filing in India in class 42.

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk | 2026-09-25 | [Gobo: Order & Sell Local](https://play.google.com/store/apps/details?id=com.gobo&hl=en_US), [@gobo.sa (via SE)](https://www.instagram.com/gobo.sa/), [@bar.gobo (via SE)](https://www.instagram.com/bar.gobo/?hl=en) | "Gobo is a super app for your city": order "from restaurants, market, pharmacy" (Nicaragua). "Gobo - جوبو (@gobo.sa)": per the summary, "a food delivery service in Jeddah offering healthy options". A wine bar in Vancouver. The category query `"Gobo" app food…` returned only burdock recipes. |
| 2 App Store | Pending (SE: Risk) | 2026-09-25 | [Gobo: Order & Sell Local](https://apps.apple.com/us/app/gobo-order-sell-local/id6504262676), [Gobo Box Office](https://apps.apple.com/us/app/gobo-box-office/id6470237867), [Omino Gobo](https://apps.apple.com/us/app/omino-gobo/id800905067) | Local ordering; ticketing; a stage-lighting tool. |
| 3 Google Play | Pending (SE: Risk) | 2026-09-25 | [Gobo Carrier](https://play.google.com/store/apps/details?id=com.gobo.carrier&hl=en_US), [GOBO Inventory](https://play.google.com/store/apps/details?id=com.goboInventory.android&gl=US) | The same local-ordering platform's courier and store apps. |
| 4 Domains | Pending (SE: Risk) | 2026-09-25 | [gobo.com](https://gobo.com/), [gobo.io](https://www.gobo.io/), [gobo.social](https://gobo.social/) | gobo.com shows a page titled "Gobo" (the summary calls it a minimal landing page); gobo.io is "Gobo · Build, brand, and monetize your app ecosystem"; gobo.social is an MIT social-media aggregator. Nothing for .app or .pl. Check first: getgobo.com, gobo.app, gobo.pl. |
| 5 Trademarks | Pending (SE: Risk) | 2026-09-25 | [registerkaro: GOBO 5100801](https://www.registerkaro.in/trademark-details/gobo-5100801) | Third-party summary: "The trademark GOBO is registered under Trademark Class 42" (India; status and owner not shown). Registries blocked. |
| 6 Language | Inconclusive | 2026-09-25 | Reviewer assessment | "gob" echo; the Fraggle Rock character. |
| 7 Confusing similarity | Risk (medium-high) | 2026-09-25 | rows 1–3 | Food ordering and healthy-food delivery under the identical name. |
| 8 Social handles | Pending (SE: Risk) | 2026-09-25 | [@wearegobo](https://www.instagram.com/wearegobo/), [@its.gobo](https://www.instagram.com/its.gobo/), [@gobo.sa](https://www.instagram.com/gobo.sa/) (via SE) | Many Gobo accounts; the exact @gobo was not seen. |

---

##### `Bibim` (next in line)

- **Concept:** Korean *bibim* = "mixed", the first half of bibimbap. The app mixes what you love with what you need.
- **Pronunciation:** PL [ˈbibim] "BI-bim". EN /ˈbiːbɪm/ "BEE-bim". Spellable after one hearing.
- **Meaning and connotations:** strongly tied to Korean cuisine (C7) and used by many Korean restaurants. No negatives found (reviewer assessment).
- **Positioning line:** "Mix what you love with what you need."
- **Store title:** "Bibim: Meal Planner" (19 characters).
- **Catchiness:** 3/5 (fun doubled "bi", but a flat ending).
- **Main risks:** crowded by restaurants (class 43); bibim.app in use; reads as a Korean-cuisine brand.

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk | 2026-09-25 | [bibimpdx.com](https://bibimpdx.com/), [bibimclt.com](https://www.bibimclt.com/) | Korean restaurants (Portland, Charlotte) and others; "BiBimSnack" Korean snack boxes. |
| 2 App Store | Pending (SE: Risk) | 2026-09-25 | [BiBim](https://apps.apple.com/my/app/bibim/id6670340531), [Bibimbox](https://apps.apple.com/us/app/bibimbox/id6749148572) | An international-student community app; a restaurant app. |
| 3 Google Play | Pending (SE: Risk) | 2026-09-25 | [BiBim](https://play.google.com/store/apps/details?id=site.bibim.app&hl=en_US) | The same student app. |
| 4 Domains | Pending (SE: Risk for .app) | 2026-09-25 | [bibim.app](https://www.bibim.app/en) | "BIBIM \| Open-Source AI Agent for Revit & ArchiCAD" at bibim.app. Nothing for bibim.com, .io or .pl. Check first: getbibim.com, bibim.pl. |
| 5 Trademarks | Pending (SE: Risk, low) | 2026-09-25 | [Justia: BIBIM 86473501](https://trademarks.justia.com/864/73/bibim-86473501.html), [Justia: BIBIMBOWL](https://trademarks.justia.com/854/92/bibimbowl-85492479.html) | US BIBIM, class 043, "cancelled on February 4, 2022"; BIBIMBOWL, class 043, active per the summary. |
| 6 Language | Inconclusive | 2026-09-25 | Reviewer assessment | As above. |
| 7 Confusing similarity | Risk (low) | 2026-09-25 | row 1 | Restaurants only (class 43). |
| 8 Social handles | Pending (SE: Risk) | 2026-09-25 | [@bibim_pdx](https://www.instagram.com/bibim_pdx/), [@bibim_charlotte](https://www.instagram.com/bibim_charlotte/), [@b_i_b_i_m_](https://www.instagram.com/b_i_b_i_m_/) (via SE) | Many restaurant accounts. |

---

##### `Zumo` (not recommended)

- **Concept:** Spanish *zumo* = juice: all the good stuff, squeezed in. The punchiest name found ("zoom" plus "-o").
- **Pronunciation:** PL [ˈzumɔ] "ZU-mo". EN /ˈzuːmoʊ/ "ZOO-moh". In Spain, "z" is [θ], so Spaniards say "THOO-mo".
- **Meaning and connotations:** ES "juice" (descriptive for drinks). Garmin uses "zūmo" for motorcycle navigators. No rude meanings found.
- **Store title:** "Zumo: Meal Planner" (18 characters). **Catchiness:** 5/5.
- **Main risks:** an EU ZUMO mark for payment software (class 9) per a search summary; the Zumo juice-bar chain across Europe; a ZUMO vape brand; many same-name apps.

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk | 2026-09-25 | [Zumo (Wikipedia)](https://en.wikipedia.org/wiki/Zumo), [The Zumo Group](https://www.thezumogroup.com/) | "Zumo, a juice and smoothie bar chain in Europe with over 100 establishments in 13 countries" (summary); "The Zumo Group, independent leader in sustainable retail". |
| 2 App Store | Pending (SE: Risk) | 2026-09-25 | [Zumo](https://apps.apple.com/us/app/zumo/id6753967313), [Zumo Thai](https://apps.apple.com/us/app/zumo-thai/id1668729047), [zūmo Radar](https://apps.apple.com/us/app/z%C5%ABmo-radar/id6449474035) | A drone-community app, a restaurant, a Garmin companion app. |
| 3 Google Play | Pending (SE: Risk) | 2026-09-25 | [Zumo](https://play.google.com/store/apps/details?id=com.zumo.android&hl=en_US), [Zumo crypto](https://play.google.com/store/apps/details?id=com.zumopay.core&hl=en_US&gl=US), [Zumo car rental](https://play.google.com/store/apps/details?id=com.zumoapp.app&hl=en), [ZumoDO](https://play.google.com/store/apps/details?id=com.zumodo&hl=en_NZ) | Quotes, crypto wallet, car rental, task manager. |
| 4 Domains | Pending (SE: Inconclusive) | 2026-09-25 | [zumo.co.uk](https://zumo.co.uk/), [app.zumo.tech](https://app.zumo.tech/downloadapp/) | zumo.co.uk and zumo.tech are in use (digital assets). The SE summary attributed zumo.app and zumo.pl to other apps, but no URLs at those domains were shown (unverified). |
| 5 Trademarks | Pending (SE: Risk, high) | 2026-09-25 | [Justia: ZUMO 88380257](https://trademarks.justia.com/883/80/zumo-88380257.html), [Trademarkia: ZUMO 88047580](https://trademark.trademarkia.com/zumo-88047580.html) | Summary: "ZUMO is a registered trade mark of Blockstar Developments Limited (EU TM Reg No 17996331)", covering "computer software for facilitating payment transactions"; a US ZUMO application (88380257). A US ZUMO (NG Sports; swim goggles, class 9) is "REGISTERED". Third-party sources only. |
| 6 Language | Risk | 2026-09-25 | Reviewer assessment | Descriptive in Spanish for drinks; the "THOO-mo" reading in Spain. |
| 7 Confusing similarity | Risk (high) | 2026-09-25 | rows 1, 5, 8 | EU class-9 mark; juice chain; vape brand. |
| 8 Social handles | Pending (SE: Risk) | 2026-09-25 | [@zumo](https://www.instagram.com/zumo/), [TikTok @zumo_official](https://www.tiktok.com/@zumo_official), [@zumovape](https://www.instagram.com/zumovape/) (via SE) | The exact Instagram @zumo is in use; "Official ZUMO (@zumovape)" sells disposable vapes. |

---

##### `Kumo` (not recommended)

- **Concept:** Japanese *kumo* = cloud: light, always with you.
- **Pronunciation:** PL [ˈkumɔ] "KU-mo". EN /ˈkuːmoʊ/ "KOO-moh". **Catchiness:** 4/5. **Store title:** "Kumo: Meal Planner" (18).
- **Meaning and connotations:** JP "cloud" (also "spider", written differently). "Kumo" was also Microsoft's pre-Bing search codename (per the SE). No negatives found.
- **Main risks:** Mitsubishi Electric's "kumo cloud" app and KUMO STATION mark (class 9); KumoHealth; kumo.ai.

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk | 2026-09-25 | [KumoHealth](https://play.google.com/store/apps/details?id=com.drkumo.kumohealth&hl=en_US), [Kumo Japanese Cuisine](https://apps.apple.com/ca/app/kumo-japanese-cuisine/id1576578875) | A health app; restaurant ordering apps. |
| 2 App Store | Pending (SE: Risk) | 2026-09-25 | [Kumo – Offline Friend](https://apps.apple.com/us/app/kumo-offline-friend/id6756067305), [kumo cloud](https://apps.apple.com/us/app/kumo-cloud/id998509713), [Kumo AI Video](https://apps.apple.com/us/app/kumo-ai-video-generator/id6753729055) | "Comfort is the new kumo", Mitsubishi Electric's HVAC app; others. |
| 3 Google Play | Pending (SE: Risk) | 2026-09-25 | [Comfort by Mitsubishi Electric](https://play.google.com/store/apps/details?id=com.mehvac.kumocloud&hl=en_US) | Package `com.mehvac.kumocloud`. |
| 4 Domains | Pending (SE: Risk) | 2026-09-25 | [kumo.ai](https://kumo.ai/) | kumo.ai in use (the SE title reads "NVIDIA Structured Data and Graph Models"). Nothing for .com, .app, .io or .pl. |
| 5 Trademarks | Pending (SE: Risk) | 2026-09-25 | [Justia: KUMO STATION](https://trademarks.justia.com/868/56/kumo-86856871.html) | "KUMO STATION Trademark of Mitsubishi Electric US, Inc. - Registration Number 5438716". |
| 6 Language | Inconclusive | 2026-09-25 | Reviewer assessment | No negatives found. |
| 7 Confusing similarity | Risk (high) | 2026-09-25 | rows 2–5 | A large brand's class-9 app and mark. |
| 8 Social handles | Pending (SE: Risk) | 2026-09-25 | [@kumoscarsdale](https://www.instagram.com/kumoscarsdale/?hl=en), [@thekumocollective](https://www.instagram.com/thekumocollective/), [TikTok @kumodev](https://www.tiktok.com/@kumodev) | Many accounts. |

---

##### `Panko` (not recommended)

- **Concept:** Japanese breadcrumbs (*pan* = bread, *ko* = crumbs): crunchy, playful, food-positive.
- **Pronunciation:** PL [ˈpankɔ] "PAN-ko". EN /ˈpæŋkoʊ/ or /ˈpɑːŋkoʊ/. **Catchiness:** 4/5. **Store title:** "Panko: Meal Planner" (19).
- **Meaning and connotations:** an ingredient word (descriptive for class 30 breadcrumbs). **PL: "Panko" is a Polish brand of pest-monitoring products** (a bad association for food). PL *pan* = Mr.
- **Main risks:** the Polish pest-control namesake; an EU "PANKO CONCEPT" filing; restaurant apps.

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk | 2026-09-25 | [Panko Polska (Facebook, via SE)](https://www.facebook.com/pankopolska/), [panko.digital](https://panko.digital/) | "Panko - Producent środków monitorujących obecność szkodników" (a maker of pest-monitoring products; Radom, since 1993 per the summary); an Australian software agency. |
| 2 App Store | Pending (SE: Risk) | 2026-09-25 | [Panko Alerts](https://apps.apple.com/us/app/panko-alerts/id6761290712), [Hot Sauce and Panko](https://apps.apple.com/us/app/hot-sauce-and-panko/id1568185986), [Panko and Sushi](https://apps.apple.com/gb/app/panko-and-sushi-macclesfield/id6737588308) | Alerts, restaurant ordering. |
| 3 Google Play | Pending (SE: Risk) | 2026-09-25 | [Panko](https://play.google.com/store/apps/details?id=jp.co.isub.panko&hl=en_US&gl=US), [Panko Easy](https://play.google.com/store/apps/details?id=com.hhy.game.panko&hl=en_US&gl=US) | A group-divider utility; a puzzle game. |
| 4 Domains | Pending (SE: Inconclusive) | 2026-09-25 | RDAP blocked | Nothing surfaced at panko.com, .app, .io or .pl. |
| 5 Trademarks | Pending (SE: Risk) | 2026-09-25 | [Trademark Elite: PANKO CONCEPT 018273183](https://www.trademarkelite.com/europe/trademark/trademark-detail/018273183/PANKO-CONCEPT) | "PANKO CONCEPT EU Trademark" filed by Projectico Oy; goods not shown. |
| 6 Language | Risk | 2026-09-25 | row 1 | The PL pest-control association. |
| 7 Confusing similarity | Risk (medium) | 2026-09-25 | rows 1, 5 | As above. |
| 8 Social handles | Pending (SE: Risk) | 2026-09-25 | [@pankote](https://www.instagram.com/pankote/), [TikTok @fatfatpankocat](https://www.tiktok.com/@fatfatpankocat) | Personal and pet accounts; heavy recipe hashtag use. |

---

##### `Gumbo` (not recommended)

- **Concept:** The Louisiana stew, and English "a gumbo of…" (a mix of everything).
- **Pronunciation:** PL [ˈɡumbɔ] "GOOM-bo". EN /ˈɡʌmboʊ/ "GUM-boh". The vowel differs, so it fails "one spelling, one sound". **Catchiness:** 4/5. **Store title:** "Gumbo: Meal Planner" (19).
- **Main risks:** a same-name digital-health company and app; a "Gumbo Brands Official | Disposables" account (product type not shown); gumbo.com in use; a Polish off-road app called GUMBO.

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk | 2026-09-25 | [getgumbo.com](https://getgumbo.com/), [Gumbo King](https://apps.apple.com/us/app/gumbo-king/id6503229616), [Gumbo Calculator](https://mwm.ai/apps/gumbo-calculator/6754898310) | Gumbo "is a healthcare technology company… bridging the gap between patients and healthcare providers"; restaurants; a gumbo-recipe calculator. |
| 2 App Store | Pending (SE: Risk) | 2026-09-25 | [Gumbo App](https://apps.apple.com/us/app/gumbo-app/id1244235497), [Gumbo 94.9](https://apps.apple.com/us/app/gumbo-94-9-country-classics/id1072552230) | Social sharing; radio. |
| 3 Google Play | Pending (SE: Risk) | 2026-09-25 | [Gumbo (GUMBO CORPORATION)](https://play.google.com/store/apps/details?id=com.gumbo.app), [GUMBO off-road](https://chrome-stats.com/d/pl.gumbo.mobile) | "Healthy Communities, No Language Barriers"; a Polish 4x4 app (package `pl.gumbo.mobile`). |
| 4 Domains | Pending (SE: Risk) | 2026-09-25 | [gumbo.com](https://www.gumbo.com/) | "Gumbo Software, Inc." at gumbo.com. |
| 5 Trademarks | Pending (SE: Inconclusive) | 2026-09-25 | Registries blocked | No mark surfaced. |
| 6 Language | Risk | 2026-09-25 | Reviewer assessment | PL/EN vowel mismatch. |
| 7 Confusing similarity | Risk (high) | 2026-09-25 | rows 1, 3 | Same-name digital-health app. |
| 8 Social handles | Pending (SE: Risk) | 2026-09-25 | [@gumbo_app](https://www.instagram.com/gumbo_app/), [@gumbobrands](https://www.instagram.com/gumbobrands/), [@gumbobrandsdisposable](https://www.instagram.com/gumbobrandsdisposable/) | `@gumbo_app` is the off-road app; "Gumbo Brands Official \| Disposables". |

---

##### `Mogu` (not recommended)

- **Concept:** Japanese *mogu-mogu* = "munch munch", the sound of happy chewing. Very catchy and on-topic.
- **Pronunciation:** PL [ˈmɔɡu] "MO-gu". EN /ˈmoʊɡuː/ "MOH-goo". **Catchiness:** 5/5. **Store title:** "Mogu: Meal Planner" (18).
- **Meaning and connotations:** **Russian *могу* ("mogu") = "I can"**, which most Poles recognise; PL *mogę* is close. That makes it read as Slavic, against the PO's international brief (C10 = 2).
- **Main risks:** "Mogu Exercise", an app that tracks chewing during meals; US MÓGU MUSHROOMS (dietary supplements); MOGU Inc. (mogu.com); MOGU MOGU drinks.

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk | 2026-09-25 | [Mogu Mogu (Wikipedia)](https://en.wikipedia.org/wiki/Mogu_Mogu), [@mogumycelium (via SE)](https://www.instagram.com/mogumycelium/) | A nata-de-coco drink brand; a mycelium design company. |
| 2 App Store | Pending (SE: Risk) | 2026-09-25 | [Mogu Exercise](https://apps.apple.com/us/app/mogu-exercise/id6757423910), [MÓGŪ Modern Chinese](https://apps.apple.com/us/app/m%C3%B3g%C5%AB-modern-chinese/id6498314806), [Mogu Router](https://apps.apple.com/us/app/mogu-router/id1530313625) | Summary: Mogu Exercise "automatically tracks chewing per bite during meals". |
| 3 Google Play | Pending (SE: Risk) | 2026-09-25 | [MOGU](https://play.google.com/store/apps/details?id=com.bella.mogu&hl=en_US), [MOGU Tours](https://play.google.com/store/apps/details?id=com.moguapp&hl=en_US) | Teacher monitoring; travel. |
| 4 Domains | Pending (SE: Risk) | 2026-09-25 | [Yahoo Finance: MOGU](https://finance.yahoo.com/quote/MOGU/), [moguplatform.com](https://moguplatform.com/en) | The summary lists "Mogu.com" among MOGU Inc.'s websites (unverified). |
| 5 Trademarks | Pending (SE: Risk) | 2026-09-25 | [Trademarkia: MOGU 76977413](https://www.trademarkia.com/mogu-76977413), [uspto.report: MÓGU MUSHROOMS](https://uspto.report/TM/98143269), [Justia: MOGU MOGU](https://trademarks.justia.com/975/76/mogu-97576111.html) | "MOGU is a registered trademark (Registration #2952844) owned by Ebisu Kasei"; MÓGU MUSHROOMS Reg #7511938 "to cover dietary supplements"; MOGU MOGU Reg 4923794 (beverages). |
| 6 Language | Risk | 2026-09-25 | Reviewer assessment | The Russian "I can" reading. |
| 7 Confusing similarity | Risk (high) | 2026-09-25 | rows 2, 5 | An eating-behaviour app and a supplements mark. |
| 8 Social handles | Pending (SE: Risk) | 2026-09-25 | [@mogumogu_global](https://www.instagram.com/mogumogu_global/), [@moguchinese](https://www.instagram.com/moguchinese/) | Many accounts. |

---

##### `Pappa` (not recommended)

- **Concept:** Italian *pappa* = grub ("la pappa è pronta", "food's ready").
- **Pronunciation:** PL [ˈpappa] "PAP-pa". EN /ˈpɑːpə/ "PAH-puh". **Catchiness:** 3/5. **Store title:** "Pappa: Meal Planner" (19).
- **Meaning and connotations:** IT *pappa* is mainly baby food; *la pappa pronta* means "spoon-fed" (having things done for you), a slightly pejorative idiom. SV/NO *pappa* = dad. It reads as "papa" everywhere.
- **Main risks:** "Papa" senior-care apps sound identical; baby-food meaning; @pappa in use.

| Check | Status | Date | Source link | What the source showed |
|---|---|---|---|---|
| 1 Competitors | Risk | 2026-09-25 | [Pappa Ciccia](https://apps.apple.com/us/app/pappa-ciccia/id858138217?uo=4), [Pappa Pastificio](https://apps.apple.com/us/app/id1587366145) | Italian restaurants and delivery. |
| 2 App Store | Pending (SE: Risk) | 2026-09-25 | [Pappa Pizza](https://apps.apple.com/us/app/pappa-pizza/id6648791468), [Pappa AB developer](https://apps.apple.com/us/developer/pappa-ab/id1169932510), [Papa Care](https://apps.apple.com/us/app/papa-care/id1534207289) | Pizza ordering; a Swedish developer; senior care. |
| 3 Google Play | Pending (SE: Risk) | 2026-09-25 | [Pappa.ai](https://play.google.com/store/apps/details?id=com.maitsys.pappaai&hl=en_US), [Papa Care](https://play.google.com/store/apps/details?id=com.papacare&hl=en_US) | A school-pickup app; senior care. |
| 4 Domains | Pending (SE: Inconclusive) | 2026-09-25 | RDAP blocked | Nothing surfaced at pappa.com, .app, .io or .pl; app.papa.com (Papa) is in use. |
| 5 Trademarks | Pending (SE: Inconclusive) | 2026-09-25 | Registries blocked | No PAPPA mark surfaced; Pappas Restaurants marks are near. |
| 6 Language | Risk | 2026-09-25 | Reviewer assessment | Baby food; "spoon-fed"; "dad". |
| 7 Confusing similarity | Risk (medium) | 2026-09-25 | rows 2–3 | Papa (senior care) sounds identical. |
| 8 Social handles | Pending (SE: Risk) | 2026-09-25 | [@pappa](https://www.instagram.com/pappa/), [@pappa_fr](https://www.instagram.com/pappa_fr/) | The exact Instagram @pappa is in use. |

#### 6.7.4 Domain strategy for short names

A 4-letter .com is almost always registered, and for Zubo, Kazu, Dozo, Nimbo and Gobo the search engine found other businesses using related domains (zubogo.com, kazu.org, dozo.app, nimbo.earth, gobo.com, gobo.io). Once RDAP is reachable, check these in this order, then decide with the owner (§8.5.2):

| Name | 1st | 2nd | 3rd | 4th (PL market) |
|---|---|---|---|---|
| Zubo | zubo.app | getzubo.com | zuboapp.com | zubo.pl |
| Kazu | kazu.app | getkazu.com | kazuapp.com | kazu.pl |
| Dozo | getdozo.com | dozoapp.com | dozo.io | dozo.pl (dozo.app appears taken) |
| Nimbo | nimbo.app | getnimbo.com | nimboapp.com | nimbo.pl |
| Gobo | gobo.app | getgobo.com | goboapp.com | gobo.pl |

All are **Pending**; none has been checked on a registry. Remember that .app requires HTTPS (HSTS preloaded) and that a registry 404 does not guarantee a standard price.

---

### Session-2 shortlist (superseded 2026-09-25, PO: too long, not catchy)

> **Superseded 2026-09-25 (PO: "i dont like those names they are too long and not catchy").** §6.1–§6.6 below are kept exactly as written, with all their evidence. The session-2 top 3 (Tangram, Ramekin, Palmo) and alternates (Sapimo, Tadam) are no longer recommended. They are replaced by §6.7.

> **Rebuilt in session 2 (2026-09-24), international-first.** The shortlist now has **9 international names** (§6.1–§6.3) and **2 Polish-flavoured alternatives** (§6.4), which are not recommended as the main brand for international expansion. The other session-1 names were removed; their evidence is kept in §6.5. The session-1 check matrix and ranking are kept in §6.6 and marked superseded.

### 6.1 Check matrix (session 2: 9 international names; superseded 2026-09-25)

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

### 6.2 Scores (C1–C7, C10) and ranking (session 2; superseded 2026-09-25)

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

### 6.3 Per-name evidence (session-2 international shortlist; superseded 2026-09-25)

All session-2 checks are dated **2026-09-24**. Store, domain, trademark and handle checks are **Pending** for every name because the official sources were egress-blocked (§5.1). The bracketed search-engine indication is given in the "What the source showed" column. "SE" means a WebSearch result that could not be opened.

---

#### `Tangram` (session-2 top 3; superseded 2026-09-25)

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

#### `Palmo` (session-2 top 3; superseded 2026-09-25)

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

#### `Sapimo` (session-2 alternate; superseded 2026-09-25)

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

#### `Ramekin` (session-2 top 3; superseded 2026-09-25)

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

#### `Tadam` (session-2 alternate; superseded 2026-09-25)

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

> **Current: §7.5 (session 4), placed first below, and §7.1 (session-level limits, still current).** §7.4 (session 3), §7.2 (session 2) and §7.3 (session 1) are kept for history.

### 7.5 Session 4 risks (current, 2026-09-25)

**Session-level risks added in session 4** (on top of §7.1):
1. **Real English food words are the most crowded naming space found.** 43 of the 111 words screened by search already name a recipe, meal-planning or nutrition app or service (§5.5). The shortlist is ranked by where same-name uses sit (food and nutrition apps are serious; dance, comics, HR software and fintech are lighter), not by absence. New same-category apps are appearing monthly (§3.6), so re-check before any decision.
2. **Weaker trademarks than coinages.** A real food word is registrable for nutrition software when it names a specific food (Pretzel, Donut, Salsa), but it will coexist with many marks for the same word in other classes, and EUIPO assesses meaning in every EU language (Salsa is "sauce" in ES/IT/PT). Portion and meal words (Handful, Batch, Lunchbox, Supper) sit closer to descriptive. The PO's style choice trades some legal strength for instant recognition; an attorney should confirm the trade is acceptable.
3. **The bare store search term will not be ours.** For every shortlisted word, the store search already returns other apps (dance for Salsa, pretzel chains for Pretzel, donut shops for Donut). Discovery will depend on the descriptor ("…: Meal Planner & Macros") and on marketing, not on the name.
4. **Exact domains and handles.** The exact .com and exact Instagram handle are very likely taken for every shortlisted word. Plan for a variant such as `<name>.app` + `get<name>.com` / `eat<name>.com` + `<name>.pl` (§6.8.4).
5. **Search summaries can be wrong.** As in session 3, some summaries attribute domains without a URL (pickle.io). These are recorded as unverified. Only RDAP settles domain status, and only the registries settle trademarks.

**Name-specific risks (top 3 and alternates):**

| Name | Main remaining risk | What would resolve it |
|---|---|---|
| **Salsa** | UK SALSA registration for food-safety compliance software (9/42); SALSA software namesakes (Salsa Labs, salsa.dev); *salsa* = "sauce" in ES/IT/PT; dance and live-streaming apps own the store term; exact handles taken | EUIPO, TMview (EM, PL, ES, IT, PT, GB), UPRP, WIPO, USPTO and UK IPO for SALSA in classes 9, 35, 41, 42, 44 (and 29/30); an attorney's view on coexistence with UK00003937773 and on ES/IT/PT descriptiveness; RDAP for salsa.app, getsalsa.com, eatsalsa.com, salsa.pl; a listener test ("food or dance first?") |
| **Pretzel** | US PRETZEL reg. 5312372 for downloadable language-learning software (class 9); pretzel chains' apps; @pretzel.app taken; PL spelling *precel*; the long store title uses all 30 characters | Registry searches for PRETZEL in 9, 42, 44 (and 29/30, 43) in the EU, PL and US; an attorney's view on reg. 5312372; RDAP for pretzel.app, getpretzel.com, eatpretzel.com, pretzel.pl; a PL listener spelling test |
| **Donut** | Donut for Slack (donut.com) is a strong same-name software brand in 9/42; "I Deserve a Donut" weight-loss devotional app; DONUT LAB class-9 application; a positioning bet (treat food as the brand of a nutrition platform); donut/doughnut spelling | Registry searches for DONUT and DOUGHNUT in 9, 42, 44; an attorney's view on Donut Technologies' marks; a listener test with the wedge and 2–3 dietitians (PRD §3) on "playful" versus "flippant"; RDAP for donut.app, eatdonut.com, donut.pl |
| Pickle (alternate) | Pickle.ph meal-plan service with macros (same category, PH); PICKLE software marks; DE *Pickel* = pimple | Registry searches in 9, 42, 43, 44; a German-speaker check; RDAP |
| Handful (alternate) | Moderate food hint only; borderline descriptive for portions; handful.com sports-bra brand and @handful | An attorney's view on descriptiveness in 9 and 44; a listener test ("does it say food?"); registry searches in 9, 25, 42, 44 |

**Open checks per shortlisted name (all Pending):** App Store (iTunes API PL/US/GB) and App Store Connect, Google Play (PL/US), RDAP for .com, .app, .io and .pl plus the §6.8.4 variants, EUIPO, TMview (EM + PL, plus ES/IT/PT for Salsa and DE for Pickle), UPRP, WIPO, USPTO, UK IPO, and handles on Instagram, TikTok, Facebook, YouTube, X, Threads and LinkedIn. For Tapas, Nacho, Melon, Bagel, Pesto, Caper and Gravy, domains, trademarks and handles were only partly searched (§6.8.3).

### 7.4 Session 3 risks (superseded 2026-09-25, PO: "nothing from proposals")

> **Superseded 2026-09-25.** The session-3 names are no longer recommended; §7.5 lists the current risks. The session-level points 1, 2 and 4 below still apply. Kept as written.

**Session-level risks added in session 3** (on top of §7.1):
1. **Short names cannot be "clean".** Every shortlisted name already has same-name apps, businesses and handles somewhere. The shortlist is ranked by *where* those uses are (outside food, nutrition and health is better), not by absence. Expect the exact .com and the exact Instagram handle to be unavailable for all of them, and plan for a variant (§6.7.4).
2. **Catchiness and language scores are the reviewer's own.** C11 is new and has not been tested with listeners. Short names depend heavily on how they sound, so the PL and EN listener test (§8.5.2 item 7) matters more than it did for longer names.
3. **Japanese-word cluster.** Six of the twelve shortlisted names are Japanese words. They pass the PL/EN reading test for the same reason (identical vowels), but a Japanese flavour is a brand choice the PO should make on purpose (§8.5.3).
4. **Search summaries are sometimes wrong about domains.** In this session the search engine attributed domains (kazu.com, zumo.app, zumo.pl) to businesses without showing a URL at those domains. Those claims are recorded as unverified and must not be relied on. Only RDAP settles domain status.

**Name-specific risks (top 3 and alternates):**

| Name | Main remaining risk | What would resolve it |
|---|---|---|
| **Zubo** | Exact-name class-9 apps in ride-hailing and kids' reading; Instagram @zubo.app in use; the *zub* (tooth) echo in CS/SK/BCS/RU; no meaning, so the descriptor carries the product | EUIPO, TMview (EM, PL), UPRP, WIPO and USPTO for ZUBO and ZUB* in classes 9, 42, 44 (and 35, 41, 29/30); RDAP for zubo.app, getzubo.com, zubo.pl; a listener test including a Czech or Croatian speaker |
| **Kazu** | The PL "Kaziu" echo (familiar form of Kazimierz) in the launch market; many exact-name class-9 apps; @kazu taken | A PL listener test first (5–10 people from the PRD §3 wedge: "what does this remind you of?"); then registry searches for KAZU and KAZ* in the same classes; RDAP |
| **Dozo** | US DOZO marks for hemp gummies and vaporizers and a DOZO PERKS supplements application (class 5); dozo.app in use; the PL *doza* (dose) echo | Registry searches for DOZO in classes 5, 9, 29, 30, 42, 44 (EU, PL, US); an attorney's view on class-5 neighbours for a nutrition app; RDAP for getdozo.com and dozo.pl; a PL listener test for the "dose" echo |
| Nimbo (alternate) | An unverified mention of a Nimbo patient-management system (health software); many Nimbo businesses | A store and registry search for a health "Nimbo"; registry searches in classes 9, 42, 44; RDAP |
| Gobo (alternate) | Exact name used by a food-ordering super-app and a healthy-food delivery service; gobo.com and gobo.io in use; a GOBO class-42 filing in India | Registry searches in classes 9, 35, 39, 42, 43; an attorney's view on coexistence with a food-ordering platform; RDAP for gobo.app and getgobo.com |

**Open checks per shortlisted name (all Pending):** App Store (iTunes API PL/US/GB) and App Store Connect, Google Play (PL/US), RDAP for .com, .app, .io and .pl plus the §6.7.4 variants, EUIPO, TMview (EM + PL, plus JP-, KR- and ES-origin checks as relevant), UPRP, WIPO, USPTO, UK IPO, and handles on Instagram, TikTok, Facebook, YouTube, X, Threads and LinkedIn.

### 7.1 Session-level limits (updated 2026-09-25; still current, see also §7.5)

1. **No authoritative check could run in any session (1, 2, 3 or 4).** Every store, domain, trademark and handle status is Pending (§5.1). Rankings rest on search-engine evidence, which can miss registered marks, unlaunched apps, and parked or reserved domains.
2. **Absence is not availability.** Where the search found nothing (for example Sapimo anywhere, or Tangram and Palmo in food), the status is Inconclusive. It must not be read as "free".
3. **Language checks are the reviewer's own assessment.** C10 raises the bar: native-speaker checks are now needed in PL, EN (UK and US), DE, FR, ES, IT, PT, NL and SV for the top 3 and the alternates. They are pending.
4. **Trademark reality.** Real words used arbitrarily (Tangram, Palmo, Ramekin, Tadam) will have registrations in other classes, and Tangram is a common noun for puzzle games in class 9. Coinages (Sapimo) are likely stronger but carry less meaning. Italian words (Sarto, Portata, Mestolo) are weak in Italy, and Portata may be descriptive there. Only a registry search and an attorney can settle this.
5. **The category is filling fast.** Session 2 found more than fifteen same-category apps that weren't in the session-1 landscape (§3.4). A name that is Inconclusive today can have a competitor next month, so re-check at decision time.

### 7.2 Name-specific risks (session 2: top 3 and alternates; superseded 2026-09-25)

> **Superseded 2026-09-25 (PO: too long, not catchy).** These names are no longer recommended; §7.4 lists the current risks. Kept as written.

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

> **Current: §8.6 (session 4), placed first below.** It is numbered 8.6 so that existing references to §8.1–§8.5 stay valid. §8.5 (session 3), §8.1–§8.3 (session 2) and §8.4 (session 1) are superseded and kept for history. The current decisions for the Product Owner are in **§8.6.3**.

### 8.6 Session 4 next steps (current, 2026-09-25)

#### 8.6.1 Re-run on a network with registry access (agent, next session)

Run these for **Salsa, Pretzel and Donut** first, then **Pickle and Handful**, then Kettle. Replace `<n>` with the lowercase name.

- App Store: `https://itunes.apple.com/search?term=<n>&entity=software&country=pl` (then `us`, `gb`). Record every exact and near match and its category (Health & Fitness and Food & Drink especially).
- Google Play: `https://play.google.com/store/search?q=<n>&c=apps&gl=PL` (then `gl=US`).
- .com: `https://rdap.verisign.com/com/v1/domain/<n>.com`, then `get<n>.com`, `eat<n>.com` and `<n>app.com`.
- .app: `https://pubapi.registry.google/rdap/domain/<n>.app`.
- .pl and .io: get the RDAP base URLs for `pl` and `io` from `https://data.iana.org/rdap/dns.json`, then `<base>/domain/<n>.pl` and `<base>/domain/<n>.io`.
- Re-check the specific findings from session 4: UK SALSA UK00003937773 (goods and status); US PRETZEL 86953904 / reg. 5312372 (goods and status); DONUT LAB 98936152 and Donut Technologies' marks; the Pickle.ph service; "I Deserve a Donut" (id529567174, category); the Polish-store "Pesto - Recipe App" (id6504192769) for the record.

#### 8.6.2 Owner actions (need an account, or are the owner's call)

1. **Trademark searches**, until the agent can reach the registries. Search each name as an exact word, then with a wildcard and phonetically:
   - **EUIPO eSearch plus** (https://euipo.europa.eu/eSearch/): Trade marks, "Word" = `SALSA`, then `PRETZEL`, `DONUT` (and `DOUGHNUT`), `PICKLE`, `HANDFUL`. Nice classes 9, 29, 30, 35, 41, 42, 43, 44. Status: all, then filed and registered only. Repeat with `SALSA*`, `PRETZEL*`, `DONUT*`, `PICKLE*`.
   - **TMview** (https://www.tmdn.org/tmview/): the same terms. Offices: EM, PL, DE, FR, ES, IT, PT, NL, GB, WO. Same classes. Record live or dead status, owner and filing date.
   - **UPRP e-Wyszukiwarka** (https://ewyszukiwarka.pue.uprp.gov.pl/): "Znaki towarowe", word element `salsa` / `pretzel` / `precel` / `donut` / `donat` / `pickle` / `handful`.
   - **WIPO Global Brand Database** (https://branddb.wipo.int/): Brand = the name, the classes above, designations PL, EU, US, GB.
   - **USPTO** (https://tmsearch.uspto.gov/): `SALSA`, `PRETZEL` (open serial 86953904 and read its goods), `DONUT` (look for Donut Technologies Inc.), `PICKLE`, `HANDFUL`; classes 9, 42, 44. **UK IPO** (https://trademarks.ipo.gov.uk/): the same, and open UK00003937773 (SALSA).
2. **App Store Connect name check** for "Salsa", "Pretzel" and "Donut", each with a descriptor (for example "Salsa: Meal Planner & Macros", 28 characters). This needs the owner's Apple Developer account. Reserve a name only when ready to commit, because Apple holds reservations for a limited time.
3. **Google Play Console check:** needs the owner's developer account.
4. **Trademark attorney clearance** before adoption, in at least the EU (EUIPO) and Poland (UPRP), plus the US and UK if English-speaking launches are planned. Ask specifically about: Salsa against UK00003937773 and its descriptiveness in ES/IT/PT; Pretzel against US reg. 5312372; Donut against Donut Technologies' software marks; and, for Handful, descriptiveness for portion features. Nothing here is a legal opinion.
5. **Social handles:** only signing up confirms a handle is free. The exact handles are very likely taken for all five, so the realistic sets are `getsalsa` / `salsa.pl`, `getpretzel` / `pretzel.pl`, `donut.pl` / `eatdonut`. The owner decides whether to sign up on Instagram, TikTok, Facebook, YouTube, X, Threads and LinkedIn.
6. **Domain purchase decisions:** the owner buys; the agent never does. Accept early that the exact .com is unlikely for a dictionary word, and choose a pattern (`<name>.app` + `get<name>.com` or `eat<name>.com` + `<name>.pl`) (§6.8.4).
7. **Listener test:** 5–10 people from the PL wedge (PRD §3), 3–5 native English speakers, and 1–2 each for DE, ES and IT. Say each name once (Salsa, Pretzel, Donut, Pickle, Handful) and ask them to write it down, say what kind of app it could be (the PO's "clearly food" test), say what it reminds them of, and rate how catchy it is. Probe specifically: "food or dance?" for Salsa; "precel" spelling for Pretzel; "playful or unserious for a nutrition app?" for Donut (include 2–3 dietitians); DE *Pickel* for Pickle; "does it say food?" for Handful.

#### 8.6.3 Decisions for the Product Owner

1. **Does the session-4 direction answer the questionnaire?** All shortlisted names are real English words with a clear food hint (Handful and Kettle moderate). Which of Salsa, Pretzel and Donut (or Pickle, Handful) feels right?
2. **Healthy-sounding versus indulgent.** The healthy and kitchen-tool words (Ladle, Spoon, Basil, Lemon, Pantry, Supper, Savor) are all taken by same-category apps. What is left is lively or indulgent food (Salsa, Pretzel, Donut, Pickle). Is an indulgent name acceptable for a nutrition platform, given the PRD §1 promise "eat what you feel like eating"? This matters most for Donut.
3. **Loanwords.** Salsa (and Tapas, Nacho, Pesto) are English dictionary words borrowed from Spanish or Italian. Do they count as "real English words" for the PO, given the earlier rejection of foreign words (Kazu, Dozo)?
4. **Handle and domain compromise.** Is a variant such as `getsalsa` / `salsa.app` / `eatpretzel.com` acceptable, given that the exact dictionary-word .com and handles are very likely taken?
5. **Legal strength versus recognition.** A real food word is instantly understood but is a weaker, more crowded trademark than a coinage. Is the PO comfortable with that trade, subject to the attorney's view?

**Do not** rename application identifiers, bundle IDs, packages, domains or assets until the Product Owner approves a final name (CLAUDE.md).

### 8.5 Session 3 next steps (superseded 2026-09-25 by §8.6)

> **Superseded 2026-09-25 (PO: "nothing from proposals").** The checks below concern the session-3 names, which are no longer recommended. Kept as written.

#### 8.5.1 Re-run on a network with registry access (agent, next session)

Run these for **Zubo, Kazu and Dozo** first, then **Nimbo and Gobo**, then Bibim. Replace `<n>` with the lowercase name.

- App Store: `https://itunes.apple.com/search?term=<n>&entity=software&country=pl` (then `us`, `gb`). Record every exact and near match and its category (Health & Fitness, Food & Drink especially).
- Google Play: `https://play.google.com/store/search?q=<n>&c=apps&gl=PL` (then `gl=US`).
- .com: `https://rdap.verisign.com/com/v1/domain/<n>.com`, and also `get<n>.com` and `<n>app.com`.
- .app: `https://pubapi.registry.google/rdap/domain/<n>.app` (for Dozo, confirm whether dozo.app is registered, as the search suggests).
- .pl and .io: get the RDAP base URLs for `pl` and `io` from `https://data.iana.org/rdap/dns.json`, then `<base>/domain/<n>.pl` and `<base>/domain/<n>.io`.
- Re-check the specific findings from session 3: the Instagram account @zubo.app; the "Kazu" App Store app id6756679772 (category unknown); US DOZO serial 97460033 and DOZO PERKS 98725477 (goods and status); the "Nimbo" patient-management mention; GOBO India 5100801; EU ZUMO 17996331.

#### 8.5.2 Owner actions (need an account, or are the owner's call)

1. **Trademark searches**, until the agent can reach the registries. Search each name as an exact word, then with a wildcard and phonetically:
   - **EUIPO eSearch plus** (https://euipo.europa.eu/eSearch/): Trade marks, "Word" = `ZUBO`, then `KAZU`, `DOZO`, `NIMBO`, `GOBO`. Nice classes 5, 9, 29, 30, 35, 41, 42, 43, 44 (class 5 because of the DOZO hemp and supplement marks). Status: all, then filed and registered only. Repeat with `ZUB*`, `KAZ*`, `DOZ*`, `NIMB*`, `GOB*`.
   - **TMview** (https://www.tmdn.org/tmview/): the same terms. Offices: EM, PL, DE, FR, ES, IT, CZ, HR, WO, plus JP for Kazu, Dozo and Gobo. Same classes. Record live or dead status, owner and filing date.
   - **UPRP e-Wyszukiwarka** (https://ewyszukiwarka.pue.uprp.gov.pl/): "Znaki towarowe", word element `zubo` / `kazu` / `dozo` / `nimbo` / `gobo`.
   - **WIPO Global Brand Database** (https://branddb.wipo.int/): Brand = the name, the classes above, designations PL, EU, US, GB.
   - **USPTO** (https://tmsearch.uspto.gov/): `ZUBO` (confirm 77462177 is dead and read 98431784's goods), `DOZO` (open 97460033 and 98725477), `KAZU`, `NIMBO`, `GOBO`; classes 5, 9, 42, 44. **UK IPO** (https://trademarks.ipo.gov.uk/): the same.
2. **App Store Connect name check** for "Zubo", "Kazu" and "Dozo", each with a descriptor (for example "Zubo: Meal Planner", 18 characters). This needs the owner's Apple Developer account. Reserve a name only when ready to commit, because Apple holds reservations for a limited time.
3. **Google Play Console check:** needs the owner's developer account.
4. **Trademark attorney clearance** before adoption, in at least the EU (EUIPO) and Poland (UPRP), plus the US and UK if English-speaking launches are planned. Ask specifically about: Zubo against the same-name class-9 apps; Dozo against the US class-5 DOZO marks; Gobo against the food-ordering platform. Nothing here is a legal opinion.
5. **Social handles:** only signing up confirms a handle is free. For Zubo, `@zubo.app` is already taken on Instagram, so the realistic set is `getzubo`, `zubo.pl`, `zuboplanner` (and `@zubo` if it turns out to be free). The owner decides whether to sign up on Instagram, TikTok, Facebook, YouTube, X, Threads and LinkedIn.
6. **Domain purchase decisions:** the owner buys; the agent never does. Accept early that a 4-letter .com is unlikely and choose a pattern (`<name>.app` + `get<name>.com` + `<name>.pl`) (§6.7.4).
7. **Listener test (the most important next step for short names):** 5–10 people from the PL wedge (PRD §3), 3–5 native English speakers, and 1–2 each for DE, ES, IT, CS or HR. Play each name once (Zubo, Kazu, Dozo, Nimbo, Gobo) and ask them to write it down, say it back, say what it reminds them of, and rate how catchy it is. Probe specifically: "Kaziu" for Kazu; "doza" (dose) for Dozo; the *zub* (tooth) echo for Zubo; "gob" for Gobo.

#### 8.5.3 Decisions for the Product Owner

1. **Does the session-3 direction answer the feedback?** All shortlisted names are 4–5 letters and 2 syllables. Is this the length and rhythm the PO had in mind, and which of Zubo, Kazu and Dozo (or Nimbo, Gobo) feels catchy?
2. **Pure sound or a hidden meaning.** Zubo means nothing, which makes it the most ownable but leaves all the explaining to the descriptor. Kazu ("number") and Dozo ("help yourself") carry a story for the brand, at the cost of more namesakes. Which does the PO prefer?
3. **Japanese flavour.** Kazu, Dozo and Gobo (and Kumo, Panko, Mogu) are Japanese words. Is a Japanese-sounding brand acceptable for a Polish-launched, internationally expanding nutrition app, or should the next round stay with coined sounds such as Zubo and Nimbo?
4. **Handle and domain compromise.** Is a variant such as `getzubo` / `zubo.app` acceptable, given that the exact 4-letter handles and .com are very likely taken for any short name?
5. **Catchiness versus conflicts.** Zumo and Mogu are the catchiest names found (C11 = 5) but carry high-weight conflicts. Does the PO want them investigated anyway?

**Do not** rename application identifiers, bundle IDs, packages, domains or assets until the Product Owner approves a final name (CLAUDE.md).

### 8.1 Re-run on a network with registry access (session 2; superseded 2026-09-25 by §8.5.1)

Run these for **Tangram, Ramekin and Palmo** first, then **Sapimo and Tadam**, then the rest of §6.1 and the §6.4 alternatives. Replace `<n>` with the lowercase name.

- App Store: `https://itunes.apple.com/search?term=<n>&entity=software&country=pl` (then `us`, `gb`)
- Google Play: `https://play.google.com/store/search?q=<n>&c=apps&gl=PL` (then `gl=US`)
- .com: `https://rdap.verisign.com/com/v1/domain/<n>.com`
- .app: `https://pubapi.registry.google/rdap/domain/<n>.app`
- .pl and .io: get the RDAP base URL for `pl` and `io` from `https://data.iana.org/rdap/dns.json`, then `<base>/domain/<n>.pl` and `<base>/domain/<n>.io`
- Also re-check the near-conflicts found in session 2: "saviMon" (for Savimo), "Sapora" (for Sapimo), PORTA and "portata.dev" (for Portata), and the US TANGRAM serial 88473186 (for Tangram).

### 8.2 Owner actions (session 2; superseded 2026-09-25 by §8.5.2)

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

### 8.3 Decisions for the Product Owner (session 2; superseded 2026-09-25 by §8.5.3)

> **Superseded 2026-09-25.** The PO answered these indirectly ("too long and not catchy"). The current decisions are in **§8.5.3**. Kept as written.

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
| 2026-09-25 | **Third research session (brand-researcher): short-and-catchy round.** It responds to the Product Owner's feedback on session 2, verbatim: "i dont like those names they are too long and not catchy" (covering Tangram, Ramekin, Palmo, Sapimo, Tadam, Savimo, Sarto, Portata, Mestolo). At the start, each official source was retried once with a plain request (curl for all; WebFetch also for the .com RDAP, iTunes, Google Play and TMview URLs). All were still egress-blocked (§5.1), so every authoritative check remains **Pending**, and screening used WebSearch only. **Added:** the session-3 strategy with the PO feedback (§2.4, numbered to keep existing references valid) and the new criterion C11 catchiness (§2.3); a short note in §1; same-category apps found in session 3 (§3.5); 111 new candidates, #161–#271, all 3–6 letters and 1–2 syllables (§4.7); the session-3 access log and screening evidence (§5.1, §5.4); a new current shortlist of **12 names** (Zubo, Kazu, Dozo, Nimbo, Gobo, Bibim, Kumo, Zumo, Mogu, Panko, Pappa, Gumbo) with a check matrix, C1–C7, C10 and C11 scores, per-name evidence and a domain-variant plan (§6.7); session-3 risks (§7.4, §7.1 updated); next steps, owner actions and PO decisions (§8.5). **Superseded, not deleted:** the session-2 form rule and "cleanest openings" conclusion (§2.1); the session-2 shortlist, matrix, ranking and top 3 (§6.1–§6.3, marked "superseded (PO: too long, not catchy)"); session-2 risks and next steps (§7.2, §8.1–§8.3). **Top 3 for further investigation** changed from Tangram, Ramekin, Palmo to **Zubo, Kazu, Dozo** (alternates: Nimbo, Gobo). No name was selected. |
| 2026-09-25 | **Fourth research session (brand-researcher): short real English food-word round.** It responds to the Product Owner's feedback on session 3, verbatim: "nothing from proposals" (covering Zubo, Kazu, Dozo, Nimbo, Gobo, Bibim, Zumo, Kumo, Panko, Gumbo, Mogu, Pappa), and to the PO's style questionnaire (2026-09-25): preferred style **short real English word** (as Bolt, Lime, Oura, Notion or Headspace are real words), not coined sounds and not foreign words; food hint **clearly** (people should guess it is a food or meal app from the name alone); no example brands given. At the start, each official source was retried once with a plain request (curl for all; WebFetch also for the .com RDAP, iTunes, Google Play and TMview URLs). All were still egress-blocked (§5.1), so every authoritative check remains **Pending**, and screening used WebSearch only (including domain-filtered searches on the stores, Instagram, TikTok and third-party trademark mirrors). **Added:** the session-4 strategy with the PO feedback and questionnaire (§2.5, numbered to keep existing references valid), a session-4 note on C11 and the Food hint and D/S columns (§2.3); a short note in §1; same-category apps found in session 4, with Savor added to the watch list (§3.6); 129 new candidates, #272–#400, all real English food, cooking or kitchen words of 3–8 letters with D/S and Polish-reading flags (§4.8); the session-4 access log and screening evidence, with a tally (111 searched, 43 already the exact name of a food, recipe, nutrition or meal-planning app or service) (§5.1, §5.5); a new current shortlist of **13 names** (Salsa, Pretzel, Donut, Pickle, Handful, Kettle, Tapas, Nacho, Melon, Bagel, Pesto, Caper, Gravy) with a check matrix, C1–C7, C10 and C11 scores, food hint, per-name evidence with distinctiveness notes, and a domain-variant plan (§6.8); session-4 risks (§7.5, §7.1 updated); next steps, owner actions and PO decisions (§8.6). **Superseded, not deleted:** the session-3 strategy (§2.4); the session-3 shortlist, matrix, ranking and top 3 (§6.7, marked "superseded (PO: 'nothing from proposals')"); session-3 risks and next steps (§7.4, §8.5); the §4.7 result line. **Top 3 for further investigation** changed from Zubo, Kazu, Dozo to **Salsa, Pretzel, Donut** (alternates: Pickle, Handful). No name was selected. |
