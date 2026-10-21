"""The Bangla Japanese and English pages carry the shared KUMIHAN copy (tools/base_copy.py).

The Bangla pages are maintained by hand, so this checks the rendered text
instead of a copy file. Skill labels (Web, Documents, Review) are not shown, and the
regional band takes the place of the shared idea band.
"""
import html
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import base_copy  # noqa: E402


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from strings(item)


class SharedCopy(unittest.TestCase):
    def test_ja_en_pages_use_shared_copy(self):
        for lang, page in (("ja", "kumihan-bn.ja.html"), ("en", "kumihan-bn.en.html")):
            text = html.unescape((ROOT / page).read_text(encoding="utf-8"))
            for key, value in base_copy.shared(lang, "bn").items():
                if key == "footer_sub":
                    continue  # every page shares tools/site_footer.py
                if key.startswith("idea_") and 'id="regions"' in text:
                    continue  # the dark band shows Bangladesh / India instead (product_site.band)
                if key == "skills":
                    value = [pair[1] for pair in value if pair]
                for s in strings(value):
                    with self.subTest(page=page, key=key, text=s):
                        self.assertIn(s, text)

    def test_ja_title_breaks_like_kumihan(self):
        text = (ROOT / "kumihan-bn.ja.html").read_text(encoding="utf-8")
        self.assertIn('<h1 id="hero-title">ベンガル語の<br>デザインを<br><span class="accent">もっと自然に</span></h1>', text)


if __name__ == "__main__":
    unittest.main()
