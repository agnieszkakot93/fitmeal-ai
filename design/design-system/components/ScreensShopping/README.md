# Shopping, paywall and profile

Shopping list (store-walk order, no prices), Economy Mode v1 preview, Paywall, Profile with Privacy & health (profile on this phone, iCloud sync, plan reminder, export), Where your data lives, Delete account (and the iCloud-not-reachable case), composed from FitMeal components on 375 × 780 iPhone frames. A showcase page, not a component: build the SwiftUI screen from the components it uses.

## Profile › Privacy & health (37, 37b)

- **Nutrition profile · On this phone** opens *Where your data lives* (37b), a floating glass sheet with three places: on this phone (and the user's private iCloud), on our servers in the EU, and never collected.
- **Sync with iCloud** (`Toggle`, on by default, `cloud` icon). Turning it off asks once: *Turn off iCloud sync? Your profile stays on this phone and is removed from your iCloud. On a new phone you'll set it up again.* with *Turn off* / *Keep sync on*.
- **Plan reminder · Thursdays** mirrors the iOS permission:
  - allowed: value *On*; tapping opens a sheet with a `Toggle` to stop the reminder in the app;
  - not asked yet (the user chose *Not now* in onboarding): value *Off*; tapping shows the iOS permission prompt;
  - denied in iOS: subtitle *Off in iOS Settings* and an *Open Settings* link to the app's page in iOS Settings.
- **Export my data** says it combines the profile from this phone with the data from our servers. The profile part is added on the phone; nothing about it is uploaded to build the file.
- **Delete account** (38) names the three places: our servers, this phone and iCloud. If iCloud can't be reached, a neutral `Notice` says the profile may stay in iCloud and how to remove it. Consent records are kept only as long as the law requires.
- There is no analytics or marketing setting, because neither exists.

## Copy

| Key | EN | PL |
| --- | --- | --- |
| profile.nutrition | Nutrition profile · On this phone | Profil żywieniowy · Na tym telefonie |
| icloud.toggle | Sync with iCloud | Synchronizuj z iCloud |
| icloud.toggle.desc | Only in your private iCloud. We can’t read it. | Tylko w Twoim prywatnym iCloud. Nie mamy do niego dostępu. |
| icloud.off.confirm | Turn off iCloud sync? Your profile stays on this phone and is removed from your iCloud. On a new phone you’ll set it up again. | Wyłączyć synchronizację z iCloud? Profil zostanie na tym telefonie i zniknie z Twojego iCloud. Na nowym telefonie ustawisz go od nowa. |
| reminder.row | Plan reminder · Thursdays | Przypomnienie o planie · czwartki |
| reminder.on | On | Włączone |
| reminder.off | Off | Wyłączone |
| reminder.denied | Off in iOS Settings | Wyłączone w Ustawieniach iOS |
| reminder.open | Open Settings | Otwórz Ustawienia |
| export.note | Combines the profile from this phone with your data from our servers. | Łączy profil z tego telefonu z Twoimi danymi z naszych serwerów. |
| consent.withdraw.note | Withdrawing health-data consent deletes your account and your profile. | Wycofanie zgody na przetwarzanie danych o zdrowiu usuwa konto i profil. |
| where.title | Where your data lives | Gdzie są Twoje dane |
| where.phone | On this phone | Na tym telefonie |
| where.phone.body | Your nutrition profile: targets, allergies and other exclusions, and body data if you added it. It syncs to your private iCloud, which we can’t read, unless you turn sync off. We receive it only to build a plan or swap, and don’t keep it. | Twój profil żywieniowy: cele, alergie i inne wykluczenia oraz dane o ciele, jeśli zostały podane. Synchronizuje się z Twoim prywatnym iCloud, do którego nie mamy dostępu, chyba że wyłączysz synchronizację. Dostajemy go tylko na czas tworzenia planu lub zamiany i go nie zapisujemy. |
| where.server | On our servers in the EU | Na naszych serwerach w UE |
| where.server.body | Your account, plans, meals you mark as eaten, saved and imported recipes, shopping lists and the record of your consents. Recipe text you import is read by our AI provider in the EU; we keep only the recipe. | Twoje konto, plany, posiłki oznaczone jako zjedzone, zapisane i zaimportowane przepisy, listy zakupów oraz zapis Twoich zgód. Tekst importowanych przepisów odczytuje nasz dostawca AI w UE; zachowujemy tylko przepis. |
| where.never | Never collected | Nigdy nie zbieramy |
| where.never.body | Medical conditions, your date of birth, device or advertising identifiers, and your PDF files. | Informacji o chorobach, daty urodzenia, identyfikatorów urządzenia ani reklamowych, ani Twoich plików PDF. |
| where.policy | Read the privacy policy | Przeczytaj politykę prywatności |
| delete.body | Permanently deletes your account, plans and private imports from our servers, and your profile from this phone and iCloud. We keep a record of your consents only as long as the law requires. | Trwale usuwa konto, plany i prywatne importy z naszych serwerów oraz profil z tego telefonu i iCloud. Zapis Twoich zgód przechowujemy tylko tak długo, jak wymaga tego prawo. |
| delete.icloud.title | We can’t reach your iCloud right now | Nie możemy teraz połączyć się z Twoim iCloud |
| delete.icloud.body | Your profile may stay in your iCloud. To remove it, open iOS Settings › your name › iCloud › Manage Storage › FitMeal and delete its data. | Twój profil może zostać w Twoim iCloud. Aby go usunąć, otwórz Ustawienia iOS › Twoje imię i nazwisko › iCloud › Zarządzaj pamięcią › FitMeal i usuń dane. |

PL copy avoids gendered verb forms (*jeśli zostały podane*, not *jeśli je podałeś*). The iOS Settings path must match the installed iOS version's labels (mobile-architect to confirm).

## Accessibility

- The iCloud `Toggle` reads its description; the Plan reminder row reads its state (*Plan reminder, Thursdays, off in iOS Settings, Open Settings, button*).
- 37b is a sheet with a heading per place, so VoiceOver users can move by heading.
