import importlib.util
from pathlib import Path
import hashlib
import unittest

ROOT=Path(__file__).resolve().parents[2]
class RuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=ROOT/'plugins/kumihan-grafia/runtime/checks.py'
        if p.exists():
            spec=importlib.util.spec_from_file_location('grafia_checks',p)
            cls.api=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.api)
        else: cls.api=None
    def review(self,*args,**kwargs):
        self.assertIsNotNone(self.api,'Grafía read-only helper must exist')
        return self.api.review(*args,**kwargs)
    def test_exact_bytes_not_canonical_equivalence(self):
        a='ñ ü ¿¡ 1.º 15\u00a0% 12\u202f345 «Té» KUMIHAN｜Grafía'.encode()
        b=a.replace('ñ'.encode(),'n\u0303'.encode())
        r=self.review(a,candidate=b)
        self.assertEqual(r['preservation']['status'],'failed')
        self.assertEqual(r['original_hash'],hashlib.sha256(a).hexdigest())
    def test_unknown_locale_rejected(self):
        for loc in ['fr','es-US','es-XX','es_ES','']:
            with self.subTest(loc=loc):
                self.assertIsNotNone(self.api,'Grafía helper must exist')
                with self.assertRaises(ValueError): self.api.review(b'original',locale=loc)
    def test_no_country_or_currency_defaults(self):
        for loc in ['es','es-ES','es-MX','es-AR','es-CO','es-CL','es-PE','es-419']:
            r=self.review('Vos tenés té. Tú tienes té. $100'.encode(),locale=loc)
            self.assertIsNone(r['context']['currency'])
            self.assertEqual(r['context']['pronoun'],'inherit')
            self.assertIsNone(r['context']['timeZone'])
            self.assertEqual(r['preservation']['status'],'passed')
    def test_editorial_candidates_are_not_blockers(self):
        r=self.review('¿Vienes?. « Té » 35% — Hola solo sólo este éste 2458 2 458'.encode())
        self.assertTrue(r['findings'])
        self.assertTrue(all(f['status']=='needs-review' for f in r['findings']))
        self.assertTrue(all(not f['edits_authorized'] for f in r['findings']))
    def test_titles_and_grouping_not_mechanically_rejected(self):
        r=self.review('Vienes mañana?\n2458 / 2 458 / sólo / éste'.encode())
        self.assertFalse(r['findings'])
    def test_invalid_utf8_explicit_error(self):
        self.assertIsNotNone(self.api,'Grafía helper must exist')
        with self.assertRaises(UnicodeDecodeError): self.api.review(b'\xff')
