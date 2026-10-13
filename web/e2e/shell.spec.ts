import AxeBuilder from "@axe-core/playwright";
import { expect, test } from "@playwright/test";
import type { Page } from "@playwright/test";

// The design-system fonts come from Google Fonts; keep the smoke test offline.
test.beforeEach(async ({ page }) => {
  await page.route(/fonts\.(googleapis|gstatic)\.com/, (route) => route.abort());
});

const STEP_COUNT_AFTER_CONSENT = 11; // 03 Consent … 13 Budget each have "Dalej"

/** Click through onboarding (placeholder steps) so the app tabs open. */
async function finishOnboarding(page: Page) {
  await page.goto("/onboarding");
  await page.getByRole("button", { name: "Zaczynamy" }).click();
  await page.getByRole("button", { name: "Mam 18 lat lub więcej" }).click();
  for (let i = 0; i < STEP_COUNT_AFTER_CONSENT; i++) {
    const before = page.url();
    await page.getByRole("button", { name: "Dalej" }).click();
    await expect(page).not.toHaveURL(before);
  }
  await page.getByRole("button", { name: "Ułóż mój plan" }).click();
  await expect(page).toHaveURL(/\/today$/);
}

test("a new visitor lands in onboarding and can't deep-link past 02", async ({ page }) => {
  await page.goto("/");
  await expect(page).toHaveURL(/\/onboarding$/);
  await expect(page.getByRole("navigation")).toHaveCount(0);
  await page.goto("/onboarding/allergies");
  await expect(page).toHaveURL(/\/onboarding\/age$/);
  await page.goto("/plan");
  await expect(page).toHaveURL(/\/onboarding$/);
});

test("an under-18 answer stops onboarding for the session", async ({ page }) => {
  await page.goto("/onboarding/age");
  await page.getByRole("button", { name: "Mam mniej niż 18 lat" }).click();
  await expect(
    page.getByRole("heading", { level: 1, name: "Donut jest dla dorosłych" }),
  ).toBeVisible();
  await page.goto("/onboarding/consent");
  await expect(page).toHaveURL(/\/onboarding\/under-18$/);
});

test.describe("after onboarding", () => {
  test.beforeEach(async ({ page }) => {
    await finishOnboarding(page);
  });

  test("loads the shell in Polish with landmarks and a skip link", async ({ page }) => {
    await page.goto("/");
    await expect(page).toHaveURL(/\/today$/);
    await expect(page.locator("html")).toHaveAttribute("lang", "pl");
    await expect(page.getByRole("heading", { level: 1, name: "Dzisiaj" })).toBeVisible();
    await expect(page).toHaveTitle("Dzisiaj · Donut");
    await expect(page.getByRole("main")).toBeVisible();
    // Exactly one main navigation is exposed at each size (TabBar or SideNav).
    await expect(page.getByRole("navigation", { name: "Menu główne" })).toHaveCount(1);

    await page.keyboard.press("Tab");
    const skip = page.getByRole("link", { name: "Przejdź do treści" });
    await expect(skip).toBeFocused();
    await expect(skip).toBeVisible();
    await page.keyboard.press("Enter");
    await expect(page.getByRole("main")).toBeFocused();
  });

  test("navigates between tabs and switches the language", async ({ page }) => {
    await page.goto("/today");
    const nav = page.getByRole("navigation", { name: "Menu główne" });
    await nav.getByRole("link", { name: "Plan" }).click();
    await expect(page).toHaveURL(/\/plan$/);
    await expect(page.getByRole("heading", { level: 1, name: "Plan" })).toBeFocused();

    await page.getByRole("button", { name: "Ustawienia" }).click();
    await expect(page).toHaveURL(/\/settings$/);
    await page.getByLabel("Język").selectOption("en");

    await expect(page.locator("html")).toHaveAttribute("lang", "en");
    await expect(page.getByRole("heading", { level: 1, name: "Settings" })).toBeVisible();
    await expect(page).toHaveTitle("Settings · Donut");
    await expect(page.getByRole("navigation", { name: "Main" })).toHaveCount(1);

    // The choice survives a reload.
    await page.reload();
    await expect(page.locator("html")).toHaveAttribute("lang", "en");
    await expect(page.getByRole("heading", { level: 1, name: "Settings" })).toBeVisible();
  });

  test("deep links and unknown URLs render inside the shell", async ({ page }) => {
    await page.goto("/recipes/abc-123");
    await expect(page.getByRole("heading", { level: 1, name: "Przepis" })).toBeVisible();
    await page.goto("/onboarding");
    await expect(page.getByRole("navigation")).toHaveCount(0);
    await page.goto("/nope");
    await expect(
      page.getByRole("heading", { level: 1, name: "Nie znaleziono strony" }),
    ).toBeVisible();
  });

  for (const path of ["/today", "/settings", "/onboarding"]) {
    test(`has no WCAG 2.2 AA violations on ${path}`, async ({ page }) => {
      await page.goto(path);
      await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
      const results = await new AxeBuilder({ page })
        .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"])
        .analyze();
      expect(results.violations).toEqual([]);
    });
  }

  test("ships a manifest and registers the service worker", async ({ page }) => {
    await page.goto("/today");
    const manifest = await page.request.get("/manifest.webmanifest");
    expect(manifest.ok()).toBe(true);
    expect(await manifest.json()).toMatchObject({ name: "Donut", start_url: "/today" });
    const scope = await page.evaluate(async () => (await navigator.serviceWorker.ready).scope);
    expect(scope).toMatch(/\/$/);
  });
});
