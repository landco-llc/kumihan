#!/usr/bin/env python3
"""G2 public trial installation is guarded, no-clobber and reversible.

The test does not require a live host or publish an endpoint. It exercises
temporary Lolipop-like public/private directory layouts with known fixtures.
"""
from __future__ import annotations

import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
INSTALL = ROOT / "tools" / "install_public_trial.sh"
ROLLBACK = ROOT / "tools" / "rollback_public_trial.sh"


def fixture(base: Path):
    web = base / "web"
    public = web / "kmhn"
    app = base / "kmhn-mcp-private" / "server"
    stage = app / ".kmhn-public-stage"
    public.mkdir(parents=True)
    stage.mkdir(parents=True)
    for name in ["public/index.php", "vendor/autoload.php", "runtime/config.php", "runtime/registry.json"]:
        p = app / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("test-fixture", encoding="utf-8")
    (app / "runtime/sessions").mkdir(parents=True)
    index = "<?php\n$entrypoint = '" + str(app / "public/index.php") + "';\nrequire $entrypoint;\n"
    htaccess = "Options -Indexes\nRewriteEngine On\nRewriteRule ^mcp/?$ index.php [L,QSA]\n"
    (stage / "index.php").write_text(index, encoding="utf-8")
    (stage / ".htaccess").write_text(htaccess, encoding="utf-8")
    return web, public, app, stage


def run(command: Path, web: Path, owner_flag: str = "YES") -> subprocess.CompletedProcess:
    env = dict(os.environ, FTP_ROOT=str(web))
    env["KUMIHAN_G2_TRIAL_APPROVED"] = owner_flag
    env["KUMIHAN_TRIAL_ROLLBACK_APPROVED"] = owner_flag
    return subprocess.run(["sh", str(command)], cwd=str(web), env=env,
                          text=True, capture_output=True, timeout=15)


class PublicTrialTests(unittest.TestCase):
    def test_install_then_exact_match_rollback(self):
        with tempfile.TemporaryDirectory() as td:
            web, public, app, stage = fixture(Path(td))
            result = run(INSTALL, web)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("G2_TWO_FILE_BOOTSTRAP_INSTALLED", result.stdout)
            self.assertIn("MCP_HTTPS_E2E_NOT_CHECKED", result.stdout)
            self.assertEqual((public / "index.php").read_bytes(), (stage / "index.php").read_bytes())
            self.assertEqual((public / ".htaccess").read_bytes(), (stage / ".htaccess").read_bytes())
            self.assertEqual({p.name for p in public.iterdir()}, {"index.php", ".htaccess"})
            self.assertTrue((app / "runtime/config.php").exists())
            rollback = run(ROLLBACK, web)
            self.assertEqual(rollback.returncode, 0, rollback.stdout + rollback.stderr)
            self.assertIn("G2_PUBLIC_TRIAL_ROLLED_BACK", rollback.stdout)
            self.assertIn("PRIVATE_RUNTIME_RETAINED", rollback.stdout)
            self.assertEqual(list(public.iterdir()), [])
            self.assertTrue((app / "vendor/autoload.php").exists())

    def test_missing_owner_approval_blocks_install(self):
        with tempfile.TemporaryDirectory() as td:
            web, public, _, _ = fixture(Path(td))
            result = run(INSTALL, web, "NO")
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(list(public.iterdir()), [])

    def test_other_public_content_blocks_without_change(self):
        with tempfile.TemporaryDirectory() as td:
            web, public, _, _ = fixture(Path(td))
            existing = public / "unrelated-site-file.txt"
            existing.write_text("preserve me", encoding="utf-8")
            result = run(INSTALL, web)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("PUBLIC_KMHN_NOT_EMPTY", result.stdout)
            self.assertEqual(existing.read_text(), "preserve me")
            self.assertFalse((public / "index.php").exists())

    def test_wrong_private_entrypoint_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            web, public, _, stage = fixture(Path(td))
            (stage / "index.php").write_text("<?php require '/wrong/path';", encoding="utf-8")
            result = run(INSTALL, web)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("STAGED_BOOTSTRAP_TARGET_MISMATCH", result.stdout)
            self.assertEqual(list(public.iterdir()), [])

    def test_rollback_refuses_modified_files(self):
        with tempfile.TemporaryDirectory() as td:
            web, public, app, _ = fixture(Path(td))
            self.assertEqual(run(INSTALL, web).returncode, 0)
            (public / "index.php").write_text("externally-modified", encoding="utf-8")
            result = run(ROLLBACK, web)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("PUBLIC_FILE_CONTENT_MISMATCH_STOP", result.stdout)
            self.assertTrue((public / "index.php").exists())
            self.assertTrue((public / ".htaccess").exists())
            self.assertTrue((app / "runtime/config.php").exists())


if __name__ == "__main__":
    unittest.main()
