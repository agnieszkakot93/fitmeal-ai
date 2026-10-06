# Onboarding 3 — exclusions, preferences, cooking, sign-in

The 14 EU allergens with severity tiers, diet and free-text exclusions, Preferences, Cooking and budget with the Thursday plan reminder, Sign in with Apple, composed from FitMeal components on 375 × 780 iPhone frames. A showcase page, not a component: build the SwiftUI screen from the components it uses.

## Plan reminder (on the cooking step, 14)

The reminder offer sits on the existing cooking step, so onboarding stays at 14 steps. It is a card inside the scroll, below the cooking and budget choices; *Create my plan* stays the one sticky primary.

- *Remind me on Thursdays* shows the iOS notification permission prompt. *Not now* dismisses the card and doesn't ask again during onboarding.
- Allowed: the card turns into a `Badge` *Reminder on · Thursdays*. Denied or *Not now*: the card collapses to one footnote, *You can turn it on in Profile.* No second ask, no nagging.
- This is the only notification the app sends. There is no marketing push or email at launch, so there is no opt-in for one.

## Sign in (15)

Plans and recipes sync through the account. The profile stays on the phone and syncs only through the user's private iCloud (on by default, managed in Profile), so the sheet doesn't offer an iCloud choice.

## Copy

| Key | EN | PL |
| --- | --- | --- |
| reminder.title | Plan reminder | Przypomnienie o planie |
| reminder.body | Get a reminder on Thursdays to plan next week. It’s the only notification we send. | Przypomnimy Ci w czwartek o zaplanowaniu kolejnego tygodnia. To jedyne powiadomienie, jakie wysyłamy. |
| reminder.allow | Remind me on Thursdays | Przypominaj mi w czwartki |
| reminder.notnow | Not now | Nie teraz |
| reminder.on | Reminder on · Thursdays | Przypomnienie włączone · czwartki |
| reminder.later | You can turn it on in Profile. | Włączysz je w Profilu. |
| signin.body | Sign in to keep your plans and recipes. Your profile stays on this phone. Hiding your email is fine. | Zaloguj się, żeby zachować plany i przepisy. Twój profil zostaje na tym telefonie. Możesz ukryć swój e-mail. |
