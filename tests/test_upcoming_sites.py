"""Newer editions (tools/build_upcoming_sites.py): released ones link their packages, the rest say coming soon.

Each of el, nl, ms, tr, he, sa, cs, hu, my, la, tl, fi, sv, da, no and uk has a landing in its
language, English and Japanese, and a top page; English (en) has an English and a Japanese
landing and is listed on every top. Editions with packages in the version catalogue (sa, my,
tl, fi, sv, da, no, uk) link their skills and installation guides; the others claim no
release, download or installation guide.
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

CODES = ("el", "nl", "ms", "tr", "he", "sa", "cs", "hu", "my", "la", "tl", "en", "fi", "sv", "da", "no", "uk")
RELEASED = ("el", "nl", "ms", "tr", "he", "sa", "cs", "hu", "my", "la", "tl", "en", "fi", "sv", "da", "no", "uk")
COMING = tuple(c for c in CODES if c not in RELEASED)
TOPS = tuple(c for c in CODES if c != "en")


def pages(code):
    for lang in upcoming.langs(code):
        path = ROOT / upcoming.landing_path(code, lang)
        yield lang, path, path.read_text(encoding="utf-8")


def top_card(text, code):
    return re.search(rf'<article[^>]*aria-labelledby="language-{code}".*?</article>', text, re.S)


class UpcomingEditions(unittest.TestCase):
    def test_generated_files_are_current(self):
        for name, content in upcoming.outputs().items():
            with self.subTest(file=name):
                self.assertEqual((ROOT / name).read_text(encoding="utf-8"), content)

    def test_released_set_follows_the_version_catalogue(self):
        self.assertEqual(tuple(upcoming.EDITIONS), CODES)
        self.assertEqual(tuple(c for c in CODES if upcoming.released(c)), RELEASED)

    def test_coming_soon_landings_have_no_release_links(self):
        for code in COMING:
            for lang, path, text in pages(code):
                with self.subTest(page=path.name):
                    self.assertIn(f'<html lang="{lang}"' + (' dir="rtl"' if lang == "he" else ""), text)
                    self.assertIn("COMING SOON / v0.1.0", text)
                    self.assertNotIn("RELEASED", text)
                    self.assertNotRegex(text, r'href="[^"]*(?:/releases/|\.zip"|docs/install-)')
                    self.assertNotIn(f"plugins/kumihan-{upcoming.EDITIONS[code][1]}", text)
                    self.assertEqual(text.count('<div class="skill-card">'), 4)
                    self.assertEqual(text.count('<div class="platform-row">'), 3)
                    self.assertIn(f'href="{upcoming.gateway(code, lang)}"', text)

    def test_released_landings_link_skills_and_installation_guides(self):
        for code in RELEASED:
            slug = upcoming.EDITIONS[code][1]
            for lang, path, text in pages(code):
                with self.subTest(page=path.name):
                    version='0.1.1' if code=='en' else '0.1.0'
                    self.assertIn('RELEASED / v'+version, text)
                    self.assertNotIn("COMING SOON", text)
                    self.assertEqual(len(re.findall(rf'class="skill-card" href="[^"]*plugins/kumihan-{re.escape(slug)}/skills/', text)), 4)
                    for host in ("chatgpt", "claude", "gemini"):
                        guide = upcoming.guide(code, host, lang)
                        self.assertIn(f'href="{guide}"', text)
                        self.assertTrue((ROOT / guide).exists(), guide)

    def test_every_top_lists_the_new_editions(self):
        for key, (file, *_rest) in gateways.GATEWAYS.items():
            text = (ROOT / file).read_text(encoding="utf-8")
            for code in CODES:
                with self.subTest(top=file, edition=code):
                    card = top_card(text, code)
                    self.assertIsNotNone(card)
                    if code in RELEASED:
                        version='0.1.1' if code=='en' else '0.1.0'
                        self.assertIn('<bdi dir="ltr">v'+version+'</bdi>', card.group(0))
                    else:
                        self.assertNotIn("<bdi dir=\"ltr\">v", card.group(0).split("</div>")[0])
                        self.assertRegex(card.group(0), r'class="version-state"[^>]*>(?:Coming soon|配布準備中|準備中|准备中)<')

    def test_new_tops_exist_and_hebrew_is_right_to_left(self):
        self.assertEqual(list(upcoming.langs("en")), ["en", "ja"])
        self.assertEqual(upcoming.landing_path("en", "en"), "kumihan-en.html")
        for code in TOPS:
            text = (ROOT / f"top-{code}.html").read_text(encoding="utf-8")
            with self.subTest(code=code):
                self.assertIn(f'<html lang="{code}"' + (' dir="rtl"' if code == "he" else ""), text)
                self.assertIn(f'privacy.html#{code}', text)

    def test_shared_copy_wording_matches_the_release_state(self):
        copy = json.loads((ROOT / "assets" / "upcoming-site-copy.json").read_text(encoding="utf-8"))
        for code in CODES:
            with self.subTest(code=code):
                if code in RELEASED:
                    self.assertEqual(copy[code]["ja"]["skill_view"], "スキルを見る")
                    self.assertEqual(copy[code]["en"]["cta"][0], "Get started")
                    self.assertIn("install_extra", copy[code][code])
                else:
                    self.assertEqual(copy[code]["ja"]["skill_view"], "近日公開")
                    self.assertEqual(copy[code]["en"]["cta"][0], "See status")
                    self.assertNotIn("install_extra", copy[code][code])


if __name__ == "__main__":
    unittest.main()
