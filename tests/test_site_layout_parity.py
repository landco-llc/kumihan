"""Product landing and install pages keep the canonical KUMIHAN page structure.

Static source check only; it does not claim browser rendering or host behavior.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX_SECTIONS = ["hero", "intro-strip", "features", "idea-band", "skills-section",
                  "install-section", "status-section", "cta-section"]
GUIDE_SKELETON = ("site-header", "breadcrumb", "hero-grid", "language-switch", "hero-logo",
                  "platform-nav", "content-layout", "toc", "guide-head", "guide-pane", "footer")


def sections(text):
    return re.findall(r'<section class="([^"]+)"', text)


class LandingParity(unittest.TestCase):
    def test_landings_follow_canonical_index_sections(self):
        canonical = sections((ROOT / "_layouts/landing.html").read_text(encoding="utf-8"))
        self.assertEqual(canonical, INDEX_SECTIONS)
        pages = ["kumihan-de.html", "kumihan-de.en.html", "kumihan-de.ja.html", "kumihan-hi.html", "kumihan-hi.en.html", "kumihan-hi.ja.html", "kumihan-th.html", "kumihan-th-en.html", "kumihan-th-ja.html",
                 "kumihan-zh-cn.html", "kumihan-zh-cn.en.html", "kumihan-zh-cn.ja.html",
                 "kumihan-ko.html", "kumihan-ko.en.html", "kumihan-ko.ja.html",
                 "kumihan-zh-han.html", "kumihan-zh-han.en.html", "kumihan-zh-han.ja.html",
                 "kumihan-fr.html", "kumihan-fr.en.html", "kumihan-fr.ja.html",
                 "kumihan-pt.html", "kumihan-pt.en.html", "kumihan-pt.ja.html",
                 "kumihan-ar.html", "kumihan-ar.en.html", "kumihan-ar.ja.html",
                 "kumihan-es.html", "kumihan-es.en.html", "kumihan-es.ja.html",
                 "kumihan-pl.html", "kumihan-pl.en.html", "kumihan-pl.ja.html"]
        for page in pages:
            with self.subTest(page=page):
                self.assertEqual(sections((ROOT / page).read_text(encoding="utf-8")), INDEX_SECTIONS)

    def test_landing_install_lists_one_row_per_host(self):
        pages = ["kumihan-de.html", "kumihan-de.en.html", "kumihan-de.ja.html", "kumihan-hi.html", "kumihan-hi.en.html", "kumihan-hi.ja.html", "kumihan-fr.html", "kumihan-fr.en.html", "kumihan-fr.ja.html",
                 "kumihan-pt.html", "kumihan-pt.en.html", "kumihan-pt.ja.html",
                 "kumihan-ar.html", "kumihan-ar.en.html", "kumihan-ar.ja.html",
                 "kumihan-th-en.html", "kumihan-zh-cn.html", "kumihan-zh-cn.en.html",
                 "kumihan-zh-han.html", "kumihan-zh-han.en.html", "kumihan-zh-han.ja.html",
                 "kumihan-fr.html", "kumihan-fr.en.html", "kumihan-fr.ja.html",
                 "kumihan-pt.html", "kumihan-pt.en.html", "kumihan-pt.ja.html",
                 "kumihan-ar.html", "kumihan-ar.en.html", "kumihan-ar.ja.html",
                 "kumihan-es.html", "kumihan-es.en.html", "kumihan-es.ja.html",
                 "kumihan-pl.html", "kumihan-pl.en.html", "kumihan-pl.ja.html"]
        for page in pages:
            with self.subTest(page=page):
                text = (ROOT / page).read_text(encoding="utf-8")
                self.assertEqual(len(re.findall(r'class="[^"]*\bplatform-row\b', text)), 3)


GATEWAY = {"ja": "index.html", "en": "top-en.html", "zh-Hant-TW": "top-zh-han.html",
           "zh-Hans-CN": "top-zh-cn.html", "ko-KR": "top-ko.html", "th": "top-th.html",
           "ar": "top-ar.html", "es": "top-es.html", "fr": "top-fr.html", "pt": "top-pt.html",
           "hi": "top-hi.html", "vi": "top-vi.html", "de": "top-de.html", "pl": "top-pl.html",
           "id": "top-id.html"}
PAGE_GATEWAY = GATEWAY


class GatewayLinks(unittest.TestCase):
    def test_every_static_page_links_to_its_language_gateway(self):
        pages = [p for p in ROOT.glob("kumihan-*.html")]
        pages += [p for p in (ROOT / "docs").glob("install-*.html")
                  if not p.read_text(encoding="utf-8").startswith("---")]
        self.assertGreaterEqual(len(pages), 30)
        for path in pages:
            text = path.read_text(encoding="utf-8")
            if text.startswith("---"):
                continue  # Jekyll sources: covered by the layout checks below.
            lang = re.search(r'<html lang="([^"]+)"', text).group(1)
            with self.subTest(page=path.name):
                self.assertRegex(text, r'href="(?:\.\./|/kumihan/)?' + re.escape(PAGE_GATEWAY[lang]) + '"')

    def test_jekyll_layouts_and_gateways(self):
        for layout in ("landing.html", "installation.html", "geuljjaim.html", "geuljjaim-index.html"):
            text = (ROOT / "_layouts" / layout).read_text(encoding="utf-8")
            with self.subTest(layout=layout):
                self.assertRegex(text, r"gateway")
        for gateway in GATEWAY.values():
            text = (ROOT / gateway).read_text(encoding="utf-8")
            with self.subTest(gateway=gateway):
                self.assertNotIn("準備中", text.split('id="language-zh-hans"')[1].split("</article>")[0])
                for other in GATEWAY.values():
                    self.assertIn(f'href="{other}"', text)


class InstallGuideParity(unittest.TestCase):
    def test_shared_stylesheet_contains_canonical_guide_css(self):
        layout = (ROOT / "_layouts/installation.html").read_text(encoding="utf-8")
        canonical = re.search(r"<style>([\s\S]*?)</style>", layout).group(1).strip("\n")
        self.assertIn(canonical, (ROOT / "assets/kumihan-install.css").read_text(encoding="utf-8"))

    def test_product_install_guides_use_canonical_frame(self):
        pages = [f"docs/install-kumihan-th-{h}{s}.html" for h in ("chatgpt", "claude", "gemini") for s in ("", ".en", ".ja")]
        pages += [f"docs/install-zilu-{h}{s}.html" for h in ("chatgpt", "claude", "gemini") for s in ("", ".en", ".ja")]
        pages += [f"docs/install-ziheng{h}{s}.html" for h in ("", "-claude", "-gemini") for s in ("", ".en", ".ja")]
        pages += [f"docs/install-accord-{h}{s}.html" for h in ("chatgpt", "claude", "gemini") for s in ("", ".en", ".ja")]
        pages += [f"docs/install-kumihan-ar-{h}{s}.html" for h in ("chatgpt", "claude", "gemini") for s in ("", ".en", ".ja")]
        pages += [f"docs/install-compasso-{h}{s}.html" for h in ("chatgpt", "claude", "gemini") for s in ("", ".en", ".ja")]
        pages += [f"docs/install-grafia-{h}{s}.html" for h in ("chatgpt", "claude", "gemini") for s in ("", ".en", ".ja")]
        pages += [f"docs/install-kumihan-hi-{h}{s}.html" for h in ("chatgpt", "claude", "gemini") for s in ("", ".en", ".ja")]
        pages += [f"docs/install-szyk-{h}{s}.html" for h in ("chatgpt", "claude", "gemini") for s in ("", ".en", ".ja")]
        pages += ["_layouts/geuljjaim.html"]
        for page in pages:
            with self.subTest(page=page):
                text = (ROOT / page).read_text(encoding="utf-8")
                self.assertIn("kumihan-install.css", text)
                for token in GUIDE_SKELETON:
                    self.assertRegex(text, r'class="[^"]*\b' + re.escape(token) + r'\b')
                self.assertEqual(text.count("<h1"), 1)
                if not page.startswith("_layouts/"):
                    # Current host tab and current language are both marked.
                    self.assertGreaterEqual(text.count('aria-current="page"'), 3)


if __name__ == "__main__":
    unittest.main()
