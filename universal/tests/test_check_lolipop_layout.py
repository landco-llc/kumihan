#!/usr/bin/env python3
"""Unit tests for non-mutating Lolipop account-root inspection."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest

TOOL = Path(__file__).resolve().parents[1] / "tools" / "check_lolipop_layout.py"
SPEC = importlib.util.spec_from_file_location("check_lolipop_layout", TOOL)
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(mod)


class LayoutCheckTests(unittest.TestCase):
    def test_matches_public_roles_without_writing_or_leaking_account_id(self):
        with tempfile.TemporaryDirectory() as work:
            parent = Path(work) / "sensitive-account-id"
            web = parent / "web"
            kmhn = web / "kmhn"
            kmhn.mkdir(parents=True)
            result = mod.inspect(str(web))
            self.assertTrue(result["ftp_root_role_confirmed"])
            self.assertTrue(result["public_folder_exists"])
            self.assertEqual(result["public_folder"], "kmhn")
            self.assertEqual(result["private_candidate_role"], "../kmhn-mcp-private/server")
            self.assertTrue(result["private_candidate_outside_ftp"])
            self.assertFalse(result["private_candidate_exists"])
            self.assertEqual(result["web_php_access_to_private"], "NOT_TESTED")
            self.assertEqual(result["effective_php85_for_subdomain"], "NOT_TESTED")
            self.assertNotIn("sensitive-account-id", str(result))
            self.assertFalse((parent / "kmhn-mcp-private").exists())

    def test_rejects_wrong_public_root_and_missing_paths(self):
        with tempfile.TemporaryDirectory() as work:
            home = Path(work)
            (home / "other").mkdir()
            for bad in ("relative/web", str(home / "missing"), str(home / "other")):
                with self.subTest(path=bad), self.assertRaises(ValueError):
                    mod.inspect(bad)


if __name__ == "__main__":
    unittest.main()
