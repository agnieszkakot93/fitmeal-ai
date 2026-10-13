# ProfileFileCard

On web the nutrition profile (targets, exclusions with their tiers, optional body data) lives **only in this browser** (IndexedDB), with no server copy (D8 on web). This card says so in the agreed words and lets the user keep a copy: *Download my profile* saves `donut-profile-YYYY-MM-DD.json` (no account data inside), *Load a profile file* restores one. It is the web stand-in for iCloud sync and the iOS *Restore profile* screen.

Where it appears: Profile › *Where your data lives* (both actions); once after the first plan (download); the *No profile in this browser* state (load, next to *Set up my profile*); and after `navigator.storage.persist()` is refused (`persistRefused`).

**Props:**
- `mode`: `both` (default), `download` or `load`.
- `title`: defaults to *Nutrition profile · In this browser*.
- `lastDownloaded`: a formatted date (*12 Oct 2026* / *12 paź 2026*); otherwise *Not downloaded yet*.
- `persistRefused`: adds the storage-durability line.
- `error`: `true` for the standard invalid-file message, or a string for another read error.
- `onDownload()`, `onLoad(file)` (the chosen `File`; the app parses and validates it), `lang`.

**Flow after loading a file:** parse and validate (schema version, ranges, the 1,200 kcal floor), then open a `Dialog` *Use this profile?* with a summary: calories, protein minimum, and **every exclusion with its tier**, allergies first with the `danger` badge. Nothing is replaced until the user confirms. A file with an unknown version or out-of-range values is rejected with `error`, never half-loaded.

**States:** never downloaded, downloaded on a date, storage may be cleared, invalid file, load only, download only.

## Accessibility

- A `<section>` labelled by its title.
- *Download my profile* has the privacy line (*This file contains your allergies and targets. Keep it private.*) as its `aria-describedby`, so it's read with the button, and it is also visible right under the buttons.
- *Load a profile file* is a button that opens the native file picker (a hidden `<input type="file" accept=".json">`, out of the Tab order). Choosing the same file twice works (the input is reset).
- The invalid-file message is `role="alert"` and uses `danger` (an error), with an icon and text.
- After a successful load, the confirmation `Dialog` takes focus; after confirming, focus returns to the button.

## Copy

| Key | EN | PL |
| --- | --- | --- |
| `data.title` | Nutrition profile · In this browser | Profil żywieniowy · W tej przeglądarce |
| `data.where` | Your profile is saved in this browser on this device. We receive it only to build a plan or swap, and don't keep it. | Twój profil jest zapisany w tej przeglądarce na tym urządzeniu. Otrzymujemy go tylko, by ułożyć plan lub zamianę, i go nie przechowujemy. |
| `data.loss_warning` | If you clear this site's data, use private browsing, or switch browser or device, your profile won't be there. Download a copy to keep it safe. | Jeśli wyczyścisz dane tej witryny, użyjesz trybu prywatnego albo zmienisz przeglądarkę lub urządzenie, profilu tam nie będzie. Pobierz kopię, aby go nie stracić. |
| `data.download` | Download my profile | Pobierz mój profil |
| `data.download_warning` | This file contains your allergies and targets. Keep it private. | Ten plik zawiera Twoje alergie i cele. Nie udostępniaj go. |
| `data.load` | Load a profile file | Wczytaj plik profilu |
| `data.last_download` | Last downloaded {date} | Ostatnio pobrano: {date} |
| `data.never_downloaded` | Not downloaded yet | Jeszcze nie pobrano |
| `data.load_invalid` | We can't read this file. Choose a profile file downloaded from Donut (.json). | Nie możemy odczytać tego pliku. Wybierz plik profilu pobrany z Donut (.json). |
| `data.persist_refused` | Your browser may clear stored data when space runs low. Download a copy of your profile to be safe. | Przeglądarka może usunąć zapisane dane, gdy zabraknie miejsca. Pobierz kopię profilu na wszelki wypadek. |
| `data.load_confirm` | Use this profile? | Użyć tego profilu? |

## Do / don't

- Do use these exact sentences wherever the profile's location is explained.
- Do show the allergy list in full in the load confirmation.
- Don't say the profile is "backed up", "in the cloud", "on our servers" or "stored in the EU".
- Don't upload the file anywhere or read it on the server; parsing happens in the browser.
- Don't nag: the post-plan offer appears once; the Profile card is always there.
