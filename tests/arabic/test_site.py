"""Acceptance tests for generated Arabic product pages and acquisition paths."""
import importlib.util
import posixpath
import re
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
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
class Tags(HTMLParser):
    def __init__(self,text):
        super().__init__();self.tags=[];self.feed(text)
    def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))
class Site(unittest.TestCase):
    def test_twelve_pages_language_navigation_and_real_host_assets(self):
        spec=importlib.util.spec_from_file_location('ar_site',ROOT/'tools/build_ar_site.py')
        self.assertTrue(spec and spec.loader and Path(spec.origin).exists(),'Arabic site generator is missing')
        m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        landings={n:b for n,b in m.outputs().items() if n.endswith('.html')};self.assertEqual(len(landings),3)
        G,guides=install_guides('ar');out={**landings,**guides};self.assertEqual(len(out),12)
        self.assertEqual((ROOT/'assets/kumihan-ar.css').read_text(),m.outputs()['assets/kumihan-ar.css'])
        sections=['hero','intro-strip','features','idea-band','skills-section','install-section','status-section','cta-section']
        for name,body in out.items():
            with self.subTest(page=name):
                self.assertEqual((ROOT/name).read_text(),body)
                t=Tags(body);html=next(a for tag,a in t.tags if tag=='html')
                # Landings state dir explicitly; English/Japanese guides inherit ltr.
                self.assertEqual(html.get('dir','ltr') if name.startswith('docs/') else html['dir'],'rtl' if html['lang']=='ar' else 'ltr')
                self.assertEqual({a['hreflang'] for tag,a in t.tags if tag=='link' and a.get('rel')=='alternate'},{'ar','en','ja','x-default'})
                # Landings use the canonical index CSS; install guides the canonical guide CSS.
                css='kumihan-install.css' if name.startswith('docs/') else 'kumihan-ar.css'
                self.assertTrue(any(css in a.get('href','') for tag,a in t.tags))
                if not name.startswith('docs/'):
                    classes=[a.get('class','').split()[0] for tag,a in t.tags if tag=='section']
                    self.assertEqual(classes,sections)
                else:
                    check_guide(self,G,'ar','ar',name,body,'KUMIHAN｜نضيد')
                    for link in re.findall(r'<a href="([^"]+\.zip)"',body):
                        self.assertIn('/releases/download/kumihan-ar-v0.1.0/',link)
                for tag,a in t.tags:
                    link=a.get('href','')
                    if link.startswith('/kumihan/') and not link.endswith('/'):
                        path=link.removeprefix('/kumihan/').split('#')[0].split('?')[0]
                        if path:self.assertTrue((ROOT/path).is_file(),link)
