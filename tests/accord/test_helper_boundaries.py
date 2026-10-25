import importlib.util
import unittest
from pathlib import Path

PATH = Path(__file__).resolve().parents[2] / 'plugins/kumihan-accord/runtime/checks.py'
spec = importlib.util.spec_from_file_location('accord_helper_boundaries', PATH)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class HelperBoundaries(unittest.TestCase):
    def test_time_and_ratio_are_not_prose_colons(self):
        for text in ('Rendez-vous à 14:30.', 'Rapport 1:2.', '14:30:00'):
            self.assertEqual(m.inspect(text, house_style='fr-fr-editorial')['findings'], [])
            self.assertEqual(m.propose_generated_plain(text, 'fr-fr-editorial'), text)
        self.assertEqual(m.propose_generated_plain('Offre: demain', 'fr-fr-editorial'), 'Offre\u00a0: demain')

    def test_oqlf_validates_forms_instead_of_skipping(self):
        for mark in '!?;':
            for gap in ('', '\u202f'):
                text = 'Prêt' + gap + mark
                r = m.inspect(text, house_style='fr-ca-oqlf')
                self.assertEqual(r['findings'], [])
                self.assertEqual(r['evaluations'][0]['status'], 'accepted')
                self.assertEqual(r['proposal_policy']['id'], 'accord-generated-plain-repair@0.1.0')
                self.assertEqual(m.propose_generated_plain(text, 'fr-ca-oqlf'), text)
            self.assertEqual(len(m.inspect('Prêt ' + mark, house_style='fr-ca-oqlf')['findings']), 1)
            self.assertEqual(m.propose_generated_plain('Prêt ' + mark, 'fr-ca-oqlf'), 'Prêt' + mark)

    def test_colon_identity_and_original_ranges(self):
        r = m.inspect('Été Offre: 25 €', house_style='fr-fr-editorial')
        f = r['findings'][0]
        self.assertEqual(f['rule_id'], 'FR-FR-02')
        self.assertEqual(f['source_range'], {'start':9, 'end':10, 'unit':'unicode_code_point'})
        self.assertEqual(f['source_ref'], {'catalog':'accord-source-catalog@0.1.0', 'id':'FR01'})

    def test_leading_and_quote_initial_punctuation_is_preserved(self):
        for text in ('! Bonjour', '  ! Bonjour'):
            out = m.propose_generated_plain(text, 'fr-fr-editorial')
            self.assertNotIn('\u202f!', out)
        self.assertEqual(m.propose_generated_plain('«! Bonjour»', 'fr-fr-editorial'), '«\u202f! Bonjour\u202f»')
        self.assertEqual(m.inspect('! Bonjour', house_style='fr-fr-editorial')['findings'], [])

    def test_quotes_exact_padding_and_idempotence(self):
        for text in ('« bonjour »', '«\u202f bonjour\u202f»', 'Offre: «bonjour!»'):
            out = m.propose_generated_plain(text, 'fr-fr-editorial')
            self.assertEqual(m.propose_generated_plain(out, 'fr-fr-editorial'), out)
            self.assertEqual(m.inspect(out, house_style='fr-fr-editorial')['findings'], [])
        self.assertEqual(m.propose_generated_plain('«»', 'fr-fr-editorial'), '«»')

    def test_unknown_space_is_review_and_preserved(self):
        text = 'Prêt\u2009?'
        r = m.inspect(text, house_style='fr-ca-oqlf')
        self.assertEqual(r['evaluations'][0]['status'], 'needs_review')
        self.assertEqual(m.propose_generated_plain(text, 'fr-ca-oqlf'), text)
        text = '«\u2009bonjour\u2009»'
        self.assertEqual(m.propose_generated_plain(text, 'fr-fr-editorial'), text)

    def test_guard_and_source_preservation(self):
        text = 'Consultez https://example.org/a?b=1; puis `x:y`.'
        with self.assertRaises(ValueError): m.propose_generated_plain(text, 'fr-fr-editorial')
        self.assertEqual(m.inspect(text, house_style='fr-fr-editorial')['findings'], [])
        text = '<div title="Bonjour!">Oui!</div>'
        self.assertEqual(len(m.inspect(text, house_style='fr-fr-editorial')['findings']), 1)
        with self.assertRaises(ValueError): m.propose_generated_plain(text, 'fr-fr-editorial')


class ContextAdapter(unittest.TestCase):
    def test_unknown_and_conflicting_context_is_scoped(self):
        self.assertEqual(m.inspect_context('Bonjour!', {'language':'fr'}, raw_locale='fr-LU')['status'], 'outside_supported_scope')
        self.assertEqual(m.inspect_context('Bonjour!', {'language':'en'}, raw_locale='fr-FR')['status'], 'blocked')
        self.assertEqual(m.inspect_context('Bonjour!', {'language':'fr'}, raw_locale=None)['status'], 'needs_review')
        self.assertEqual(m.inspect_context('Bonjour!', {'language':'fr', 'extensions':[{'namespace':'x.y','version':'1.0.0','critical':True,'payload':{}}]}, raw_locale='fr-FR')['status'], 'blocked')

    def test_source_bound_protected_ranges_use_scalar_coordinates(self):
        import hashlib
        text = 'Été! Bonjour!'
        context = {'language':'fr', 'house_style':'fr-fr-editorial'}
        digest = hashlib.sha256(text.encode()).hexdigest()
        ranges = [{'start':0,'end':4,'coordinate':'scalar'}]
        self.assertEqual(m.inspect_context(text, context, raw_locale='fr-FR', protected_ranges=ranges)['status'], 'blocked')
        r = m.inspect_context(text, context, raw_locale='fr-FR', source_sha256=digest, protected_ranges=ranges)
        self.assertEqual(r['status'], 'completed')
        self.assertEqual(len(r['report']['findings']), 1)
        self.assertEqual(r['source_sha256'], digest)
        self.assertEqual(r['report']['findings'][0]['offset'],12)
        self.assertEqual(m.inspect_context(text,context,raw_locale='fr-FR',source_sha256='0'*64,protected_ranges=ranges)['status'],'blocked')

    def test_structured_and_typed_inputs_are_not_claimed(self):
        context = {'language':'fr', 'house_style':'fr-fr-editorial'}
        self.assertEqual(m.inspect_context('<p>Bonjour!</p>',context,raw_locale='fr-FR')['status'],'outside_supported_scope')
        self.assertEqual(m.inspect_context('Bonjour!',context,raw_locale='fr-FR',typed_values=[{'kind':'decimal'}])['status'],'outside_supported_scope')

