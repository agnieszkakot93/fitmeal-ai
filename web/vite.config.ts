/// <reference types="vitest/config" />
import { readFileSync } from "node:fs";
import { fileURLToPath, URL } from "node:url";

import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";
import type { Plugin } from "vite";
import { VitePWA } from "vite-plugin-pwa";

import { tokensToCss } from "./build/tokens-css";
import type { Tokens } from "./build/tokens-css";

const repoRoot = fileURLToPath(new URL("..", import.meta.url));
const tokensPath = fileURLToPath(new URL("../design/design-system/tokens.json", import.meta.url));

/** `virtual:donut-tokens.css`: design tokens as CSS variables, built from tokens.json. */
function donutTokens(): Plugin {
  const id = "virtual:donut-tokens.css";
  const resolved = "\0" + id;
  return {
    name: "donut-tokens",
    resolveId: (source) => (source === id ? resolved : undefined),
    load(loadId) {
      if (loadId !== resolved) return undefined;
      this.addWatchFile(tokensPath);
      return tokensToCss(JSON.parse(readFileSync(tokensPath, "utf8")) as Tokens);
    },
  };
}

// The theme colour is the light `surface` token (design-system README, "Theme").
const surface = "#f6f3ec";

export default defineConfig({
  plugins: [
    donutTokens(),
    react(),
    VitePWA({
      strategies: "injectManifest",
      srcDir: "src/sw",
      filename: "sw.ts",
      registerType: "prompt",
      injectRegister: false,
      manifest: {
        name: "Donut",
        short_name: "Donut",
        description: "Twoje ulubione jedzenie. Twoje makro.",
        lang: "pl",
        start_url: "/today",
        scope: "/",
        display: "standalone",
        background_color: surface,
        theme_color: surface,
        icons: [
          { src: "/icons/icon-192.png", sizes: "192x192", type: "image/png" },
          { src: "/icons/icon-512.png", sizes: "512x512", type: "image/png" },
          {
            src: "/icons/icon-maskable-512.png",
            sizes: "512x512",
            type: "image/png",
            purpose: "maskable",
          },
        ],
      },
      injectManifest: {
        globPatterns: ["**/*.{js,css,html,svg,png,woff2,webmanifest}"],
      },
      devOptions: { enabled: false },
    }),
  ],
  server: {
    // The design system lives outside web/ (design/design-system/).
    fs: { allow: [repoRoot] },
    // Same origin in dev, so the /v1/auth refresh cookie works like in production.
    proxy: { "/v1": "http://127.0.0.1:8000", "/healthz": "http://127.0.0.1:8000" },
  },
  test: {
    environment: "jsdom",
    setupFiles: ["./src/test/setup.ts"],
    include: ["src/**/*.test.{ts,tsx}", "build/**/*.test.ts"],
    css: false,
  },
});
