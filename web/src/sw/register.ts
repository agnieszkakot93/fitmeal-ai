import { registerSW } from "virtual:pwa-register";

/** Register the service worker in production builds. Updates wait for the next visit. */
export function registerServiceWorker(): void {
  if (!import.meta.env.PROD || !("serviceWorker" in navigator)) return;
  registerSW({ immediate: true });
}
