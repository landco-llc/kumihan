"""Every KUMIHAN page carries the one shared footer (tools/site_footer.py).

KUMIHAN, "Open-source typography & design guidance by L&Co. LLC.", and the
links KUMIHAN (the top in the page's language), the language-edition menu,
GitHub and Apache 2.0.
"""
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import site_footer  # noqa: E402


def static_pages():
    pages = [*ROOT.glob("*.html"), *(ROOT / "docs").glob("*.html")]
    return [p for p in pages if not p.read_text(encoding="utf-8").startswith("---")]


class SharedFooter(unittest.TestCase):
    def test_every_static_page_has_the_shared_footer(self):
        pages = static_pages()
        self.assertGreaterEqual(len(pages), 200)
        for path in pages:
            text = path.read_text(encoding="utf-8")
            lang = re.search(r'<html lang="([^"]+)"', text).group(1)
            # Pages link the site root relatively, or absolutely as /kumihan/.
            roots = ("../" if path.parent.name == "docs" else "", "/kumihan/")
            with self.subTest(page=str(path.relative_to(ROOT))):
                self.assertEqual(text.count("<footer"), 1)
                self.assertTrue(any(site_footer.footer(lang, root) in text for root in roots))

    def test_footer_content(self):
        html = site_footer.footer("pl")
        self.assertIn('<div class="kf-mark">KUMIHAN</div>', html)
        self.assertIn("Open-source typography &amp; design guidance by", html)
        self.assertIn(">L&amp;Co. LLC</a>.</p>", html)
        links = re.search(r'<nav class="kf-links"[^>]*>(.*)</nav>', html).group(1)
        self.assertRegex(links, r'^<a href="top-pl\.html">KUMIHAN</a><details class="kf-menu"><summary>Wybierz język</summary>')
        self.assertTrue(links.endswith('>GitHub</a><a href="https://github.com/landco-llc/kumihan/blob/main/LICENSE" '
                                       'target="_blank" rel="noopener noreferrer">Apache 2.0</a>'))
        self.assertIn('<span class="code">JA</span> - Japoński</a>', links)

    def test_jekyll_layouts_use_the_shared_footer(self):
        data = json.loads((ROOT / "_data/site_footer.json").read_text(encoding="utf-8"))
        for lang, html in data.items():
            with self.subTest(lang=lang):
                self.assertEqual(html, site_footer.footer(lang, site_footer.ROOT_MARK))
        for layout in ("landing.html", "installation.html", "geuljjaim.html", "geuljjaim-index.html"):
            text = (ROOT / "_layouts" / layout).read_text(encoding="utf-8")
            with self.subTest(layout=layout):
                self.assertIn("site.data.site_footer[kumihan_lang]", text)
                self.assertNotIn("<footer", text)


if __name__ == "__main__":
    unittest.main()
