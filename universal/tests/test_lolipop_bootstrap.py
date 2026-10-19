#!/usr/bin/env python3
"""Prove kmhn public-root mapping and rejection of unsafe Lolipop layouts."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SRC = Path(__file__).resolve().parents[1] / "tools" / "build_lolipop_bootstrap.py"
SPEC = importlib.util.spec_from_file_location("kmhn_lolipop_bootstrap", SRC)
builder = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(builder)


class LolipopBootstrapTests(unittest.TestCase):
    def test_public_layout_has_only_safe_loader_and_rewrite(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp) / "owner"
            ftp_root = home / "web"
            ftp_root.mkdir(parents=True)
            private_root = home / "kumihan-mcp-private" / "server"
            out = Path(temp) / "offline"
            manifest = builder.build(str(ftp_root), str(private_root), out)
            self.assertEqual(manifest["public_ftp_relative"], "kmhn")
            self.assertEqual(manifest["public_ssh_absolute"], str(ftp_root / "kmhn"))
            self.assertEqual(manifest["private_entrypoint"], str(private_root / "public" / "index.php"))
            expected = {"index.php", ".htaccess"}
            self.assertEqual({x.name for x in (out / "kmhn").iterdir()}, expected)
            index = (out / "kmhn" / "index.php").read_text(encoding="utf-8")
            self.assertIn(str(private_root / "public" / "index.php"), index)
            self.assertIn("KUMIHAN_MCP_NOT_DEPLOYED", index)
            self.assertNotIn("runtime/config.php", index)
            self.assertIn("RewriteRule ^mcp/?$", (out / "kmhn" / ".htaccess").read_text(encoding="utf-8"))
            self.assertEqual(json.loads((out / "placement.json").read_text())["status"], "offline_generated_not_deployed")
            self.assertFalse((ftp_root / "kmhn").exists(), "offline build must never write to the actual FTP root")

    def test_prevents_private_material_inside_default_web_root(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            web = root / "web"
            web.mkdir()
            for unsafe in (str(web), str(web / "kmhn" / "server"), str(web / "kmhn-secret")):
                with self.subTest(private=unsafe), self.assertRaises(ValueError):
                    builder.resolve_layout(str(web), unsafe)
            with self.assertRaises(ValueError):
                builder.build(str(web), str(root / "kmhn-private" / "server"), web / "tmp")

    def test_paths_need_absolute_and_nonroot(self):
        for ftp, private in [
            ("web", "/tmp/private/server"),
            ("/tmp/web", "../private"),
            ("/", "/tmp/private/server"),
            ("/tmp/web", "/"),
        ]:
            with self.subTest(ftp=ftp, private=private), self.assertRaises(ValueError):
                builder.resolve_layout(ftp, private)


if __name__ == "__main__":
    unittest.main()
