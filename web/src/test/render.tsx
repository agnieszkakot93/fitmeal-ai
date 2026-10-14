import { render, waitFor } from "@testing-library/react";
import { RouterProvider, createMemoryRouter } from "react-router";

import { routes } from "../app/routes";
import { finishOnboarding } from "../features/onboarding/progress";
import { LocaleProvider } from "../i18n/LocaleProvider";
import type { Locale } from "../i18n/locale";

/**
 * Render the app at `path` and wait for the route loaders. By default the
 * user has finished onboarding, so the app tabs open.
 */
export async function renderApp(
  path: string,
  { locale, onboarded = true }: { locale?: Locale; onboarded?: boolean } = {},
) {
  if (onboarded) await finishOnboarding();
  const router = createMemoryRouter(routes, { initialEntries: [path] });
  const utils = render(
    <LocaleProvider initialLocale={locale}>
      <RouterProvider router={router} />
    </LocaleProvider>,
  );
  await waitFor(() => {
    if (!router.state.initialized || router.state.navigation.state !== "idle") {
      throw new Error("router still loading");
    }
  });
  await utils.findByRole("main");
  return { router, ...utils };
}
