import unittest
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[2]

class Tags(HTMLParser):
    def __init__(self,text):
        super().__init__();self.tags=[];self.feed(text)
    def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))

class Site(unittest.TestCase):
    def test_twelve_pages_locale_navigation_and_downloads(self):
        for suffix,lang in [('', 'zh-Hans-CN'),('.en','en'),('.ja','ja')]:
            names=[f'kumihan-zh-cn{suffix}.html']+[f'docs/install-zilu-{h}{suffix}.html' for h in ('chatgpt','claude','gemini')]
            for name in names:
                p=ROOT/name;self.assertTrue(p.exists(),name)
                text=p.read_text();tags=Tags(text).tags
                self.assertEqual([a['lang'] for t,a in tags if t=='html'],[lang])
                self.assertEqual(sum(t=='h1' for t,a in tags),1)
                alternates=[a for t,a in tags if t=='link' and a.get('rel')=='alternate']
                self.assertEqual({a['hreflang'] for a in alternates},{'zh-Hans-CN','en','ja','x-default'})
                for tag,attrs in tags:
                    if tag=='a' and attrs.get('href','').startswith('/kumihan/'):
                        target=attrs['href'].split('#')[0].removeprefix('/kumihan/')
                        if target:self.assertTrue((ROOT/target).exists(),target)
                self.assertNotIn('drive.google.com',text)
