#!/usr/bin/env python3
"""Read-only symlink diagnostics for Lolipop's FTP document-root.

These tests intentionally simulate a full-tree find permission error without
declaring a missing scan to be clean, and protect unrelated public content.
"""
from __future__ import annotations

import os
from pathlib import Path
import shlex
import shutil
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "diagnose_public_symlink_scan.sh"


def invoke(root: Path, extra_path: str | None = None) -> tuple[int, str]:
    env = os.environ.copy()
    env["FTP_ROOT"] = str(root)
    if extra_path is not None:
        env["PATH"] = extra_path + os.pathsep + env.get("PATH", "")
    run = subprocess.run(["sh", str(SCRIPT)], env=env, capture_output=True, text=True, timeout=15)
    return run.returncode, run.stdout + run.stderr


class PublicSymlinkDiagnosticTests(unittest.TestCase):
    def test_empty_public_tree_is_clean_and_unchanged(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "web"
            (root / "kmhn").mkdir(parents=True)
            rc, output = invoke(root)
            self.assertEqual(rc, 0, output)
            self.assertIn("KMHN_SYMLINK_SCOPE_CLEAR", output)
            self.assertIn("WEB_WIDE_SYMLINK_SCAN_CLEAR", output)
            self.assertIn("NO_FILES_CHANGED", output)
            self.assertEqual(list((root / "kmhn").iterdir()), [])

    def test_other_site_symlink_does_not_hide_scoped_status(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "web"
            (root / "kmhn").mkdir(parents=True)
            (root / "other-site-link").symlink_to("/nonexistent")
            rc, output = invoke(root)
            self.assertEqual(rc, 0, output)
            self.assertIn("KMHN_SYMLINK_SCOPE_CLEAR", output)
            self.assertIn("WEB_WIDE_SYMLINKS_NEED_REVIEW", output)
            self.assertNotIn("WEB_WIDE_SYMLINK_SCAN_CLEAR", output)
            self.assertTrue((root / "other-site-link").is_symlink())

    def test_permission_denied_does_not_claim_clean_web(self):
        with tempfile.TemporaryDirectory() as td:
            parent = Path(td)
            root = parent / "web"
            (root / "kmhn").mkdir(parents=True)
            bin_dir = parent / "bin"
            bin_dir.mkdir()
            real_find = shutil.which("find")
            self.assertIsNotNone(real_find)
            stub = bin_dir / "find"
            stub.write_text(
                "#!/bin/sh\n"
                "case \"$1\" in\n"
                "  */web) echo 'find: Permission denied' >&2; exit 1 ;;\n"
                f"  *) exec {shlex.quote(str(real_find))} \"$@\" ;;\n"
                "esac\n", encoding="utf-8"
            )
            stub.chmod(0o755)
            rc, output = invoke(root, str(bin_dir))
            self.assertEqual(rc, 0, output)
            self.assertIn("KMHN_SYMLINK_SCOPE_CLEAR", output)
            self.assertIn("WEB_WIDE_SCAN_PERMISSION_LIMIT", output)
            self.assertIn("WEB_WIDE_SYMLINK_SCAN_INCOMPLETE", output)
            self.assertNotIn("WEB_WIDE_SYMLINK_SCAN_CLEAR", output)
            self.assertIn("NO_FILES_CHANGED", output)

    def test_symlink_inside_kmhn_requires_review(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "web"
            (root / "kmhn").mkdir(parents=True)
            (root / "kmhn" / "nested-link").symlink_to("/nonexistent")
            rc, output = invoke(root)
            self.assertEqual(rc, 0, output)
            self.assertIn("KMHN_SYMLINKS_NEED_REVIEW", output)
            self.assertIn("WEB_WIDE_SYMLINKS_NEED_REVIEW", output)


if __name__ == "__main__":
    unittest.main()
