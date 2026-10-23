"""Vertical contracts: selection/integrity/declaration tests, not visual acceptance."""
import copy
import hashlib
import json
import unittest
from pathlib import Path

from test_ziheng_v020_context import BASE, ROOT, load


def read(path):
    return json.loads((BASE / path).read_text(encoding='utf-8'))


class VerticalFixtureTests(unittest.TestCase):
    def setUp(self):
        self.api = load('checks')
        self.suite = read('fixtures/research-v022/cases.json')

    def test_all_30_templates_are_structurally_valid_and_unexecuted(self):
        self.assertEqual(self.api.validate_vertical_suite(self.suite), [])
        fixtures = self.suite['fixtures']
        self.assertEqual({g: sum(f['group'] == g for f in fixtures) for g in ('TW', 'HK', 'shared')}, {'TW': 12, 'HK': 10, 'shared': 8})
        sources = {s['id'] for s in read('sources.json')['sources']}
        mapping = read('references/vertical-adoption.json')
        candidates = {c['candidate_id'] for c in mapping['candidates']}
        for f in fixtures:
            with self.subTest(fixture=f['id']):
                self.assertTrue(set(f['source_refs']) <= sources)
                self.assertTrue(set(f['candidate_ids']) <= candidates)
                self.assertEqual(f['status'], 'not-checked')
                self.assertIsNone(f['result'])
                self.assertEqual(f['execution_evidence'], [])
                self.assertEqual(set(f['execution_status_by_method'].values()), {'not-checked'})
                load('context').resolve_review_context(f['review_context'])

    def test_unicode_changes_are_detected_without_normalization(self):
        f = copy.deepcopy(next(f for f in self.suite['fixtures'] if f['id'] == 'V-SH01'))
        self.assertIn('e\u0301', f['text'])
        f['text'] = f['text'].replace('e\u0301', 'é')
        self.assertTrue(self.api.validate_vertical_fixture(f))
        for original, changed in [('臺', '台'), ('裏', '裡'), ('葛\U000e0100', '葛'), ('👩\u200d💻', '👩💻'), ('\r\n', '\n')]:
            with self.subTest(original=original):
                result = self.api.check_preservation(original.encode(), changed.encode())
                self.assertEqual(result['status'], 'failed')
                self.assertEqual(result['method'], 'static')

    def test_annotation_uses_code_points_and_exact_substrings(self):
        f = copy.deepcopy(next(f for f in self.suite['fixtures'] if f['id'] == 'V-TW06'))
        f['annotations'][0]['end_code_point_exclusive'] = True
        self.assertTrue(self.api.validate_vertical_fixture(f))
        f = copy.deepcopy(next(f for f in self.suite['fixtures'] if f['id'] == 'V-TW07'))
        f['annotations'][0]['text'] = '林清'
        self.assertTrue(self.api.validate_vertical_fixture(f))
        text = '😀e\u0301ABC'
        result = self.api.inspect_vertical_runs(text, [dict(text='ABC', start_code_point=3, end_code_point_exclusive=6, role='initialism', orientation='sideways')])
        self.assertEqual(result['errors'], [])
        self.assertFalse(result['source_changed'])
        self.assertIn('grapheme', result['limitations'][0])

    def test_shipped_template_cannot_import_a_render_pass(self):
        f = copy.deepcopy(self.suite['fixtures'][0]); f['status'] = 'passed'
        self.assertTrue(self.api.validate_vertical_fixture(f))
        f = copy.deepcopy(self.suite['fixtures'][0]); f['execution_status_by_method']['rendered'] = 'passed'
        self.assertTrue(self.api.validate_vertical_fixture(f))
        suite = copy.deepcopy(self.suite); suite['fixtures'][0]['id'] = suite['fixtures'][1]['id']
        self.assertTrue(self.api.validate_vertical_suite(suite))

    def test_full_input_digest_covers_annotations_and_context(self):
        f = copy.deepcopy(self.suite['fixtures'][5])
        original = self.api.fixture_input_sha256(f)
        self.assertNotEqual(original, f['text_utf8_sha256'])
        f['annotations'][0]['annotation_text'] = 'ㄔㄚˋ'
        self.assertNotEqual(original, self.api.fixture_input_sha256(f))
        f = copy.deepcopy(self.suite['fixtures'][5]); f['review_context']['editorial_style'] = 'publisher-defined'
        self.assertNotEqual(original, self.api.fixture_input_sha256(f))
        f = copy.deepcopy(self.suite['fixtures'][5]); f['status'] = 'failed'
        self.assertEqual(original, self.api.fixture_input_sha256(f))

    def test_meaningful_url_run_is_reviewed_not_rewritten(self):
        text = 'https://example.org/a?b=12'
        result = self.api.inspect_vertical_runs(text, [dict(text=text, start_code_point=0, end_code_point_exclusive=len(text), role='url', orientation='combine-upright')])
        self.assertEqual(result['errors'], [])
        self.assertEqual(result['findings'][0]['status'], 'needs-review')
        self.assertFalse(result['source_changed'])
        self.assertNotIn('artifact_status', result)

    def test_supplied_column_breaks_do_not_become_a_layout_pass(self):
        text = '😀甲——乙……丙'
        result = self.api.inspect_vertical_pair_breaks(text, [3, 6])
        self.assertEqual({f['break_code_point'] for f in result['findings']}, {3, 6})
        result = self.api.inspect_vertical_pair_breaks(text, [2, 4, 5, 7])
        self.assertEqual(result['findings'], [])
        self.assertNotIn('status', result)
        with self.assertRaises(ValueError): self.api.inspect_vertical_pair_breaks(text, [True])

    def test_fixture_schema_with_relative_context_contract(self):
        import jsonschema
        from referencing import Registry, Resource
        context = read('schemas/review-context-v2.schema.json')
        fixture = read('schemas/vertical-fixtures-v022.schema.json')
        uri = 'https://example.org/schemas/vertical-fixtures-v022.schema.json'
        fixture['$id'] = uri
        registry = Registry().with_resource('https://example.org/schemas/review-context-v2.schema.json', Resource.from_contents(context))
        jsonschema.Draft202012Validator.check_schema(fixture)
        jsonschema.Draft202012Validator(fixture, registry=registry).validate(self.suite)


