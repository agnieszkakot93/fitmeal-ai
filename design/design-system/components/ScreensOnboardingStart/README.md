# Onboarding 1 — welcome, new phone, age, consent, goal

Welcome, Restore profile and No profile on this phone (new phone), 18+ confirmation (and the under-18 stop), health-data consent with the health notice, Goal, composed from FitMeal components on 375 × 780 iPhone frames. A showcase page, not a component: build the SwiftUI screen from the components it uses.

## New-phone path (01b, 01c)

*I already have an account* → Sign in with Apple → 02 (18+) → 03 (consent) again, no skipping → then one of:

- **01b Restore profile**, the normal path: the profile is in the user's private iCloud (sync is on by default). A summary to check (calories, protein, number of exclusions with the allergy count), then *Restore my profile* or *Set up again*. Restoring keeps iCloud sync on. *Set up again* goes to steps 04–14 and replaces the iCloud copy when it's finished.
- **01c No profile on this phone**, the fallback when sync was off or iCloud can't be reached. Plans, recipes and the shopping list are back; plan, swap and the Import Preview allergen check are paused until the profile is set up (steps 04–14) or restored. The *Sync with iCloud* `Toggle` is shown (on by default). *Restore from iCloud* retries; if the user isn't signed in to iCloud, it says so and points to iOS Settings.

Neither screen shows `OnboardingProgress`: they aren't among the 14 steps.

## Copy

| Key | EN | PL |
| --- | --- | --- |
| consent.footnote | Your profile (targets, allergies, age, weight, height) stays on this phone and syncs to your private iCloud; you can turn sync off in Profile. We receive it only to build a plan or swap, and don’t keep it. It’s never sent to AI. Withdraw consent in Profile anytime. | Twój profil (cele, alergie, wiek, waga, wzrost) zostaje na tym telefonie i synchronizuje się z Twoim prywatnym iCloud; synchronizację wyłączysz w Profilu. Dostajemy go tylko na czas tworzenia planu lub zamiany i go nie zapisujemy. Nigdy nie trafia do AI. Zgodę wycofasz w Profilu w każdej chwili. |
| restore.title | Restore your profile? | Przywrócić Twój profil? |
| restore.body | We found your profile in your private iCloud. Check that it’s yours and up to date. | Znaleźliśmy Twój profil w Twoim prywatnym iCloud. Sprawdź, czy jest Twój i aktualny. |
| restore.kcal | 1,500 kcal a day | 1500 kcal dziennie |
| restore.protein | 115 g minimum | co najmniej 115 g |
| restore.exclusions | 4 · incl. 1 allergy | 4 · w tym 1 alergia |
| restore.saved | Saved in iCloud on 12 Sep 2026. You can change anything in Profile after restoring. | Zapisano w iCloud 12 wrz 2026. Po przywróceniu wszystko zmienisz w Profilu. |
| restore.cta | Restore my profile | Przywróć mój profil |
| restore.again | Set up again | Ustaw od nowa |
| restore.again.note | Setting up again replaces this profile in iCloud when you finish. | Nowy profil po zakończeniu zastąpi ten w iCloud. |
| noprofile.title | Set up your profile | Ustaw swój profil |
| noprofile.body | Your plans are back. Your profile isn’t on this phone. Restore it from iCloud or set it up again. | Twoje plany wróciły. Profilu nie ma na tym telefonie. Przywróć go z iCloud albo ustaw ponownie. |
| noprofile.paused | Paused until your profile is set up | Wstrzymane do czasu ustawienia profilu |
| noprofile.items | Building plans · Swapping meals and ingredients · Checking imported recipes for your allergens | Tworzenie planów · Zamiany posiłków i składników · Sprawdzanie importowanych przepisów pod kątem alergenów |
| icloud.toggle | Sync with iCloud | Synchronizuj z iCloud |
| icloud.toggle.desc | Only in your private iCloud. We can’t read it. | Tylko w Twoim prywatnym iCloud. Nie mamy do niego dostępu. |
| noprofile.cta | Set up my profile | Ustaw mój profil |
| noprofile.restore | Restore from iCloud | Przywróć z iCloud |
| noprofile.foot | Takes about 2 minutes. Your plans, recipes and shopping list work now. | Zajmie to około 2 minut. Plany, przepisy i lista zakupów już działają. |

Plurals (PL): *1 wykluczenie, 2–4 wykluczenia, 5+ wykluczeń*; *1 alergia, 2–4 alergie, 5+ alergii*.

## Accessibility

- 01b: the three summary rows read as one element each (*Exclusions, 4, including 1 allergy*). *Restore my profile* is the default action.
- 01c: the paused list is a `Notice` with `role="status"`, not an alert: nothing is wrong, something is missing.
