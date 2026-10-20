#!/usr/bin/env python3
"""Read-only verification of Lolipop account roles, without printing account paths.

Run from an SSH shell or authorized operator environment after cd'ing to the
full-path FTP root shown in the Lolipop account settings. This tool NEVER
creates directories, writes files, changes permissions or uploads a payload.

Use:
    cd '<full path from Lolipop Account Info>'
    python3 /path/to/kumihan/universal/tools/check_lolipop_layout.py --ftp-root "$PWD"

The full path must stay in operator-local variables, never be committed to Git.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys


def inspect(ftp_root: str) -> dict:
    original = Path(ftp_root)
    if not original.is_absolute():
        raise ValueError("FTP root must be an absolute path")
    if not original.exists():
        raise ValueError("FTP root does not exist")
    ftp = original.resolve(strict=True)
    if not ftp.is_dir() or ftp.name != "web":
        raise ValueError("Supplied FTP root must resolve to the account web directory")
    public = ftp / "kmhn"
    public_exists = public.is_dir()
    public_symlink = public.is_symlink()
    public_target_inside_ftp = False
    if public_exists:
        public_target_inside_ftp = public.resolve(strict=True).is_relative_to(ftp)
    account_parent = ftp.parent
    private_candidate = account_parent / "kmhn-mcp-private" / "server"
    private_candidate_real = private_candidate.resolve(strict=False)
    private_outside_ftp = not private_candidate_real.is_relative_to(ftp)
    if not private_outside_ftp:
        raise ValueError("Private candidate resolves inside public FTP root")
    if private_candidate.exists() and not private_candidate.is_dir():
        raise ValueError("Private candidate exists but is not a directory")
    return {
        "read_only_probe": True,
        "ftp_root_role_confirmed": True,
        "public_folder": "kmhn",
        "public_folder_exists": public_exists,
        "public_folder_symlink": public_symlink,
        "public_folder_resolves_inside_ftp": public_target_inside_ftp,
        "private_candidate_role": "../kmhn-mcp-private/server",
        "private_candidate_outside_ftp": private_outside_ftp,
        "private_candidate_exists": private_candidate.is_dir(),
        "account_parent_writable_as_ssh_user": os.access(account_parent, os.W_OK),
        "web_php_access_to_private": "NOT_TESTED",
        "other_http_document_roots": "NOT_TESTED",
        "effective_php85_for_subdomain": "NOT_TESTED",
        "host_mcp_status": "NOT_DEPLOYED",
        "no_absolute_account_paths_emitted": True,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--ftp-root", required=True)
    args = p.parse_args()
    try:
        print(json.dumps(inspect(args.ftp_root), ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError) as exc:
        print("LAYOUT_NOT_VERIFIED: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
