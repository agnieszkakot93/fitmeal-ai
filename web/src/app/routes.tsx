import { Navigate } from "react-router";
import type { RouteObject } from "react-router";

import { NotFoundPage } from "../features/not-found/NotFoundPage";
import { OnboardingPage } from "../features/onboarding/OnboardingPage";
import { PlanPage } from "../features/plan/PlanPage";
import { RecipePage } from "../features/recipe/RecipePage";
import { SettingsPage } from "../features/settings/SettingsPage";
import { ShoppingPage } from "../features/shopping/ShoppingPage";
import { TodayPage } from "../features/today/TodayPage";
import type { RouteHandle } from "./handle";
import { Layout } from "./Layout";
import { paths } from "./paths";

const handle = (h: RouteHandle) => h;

/** One URL per screen (Dev Plan §3.1), so Back, refresh and deep links work. */
export const routes: RouteObject[] = [
  {
    element: <Layout />,
    children: [
      { index: true, element: <Navigate to={paths.today} replace /> },
      {
        path: "onboarding/*",
        element: <OnboardingPage />,
        handle: handle({ titleId: "onb.welcome.title", nav: false, narrow: true }),
      },
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
        path: "shopping",
        element: <ShoppingPage />,
        handle: handle({ titleId: "shopping.title", active: "shopping" }),
      },
      {
        path: "settings",
        element: <SettingsPage />,
        handle: handle({ titleId: "settings.title" }),
      },
      { path: "*", element: <NotFoundPage />, handle: handle({ titleId: "notFound.title" }) },
    ],
  },
];
