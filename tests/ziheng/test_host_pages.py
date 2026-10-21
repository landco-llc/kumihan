"""Bounded host documentation checks; no native-host behavioral claim."""
import hashlib
import json
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]
PRODUCT = ROOT/'plugins/kumihan-ziheng'
HOSTS=('claude','gemini')
LANGS={'':'zh-Hant-TW','.en':'en','.ja':'ja'}

class Tags(HTMLParser):
    def __init__(self):
        super().__init__()
        self.all=[]
    def handle_starttag(self,tag,attrs):
        self.all.append((tag,dict(attrs)))

class HostDocsTests(unittest.TestCase):
    def test_host_page_localization_and_links(self):
        for host in HOSTS:
            for suffix,tag in LANGS.items():
                path=ROOT/f'docs/install-ziheng-{host}{suffix}.html'
                with self.subTest(page=path.name):
                    s=path.read_text(encoding='utf-8')
                    parsed=Tags();parsed.feed(s)
                    self.assertEqual([attrs.get('lang') for name,attrs in parsed.all if name=='html'],[tag])
                    self.assertEqual(sum(n=='h1' for n,_ in parsed.all),1)
                    self.assertIn('KUMIHAN｜字衡',s)
                    self.assertIn('KUMIHAN<span class="brand-rule">｜</span>字衡',s)  # landing brand
                    # Language switch: native / English / 日本語, current page marked.
                    switch=[d for n,d in parsed.all if n=='a' and 'data-language' in d]
                    self.assertEqual([(d['lang'],d['href']) for d in switch],
                                     [(t,f'install-ziheng-{host}{x}.html') for x,t in LANGS.items()])
                    self.assertEqual([d['lang'] for d in switch if d.get('aria-current')=='page'],[tag])
                    self.assertIn('kumihan-ziheng-'+host+'-plugin-0.2.0.zip',s)
                    self.assertIn('kumihan-install.css',s)  # canonical KUMIHAN install-guide layout
                    self.assertTrue(any(n=='link' and d.get('rel')=='canonical' and path.name in d.get('href','') for n,d in parsed.all))
                    alts={d['hreflang']:d['href'] for n,d in parsed.all if n=='link' and d.get('rel')=='alternate'}
                    self.assertEqual(set(alts), {'zh-Hant-TW','en','ja','x-default'})
                    self.assertTrue(alts['x-default'].endswith(f'docs/install-ziheng-{host}.html'))
                    for n,attr in parsed.all:
                        for key in ('href','src'):
                            v=attr.get(key)
                            if not v or v.startswith(('http://','https://','#','mailto:','data:')):
                                continue
                            ref=unquote(urlsplit(v).path)
                            target=(path.parent/ref).resolve()
                            if ref.endswith('/favicon-32x32.png'):
                                continue  # Root asset verified by GitHub's existing website CI.
                            self.assertTrue(target.is_relative_to(ROOT) and target.exists(),(path,v))
                    links=[d.get('href') for n,d in parsed.all if n=='a']
                    self.assertTrue(any('install-ziheng' in p for p in links if p))

    def test_existing_zi_heng_portal_and_top_links(self):
        for suffix in LANGS:
            for page in [ROOT/f'docs/install-ziheng{suffix}.html',ROOT/f'kumihan-zh-han{suffix}.html']:
                with self.subTest(page=page.name):
                    s=page.read_text(encoding='utf-8')
                    self.assertIn(f'install-ziheng-claude{suffix}.html',s)
                    self.assertIn(f'install-ziheng-gemini{suffix}.html',s)
                    self.assertNotIn('Claude/Gemini専用配布物はありません。',s)
                    self.assertNotIn('Claude／Gemini 專屬套件尚未提供。',s)

    def test_host_markdown_zip_checksum_and_instruction_separation(self):
        mapping={"":'zh-hant','.en':'en','.ja':'ja'}
        facts=json.loads((ROOT/'assets/edition-versions.json').read_text(encoding='utf-8'))['editions']['zh-hant']
        sums=next(m['url'] for m in facts['verified_metadata'] if m['name']=='SHA256SUMS.txt')
        for host in HOSTS:
            folder=f'downloads {host.title()}'
            dist=json.loads((PRODUCT/folder/'MANIFEST.json').read_text())
            bundle=next(x for x in dist['archives'] if x['file'].startswith('plugins/' if host=='claude' else 'extensions/'))
            # Each packaged archive is published as exactly one verified Release asset of this host
            # with the same SHA-256; the guide must link exactly those assets plus SHA256SUMS.txt.
            expected=set()
            for archive in dist['archives']:
                match=[a for a in facts['verified_assets'] if a['sha256']==archive['sha256'] and f'-{host}-' in a['name']]
                self.assertEqual(len(match),1,(host,archive['file']))
                expected.add(match[0]['url'])
            plugin=next(a for a in facts['verified_assets'] if a['sha256']==bundle['sha256'] and f'-{host}-' in a['name'])
            self.assertEqual(plugin['name'],f'kumihan-ziheng-{host}-plugin-0.2.0.zip')
            for suffix,locale in mapping.items():
                with self.subTest(host=host,lang=locale):
                    page=(ROOT/f'docs/install-ziheng-{host}{suffix}.html').read_text(encoding='utf-8')
                    parsed=Tags();parsed.feed(page)
                    guide=(PRODUCT/f'docs/installation-{host}.{locale}.md').read_text(encoding='utf-8')
                    downloads={d['href'] for n,d in parsed.all if n=='a' and '/releases/download/' in d.get('href','')}
                    self.assertEqual(downloads,expected|{sums})
                    self.assertIn(f'href="{plugin["url"]}"',page)
                    self.assertIn(bundle['sha256'],guide)
                    self.assertIn('0.2.0',page)
                    self.assertIn('0.1.0',guide)
                    for skill in ('kumihan-ziheng','kumihan-ziheng-web','kumihan-ziheng-documents','kumihan-ziheng-review'):
                        self.assertIn(skill,guide)
                        self.assertIn(skill,page)
                    if host=='gemini':
                        self.assertNotIn('gemini extensions install https://github.com/landco-llc/kumihan',guide)
                    else:
                        self.assertIn('kumihan-ziheng@kumihan-marketplace',guide)

if __name__=='__main__':unittest.main()
