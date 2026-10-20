#!/usr/bin/env python3
"""CI checks that KUMIHAN's scoped preflight fails closed and does no writes.

This check intentionally does NOT turn unknown symlinks in other virtual-host
directories into a globally clean state; Owner must still inspect mappings.
"""
from __future__ import annotations

import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "preflight_public_bootstrap_scoped.sh"


def setup_layout(base: Path):
    web = base / "web"
    kmhn = web / "kmhn"
    private = base / "kmhn-mcp-private" / "server"
    kmhn.mkdir(parents=True)
    for name in ("public/index.php", "src/Registry.php", "vendor/autoload.php",
                 "runtime/config.php", "runtime/registry.json", "composer.lock"):
        path = private / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("test", encoding="utf-8")
    (private / "runtime" / "sessions").mkdir()
    return web, kmhn, private


def check(web: Path):
    env = dict(os.environ, FTP_ROOT=str(web))
    return subprocess.run(["sh", str(SCRIPT)], env=env, text=True,
                          capture_output=True, timeout=15)


class ScopedPublicPreflightTests(unittest.TestCase):
    def test_clean_scoped_filesystem_does_not_claim_sitewide_safety(self):
        with tempfile.TemporaryDirectory() as td:
            web, kmhn, private = setup_layout(Path(td))
            result = check(web)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("SCOPED_PREBOOTSTRAP_CHECKS_PASS", result.stdout)
            self.assertIn("KMHN_SYMLINK_SCOPE_CLEAR", result.stdout)
            self.assertIn("WEB_WIDE_SYMLINK_SCAN_NOT_ATTESTED", result.stdout)
            self.assertIn("OTHER_VHOST_UPLOAD_MAPPINGS_NEED_OWNER_REVIEW", result.stdout)
            self.assertIn("MCP_NOT_PUBLIC", result.stdout)
            self.assertEqual(list(kmhn.iterdir()), [])
            self.assertFalse((private / "runtime" / "sessions" / "marker").exists())

    def test_other_site_symlink_is_not_misrepresented_as_global_clearance(self):
        with tempfile.TemporaryDirectory() as td:
            web, kmhn, private = setup_layout(Path(td))
            (web / "another-site-link").symlink_to(private)
            result = check(web)
            self.assertEqual(result.returncode, 0)
            self.assertIn("WEB_WIDE_SYMLINK_SCAN_NOT_ATTESTED", result.stdout)
            self.assertIn("OTHER_VHOST_UPLOAD_MAPPINGS_NEED_OWNER_REVIEW", result.stdout)
            self.assertNotIn("WEB_WIDE_SYMLINK_SCAN_CLEAR", result.stdout)
            self.assertTrue((web / "another-site-link").is_symlink())

    def test_foreign_content_in_kmhn_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            web, kmhn, _ = setup_layout(Path(td))
            (kmhn / "already-live.txt").write_text("existing", encoding="utf-8")
            result = check(web)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("PUBLIC_KMHN_HAS_EXISTING_FILES", result.stdout)
            self.assertNotIn("SCOPED_PREBOOTSTRAP_CHECKS_PASS", result.stdout)

    def test_private_symlink_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            web, kmhn, private = setup_layout(Path(td))
            server = private
            backup = server.parent / "server_real"
            server.rename(backup)
            server.symlink_to(backup, target_is_directory=True)
            result = check(web)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("PRIVATE_SERVER_SYMLINK_BLOCKED", result.stdout)

    def test_private_required_file_missing_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            web, _, private = setup_layout(Path(td))
            (private / "vendor" / "autoload.php").unlink()
            result = check(web)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("PRIVATE_RUNTIME_FILE_MISSING", result.stdout)


if __name__ == "__main__":
    unittest.main()
