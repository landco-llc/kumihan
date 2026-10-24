"""The Measure patch changes one source edition while retaining published facts."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from en_measure_v011_transition import admitted,predecessor

class MeasureSourceAdmission(unittest.TestCase):
    def test_only_the_exact_source_cell_is_admitted(self):
        data,old=predecessor(ROOT);raw=old.replace(data['before_line'].encode(),data['after_line'].encode(),1)
        self.assertTrue(admitted(ROOT,'README.md',data['baseline_sha256'],raw,'protected'))
        for path,family,before,payload in [('README.md','bodies',data['baseline_sha256'],raw),('index.html','protected',data['baseline_sha256'],raw),('README.md','protected','0'*64,raw),('README.md','protected',data['baseline_sha256'],raw+b'!')]:
            self.assertFalse(admitted(ROOT,path,before,payload,family))
        self.assertFalse(admitted(ROOT,'README.md',data['baseline_sha256'],raw.replace(b'Published',b'Changed',1),'protected'))

    def test_only_english_source_facts_change(self):
        current=json.loads((ROOT/'assets/edition-versions.json').read_text())
        self.assertEqual(current['editions']['en']['source_version'],'0.1.1')
        original=json.loads((ROOT/'tests/contracts/en-measure-v010-published-facts.json').read_text())
        expected=copy.deepcopy(original);expected['source_version']='0.1.1'
        # Retain the source-only phase independently of the later verified release.
        phase=copy.deepcopy(current);phase['editions']['en']=expected
        phase_raw=(json.dumps(phase,ensure_ascii=False,indent=2)+'\n').encode()
        self.assertEqual(hashlib.sha256(phase_raw).hexdigest(),'fb46376cc16e9e0a18cc205a62cfab6972feed495cf9f8846539b39f000e50db')
        predecessor_facts=copy.deepcopy(current);predecessor_facts['editions']['en']=original
        raw=(json.dumps(predecessor_facts,ensure_ascii=False,indent=2)+'\n').encode()
        self.assertEqual(hashlib.sha256(raw).hexdigest(),'17f9106e88b03b4a9364f792e6351215a691e49da934971c5700e9ad5b7fcb3d')