class VerticalSelectionTests(unittest.TestCase):
    def setUp(self):
        self.api = load('context')
        self.records = read('rules/zh-hant.json')
        self.profile = {'id': 'web-editorial', 'rule_ids': [r['id'] for r in self.records]}
        self.context = dict(content_locale='zh-Hant-TW', medium='web-editorial', editorial_style='TW-MOE-reference', element_role='prose', expression_mode='reading', writing_mode='vertical-rl')

    def select(self, **changes):
        context = dict(self.context); context.update(changes)
        return self.api.select_review_rules(context, self.records, self.profile)

    def test_vertical_font_and_role_obligations_are_not_passes(self):
        result = self.select()
        for rid in ('ZH-HANT-012', 'ZH-HANT-016', 'ZH-HANT-018'):
            self.assertIn(rid, result['applicable_rule_ids'])
        self.assertNotIn('ZH-HANT-017', result['applicable_rule_ids'])
        self.assertNotIn('status', result)
        self.assertEqual(set(result['candidate_rule_ids']), set(result['applicable_rule_ids']) | {r['rule_id'] for r in result['deferred_rules']})
        self.assertEqual(len(result['candidate_rule_ids']), len(set(result['candidate_rule_ids'])))

    def test_horizontal_and_unspecified_roles_defer_new_vertical_contracts(self):
        result = self.select(writing_mode='horizontal-tb')
        for rid in ('ZH-HANT-016', 'ZH-HANT-017', 'ZH-HANT-018'):
            self.assertNotIn(rid, result['applicable_rule_ids'])
        for change in ({'element_role': None}, {'expression_mode': None}):
            self.assertNotIn('ZH-HANT-018', self.select(**change)['applicable_rule_ids'])

    def test_neutral_unknown_region_is_not_regional_acceptance(self):
        result = self.select(content_locale='zh-Hant', editorial_style=None)
        for rid in ('ZH-HANT-016', 'ZH-HANT-018'):
            self.assertIn(rid, result['applicable_rule_ids'])
        self.assertNotIn('ZH-HANT-017', result['applicable_rule_ids'])
        self.assertTrue(any('regional glyph' in x for x in result['limitations']))
        result = self.select(content_locale='zh-Hant-MO', editorial_style=None)
        self.assertNotIn('ZH-HANT-004', result['applicable_rule_ids'])
        result = self.select(content_locale='en-US')
        self.assertNotIn('ZH-HANT-016', result['applicable_rule_ids'])

    def test_decoration_requires_feature_and_editorial_style(self):
        for feature in ('proper-name-mark', 'title-mark', 'text-emphasis'):
            self.assertIn('ZH-HANT-017', self.select(features=[feature])['applicable_rule_ids'])
            self.assertNotIn('ZH-HANT-017', self.select(features=[feature], editorial_style=None)['applicable_rule_ids'])
        self.assertNotIn('ZH-HANT-017', self.select(features=['ruby'])['applicable_rule_ids'])

    def test_vertical_lr_retains_review_obligation_and_explicit_limitation(self):
        result = self.select(writing_mode='vertical-lr')
        self.assertIn('ZH-HANT-012', result['applicable_rule_ids'])
        self.assertTrue(any('vertical-lr' in limit for limit in result['limitations']))
        self.assertNotIn('normalized_context', result)


