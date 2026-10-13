import { QueryClientProvider } from "@tanstack/react-query";
import { renderHook, waitFor } from "@testing-library/react";
import type { ReactNode } from "react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { createApiClient } from "./client";
import { ApiError, unwrap, useMe } from "./queries";
import { createQueryClient } from "./queryClient";
import { clearSession } from "./session";

const BASE = "https://api.example.test";

function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

function wrapper({ children }: { children: ReactNode }) {
  return <QueryClientProvider client={createQueryClient()}>{children}</QueryClientProvider>;
}

afterEach(() => {
  vi.restoreAllMocks();
  clearSession();
});

describe("unwrap", () => {
  it("returns the data of a 2xx response", async () => {
    const data = await unwrap(Promise.resolve({ data: { a: 1 }, response: json({ a: 1 }) }));
    expect(data).toEqual({ a: 1 });
  });

  it("throws ApiError with the status and body otherwise", async () => {
    const call = Promise.resolve({ error: { detail: "nope" }, response: json({}, 404) });
    await expect(unwrap(call)).rejects.toEqual(new ApiError(404, { detail: "nope" }));
  });
});

describe("useMe", () => {
  it("loads the account through the generated client", async () => {
    const me = { id: "u1", created_at: "2026-10-13T00:00:00Z" };
    const fetchSpy = vi.spyOn(globalThis, "fetch").mockResolvedValue(json(me));
    const { result } = renderHook(() => useMe(createApiClient(BASE)), { wrapper });
    await waitFor(() => {
      expect(result.current.isSuccess).toBe(true);
    });
    expect(result.current.data).toEqual(me);
    expect((fetchSpy.mock.calls[0]![0] as Request).url).toBe(`${BASE}/v1/me`);
  });

  it("does not retry a 4xx", async () => {
    // Signed out: no token, and the refresh after the 401 fails too.
    const fetchSpy = vi
      .spyOn(globalThis, "fetch")
      .mockImplementation(async () => json({ detail: "unauthorized" }, 401));
    const { result } = renderHook(() => useMe(createApiClient(BASE)), { wrapper });
    await waitFor(() => {
      expect(result.current.isError).toBe(true);
    });
    expect(result.current.error).toBeInstanceOf(ApiError);
    expect((result.current.error as ApiError).status).toBe(401);
    // the request, then one refresh attempt; no query retries
    expect(fetchSpy).toHaveBeenCalledTimes(2);
  });
});
