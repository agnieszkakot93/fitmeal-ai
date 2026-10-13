#!/usr/bin/env bash
# Restore an encrypted backup into a database.
#
#   restore.sh <source> <target-db>
#
# <source> is either an R2 key under BACKUP_PREFIX (e.g. donut-2026-10-13T020000Z.dump.age),
# the word `latest`, or a path to a local .dump.age file.
# The age private key is read from AGE_IDENTITY_FILE (mounted read-only, never baked in).
# The target database is dropped and recreated unless it is the live PGDATABASE, which
# requires RESTORE_INTO_LIVE=yes (disaster recovery only).
set -euo pipefail

source_ref="${1:?usage: restore.sh <key|latest|file> <target-db>}"
target_db="${2:?usage: restore.sh <key|latest|file> <target-db>}"
identity="${AGE_IDENTITY_FILE:?AGE_IDENTITY_FILE must point to the age private key}"
prefix="${BACKUP_PREFIX:-postgres}"

log() { printf '%s restore: %s\n' "$(date -u +%FT%TZ)" "$*" >&2; }

if [[ "$target_db" == "${PGDATABASE:-}" && "${RESTORE_INTO_LIVE:-}" != "yes" ]]; then
	log "refusing to overwrite live database ${target_db}; set RESTORE_INTO_LIVE=yes"
	exit 1
fi

fetch() {
	if [[ -f "$source_ref" ]]; then
		cat "$source_ref"
		return
	fi
	: "${R2_ACCOUNT_ID:?}" "${R2_BUCKET:?}"
	export AWS_DEFAULT_REGION=auto
	local endpoint="https://${R2_ACCOUNT_ID}.r2.cloudflarestorage.com" key="$source_ref"
	if [[ "$key" == "latest" ]]; then
		key="$(aws --endpoint-url "$endpoint" s3api list-objects-v2 --bucket "$R2_BUCKET" \
			--prefix "${prefix}/" --query 'sort_by(Contents,&Key)[-1].Key' --output text)"
		key="${key#"${prefix}"/}"
	fi
	log "fetching ${prefix}/${key}"
	aws --endpoint-url "$endpoint" s3 cp --only-show-errors "s3://${R2_BUCKET}/${prefix}/${key}" -
}

tmp="/tmp/restore.dump"
trap 'rm -f "$tmp"' EXIT
fetch | age --decrypt --identity "$identity" >"$tmp"

psql --dbname=postgres -v ON_ERROR_STOP=1 -q \
	-c "DROP DATABASE IF EXISTS \"${target_db}\" WITH (FORCE)" \
	-c "CREATE DATABASE \"${target_db}\""
pg_restore --dbname="$target_db" --no-owner --no-privileges --exit-on-error "$tmp"
log "restored into ${target_db}"
