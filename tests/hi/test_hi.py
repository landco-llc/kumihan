import unittest, importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
class Integrity(unittest.TestCase):
 def test_rejects_text_damaging_transformations(self):
  p=ROOT/'plugins/kumihan-hi/runtime/checks.py'
  spec=importlib.util.spec_from_file_location('hi_damage',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  for before,after in [('क्\u200dष','क्ष'),('क्\u200cष','क्ष'),('ज़','ज'),('हँस','हंस'),('निःशुल्क','नि:शुल्क'),('नमस्ते।','नमस्ते|'),('OTP 012345','OTP ०१२३४५'),('₹1,23,456.78','₹123,456.78')]:
   self.assertEqual(m.compare(before.encode(),after.encode())['status'],'failed')
 def test_runtime_exists(self):
  self.assertTrue((ROOT/'plugins/kumihan-hi/runtime/checks.py').is_file(), 'Hindi read-only core missing')
 def test_preserves_distinct_nfc_sources(self):
  p=ROOT/'plugins/kumihan-hi/runtime/checks.py'
  if not p.exists(): self.fail('Hindi read-only core missing')
  s=importlib.util.spec_from_file_location('hi_checks',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
  a='क़'.encode();b='क़'.encode();r=m.compare(a,b)
  self.assertFalse(r['bytes_equal']);self.assertTrue(r['derived_nfc_equal']);self.assertEqual(r['status'],'failed')
  for text in ['क्\u200dष','क्\u200cष','हिंदी / हिन्दी','निःशुल्क / समय: 10:30','OTP 012345 v0.1.0']:
   raw=text.encode();self.assertEqual(m.compare(raw,raw)['status'],'passed');self.assertEqual(raw,text.encode())

import json, hashlib, tempfile, sys
from zipfile import ZipFile
sys.path.insert(0,str(ROOT/'tools'))
import build_hi
class Packages(unittest.TestCase):
 def test_all_fifteen_safe_reproducible_self_contained(self):
  with tempfile.TemporaryDirectory() as a,tempfile.TemporaryDirectory() as b:
   a=Path(a);b=Path(b);self.assertEqual(build_hi.build(a),15);build_hi.build(b)
   manifest=json.loads((a/'MANIFEST.json').read_text());self.assertEqual(len(manifest['packages']),15)
   for item in manifest['packages']:
    p=a/item['name'];self.assertEqual(p.read_bytes(),(b/p.name).read_bytes());self.assertEqual(item['size'],p.stat().st_size);self.assertEqual(item['sha256'],hashlib.sha256(p.read_bytes()).hexdigest())
    with ZipFile(p) as z:
     names=z.namelist();self.assertTrue(any(n.endswith('.png') for n in names))
     for n in names:
      self.assertFalse(n.startswith('/'));self.assertNotIn('..',Path(n).parts);self.assertNotEqual(z.getinfo(n).external_attr>>16 & 0o170000,0o120000)
     skills=[n for n in names if n.endswith('/SKILL.md')];self.assertEqual(len(skills),1 if '-skill-' in p.name else 4)
     for sk in skills:
      prefix=sk.removesuffix('SKILL.md')
      for f in ['sources.json','rules/catalog.json','fixtures/qa.json','references/workflow.md','references/web.md','references/documents.md','references/review.md','profiles/profiles.json','locales/hi-IN.json','runtime/checks.py','assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png']:
       self.assertIn(prefix+f,names)
 def test_contract_and_bilingual_identity(self):
  p=ROOT/'plugins/kumihan-hi';rules=json.loads((p/'rules/catalog.json').read_text());sources=json.loads((p/'sources.json').read_text())
  self.assertEqual({r['id'] for r in rules},{f'HI-{t}{i:02}' for t,n in [('T',14),('C',6),('D',4)] for i in range(1,n+1)})
  self.assertEqual({x['id'] for x in json.loads((p/'fixtures/qa.json').read_text())},{f'Q{i:02}' for i in range(1,25)})
  for r in rules:
   for field in ['application_condition','kind','source_refs','exception','recommended_action','qa_ids','implementation_status','evidence_status']:self.assertTrue(r[field])
   for ref in r['source_refs']:self.assertIn(ref,sources)
  for path in [p/'plugin.json',p/'.codex-plugin/plugin.json',p/'.claude-plugin/plugin.json',p/'gemini-extension.json']:
   d=json.loads(path.read_text());self.assertRegex(d['description'],r'[\u0900-\u097f]');self.assertRegex(d['description'],r'[A-Za-z]');self.assertNotRegex(d['description'],r'[\u3040-\u30ff]');self.assertEqual(d['name'],'kumihan-hi')
  d=json.loads((p/'plugin.json').read_text());self.assertEqual(d['extensions']['com.openai']['interface']['displayName'],'KUMIHAN｜अक्षर-संगति')

import build_hi_site, base_copy
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set()
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.add(a['id'])
  for k in ('href','src'):
   if a.get(k):self.links.append(a[k])
class Site(unittest.TestCase):
 def test_generated_pages_and_links(self):
  outputs=build_hi_site.outputs();self.assertEqual(len(outputs),13)
  for name,text in outputs.items():
   self.assertEqual((ROOT/name).read_text(),text,name)
   if not name.endswith('.html'):continue
   self.assertIn('hreflang="hi"',text);self.assertIn('hreflang="x-default"',text);self.assertIn('rel="canonical"',text)
   self.assertIn('KUMIHAN',text);self.assertNotIn('dir="rtl"',text)
   p=Links();p.feed(text)
   for link in p.links:
    u=urlparse(link)
    if u.scheme:continue
    target=(ROOT/name).parent/unquote(u.path) if u.path else ROOT/name
    self.assertTrue(target.is_file(),f'{name}: {link}')
    if u.fragment:
     other=Links();other.feed(target.read_text());self.assertIn(u.fragment,other.ids,f'{name}: {link}')
 def test_master_copy_parity(self):
  data=json.loads((ROOT/'assets/hi-site-copy.json').read_text())
  for lang in ['ja','en']:self.assertEqual(base_copy.apply(data[lang],lang,'hi'),data[lang])
  for lang,c in data.items():
   self.assertNotIn('pt-PT',json.dumps(c));self.assertNotIn('Portuguese',json.dumps(c));self.assertNotIn('Compasso',json.dumps(c))
 def test_download_filenames_and_gateway(self):
  with tempfile.TemporaryDirectory() as tmp:
   build_hi.build(Path(tmp));names={p.name for p in Path(tmp).iterdir()}
   for host in build_hi.HOSTS:
    for lang in ['hi','en','ja']:
     p=Links();p.feed(build_hi_site.guide(host,lang,json.loads((ROOT/'assets/hi-site-copy.json').read_text())[lang]))
     for link in p.links:
      if '/releases/download/' in link:self.assertIn(link.rsplit('/',1)[-1],names)
  for page in ['index.html','top-en.html']:
   p=(ROOT/page).read_text();self.assertIn('kumihan-hi',p);self.assertIn('target="_blank"',p)
