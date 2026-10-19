"""Language tops: six cards at first, and an edition menu under the section title.

The menu lists every language edition as "CODE - name" in the page's language,
the page's own language first and the rest by code.
"""
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build_gateways as gateways  # noqa: E402


class EditionMenu(unittest.TestCase):
    def test_every_top_has_the_menu_in_its_language(self):
        for key, (file, *_rest) in gateways.GATEWAYS.items():
            text = (ROOT / file).read_text(encoding="utf-8")
            with self.subTest(page=file):
                menu = re.search(r'<details class="lang-menu edition-menu"><summary>(.*?)</summary><ul>(.*?)</ul>', text)
                self.assertIsNotNone(menu)
                self.assertEqual(menu.group(1), gateways.PICK[key])
                codes = re.findall(r'<span class="code">([A-Z-]+)</span> - ', menu.group(2))
                expected = ([key] if key in gateways.PRODUCTS else []) + sorted(c for c in gateways.PRODUCTS if c != key)
                self.assertEqual(codes, [c.upper() for c in expected])
                names = re.findall(r'</span> - ([^<]+)</a>', menu.group(2))
                self.assertEqual(names, [gateways.EDITION_NAMES[key][c] for c in expected])

    def test_six_cards_before_show_more(self):
        self.assertEqual(gateways.VISIBLE, 6)
        text = (ROOT / "index.html").read_text(encoding="utf-8")
        cards = re.findall(r'<article class="lang-card[^"]*"[^>]*>', text)
        self.assertEqual(sum("data-extra" not in c for c in cards), 6)

    def test_polish_example(self):
        text = (ROOT / "top-pl.html").read_text(encoding="utf-8")
        self.assertIn('<span class="code">JA</span> - Japoński</a>', text)
        self.assertIn('<summary>Wybierz język</summary>', text)


if __name__ == "__main__":
    unittest.main()
