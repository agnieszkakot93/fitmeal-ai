# Button

The call to action. Every size is a capsule, following iOS 26. Solid variants sit on content; glass variants float over it.

**Props:** `variant`:
- `primary`: a basil fill. Use one per screen, for example *Generate week* or *Add to this week*.
- `secondary`: bordered, for example *Recipe*.
- `quiet`: text only, for example *Swap* or *Keep as is*.
- `danger`: outlined, for example *Delete account*.
- `premium`: an ink fill, for example *Optimize with Premium*.
- `accent`: a paprika fill, reserved for *Import recipe*.
- *Sign in with Apple* is not a FitMeal button. The app uses Apple's own `SignInWithAppleButton` (black in light, white in dark), which the previews stand in for with a `premium` button.
- `glass`: Liquid Glass in `ink`, a floating secondary action.
- `glass-prominent`: basil-tinted glass, the one floating primary action (SwiftUI `.buttonStyle(.glassProminent)`).

`size`: `lg` (54px, the bottom call to action), `md` (44px) or `sm` (36px, inside cards). Also takes `icon`, `trailingIcon`, `block` and any `<button>` prop. Children are the label.

- Use glass only for controls that float above scrolling content, such as a sticky CTA, toolbars or a hero. Inside cards and lists, use the solid variants.
- Write labels as verbs in sentence case: *Generate week*, *See optimized recipe*. Never *OK* or *Submit*.
- Never put two primary buttons side by side. Pair a primary with a quiet or glass button.
