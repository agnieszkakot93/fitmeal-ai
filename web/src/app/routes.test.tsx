import { act, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it } from "vitest";

import { resetStorage } from "../test/storage";
import { renderApp } from "../test/render";

afterEach(async () => {
  await resetStorage();
});

const h1 = () => screen.getByRole("heading", { level: 1 });
// jsdom has no CSS, so both the phone TabBar and the SideNav are in the tree.
const mainNavs = () => screen.getAllByRole("navigation", { name: "Menu główne" });

describe("router", () => {
  it("redirects / to Today", async () => {
    const { router } = await renderApp("/");
    expect(await screen.findByRole("heading", { level: 1, name: "Dzisiaj" })).toBeInTheDocument();
    expect(router.state.location.pathname).toBe("/today");
  });

  it.each([
    ["/today", "Dzisiaj"],
    ["/plan", "Plan"],
    ["/shopping", "Zakupy"],
    ["/recipes/abc-123", "Przepis"],
    ["/settings", "Ustawienia"],
    ["/onboarding", "Twoje ulubione jedzenie. Twoje makro."],
    ["/no-such-page", "Nie znaleziono strony"],
  ])("%s renders its placeholder with title %s", async (path, title) => {
    await renderApp(path);
    expect(h1()).toHaveTextContent(title);
    expect(document.title).toBe(`${title} · Donut`);
    expect(screen.getByRole("main")).toBeInTheDocument();
  });

  it("marks the current destination in the main navigation", async () => {
    await renderApp("/plan");
    for (const nav of mainNavs()) {
      expect(within(nav).getByRole("link", { name: "Plan" })).toHaveAttribute(
        "aria-current",
        "page",
      );
      expect(within(nav).getByRole("link", { name: "Dzisiaj" })).not.toHaveAttribute(
        "aria-current",
      );
    }
  });

  it("marks no destination on Settings", async () => {
    await renderApp("/settings");
    for (const nav of mainNavs()) {
      expect(within(nav).queryByRole("link", { current: "page" })).toBeNull();
    }
  });

  it("hides the navigation during onboarding", async () => {
    await renderApp("/onboarding");
    expect(screen.queryByRole("navigation")).toBeNull();
  });

  it.each(["/today", "/"])("%s: the skip link to <main> is the first Tab stop", async (path) => {
    await renderApp(path);
    await screen.findByRole("heading", { level: 1, name: "Dzisiaj" });
    await userEvent.tab();
    const skip = screen.getByRole("link", { name: "Przejdź do treści" });
    expect(skip).toHaveFocus();
    expect(skip).toHaveAttribute("href", `#${screen.getByRole("main").id}`);
  });

  it("navigates client-side and moves focus to the new <h1>", async () => {
    const { router } = await renderApp("/today");
    const [nav] = mainNavs();
    await userEvent.click(within(nav!).getByRole("link", { name: "Plan" }));
    expect(router.state.location.pathname).toBe("/plan");
    expect(h1()).toHaveTextContent("Plan");
    expect(h1()).toHaveFocus();
  });

  it("opens Settings from the profile button and switches the language", async () => {
    const { router } = await renderApp("/today");
    await userEvent.click(screen.getAllByRole("button", { name: "Ustawienia" })[0]!);
    expect(router.state.location.pathname).toBe("/settings");

    await userEvent.selectOptions(screen.getByLabelText("Język"), "en");
    expect(h1()).toHaveTextContent("Settings");
    expect(document.documentElement.lang).toBe("en");
    expect(screen.getAllByRole("navigation", { name: "Main" }).length).toBeGreaterThan(0);
    expect(screen.getByLabelText("Language")).toHaveValue("en");

    await act(() => router.navigate("/today"));
    expect(h1()).toHaveTextContent("Today");
  });
});
