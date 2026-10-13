import { ErrorBoundary } from "@sentry/react";
import { RouterProvider, createBrowserRouter } from "react-router";

import { LocaleProvider } from "../i18n/LocaleProvider";
import { ErrorFallback } from "./ErrorFallback";
import { routes } from "./routes";

const router = createBrowserRouter(routes);

export function App() {
  return (
    <LocaleProvider>
      {/* Route render errors go to the router's errorElement; this catches the rest. */}
      <ErrorBoundary fallback={<ErrorFallback />}>
        <RouterProvider router={router} />
      </ErrorBoundary>
    </LocaleProvider>
  );
}
