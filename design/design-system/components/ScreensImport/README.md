# Add and import a recipe

Add recipe with the import notice, PDF recipe picker, import fallbacks (scanned PDF, no recipe data, site opts out, Instagram/TikTok link), Share Extension (with and without a caption), Import preview with a blocking allergen notice, No profile on this phone, Clarification prompt, Your version with source nutrition, Target missed, I don't have this, composed from FitMeal components on 375 × 780 iPhone frames. A showcase page, not a component: build the SwiftUI screen from the components it uses.

## Rules

- **What leaves the phone.** Link import reads only schema.org recipe data. PDFs are read on the phone (text layer only); the user ticks the recipes and only that text is sent, never the file. Shares from Instagram or TikTok send only the caption text; the post URL is kept as the source and never opened. Imports are always private and never feed a public catalog.
- **Import notice** sits next to the import actions on 25 and in the Share Extension (25g). It's a neutral note (`shield`, `surface-sunken`), not a `Notice` tone: it informs, it doesn't warn.
- **Every fallback offers *Paste recipe text*** as the primary action (25c–25f, empty caption in 25g). The fallbacks use `Notice` tone `info`, never `danger` or `warning`: nothing is wrong with the user's input. The URL stays as the source (`link` row), and the row says whether we opened it.
- **No OCR and no fetching of Instagram or TikTok links.** A scanned PDF gets *Paste recipe text* or *Choose another PDF*.
- **Quota:** each recipe ticked in a PDF counts as 1 import. 25b shows what's left; if the ticked count is higher, *Import N recipes* is disabled and the footnote says *You have 2 imports left this month. Untick 1 recipe.*
- **26b No profile on this phone:** the allergen check can't run, so the Import Preview is blocked with a `warning` `Notice` at the top, never collapsed. *Set up my profile* is primary, *Restore from iCloud* is second. The recipe can be saved but isn't fitted or planned until the check has run. Allergy conflicts found after setup still use `danger` (26).
- **26 from a share:** the source line reads *Shared from instagram.com · caption only*. A PDF import reads *From <file name> · pages 12–13*.

## States

| State | What the user sees |
| --- | --- |
| PDF opened, reading text | Picker with a spinner row *Reading your PDF…*; reading happens on the phone, works offline |
| PDF has text but no recipes found | 25c layout, title *We couldn’t find a recipe in this PDF*, same actions |
| Offline after ticking recipes | *Import N recipes* is disabled; `Notice` tone `offline`: *Importing needs a connection. Your ticks are kept.* |
| Link fetch fails (timeout, 404) | 25d layout with *Try again* as the second action |
| Share Extension while signed out | Sheet says *Open FitMeal to sign in first* with *Open FitMeal*; the caption isn't sent |

## Copy

