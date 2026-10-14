"""Health profile admin commands (not wired into ``donut-admin`` yet: docs/dev/PARALLEL_WORK.md).

``python -m app.profile.cli rotate [--batch N]``: re-encrypt every profile still
under a retired key with the current one (docs/ops/PROFILE_KEY.md). Prints
counts and user ids only, never profile contents. Exit code 1 if any row is
left under another key.
"""

from __future__ import annotations

import argparse
import asyncio
import sys
import uuid

from app.core.db import get_sessionmaker
from app.profile import repository
from app.profile.crypto import KeyUnavailable, get_cipher


async def rotate(batch: int = 500) -> int:
    try:
        cipher = get_cipher()
    except KeyUnavailable as exc:
        print(f"no usable key: {exc}", file=sys.stderr)
        return 1
    done = 0
    failed: list[uuid.UUID] = []
    async with get_sessionmaker()() as session:
        while True:
            result = await repository.reencrypt(session, cipher, batch, skip=failed)
            await session.commit()
            done += result.done
            failed += result.failed
            if not result.done and not result.failed:
                break
        left = await repository.count_under_other_keys(session, cipher.key_id)
    print(f"re-encrypted {done} profile(s) under key {cipher.key_id!r}")
    for user_id in failed:
        print(f"could not decrypt the profile of user {user_id}", file=sys.stderr)
    if left:
        # failed rows, plus any a save held locked: run again to pick those up
        print(f"{left} profile(s) still under another key", file=sys.stderr)
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m app.profile.cli")
    sub = parser.add_subparsers(dest="command", required=True)
    rot = sub.add_parser("rotate", help="re-encrypt profiles under retired keys")
    rot.add_argument("--batch", type=int, default=500)
    args = parser.parse_args(argv)
    return asyncio.run(rotate(args.batch))


if __name__ == "__main__":
    sys.exit(main())
