import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
PRODUCT=ROOT/'plugins/kumihan-ziheng'
NAMES=['kumihan-ziheng','kumihan-ziheng-web','kumihan-ziheng-documents','kumihan-ziheng-review']

class PackageTests(unittest.TestCase):
    def test_builder_isolated_deterministic_and_self_contained(self):
        self.assertTrue((ROOT/'tools/build_ziheng.py').is_file(), 'independent builder missing')
        import build_ziheng
        first=build_ziheng.plan_outputs(ROOT)
        self.assertEqual(first,build_ziheng.plan_outputs(ROOT))
        self.assertTrue(all(p.startswith('plugins/kumihan-ziheng/') for p in first))
        for name in NAMES:
            version=json.loads((PRODUCT/'plugin.json').read_text())['version']
            key=next(p for p in first if p.endswith(f'{name}-{version}.zip'))
            with tempfile.TemporaryDirectory() as td:
                archive=Path(td)/'skill.zip';archive.write_bytes(first[key])
                with zipfile.ZipFile(archive) as z:
                    self.assertTrue(all(not Path(p).is_absolute() and '..' not in Path(p).parts for p in z.namelist()))
                    z.extractall(td)
                skill=Path(td)/name
                for path in skill.rglob('*.md'):
                    for link in re.findall(r'\]\(([^)]+)\)',path.read_text()):
                        if '://' not in link and not link.startswith('#'):
                            self.assertTrue((path.parent/link.split('#')[0]).resolve().is_relative_to(skill.resolve()))
                            self.assertTrue((path.parent/link.split('#')[0]).exists(), (name,link))
                inv=json.loads((skill/'inventory.json').read_text())
                for member in inv['files']:
                    data=(skill/member['path']).read_bytes()
                    self.assertEqual(hashlib.sha256(data).hexdigest(),member['sha256'])
                spec=importlib.util.spec_from_file_location('isolated_checks',skill/'scripts/checks.py')
                api=importlib.util.module_from_spec(spec);spec.loader.exec_module(api)
                self.assertEqual(api.check_preservation(b'unchanged',b'unchanged')['status'],'passed')
                catalog=json.loads((skill/'rules/catalog.json').read_text())
                self.assertFalse(any(r['id'].startswith('JA-TYPE') for r in catalog))
                sources=json.loads((skill/'sources/public-sources.json').read_text())
                source_ids={s['id'] for s in sources['sources']}
                self.assertTrue(all(set(r['source_refs'])<=source_ids for r in catalog))
                for locale in ['zh-Hant-TW','zh-Hant-HK']:
                    for medium in build_ziheng.MEDIA:
                        profile=json.loads((skill/f'profiles/{medium}.json').read_text())
                        ids=profile['rules_by_locale'][locale]
                        self.assertEqual(len(ids),len(set(ids)))
                        self.assertNotIn('ZH-HANT-004' if locale.endswith('TW') else 'ZH-HANT-003',ids)
                self.assertEqual((skill/'LICENSE').read_bytes(),(ROOT/'LICENSE').read_bytes())

    def test_zh_resolver_regions_are_disjoint_and_deterministic(self):
        import locale_resolver
        for locale in ['zh-Hant-TW','zh-Hant-HK']:
            for medium in locale_resolver.MEDIA:
                context=locale_resolver.resolve_context(locale,medium)
                rules=locale_resolver.resolve_rules(context,ROOT)
                ids=[r['id'] for r in rules]
                self.assertTrue(ids)
                self.assertEqual(ids,list(dict.fromkeys(ids)))
                self.assertIn('ZH-HANT-003' if locale.endswith('TW') else 'ZH-HANT-004',ids)
                self.assertNotIn('ZH-HANT-004' if locale.endswith('TW') else 'ZH-HANT-003',ids)
                self.assertFalse(any(i.startswith('JA-TYPE') for i in ids))
                self.assertEqual(rules,locale_resolver.resolve_rules(context,ROOT))

    def test_new_schemas_and_rules(self):
        import jsonschema
        schema=json.loads((PRODUCT/'schemas/rule.schema.json').read_text())
        jsonschema.Draft202012Validator.check_schema(schema)
        records=json.loads((PRODUCT/'rules/zh-hant.json').read_text())
        self.assertEqual(len(records),15)
        for r in records: jsonschema.validate(r,schema)
        for group in ['content','design','evidence']:
            for r in json.loads((ROOT/f'skills/kumihan/rules/{group}.json').read_text()):jsonschema.validate(r,schema)
        for f in (PRODUCT/'schemas').glob('*.json'):
            jsonschema.Draft202012Validator.check_schema(json.loads(f.read_text()))

if __name__=='__main__':unittest.main()

