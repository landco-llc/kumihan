"""Regression for the KUMIHAN-style ZiLu Japanese landing."""
import re
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from seo_metadata import enrich_html

PAGE = ROOT / "kumihan-zh-cn.ja.html"
TEMPLATE = ROOT / "templates" / "zilu-ja-landing.html"
STYLESHEET = ROOT / "assets" / "zilu-index-ja.css"
INDEX = ROOT / "_layouts" / "landing.html"

class Parse(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.text_by_heading = []
        self.heading = None
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags.append((tag, a))
        if tag in ("h1", "h2", "h3"):
            self.heading = tag
            self.text_by_heading.append("")
    def handle_endtag(self, tag):
        if tag == self.heading:
            self.heading = None
    def handle_data(self, data):
        if self.heading is not None:
            self.text_by_heading[-1] += data

class JapaneseLanding(unittest.TestCase):
    def test_source_template_and_sections(self):
        page = PAGE.read_text(encoding="utf-8")
        source = TEMPLATE.read_text(encoding="utf-8")
        from version_display import apply_html
        self.assertEqual(page, apply_html(enrich_html(source, PAGE.name), PAGE.name))
        self.assertEqual(page.split("<body", 1)[1], apply_html(source, PAGE.name).split("<body", 1)[1])
        p = Parse()
        p.feed(page)
        self.assertEqual([v["lang"] for t, v in p.tags if t=="html"], ["ja"])
        sections = [v["class"] for t,v in p.tags if t=="section" and "class" in v]
        self.assertEqual(sections,["hero","intro-strip","features","idea-band","skills-section","install-section","status-section","cta-section"])
        self.assertEqual(len([1 for tag,_ in p.tags if tag=="h1"]),1)
        for text in p.text_by_heading:
            self.assertFalse(re.search(r"[、。！？!?.,]",text),f"headline punctuation: {text}")
        self.assertTrue(STYLESHEET.exists())
        css = STYLESHEET.read_text(encoding="utf-8")
        baseline = re.search(r"<style>(.*?)</style>", INDEX.read_text(encoding="utf-8"),re.S).group(1)
        self.assertIn(baseline,css)
        self.assertIn("line-break:strict",css)
    def test_original_content_and_links(self):
        page=PAGE.read_text(encoding="utf-8")
        p=Parse()
        p.feed(page)
        links=[v.get("href") for tag,v in p.tags if tag=="a"]
        self.assertIn("kumihan-zh-cn.html",links)
        self.assertIn("kumihan-zh-cn.en.html",links)
        self.assertIn("docs/install-zilu-chatgpt.ja.html",links)
        self.assertIn("docs/install-zilu-claude.ja.html",links)
        self.assertIn("docs/install-zilu-gemini.ja.html",links)
        self.assertNotIn("最終公開承認待ち",page)
        for label in ("kumihan-zilu-web","kumihan-zilu-documents","kumihan-zilu-review"):
            self.assertIn(label,page)
        self.assertEqual(len([1 for tag,v in p.tags if tag=="img" and "KUMIHAN_OFFICIAL" in v.get("src","")]),1)
        self.assertEqual(len([1 for tag,v in p.tags if tag=="a" and v.get("aria-current")=="page"]),1)
