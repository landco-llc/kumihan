"""Regression: ZiHeng uses only its approved logo and punctuation-free headline copy.

The KUMIHAN / ZiHeng skills informed editorial changes; this is a static check,
not a live-browser visual or host-native skill acceptance claim.
"""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
SITE_PAGES = (
    "kumihan-zh-han.html",
    "kumihan-zh-han.en.html",
    "kumihan-zh-han.ja.html",
    "docs/install-ziheng.html",
    "docs/install-ziheng.en.html",
    "docs/install-ziheng.ja.html",
    "docs/install-ziheng-claude.html",
    "docs/install-ziheng-claude.en.html",
    "docs/install-ziheng-claude.ja.html",
    "docs/install-ziheng-gemini.html",
    "docs/install-ziheng-gemini.en.html",
    "docs/install-ziheng-gemini.ja.html",
)
HOST_PAGES = [p for p in SITE_PAGES if "install-ziheng-claude" in p or "install-ziheng-gemini" in p]
PUNCTUATION = re.compile(r"[、。，,.!?！？：:；;（）()「」『』“”‘’—–]")


class HeadingReader(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.current = None
        self.headings = []
        self.og_title = None

    def handle_starttag(self, tag, attrs):
        meta = dict(attrs)
        if tag == "meta" and meta.get("property") == "og:title":
            self.og_title = meta.get("content")
        if tag in ("title", "h1", "h2", "h3"):
            if self.current is not None:
                raise AssertionError("Unexpected nested heading")
            self.current = {"tag": tag, "text": []}
        elif tag == "br" and self.current is not None:
            self.current["text"].append(" ")

    def handle_data(self, data):
        if self.current is not None:
            self.current["text"].append(data)

    def handle_endtag(self, tag):
        if self.current is not None and tag == self.current["tag"]:
            self.headings.append((tag, "".join(self.current["text"]).strip()))
            self.current = None


class ZiHengApprovedBrandAndHeadlines(unittest.TestCase):
    def test_all_twelve_pages_use_punctuation_free_headings(self):
        for path in SITE_PAGES:
            with self.subTest(page=path):
                html = (ROOT / path).read_text(encoding="utf-8")
                tags = HeadingReader()
                tags.feed(html)
                self.assertIsNone(tags.current)
                self.assertTrue(tags.headings)
                self.assertEqual(len([h for h, _ in tags.headings if h == "title"]), 1)
                self.assertEqual(len([h for h, _ in tags.headings if h == "h1"]), 1)
                for element, copy in tags.headings:
                    self.assertTrue(copy, (path, element))
                    self.assertIsNone(PUNCTUATION.search(copy), (path, element, copy))
                self.assertIsNotNone(tags.og_title, path)
                self.assertIsNone(PUNCTUATION.search(tags.og_title), (path, "og:title"))
                self.assertEqual(tags.og_title, next(t for h, t in tags.headings if h == "title"))

    def test_only_approved_kumihan_image_mark_is_used(self):
        css = (ROOT / "assets/ziheng-site.css").read_text(encoding="utf-8")
        self.assertNotIn("brand-sigil", css)
        self.assertTrue((ROOT / "assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png").is_file())
        for path in SITE_PAGES:
            with self.subTest(page=path):
                html = (ROOT / path).read_text(encoding="utf-8")
                self.assertNotIn("brand-sigil", html)
                self.assertIn("KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png", html)
                self.assertIn('KUMIHAN<span class="brand-rule">｜</span>字衡', html)

    def test_host_steps_preserve_instructions_as_body_copy(self):
        for path in HOST_PAGES:
            with self.subTest(page=path):
                html = (ROOT / path).read_text(encoding="utf-8")
                self.assertEqual(html.count('class="step-detail"'), 4)
                self.assertEqual(html.count("<h3>"), 4)
                self.assertIn('class="steps"', html)
                self.assertIn("0.1.0.zip", html)


if __name__ == "__main__":
    unittest.main()
