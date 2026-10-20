"""Bounded PR #122 source integration and fail-closed retention regressions."""
import copy
import hashlib
import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
PREFIX = 'docs/development/zh-hant-v020-20261020/'
sys.path.insert(0, str(ROOT/'tools'))
BASELINE = json.loads((ROOT/PREFIX/'evidence/shared-integration-baseline.json').read_text())


class SharedIntegrationTests(unittest.TestCase):
    def test_ziheng_source_bump_preserves_publication_facts(self):
        editions = json.loads((ROOT/'assets/edition-versions.json').read_text())['editions']
        current = copy.deepcopy(editions['zh-hant'])
        self.assertEqual(current.pop('source_version'), '0.2.0')
        before = copy.deepcopy(BASELINE['editions']['zh-hant'])
        before.pop('source_version')
        self.assertEqual(current, before)
        self.assertIsNone(current['published_version'])
        self.assertEqual(current['release_status'], 'unpublished')

    def test_other_edition_facts_are_unchanged(self):
        editions = json.loads((ROOT/'assets/edition-versions.json').read_text())['editions']
        self.assertEqual(set(editions), set(BASELINE['editions']))
        for code, before in BASELINE['editions'].items():
            if code != 'zh-hant':
                with self.subTest(edition=code):
                    self.assertEqual(editions[code], before)
        for rel, before in BASELINE['protected'].items():
            with self.subTest(path=rel):
                raw = (ROOT/rel).read_bytes()
                self.assertEqual(len(raw), before['bytes'])
                self.assertEqual(hashlib.sha256(raw).hexdigest(), before['sha256'])

    def test_history_manifest_exception_requires_exact_retention(self):
        from ziheng_retention import is_retained_manifest, FOLDERS, PRODUCT
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            shutil.copytree(ROOT/PRODUCT, root/PRODUCT, ignore=shutil.ignore_patterns('__pycache__'))
            for folder in FOLDERS:
                valid = root/PRODUCT/folder/'history/0.1.0/MANIFEST.json'
                self.assertTrue(is_retained_manifest(root, valid))
                raw = valid.read_bytes()
                valid.write_bytes(raw + b' ')
                with self.assertRaises(ValueError):
                    is_retained_manifest(root, valid)
                valid.write_bytes(raw)
            for rel in ('plugins/kumihan-zilu/downloads/history/0.1.0/MANIFEST.json',
                        PRODUCT+'/downloads/history/unregistered/MANIFEST.json'):
                target = root/rel
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text('{"version":"0.1.0"}')
                self.assertFalse(is_retained_manifest(root, target))
            # Unknown histories still reach the original version assertion.
            import test_version_naming as naming
            product = root/'plugins/kumihan-zilu'
            (root/'plugin.json').write_text('{"version":"0.1.8"}')
            (product/'plugin.json').write_text('{"version":"0.2.0"}')
            case = naming.VersionNamingPolicyTests('test_current_distribution_manifest_versions_match_their_products')
            with patch.object(naming, 'ROOT', root):
                result = unittest.TestResult()
                case.run(result)
            self.assertTrue(result.failures, 'other-product historical manifest bypassed version assertion')
            self.assertEqual(result.errors, [])

    def test_transition_rejects_unknown_path_and_changed_preimage(self):
        import ziheng_v020_transition as transition
        rel = 'plugins/kumihan-ziheng/plugin.json'
        names = (PREFIX+'source-transition.json', PREFIX+'source-transition-baseline.json',
                 'docs/seo/evidence/20261019-main-preservation.json', rel)
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            for name in names:
                target = root/name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT/name, target)
            self.assertTrue(transition.allowed(rel, 'protected', root))
            self.assertFalse(transition.allowed('plugins/kumihan-ziheng/unknown.json', 'protected', root))
            ledger = root/PREFIX/'source-transition.json'
            original = ledger.read_bytes()
            for key in ('main_before', 'snapshot_before', 'after'):
                data = json.loads(original)
                data['updates']['protected'][rel][key] = '0'*64
                ledger.write_text(json.dumps(data))
                self.assertFalse(transition.allowed(rel, 'protected', root), key)
            ledger.write_bytes(original)
            frozen = root/PREFIX/'source-transition-baseline.json'
            frozen.write_bytes(frozen.read_bytes()+b' ')
            self.assertFalse(transition.allowed(rel, 'protected', root))
            shutil.copy2(ROOT/PREFIX/'source-transition-baseline.json', frozen)
            snapshot = root/'docs/seo/evidence/20261019-main-preservation.json'
            data = json.loads(snapshot.read_bytes())
            data['protected'][rel] = '0'*64
            snapshot.write_text(json.dumps(data))
            self.assertFalse(transition.allowed(rel, 'protected', root))
            shutil.copy2(ROOT/'docs/seo/evidence/20261019-main-preservation.json', snapshot)
            (root/rel).write_text('{}')
            self.assertFalse(transition.allowed(rel, 'protected', root))

    def test_legacy_zip_mutation_remains_rejected(self):
        from ziheng_retention import retained_outputs, FOLDERS, PRODUCT
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            shutil.copytree(ROOT/PRODUCT, root/PRODUCT, ignore=shutil.ignore_patterns('__pycache__'))
            old = {rel: raw for rel, raw in retained_outputs(root, FOLDERS).items() if rel.endswith('.zip')}
            current = {p.relative_to(root).as_posix() for p in (root/PRODUCT).rglob('*-0.2.0.zip')}
            self.assertEqual(len(old), 15)
            self.assertEqual(len(current), 15)
            self.assertFalse(set(old) & current)
            rel, raw = next(iter(old.items()))
            target = root/rel
            target.write_bytes(bytes([raw[0] ^ 1])+raw[1:])
            with self.assertRaises(ValueError):
                retained_outputs(root, FOLDERS)
            target.write_bytes(raw)
            self.assertEqual(retained_outputs(root, FOLDERS)[rel], raw)
            target.unlink()
            with self.assertRaises(ValueError):
                retained_outputs(root, FOLDERS)

    def test_cross_locale_transition_rejects_unregistered_or_tampered_outputs(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location('thai_shared_consumer', ROOT/'tests/thai/test_core.py')
        consumer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(consumer)
        self.assertTrue(hasattr(consumer, 'ziheng_rules_transition'), 'exact cross-locale transition consumer missing')
        baseline = json.loads((ROOT/'tests/thai/locale-baseline.json').read_text())
        record = next(row for row in baseline['records'] if row['locale']=='zh-Hant-TW')
        self.assertIsNotNone(consumer.ziheng_rules_transition(record, ROOT))
        for key, value in [('locale', 'zh-Hant-MO'), ('medium', 'unknown'), ('rules_sha256', '0'*64), ('context_sha256', '0'*64)]:
            changed = dict(record, **{key: value})
            self.assertIsNone(consumer.ziheng_rules_transition(changed, ROOT), key)
        fixture = PREFIX+'locale-output-transition.json'
        rel = 'plugins/kumihan-ziheng/rules/zh-hant.json'
        names = (fixture, PREFIX+'source-transition.json', PREFIX+'source-transition-baseline.json',
                 'docs/seo/evidence/20261019-main-preservation.json', 'tests/thai/locale-baseline.json', rel)
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            for name in names:
                target = root/name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT/name, target)
            self.assertIsNotNone(consumer.ziheng_rules_transition(record, root))
            target = root/fixture
            original = target.read_bytes()
            for mutation in ('after', 'before', 'missing', 'additional'):
                data = json.loads(original)
                if mutation == 'missing':
                    data['records'].pop()
                elif mutation == 'additional':
                    data['records'].append(dict(data['records'][0], medium='unknown'))
                else:
                    data['records'][0][mutation] = '0'*64
                target.write_text(json.dumps(data))
                self.assertIsNone(consumer.ziheng_rules_transition(record, root), mutation)
            target.write_bytes(original)
            target = root/'tests/thai/locale-baseline.json'
            original = target.read_bytes()
            target.write_bytes(original+b' ')
            self.assertIsNone(consumer.ziheng_rules_transition(record, root))
            target.write_bytes(original)
            target = root/PREFIX/'source-transition.json'
            original = target.read_bytes()
            data = json.loads(original)
            data['updates']['protected'][rel]['main_before'] = '0'*64
            target.write_text(json.dumps(data))
            self.assertIsNone(consumer.ziheng_rules_transition(record, root))
            target.write_bytes(original)
            (root/rel).write_bytes((root/rel).read_bytes()+b' ')
            self.assertIsNone(consumer.ziheng_rules_transition(record, root))
            # Matching a tampered ledger to tampered bytes cannot broaden admission.
            data = json.loads(original)
            data['updates']['protected'][rel]['after'] = hashlib.sha256((root/rel).read_bytes()).hexdigest()
            target.write_text(json.dumps(data))
            self.assertIsNone(consumer.ziheng_rules_transition(record, root))

    def test_source_links_keep_versions_distinct(self):
        from version_display import source_archives
        old = source_archives('zh-hant', '0.1.0')
        new = source_archives('zh-hant', '0.2.0')
        self.assertEqual(len(old), 15)
        self.assertEqual(len(new), 15)
        self.assertFalse(old & new)
        for p in [*ROOT.glob('kumihan-zh-han*.html'), *(ROOT/'docs').glob('install-ziheng*.html')]:
            text = p.read_text()
            with self.subTest(path=p.name):
                self.assertIn('data-release-status="unpublished"', text)
                self.assertIn('v0.2.0</bdi>', text)
                self.assertNotIn('data-release-status="published"', text)
                for url, label in re.findall(r'<a\b[^>]*href="([^"]+0\.1\.0\.zip)"[^>]*>(.*?)</a>', text, re.S):
                    self.assertIn('0.1.0', re.sub('<[^>]+>', '', label), url)
                self.assertNotRegex(text, r'https://raw\.githubusercontent\.com/landco-llc/kumihan/main/[^" ]*0\.2\.0\.zip')
