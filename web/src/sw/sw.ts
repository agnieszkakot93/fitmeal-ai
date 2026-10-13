/// <reference lib="webworker" />
// Service worker skeleton (Workbox, injectManifest). Precaches the app shell
// and serves index.html for navigations so every route opens offline.
// Runtime caching of API data and the outbox sync come later (§3.1 Offline).
import {
  cleanupOutdatedCaches,
  createHandlerBoundToURL,
  precacheAndRoute,
} from "workbox-precaching";
import { NavigationRoute, registerRoute } from "workbox-routing";

declare const self: ServiceWorkerGlobalScope;

precacheAndRoute(self.__WB_MANIFEST);
cleanupOutdatedCaches();

// API calls never get the shell; they go to the network.
registerRoute(
  new NavigationRoute(createHandlerBoundToURL("/index.html"), {
    denylist: [/^\/v1\//, /^\/healthz$/],
  }),
);

self.addEventListener("message", (event) => {
  if ((event.data as { type?: string } | null)?.type === "SKIP_WAITING") void self.skipWaiting();
});
