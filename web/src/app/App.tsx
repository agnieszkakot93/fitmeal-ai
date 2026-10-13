import { RouterProvider, createBrowserRouter } from "react-router";

import { LocaleProvider } from "../i18n/LocaleProvider";
import { routes } from "./routes";

const router = createBrowserRouter(routes);

export function App() {
  return (
    <LocaleProvider>
      <RouterProvider router={router} />
    </LocaleProvider>
  );
}
