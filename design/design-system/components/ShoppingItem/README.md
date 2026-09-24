# ShoppingItem

One aggregated line of the shopping list: name, total and package count.

**Props:** `name`, `qty` (*1.2 kg*), `packages` (*4 × 300 g cup*), `checked`, `extra` (*200 g*). `extra` is for a checked item whose required amount grew after a confirmed plan change: the row turns warning-tinted and shows *+200 g more to buy* instead of being struck through.

Group items under a `SectionHeader` per category, in the backend's store-walk order: vegetables, fruit, meat & fish, dairy & eggs, bakery, grains & pasta, legumes, nuts & seeds, oils & fats, condiments, spices, sweets & baking, beverages, other. Checkmarks work offline and survive regeneration.

`pantry` (*350 g at home*) and `price` (*~24 PLN*) are **Phase 2**, arriving with Pantry Mode and estimated pricing. Don't show them in the MVP.
