"""Polish pages keep one-letter words (a, i, o, u, w, z) off line ends (kumihan-szyk-web).

Static check of the generated text: each such word is followed by U+00A0, not a
plain space. Option flags in commands (e.g. "-a 256") are not words and are left alone.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOOSE = re.compile(r"(?<![\w/=-])[AaIiOoUuWwZz] (?=\w)")


def visible_text(html):
    html = re.sub(r"<(script|style|pre|code)[\s\S]*?</\1>", " ", html)
    return re.sub(r"<[^>]+>", "‖", html)


class OneLetterWords(unittest.TestCase):
    def test_polish_pages_bind_one_letter_words(self):
        pages = [ROOT / "kumihan-pl.html", ROOT / "top-pl.html", *(ROOT / "docs").glob("install-szyk-*.html")]
        pages = [p for p in pages if p.name in ("kumihan-pl.html", "top-pl.html") or not re.search(r"\.(en|ja)\.html$", p.name)]
        for path in pages:
            with self.subTest(page=path.name):
                self.assertEqual(LOOSE.findall(visible_text(path.read_text(encoding="utf-8"))), [])


if __name__ == "__main__":
    unittest.main()
