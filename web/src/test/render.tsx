import { render } from "@testing-library/react";
import { RouterProvider, createMemoryRouter } from "react-router";

import { routes } from "../app/routes";
import { LocaleProvider } from "../i18n/LocaleProvider";
import type { Locale } from "../i18n/locale";

export function renderApp(path: string, initialLocale?: Locale) {
  const router = createMemoryRouter(routes, { initialEntries: [path] });
  const utils = render(
    <LocaleProvider initialLocale={initialLocale}>
      <RouterProvider router={router} />
    </LocaleProvider>,
  );
  return { router, ...utils };
}
