import { screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it } from "vitest";

import { renderApp } from "../../test/render";
import { resetStorage } from "../../test/storage";
import { redirectFor, resumePath } from "./guard";
import type { GuardTarget } from "./guard";
import { completeStep, setUnder18 } from "./progress";
import { STEPS } from "./steps";
import type { StepId } from "./steps";

afterEach(async () => {
  await resetStorage();
});

const state = (completed: StepId[], { done = false, under18 = false } = {}) => ({
  completed,
  done,
  under18,
});
const step = (id: StepId): GuardTarget => ({ kind: "step", step: id });

describe("redirectFor", () => {
  it("lets a new user see Welcome and 02, but nothing past 02", () => {
    expect(redirectFor(step("welcome"), state([]))).toBeNull();
    expect(redirectFor(step("age"), state([]))).toBeNull();
    expect(redirectFor(step("consent"), state([]))).toBe("/onboarding/age");
    expect(redirectFor(step("calories"), state([]))).toBe("/onboarding/age");
  });

  it("sends deep links past an unconsented 03 back to 03", () => {
    expect(redirectFor(step("consent"), state(["age"]))).toBeNull();
    expect(redirectFor(step("allergies"), state(["age"]))).toBe("/onboarding/consent");
  });

  it("allows any step once 02 and 03 are done, optional ones included", () => {
    expect(redirectFor(step("cooking"), state(["age", "consent"]))).toBeNull();
  });

  it("keeps the app closed until onboarding is done", () => {
    expect(redirectFor({ kind: "app" }, state([]))).toBe("/onboarding");
    expect(redirectFor({ kind: "app" }, state(["age", "consent", "goal"]))).toBe(
      "/onboarding/body",
    );
    expect(redirectFor({ kind: "app" }, state(["age", "consent"], { done: true }))).toBeNull();
  });

  it("holds an under-18 user on the stop page, with Back to 02 only", () => {
    const under18 = state([], { under18: true });
    expect(redirectFor({ kind: "under18" }, under18)).toBeNull();
    expect(redirectFor(step("age"), under18)).toBeNull();
    expect(redirectFor(step("consent"), under18)).toBe("/onboarding/under-18");
    expect(redirectFor(step("welcome"), under18)).toBe("/onboarding/under-18");
    expect(redirectFor({ kind: "app" }, state([], { done: true, under18: true }))).toBe(
      "/onboarding/under-18",
    );
  });

  it("doesn't show the stop page to anyone else", () => {
    expect(redirectFor({ kind: "under18" }, state(["age"]))).toBe("/onboarding/consent");
  });

  it("resumes at the first step not completed", () => {
    expect(resumePath(state([]))).toBe("/onboarding");
    expect(resumePath(state(["age", "consent", "goal", "body"]))).toBe("/onboarding/calories");
  });
});

describe("onboarding routes", () => {
  it("sends a new user from / to Welcome", async () => {
    const { router } = await renderApp("/", { onboarded: false });
    expect(router.state.location.pathname).toBe("/onboarding");
    expect(screen.queryByRole("navigation")).toBeNull();
  });

  it("redirects a deep link to a later step back to 02", async () => {
    const { router } = await renderApp("/onboarding/calories", { onboarded: false });
    expect(router.state.location.pathname).toBe("/onboarding/age");
    expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent(
      "Czy masz ukończone 18 lat?",
    );
  });

  it("resumes where the user left off", async () => {
    await completeStep("age");
    await completeStep("consent");
    const { router } = await renderApp("/today", { onboarded: false });
    expect(router.state.location.pathname).toBe("/onboarding/goal");
    expect(screen.getByRole("progressbar", { name: "Krok 4 z 14" })).toBeInTheDocument();
  });

  it("keeps an under-18 user on the stop page", async () => {
    setUnder18(true);
    const { router } = await renderApp("/onboarding/consent", { onboarded: false });
    expect(router.state.location.pathname).toBe("/onboarding/under-18");
    expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent("Donut jest dla dorosłych");
    await userEvent.click(screen.getByRole("link", { name: "Wróć" }));
    expect(router.state.location.pathname).toBe("/onboarding/age");
  });

  it("walks Welcome → 02 → … → 14 and opens Today", async () => {
    const { router } = await renderApp("/onboarding", { onboarded: false });
    const clickTo = async (name: string, path: string) => {
      await userEvent.click(screen.getByRole("button", { name }));
      await waitFor(() => {
        expect(router.state.location.pathname).toBe(path);
      });
    };
    await clickTo("Zaczynamy", "/onboarding/age");
    await clickTo("Mam 18 lat lub więcej", "/onboarding/consent");
    const rest = STEPS.slice(3).map((s) => s.id);
    for (const id of rest) await clickTo("Dalej", `/onboarding/${id}`);
    await clickTo("Ułóż mój plan", "/today");
    await screen.findByRole("heading", { level: 1, name: "Dzisiaj" });
    expect(router.state.location.pathname).toBe("/today");
  });
});
