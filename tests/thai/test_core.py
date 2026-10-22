import importlib.util
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('thai_source', ROOT/'plugins/kumihan-th/runtime/check_source.py')
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)



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
        from tools.ziheng_v022_transition import admitted_locale
        baseline_raw = (ROOT/'tests/thai/locale-baseline.json').read_bytes()
        baseline = json.loads(baseline_raw)
        self.assertEqual(len(baseline['records']), 18)
        def digest(value):
            encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
            return hashlib.sha256(encoded).hexdigest()
        for record in baseline['records']:
            with self.subTest(locale=record['locale'], medium=record['medium']):
                context = resolve_context(record['locale'], record['medium'])
                self.assertEqual(digest(context), record['context_sha256'])
                expected = record['rules_sha256']
                actual = digest(resolve_rules(context, ROOT))
                if not admitted_locale(ROOT, record['locale'], record['medium'],
                                       expected, digest(context), actual):
                    self.assertEqual(actual, expected)
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
