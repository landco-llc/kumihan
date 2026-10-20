"""A new JA distribution keeps immutable older downloads and exact preservation."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))


class JapaneseReleaseTransition(unittest.TestCase):
    def test_retains_known_old_zip_and_rejects_changed_bytes(self):
        import build_dist as b
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = 'downloads Claude/skills/kumihan-Claude-skill-0.1.8.zip'
            p = root / path
            p.parent.mkdir(parents=True)
            p.write_bytes(b'original archive')
            ledger = {path: hashlib.sha256(p.read_bytes()).hexdigest()}
            self.assertEqual(b.retained_downloads(root, ledger), {path: p.read_bytes()})
            p.write_bytes(b'changed archive')
            with self.assertRaises(ValueError):
                b.retained_downloads(root, ledger)

    def test_retention_rejects_unrelated_and_traversal_paths(self):
        import build_dist as b
        for path in ('plugin.json', '../outside.zip', 'downloads Claude/skills/other-0.1.8.zip'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                b.retained_downloads(Path('/tmp'), {path: '0' * 64})

    def test_transition_cannot_allow_license_or_other_language(self):
        import ja_release_transition as j
        self.assertFalse(j.allowed('LICENSE'))
        self.assertFalse(j.allowed('plugins/kumihan-ziheng/plugin.json'))
        self.assertFalse(j.allowed('skills/kumihan/rules/catalog.json'))
        self.assertTrue(j.allowed('plugin.json'))

    def test_transition_requires_exact_before_and_after(self):
        import ja_release_transition as j
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / 'tests/contracts').mkdir(parents=True)
            (root / 'plugin.json').write_bytes(b'new')
            record = {'paths': {'plugin.json': {'before': 'old', 'after': hashlib.sha256(b'new').hexdigest()}}}
            (root / j.RECORD).write_text(json.dumps(record))
            self.assertTrue(j.admitted(root, 'plugin.json', 'old'))
            self.assertFalse(j.admitted(root, 'plugin.json', 'other'))
            (root / 'plugin.json').write_bytes(b'corrupt')
            self.assertFalse(j.admitted(root, 'plugin.json', 'old'))
