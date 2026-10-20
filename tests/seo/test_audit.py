import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
import seo_metadata as seo


class AuditTests(unittest.TestCase):
    def page(self, root, path='index.html', **changes):
        values = dict(title='試験 & test', description='原稿を保持するテスト', lang='ja', canonical=seo.canonical_url(path), alternates={'ja': seo.canonical_url(path)})
        values.update(changes)
        html = '<html lang="%s"><head>%s</head><body>unchanged</body></html>' % (values['lang'], seo.render_metadata(**values))
        p = root / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(html)
        return p

    def test_new_language_is_discovered_and_missing_metadata_fails(self):
        from check_seo import audit
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            self.page(root)
            p = root / 'top-fixture.html'
            p.write_text((Path(__file__).parent/'fixtures/test-fixture-new-language/page.html').read_text())
            self.assertTrue(any('top-fixture.html' in e for e in audit(root, check_sitemap=False)))
            self.page(root, 'top-fixture.html', lang='fr', alternates={'fr':seo.canonical_url('top-fixture.html')})
            self.assertEqual([], audit(root, check_sitemap=False))

    def test_new_directory_is_discovered_and_sources_excluded(self):
        from check_seo import audit
        from build_sitemap import sitemap
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); self.page(root)
            p=root/'guides/new.html'; p.parent.mkdir(); p.write_text('<html><head></head></html>')
            self.assertTrue(any('guides/new.html' in e for e in audit(root,check_sitemap=False)))
            self.page(root,'guides/new.html')
            ignored=root/'templates/hidden.html'; ignored.parent.mkdir(); ignored.write_text('not public')
            qa=root/'docs/development/qa/evidence/prototype.html'
            qa.parent.mkdir(parents=True); qa.write_text('standalone QA artifact, not public')
            self.assertEqual([],audit(root,check_sitemap=False))
            self.assertEqual(2,sitemap(root).count('<loc>'))

    def test_sitemap_sorted_noindex_and_external_excluded_without_lastmod(self):
        from build_sitemap import sitemap
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            self.page(root)
            self.page(root, 'docs/a.html')
            p = self.page(root, 'private.html')
            p.write_text(p.read_text().replace('</head>', '<meta name="robots" content="noindex"></head>'))
            self.page(root, 'external.html', canonical='https://example.com/a')
            result = sitemap(root)
            self.assertEqual(2, result.count('<loc>'))
            self.assertNotIn('index.html', result)
            self.assertNotIn('private.html', result)
            self.assertNotIn('external.html', result)
            self.assertNotIn('lastmod', result)

    def test_wrong_canonical_and_nonreciprocal_alternates_rejected(self):
        from check_seo import audit
        from build_sitemap import sitemap
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            self.page(root)
            self.page(root, 'bad.html', canonical=seo.canonical_url('absent.html'))
            self.assertTrue(any('canonical' in e for e in audit(root, check_sitemap=False)))
            with self.assertRaises(ValueError):
                sitemap(root)
            self.page(root, 'bad.html', alternates={'ja':seo.canonical_url('bad.html'), 'en':seo.canonical_url('en.html')})
            self.page(root, 'en.html', lang='en', alternates={'en':seo.canonical_url('en.html')})
            self.assertTrue(any('reciprocal' in e for e in audit(root, check_sitemap=False)))

    def test_duplicate_meta_jsonld_mismatch_and_sitemap_drift_rejected(self):
        from check_seo import audit
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            p=self.page(root)
            p.write_text(p.read_text().replace('</head>', '<meta name="description" content="duplicate"></head>').replace('"inLanguage":"ja"','"inLanguage":"en"'))
            errors=audit(root)
            self.assertTrue(any('description' in e for e in errors))
            self.assertTrue(any('inLanguage' in e for e in errors))
            self.assertTrue(any('sitemap' in e for e in errors))

    def test_comma_delimited_robots_none_is_not_indexable(self):
        from build_sitemap import sitemap
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); self.page(root)
            p=self.page(root,'private.html')
            p.write_text(p.read_text().replace('</head>','<meta name="robots" content="none, max-snippet:-1"></head>'))
            self.assertNotIn('private.html',sitemap(root))

    def test_check_mode_is_nonwriting(self):
        import subprocess
        from build_sitemap import sitemap
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); self.page(root)
            target=root/'sitemap.xml'; target.write_text('stale')
            tool=Path(__file__).resolve().parents[2]/'tools/build_sitemap.py'
            result=subprocess.run([sys.executable,str(tool),'--root',str(root),'--check'],capture_output=True)
            self.assertNotEqual(0,result.returncode)
            self.assertEqual('stale',target.read_text())
            target.write_text(sitemap(root))
            self.assertEqual(0,subprocess.run([sys.executable,str(tool),'--root',str(root),'--check'],capture_output=True).returncode)
