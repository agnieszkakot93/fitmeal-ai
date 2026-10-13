/// <reference types="vite/client" />

interface ImportMetaEnv {
  /** API origin. Empty: same origin (Caddy in production, the Vite proxy in dev). */
  readonly VITE_API_BASE_URL?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
