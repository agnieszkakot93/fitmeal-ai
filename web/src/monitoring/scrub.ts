// What may reach Sentry (Dev Plan §3.1, GDPR table: legitimate interest,
// scrubbed): the error, its stack, the route shape and the app version.
// Never the user, request bodies, headers, cookies, query strings, ids in
// URLs, UI text or console output, because any of them can carry health
// data (allergies, targets) or tokens.
import type { Breadcrumb, ErrorEvent } from "@sentry/react";

const UUID = /[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/gi;
const NUMBER_SEGMENT = /\/\d+(?=\/|$)/g;
// Path segments after these are free-form ids or slugs (recipe names, food slugs).
const ID_PARENTS = /\/(recipes|foods|plans|imports|shopping)\/[^/?#]+/g;

/** Keep the route shape, drop ids, the query string and the fragment. */
export function redactUrl(url: string): string {
  const [noFragment = ""] = url.split("#");
  const [path = ""] = noFragment.split("?");
  return path.replace(UUID, ":id").replace(ID_PARENTS, "/$1/:id").replace(NUMBER_SEGMENT, "/:id");
}

const KEPT_BREADCRUMBS = new Set(["navigation", "fetch", "xhr"]);

export function scrubBreadcrumb(crumb: Breadcrumb): Breadcrumb | null {
  if (!crumb.category || !KEPT_BREADCRUMBS.has(crumb.category)) return null;
  const data = crumb.data ?? {};
  const kept: Record<string, unknown> = {};
  if (crumb.category === "navigation") {
    if (typeof data.from === "string") kept.from = redactUrl(data.from);
    if (typeof data.to === "string") kept.to = redactUrl(data.to);
  } else {
    if (typeof data.method === "string") kept.method = data.method;
    if (typeof data.status_code === "number") kept.status_code = data.status_code;
    if (typeof data.url === "string") kept.url = redactUrl(data.url);
  }
  return {
    category: crumb.category,
    type: crumb.type,
    level: crumb.level,
    timestamp: crumb.timestamp,
    data: kept,
  };
}

export function scrubEvent(event: ErrorEvent): ErrorEvent {
  delete event.user;
  delete event.extra;
  delete event.server_name;
  if (event.request) {
    event.request = event.request.url ? { url: redactUrl(event.request.url) } : {};
  }
  if (event.breadcrumbs) {
    event.breadcrumbs = event.breadcrumbs
      .map(scrubBreadcrumb)
      .filter((crumb): crumb is Breadcrumb => crumb !== null);
  }
  return event;
}
