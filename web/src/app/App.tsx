import { ErrorBoundary } from "@sentry/react";
import { QueryClientProvider } from "@tanstack/react-query";
import { RouterProvider, createBrowserRouter } from "react-router";

import { createQueryClient } from "../api/queryClient";
import { LocaleProvider } from "../i18n/LocaleProvider";
import { ErrorFallback } from "./ErrorFallback";
import { routes } from "./routes";

const router = createBrowserRouter(routes);
const queryClient = createQueryClient();

export function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <LocaleProvider>
        {/* Route render errors go to the router's errorElement; this catches the rest. */}
        <ErrorBoundary fallback={<ErrorFallback />}>
          <RouterProvider router={router} />
        </ErrorBoundary>
      </LocaleProvider>
    </QueryClientProvider>
  );
}
