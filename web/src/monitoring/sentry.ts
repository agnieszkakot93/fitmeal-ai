import * as Sentry from "@sentry/react";

import { scrubBreadcrumb, scrubEvent } from "./scrub";

/** Sentry's EU data region; events must not be stored elsewhere (Dev Plan §3.1). */
const EU_INGEST = /\.de\.sentry\.io$/;

export function isEuDsn(dsn: string): boolean {
  try {
    return EU_INGEST.test(new URL(dsn).hostname);
  } catch {
    return false;
  }
}

/**
 * Crash reporting for production builds. Off unless VITE_SENTRY_DSN is set to
 * an EU-region DSN. No tracing, no session replay, no PII collection, and every
 * event and breadcrumb goes through the scrubber.
 */
export function initSentry(dsn = import.meta.env.VITE_SENTRY_DSN): boolean {
  if (!import.meta.env.PROD || !dsn) return false;
  if (!isEuDsn(dsn)) {
    console.error("Sentry is off: VITE_SENTRY_DSN must use the EU region (*.de.sentry.io).");
    return false;
  }
  Sentry.init({
    dsn,
    release: import.meta.env.VITE_RELEASE,
    environment: import.meta.env.MODE,
    // Nothing about the person or the request beyond the error itself.
    dataCollection: {
      userInfo: false,
      cookies: false,
      httpHeaders: false,
      httpBodies: [],
      urlQueryParams: false,
      stackFrameVariables: false,
    },
    tracesSampleRate: 0,
    // UI clicks can contain allergies or targets; console crumbs are dropped by the scrubber.
    integrations: (defaults) => [
      ...defaults.filter((integration) => integration.name !== "Breadcrumbs"),
      Sentry.breadcrumbsIntegration({ dom: false, sentry: false }),
    ],
    beforeBreadcrumb: (crumb) => scrubBreadcrumb(crumb),
    beforeSend: (event) => scrubEvent(event),
  });
  return true;
}

export const reportError = (error: unknown) => Sentry.captureException(error);
