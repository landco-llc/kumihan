"""The published ES successor must retain all other edition content exactly."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))

class GrafiaPublishedAdmission(unittest.TestCase):
    def test_verified_facts_and_exact_predecessors(self):
        from grafia_v011_published_transition import load, predecessor_facts, predecessor_readme
        data,facts=load(ROOT)
        raw=(ROOT/'assets/edition-versions.json').read_bytes()
        self.assertEqual(json.loads(raw)['editions']['es'],facts)
        before=json.loads(predecessor_facts(raw,ROOT))
        self.assertEqual(before['editions']['es']['published_version'],'0.1.0')
        self.assertEqual(before['editions']['es']['source_version'],'0.1.1')
        for code,row in json.loads(raw)['editions'].items():
            if code!='es':self.assertEqual(row,before['editions'][code],code)
        readme=(ROOT/'README.md').read_bytes()
        previous=predecessor_readme(readme,ROOT)
        row=data['readme'];self.assertEqual(previous.replace(row['before_line'].encode(),row['after_line'].encode(),1),readme)

    def test_only_es_card_changes_in_shared_gateways(self):
        from grafia_v011_published_transition import load, predecessor_body, admitted
        import re
        data,_=load(ROOT)
        gateways=[name for name,row in data['paths'].items() if row.get('kind')=='gateway-es-card']
        self.assertEqual(len(gateways),38)
        for name in gateways:
            row=data['paths'][name];raw=re.search(rb'<body\b[\s\S]*',(ROOT/name).read_bytes(),re.I)[0]
            before=predecessor_body(ROOT,name,raw)
            self.assertEqual(before.replace(row['before_card'].encode(),row['after_card'].encode(),1),raw,name)
            self.assertTrue(admitted(ROOT,name,row['baseline_sha256'],raw,'bodies'))
            self.assertFalse(admitted(ROOT,name,'0'*64,raw,'bodies'))
            with self.assertRaises(ValueError):predecessor_body(ROOT,name,raw+b' ')

    def test_unrelated_facts_and_readme_changes_cannot_be_hidden(self):
        from grafia_v011_published_transition import predecessor_facts, predecessor_readme
        raw=(ROOT/'assets/edition-versions.json').read_bytes();facts=json.loads(raw)
        facts['editions']['en']['source_version']='9.9.9'
        with self.assertRaises(ValueError):predecessor_facts((json.dumps(facts,ensure_ascii=False,indent=2)+'\n').encode(),ROOT)
        with self.assertRaises(ValueError):predecessor_facts(raw+b' ',ROOT)
        readme=(ROOT/'README.md').read_bytes()
        with self.assertRaises(ValueError):predecessor_readme(readme.replace(b'| EN |',b'| XX |',1),ROOT)

    def test_records_frozen_inputs_and_current_facts_cannot_be_rebaselined(self):
        from grafia_v011_published_transition import RECORD, FACTS, FROZEN, load
        import shutil
        import tempfile
        names=(RECORD,FACTS,*FROZEN,'assets/edition-versions.json')
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)
            for name in names:
                target=root/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,target)
            load(root)
            for name in names:
                target=root/name;raw=target.read_bytes();target.write_bytes(raw+b' ')
                with self.assertRaises(ValueError):load(root)
                target.write_bytes(raw)

    def test_copy_has_nine_profiles_and_does_not_certify_unrun_acceptance(self):
        copy=json.loads((ROOT/'assets/grafia-site-copy.json').read_bytes())
        for lang,c in copy.items():
            self.assertEqual(c['status_title'],'RELEASED / v0.1.1')
            self.assertIn('60',c['status_body'])
            self.assertIn('Office/PDF',c['status_body'])
            self.assertIn('es-US',c['regions']['body'])
            self.assertEqual({row['code'] for row in c['regions']['cards']},{'es-ES','es-MX','es-AR','es-CO','es-CL','es-PE','es-419','es-US'})
