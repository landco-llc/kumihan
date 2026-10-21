"""Editions not yet distributed (tools/build_upcoming_sites.py): landings and tops say coming soon.

Each of el, nl, ms, tr, he and sa has a landing in its language, English and
Japanese, and a top page. None claims a release, download or installation guide.
"""
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build_gateways as gateways  # noqa: E402
import build_upcoming_sites as upcoming  # noqa: E402

CODES = ("el", "nl", "ms", "tr", "he", "sa")


class UpcomingEditions(unittest.TestCase):
    def test_generated_files_are_current(self):
        for name, content in upcoming.outputs().items():
            with self.subTest(file=name):
                self.assertEqual((ROOT / name).read_text(encoding="utf-8"), content)

    def test_landings_say_coming_soon_without_release_links(self):
        self.assertEqual(tuple(upcoming.EDITIONS), CODES)
        for code in CODES:
            for lang in (code, "en", "ja"):
                path = ROOT / upcoming.landing_path(code, lang)
                text = path.read_text(encoding="utf-8")
                with self.subTest(page=path.name):
                    self.assertIn(f'<html lang="{lang}"' + (' dir="rtl"' if lang == "he" else ""), text)
                    self.assertIn("COMING SOON / v0.1.0", text)
                    self.assertNotIn("RELEASED", text)
                    self.assertNotRegex(text, r'href="[^"]*(?:/releases/|\.zip"|docs/install-)')
                    self.assertNotIn(f"plugins/kumihan-{upcoming.EDITIONS[code][1]}", text)
                    self.assertEqual(text.count('<div class="skill-card">'), 4)
                    self.assertEqual(text.count('<div class="platform-row">'), 3)
                    self.assertIn(f'href="{upcoming.gateway(code, lang)}"', text)

    def test_every_top_lists_the_new_editions_as_coming_soon(self):
        for key, (file, *_rest) in gateways.GATEWAYS.items():
            text = (ROOT / file).read_text(encoding="utf-8")
            for code in CODES:
                with self.subTest(top=file, edition=code):
                    card = re.search(rf'<article[^>]*aria-labelledby="language-{code}".*?</article>', text, re.S)
                    self.assertIsNotNone(card)
                    self.assertNotIn("<bdi dir=\"ltr\">v", card.group(0).split("</div>")[0])
                    self.assertRegex(card.group(0), r'class="version-state"[^>]*>(?:Coming soon|配布準備中|準備中|准备中)<')

    def test_new_tops_exist_and_hebrew_is_right_to_left(self):
        for code in CODES:
            text = (ROOT / f"top-{code}.html").read_text(encoding="utf-8")
            with self.subTest(code=code):
                self.assertIn(f'<html lang="{code}"' + (' dir="rtl"' if code == "he" else ""), text)
                self.assertIn(f'privacy.html#{code}', text)

    def test_shared_copy_uses_coming_soon_wording(self):
        copy = json.loads((ROOT / "assets" / "upcoming-site-copy.json").read_text(encoding="utf-8"))
        for code in CODES:
            with self.subTest(code=code):
                self.assertEqual(copy[code]["ja"]["skill_view"], "近日公開")
                self.assertEqual(copy[code]["en"]["cta"][0], "See status")
                self.assertNotIn("install_extra", copy[code][code])


if __name__ == "__main__":
    unittest.main()
