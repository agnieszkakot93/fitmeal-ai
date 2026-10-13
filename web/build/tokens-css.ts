// Builds the CSS custom properties that bundle.css reads (`--surface`,
// `--space-4`, `--font-text` …) from design/design-system/tokens.json, so the
// tokens are used from the design system rather than copied into web/.

type Themed = { light: string; dark: string };
interface Token {
  name: string;
  value: string | Themed;
}
interface Group {
  tokens?: Token[];
}
export interface Tokens {
  type?: { families?: Record<string, string> };
  [group: string]: unknown;
}

const isThemed = (v: Token["value"]): v is Themed => typeof v === "object";

export function tokensToCss(tokens: Tokens): string {
  const light: string[] = [];
  const dark: string[] = [];
  for (const group of Object.values(tokens)) {
    const list = (group as Group | null)?.tokens;
    if (!Array.isArray(list)) continue;
    for (const { name, value } of list) {
      if (isThemed(value)) {
        light.push(`--${name}: ${value.light};`);
        dark.push(`--${name}: ${value.dark};`);
      } else {
        light.push(`--${name}: ${value};`);
      }
    }
  }
  for (const [family, stack] of Object.entries(tokens.type?.families ?? {})) {
    light.push(`--font-${family}: ${stack};`);
  }
  const block = (decls: string[]) => decls.map((d) => `  ${d}`).join("\n");
  return [
    `:root {\n  color-scheme: light dark;\n${block(light)}\n}`,
    // System dark mode, unless the user forced light in Profile (data-theme).
    `@media (prefers-color-scheme: dark) {\n:root:not([data-theme="light"]) {\n${block(dark)}\n}\n}`,
    `:root[data-theme="dark"] {\n  color-scheme: dark;\n${block(dark)}\n}`,
    `:root[data-theme="light"] {\n  color-scheme: light;\n}`,
  ].join("\n");
}
