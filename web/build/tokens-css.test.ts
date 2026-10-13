import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { describe, expect, it } from "vitest";

import { tokensToCss } from "./tokens-css";
import type { Tokens } from "./tokens-css";

const designSystem = resolve(dirname(fileURLToPath(import.meta.url)), "../../design/design-system");
const tokens = JSON.parse(readFileSync(resolve(designSystem, "tokens.json"), "utf8")) as Tokens;
const bundleCss = readFileSync(resolve(designSystem, "components/bundle.css"), "utf8");

describe("tokensToCss", () => {
  const css = tokensToCss(tokens);

  it("defines every variable bundle.css reads", () => {
    // --wk-cols is set inline by WeekTable, not a token.
    const used = new Set([...bundleCss.matchAll(/var\((--[a-z0-9-]+)/g)].map((m) => m[1]));
    used.delete("--wk-cols");
    const missing = [...used].filter((name) => !css.includes(`${name}:`));
    expect(missing).toEqual([]);
  });

  it("emits light values by default and dark values for dark mode", () => {
    expect(css).toMatch(/:root \{[^}]*--surface: #f6f3ec;/);
    expect(css).toMatch(/prefers-color-scheme: dark[\s\S]*--surface: #121612;/);
  });
});
