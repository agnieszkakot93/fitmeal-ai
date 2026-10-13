# Backups and restore

Nightly logical backup of Postgres: `pg_dump --format=custom`, encrypted with
[age](https://age-encryption.org) to a public key, uploaded to a Cloudflare R2 bucket
(S3 API), kept for 30 days. Code: `infra/backup/`. Redis holds only queues and caches and
is not backed up. `dc` below is the compose alias from DEPLOY.md §3.

Targets: RPO 24 h, RTO under 1 h for the expected data size.

## 1. One-time setup

1. **[PO]** Create a Cloudflare account with R2 enabled and a private bucket
   `donut-backups` (EU jurisdiction).
2. **[PO]** R2 lifecycle rule on the bucket: delete objects under `postgres/` after
   30 days. This is the primary retention control; `backup.sh` also prunes as a backstop.
3. **[PO]** R2 API token scoped to that bucket only, Object Read & Write. Put the access
   key id/secret and account id in `infra/.env.prod`.
4. Backup encryption key, generated on an admin laptop, **not** the server:
   ```sh
   age-keygen -o donut-backup.agekey   # prints the public key: age1...
   ```
   Put the public key in `BACKUP_AGE_RECIPIENT`. Store `donut-backup.agekey` in the
   password manager **[PO]** (and one offline copy). Without it backups are unreadable;
   with only the server compromised, past backups stay confidential.

## 2. Schedule

```sh
cd /opt/donut
dc --profile backup build backup
sudo cp infra/systemd/donut-backup.{service,timer} /etc/systemd/system/
sudo systemctl daemon-reload && sudo systemctl enable --now donut-backup.timer
sudo systemctl start donut-backup.service && journalctl -u donut-backup -n 20
```

Runs at 02:30 UTC (± 15 min). Failure shows in `systemctl --failed`; wiring that into
alerting is a follow-up (S9 monitoring).

## 3. Monthly restore test (first Monday of the month)

A backup is only real once it has been restored. On an admin machine with Docker,
the age private key and the R2 credentials:

```sh
docker build -t donut-backup:local infra/backup
docker network create donut-restore-test
docker run -d --rm --name pg-restore-test --network donut-restore-test \
  -e POSTGRES_USER=donut -e POSTGRES_HOST_AUTH_METHOD=trust postgres:16
docker run --rm --network donut-restore-test \
  -e PGHOST=pg-restore-test -e PGUSER=donut -e PGDATABASE=postgres \
  -e R2_ACCOUNT_ID -e R2_BUCKET -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY \
  -e AGE_IDENTITY_FILE=/key -v "$PWD/donut-backup.agekey:/key:ro" \
  donut-backup:local restore.sh latest donut
docker run --rm --network donut-restore-test donut-backup:local \
  psql -h pg-restore-test -U donut -d donut -c '\dt' -c 'SELECT version_num FROM alembic_version' -c 'SELECT count(*) FROM users'
docker stop pg-restore-test && docker network rm donut-restore-test
```

Pass criteria: restore exits 0, `alembic_version` matches production, key tables have
plausible row counts. Record date, backup key, duration and result in the ops log.
If it fails, treat it as an incident: backups are broken until proven otherwise.

The same scripts can be exercised against the local dev stack, no R2 needed:

```sh
docker compose -f infra/docker-compose.yml up -d postgres
infra/backup/restore-test-local.sh   # throwaway age key, compares per-table row counts
```

## 4. Disaster recovery (restore into production)

1. `dc stop caddy api worker` (stop writes).
2. Restore the chosen backup into the live database:
   ```sh
   dc --profile backup run --rm -e RESTORE_INTO_LIVE=yes -e AGE_IDENTITY_FILE=/key \
     -v /root/donut-backup.agekey:/key:ro backup restore.sh <key|latest> donut
   ```
   Copy the age key onto the server only for the duration, then `shred -u` it.
3. `dc up -d` (migrate brings the schema forward if the backup is older).
4. Verify `/healthz` and spot-check data.

On a fresh VPS: follow DEPLOY.md §1-3 first, then step 2 above.
