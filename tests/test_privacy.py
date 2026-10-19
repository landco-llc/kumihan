"""The privacy policy pages (tools/build_privacy.py) are current and linked from every footer."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build_privacy  # noqa: E402
from test_site_footer import static_pages  # noqa: E402


class PrivacyPolicy(unittest.TestCase):
    def test_pages_are_current(self):
        for name, text in build_privacy.outputs().items():
            with self.subTest(page=name):
                self.assertEqual((ROOT / name).read_text(encoding="utf-8"), text)

    def test_english_and_japanese_have_the_same_sections(self):
        import json
        copy = json.loads((ROOT / "assets/privacy-copy.json").read_text(encoding="utf-8"))
        self.assertEqual([s["id"] for s in copy["en"]["sections"]], [s["id"] for s in copy["ja"]["sections"]])
        for lang in copy:
            text = json.dumps(copy[lang], ensure_ascii=False)
            with self.subTest(lang=lang):
                self.assertNotRegex(text, r"(?i)draft|TODO|must be confirmed|確認します")

    def test_every_page_links_to_the_policy(self):
        for path in static_pages():
            with self.subTest(page=str(path.relative_to(ROOT))):
                self.assertRegex(path.read_text(encoding="utf-8"), r'<a href="[./]*(?:/kumihan/)?privacy(?:-ja)?\.html"')


if __name__ == "__main__":
    unittest.main()
