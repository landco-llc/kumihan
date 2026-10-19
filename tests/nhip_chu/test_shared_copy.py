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

KEYS = {"title": "title", "description": "description", "nav": "nav", "eyebrow": "eyebrow", "h1": "h1",
        "lead": "lead", "cta": "cta", "heroFoot": "hero_foot", "concept": "concept_h2",
        "conceptBody": "concept_body", "featuresH2": "features_h2", "featuresDeck": "features_deck",
        "idea": "idea_h2", "ideaBody": "idea_body", "skillsH2": "skills_h2", "skillsDeck": "skills_deck",
        "installH2": "install_h2", "installNotes": "install_notes", "statusTitle": "status_title",
        "finalH2": "cta_h2", "finalBody": "cta_body", "finalCta": "cta_button", "footerSub": "footer_sub"}


class SharedCopy(unittest.TestCase):
    def test_japanese_and_english_follow_the_shared_copy(self):
        data = json.loads((ROOT / "assets/nhip-chu-site-copy.json").read_text(encoding="utf-8"))
        for lang in ("ja", "en"):
            shared, copy = base_copy.shared(lang, "vi"), data[lang]
            for key, base_key in KEYS.items():
                with self.subTest(lang=lang, key=key):
                    self.assertEqual(copy[key], shared[base_key])
            self.assertTrue(copy["installBody"].startswith(shared["install_body"]))
            for i in (1, 3):
                self.assertEqual(copy["features"][i][2:], [shared["features"][i]["h3"], shared["features"][i]["p"]])


if __name__ == "__main__":
    unittest.main()
