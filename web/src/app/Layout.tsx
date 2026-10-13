import { useEffect, useRef } from "react";
import type { MouseEvent } from "react";
import {
  NavigationType,
  Outlet,
  useLocation,
  useMatches,
  useNavigate,
  useNavigationType,
} from "react-router";

import { AppShell, Avatar, TopBar } from "../design-system";
import type { TabId } from "../design-system";
import { useLocale } from "../i18n/LocaleProvider";
import { useT } from "../i18n/useT";
import { isRouteHandle } from "./handle";
import type { RouteHandle } from "./handle";
import { paths } from "./paths";

const TITLE_ID = "page-title";
const HREFS: Record<TabId, string> = {
  today: paths.today,
  plan: paths.plan,
  shopping: paths.shopping,
};
// The bundle marks Today current when `active` is missing; an id that matches
// no tab leaves every destination unmarked (Settings, Recipe, 404).
const NO_TAB = "none" as TabId;

function isPlainLeftClick(e: MouseEvent) {
  return e.button === 0 && !e.metaKey && !e.ctrlKey && !e.shiftKey && !e.altKey;
}

function useRouteHandle(): RouteHandle {
  const matches = useMatches();
  const handle = [...matches].reverse().find((m) => isRouteHandle(m.handle))?.handle;
  return isRouteHandle(handle) ? handle : { titleId: "notFound.title" };
}

/** The app frame: design-system AppShell, page title, focus on navigation. */
export function Layout() {
  const handle = useRouteHandle();
  const { locale } = useLocale();
  const t = useT();
  const navigate = useNavigate();
  const { pathname } = useLocation();
  const title = t(handle.titleId);
  const nav = handle.nav !== false;

  useEffect(() => {
    document.title = t("app.documentTitle", { page: title });
  }, [t, title]);

  // On route change, move focus to the new page's <h1> so screen readers
  // announce it. Not on the first load or a redirect (REPLACE, e.g. / to
  // /today): there the skip link stays the first thing Tab reaches.
  const navigationType = useNavigationType();
  // Track the path, not the location: the skip link only changes the hash.
  const lastPathname = useRef(pathname);
  useEffect(() => {
    if (lastPathname.current === pathname) return;
    lastPathname.current = pathname;
    if (navigationType === NavigationType.Replace) return;
    document.getElementById(TITLE_ID)?.focus();
  }, [pathname, navigationType]);

  const onNavigate = (id: TabId, e: MouseEvent) => {
    if (!isPlainLeftClick(e)) return; // let the browser open new tabs/windows
    e.preventDefault();
    void navigate(HREFS[id]);
  };

  // The bundle's Avatar is a <button> without an onClick prop; its click
  // (mouse, Enter or Space) bubbles to this wrapper.
  const avatar = (
    // eslint-disable-next-line jsx-a11y/click-events-have-key-events, jsx-a11y/no-static-element-interactions
    <span className="dn-avatar-link" onClick={() => void navigate(paths.settings)}>
      <Avatar label={t("shell.settings")} />
    </span>
  );

  return (
    <AppShell
      lang={locale}
      active={handle.active ?? NO_TAB}
      hrefs={HREFS}
      onNavigate={onNavigate}
      nav={nav}
      narrow={handle.narrow ?? false}
      avatar={nav ? avatar : undefined}
      header={
        <TopBar
          title={title}
          titleId={TITLE_ID}
          large={nav}
          lang={locale}
          avatar={nav ? avatar : undefined}
        />
      }
    >
      <Outlet />
    </AppShell>
  );
}
