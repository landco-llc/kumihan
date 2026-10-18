import importlib.util
import unittest
from pathlib import Path
P=Path(__file__).resolve().parents[2]/'plugins/kumihan-ar/runtime/check_source.py'
def runtime():
 s=importlib.util.spec_from_file_location('arabic_checker',P); m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
class SourceTests(unittest.TestCase):
 def test_exact_bytes_metadata_and_protected_unicode(self):
  m=runtime();raw='بِسْمِ ـ العربية\u200d\u200c\u2067 ١٢٣ 123'.encode();self.assertEqual(m.compare(raw,raw,{'id':'a'},{'id':'a'})['status'],'passed')
  self.assertEqual(m.compare(raw,raw+b' ',{'id':'a'},{'id':'a'})['status'],'failed')
  self.assertEqual(m.compare(raw,raw,{'id':'a'},{'id':'b'})['status'],'failed')
 def test_normalization_is_only_derived(self):
  m=runtime();raw='ا\u0654'.encode();r=m.compare(raw,'أ'.encode());self.assertEqual(r['status'],'failed');self.assertEqual(r['derived_nfc_equal'],True)
 def test_html_positive_negative_and_no_render_claim(self):
  m=runtime();good='<html lang="ar" dir="rtl"><p>نص <bdi dir="ltr">https://example.org</bdi></p></html>'
  r=m.check_html(good);self.assertFalse(any(x['status']=='failed' for x in r['checks']));self.assertEqual(r['rendered'],'not-checked')
  bad=m.check_html('<html lang="ar" dir="ltr"><p style="letter-spacing:2px;white-space:nowrap">نص https://a.org</p></html>')
  self.assertTrue(any(x['rule_id']=='AR-BIDI-01' and x['status']=='failed' for x in bad['checks']))
  self.assertTrue(any(x['status']=='needs-review' for x in bad['checks']))
 def test_language_exclusions_and_locale_unknown(self):
  m=runtime()
  for lang in ('fa','ur'):
   r=m.check_html(f'<html lang="{lang}" dir="rtl"><p>نص</p></html>');self.assertEqual(r['arabic_specialized'],'unsupported')
  self.assertEqual(m.check_html('<p>نص</p>')['arabic_specialized'],'not-checked')
 def test_locale_digits_are_never_converted(self):
  m=runtime()
  for locale in ('ar-SA','ar-AE','ar-EG','ar-MA'):
   src=f'<html lang="{locale}" dir="rtl"><input value="١٢٣ 123"></html>'; r=m.check_html(src);self.assertEqual(r['source_sha256'],m.sha(src.encode()));self.assertEqual(r['locale'],locale)
 def test_bounded_input(self):
  with self.assertRaises(ValueError):runtime().check_html('x'*1048577)

class CandidateControls(unittest.TestCase):
 def test_control_tatweel_tracking_and_wrapping_are_candidates(self):
  src='<html lang="ar" dir="rtl"><p style="letter-spacing:.1em;word-break:break-all;overflow:hidden">نـص\u2067</p></html>'
  report=runtime().check_html(src)
  for rule in ('AR-BIDI-05','AR-TYPE-01','AR-TYPE-03','AR-TYPE-05'):
   self.assertTrue(any(c['rule_id']==rule and c['status']=='needs-review' for c in report['checks']))
  self.assertEqual(runtime().sha(src.encode()),report['source_sha256'])
 def test_intentional_nonjoining_label_is_not_failed(self):
  report=runtime().check_html('<html lang="ar" dir="rtl"><code style="white-space:nowrap">ABC-123</code></html>')
  self.assertFalse(any(c['status']=='failed' for c in report['checks']))
 def test_explicit_fa_does_not_get_arabic_tracking_checks(self):
  report=runtime().check_html('<html lang="fa" dir="rtl"><p style="letter-spacing:2px">نص</p></html>')
  self.assertFalse(any(c['rule_id']=='AR-TYPE-01' for c in report['checks']))
 def test_original_number_proposal_has_real_input(self):
  self.assertEqual(runtime().compare('السعر 123'.encode(),'السعر ١٢٣'.encode())['status'],'failed')
 def test_nfkc_proposal_has_real_input(self):
  self.assertEqual(runtime().compare('ﻻ'.encode(),'لا'.encode())['status'],'failed')

 def test_mixed_url_local_isolation_negative_and_exception(self):
  m=runtime()
  unsafe=m.check_html('<html lang="ar" dir="rtl"><p>نص https://example.org</p></html>')
  self.assertTrue(any(c['rule_id']=='AR-BIDI-02' and c['status']=='needs-review' for c in unsafe['checks']))
  safe=m.check_html('<html lang="ar" dir="rtl"><p>نص <bdi dir="ltr">https://example.org</bdi></p></html>')
  self.assertFalse(any(c['rule_id']=='AR-BIDI-02' for c in safe['checks']))
 def test_report_items_have_evidence_contract(self):
  m=runtime();required={'rule_id','status','scope','evidence','host','remediation','dependencies','notes'}
  for item in m.check_html('<html lang="ar" dir="rtl"><p>نص</p></html>')['checks']+[m.compare(b'a',b'a')]:
   self.assertFalse(required-set(item));self.assertIn(item['status'],m.STATUSES)
