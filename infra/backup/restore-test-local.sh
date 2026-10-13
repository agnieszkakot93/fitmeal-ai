#!/usr/bin/env bash
# Exercises backup.sh + restore.sh end to end against the local dev stack:
#   docker compose -f infra/docker-compose.yml up -d postgres
#   infra/backup/restore-test-local.sh
# Uses a throwaway age key and a local directory instead of R2, restores into
# `donut_restore_test`, compares per-table row counts with `donut`, then drops it.
set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
network="${DEV_NETWORK:-donut_default}"
image="donut-backup:local"
# Read the dev password from the running dev container instead of hardcoding it.
pgpass="${PGPASSWORD:-$(docker compose -f "$here/../docker-compose.yml" exec -T postgres printenv POSTGRES_PASSWORD)}"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT
chmod 0777 "$work"

docker build -q -t "$image" "$here" >/dev/null

run() {
	docker run --rm --network "$network" -v "$work:/work" \
		-e PGHOST=postgres -e PGUSER=donut -e PGPASSWORD="$pgpass" -e PGDATABASE=donut \
		"$@"
}

run "$image" age-keygen -o /work/key.txt 2>/dev/null
recipient="$(run "$image" age-keygen -y /work/key.txt)"

run -e BACKUP_AGE_RECIPIENT="$recipient" -e BACKUP_LOCAL_DIR=/work "$image" backup.sh
dumps=("$work"/*.dump.age)
dump="$(basename "${dumps[0]}")"
run -e AGE_IDENTITY_FILE=/work/key.txt "$image" restore.sh "/work/${dump}" donut_restore_test

counts_sql="SELECT string_agg(format('%s=%s', relname, n), ',' ORDER BY relname) FROM (
  SELECT c.relname, (xpath('/row/n/text()', query_to_xml(format('SELECT count(*) AS n FROM %I.%I', n.nspname, c.relname), false, true, '')))[1]::text AS n
  FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
  WHERE c.relkind = 'r' AND n.nspname = 'public') t"
live="$(run "$image" psql -d donut -Atc "$counts_sql")"
restored="$(run "$image" psql -d donut_restore_test -Atc "$counts_sql")"
run "$image" psql -d postgres -qc 'DROP DATABASE donut_restore_test WITH (FORCE)'

if [[ "$live" != "$restored" ]]; then
	echo "RESTORE TEST FAILED: row counts differ" >&2
	echo "live:     $live" >&2
	echo "restored: $restored" >&2
	exit 1
fi
echo "restore test passed: ${live:-<no tables>}"
