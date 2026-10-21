"""The Japanese and English Nhịp Chữ pages use the shared KUMIHAN copy (tools/base_copy.py).

Vietnamese-specific text (feature 01, the fidelity detail, the entry skill,
release status and the bilingual-description note) stays edition-specific.
"""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import base_copy  # noqa: E402

KEYS = ("title", "description", "nav", "eyebrow", "h1", "lead", "cta", "hero_foot", "concept_h2", "concept_body",
        "features_h2", "features_deck", "idea_h2", "idea_body", "skills_h2", "skills_deck", "install_h2",
        "install_notes", "status_title", "cta_h2", "cta_body", "cta_button", "footer_sub")


class SharedCopy(unittest.TestCase):
    def test_japanese_and_english_follow_the_shared_copy(self):
        data = json.loads((ROOT / "assets/nhip-chu-site-copy.json").read_text(encoding="utf-8"))
        for lang in ("ja", "en"):
            shared, copy = base_copy.shared(lang, "vi"), data[lang]
            for key in KEYS:
                with self.subTest(lang=lang, key=key):
                    self.assertEqual(copy[key], shared[key])
            self.assertTrue(copy["install_body"].startswith(shared["install_body"]))
            for i in (1, 3):
                self.assertEqual(copy["features"][i], shared["features"][i])


if __name__ == "__main__":
    unittest.main()