| Key | EN | PL |
| --- | --- | --- |
| add.subtitle | From a recipe page, a PDF, a shared post or your notes. | Ze strony z przepisem, PDF-a, udostępnionego posta albo notatek. |
| add.link.desc | Recipe pages and blogs | Strony z przepisami i blogi |
| add.pdf | Choose a PDF | Wybierz PDF |
| add.pdf.desc | PDFs with selectable text, read on your phone | PDF z tekstem do zaznaczenia, czytany na Twoim telefonie |
| add.paste | Paste recipe text | Wklej tekst przepisu |
| add.tip | Tip: in Instagram or TikTok, tap Share → FitMeal. | Wskazówka: w Instagramie lub TikToku dotknij Udostępnij → FitMeal. |
| import.notice | **Import recipes only.** Don’t import documents with other people’s personal or health information. PDFs are read on your phone and never leave it. Recipe text is processed by our AI provider in the EU. Imports stay private to you. | **Importuj tylko przepisy.** Nie dodawaj dokumentów z danymi osobowymi ani zdrowotnymi innych osób. PDF-y czytamy na Twoim telefonie i nigdy go nie opuszczają. Tekst przepisu przetwarza nasz dostawca AI w UE. Importy widzisz tylko Ty. |
| picker.title | Choose recipes | Wybierz przepisy |
| picker.file.meta | 42 pages · read on this phone | 42 strony · odczytany na tym telefonie |
| picker.found | 4 found · 3 ticked | Znaleziono 4 · zaznaczono 3 |
| picker.note | Only the text of the ticked recipes is sent. The PDF stays on your phone. | Wysyłamy tylko tekst zaznaczonych przepisów. PDF zostaje na Twoim telefonie. |
| picker.quota | Each recipe counts as 1 import · 27 left this month | Każdy przepis to 1 import · w tym miesiącu zostało 27 |
| picker.cta | Import 3 recipes | Importuj 3 przepisy |
| picker.over | You have 2 imports left this month. Untick 1 recipe. | W tym miesiącu zostały Ci 2 importy. Odznacz 1 przepis. |
| scan.title | This PDF is a scan | Ten PDF to skan |
| scan.body | We can only read PDFs with selectable text. Paste the recipe text instead. | Odczytamy tylko PDF z tekstem, który da się zaznaczyć. Wklej tekst przepisu. |
| scan.other | Choose another PDF | Wybierz inny PDF |
| nodata.title | We can’t read a recipe on this page | Nie możemy odczytać przepisu z tej strony |
| nodata.body | Paste the recipe text and we’ll keep the link as the source. | Wklej tekst przepisu, a link zapiszemy jako źródło. |
| tdm.title | We don’t open this site | Nie otwieramy tej strony |
| tdm.body | This site doesn’t allow automated reading, so we don’t open it. Paste the recipe text and we’ll keep the link as the source. | Ta strona nie zezwala na automatyczne odczytywanie treści, więc jej nie otwieramy. Wklej tekst przepisu, a link zapiszemy jako źródło. |
| social.title | We don’t open Instagram or TikTok links | Nie otwieramy linków z Instagrama ani TikToka |
| social.body | Share the post to FitMeal, or paste the caption. We’ll keep the link as the source. | Udostępnij post do FitMeal albo wklej opis. Link zapiszemy jako źródło. |
| social.steps | In Instagram or TikTok, tap Share · Then choose FitMeal | W Instagramie lub TikToku dotknij Udostępnij · Potem wybierz FitMeal |
| other.link | Try another link | Spróbuj innego linku |
| source.kept | Saved with the recipe as its source. | Zapisany przy przepisie jako źródło. |
| source.notopened | Saved as the source. We don’t open it. | Zapisany jako źródło. Nie otwieramy go. |
| share.title | Add to FitMeal | Dodaj do FitMeal |
| share.caption | Caption we’ll use | Opis, którego użyjemy |
| share.more | Paste more text | Wklej więcej tekstu |
| share.note | We’ll use only this text. The link is saved as the source and never opened. | Użyjemy tylko tego tekstu. Link zapiszemy jako źródło i nie będziemy go otwierać. |
| share.empty.title | This post has no caption to use | Ten post nie ma opisu, którego możemy użyć |
| share.empty.body | Paste the recipe text, for example from the comments. We’ll keep the link as the source. | Wklej tekst przepisu, na przykład z komentarzy. Link zapiszemy jako źródło. |
| share.cta | Import recipe | Importuj przepis |
| preview.shared | Shared from instagram.com · caption only | Udostępnione z instagram.com · tylko opis |
| noprofile.title | We can’t check this recipe for your allergens | Nie możemy sprawdzić tego przepisu pod kątem Twoich alergenów |
| noprofile.body | Your profile isn’t on this phone, so we don’t know your allergies. Set it up to check, fit and plan this recipe. You can save it now. | Twojego profilu nie ma na tym telefonie, więc nie znamy Twoich alergii. Ustaw go, żeby sprawdzić, dopasować i zaplanować ten przepis. Zapisać możesz go już teraz. |
| noprofile.setup | Set up my profile | Ustaw mój profil |
| noprofile.restore | Restore from iCloud | Przywróć z iCloud |
| noprofile.foot | Saved recipes aren’t fitted or planned until the allergen check has run. | Zapisane przepisy nie są dopasowywane ani planowane, dopóki nie sprawdzimy alergenów. |

Plurals (PL): *Importuj 1 przepis / 2–4 przepisy / 5+ przepisów*; *został 1 import / zostały 2–4 importy / zostało 5+ importów* (22–24 → *importy*, 25–31 → *importów*); *1 strona / 2–4 strony / 5+ stron*. PL strings run about 25–35% longer: the fallback `Notice` titles wrap to two lines at 375 pt, which the layouts allow.

## Accessibility

- The fallback `Notice`s use `role="status"`, so VoiceOver reads them when they appear without interrupting. 26b is also `status`; only allergy conflicts (26) are alerts.
- In 25b each row is one checkbox whose label includes the pages (*Chicken Burrito Bowl, pages 12–13*), and the whole row is the hit target. The CTA label updates with the count.
- The URL in the source row truncates visually but VoiceOver reads it in full.

## For the API (backend-engineer)

- Link import responds with a reason when it can't parse: `no_recipe_data`, `tdm_opt_out`, `platform_not_fetched` (Instagram, TikTok and similar), `fetch_failed`. Each maps to 25d, 25e, 25f and the fetch-failure state. The URL is echoed back as `source_reference`.
- Import quota returns `remaining` for the current period so 25b can show it before sending.
- Import Preview carries `source.type` (`link`, `pdf_text`, `shared_caption`, `text`), `source.reference` and, for PDFs, the page range, to build the source line.
- The allergen check needs the profile snapshot sent from the phone; with none, the app shows 26b without calling it.
