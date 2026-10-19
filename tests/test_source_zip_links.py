"""Regression: source downloads are independent of formal Release admission."""
import sys
from pathlib import Path
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'tools'))
import edition_versions as v
from version_display import rewrite_downloads

class SourceDownloads(unittest.TestCase):
    def test_corrupt_source_bytes_abort_instead_of_promoting(self):
        import tempfile
        import json
        from unittest.mock import patch
        from version_display import source_archives
        source_archives.cache_clear()
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            folder=root/'plugins/kumihan-zilu/downloads'
            folder.mkdir(parents=True)
            (folder/'bad.zip').write_bytes(b'corrupt')
            (folder/'MANIFEST.json').write_text(json.dumps(dict(version='0.1.0',archives=[
                dict(file='bad.zip',bytes=7,sha256='0'*64)])))
            with patch('version_display.ROOT',root):
                with self.assertRaisesRegex(ValueError,'checksum mismatch'):
                    source_archives('zh-hans','0.1.0')
        source_archives.cache_clear()

    def test_source_inventory_preserves_distinct_roles(self):
        from version_display import source_archives
        for code in ['zh-hans','zh-hant']:
            self.assertEqual(len(source_archives(code,'0.1.0')),15)

    def test_existing_sources_remain_links_without_claiming_release(self):
        for code, path in [
            ('zh-hant','plugins/kumihan-ziheng/downloads/plugins/kumihan-ziheng-0.1.0.zip'),
            ('zh-hant','plugins/kumihan-ziheng/downloads/skills/kumihan-ziheng-0.1.0.zip'),
            ('zh-hans','plugins/kumihan-zilu/downloads/plugins/kumihan-zilu-plugin-v0.1.0.zip')]:
            f=v.load()['editions'][code]
            for url in ['../'+path, v.REPO.replace('github.com','raw.githubusercontent.com')+'/main/'+path]:
                with self.subTest(url=url):
                    out=rewrite_downloads(f'<a href="{url}">ZIP</a>',f)
                    self.assertIn('href="'+url+'"',out)
                    self.assertIn('Source ZIP',out)
                    self.assertNotIn('/releases/download/',out)
                    self.assertEqual(rewrite_downloads(out,f),out)

    def test_untrusted_or_wrong_product_sources_stay_disabled(self):
        f=v.load()['editions']['zh-hant']
        path='plugins/kumihan-ziheng/downloads/plugins/kumihan-ziheng-0.1.0.zip'
        for url in ['https://example.com/'+path,'../'+path.replace('0.1.0','9.9.9'),
                    '../plugins/kumihan-zilu/downloads/plugins/kumihan-zilu-plugin-v0.1.0.zip']:
            self.assertNotIn('href=',rewrite_downloads(f'<a href="{url}">ZIP</a>',f))
