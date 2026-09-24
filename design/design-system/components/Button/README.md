# Button

The single call to action on a screen or card; five variants, three sizes.

**Props:** `variant` — `primary` (basil fill; one per screen: *Generate week*, *Add to this week*), `secondary` (bordered; *Recipe*), `quiet` (text only; *Swap*, *Keep as is*), `danger` (outlined; *Delete account*), `premium` (ink fill; *Optimize with Premium*), `accent` (paprika; reserved for *Import recipe*). `size` `lg` (54px, sticky screen CTA) · `md` (44px) · `sm` (36px, inside cards). `icon`, `trailingIcon`, `block`, plus any `<button>` prop. Children = the label.

- Labels are verbs in sentence case: *Generate week*, *See optimized recipe*, never *OK* or *Submit*.
- Paywall CTAs name the result, not the tier: *Unlock Economy Mode*, not *Go Premium*.
- Never put two primary buttons side by side — pair primary with quiet.
