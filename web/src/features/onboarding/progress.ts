// Onboarding progress: Browser (app state) in the screen specs. Which steps
// are done lives in IndexedDB so a reload or a return visit resumes; the
// answers themselves are written by each step later. The under-18 stop is
// kept for the browser session only (onboarding.md, 02b), and a "No" is
// never stored anywhere else.
import { kvGet, kvSet } from "../../storage/db";
import type { StepId } from "./steps";

export interface OnboardingState {
  completed: StepId[];
  /** "Build my plan" was pressed: the app tabs open. */
  done: boolean;
}

const KEY = "onboarding";
const UNDER_18_KEY = "donut.under18";
const EMPTY: OnboardingState = { completed: [], done: false };

export async function loadProgress(): Promise<OnboardingState> {
  try {
    return (await kvGet<OnboardingState>(KEY)) ?? EMPTY;
  } catch {
    // IndexedDB blocked (private window): start over; step 03 handles the notice.
    return EMPTY;
  }
}

export async function completeStep(id: StepId): Promise<void> {
  const state = await loadProgress();
  if (!state.completed.includes(id)) {
    await kvSet(KEY, { ...state, completed: [...state.completed, id] });
  }
}

export async function finishOnboarding(): Promise<void> {
  await kvSet(KEY, { ...(await loadProgress()), done: true });
}

export function isUnder18(): boolean {
  try {
    return window.sessionStorage.getItem(UNDER_18_KEY) === "1";
  } catch {
    return false;
  }
}

export function setUnder18(value: boolean): void {
  try {
    if (value) window.sessionStorage.setItem(UNDER_18_KEY, "1");
    else window.sessionStorage.removeItem(UNDER_18_KEY);
  } catch {
    // Storage blocked: the stop lasts until the page is left.
  }
}
