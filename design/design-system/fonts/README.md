# Fonts

Self-hosted so the app makes no request to Google Fonts (strict CSP, Dev Plan §3.1; no visitor IPs sent to a third party). `components/bundle.css` declares them with `@font-face`.

| File | Family | Axes | Subset |
| --- | --- | --- | --- |
| `bricolage-grotesque-latin-opsz-normal.woff2` | Bricolage Grotesque | wght 200–800, opsz 12–96 | latin |
| `bricolage-grotesque-latin-ext-opsz-normal.woff2` | Bricolage Grotesque | wght 200–800, opsz 12–96 | latin-ext (Polish) |
| `figtree-latin-wght-normal.woff2` | Figtree | wght 300–900 | latin |
| `figtree-latin-ext-wght-normal.woff2` | Figtree | wght 300–900 | latin-ext (Polish) |

Source: the Fontsource packages `@fontsource-variable/bricolage-grotesque@5.3.0` and `@fontsource-variable/figtree@5.3.0`. Both fonts are licensed under the SIL Open Font License 1.1 (`OFL-*.txt`). To update, take the same files from a newer package version.
