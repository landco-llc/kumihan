import copy
import hashlib
import unittest
from pathlib import Path
from fixtures import request, plan, module, observation, audit, error

ROOT = Path(__file__).resolve().parents[1]

class ContractTests(unittest.TestCase):
    def test_validator_exists(self):
        self.assertTrue((ROOT / 'contract.py').exists(), 'Full development Draft202012 validator is missing')

    def validate(self, value):
        from contract import validate_record
        return validate_record(value)

    def test_six_record_kinds(self):
        r = request(); p = plan(r)
        for value in (r, p, module(), observation(r), audit(r, p), error()):
            with self.subTest(kind=value['kind']):
                self.validate(value)

    def test_unknown_fields_and_version_rejected(self):
        for key, value in (('unknown_core', True), ('contract_version', '1.0')):
            r = request(); r[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.validate(r)

    def test_forged_status_and_waiver_structure_rejected(self):
        r = request(); a = audit(r, plan(r))
        for change in ({'status':'passed'}, {'status':'checked'}, {'status':'waived'}, {'status':'verified'}):
            value = copy.deepcopy(a); value['checks'][0].update(change)
            with self.subTest(change=change), self.assertRaises(ValueError): self.validate(value)

    def test_reference_copy_exact(self):
        self.assertEqual(hashlib.sha256((ROOT/'schemas/composition-0.1.0-design.1.schema.json').read_bytes()).hexdigest(),
                         '14d9226833c8ff1af8a92f8da56de4c852f003e87803f78c3ec8bf45c8c75cda')

    def test_legacy_mapping_is_separate_and_lossless(self):
        from contract import legacy_snapshot, restore_legacy
        old = {'status':'guidance-only', 'source_unchanged':True, 'checked':[], 'not_checked':['visual_rendering']}
        before = copy.deepcopy(old)
        side = legacy_snapshot(old)
        self.assertEqual(restore_legacy(side), old)
        self.assertEqual(old, before)
        self.assertNotIn('contract_version', old)
        with self.assertRaises(ValueError): legacy_snapshot(dict(old, checked=['MIX-001']))

if __name__ == '__main__': unittest.main()
