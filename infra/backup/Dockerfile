# Backup/restore toolbox: pg_dump/pg_restore 16, age (encryption), aws-cli (R2 S3 API).
FROM postgres:16-alpine

RUN apk add --no-cache age aws-cli bash coreutils

COPY backup.sh restore.sh /usr/local/bin/
RUN chmod 0755 /usr/local/bin/backup.sh /usr/local/bin/restore.sh

# `postgres` (uid 70) exists in the base image; no root needed at runtime
USER postgres
WORKDIR /tmp
ENTRYPOINT []
CMD ["backup.sh"]
