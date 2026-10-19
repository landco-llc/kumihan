"""Every site page loads the typefaces for its own language (tools/web_fonts.py).

Static source check: system fonts first, the script's Google Fonts family only
as a fallback, served from this site; it does not claim which font a given
browser renders.
"""
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import web_fonts  # noqa: E402


class WebFonts(unittest.TestCase):
    def test_every_static_page_links_its_language_fonts(self):
        pages = [ROOT / "index.html", *(p for p in ROOT.glob("top-*.html") if "http-equiv=\"refresh\"" not in p.read_text(encoding="utf-8")), *ROOT.glob("kumihan*.html"),
                 *(ROOT / "docs").glob("install-*.html")]
        checked = 0
        for path in pages:
            text = path.read_text(encoding="utf-8")
            if text.startswith("---"):
                continue  # Jekyll sources: covered by the layout test below.
            lang = re.search(r'<html lang="([^"]+)"', text).group(1)
            with self.subTest(page=path.name):
                # Pages link the site root relatively, or absolutely as /kumihan/.
                roots = ("../" if path.parent.name == "docs" else "", "/kumihan/")
                self.assertTrue(any(web_fonts.font_links(lang, root) in text for root in roots))
                self.assertIn("assets/kumihan-fonts.css", text)
                # The shared typeface sheet comes after the page's own styles.
                head = text.split("</head>")[0]
                others = [m.end() for m in re.finditer(r'href="[^"]*\.css(?:\?[^"]*)?"|</style>', head)
                          if "kumihan-fonts.css" not in m.group(0)]
                self.assertGreater(head.index("kumihan-fonts.css"), max(others))
            checked += 1
        self.assertGreaterEqual(checked, 60)

    def test_no_page_requests_fonts_from_google(self):
        pages = [*ROOT.glob("*.html"), *(ROOT / "docs").glob("*.html"), *(ROOT / "_layouts").glob("*.html"),
                 *(ROOT / "templates").glob("*.html"), ROOT / "_data/web_fonts.yml"]
        for path in pages:
            with self.subTest(page=str(path.relative_to(ROOT))):
                self.assertNotRegex(path.read_text(encoding="utf-8"), r"fonts\.(?:googleapis|gstatic)\.com")

    def test_every_font_file_is_on_this_site(self):
        fonts = ROOT / "assets/fonts/google"
        for url in web_fonts.google_urls():
            css = (fonts / f"{web_fonts.local_id(url)}.css").read_text(encoding="utf-8")
            with self.subTest(url=url):
                files = re.findall(r"url\(([^)]+)\)", css)
                self.assertTrue(files)
                self.assertNotIn("https://", " ".join(files))
                for name in files:
                    self.assertTrue((fonts / name).is_file(), name)

    def test_jekyll_layouts_link_language_fonts(self):
        for layout in ("landing.html", "installation.html", "geuljjaim.html", "geuljjaim-index.html"):
            text = (ROOT / "_layouts" / layout).read_text(encoding="utf-8")
            with self.subTest(layout=layout):
                self.assertIn("site.data.web_fonts[page.lang]", text)
                self.assertIn("site.data.kumihan_assets.fonts_css", text)

    def test_system_fonts_come_before_google_fonts(self):
        for key, (local_sans, _, sans, serif) in web_fonts.SCRIPTS.items():
            s, r = web_fonts.stacks(key)
            with self.subTest(script=key):
                self.assertLess(s.index(local_sans.split(",")[0]), s.index(f'"{sans}"'))
                self.assertTrue(s.endswith("sans-serif") and r.endswith("serif"))


if __name__ == "__main__":
    unittest.main()