class ContextShape(unittest.TestCase):
    def test_malformed_ranges_and_extensions_are_blocked(self):
        c = {'language':'fr','house_style':'fr-fr-editorial'}
        for ranges in (42, None, 'bad'):
            self.assertEqual(m.inspect_context('Bonjour!', c, raw_locale='fr-FR', protected_ranges=ranges)['status'],'blocked')
        self.assertEqual(m.inspect_context('Bonjour!',dict(c,extensions=[{'namespace':'bad space','version':'x','critical':False,'payload':{}}]),raw_locale='fr-FR')['status'],'blocked')

    def test_unconnected_norm_edition_is_explicit(self):
        r = m.inspect_context('Bonjour!', {'language':'fr','house_style':'fr-fr-editorial','norm_edition':'future-edition'}, raw_locale='fr-FR')
        self.assertEqual(r['status'],'needs_review')
        self.assertEqual(r['reason'],'norm_edition_not_connected')

class CanonicalEquivalentSource(unittest.TestCase):
    def test_nfc_and_nfd_letter_marks_share_prose_rule_without_normalizing(self):
        import hashlib
        for text in ('Café!', 'Cafe\u0301!', 'Cafe\u0301\u0327!'):
            with self.subTest(text=text):
                raw = text.encode('utf-8')
                report = m.inspect(text, house_style='fr-fr-editorial')
                self.assertEqual(len(report['findings']), 1)
                finding = report['findings'][0]
                self.assertEqual(finding['rule_id'], 'FR-FR-01')
                self.assertEqual(finding['source_range'], {'start':len(text)-1,'end':len(text),'unit':'unicode_code_point'})
                self.assertEqual(report['source_sha256'], hashlib.sha256(raw).hexdigest())
                proposed = m.propose_generated_plain(text, 'fr-fr-editorial')
                self.assertEqual(proposed.encode('utf-8'), raw[:-1] + '\u202f!'.encode('utf-8'))
                self.assertEqual(m.propose_generated_plain(proposed, 'fr-fr-editorial'), proposed)
                self.assertEqual(m.inspect(proposed, house_style='fr-fr-editorial')['findings'], [])
                self.assertEqual(text.encode('utf-8'), raw)

    def test_orphan_combining_mark_does_not_count_as_prose(self):
        for text in ('\u0301!', ' \u0301!', '«\u0301!', '1\u0301!'):
            with self.subTest(text=text):
                self.assertEqual(m.inspect(text, house_style='fr-fr-editorial')['findings'], [])
                self.assertEqual(m.propose_generated_plain(text, 'fr-fr-editorial'), text)

class StructuredGeneratedCopy(unittest.TestCase):
    CASES = (
        '[Offre!](./vente?jour=1)',
        '![Offre!](../image?jour=1)',
        '[Offre!][vente]', '[Offre!][]', '[Offre!]',
        '[vente]: ./vente?jour=1 "Offre!"',
        '<./vente?jour=1>', '<https://example.org/a?b=1>',
        '# Bonjour!', '## Bonjour!', '###### Bonjour!',
        '- Bonjour!', '+ Bonjour!', '* Bonjour!',
        '1. Bonjour!', '2) Bonjour!', '> Bonjour!',
        '~~~python', '*Bonjour!*', '**Bonjour!**', '_Bonjour!_',
    )

    def test_direct_proposal_rejects_markdown_structure_without_changes(self):
        for text in self.CASES:
            with self.subTest(text=text):
                raw = text.encode('utf-8')
                with self.assertRaises(ValueError):
                    m.propose_generated_plain(text, 'fr-fr-editorial')
                self.assertEqual(text.encode('utf-8'), raw)
        self.assertEqual(m.propose_generated_plain('Offre! Bonjour?', 'fr-fr-editorial'), 'Offre\u202f! Bonjour\u202f?')

    def test_context_reports_structure_outside_scope(self):
        for text in self.CASES:
            with self.subTest(text=text):
                result = m.inspect_context(text, {'language':'fr', 'house_style':'fr-fr-editorial'}, raw_locale='fr-FR')
                self.assertEqual(result['status'], 'outside_supported_scope')
                self.assertEqual(result['reason'], 'structured_input_not_parsed')
                self.assertIsNone(result['report'])

    def test_cli_rejects_relative_markdown_destination_and_keeps_source(self):
        import subprocess
        import sys
        import tempfile
        raw = '[Offre!](./vente?jour=1)'.encode('utf-8')
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / 'source.md'
            source.write_bytes(raw)
            result = subprocess.run([sys.executable, str(PATH), str(source), '--propose', '--source-origin', 'generated', '--house-style', 'fr-fr-editorial'], capture_output=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, b'')
            self.assertEqual(source.read_bytes(), raw)

if __name__ == '__main__': unittest.main()
