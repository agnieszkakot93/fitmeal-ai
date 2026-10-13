import { afterEach, describe, expect, it, vi } from "vitest";

import { createApiClient } from "./client";
import {
  clearSession,
  createAuthFetch,
  getAccessToken,
  refreshSession,
  setSession,
  signOut,
} from "./session";

const BASE = "https://api.example.test";

function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}
const pair = (access: string) => ({
  access_token: access,
  refresh_token: "must-be-ignored",
  token_type: "bearer",
  expires_in: 900,
  refresh_expires_in: 2_592_000,
});

afterEach(() => {
  clearSession();
  window.localStorage.clear();
  window.sessionStorage.clear();
});

describe("session", () => {
  it("keeps the access token in memory only", () => {
    const setItem = vi.spyOn(Storage.prototype, "setItem");
    setSession(pair("a1"));
    expect(getAccessToken()).toBe("a1");
    expect(setItem).not.toHaveBeenCalled();
    expect(window.localStorage.length + window.sessionStorage.length).toBe(0);
    setItem.mockRestore();
  });

  it("treats a token close to expiry as missing", () => {
    setSession({ access_token: "a1", expires_in: 900 }, 0);
    expect(getAccessToken(1_000)).toBe("a1");
    expect(getAccessToken(900_000)).toBeNull();
  });

  it("refreshes with the HttpOnly cookie, sending no token in the body", async () => {
    const fetchImpl = vi.fn(async (_req: Request) => json(pair("a2")));
    expect(await refreshSession(BASE, fetchImpl)).toBe(true);
    const req = fetchImpl.mock.calls[0]![0];
    expect(req.url).toBe(`${BASE}/v1/auth/refresh`);
    expect(req.method).toBe("POST");
    expect(req.credentials).toBe("include");
    expect(await req.text()).toBe("");
    expect(getAccessToken()).toBe("a2");
  });

  it("shares one refresh between concurrent callers", async () => {
    const fetchImpl = vi.fn(async (_req: Request) => json(pair("a3")));
    const results = await Promise.all([
      refreshSession(BASE, fetchImpl),
      refreshSession(BASE, fetchImpl),
    ]);
    expect(results).toEqual([true, true]);
    expect(fetchImpl).toHaveBeenCalledTimes(1);
  });

  it("signs out when the refresh is rejected", async () => {
    setSession(pair("old"));
    expect(await refreshSession(BASE, async () => json({ detail: "invalid" }, 401))).toBe(false);
    expect(getAccessToken()).toBeNull();
  });
});

describe("signOut", () => {
  it("drops the token and asks the server to revoke and clear the cookie", async () => {
    setSession(pair("a1"));
    const fetchImpl = vi.fn(async (_req: Request) => new Response(null, { status: 204 }));
    await signOut(BASE, fetchImpl);
    expect(getAccessToken()).toBeNull();
    const req = fetchImpl.mock.calls[0]![0];
    expect(req.url).toBe(`${BASE}/v1/auth/logout`);
    expect(req.method).toBe("POST");
    expect(req.credentials).toBe("include");
  });

  it("still signs out locally when offline", async () => {
    setSession(pair("a1"));
    await signOut(BASE, async () => {
      throw new TypeError("Failed to fetch");
    });
    expect(getAccessToken()).toBeNull();
  });
});

describe("createAuthFetch", () => {
  it("adds the bearer token", async () => {
    setSession(pair("a1"));
    const fetchImpl = vi.fn(async (_req: Request) => json({}));
    await createAuthFetch(BASE, fetchImpl)(new Request(`${BASE}/v1/me`));
    expect(fetchImpl.mock.calls[0]![0].headers.get("Authorization")).toBe("Bearer a1");
  });

  it("refreshes once on 401 and retries the request", async () => {
    setSession(pair("stale"));
    const fetchImpl = vi.fn(async (req: Request) => {
      if (req.url.endsWith("/v1/auth/refresh")) return json(pair("fresh"));
      return req.headers.get("Authorization") === "Bearer fresh"
        ? json({ ok: true })
        : json({ detail: "expired" }, 401);
    });
    const res = await createAuthFetch(
      BASE,
      fetchImpl,
    )(new Request(`${BASE}/v1/me/consents`, { method: "POST", body: '{"a":1}' }));
    expect(res.status).toBe(200);
    const retried = fetchImpl.mock.calls[2]![0];
    expect(await retried.text()).toBe('{"a":1}');
    expect(fetchImpl).toHaveBeenCalledTimes(3);
  });

  it("never retries auth endpoints", async () => {
    const fetchImpl = vi.fn(async (_req: Request) => json({ detail: "no" }, 401));
    const res = await createAuthFetch(
      BASE,
      fetchImpl,
    )(new Request(`${BASE}/v1/auth/refresh`, { method: "POST" }));
    expect(res.status).toBe(401);
    expect(fetchImpl).toHaveBeenCalledTimes(1);
  });
});

describe("generated client", () => {
  it("calls typed paths with the auth fetch", async () => {
    setSession(pair("a1"));
    const fetchSpy = vi.spyOn(globalThis, "fetch").mockResolvedValue(json({ results: [] }));
    const api = createApiClient(BASE);
    const { response } = await api.GET("/v1/foods/search", { params: { query: { q: "pierś" } } });
    expect(response.status).toBe(200);
    const req = fetchSpy.mock.calls[0]![0] as Request;
    expect(req.url).toBe(`${BASE}/v1/foods/search?q=pier%C5%9B`);
    expect(req.headers.get("Authorization")).toBe("Bearer a1");
    fetchSpy.mockRestore();
  });
});
