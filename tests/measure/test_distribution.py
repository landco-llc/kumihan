"""Current Measure consumers retain exact provenance and fail-closed validation."""
import hashlib
import json
from pathlib import Path
import sys
import unittest
from zipfile import ZipFile

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
from measure_consumer import check_source,check_distribution,check_entries,check_member
P=ROOT/'plugins/kumihan-measure'

class MeasureDistribution(unittest.TestCase):
    def test_current_source_and_all_fifteen_archives(self):
        check_source(P)
        manifest=check_distribution(P,P/'downloads')
        self.assertEqual(manifest['version'],'0.1.1')
        self.assertEqual(len(manifest['packages']),15)
        self.assertEqual(manifest['rule_count'],51)

    def test_historical_archives_are_unchanged(self):
        pins=json.loads((ROOT/'tools/measure_legacy_v010.json').read_text())
        self.assertEqual(len(pins),15)
        for name,sha in pins.items():
            self.assertEqual(hashlib.sha256((P/'downloads'/name).read_bytes()).hexdigest(),sha)

    def test_current_archive_rejects_wrong_identity_or_missing_dependencies(self):
        path=P/'downloads/kumihan-measure-gpt-codex-skill-v0.1.1.zip'
        with ZipFile(path) as archive:clean={n:archive.read(n) for n in archive.namelist()}
        prefix='kumihan-measure/'
        for dependency in ('profiles/house-styles.json','locales/en-CA.json','references/regional-typography.md','fixtures/regional-acceptance.json'):
            changed=dict(clean);del changed[prefix+dependency]
            with self.assertRaises(ValueError):check_entries(changed,standalone=True)
        for key,value in (('version','0.1.0'),('rule_count',45)):
            changed=dict(clean);inventory=json.loads(changed[prefix+'inventory.json']);inventory[key]=value
            changed[prefix+'inventory.json']=json.dumps(inventory).encode()
            with self.assertRaises(ValueError):check_entries(changed,standalone=True)

    def test_hidden_payloads_and_unsafe_paths_are_rejected(self):
        for name in ('../escape.md','references/GOAL.md','.env','control/input.json'):
            with self.assertRaises(ValueError):check_member(name,b'innocent')
        for raw in (b'WORK_ID: hidden',b'[mcp_servers.test]',b'Private candidate',b'-----BEGIN PRIVATE KEY-----'):
            with self.assertRaises(ValueError):check_member('references/payload.bin',raw)
