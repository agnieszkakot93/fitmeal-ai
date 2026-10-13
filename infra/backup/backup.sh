#!/usr/bin/env bash
# Nightly logical backup: pg_dump (custom format) | age encrypt | upload to R2.
# Then deletes objects older than BACKUP_RETENTION_DAYS (the R2 lifecycle rule is the
# primary retention control; this is a second line of defence).
#
# Env: PGHOST PGUSER PGPASSWORD PGDATABASE R2_ACCOUNT_ID R2_BUCKET AWS_ACCESS_KEY_ID
#      AWS_SECRET_ACCESS_KEY BACKUP_AGE_RECIPIENT [BACKUP_PREFIX] [BACKUP_RETENTION_DAYS]
# Optional: BACKUP_LOCAL_DIR writes to a local directory instead of R2 (restore tests).
set -euo pipefail

: "${PGDATABASE:?}" "${BACKUP_AGE_RECIPIENT:?BACKUP_AGE_RECIPIENT must be an age public key}"
prefix="${BACKUP_PREFIX:-postgres}"
retention_days="${BACKUP_RETENTION_DAYS:-30}"
stamp="$(date -u +%Y-%m-%dT%H%M%SZ)"
name="${PGDATABASE}-${stamp}.dump.age"

log() { printf '%s backup: %s\n' "$(date -u +%FT%TZ)" "$*" >&2; }

dump() {
	pg_dump --format=custom --compress=6 --no-owner --no-privileges | age --encrypt --recipient "$BACKUP_AGE_RECIPIENT"
}

if [[ -n "${BACKUP_LOCAL_DIR:-}" ]]; then
	dump >"${BACKUP_LOCAL_DIR}/${name}"
	log "wrote ${BACKUP_LOCAL_DIR}/${name}"
	exit 0
fi

: "${R2_ACCOUNT_ID:?}" "${R2_BUCKET:?}" "${AWS_ACCESS_KEY_ID:?}" "${AWS_SECRET_ACCESS_KEY:?}"
export AWS_DEFAULT_REGION=auto
endpoint="https://${R2_ACCOUNT_ID}.r2.cloudflarestorage.com"
s3() { aws --endpoint-url "$endpoint" "$@"; }

# Write to /tmp first so a failed dump never uploads a truncated object.
tmp="/tmp/${name}"
trap 'rm -f "$tmp"' EXIT
dump >"$tmp"
size="$(stat -c %s "$tmp")"
if ((size < 1024)); then
	log "dump is only ${size} bytes, refusing to upload"
	exit 1
fi
s3 s3 cp --only-show-errors "$tmp" "s3://${R2_BUCKET}/${prefix}/${name}"
log "uploaded ${prefix}/${name} (${size} bytes)"

cutoff="$(date -u -d "-${retention_days} days" +%Y-%m-%dT%H%M%SZ)"
s3 s3api list-objects-v2 --bucket "$R2_BUCKET" --prefix "${prefix}/" \
	--query 'Contents[].Key' --output text | tr '\t' '\n' | while read -r key; do
	[[ -z "$key" || "$key" == "None" ]] && continue
	# keys look like <db>-<YYYY-MM-DDTHHMMSSZ>.dump.age; lexical compare works on that format
	key_stamp="$(basename "$key" .dump.age)"
	key_stamp="${key_stamp#"${PGDATABASE}"-}"
	if [[ "$key_stamp" < "$cutoff" ]]; then
		s3 s3 rm --only-show-errors "s3://${R2_BUCKET}/${key}"
		log "pruned ${key}"
	fi
done
