"""Static checks for Bengali site and the 9 installation guides."""
import json, posixpath, re, sys, unittest
from urllib.parse import urlsplit
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
BRAND="KUMIHAN｜অক্ষরসজ্জা"
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
class SiteContract(unittest.TestCase):
 def test_main_pages(self):
  for code in ("bn","en","ja"):
   name="kumihan-bn"+("" if code=="bn" else "."+code)+".html"
   s=(ROOT/name).read_text("utf-8")
   self.assertIn(f'<html lang="{code}"',s)
   self.assertIn(BRAND,s)
   self.assertIn('assets/bn-site-overrides.css',s)
   self.assertIn('href="#install"',s)
   self.assertIn('rel="canonical"',s)
   self.assertIn('href="https://landco.co.jp/"',s)
   self.assertNotIn("Satzbild",s)
   self.assertNotIn("अक्षर-संगति",s)
 def test_all_guides(self):
  G,guides=install_guides("bn");self.assertEqual(len(guides),9)
  for path,s in guides.items():
   with self.subTest(page=path):
    self.assertIn(BRAND,s)
    check_guide(self,G,"bn","bn",path,s,'KUMIHAN<span class="brand-sub">｜অক্ষরসজ্জা</span>')
    # Sections of the unified guide: 1. choose method, 2. download, host sections A/B.
    for anchor in ('id="step-1"','id="step-2"','id="a"','id="b"'): self.assertIn(anchor,s)
 def test_archive_links(self):
  d=ROOT/"plugins/kumihan-bn/downloads"
  for page in ROOT.glob("kumihan-bn*.html"):
   s=page.read_text("utf-8")
   self.assertIn("docs/install-kumihan-bn-",s)
  for p in (ROOT/"docs").glob("install-kumihan-bn-*.html"):
   s=p.read_text("utf-8")
   fns=re.findall(r"downloads?/(?:kumihan-bn-v0\.1\.0/)?([\w.-]+\.zip)",s)
   self.assertEqual(len(fns),5,p.name)
   for fn in fns:
    self.assertTrue((d/fn).is_file(),f"{p.name} -> {fn}")
if __name__=="__main__": unittest.main()
