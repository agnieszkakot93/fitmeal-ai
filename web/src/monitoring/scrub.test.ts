import type { ErrorEvent } from "@sentry/react";
import { describe, expect, it } from "vitest";

import { redactUrl, scrubBreadcrumb, scrubEvent } from "./scrub";
import { isEuDsn } from "./sentry";

describe("redactUrl", () => {
  it.each([
    ["https://donut.test/recipes/kurczak-curry?portion=2#steps", "https://donut.test/recipes/:id"],
    ["/v1/plans/3f2b1c9e-1d2a-4b3c-8d4e-5f6a7b8c9d0e/slots/12", "/v1/plans/:id/slots/:id"],
    ["/v1/foods/piers-z-kurczaka", "/v1/foods/:id"],
    ["/today", "/today"],
  ])("%s → %s", (url, expected) => {
    expect(redactUrl(url)).toBe(expected);
  });
});

describe("scrubEvent", () => {
  it("drops the user, extras, request details and UI breadcrumbs", () => {
    const event = {
      type: undefined,
      message: "boom",
      user: { id: "u1", email: "a@b.test", ip_address: "1.2.3.4" },
      extra: { profile: { allergies: ["peanuts"] } },
      server_name: "host",
      request: {
        url: "https://donut.test/recipes/abc?q=1",
        headers: { Authorization: "Bearer secret" },
        cookies: { refresh_token: "secret" },
        data: '{"allergies":["peanuts"]}',
        query_string: "q=1",
      },
      breadcrumbs: [
        { category: "ui.click", message: "button: Orzeszki ziemne" },
        { category: "console", message: "profile {allergies: peanuts}" },
        {
          category: "fetch",
          data: { method: "PUT", url: "/v1/me/profile?x=1", status_code: 200, body: "peanuts" },
        },
        { category: "navigation", data: { from: "/recipes/abc", to: "/today" } },
      ],
    } as unknown as ErrorEvent;

    const out = JSON.stringify(scrubEvent(event));
    for (const secret of [
      "u1",
      "a@b.test",
      "1.2.3.4",
      "peanuts",
      "Orzeszki",
      "secret",
      "q=1",
      "host",
    ]) {
      expect(out).not.toContain(secret);
    }
    expect(event.request).toEqual({ url: "https://donut.test/recipes/:id" });
    expect(event.breadcrumbs).toEqual([
      { category: "fetch", data: { method: "PUT", url: "/v1/me/profile", status_code: 200 } },
      { category: "navigation", data: { from: "/recipes/:id", to: "/today" } },
    ]);
  });

  it("drops breadcrumbs without a category", () => {
    expect(scrubBreadcrumb({ message: "anything" })).toBeNull();
  });
});

describe("isEuDsn", () => {
  it("accepts only the EU (de) ingest region", () => {
    expect(isEuDsn("https://abc@o1.ingest.de.sentry.io/123")).toBe(true);
    expect(isEuDsn("https://abc@o1.ingest.us.sentry.io/123")).toBe(false);
    expect(isEuDsn("https://abc@o1.ingest.sentry.io/123")).toBe(false);
    expect(isEuDsn("not a url")).toBe(false);
  });
});
