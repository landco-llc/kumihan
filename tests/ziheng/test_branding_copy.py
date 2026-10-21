"""Regression: ZiHeng uses only its approved logo and punctuation-free headline copy.

Landings are built by tools/build_ziheng_site.py; the nine install guides by
tools/build_install_guides.py from the shared template (modeled on the Japanese
KUMIHAN guide, whose numbered "1. ..." / "A. ..." section headings are part of the
standard), so guide section headings are checked for structure, not punctuation.

The KUMIHAN / ZiHeng skills informed editorial changes; this is a static check,
not a live-browser visual or host-native skill acceptance claim.
"""
from html.parser import HTMLParser
from pathlib import Path
import json
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
LANDINGS = [p for p in SITE_PAGES if not p.startswith("docs/")]
GUIDES = [p for p in SITE_PAGES if p.startswith("docs/")]
PUNCTUATION = re.compile(r"[、。，,.!?！？：:；;（）()「」『』“”‘’—–]")


class HeadingReader(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.current = None
        self.headings = []
        self.og_title = None
        self.ids = set()
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        meta = dict(attrs)
        if meta.get("id"):
            self.ids.add(meta["id"])
        if tag == "a" and meta.get("href"):
            self.hrefs.append(meta["href"])
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
    def test_all_twelve_pages_use_punctuation_free_headlines(self):
        for path in SITE_PAGES:
            with self.subTest(page=path):
                html = (ROOT / path).read_text(encoding="utf-8")
                tags = HeadingReader()
                tags.feed(html)
                self.assertIsNone(tags.current)
                self.assertTrue(tags.headings)
                self.assertEqual(len([h for h, _ in tags.headings if h == "title"]), 1)
                self.assertEqual(len([h for h, _ in tags.headings if h == "h1"]), 1)
                # Landings: every heading; guides: the headline (title / h1 / og:title).
                checked = tags.headings if path in LANDINGS else [
                    (h, t) for h, t in tags.headings if h in ("title", "h1")]
                for element, copy in tags.headings:
                    self.assertTrue(copy, (path, element))
                for element, copy in checked:
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

    def test_guides_follow_standard_sections_with_verified_downloads(self):
        facts = json.loads((ROOT / "assets/edition-versions.json").read_text(encoding="utf-8"))["editions"]["zh-hant"]
        assets = {a["name"]: a["url"] for a in facts["verified_assets"]}
        for path in GUIDES:
            with self.subTest(page=path):
                html = (ROOT / path).read_text(encoding="utf-8")
                tags = HeadingReader()
                tags.feed(html)
                h2 = [t for h, t in tags.headings if h == "h2"]
                # Choose a method, host sections A/B/C, try it out (numbered).
                self.assertTrue(any(t.startswith("1. ") for t in h2), h2)
                for letter in "ABC":
                    self.assertTrue(any(t.startswith(letter + ". ") for t in h2), (letter, h2))
                self.assertTrue(any(re.match(r"[23]\. ", t) for t in h2), h2)
                # The method table and table of contents jump to sections that exist.
                for href in tags.hrefs:
                    if href.startswith("#"):
                        self.assertIn(href[1:], tags.ids, href)
                for anchor in ("#a", "#b", "#c"):
                    self.assertIn(anchor, tags.hrefs)
                host = "claude" if "-claude" in path else "gemini" if "-gemini" in path else "openai-codex"
                plugin = f"kumihan-ziheng-{host}-plugin-0.2.0.zip"
                self.assertIn(f'href="{assets[plugin]}"', html)


if __name__ == "__main__":
    unittest.main()
