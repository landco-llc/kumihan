"""Editions whose skills distinguish regions show them in the dark band, as KUMIHAN｜字衡 does."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# edition copy file -> (plugin, landing pages)
EDITIONS = {
    "accord": ("kumihan-accord", "kumihan-fr"), "equilibrio": ("kumihan-equilibrio", "kumihan-it"),
    "satzbild": ("kumihan-satzbild", "kumihan-de"), "grafia": ("kumihan-grafia", "kumihan-es"),
    "compasso": ("kumihan-compasso", "kumihan-pt"), "mizani": ("kumihan-mizani", "kumihan-sw"),
    "ar": ("kumihan-ar", "kumihan-ar"), "fa": ("kumihan-fa", "kumihan-fa"),
}


def plugin_text(plugin):
    return "\n".join(p.read_text(encoding="utf-8", errors="ignore")
                     for p in (ROOT / "plugins" / plugin).rglob("*") if p.suffix in (".json", ".md", ".py"))


class RegionBands(unittest.TestCase):
    def check(self, page, regions, source):
        html = (ROOT / page).read_text(encoding="utf-8")
        band = re.search(r'<section class="idea-band" id="regions"[\s\S]*?</section>', html)
        self.assertIsNotNone(band, page)
        codes = re.findall(r'<code lang="en" dir="ltr">([^<]+)</code>', band[0])
        self.assertEqual(codes, [c["code"] for c in regions["cards"]], page)
        for code in codes:
            self.assertIn(code, source, f"{page}: {code} is not a region of the plugin")

    def test_product_site_editions(self):
        for name, (plugin, stem) in EDITIONS.items():
            copy = json.loads((ROOT / f"assets/{name}-site-copy.json").read_text(encoding="utf-8"))
            source = plugin_text(plugin)
            for lang, c in copy.items():
                page = f"{stem}.html" if lang not in ("en", "ja") else f"{stem}.{lang}.html"
                with self.subTest(page=page):
                    self.check(page, c["regions"], source)

    def test_bangla_templates(self):
        source = plugin_text("kumihan-bn")
        for page in ("kumihan-bn.html", "kumihan-bn.en.html", "kumihan-bn.ja.html"):
            html = (ROOT / page).read_text(encoding="utf-8")
            codes = re.findall(r'<code lang="en" dir="ltr">([^<]+)</code>', html)
            with self.subTest(page=page):
                self.assertEqual(codes, ["bn-BD", "bn-IN"])
                for code in codes:
                    self.assertIn(code, source)


if __name__ == "__main__":
    unittest.main()
