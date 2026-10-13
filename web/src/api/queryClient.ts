import { QueryClient } from "@tanstack/react-query";

import { ApiError } from "./queries";

const MAX_RETRIES = 2;

/**
 * Server state (Dev Plan §3.1): cached data renders first, then refreshes.
 * Client errors (4xx) are answers, not outages, so they are never retried.
 *
 * The cache lives in memory for now. The offline copies of the plan, its
 * recipes and the shopping list go to IndexedDB (src/storage/db.ts) with the
 * offline work; auth tokens are never cached or persisted.
 */
export function createQueryClient(): QueryClient {
  return new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 60_000,
        retry: (failureCount, error) =>
          !(error instanceof ApiError && error.status < 500) && failureCount < MAX_RETRIES,
      },
      mutations: { retry: false },
    },
  });
}
