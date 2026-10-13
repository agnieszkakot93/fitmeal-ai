// Auth plumbing (Dev Plan §3.1). The access JWT lives only in this module's
// memory: never localStorage, sessionStorage or IndexedDB, so a reload or a
// new tab starts signed out until the refresh call succeeds. The refresh
// token is an HttpOnly, Secure, SameSite=Strict cookie scoped to /v1/auth;
// JavaScript never sees it, the browser attaches it to the refresh call.
//
// Sign-in (Google + email magic link, §1.1 Q1) will call setSession() with
// the pair the backend returns; any refresh_token in a body is ignored.
import type { components } from "./schema";

type TokenPair = components["schemas"]["TokenPair"];
type Fetch = (input: Request) => Promise<Response>;

export const REFRESH_PATH = "/v1/auth/refresh";
const AUTH_PREFIX = "/v1/auth/";

let accessToken: string | null = null;
let expiresAt = 0;
let refreshing: Promise<boolean> | null = null;

// Refresh this many ms before the access token expires.
const EXPIRY_SKEW_MS = 30_000;

export function getAccessToken(now = Date.now()): string | null {
  return accessToken && now < expiresAt - EXPIRY_SKEW_MS ? accessToken : null;
}

export function setSession(pair: Pick<TokenPair, "access_token" | "expires_in">, now = Date.now()) {
  accessToken = pair.access_token;
  expiresAt = now + pair.expires_in * 1000;
}

export function clearSession() {
  accessToken = null;
  expiresAt = 0;
}

const defaultFetch: Fetch = (input) => globalThis.fetch(input);

/**
 * Get a new access token with the refresh cookie. Concurrent callers share
 * one request, because each refresh token works only once.
 */
export function refreshSession(baseUrl: string, fetchImpl: Fetch = defaultFetch): Promise<boolean> {
  refreshing ??= (async () => {
    try {
      const res = await fetchImpl(
        new Request(new URL(REFRESH_PATH, baseUrl), {
          method: "POST",
          credentials: "include",
          headers: { Accept: "application/json" },
        }),
      );
      if (!res.ok) {
        clearSession();
        return false;
      }
      setSession((await res.json()) as TokenPair);
      return true;
    } catch {
      return false;
    } finally {
      refreshing = null;
    }
  })();
  return refreshing;
}

function withBearer(request: Request, token: string | null): Request {
  const out = new Request(request);
  if (token) out.headers.set("Authorization", `Bearer ${token}`);
  return out;
}

/**
 * A fetch for the generated client: adds the bearer token, and on a 401
 * refreshes once and retries. Auth endpoints are never retried.
 */
export function createAuthFetch(baseUrl: string, fetchImpl: Fetch = defaultFetch): Fetch {
  return async (request) => {
    const isAuthCall = new URL(request.url).pathname.startsWith(AUTH_PREFIX);
    const retry = isAuthCall ? null : request.clone();
    let token = getAccessToken();
    if (!token && accessToken && !isAuthCall && (await refreshSession(baseUrl, fetchImpl))) {
      token = getAccessToken();
    }
    const res = await fetchImpl(withBearer(request, token));
    if (res.status !== 401 || !retry) return res;
    if (!(await refreshSession(baseUrl, fetchImpl))) return res;
    return fetchImpl(withBearer(retry, getAccessToken()));
  };
}
