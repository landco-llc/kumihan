import importlib.util, json, unittest, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'plugins/kumihan-fa'
def load(file,name):
    spec=importlib.util.spec_from_file_location(name,file)
    obj=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj
class PersianTests(unittest.TestCase):
    def test_research_alignment(self):
        a=json.loads((BASE/'rules/catalog.json').read_text())
        b=json.loads((BASE/'fixtures/acceptance.json').read_text())
        self.assertEqual(len(a['rules']),32)
        self.assertEqual(len({r['id'] for r in a['rules']}),32)
        self.assertEqual(len(b['fixtures']),24)
        self.assertTrue(all(f['status']=='not-run' for f in b['fixtures']))
    def test_byte_identity_and_half_space(self):
        m=load(BASE/'runtime/check_source.py','fa1')
        source='می‌روم ک ی هٔ ۱۲۳'.encode()
        self.assertEqual(m.compare(source,source)['status'],'passed')
        self.assertEqual(m.compare(source,source.replace('\u200c'.encode(),b' '))['status'],'failed')
        self.assertEqual(m.compare('أ'.encode(),'أ'.encode())['status'],'failed')
    def test_fa_html_and_candidates(self):
        m=load(BASE/'runtime/check_source.py','fa2')
        good='<html lang="fa-IR" dir="rtl"><p>می‌روم ک ی <bdi dir="ltr">v0.1.0</bdi></p></html>'
        r=m.check_html(good)
        self.assertEqual(r['persian_specialized'],'available')
        self.assertEqual(r['rendered'],'not-checked')
        self.assertFalse(any(x['status']=='failed' for x in r['checks']))
        source='<html lang="fa" dir="rtl"><p>ك ي https://example.invalid</p></html>'
        v=m.check_html(source)
        self.assertTrue(any(x['rule_id']=='FA-ENC-02' for x in v['checks']))
        self.assertTrue(any(x['rule_id']=='FA-BIDI-03' for x in v['checks']))
    def test_lang_and_direction(self):
        m=load(BASE/'runtime/check_source.py','fa3')
        self.assertTrue(any(x['status']=='failed' for x in m.check_html('<html lang="fa" dir="ltr"><p>متن</p></html>')['checks']))
        self.assertEqual(m.check_html('<html lang="ar" dir="rtl">نص</html>')['persian_specialized'],'unsupported')
    def test_reproducible_archives(self):
        m=load(ROOT/'tools/build_fa.py','fa4')
        p=m.plan_outputs()
        manifest=json.loads(p['plugins/kumihan-fa/downloads/MANIFEST.json'])
        self.assertEqual(len(manifest['archives']),15)
        self.assertEqual(manifest['product'],'KUMIHAN｜تراز')
        self.assertTrue(all('v0.1.0' in a['file'] for a in manifest['archives']))
        self.assertTrue(all(a['source_path'] in p for a in manifest['archives']))
        self.assertEqual(json.loads((BASE/'plugin.json').read_text())['extensions']['com.openai']['interface']['displayName'],'KUMIHAN｜تراز')
        with zipfile.ZipFile(BASE/'downloads/kumihan-fa-Claude-Code-plugin-v0.1.0.zip') as z:
            self.assertIn('kumihan-fa/.claude-plugin/plugin.json',z.namelist())
            self.assertIn('kumihan-fa/skills/kumihan-fa/SKILL.md',z.namelist())
            self.assertIn('kumihan-fa/assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png',z.namelist())
if __name__=="__main__":
    unittest.main()
