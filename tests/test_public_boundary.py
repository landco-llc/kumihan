"""Public release boundary: exact retention and rejection of new internal material."""
import io
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'tools'))

class PublicBoundaryTests(unittest.TestCase):
    def test_unlisted_path_internal_text_and_mcp_are_rejected(self):
        import public_boundary as b
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root/'safe.txt').write_text('User installation guide')
            contract = {'files': {'safe.txt': b.digest(b'User installation guide')}, 'legacy_archives': {}}
            self.assertEqual(b.audit(root, contract), [])
            for name, text in [('docs/RESULT.md', 'execution result'), ('mcp.json', '{"mcpServers": {}}'), ('safe.txt', 'WORK_ID: SECRET\nNEXT_GATE: deploy')]:
                target=root/name; target.parent.mkdir(parents=True, exist_ok=True); target.write_text(text)
                self.assertTrue(b.audit(root, contract), name)
                if name!='safe.txt':target.unlink()
            (root/'safe.txt').write_text('User installation guide changed')
            self.assertTrue(b.audit(root, contract))

    def test_clean_candidate_removes_internal_members_and_rejects_mcp(self):
        import public_boundary as b
        def archive(files):
            out=io.BytesIO()
            with zipfile.ZipFile(out,'w') as z:
                for name,raw in files.items():z.writestr(name,raw)
            return out.getvalue()
        safe=next((ROOT/'downloads Claude/skills').glob('*.zip')).read_bytes()
        self.assertEqual(b.clean_archive(safe),safe)
        raw=archive({'pkg/SKILL.md':b'Product guidance','pkg/LIGHT_REVIEW.md':b'internal','pkg/LICENSE':b'license'})
        clean=b.clean_archive(raw)
        with zipfile.ZipFile(io.BytesIO(clean)) as z:
            self.assertEqual(set(z.namelist()), {'pkg/SKILL.md','pkg/LICENSE'})
            self.assertEqual(z.read('pkg/SKILL.md'),b'Product guidance')
        for name, content in [('pkg/.mcp.json', b'{}'), ('pkg/settings.json', b'{"mcpServers": {"prod": {"url": "https://example.test"}}}'), ('pkg/config.toml', b'[mcp_servers.production]\nurl = "https://example.test/mcp"')]:
            with self.assertRaises(ValueError):b.clean_archive(archive({name: content}))

    def test_built_site_rejects_unknown_and_modified_archives(self):
        import public_boundary as b
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            raw=b'unchanged committed archive'
            (root/'old.zip').write_bytes(raw)
            contract={'files': {'old.zip': b.digest(raw)}, 'legacy_archives': {'old.zip': b.digest(raw)}}
            self.assertEqual(b.audit_site(root, contract), [])
            (root/'old.zip').write_bytes(b'injected')
            self.assertTrue(b.audit_site(root, contract))
            (root/'old.zip').write_bytes(raw)
            (root/'new.zip').write_bytes(b'injected')
            self.assertTrue(b.audit_site(root, contract))

    def test_ignored_dependency_cache_does_not_exempt_tracked_injection(self):
        import public_boundary as b
        import subprocess
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            subprocess.run(['git','init','-q',td],check=True)
            rules=b'/vendor/\n/.bundle/\n'
            (root/'.gitignore').write_bytes(rules)
            (root/'vendor').mkdir()
            (root/'vendor/cache.txt').write_text('dependency cache')
            contract={'files': {'.gitignore': b.digest(rules)}, 'legacy_archives': {}}
            self.assertEqual(b.audit(root,contract), [])
            subprocess.run(['git','-C',td,'add','-f','vendor/cache.txt'],check=True)
            self.assertTrue(b.audit(root,contract))

    def test_contract_and_legacy_archives_are_exact(self):
        import public_boundary as b
        self.assertEqual(b.audit(ROOT), [])
