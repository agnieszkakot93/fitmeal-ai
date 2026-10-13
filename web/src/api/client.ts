import createClient from "openapi-fetch";

import type { paths } from "./schema";
import { createAuthFetch } from "./session";

/** API origin: VITE_API_BASE_URL, else this page's origin. */
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || globalThis.location.origin;

/**
 * The typed API client. Paths, params and bodies come from src/api/schema.d.ts,
 * generated from the backend's OpenAPI (`pnpm api:generate`).
 */
export function createApiClient(baseUrl = API_BASE_URL) {
  return createClient<paths>({ baseUrl, fetch: createAuthFetch(baseUrl) });
}

export const api = createApiClient();
export type ApiClient = ReturnType<typeof createApiClient>;
