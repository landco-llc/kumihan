"""Every edition's installation guides follow the Japanese guide (tools/build_install_guides.py)."""
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build_install_guides as G  # noqa: E402

MARK = re.compile(r"\{\{[^}]+\}\}")


def section_ids(html):
    return re.findall(r'<h2 id="([^"]+)"', html.split('<div class="guide-pane">', 1)[1])


class InstallGuides(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = G.outputs()

    def test_committed_pages_are_current(self):
        subprocess.run([sys.executable, str(ROOT / "tools/build_install_guides.py"), "--check"], check=True,
                       capture_output=True)

    def test_every_edition_has_nine_guides(self):
        for code in G.editions():
            for host in G.HOSTS:
                for lang in (code, "en", "ja"):
                    self.assertIn(G.guide_path(code, host, lang), self.files)

    def test_templates_keep_the_japanese_structure_and_markers(self):
        for lang_dir in sorted(p for p in G.TEMPLATES.iterdir() if p.is_dir()):
            ui = json.loads((lang_dir / "ui.json").read_text(encoding="utf-8"))
            self.assertTrue(ui["note_title"].startswith("INSTALLATION / "), lang_dir.name)
            for host in G.HOSTS:
                ja = (G.TEMPLATES / "ja" / f"{host}.md").read_text(encoding="utf-8")
                text = (lang_dir / f"{host}.md").read_text(encoding="utf-8")
                with self.subTest(lang=lang_dir.name, host=host):
                    keep = lambda t: sorted(m for m in MARK.findall(t) if m not in ("{{lang}}", "{{brand}}"))
                    self.assertEqual(keep(text), keep(ja))
                    heads = lambda t: re.findall(r"^## ((?:[A-Z0-9]|\{\{L_\w+\}\})\.)?", t, re.M)
                    self.assertEqual(heads(text), heads(ja))

    def test_sections_match_the_japanese_guide_in_every_language(self):
        for code in G.editions():
            for host in G.HOSTS:
                ids = {lang: section_ids(self.files[G.guide_path(code, host, lang)]) for lang in (code, "en", "ja")}
                with self.subTest(code=code, host=host):
                    self.assertEqual(ids[code], ids["ja"])
                    self.assertEqual(ids["en"], ids["ja"])
                    self.assertEqual(ids["ja"][0], "step-1")

    def test_downloads_are_the_editions_own_packages(self):
        for code in G.editions():
            ed = G.edition(code)
            allowed = {url for h in ed["hosts"].values() for url in
                       [h["plugin"][1], *(entry[1] for entry in h["skills"].values())]} | {G.sums(ed, h) for h in G.HOSTS}
            for host in G.HOSTS:
                html = self.files[G.guide_path(code, host, "ja")]
                zips = set(re.findall(r'href="([^"]+\.zip)"', html))
                with self.subTest(code=code, host=host):
                    self.assertTrue(zips)
                    self.assertLessEqual(zips, allowed)
                    self.assertIn(ed["hosts"][host]["plugin"][1], zips)
                    self.assertIn(f'href="{G.sums(ed, host)}"', html)

    def test_display_name_and_no_stale_version_label(self):
        for code in G.editions():
            ed = G.edition(code)
            html = self.files[G.guide_path(code, "chatgpt", "ja")]
            with self.subTest(code=code):
                self.assertIn(f"<strong>{G.x(ed['display'])}</strong>", html)
                self.assertNotIn("KUMIHAN v0.1.6", html)
                self.assertNotRegex(html, r"\{\{[^}]*\}\}")

    def test_language_attributes_and_alternates(self):
        for code in G.editions():
            native = G.page_lang_attr(code, code)
            for lang, attr in ((code, native), ("en", "en"), ("ja", "ja")):
                html = self.files[G.guide_path(code, "claude", lang)]
                with self.subTest(code=code, lang=lang):
                    self.assertRegex(html, rf'<html lang="{re.escape(attr)}"')
                    self.assertEqual(len(re.findall(r'rel="alternate" hreflang=', html)), len({code, "en", "ja"}) + 1)
                    if lang == code and code in G.RTL:
                        self.assertIn('dir="rtl"', html.split(">", 2)[1])


if __name__ == "__main__":
    unittest.main()
