import js from "@eslint/js";
import jsxA11y from "eslint-plugin-jsx-a11y";
import reactHooks from "eslint-plugin-react-hooks";
import globals from "globals";
import tseslint from "typescript-eslint";

export default tseslint.config(
  {
    ignores: [
      "dist",
      "dev-dist",
      "coverage",
      "playwright-report",
      "test-results",
      "src/api/schema.d.ts",
    ],
  },
  {
    extends: [js.configs.recommended, ...tseslint.configs.strictTypeChecked],
    files: ["**/*.{ts,tsx}"],
    languageOptions: {
      ecmaVersion: 2022,
      globals: globals.browser,
      parserOptions: { projectService: true, tsconfigRootDir: import.meta.dirname },
    },
    plugins: { "react-hooks": reactHooks, "jsx-a11y": jsxA11y },
    rules: {
      ...reactHooks.configs.recommended.rules,
      ...jsxA11y.flatConfigs.strict.rules,
      "@typescript-eslint/restrict-template-expressions": ["error", { allowNumber: true }],
      "@typescript-eslint/no-unused-vars": [
        "error",
        { argsIgnorePattern: "^_", varsIgnorePattern: "^_" },
      ],
    },
  },
  {
    files: ["**/*.test.{ts,tsx}", "e2e/**", "build/**", "*.config.ts"],
    languageOptions: { globals: globals.node },
    rules: {
      "@typescript-eslint/no-non-null-assertion": "off",
      "@typescript-eslint/require-await": "off",
    },
  },
  {
    files: ["scripts/**/*.mjs", "eslint.config.js"],
    extends: [js.configs.recommended],
    languageOptions: { globals: globals.node },
  },
);
