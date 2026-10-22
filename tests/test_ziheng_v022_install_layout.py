"""Ziheng v0.2.2 unpacking instructions follow the actual fifteen ZIP layouts."""
import copy
import io
import json
import sys
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build_install_guides as guides  # noqa: E402
from release_ziheng_v022 import TAG, collect_source_archives  # noqa: E402


class ZihengV022InstallLayout(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # This verifies all three active host manifests and their archive bytes.
        cls.archives = collect_source_archives(ROOT)
        cls.layouts = json.loads((ROOT / "templates/install-guide/zip-layout.json").read_text())["archives"]

    def test_all_fifteen_layouts_match_inspected_archives(self):
        registered = {name for name in self.layouts
                      if name.startswith("kumihan-ziheng-") and name.endswith("-0.2.2.zip")}
        self.assertEqual(registered, set(self.archives))
        self.assertEqual(len(registered), 15)
        for name, raw in self.archives.items():
            with self.subTest(archive=name), zipfile.ZipFile(io.BytesIO(raw)) as archive:
                files = [row.filename for row in archive.infolist() if not row.is_dir()]
                roots = {path.split("/", 1)[0] for path in files}
                folder = (next(iter(roots)) if len(roots) == 1 and
                          all("/" in path for path in files) else None)
                self.assertEqual(self.layouts[name], folder)
                self.assertEqual(folder is None, "-gemini-" in name)

    def test_published_fixture_uses_correct_root_and_host_roles(self):
        # Simulated facts exercise rendering only; no publication record is written.
        facts = copy.deepcopy(guides.V.load())
        release = f"https://github.com/landco-llc/kumihan/releases/download/{TAG}/"
        facts["editions"]["zh-hant"].update(
            release_status="published", published_version="0.2.2",
            release_url=f"https://github.com/landco-llc/kumihan/releases/tag/{TAG}",
            verified_assets=[{"name": name, "url": release + name} for name in self.archives],
            verified_metadata=[{"name": "SHA256SUMS.txt", "url": release + "SHA256SUMS.txt"}],
        )
        with patch.object(guides.V, "load", return_value=facts):
            edition = guides.edition("zh-hant")
        for host in guides.HOSTS:
            data = edition["hosts"][host]
            self.assertIsNotNone(data["plugin"], host)
            self.assertEqual(set(data["skills"]), set(guides.SKILLS))
            self.assertEqual(data["plugin"][2], None if host == "gemini" else "kumihan-ziheng")
            for role, entry in data["skills"].items():
                folder = "kumihan-ziheng" + ("-" + role if role != "base" else "")
                self.assertEqual(entry[2], None if host == "gemini" else folder)
            for language in ("zh-hant", "en", "ja"):
                html = guides.render("zh-hant", host, language, edition)
                self.assertNotIn("{{", html)
                self.assertIn(data["plugin"][1], html)
        gemini = guides.render("zh-hant", "gemini", "en", edition)
        self.assertIn("Create an empty <code>kumihan-ziheng</code> folder and extract the ZIP into it.", gemini)


if __name__ == "__main__":
    unittest.main()
