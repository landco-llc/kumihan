"""Ensure CI executes the bounded fixtures and keeps recorded evidence current."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('thai_fixture_runner', HERE/'run_fixtures.py')
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)

class FixtureTests(unittest.TestCase):
    def test_actual_results_match_execution(self):
        actual = runner.run()
        recorded = json.loads((HERE/'actual-results.json').read_text())
        self.assertEqual(actual, recorded)
        self.assertEqual(actual['counts'], {'passed': 5, 'failed': 0, 'not-checked': 35})
        self.assertEqual(len(actual['results']), 40)
        self.assertEqual({r['id'] for r in actual['results']}, {f'TH-F{i:03d}' for i in range(1, 41)})
        catalog = json.loads((ROOT/'plugins/kumihan-th/rules/catalog.json').read_text())
        rule_ids = {r['id'] for r in catalog}
        fixtures = {f['id']: f for f in json.loads((HERE/'fixtures.json').read_text())}
        for result in actual['results']:
            with self.subTest(fixture=result['id']):
                self.assertTrue(result['rule_ids'])
                self.assertEqual(len(result['rule_ids']), len(set(result['rule_ids'])))
                self.assertTrue(set(result['rule_ids']) <= rule_ids)
                self.assertEqual(result['rule_ids'], fixtures[result['id']]['rule_ids'])
