import { screen } from "@testing-library/react";
import { RouterProvider, createMemoryRouter } from "react-router";
import { render } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { LocaleProvider } from "../i18n/LocaleProvider";
import { RouteError } from "./ErrorFallback";

const reportError = vi.hoisted(() => vi.fn());
vi.mock("../monitoring/sentry", () => ({ reportError }));

function Boom(): never {
  throw new Error("render failed");
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe("RouteError", () => {
  it("reports the error and shows a translated fallback with a reload button", () => {
    vi.spyOn(console, "error").mockImplementation(() => undefined);
    const router = createMemoryRouter([
      { path: "/", element: <Boom />, errorElement: <RouteError /> },
    ]);
    render(
      <LocaleProvider initialLocale="pl">
        <RouterProvider router={router} />
      </LocaleProvider>,
    );
    expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent("Coś poszło nie tak");
    expect(screen.getByRole("button", { name: "Odśwież" })).toBeInTheDocument();
    expect(screen.getByRole("main")).toBeInTheDocument();
    expect(reportError).toHaveBeenCalledWith(expect.objectContaining({ message: "render failed" }));
  });
});
