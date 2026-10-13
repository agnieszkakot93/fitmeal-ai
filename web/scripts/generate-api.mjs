// Export the backend's OpenAPI spec to web/openapi.json and generate the
// typed client schema from it. Runs backend code read-only: it imports the
// FastAPI app and calls app.openapi(); nothing under backend/ is written
// (uv may create backend/.venv, which is git-ignored).
import { execFileSync } from "node:child_process";
import { writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const web = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const backend = resolve(web, "../backend");
const specPath = resolve(web, "openapi.json");
const schemaPath = resolve(web, "src/api/schema.d.ts");

const exportSpec = [
  "import json, sys",
  "from app.main import app",
  "json.dump(app.openapi(), sys.stdout, indent=2, ensure_ascii=False)",
].join("\n");

const spec = execFileSync("uv", ["run", "--frozen", "python", "-c", exportSpec], {
  cwd: backend,
  encoding: "utf8",
  stdio: ["ignore", "pipe", "inherit"],
  maxBuffer: 64 * 1024 * 1024,
});
writeFileSync(specPath, spec + "\n");
console.log(`wrote ${specPath}`);

execFileSync(
  "pnpm",
  ["exec", "openapi-typescript", specPath, "--output", schemaPath, "--root-types"],
  { cwd: web, stdio: "inherit" },
);
