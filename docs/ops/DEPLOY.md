# Deploying Donut to production

Single Hetzner VPS (2 vCPU / 4 GB, Development Plan D4, §6.4) running
`infra/docker-compose.prod.yml`: Caddy (TLS, headers, logs) → api (uvicorn) →
Postgres 16 + Redis. Backups: [BACKUPS.md](BACKUPS.md).

Steps marked **[PO]** need the Product Owner: they cost money, create an account, or
touch an external identity. Nothing in this repo buys or provisions anything.

## 0. Prerequisites

1. **[PO]** Buy a Hetzner Cloud VPS (CX22 or similar, Ubuntu 24.04 LTS, EU region),
   with an IPv4 + IPv6 and your SSH public key added at creation.
2. **[PO]** Domain and DNS: an `A` (and `AAAA`) record for the API host (placeholder
   `api.example.com`) pointing at the VPS. Per RENAME_PLAN, the real domain is only
   chosen in its own phase.
3. **[PO]** Cloudflare R2 account, bucket and scoped API token (BACKUPS.md §1).
4. **[PO]** Hetzner Cloud firewall (optional, in addition to ufw): allow 22/tcp
   (ideally from your IPs only), 80/tcp, 443/tcp, 443/udp.

## 1. First-time server setup (as root, once)

```sh
apt update && apt full-upgrade -y
adduser --disabled-password --gecos "" deploy
usermod -aG sudo deploy
install -d -m 700 -o deploy -g deploy /home/deploy/.ssh
cp /root/.ssh/authorized_keys /home/deploy/.ssh/ && chown deploy: /home/deploy/.ssh/authorized_keys
```

SSH hardening: `/etc/ssh/sshd_config.d/10-donut.conf`

```
PermitRootLogin no
PasswordAuthentication no
KbdInteractiveAuthentication no
PubkeyAuthentication yes
AllowUsers deploy
MaxAuthTries 3
```

`sshd -t && systemctl reload ssh`. Keep the current session open and test a new
login as `deploy` before closing it.

Firewall:

```sh
ufw default deny incoming && ufw default allow outgoing
ufw allow OpenSSH && ufw allow 80/tcp && ufw allow 443/tcp && ufw allow 443/udp
ufw enable
apt install -y fail2ban   # default sshd jail
```

Docker publishes ports by editing iptables directly, bypassing ufw. That is why only
Caddy has `ports:` in the prod compose file; never add `ports:` to postgres or redis.

Unattended security upgrades:

```sh
apt install -y unattended-upgrades
dpkg-reconfigure -plow unattended-upgrades
# /etc/apt/apt.conf.d/50unattended-upgrades: Automatic-Reboot "true"; Automatic-Reboot-Time "04:00";
```

Docker Engine + compose plugin (official repo, https://docs.docker.com/engine/install/ubuntu/),
then `usermod -aG docker deploy`. Log rotation for containers is set per service in the
compose file.

## 2. Secrets

- Secrets live only in `/opt/donut/infra/.env.prod` (`chmod 600`, owner `deploy`).
  Template: `infra/.env.prod.example`. Never commit it, never paste it into tickets or chat.
- Generate each secret with `openssl rand -hex 32`. `DONUT_JWT_SECRET` must not be the
  dev default (the app refuses it outside dev/test).
- A copy of `.env.prod` and the backup age **private** key go in the team password
  manager **[PO: choose/own it]**. The age private key is never stored on the VPS.
- Rotation: edit `.env.prod`, then `up -d` (recreates affected containers). Rotating
  `POSTGRES_PASSWORD` also needs `ALTER USER donut PASSWORD '...'` first, since Postgres
  only reads it on first init. Rotating `DONUT_JWT_SECRET` logs everyone out.

## 3. First deploy

```sh
sudo install -d -o deploy -g deploy /opt/donut
git clone <repo> /opt/donut && cd /opt/donut   # [PO] grant the server a read-only deploy key
cp infra/.env.prod.example infra/.env.prod && chmod 600 infra/.env.prod && $EDITOR infra/.env.prod
echo "$GHCR_READ_TOKEN" | docker login ghcr.io -u <user> --password-stdin   # read:packages only
alias dc='docker compose --env-file infra/.env.prod -f infra/docker-compose.prod.yml'
dc config -q && dc pull && dc up -d
dc ps && curl -fsS https://api.example.com/healthz
```

Startup order is enforced by compose: postgres/redis healthy → `migrate`
(`alembic upgrade head`, one-shot) exits 0 → api healthy → caddy. If `migrate` fails,
api does not start; read `dc logs migrate`.

Then install the backup timer (BACKUPS.md §2).

## 4. Routine deploy

1. CI (`.github/workflows/backend-image.yml`) pushes `ghcr.io/<owner>/donut-api:<git-sha>`
   on merge to `develop`/`main`.
2. On the server: `git pull` (for infra changes), set `DONUT_IMAGE=...:<new-sha>` in
   `.env.prod`, and record the previous value in `/opt/donut/DEPLOYS.log`.
3. Take an on-demand backup if the release contains migrations:
   `dc --profile backup run --rm backup`.
4. `dc pull && dc up -d`. The api is recreated after `migrate` succeeds; expect a few
   seconds of 502 while it restarts (single host, no blue/green yet).
5. Verify: `dc ps`, `curl -fsS https://api.example.com/healthz`, `dc logs --since 5m api`.

## 5. Rollback

- **No migration in the release:** set `DONUT_IMAGE` back to the previous SHA, `dc up -d`.
- **With a migration:** migrations should be backwards compatible (expand/contract), so
  the old image normally runs fine on the new schema; roll back the image only. If the
  schema itself must go back: `dc run --rm migrate alembic downgrade <revision>` with the
  **new** image (it has the downgrade), then switch to the old image.
- **Data damaged:** restore the pre-deploy backup (BACKUPS.md §4).

## 6. Notes and follow-ups

- **arq worker:** `backend/app` has no `WorkerSettings` and `arq` is not a dependency yet.
  The `worker` service is defined behind the `worker` profile and is not started. When
  the worker lands, deploy with `dc --profile worker up -d`.
- **API process model:** `uvicorn --workers $API_WORKERS` (gunicorn is not a dependency).
- **API docs in prod:** Caddy's CSP is `default-src 'none'`, which blocks Swagger UI
  assets at `/docs`. Intentional for an API-only host; the OpenAPI JSON stays available.
- **Logs:** uvicorn's access log is off; Caddy's access log strips query strings and all
  request/response headers (D8). Do not raise app log levels to debug in prod.
- **Caddy user:** runs as root in its container (to own its volume) with all capabilities
  dropped except `NET_BIND_SERVICE` and a read-only root FS. api, migrate and worker run
  as uid 1000 with a read-only FS; postgres and redis drop privileges in their entrypoints.
