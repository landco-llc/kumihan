#!/usr/bin/env python3
"""Offline fixtures for 3 platform-specific plugin package generators."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

script = Path(__file__).resolve().parents[1] / "tools" / "build_adapters.py"
spec = importlib.util.spec_from_file_location("kumihan_adapters", script)
builder = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(builder)


class AdapterTests(unittest.TestCase):
    def test_rejects_unverified_placeholder_and_cleartext(self):
        for url in ("http://mcp.example.org/mcp", "https://mcp.example/mcp",
                    "https://localhost/mcp", "https://YOUR-DOMAIN.com/mcp",
                    "https://mcp.example.org/sse"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                builder.validate_endpoint(url)

    def test_builds_three_isolated_reproducible_host_packages(self):
        # Fixture URL is intentionally NOT a real deployment; the bundle stays temporary.
        fixture_url = "https://mcp.fixture-domain.example.org/mcp"
        with tempfile.TemporaryDirectory() as work:
            target = Path(work) / "dist"
            files = builder.build(fixture_url, target)
            self.assertEqual(len(files), 3)
            first = {x.name: x.read_bytes() for x in files}
            openai = json.loads((target / "openai" / "plugin.json").read_text())
            self.assertEqual(openai["name"], "kumihan")
            self.assertEqual(openai["extensions"]["com.openai"]["interface"]["displayName"], "KUMIHAN")
            mcp = json.loads((target / "openai" / "mcp.json").read_text())
            self.assertEqual(mcp["mcpServers"]["kumihan"]["url"], fixture_url)
            gemini = json.loads((target / "gemini-cli" / "gemini-extension.json").read_text())
            self.assertEqual(gemini["mcpServers"]["kumihan"]["httpUrl"], fixture_url)
            for zipfile_path in files:
                with zipfile.ZipFile(zipfile_path) as archive:
                    self.assertIn("skills/kumihan-universal/SKILL.md", archive.namelist())
            second = builder.build(fixture_url, target)
            for path in second:
                self.assertEqual(first[path.name], path.read_bytes(), path.name)


if __name__ == "__main__":
    unittest.main()
