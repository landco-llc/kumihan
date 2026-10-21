"""Bounded static contract for the ZiHeng public website (stdlib only).

This does not claim a Jekyll deploy or a browser-rendering acceptance test.
"""
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import unittest

ROOT = Path(__file__).resolve().parents[2]
CASE = {
    'kumihan-zh-han.html': 'zh-Hant-TW',
    'kumihan-zh-han.en.html': 'en',
    'kumihan-zh-han.ja.html': 'ja',
    'docs/install-ziheng.html': 'zh-Hant-TW',
    'docs/install-ziheng.en.html': 'en',
    'docs/install-ziheng.ja.html': 'ja',
}


class PageTags(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = []

    def handle_starttag(self, name, attrs):
        self.tags.append((name, dict(attrs)))


class ZiHengWebsiteTests(unittest.TestCase):
    def test_language_pages_headings_and_site_identity(self):
        for path, language in CASE.items():
            with self.subTest(path=path):
                content = (ROOT/path).read_text(encoding='utf-8')
                parsed = PageTags()
                parsed.feed(content)
                self.assertIn('KUMIHAN｜字衡', content)
                self.assertEqual([attr.get('lang') for tag,attr in parsed.tags if tag=='html'], [language])
                self.assertEqual(sum(tag=='h1' for tag,_ in parsed.tags), 1)
                self.assertTrue(any(tag=='link' and attr.get('rel')=='canonical' and path in attr.get('href','') for tag,attr in parsed.tags))
                alts=[attr for tag,attr in parsed.tags if tag=='link' and attr.get('rel')=='alternate']
                self.assertEqual({a.get('hreflang') for a in alts},{'ja','en','zh-Hant-TW','x-default'})
                self.assertNotIn('lang="zh-han"',content)
                self.assertNotIn('kumihan-zh-ch.html',content)
                if path.startswith('docs/'):
                    # Install guide (tools/build_install_guides.py): shared frame language switch.
                    self.assertEqual(len([1 for tag,attr in parsed.tags if tag=='nav' and 'language-switch' in attr.get('class','')]),1)
                    switch=[attr for tag,attr in parsed.tags if tag=='a' and 'data-language' in attr]
                    self.assertEqual([a['lang'] for a in switch],['zh-Hant-TW','en','ja'])
                    self.assertEqual([a['lang'] for a in switch if a.get('aria-current')=='page'],[language])
                    continue
                self.assertTrue(any(tag=='meta' and attr.get('name')=='kumihan-product-route' and attr.get('content')=='zh-han' for tag,attr in parsed.tags))
                self.assertEqual(len([1 for tag,attr in parsed.tags if tag=='nav' and 'lang-picker' in attr.get('class','')]),1)

    def test_internal_links_and_images_exist(self):
        for path in CASE:
            with self.subTest(path=path):
                base = ROOT / path
                parsed = PageTags()
                parsed.feed(base.read_text(encoding='utf-8'))
                for tag, attr in parsed.tags:
                    for key in ('href','src'):
                        value=attr.get(key)
                        if not value or value.startswith(('#','http://','https://','data:','mailto:')):
                            continue
                        ref=unquote(urlsplit(value).path)
                        target=(base.parent/ref).resolve()
                        self.assertTrue(target.is_relative_to(ROOT), (path,key,value))
                        self.assertTrue(target.is_file(), (path,key,value))

    def test_installation_claims_versioned_zip_and_unversioned_display(self):
        zipfilename='kumihan-ziheng-openai-codex-plugin-0.2.0.zip'
        for path in CASE:
            content=(ROOT/path).read_text(encoding='utf-8')
            self.assertIn(zipfilename, content, path)
            self.assertIn('zh-Hant-TW',content)
            if not path.startswith('docs/'):
                self.assertIn('zh-Hant-HK',content)
        facts=json.loads((ROOT/'assets/edition-versions.json').read_text())['editions']['zh-hant']
        sums=next(m['url'] for m in facts['verified_metadata'] if m['name']=='SHA256SUMS.txt')
        codex={a['url'] for a in facts['verified_assets'] if '-openai-codex-' in a['name']}
        plugin=next(a for a in facts['verified_assets'] if a['name']==zipfilename)
        self.assertIn(plugin['url'],codex)
        self.assertEqual(len(codex),5)  # plugin ZIP + four skill ZIPs
        for path in ('docs/install-ziheng.html','docs/install-ziheng.en.html','docs/install-ziheng.ja.html'):
            with self.subTest(path=path):
                content=(ROOT/path).read_text(encoding='utf-8')
                parsed=PageTags();parsed.feed(content)
                # Downloads are exactly the verified ChatGPT/Codex Release assets + SHA256SUMS.txt.
                downloads={attr['href'] for tag,attr in parsed.tags if tag=='a' and '/releases/download/' in attr.get('href','')}
                self.assertEqual(downloads,codex|{sums})
                self.assertIn('0.2.0',content)
                self.assertNotIn('https://chatgpt.com/plugins/plugins_',content)

    def test_logo_styles_and_japanese_site_footer(self):
        self.assertTrue((ROOT/'assets/ziheng-site.css').is_file())
        for path in CASE:
            content=(ROOT/path).read_text(encoding='utf-8')
            self.assertIn('KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png',content)
            # Landing pages use the ZiHeng index stylesheet; install guides share the
            # canonical KUMIHAN install-guide layout.
            self.assertIn('kumihan-install.css' if path.startswith('docs/') else 'ziheng-site.css',content)
        landing=(ROOT/'_layouts/landing.html').read_text(encoding='utf-8')
        # The shared footer lists every edition, ZiHeng included.
        self.assertIn("site.data.site_footer",landing)
        footer=json.loads((ROOT/'_data/site_footer.json').read_text(encoding='utf-8'))
        self.assertIn('kumihan-zh-han.html',footer['zh-Hant-TW'])

if __name__ == '__main__':
    unittest.main()
