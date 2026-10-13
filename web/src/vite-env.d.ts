/// <reference types="vite/client" />

interface ImportMetaEnv {
  /** API origin. Empty: same origin (Caddy in production, the Vite proxy in dev). */
  readonly VITE_API_BASE_URL?: string;
  /** Sentry DSN, EU region only (*.de.sentry.io). Unset: crash reporting is off. */
  readonly VITE_SENTRY_DSN?: string;
  /** Release name shown in Sentry, set by the deploy (e.g. the git SHA). */
  readonly VITE_RELEASE?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
