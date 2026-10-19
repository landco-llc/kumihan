"""Every KUMIHAN page has the shared link-preview tags (tools/site_share.py).

Shared pages show the page title, what KUMIHAN is in the page's language followed
by the page's own description, and the KUMIHAN logo.
"""
import json
import re
import struct
import sys
import unittest
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import site_share  # noqa: E402
from test_site_footer import static_pages  # noqa: E402


def meta(html, name):
    return [unescape(m) for m in re.findall(rf'<meta (?:property|name)="{name}" content="([^"]*)">', html)]


class SharedPreview(unittest.TestCase):
    def test_every_static_page_has_the_shared_tags(self):
        pages = static_pages()
        self.assertGreaterEqual(len(pages), 200)
        for path in pages:
            text = path.read_text(encoding="utf-8")
            with self.subTest(page=str(path.relative_to(ROOT))):
                self.assertEqual(text, site_share.apply(text))
                lang = re.search(r'<html lang="([^"]+)"', text).group(1)
                self.assertEqual(meta(text, "og:image"), [site_share.IMAGE])
                self.assertEqual(meta(text, "twitter:card"), ["summary_large_image"])
                self.assertTrue(meta(text, "og:description")[0].startswith(site_share.ABOUT[site_share.key(lang)]))

    def test_description_joins_kumihan_and_the_page(self):
        self.assertEqual(site_share.description("en", "Page."), site_share.ABOUT["en"] + " Page.")
        self.assertEqual(site_share.description("ja", "ページ。"), site_share.ABOUT["ja"] + "ページ。")
        self.assertEqual(site_share.description("ja", site_share.ABOUT["ja"]), site_share.ABOUT["ja"])
        self.assertEqual(site_share.locale("zh-Hant-HK"), "zh_HK")

    def test_share_image_is_a_wide_logo(self):
        data = (ROOT / "assets" / "kumihan-share.png").read_bytes()
        self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
        self.assertEqual(struct.unpack(">II", data[16:24]), (1200, 630))

    def test_jekyll_layouts_use_the_shared_tags(self):
        data = json.loads((ROOT / "_data/site_share.json").read_text(encoding="utf-8"))
        self.assertEqual(data, site_share.data())
        for layout in ("landing.html", "installation.html", "geuljjaim.html", "geuljjaim-index.html"):
            text = (ROOT / "_layouts" / layout).read_text(encoding="utf-8")
            with self.subTest(layout=layout):
                self.assertIn("{% include share.html", text)
                self.assertNotIn('property="og:', text)


if __name__ == "__main__":
    unittest.main()
