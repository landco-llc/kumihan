"""Grafía's admitted source transition must fail closed under tampering."""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


class GrafiaTransitionTests(unittest.TestCase):
    def test_exact_transition_rejects_unregistered_and_tampered_inputs(self):
        spec = importlib.util.spec_from_file_location('grafia_transition', ROOT / 'tools/grafia_v011_transition.py')
        transition = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(transition)
        rel = 'plugins/kumihan-grafia/fixtures/acceptance-ledger.json'
        self.assertTrue(transition.allowed(rel, 'protected', ROOT))
        self.assertFalse(transition.allowed(rel, 'invented-family', ROOT))
        self.assertFalse(transition.allowed('plugins/kumihan-grafia/unknown.json', 'protected', ROOT))
        self.assertFalse(transition.allowed(rel, 'protected', ROOT, expected_preimage='0' * 64))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            names = [*transition.FROZEN_INPUTS, transition.CONTRACT, rel]
            for name in names:
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / name, target)
            self.assertTrue(transition.allowed(rel, 'protected', root))
            target = root / rel
            original = target.read_bytes()
            target.write_bytes(original + b' ')
            self.assertFalse(transition.allowed(rel, 'protected', root))
            target.write_bytes(original)
            for name in [*transition.FROZEN_INPUTS, transition.CONTRACT]:
                target = root / name
                original = target.read_bytes()
                target.write_bytes(original + b' ')
                self.assertFalse(transition.allowed(rel, 'protected', root), name)
                target.write_bytes(original)
                self.assertTrue(transition.allowed(rel, 'protected', root), name)
            # Supplying a plausible but unrelated legacy hash must not broaden admission.
            self.assertFalse(transition.allowed(rel, 'protected', root, expected_preimage='f' * 64))

    def test_predecessor_normalization_rejects_other_cells_and_whitespace(self):
        spec = importlib.util.spec_from_file_location('grafia_transition', ROOT / 'tools/grafia_v011_transition.py')
        transition = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(transition)
        facts = (ROOT/'assets/edition-versions.json').read_bytes()
        readme = (ROOT/'README.md').read_bytes()
        self.assertNotEqual(transition.predecessor_facts(facts, ROOT), facts)
        self.assertNotEqual(transition.predecessor_readme(readme, ROOT), readme)
        for normalizer, raw in ((transition.predecessor_facts, facts), (transition.predecessor_readme, readme)):
            with self.assertRaises(ValueError): normalizer(raw+b' ', ROOT)
        forged = json.loads(facts)
        forged['editions']['en']['source_version'] = '9.9.9'
        with self.assertRaises(ValueError): transition.predecessor_facts((json.dumps(forged, ensure_ascii=False, indent=2)+'\n').encode(), ROOT)
        with self.assertRaises(ValueError): transition.predecessor_readme(readme.replace(b'| EN |', b'| XX |', 1), ROOT)
