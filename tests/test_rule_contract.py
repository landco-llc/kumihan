"""Catalog/schema and packaged rule contracts; no renderer claims.

Run: python3 -m unittest discover -s tests -v
Requires the development-only dependency in requirements-dev.txt.
"""
import copy
import hashlib
import json
import unittest
import zipfile
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ('kumihan', 'kumihan-web', 'kumihan-documents', 'kumihan-review')


def check_contract(catalog, schema, expected):
    ids = [rule['id'] for rule in catalog]
    enum = schema['$defs']['rule_id']['enum']
    if len(ids) != len(set(ids)) or len(enum) != len(set(enum)):
        raise ValueError('duplicate rule IDs')
    if set(ids) != set(enum) or set(ids) != expected:
        raise ValueError(f'catalog/schema ID mismatch: {set(ids) ^ set(enum)}')
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    for rule in catalog:
        validator.validate(rule)
    rule = next(rule for rule in catalog if rule['id'] == 'JA-TYPE-011')
    if rule['verification']['method'] != 'assisted' or rule['verification']['coverage'] != 'guidance-only':
        raise ValueError('JA-TYPE-011 must remain assisted/guidance-only')


class RuleContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base = ROOT / 'skills/kumihan'
        cls.catalog = json.loads((base / 'rules/catalog.json').read_bytes())
        cls.schema = json.loads((base / 'schemas/rule.schema.json').read_bytes())
        cls.expected = {rule['id'] for rule in cls.catalog}

    def test_four_skills_and_six_profiles(self):
        self.assertEqual(len(self.expected), 39)
        for name in SKILLS:
            with self.subTest(skill=name):
                base = ROOT / 'skills' / name
                catalog = json.loads((base / 'rules/catalog.json').read_bytes())
                schema = json.loads((base / 'schemas/rule.schema.json').read_bytes())
                check_contract(catalog, schema, self.expected)
                self.assertEqual(catalog, self.catalog)
                self.assertEqual(schema, self.schema)
                profiles = list((base / 'profiles').glob('*.json'))
                self.assertEqual(len(profiles), 6)
                for path in profiles:
                    ids = json.loads(path.read_bytes())['rule_ids']
                    self.assertEqual(len(ids), len(set(ids)), path)
                    self.assertLessEqual(set(ids), self.expected, path)
                    self.assertIn('JA-TYPE-011', ids, path)

    def test_archives_match_manifest_inventory_and_rule_contract(self):
        folders = sorted(ROOT.glob('downloads *'))
        self.assertEqual(len(folders), 3)
        for folder in folders:
            manifest = json.loads((folder / 'MANIFEST.json').read_bytes())
            self.assertEqual(manifest['version'], json.loads((ROOT / 'plugin.json').read_text(encoding='utf-8'))['version'])
            self.assertEqual(len(manifest['archives']), 5)
            for entry in manifest['archives']:
                path = folder / entry['file']
                with self.subTest(archive=str(path.relative_to(ROOT))):
                    self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), entry['sha256'])
                    with zipfile.ZipFile(path) as archive:
                        names = archive.namelist()
                        self.assertEqual(len(names), len(set(names)))
                        self.assertEqual(set(names), {m['path'] for m in entry['members']})
                        for member in entry['members']:
                            data = archive.read(member['path'])
                            self.assertEqual(len(data), member['bytes'])
                            self.assertEqual(hashlib.sha256(data).hexdigest(), member['sha256'])
                        catalogs = [n for n in names if n.endswith('rules/catalog.json')]
                        self.assertEqual(len(catalogs), 1 if entry['file'].startswith('skills/') else 4)
                        for name in catalogs:
                            prefix = name[:-len('rules/catalog.json')]
                            catalog = json.loads(archive.read(name))
                            schema = json.loads(archive.read(prefix + 'schemas/rule.schema.json'))
                            check_contract(catalog, schema, self.expected)
                            self.assertEqual(catalog, self.catalog)
                            self.assertEqual(schema, self.schema)
                            inventory = json.loads(archive.read(prefix + 'inventory.json'))
                            self.assertEqual(inventory['version'], manifest['version'])
                            for item in inventory['files']:
                                data = archive.read(prefix + item['path'])
                                self.assertEqual(len(data), item['bytes'])
                                self.assertEqual(hashlib.sha256(data).hexdigest(), item['sha256'])
                            for profile in self.schema['$defs']['media_profile']['enum']:
                                ids = json.loads(archive.read(prefix + f'profiles/{profile}.json'))['rule_ids']
                                self.assertEqual(len(ids), len(set(ids)))
                                self.assertLessEqual(set(ids), self.expected)
                                self.assertIn('JA-TYPE-011', ids)

    def test_reject_missing_enum_id(self):
        schema = copy.deepcopy(self.schema)
        schema['$defs']['rule_id']['enum'].remove('JA-TYPE-011')
        with self.assertRaisesRegex(ValueError, 'ID mismatch'):
            check_contract(self.catalog, schema, self.expected)

    def test_reject_duplicate_catalog_and_enum_ids(self):
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            check_contract(self.catalog + [self.catalog[0]], self.schema, self.expected)
        schema = copy.deepcopy(self.schema)
        schema['$defs']['rule_id']['enum'].append('CONTENT-001')
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            check_contract(self.catalog, schema, self.expected)

    def test_reject_invalid_rule_objects(self):
        from jsonschema import ValidationError
        for field, value in [('revision', '1'), ('strength', 'unknown'), ('title_ja', '')]:
            catalog = copy.deepcopy(self.catalog)
            catalog[0][field] = value
            with self.subTest(field=field), self.assertRaises(ValidationError):
                # Use a consistent enum so this specifically exercises object validation.
                schema = copy.deepcopy(self.schema)
                schema['$defs']['rule_id']['enum'] = sorted(self.expected)
                check_contract(catalog, schema, self.expected)
        catalog = copy.deepcopy(self.catalog)
        del catalog[0]['title_ja']
        schema = copy.deepcopy(self.schema)
        schema['$defs']['rule_id']['enum'] = sorted(self.expected)
        with self.assertRaises(ValidationError):
            check_contract(catalog, schema, self.expected)


if __name__ == '__main__':
    unittest.main()
