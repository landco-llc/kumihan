import importlib.util
from pathlib import Path
import unittest
from html.parser import HTMLParser
import re
import sys
from urllib.parse import urlsplit
import posixpath
ROOT=Path(__file__).resolve().parents[2]
# Installation guides come from tools/build_install_guides.py (one generator for every edition).
HOST_MARK={'chatgpt':'GPT-Codex','claude':'Claude','gemini':'Gemini'}
def install_guides(code):
 """(generator, {path: html}) for the edition's nine guides (3 hosts x native/en/ja)."""
 sys.path.insert(0,str(ROOT/'tools'))
 import build_install_guides as G
 out=G.outputs()
 return G,{G.guide_path(code,h,l):out[G.guide_path(code,h,l)] for h in G.HOSTS for l in (code,'en','ja')}
def check_guide(t,G,code,native,path,text,brand):
 """Release downloads, language attributes/switch/alternates and brand of one guide."""
 import edition_versions as V
 facts=V.load()['editions'][code];slug=V.catalogue()[code]['product']
 host,lang=next((h,l) for h in G.HOSTS for l in (code,'en','ja') if G.guide_path(code,h,l)==path)
 t.assertEqual((ROOT/path).read_text(encoding='utf-8'),text,path+' is stale')
 attr=native if lang==code else lang
 t.assertIn(f'<html lang="{attr}"'+(' dir="rtl"' if lang==code and code in G.RTL else '')+'>',text)
 t.assertIn(brand,text);t.assertIn('<main',text)
 alts=dict(re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)">',text))
 expected={(native if k==code else k):G.BASE+G.guide_path(code,host,k) for k in (code,'en','ja')}
 t.assertEqual(alts,dict(expected,**{'x-default':G.BASE+G.guide_path(code,host,code)}))
 switch=re.findall(r'<a href="([^"]+)" lang="([^"]+)" hreflang="[^"]+" data-language( aria-current="page")?>',text)
 t.assertEqual([(h,l) for h,l,_ in switch],[(G.guide_path(code,host,k).removeprefix('docs/'),native if k==code else k) for k in (code,'en','ja')])
 t.assertEqual([h for h,_,c in switch if c],[G.guide_path(code,host,lang).removeprefix('docs/')])
 # Downloads: exactly the edition's verified Release assets for this host + SHA256SUMS.
 t.assertEqual(facts['release_status'],'published')
 verified={a['url'] for a in facts['verified_assets']}
 zips=re.findall(r'<a href="([^"]+\.zip)"',text);names=[z.rsplit('/',1)[1] for z in zips]
 t.assertEqual(len(zips),5,path);t.assertEqual(len(set(zips)),5,path);t.assertLessEqual(set(zips),verified,path)
 t.assertTrue(all(z.startswith(f"{facts['release_url'].replace('/tag/','/download/')}/") for z in zips),path)
 plugins=[n for n in names if re.search(r'plugin|extension',n)];t.assertEqual(len(plugins),1,path)
 t.assertIn(HOST_MARK[host],plugins[0])
 for n in names:
  t.assertTrue((ROOT/'plugins'/slug/'downloads'/n).is_file(),n)
  for other,mark in HOST_MARK.items():
   if other!=host:t.assertNotIn(mark,n,(path,n))
 sums=next(m['url'] for m in facts['verified_metadata'] if m['name']=='SHA256SUMS.txt')
 t.assertIn(f'<a href="{sums}">SHA256SUMS.txt</a>',text)
 for v in re.findall(r'(?:href|src)="([^"]+)"',text):
  if urlsplit(v).scheme or v.startswith(('#','/')):continue
  target=posixpath.normpath(posixpath.join(posixpath.dirname(path),urlsplit(v).path))
  t.assertTrue((ROOT/target).is_file(),(path,v))
class SiteTests(unittest.TestCase):
 def test_twelve_pages_languages_downloads_and_alternates(self):
  path=ROOT/'tools/build_grafia_site.py';self.assertTrue(path.exists(),'Grafía site generator must exist')
  spec=importlib.util.spec_from_file_location('grafia_site',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  landings=m.outputs();self.assertEqual(len(landings),3)
  G,guides=install_guides('es');outputs={**landings,**guides};self.assertEqual(len(outputs),12)
  for path,text in outputs.items():
   locale='ja' if '.ja.' in path else 'en' if '.en.' in path else 'es'
   self.assertIn(f'<html lang="{locale}">',text)
   for language in ('es','en','ja'):self.assertIn(f'hreflang="{language}"',text)
   self.assertNotIn('hreflang="es-419"',text)
   self.assertIn('KUMIHAN｜Grafía',text);self.assertIn('<main',text)
   class Links(HTMLParser):
    def handle_starttag(self,tag,attrs):
     d=dict(attrs)
     for key in ('href','src'):
      value=d.get(key,'')
      if value.startswith('/kumihan/'):
       target=value[len('/kumihan/'):].split('#')[0]
       if target:self_test.assertTrue(target in outputs or (ROOT/target).is_file(),(path,target))
   self_test=self;Links().feed(text)
   if path.startswith('docs/'):
    check_guide(self,G,'es','es',path,text,'KUMIHAN<span class="brand-sub">｜Grafía</span>')
