"""Offline synthetic controls. Inputs are data in temporary directories, never executed.

No fixture exemptions: the boundary scans every tracked byte, including this file.
Sensitive-looking test values are assembled at run time from synthetic fragments.
"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True


def checker(name):
    path = ROOT / 'scripts' / (name + '.py')
    if not path.is_file():
        raise AssertionError('required checker has not been implemented: ' + name)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class StaticChecks(unittest.TestCase):
    def setUp(self):
        self.s = checker('check_standalone')
        self.b = checker('check_public_boundary')

    def test_fixed_candidate_and_independent_copy(self):
        self.s.check_repository(ROOT)
        with tempfile.TemporaryDirectory() as d:
            for name in self.s.SKILLS:
                folder = Path(d) / name
                shutil.copytree(ROOT / 'skills' / name, folder)
                self.s.check_folder(folder, ROOT)

    def test_cli_and_nonmutation(self):
        def digest():
            return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                    for base in ('skills', 'rules', 'profiles', 'schemas', 'sources', 'skill-src', 'docs')
                    for p in (ROOT / base).rglob('*') if p.is_file()}
        before = digest()
        for _ in range(2):
            for name in ('check_standalone', 'check_public_boundary'):
                run = subprocess.run([sys.executable, '-B', str(ROOT / 'scripts' / (name + '.py')),
                                      '--root', str(ROOT)], capture_output=True, text=True)
                self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        self.assertEqual(before, digest())

    def test_javascript_forms_rejected_as_data(self):
        for form in ("import 'dep'", "import/*c*/x from 'dep'", "import x/*c*/from 'dep'",
                     "import {x} from 'dep'", "import( 'dep' )", "export/*c*/{x}from 'dep'",
                     "export * from 'dep'", "export/*c*/* as x from 'dep'", "require('dep')",
                     "IMPORT /*c*/ x FROM 'dep'", "import\\u0020x from 'dep'"):
            with self.subTest(form=form), self.assertRaises(ValueError):
                self.s.check_text(form, {'local.md'}, 'sample.md')

    def test_html_css_runtime_rejected(self):
        for text in ('<ScRiPt>anything</ScRiPt>', '<iframe src="local.md"></iframe>',
                     '<p OnClick="x()">text</p>', '<img src="https://example.org/a">',
                     '<video poster="//example.org/a">', '<link href="https://example.org/a" rel="stylesheet">',
                     '<style>p{background: url(https://example.org/a)}</style>',
                     '<p style="background:u\\72l(https://example.org/a)">',
                     '@import/*x*/"https://example.org/a";',
                     '![image](https://example.org/a)', '<object data="local.md">',
                     '<img srcset="local.md 1x,">', '<img srcset="local.md nope">',
                     '<img srcset="local.md 1x, https://example.org/a 2x">',
                     '<img srcset="local.md 1x, local.md 1x">', '<script/src="local.md">'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                self.s.check_text(text, {'local.md'}, 'sample.md')

    def test_positive_citations_and_local_transitive_resources(self):
        for text in ('[citation](https://www.w3.org/TR/jlreq/)',
                     '<a href="https://example.org/paper">citation</a>',
                     '[local](local.md#section)', '<img src="local.md">',
                     '<img srcset="local.md 1x, other.md 2x">',
                     'Ordinary prose: do not import fonts without permission.'):
            self.s.check_text(text, {'local.md', 'other.md'}, 'sample.md')
        for text in ('[missing](missing.md)', '[ref][missing]', '[missing]: other.md',
                     '`references/missing.md`', '<img src="missing.md">'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                self.s.check_text(text, {'local.md'}, 'sample.md')

    def test_unsafe_reference_paths(self):
        for path in ('../local.md', '/local.md', 'C:/local.md', '//server/a',
                     './local.md', 'a/../../local.md', '%2e%2e/local.md',
                     '%252e%252e/local.md', 'local%2emd', 'LOCAL.md', 'a\\b.md',
                     'file:///local.md', 'data:text/plain,a', 'javascript:thing', '.hidden/a'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                self.s.local_reference(path, {'local.md'})

    def test_conservative_syntax_rejects_unsupported_active_forms(self):
        for text in ("export {x}\nfrom 'dep'", '<style>p{background:u\\72l(https://example.org/a)}</style>',
                     '<a ping="https://example.org/a" href="local.md">text</a>',
                     '<meta http-equiv="refresh" content="0;url=https://example.org/a">',
                     '<custom-widget resource="https://example.org/a">'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                self.s.check_text(text, {'local.md'}, 'sample.md')

    def test_semantic_controls_without_inventory_shortcut(self):
        original = self.s.read_files(ROOT / 'skills/kumihan')
        self.s.check_catalog(original)
        for path, action in (
            ('rules/catalog.json', lambda v: v.append(v[0])),
            ('rules/catalog.json', lambda v: v[0]['source_refs'].append('absent')),
            ('rules/catalog.json', lambda v: v[0]['verification'].update(coverage='implemented')),
            ('rules/catalog.json', lambda v: v[1]['case_ids'].append(v[0]['case_ids'][0])),
            ('profiles/web-ui.json', lambda v: v['rule_ids'].append(v['rule_ids'][0])),
            ('profiles/web-ui.json', lambda v: v['rule_ids'].append('DOC-001')),
            ('sources/public-sources.json', lambda v: v['sources'].append(v['sources'][0])),
            ('sources/public-sources.json', lambda v: v['sources'][-1].update(statement=None)),
            ('sources/public-sources.json', lambda v: v['sources'][-1].update(rule_ids=['CONTENT-001'])),
            ('schemas/profile.schema.json', lambda v: v['properties']['id'].update({'$ref':'https://example.org/schema'})),
        ):
            files = dict(original); value=json.loads(files[path]); action(value)
            files[path]=json.dumps(value).encode()
            with self.subTest(path=path), self.assertRaises(ValueError): self.s.check_catalog(files)

    def test_rule_profile_and_evidence_schemas_offline(self):
        files=self.s.read_files(ROOT/'skills/kumihan'); validators=self.s.schema_registry(files)
        rule=json.loads(files['rules/catalog.json'])[0]
        profile=json.loads(files['profiles/web-ui.json'])
        for key, obj in (('rule',rule),('profile',profile)):
            for required in validators[key].schema['required']:
                changed=dict(obj); del changed[required]
                self.assertFalse(validators[key].is_valid(changed))
            self.assertFalse(validators[key].is_valid(dict(obj, unknown=True)))
        design_text=(ROOT/'skills/kumihan/references/design-contract.md').read_text()
        design=json.loads(design_text.split('```json\n',1)[1].split('```',1)[0])
        self.assertTrue(validators['design-contract'].is_valid(design))
        self.assertFalse(validators['design-contract'].is_valid(dict(design,created_before_generation=False)))
        report={'report_id':'synthetic','artifact_ref':'synthetic.md','artifact_digest':'sha256:'+'0'*64,
                'ruleset_version':'0.1.0','profile':'web-ui','checks':[],
                'environment':{'host':'synthetic','tools':{},'renderers':[]},
                'limitations':[],'content_change_summary':[]}
        for status in ('passed','failed','needs-review','not-checked','unsupported','waived','not-applicable'):
            check={'rule_id':'CONTENT-001','status':status,'method':'manual','evidence_refs':['synthetic'],
                   'scope':'synthetic','reason':'synthetic'}
            if status=='waived': check['waiver']={'approval_ref':'synthetic','scope':'synthetic','reason':'synthetic',
                                                  'artifact_digest':report['artifact_digest']}
            report['checks']=[check]
            self.assertTrue(validators['report'].is_valid(report),status)
        report['checks'][0].update(status='passed',evidence_refs=[])
        self.assertFalse(validators['report'].is_valid(report))

    def test_json_duplicate_keys_and_unsupported_includes(self):
        for text in ('{"a":1,"a":2}', '{"include":"local.md"}', '{"$include":"local.md"}',
                     '{"nested":{"imports":["local.md"]}}', '{"x":NaN}'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                self.s.json_data(text)

    def test_folder_mutations_rejected_even_with_updated_inventory(self):
        def mutate(path, change, rehash=False):
            with tempfile.TemporaryDirectory() as d:
                folder = Path(d) / 'kumihan'
                shutil.copytree(ROOT / 'skills/kumihan', folder)
                change(folder / path)
                if rehash:
                    inv = json.loads((folder / 'inventory.json').read_text())
                    for entry in inv['files']:
                        p = folder / entry['path']
                        entry['bytes'] = p.stat().st_size
                        entry['sha256'] = hashlib.sha256(p.read_bytes()).hexdigest()
                    (folder / 'inventory.json').write_text(json.dumps(inv))
                with self.assertRaises(ValueError):
                    self.s.check_folder(folder, ROOT)
        def edit_json(p, action):
            value = json.loads(p.read_text()); action(value); p.write_text(json.dumps(value))
        cases = [
            ('rules/catalog.json', lambda p: edit_json(p, lambda v: v.append(v[0])), True),
            ('sources/public-sources.json', lambda p: edit_json(p, lambda v: v['sources'].append(v['sources'][0])), True),
            ('profiles/web-ui.json', lambda p: edit_json(p, lambda v: v['rule_ids'].append('UNKNOWN-001')), True),
            ('rules/content.json', lambda p: p.write_text('[]'), True),
            ('schemas/rule.schema.json', lambda p: p.write_text('{}'), True),
            ('references/architecture.md', lambda p: p.write_text(p.read_text().replace('reject admission', 'accept admission')), True),
            ('SKILL.md', lambda p: p.write_text(p.read_text() + '\n[escape](../secret.md)\n'), True),
            ('rules/catalog.json', lambda p: p.write_text('[]'), False),
            ('inventory.json', lambda p: edit_json(p, lambda v: v['files'].append(v['files'][0])), False),
            ('inventory.json', lambda p: edit_json(p, lambda v: v.update(canonical_commit='0'*40)), False),
            ('references/review-protocol.md', lambda p: p.unlink(), False),
            ('SKILL.md', lambda p: p.write_bytes(b'\xff'), False),
            ('.hidden', lambda p: p.write_text('synthetic'), False),
            ('skill.md', lambda p: p.write_text('alias'), False),
            ('extra.js', lambda p: p.write_text('console.log(1)'), False),
            ('references/linked.md', lambda p: p.symlink_to('architecture.md'), False),
            ('pipe', lambda p: os.mkfifo(p), False),
        ]
        for path, action, rehash in cases:
            with self.subTest(path=path, rehash=rehash): mutate(path, action, rehash)

    def test_canonical_corruption_and_relationships(self):
        for path, action in (
            ('rules/content.json', lambda v: v.append(v[0])),
            ('rules/content.json', lambda v: v[0]['source_refs'].append('absent')),
            ('sources/public-sources.json', lambda v: v['sources'].append(v['sources'][0])),
            ('profiles/web-ui.json', lambda v: v['rule_ids'].append('DOC-001')),
            ('schemas/report.schema.json', lambda v: v.update(extra_keyword=True)),
        ):
            with self.subTest(path=path), tempfile.TemporaryDirectory() as d:
                root = Path(d)
                for directory in ('rules','profiles','schemas','sources','skill-src','docs'):
                    shutil.copytree(ROOT / directory, root / directory)
                shutil.copy(ROOT / 'LICENSE', root / 'LICENSE')
                p=root/path; v=json.loads(p.read_text()); action(v); p.write_text(json.dumps(v))
                with self.assertRaises(ValueError): self.s.check_folder(ROOT/'skills/kumihan', root)

    def test_cli_invalid_schema_is_sanitized(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); shutil.copytree(ROOT/'skills',root/'skills')
            p=root/'skills/kumihan/schemas/rule.schema.json'
            value=json.loads(p.read_text()); value['type']='synthetic-invalid-type';p.write_text(json.dumps(value))
            run=subprocess.run([sys.executable,'-B',str(ROOT/'scripts/check_standalone.py'),'--root',str(root)],
                               capture_output=True,text=True)
            self.assertEqual(run.returncode,1)
            self.assertEqual(run.stderr,'')
            self.assertEqual(json.loads(run.stdout)['status'],'failed')
            self.assertNotIn('synthetic-invalid-type',run.stdout)

    def documentation_copy(self, root):
        shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns('.git', '__pycache__'))
        p=root/'README.md'
        p.write_bytes(p.read_bytes()+b'\nPublic documentation clarification for standalone users.\n')
        subprocess.run(['git','init','-q',str(root)],check=True)
        subprocess.run(['git','-C',str(root),'add','.'],check=True)

    def tracked_digests(self, root):
        names=subprocess.check_output(['git','-C',str(root),'ls-files','-z']).split(b'\0')
        return {name: hashlib.sha256((root/name.decode()).read_bytes()).hexdigest()
                for name in names if name}

    def test_public_documentation_update_and_nonmutation(self):
        original=self.tracked_digests(ROOT)
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/'repository'; self.documentation_copy(root)
            before=self.tracked_digests(root)
            self.assertEqual({n for n in original if original[n]!=before[n]}, {b'README.md'})
            for _ in range(2):
                self.s.check_repository(root)
                self.assertEqual(self.b.check_repository(root)['fixture_exemptions'],0)
                for name in ('check_standalone','check_public_boundary'):
                    run=subprocess.run([sys.executable,'-B',str(root/'scripts'/(name+'.py')),
                                        '--root',str(root)],capture_output=True,text=True)
                    self.assertEqual(run.returncode,0,run.stdout+run.stderr)
            self.assertEqual(before,self.tracked_digests(root))
        self.assertEqual(original,self.tracked_digests(ROOT))

    def test_documentation_update_preserves_fixed_input_rejections(self):
        cases=[(path,'canonical-digest') for path in
               ('rules/content.json','profiles/web-ui.json','schemas/rule.schema.json',
                'sources/public-sources.json','skill-src/kumihan/SKILL.md',
                'docs/architecture.md','LICENSE')]
        cases.append(('schemas/release-manifest.schema.json','canonical-extra-digest'))
        for skill in self.s.SKILLS:
            cases.extend(((f'skills/{skill}/rules/content.json','inventory-file-digest'),
                          (f'skills/{skill}/inventory.json','inventory-snapshot')))
        original=self.tracked_digests(ROOT)
        for path,code in cases:
            with self.subTest(path=path), tempfile.TemporaryDirectory() as d:
                root=Path(d)/'repository'; self.documentation_copy(root)
                p=root/path; p.write_bytes(p.read_bytes()+b'\n')
                before=self.tracked_digests(root)
                with self.assertRaisesRegex(ValueError,'^'+code+'$'):
                    self.s.check_repository(root)
                run=subprocess.run([sys.executable,'-B',str(root/'scripts/check_standalone.py'),
                                    '--root',str(root)],capture_output=True,text=True)
                self.assertEqual(run.returncode,1)
                self.assertEqual(run.stderr,'')
                self.assertEqual(json.loads(run.stdout)['status'],'failed')
                self.assertEqual(self.b.check_repository(root)['fixture_exemptions'],0)
                self.assertEqual(before,self.tracked_digests(root))
        self.assertEqual(original,self.tracked_digests(ROOT))

    def test_public_documentation_still_scanned_by_boundary(self):
        original=self.tracked_digests(ROOT)
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/'repository'; self.documentation_copy(root)
            p=root/'README.md'
            p.write_text(p.read_text()+'customer_email: '+'synthetic'+'@'+'example.invalid')
            before=self.tracked_digests(root)
            self.s.check_repository(root)
            with self.assertRaisesRegex(ValueError,'^public-boundary-rejected-file-'):
                self.b.check_repository(root)
            run=subprocess.run([sys.executable,'-B',str(root/'scripts/check_public_boundary.py'),
                                '--root',str(root)],capture_output=True,text=True)
            self.assertEqual(run.returncode,1)
            self.assertEqual(run.stderr,'')
            self.assertEqual(json.loads(run.stdout)['status'],'failed')
            self.assertNotIn('example.invalid',run.stdout)
            self.assertEqual(before,self.tracked_digests(root))
        self.assertEqual(original,self.tracked_digests(ROOT))

    def test_test_source_is_public_safe_without_exemption(self):
        self.b.check_text(Path(__file__).read_text())

    def test_public_boundary_synthetic_controls_and_redaction(self):
        controls = [('gh'+'p_'+'A'*36), ('AK'+'IA'+'0'*16),
                    '-----BEGIN '+'PRIVATE KEY-----', 'https://drive.'+'google.com/file/d/'+'synthetic-id',
                    's3'+'://synthetic-private/bucket', '/home/'+'synthetic/private/notes',
                    '/Users/'+'synthetic/private.txt', 'customer_email: '+'person'+'@'+'example.invalid',
                    'user: synthetic private message\nassistant: synthetic reply',
                    'https://example.invalid/a?X-Amz-'+'Signature=synthetic',
                    'customer_name: '+'Synthetic Person', 'private_storage_id: '+'synthetic-123']
        for value in controls:
            with self.subTest(kind=controls.index(value)):
                with self.assertRaises(ValueError) as caught: self.b.check_text(value)
                self.assertNotIn(value, str(caught.exception))
        self.b.check_text('Public citation https://www.w3.org/TR/jlreq/ and Apache License')
        self.b.check_repository(ROOT)

    def test_public_boundary_scans_tracked_files_and_no_fixture_exemption(self):
        for name in ('rules/data.json', 'skills/kumihan/SKILL.md',
                     'tests/fixtures/standalone/synthetic.txt', 'private/transcript.log'):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as d:
                r=Path(d); subprocess.run(['git','init','-q',str(r)],check=True)
                p=r/name;p.parent.mkdir(parents=True);p.write_text('customer_email: '+'synthetic'+'@'+'example.invalid')
                subprocess.run(['git','-C',str(r),'add','.'],check=True)
                with self.assertRaises(ValueError): self.b.check_repository(r)


if __name__ == '__main__':
    unittest.main()
