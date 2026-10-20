import importlib.util
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('thai_source', ROOT/'plugins/kumihan-th/runtime/check_source.py')
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)

# The immutable Thai baseline still asserts all 18 context and rule records.
# Only the registered Ziheng source transition may supply 12 exact new outputs.
LOCALE_BASELINE_SHA256 = '52307ccadbe04ced592d2854c4d4ecfbb15551ba281d70a104cec6eb750b4f3a'
ZIHENG_OUTPUT_TRANSITION_SHA256 = '3136ef8a1cbcf85eba725a14f0a1a0f24a5bea3f84b6f22d1f80a7f64687cc79'


def ziheng_rules_transition(record, root=ROOT):
    import hashlib
    import json
    import sys
    sys.path.insert(0, str(ROOT))
    from tools.ziheng_v020_transition import allowed
    root = Path(root)
    try:
        baseline_raw = (root/'tests/thai/locale-baseline.json').read_bytes()
        fixture_raw = (root/'docs/development/zh-hant-v020-20261020/locale-output-transition.json').read_bytes()
        if hashlib.sha256(baseline_raw).hexdigest() != LOCALE_BASELINE_SHA256:
            return None
        if hashlib.sha256(fixture_raw).hexdigest() != ZIHENG_OUTPUT_TRANSITION_SHA256:
            return None
        data = json.loads(fixture_raw)
        if (data['format'] != 'ziheng-locale-output-transition-1'
                or data['base_commit'] != '5f4925460e118398f99003ff475bcc686c1c2e76'
                or data['baseline_sha256'] != LOCALE_BASELINE_SHA256
                or data['rules_path'] != 'plugins/kumihan-ziheng/rules/zh-hant.json'):
            return None
        expected = {(locale, medium) for locale in ('zh-Hant-TW', 'zh-Hant-HK')
                    for medium in ('web-editorial', 'web-marketing', 'web-ui',
                                   'report-document', 'presentation', 'display-copy')}
        rows = data['records']
        indexed = {(row['locale'], row['medium']): row for row in rows}
        if len(rows) != 12 or set(indexed) != expected:
            return None
        row = indexed.get((record['locale'], record['medium']))
        if (row is None or row['before'] != record['rules_sha256']
                or row['context_sha256'] != record['context_sha256']):
            return None
        ledger = json.loads((root/'docs/development/zh-hant-v020-20261020/source-transition.json').read_bytes())
        source = ledger['updates']['protected'][data['rules_path']]
        if (source['main_before'] != data['rules_before']
                or source['after'] != data['rules_after']
                or hashlib.sha256((root/data['rules_path']).read_bytes()).hexdigest() != data['rules_after']
                or not allowed(data['rules_path'], 'protected', root)):
            return None
        return row['after']
    except (OSError, ValueError, KeyError, TypeError):
        return None


class IntegrityTests(unittest.TestCase):
    def test_positive_and_negative_unicode(self):
        for source in ['เก', 'น้ำ', 'ก่ํ', '😀ไทย', 'ชื่อแบรนด์', '\u200b\u2060\u00a0\ufeff']:
            self.assertEqual(helper.compare(source, source)['status'], 'passed')
            self.assertEqual(helper.compare(source, source+' ')['status'], 'failed')
    def test_utf16_protected_range(self):
        result = helper.compare('😀ไทย', '😀ไทX', [{'start': 2, 'end': 5}])
        self.assertEqual(result['protected'][0]['status'], 'failed')
        self.assertEqual(helper.compare('😀ไทย', '😀ไทย', [{'start': 1, 'end': 3}])['protected'][0]['status'], 'not-checked')
    def test_bounds(self):
        with self.assertRaises(ValueError): helper.compare('x'*(helper.MAX_BYTES+1), '')
    def test_offsets_are_utf16(self):
        self.assertEqual(helper.inspect('😀ไทย\u200b')['controls'][0]['utf16_offset'],5)

class LocaleTests(unittest.TestCase):
    def test_existing_locale_outputs_match_base(self):
        import hashlib
        import json
        import sys
        sys.path.insert(0, str(ROOT))
        from tools.locale_resolver import resolve_context, resolve_rules
        baseline_raw = (ROOT/'tests/thai/locale-baseline.json').read_bytes()
        self.assertEqual(hashlib.sha256(baseline_raw).hexdigest(), LOCALE_BASELINE_SHA256)
        baseline = json.loads(baseline_raw)
        self.assertEqual(baseline['base_commit'], '5f4925460e118398f99003ff475bcc686c1c2e76')
        self.assertEqual(len(baseline['records']), 18)
        def digest(value):
            encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
            return hashlib.sha256(encoded).hexdigest()
        for record in baseline['records']:
            with self.subTest(locale=record['locale'], medium=record['medium']):
                context = resolve_context(record['locale'], record['medium'])
                self.assertEqual(digest(context), record['context_sha256'])
                expected = ziheng_rules_transition(record, ROOT) or record['rules_sha256']
                self.assertEqual(digest(resolve_rules(context, ROOT)), expected)
    def test_thai_explicit_profiles(self):
        import sys
        sys.path.insert(0,str(ROOT))
        from tools.locale_resolver import resolve_context, resolve_rules, MEDIA
        for medium in MEDIA:
            context=resolve_context('th-TH',medium)
            self.assertEqual(context['script'],'Thai')
            self.assertEqual(len(resolve_rules(context,ROOT)),32)
        for locale in ['th', '', None]:
            with self.assertRaises(ValueError): resolve_context(locale,'web-ui')
