#!/usr/bin/env python3
"""Regression tests for modular registry generation without a running MCP server."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

BUILDER_PATH = Path(__file__).resolve().parents[1] / "tools" / "build_registry.py"
spec = importlib.util.spec_from_file_location("kumihan_registry_builder", BUILDER_PATH)
builder = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(builder)


class RegistryTests(unittest.TestCase):
    def test_current_repository_builds_all_listed_modules(self):
        registry = builder.build()
        mapping = builder.load_json(builder.PROJECT_ROOT / "universal" / "languages.json")["modules"]
        self.assertEqual(set(registry["modules"]), set(mapping))
        self.assertGreaterEqual(registry["module_count"], 20)
        for module_id, module in registry["modules"].items():
            with self.subTest(module=module_id):
                self.assertGreater(len(module["rules"]), 0)
                self.assertEqual(len(module["module_sha256"]), 64)
                self.assertEqual(module["status"], "preview_unverified")
                self.assertIn("source-preserving", "source-preserving")

    def test_add_and_update_modules_without_engine_changes(self):
        original = builder.PROJECT_ROOT
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            for code in ("xx", "yy"):
                stem = f"kumihan-{code}"
                module = repo / "plugins" / stem
                (module / "rules").mkdir(parents=True)
                (module / "skills" / stem).mkdir(parents=True)
                (module / "plugin.json").write_text(json.dumps({"name": stem, "version": "0.1.0", "description": "Test"}, ensure_ascii=False))
                (module / "rules" / "catalog.json").write_text(json.dumps([{"id": code + "-1", "title": "Preserve text"}]))
                (module / "skills" / stem / "SKILL.md").write_text("# " + stem)
            (repo / "universal").mkdir()
            mapping = {"modules": {
                "xx": {"source": "plugins/kumihan-xx"},
                "yy": {"source": "plugins/kumihan-yy"}
            }}
            (repo / "universal" / "languages.json").write_text(json.dumps(mapping))
            try:
                builder.PROJECT_ROOT = repo
                first = builder.build()
                self.assertEqual(first["module_count"], 2)
                sha_y = first["modules"]["yy"]["module_sha256"]
                plugin_x = repo / "plugins" / "kumihan-xx" / "plugin.json"
                plugin_x.write_text(json.dumps({"name": "kumihan-xx", "version": "0.1.1", "description": "Test"}))
                updated = builder.build()
                self.assertNotEqual(first["modules"]["xx"]["module_sha256"], updated["modules"]["xx"]["module_sha256"])
                self.assertEqual(sha_y, updated["modules"]["yy"]["module_sha256"])
            finally:
                builder.PROJECT_ROOT = original


if __name__ == "__main__":
    unittest.main()
