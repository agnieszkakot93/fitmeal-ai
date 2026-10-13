import type { TabId } from "../design-system";
import type { MessageId } from "../i18n/locale";

/** Per-route shell settings, read by <Layout> through `useMatches()`. */
export interface RouteHandle {
  /** Page title: the TopBar <h1> and document.title. */
  titleId: MessageId;
  /** Which main destination is current; none for Settings, Recipe, 404. */
  active?: TabId;
  /** false hides TabBar and SideNav (onboarding). */
  nav?: boolean;
  /** Onboarding column (container-onboarding). */
  narrow?: boolean;
}

export function isRouteHandle(value: unknown): value is RouteHandle {
  return typeof value === "object" && value !== null && "titleId" in value;
}
