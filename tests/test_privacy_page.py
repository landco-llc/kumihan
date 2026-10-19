"""Structural tests for the one-file multilingual privacy policy.

These tests check source-level invariants only. They do not claim browser E2E
coverage or legal approval of translated policy text.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "privacy.html"
CODES = ("en", "ja", "ar", "bn", "de", "es", "fa", "fr", "hi", "id",
         "it", "km", "ko", "pl", "pt", "ru", "sw", "th", "vi",
         "zh-hans", "zh-hant", "zu")


class PrivacyPolicy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = POLICY.read_text(encoding="utf-8")

    def test_single_self_contained_html_and_canonical(self):
        html = self.html
        self.assertIn("<!doctype html>", html)
        self.assertIn("<style>", html)
        self.assertIn("<script>", html)
        self.assertNotRegex(html, r'<(?:script|link)[^>]+(?:src|rel)="(?:https?://|stylesheet)')
        self.assertIn(
            '<link rel="canonical" href="https://landco-llc.github.io/kumihan/privacy.html">',
            html)

    def test_language_order_and_full_section_coverage(self):
        html = self.html
        codes = re.findall(r'<details class="locale-panel" id="lang-([^"]+)"', html)
        self.assertEqual(codes, list(CODES))
        self.assertEqual(html.count('class="translation-notice"'), len(CODES) - 2)
        self.assertEqual(html.count('class="clause"'), len(CODES) * 9)
        for code in CODES:
            with self.subTest(code=code):
                self.assertIn(f'<option value="{code}">', html)
                self.assertIn(f'id="lang-{code}"', html)
                for index in range(1, 10):
                    self.assertIn(f'id="lang-{code}-{index:02d}"', html)

    def test_accessible_navigation_and_deep_links(self):
        html = self.html
        self.assertIn('<label class="picker-label" for="language-picker">', html)
        self.assertIn('<select id="language-picker"', html)
        self.assertIn('window.addEventListener("popstate"', html)
        self.assertIn('window.addEventListener("hashchange"', html)
        self.assertIn('scrollIntoView(', html)
        self.assertIn('<noscript>', html)
        ids = re.findall(r'\bid="([^"]+)"', html)
        self.assertEqual(len(ids), len(set(ids)))

    def test_authoritative_versions_and_translation_disclaimer(self):
        html = self.html
        self.assertIn('The English and Japanese texts are equally authoritative', html)
        self.assertEqual(html.count('class="translation-notice"'), 20)
        self.assertIn('English original ↗', html)
        self.assertIn('日本語正本 ↗', html)
        self.assertRegex(html, r'id="lang-ar".*?dir="rtl"')
        self.assertRegex(html, r'id="lang-fa".*?dir="rtl"')

    def test_privacy_disclosures_and_contact(self):
        html = self.html
        for key in ("GitHub Pages", "Google Fonts", "ChatGPT", "Claude",
                    "Gemini", "Codex", "MCP", "https://landco.co.jp/"):
            with self.subTest(topic=key):
                self.assertIn(key, html)
        self.assertNotIn("mailto:example", html)


if __name__ == "__main__":
    unittest.main()