class DistributionContractTests(unittest.TestCase):
    def test_bilingual_branding_and_portable_icon(self):
        import io
        import build_ziheng
        m = json.loads((PRODUCT/'plugin.json').read_text(encoding='utf-8'))
        ui = m['extensions']['com.openai']['interface']
        self.assertEqual(ui['displayName'], 'KUMIHAN｜字衡')
        self.assertEqual(m['name'], 'kumihan-ziheng')
        for text in [m['description'], ui['shortDescription'], ui['longDescription']]:
            self.assertIn('Traditional Chinese', text)
            self.assertIn('繁體中文', text)
        asset = 'assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png'
        self.assertEqual(ui['logo'], './'+asset)
        self.assertEqual(ui['composerIcon'], './'+asset)
        original = (ROOT/asset).read_bytes()
        outputs = build_ziheng.plan_outputs(ROOT)
        self.assertEqual(outputs['plugins/kumihan-ziheng/'+asset], original)
        version = m['version']
        zip_rel = 'plugins/kumihan-ziheng/downloads/plugins/kumihan-ziheng-'+version+'.zip'
        with zipfile.ZipFile(io.BytesIO(outputs[zip_rel])) as z:
            self.assertEqual(z.read('kumihan-ziheng/'+asset), original)
            overlay = json.loads(z.read('kumihan-ziheng/.codex-plugin/plugin.json'))
            self.assertEqual(overlay['interface']['displayName'], ui['displayName'])
            self.assertEqual(overlay['interface']['logo'], ui['logo'])
            self.assertEqual(overlay['interface']['composerIcon'], ui['composerIcon'])

    def test_plugin_archive_paths_and_identity(self):
        import build_ziheng
        version=json.loads((PRODUCT/'plugin.json').read_text())['version']
        outputs=build_ziheng.plan_outputs(ROOT)
        import io
        data=outputs[f'plugins/kumihan-ziheng/downloads/plugins/kumihan-ziheng-{version}.zip']
        with tempfile.TemporaryDirectory() as td:
            with zipfile.ZipFile(io.BytesIO(data)) as z: z.extractall(td)
            base=Path(td)/'kumihan-ziheng'
            portable=json.loads((base/'plugin.json').read_text())
            overlay=json.loads((base/'.codex-plugin/plugin.json').read_text())
            self.assertEqual(portable['name'],'kumihan-ziheng')
            self.assertEqual(portable['version'],overlay['version'])
            self.assertNotEqual(portable['name'],json.loads((ROOT/'plugin.json').read_text())['name'])
            self.assertTrue((base/overlay['skills']).is_dir())
            for p in base.rglob('*.md'):
                for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
                    if '://' not in link and not link.startswith('#'):
                        target=(p.parent/link.split('#')[0]).resolve()
                        self.assertTrue(target.is_relative_to(base.resolve()),(p,link))
                        self.assertTrue(target.exists(),(p,link))

    def test_report_and_profiles_resolve_offline(self):
        import jsonschema
        from referencing import Registry,Resource
        import build_ziheng
        outputs=build_ziheng.plan_outputs(ROOT)
        rule=json.loads((PRODUCT/'schemas/rule.schema.json').read_text())
        reg=Registry().with_resource(rule['$id'],Resource.from_contents(rule))
        profile_schema=json.loads((PRODUCT/'schemas/profile.schema.json').read_text())
        validator=jsonschema.Draft202012Validator(profile_schema,registry=reg)
        for p,b in outputs.items():
            if '/profiles/' in p: validator.validate(json.loads(b))
        import locale_resolver
        context_schema=json.loads((PRODUCT/'schemas/context.schema.json').read_text())
        for locale in ['zh-Hant-TW','zh-Hant-HK']:
            jsonschema.validate(locale_resolver.resolve_context(locale,'web-editorial'),context_schema)
        with self.assertRaises(jsonschema.ValidationError):
            c=locale_resolver.resolve_context('zh-Hant-TW','web-ui');c['region']='HK';jsonschema.validate(c,context_schema)
        report_schema=json.loads((PRODUCT/'schemas/report.schema.json').read_text())
        validator=jsonschema.Draft202012Validator(report_schema,registry=reg)
        report=dict(report_id='fixture',artifact_ref='sample bytes',artifact_digest='sha256:'+'0'*64,ruleset_version='0.1.0',profile='web-editorial',locale='zh-Hant-TW',environment={'host':'test','tools':{'Python':'3.12'},'renderers':[]},limitations=['No rendered checks'],content_change_summary=[],checks=[{'rule_id':'ZH-HANT-005','status':'not-checked','method':'static','evidence_refs':[],'scope':'fixture','reason':'Not run'}])
        validator.validate(report)
        report['checks'][0]['status']='passed'
        with self.assertRaises(jsonschema.ValidationError):validator.validate(report)

    def test_version_change_and_check_do_not_touch_japanese(self):
        import shutil
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            for rel in ['plugins/kumihan-ziheng','skills/kumihan','tools','assets']:
                shutil.copytree(ROOT/rel,root/rel,ignore=shutil.ignore_patterns('__pycache__'))
            shutil.copy2(ROOT/'LICENSE',root/'LICENSE')
            before={p.relative_to(root):p.read_bytes() for p in (root/'skills').rglob('*') if p.is_file()}
            script=root/'tools/build_ziheng.py'
            subprocess.run([sys.executable,str(script),'--set-version','0.2.0'],check=True,capture_output=True)
            self.assertEqual(before,{p.relative_to(root):p.read_bytes() for p in (root/'skills').rglob('*') if p.is_file()})
            self.assertTrue((root/'plugins/kumihan-ziheng/downloads/plugins/kumihan-ziheng-0.2.0.zip').is_file())
            self.assertFalse(list((root/'plugins/kumihan-ziheng/downloads').rglob('*-0.1.0.zip')))
            target=root/'plugins/kumihan-ziheng/skills/kumihan-ziheng/SKILL.md'
            target.write_bytes(b'changed')
            check=subprocess.run([sys.executable,str(script),'--check'],capture_output=True)
            self.assertEqual(check.returncode,1)
            self.assertEqual(target.read_bytes(),b'changed')
            for bad in ['../escape','0.1.0/escape','1.2','-1.2.3','0.2.0-preview']:
                run=subprocess.run([sys.executable,str(script),'--set-version',bad],capture_output=True)
                self.assertNotEqual(run.returncode,0)