class VerticalEvidenceTests(unittest.TestCase):
    def setUp(self): self.api = load('evidence')

    def record(self, method='static', scope='source-preservation'):
        return dict(schema_version='0.2.2', fixture_id='V-TW01', variant_id='vertical-baseline', artifact={'path': 'sample.html', 'sha256': 'a'*64}, full_input_bundle_sha256='b'*64, method=method, scope=scope, status='passed', evidence_refs=[{'path': 'observation.json', 'kind': 'byte-comparison', 'artifact_sha256': 'a'*64}], limitations=['Synthetic declaration used only to exercise validation; not an executed typography fixture.'], observation='Declared test observation', reviewer={'id': 'test-reviewer', 'date': '2026-10-22'})

    def rendered(self, scope='vertical-glyph'):
        r = self.record('rendered', scope)
        r['evidence_refs'] = [dict(path='render.png', kind='screenshot', artifact_sha256='a'*64), dict(path='glyphs.json', kind='glyph-observation', artifact_sha256='a'*64)]
        r['environment'] = dict(target='web', os='test-os', application='test-browser', application_version='test-version', engine='test-engine', engine_version='test-version', dimensions={'width': 960, 'height': 256, 'unit': 'CSS-px'}, zoom={'method': 'viewport resize', 'factor': 1})
        r['layout'] = dict(writing_mode='vertical-rl', text_orientation='mixed', font_size='20px', font_weight='400', line_height='1.8', letter_spacing='normal', inline_size='16em', tcy='none', enabled_font_features=[])
        r['fonts'] = [dict(family='test-family', face='regular', release='tag-1.0', internal_version='Version 0.9', sha256='c'*64, fallback='none observed in scope', actual_used=True)]
        r['shaping'] = dict(renderer_path='CSS Writing Modes', vertical_metrics='vhea/vmtx observed', feature_application='engine-managed vert; actual glyph observation recorded')
        return r

    def test_static_is_valid_without_browser_and_cannot_pass_glyphs(self):
        self.assertEqual(self.api.validate_vertical_evidence(self.record()), [])
        for scope in ('vertical-glyph', 'regional-glyph', 'punctuation-placement', 'reflow', 'native-reopen', 'native-proofreading'):
            self.assertTrue(self.api.validate_vertical_evidence(self.record(scope=scope)))

    def test_glyph_declaration_needs_instance_and_shaping_not_font_brand(self):
        r = self.rendered(); self.assertEqual(self.api.validate_vertical_evidence(r), [])
        for field in ('sha256', 'internal_version', 'release', 'actual_used'):
            bad = copy.deepcopy(r); bad['fonts'][0].pop(field)
            self.assertTrue(self.api.validate_vertical_evidence(bad), field)
        bad = copy.deepcopy(r); bad.pop('shaping')
        self.assertTrue(self.api.validate_vertical_evidence(bad))
        bad = copy.deepcopy(r); bad['evidence_refs'] = bad['evidence_refs'][:1]
        self.assertTrue(self.api.validate_vertical_evidence(bad))

    def test_mismatched_digest_and_css_only_are_rejected(self):
        r = self.rendered(); r['evidence_refs'][0]['artifact_sha256'] = 'd'*64
        self.assertTrue(self.api.validate_vertical_evidence(r))
        r = self.rendered(); r['evidence_refs'] = [dict(path='style.css', kind='css-declaration', artifact_sha256='a'*64)]
        self.assertTrue(self.api.validate_vertical_evidence(r))

    def test_reflow_tracks_scroll_direction_not_writing_direction(self):
        r = self.rendered('reflow')
        r['reflow'] = dict(scroll_direction='horizontal', constraint_axis='height', constraint_css_px=256)
        self.assertEqual(self.api.validate_vertical_evidence(r), [])
        r['reflow']['constraint_axis'] = 'width'; r['reflow']['constraint_css_px'] = 320
        self.assertTrue(self.api.validate_vertical_evidence(r))
        r['reflow']['scroll_direction'] = 'vertical'
        self.assertTrue(self.api.validate_vertical_evidence(r))
        r['environment']['dimensions']['width'] = 320
        self.assertEqual(self.api.validate_vertical_evidence(r), [])

    def test_native_application_and_native_proofreading_are_separate(self):
        r = self.rendered('native-reopen'); r['method'] = 'native-application'
        r['environment']['target'] = 'office'
        r['evidence_refs'] = [dict(path='reopen.json', kind='native-application-log', artifact_sha256='a'*64)]
        self.assertEqual(self.api.validate_vertical_evidence(r), [])
        r['scope'] = 'native-proofreading'
        self.assertTrue(self.api.validate_vertical_evidence(r))
        r = self.record('native-proofreading', 'native-proofreading')
        r['evidence_refs'][0]['kind'] = 'editorial-review'
        self.assertTrue(self.api.validate_vertical_evidence(r))
        r['reviewer'].update(locale='zh-Hant-TW', editorial_scope='TW punctuation and reading order')
        self.assertEqual(self.api.validate_vertical_evidence(r), [])

    def test_at_requires_actual_interaction_and_at_environment(self):
        r = self.rendered('assistive-technology'); r['method'] = 'interaction'
        self.assertTrue(self.api.validate_vertical_evidence(r))
        r['evidence_refs'] = [dict(path='at.json', kind='interaction-log', artifact_sha256='a'*64)]
        r['environment']['assistive_technology'] = {'name': 'test-AT', 'version': 'test-version'}
        self.assertEqual(self.api.validate_vertical_evidence(r), [])

    def test_nonexecution_and_waiver_do_not_become_success(self):
        for status in self.api.STATUSES:
            if status == 'passed': continue
            r = self.record(); r['status'] = status; r['evidence_refs'] = []
            if status in ('waived', 'unsupported', 'not-applicable'): r['reason'] = 'Explicit test-only reason'
            if status == 'waived': r['waiver'] = {'approval_ref': 'test-approval', 'artifact_sha256': 'a'*64}
            self.assertEqual(self.api.validate_vertical_evidence(r), [], status)
            self.assertEqual(r['status'], status)
        r = self.record(); r['status'] = 'waived'; r['reason'] = 'test'; r['waiver'] = {'approval_ref': 'x', 'artifact_sha256': 'b'*64}
        self.assertTrue(self.api.validate_vertical_evidence(r))

    def test_evidence_schema_and_new_rule_ids(self):
        import jsonschema
        schema = read('schemas/vertical-evidence-v022.schema.json')
        jsonschema.Draft202012Validator.check_schema(schema)
        for r in (self.record(), self.rendered()): jsonschema.validate(r, schema)
        enum = read('schemas/rule.schema.json')['$defs']['rule_id']['enum']
        for i in (16, 17, 18): self.assertIn(f'ZH-HANT-{i:03d}', enum)
