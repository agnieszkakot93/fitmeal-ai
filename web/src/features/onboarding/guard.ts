import { redirect } from "react-router";

import { paths } from "../../app/paths";
import { isUnder18, loadProgress } from "./progress";
import type { OnboardingState } from "./progress";
import { REQUIRED_STEPS, STEPS, UNDER_18_PATH, stepIndex, stepPath } from "./steps";
import type { StepId } from "./steps";

export type GuardTarget = { kind: "step"; step: StepId } | { kind: "under18" } | { kind: "app" };

interface GuardState extends OnboardingState {
  under18: boolean;
}

/** Where an unfinished onboarding reopens: the first step not yet completed. */
export function resumePath(state: OnboardingState): string {
  if (state.completed.length === 0) return stepPath("welcome");
  const next = STEPS.find((s) => s.id !== "welcome" && !state.completed.includes(s.id));
  return next ? stepPath(next.id) : stepPath("cooking");
}

/**
 * The redirect for a navigation, or null to let it through.
 * - Under 18 (this session): only the stop page and 02 (Back, for a mis-tap).
 * - Steps past an incomplete required step (02, 03) go back to it.
 * - The app tabs wait until onboarding is done.
 */
export function redirectFor(target: GuardTarget, state: GuardState): string | null {
  if (state.under18) {
    const allowed = target.kind === "under18" || (target.kind === "step" && target.step === "age");
    return allowed ? null : UNDER_18_PATH;
  }
  if (target.kind === "under18") return resumePath(state);
  if (target.kind === "app") return state.done ? null : resumePath(state);
  const missing = REQUIRED_STEPS.find((id) => !state.completed.includes(id));
  if (missing && stepIndex(target.step) > stepIndex(missing)) return stepPath(missing);
  return null;
}

/** A route loader that applies redirectFor() to the current progress. */
export function guard(target: GuardTarget) {
  return async () => {
    const to = redirectFor(target, { ...(await loadProgress()), under18: isUnder18() });
    return to ? redirect(to) : null;
  };
}

/** `/`: Today once onboarded, else wherever onboarding resumes. */
export async function rootLoader() {
  const to = redirectFor({ kind: "app" }, { ...(await loadProgress()), under18: isUnder18() });
  return redirect(to ?? paths.today);
}
