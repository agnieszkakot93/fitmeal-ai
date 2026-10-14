# Health profile key

The stored health profile (Development Plan D13, §7.2) is encrypted at column level with
AES-256-GCM under an application key that is kept apart from the database credentials. A
database dump, a backup or a leaked `POSTGRES_PASSWORD` alone exposes no profile.
Code: `backend/app/profile/crypto.py`.

- **Key:** base64 of 32 random bytes, in the Docker secret file
  `infra/secrets/donut_profile_key`, mounted into the `api` container only.
  It is not in `.env.prod`, so a leaked env file or `docker inspect` doesn't reveal it.
- **Key id:** `DONUT_PROFILE_KEY_ID` in `.env.prod`. It is stored with every row and
  names the key that encrypted it.
- **Retired keys:** `infra/secrets/donut_profile_old_keys`, JSON `{"<id>": "<base64 key>"}`.
  Set to `{}` outside a rotation.
- **No default, fail closed:** without a usable key `/v1/me/profile`, the export (for users
  with a profile) and plan generation from a stored profile answer
  `503 health_profile_unavailable`. Nothing is written in plaintext.

Outside Docker (dev, tests) the same settings come from the environment:
`DONUT_PROFILE_KEY`, `DONUT_PROFILE_KEY_ID`, `DONUT_PROFILE_OLD_KEYS`. Environment
variables win over secret files.

## First setup

```sh
cd /opt/donut
sudo install -d -m 700 -o 1000 -g 1000 infra/secrets
openssl rand -base64 32 | sudo install -m 400 -o 1000 -g 1000 /dev/stdin infra/secrets/donut_profile_key
echo '{}' | sudo install -m 400 -o 1000 -g 1000 /dev/stdin infra/secrets/donut_profile_old_keys
# .env.prod: DONUT_PROFILE_KEY_ID=1
dc up -d api
```

Use `-base64`, not `-hex`. A 64-character hex string is also valid base64, but it decodes
to 48 bytes and the app refuses it.

## Escrow

**Losing the key loses every stored profile.** It can't be recovered from the database
or the backups. Keep a copy of each key with its id in the team password manager
**[PO: owns it]**, in a separate entry from `.env.prod`. Keep retired keys there until
the rotation below reports nothing left and the last backup made before it has aged
out (`BACKUP_RETENTION_DAYS`). A restore from such a backup needs the old key again.

## Rotation

Rotate yearly, and at once if the key may have leaked.

1. Move the current key into `donut_profile_old_keys` under its id, for example
   `{"1": "<old key>"}`.
2. Write a new key to `donut_profile_key` (as in First setup) and set
   `DONUT_PROFILE_KEY_ID=2` in `.env.prod`. Store the new key in the password manager.
3. `dc up -d api`. New saves now use the new key, and old rows still decrypt.
4. Re-encrypt the old rows:
   `dc run --rm --no-deps api python -m app.profile.cli rotate`.
   It works in batches and prints counts and user ids only. It exits 1 while rows remain
   under another key: a row a save held locked (run it again), or a row that doesn't
   decrypt (listed by user id; investigate, never delete it blindly).
5. When it reports nothing left, set `donut_profile_old_keys` back to `{}` and run
   `dc up -d api`. Keep the old key in escrow as described above.

After a suspected leak, also treat the backups made with the old key as exposed if
they could have leaked together with it, and assess it as a personal data breach
(GDPR Art. 33).
