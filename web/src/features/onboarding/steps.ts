import type { MessageId } from "../../i18n/locale";

/** Onboarding steps in order (docs/design/screens/onboarding.md, 01–14). */
export const STEPS = [
  { id: "welcome", titleId: "onb.welcome.title" },
  { id: "age", titleId: "onb.age.title" },
  { id: "consent", titleId: "onb.consent.title" },
  { id: "goal", titleId: "onb.goal.title" },
  { id: "body", titleId: "onb.body.title" },
  { id: "calories", titleId: "onb.kcal.title" },
  { id: "macros", titleId: "onb.macros.title" },
  { id: "meals", titleId: "onb.meals.title" },
  { id: "distribution", titleId: "onb.dist.title" },
  { id: "allergies", titleId: "onb.allergy.title" },
  { id: "restrictions", titleId: "onb.restr.title" },
  { id: "preferences", titleId: "onb.pref.title" },
  { id: "budget", titleId: "onb.budget.title" },
  { id: "cooking", titleId: "onb.cook.title" },
] as const satisfies readonly { id: string; titleId: MessageId }[];

export type StepId = (typeof STEPS)[number]["id"];

/** 02 and 03 can't be skipped, not even by editing the URL. */
export const REQUIRED_STEPS: readonly StepId[] = ["age", "consent"];

export const TOTAL_STEPS = STEPS.length;

export function stepIndex(id: StepId): number {
  return STEPS.findIndex((s) => s.id === id);
}

/** 1-based number shown as "Step n of 14"; Welcome is step 1 and shows no progress. */
export function stepNumber(id: StepId): number {
  return stepIndex(id) + 1;
}

export function nextStep(id: StepId): StepId | null {
  return STEPS[stepIndex(id) + 1]?.id ?? null;
}

export function stepPath(id: StepId): string {
  return id === "welcome" ? "/onboarding" : `/onboarding/${id}`;
}

export const UNDER_18_PATH = "/onboarding/under-18";
