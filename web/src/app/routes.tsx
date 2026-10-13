import { redirect } from "react-router";
import type { RouteObject } from "react-router";

import { ImportPage } from "../features/import/ImportPage";
import { NotFoundPage } from "../features/not-found/NotFoundPage";
import { guard, rootLoader } from "../features/onboarding/guard";
import { OnboardingStepPage } from "../features/onboarding/OnboardingStepPage";
import { STEPS, stepPath } from "../features/onboarding/steps";
import { Under18Page } from "../features/onboarding/Under18Page";
import { PlanPage } from "../features/plan/PlanPage";
import { RecipePage } from "../features/recipe/RecipePage";
import { SettingsPage } from "../features/settings/SettingsPage";
import { ShoppingPage } from "../features/shopping/ShoppingPage";
import { TodayPage } from "../features/today/TodayPage";
import { RouteError } from "./ErrorFallback";
import type { RouteHandle } from "./handle";
import { Layout } from "./Layout";

const handle = (h: RouteHandle) => h;
const onboarding = { nav: false, narrow: true } as const;

/**
 * One URL per screen (Dev Plan §3.1), so Back, refresh and deep links work.
 * Loaders apply the onboarding guard before anything renders.
 */
export const routes: RouteObject[] = [
  {
    element: <Layout />,
    HydrateFallback: () => null,
    errorElement: <RouteError />,
    children: [
      { index: true, loader: rootLoader },
      {
        path: "onboarding",
        children: [
          ...STEPS.map(({ id, titleId }): RouteObject =>
            id === "welcome"
              ? {
                  index: true,
                  loader: guard({ kind: "step", step: id }),
                  element: <OnboardingStepPage key={id} step={id} />,
                  handle: handle({ titleId, ...onboarding }),
                }
              : {
                  path: id,
                  loader: guard({ kind: "step", step: id }),
                  element: <OnboardingStepPage key={id} step={id} />,
                  handle: handle({ titleId, ...onboarding }),
                },
          ),
          {
            path: "under-18",
            loader: guard({ kind: "under18" }),
            element: <Under18Page />,
            handle: handle({ titleId: "onb.age.stop.title", ...onboarding }),
          },
          { path: "*", loader: () => redirect(stepPath("welcome")) },
        ],
      },
      {
        // The app itself opens once onboarding is done.
        loader: guard({ kind: "app" }),
        children: [
          {
            path: "today",
            element: <TodayPage />,
            handle: handle({ titleId: "today.title", active: "today" }),
          },
          {
            path: "plan",
            element: <PlanPage />,
            handle: handle({ titleId: "plan.title", active: "plan" }),
          },
          {
            path: "recipes/:recipeId",
            element: <RecipePage />,
            handle: handle({ titleId: "recipe.title" }),
          },
          {
            path: "import",
            element: <ImportPage />,
            handle: handle({ titleId: "import.title" }),
          },
          {
            path: "shopping",
            element: <ShoppingPage />,
            handle: handle({ titleId: "shopping.title", active: "shopping" }),
          },
          {
            path: "settings",
            element: <SettingsPage />,
            handle: handle({ titleId: "settings.title" }),
          },
        ],
      },
      { path: "*", element: <NotFoundPage />, handle: handle({ titleId: "notFound.title" }) },
    ],
  },
];
