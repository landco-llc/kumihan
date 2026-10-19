"""Source adapters must handle future Jekyll pages and preserve authored bodies."""
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
import build_bn_site
import build_jekyll_seo
from seo_metadata import _Head


class AdapterTests(unittest.TestCase):
    def test_new_jekyll_page_uses_frontmatter_without_page_registry(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'templates').mkdir()
            (root / 'templates/seo-fixture-head.html').write_text(
                '<title>{{ page.title | escape }}</title>'
                '<meta name="description" content="{{ page.description | escape }}">')
            (root / 'new-language.html').write_text(
                '---\nlayout: fixture\nlang: fr\ntitle: "Texte & forme"\n'
                'description: "Un texte original"\n---\nKeep this original body.')
            with patch.object(build_jekyll_seo, 'ROOT', root):
                out = build_jekyll_seo.outputs()
            self.assertEqual(set(out), {'_includes/seo-pages/new-language.html'})
            head = next(iter(out.values()))
            parser = _Head()
            parser.feed(head)
            self.assertEqual(parser.canonical,
                             'https://landco-llc.github.io/kumihan/new-language.html')
            data = json.loads(re.search(r'application/ld\+json">(.*?)</script>', head)[1])
            page = next(node for node in data['@graph'] if node['@type'] == 'WebPage')
            self.assertEqual(page['name'], 'Texte & forme')
            self.assertEqual(page['inLanguage'], 'fr')

    def test_jekyll_missing_share_data_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'templates').mkdir()
            (root / '_data').mkdir()
            (root / '_data/site_share.json').write_text('{}')
            (root / 'templates/seo-fixture-head.html').write_text('<title>T</title><meta name="description" content="D">')
            (root / 'new.html').write_text('---\nlayout: fixture\nlang: fa\n---\nBody')
            with patch.object(build_jekyll_seo, 'ROOT', root):
                with self.assertRaisesRegex(ValueError, 'Stale Jekyll share data'):
                    build_jekyll_seo.outputs()
            (root / 'new.html').write_text('---\nlayout: fixture\nlang: xx\n---\nBody')
            with patch.object(build_jekyll_seo, 'ROOT', root):
                with self.assertRaisesRegex(ValueError, 'Unregistered Jekyll share language'):
                    build_jekyll_seo.outputs()

    def test_layout_does_not_duplicate_generated_alternates(self):
        layout = (build_jekyll_seo.ROOT / '_layouts/landing.html').read_text()
        self.assertNotIn('hreflang=', layout.split('</head>')[0])

    def test_default_jekyll_language_is_passed_to_share_renderer(self):
        head = build_jekyll_seo.outputs()['_includes/seo-pages/docs/install-chatgpt.html']
        self.assertIn('{% capture seo_share_lang %}ja{% endcapture %}', head)
        layout = (build_jekyll_seo.ROOT / '_layouts/installation.html').read_text()
        self.assertIn('lang=seo_share_lang', layout)
        share = (build_jekyll_seo.ROOT / '_includes/share.html').read_text()
        self.assertIn('include.lang | default: page.lang', share)

    def test_head_branches_and_unknown_syntax_fail_explicitly(self):
        source = "{% if page.lang == 'ja' %}日本語{% elsif page.lang == 'en' %}English{% else %}其他{% endif %}"
        for lang, expected in [('ja', '日本語'), ('en', 'English'), ('zh-Hant-TW', '其他')]:
            self.assertEqual(build_jekyll_seo.render_head(source, {'lang': lang}), expected)
        with self.assertRaises(ValueError):
            build_jekyll_seo.render_head('{{ page.title | unknown }}', {'title': 'original'})

    def test_bengali_body_is_exactly_preserved(self):
        templates = build_bn_site.ROOT / 'templates/bn'
        for path, output in build_bn_site.outputs().items():
            authored = (templates / path).read_text(encoding='utf-8')
            body = lambda html: re.search(r'<body\b[\s\S]*', html, re.I)[0]
            with self.subTest(path=path):
                self.assertEqual(body(output), body(authored))
                self.assertIn('application/ld+json', output)


if __name__ == '__main__':
    unittest.main()
