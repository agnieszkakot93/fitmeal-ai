import { useQuery } from "@tanstack/react-query";

import { api } from "./client";
import type { ApiClient } from "./client";

/** A non-2xx API response, with the parsed error body. */
export class ApiError extends Error {
  constructor(
    readonly status: number,
    readonly body: unknown,
  ) {
    super(`API error ${status}`);
    this.name = "ApiError";
  }
}

/** Turn an openapi-fetch result into its data, or throw ApiError for a query to catch. */
export async function unwrap<T>(
  call: Promise<{ data?: T; error?: unknown; response: Response }>,
): Promise<T> {
  const { data, error, response } = await call;
  if (!response.ok || data === undefined) throw new ApiError(response.status, error);
  return data;
}

/** Query keys in one place so invalidation can't drift from the queries. */
export const queryKeys = {
  me: ["me"] as const,
};

/** The signed-in account (GET /v1/me). */
export function useMe(client: ApiClient = api) {
  return useQuery({
    queryKey: queryKeys.me,
    queryFn: ({ signal }) => unwrap(client.GET("/v1/me", { signal })),
  });
}
