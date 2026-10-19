"""The privacy policy (tools/build_privacy.py): one page with every KUMIHAN language, linked from every footer."""
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build_privacy  # noqa: E402
import site_footer  # noqa: E402
from test_site_footer import static_pages  # noqa: E402

COPY = json.loads((ROOT / "assets/privacy-copy.json").read_text(encoding="utf-8"))


class PrivacyPolicy(unittest.TestCase):
    def test_pages_are_current(self):
        for name, text in build_privacy.outputs().items():
            with self.subTest(page=name):
                self.assertEqual((ROOT / name).read_text(encoding="utf-8"), text)

    def test_every_gateway_language_has_a_complete_section(self):
        keys = [l["key"] for l in COPY["languages"]]
        self.assertEqual(sorted(keys), sorted(site_footer.PRIVACY))
        html = (ROOT / "privacy.html").read_text(encoding="utf-8")
        for l in COPY["languages"]:
            with self.subTest(lang=l["key"]):
                self.assertEqual(len(l["sections"]), len(COPY["sections"]))
                self.assertEqual(l["title"], site_footer.PRIVACY[l["key"]])
                self.assertIn(f'<section id="{l["key"]}" class="privacy-language" lang="{l["lang"]}"', html)
                # Japanese and English are authoritative; every other text says it is a reference translation.
                self.assertEqual("notice" in l, l["key"] not in ("en", "ja"))

    def test_company_name_and_no_draft_notes(self):
        text = json.dumps(COPY, ensure_ascii=False)
        self.assertNotIn("合同会社", text)
        self.assertNotRegex(text, r"(?i)draft|TODO|must be confirmed|確認します")

    def test_every_page_links_to_its_language(self):
        for path in static_pages():
            with self.subTest(page=str(path.relative_to(ROOT))):
                self.assertRegex(path.read_text(encoding="utf-8"), r'<a href="(?:\.\./|/kumihan/)?privacy\.html#[a-z-]+">')


if __name__ == "__main__":
    unittest.main()
