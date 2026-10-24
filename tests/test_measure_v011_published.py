"""Only verified English publication facts and English gateway cards may change."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from en_measure_v011_published_transition import RECORD,FACTS,load,admitted,predecessor_body

def scoped(name,family):
    raw=(ROOT/name).read_bytes()
    return re.search(rb'<body\b[\s\S]*',raw,re.I)[0] if family=='bodies' else raw

class MeasurePublishedAdmission(unittest.TestCase):
    def test_current_facts_and_pages_match_exact_published_admission(self):
        data,facts=load(ROOT)
        current=json.loads((ROOT/'assets/edition-versions.json').read_text())
        self.assertEqual(current['editions']['en'],facts)
        self.assertEqual(data['published_at'],'2026-10-24T16:17:36Z')
        self.assertEqual(len(data['paths']),39)
        for name,row in data['paths'].items():
            raw=scoped(name,row['family'])
            self.assertTrue(admitted(ROOT,name,row['baseline_sha256'],raw,row['family']),name)
            if row['family']=='bodies':
                self.assertIn('aria-labelledby="language-en"',row['before_card'])
                self.assertIn('aria-labelledby="language-en"',row['after_card'])
                before=predecessor_body(ROOT,name,raw)
                self.assertEqual(before.replace(row['before_card'].encode(),row['after_card'].encode(),1),raw)
        for name,row in data['site_files'].items():
            raw=(ROOT/name).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(),row['after_sha256'],name)
            self.assertIn(b'0.1.1',raw,name)
            self.assertNotIn(b'Private candidate',raw,name)

    def test_wrong_path_family_hash_and_bytes_are_rejected(self):
        data,_=load(ROOT);name='index.html';row=data['paths'][name];raw=scoped(name,'bodies')
        for path,family,before,payload in [('index.html','protected',row['baseline_sha256'],raw),
            ('other.html','bodies',row['baseline_sha256'],raw),('index.html','bodies','0'*64,raw),
            ('index.html','bodies',row['baseline_sha256'],raw+b'!')]:
            self.assertFalse(admitted(ROOT,path,before,payload,family))
        with self.assertRaises(ValueError):predecessor_body(ROOT,name,raw+b'!')

    def test_pinned_publication_record_and_facts_cannot_be_changed(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary)
            for name in (RECORD,FACTS):
                target=root/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,target)
            load(root)
            for name in (RECORD,FACTS):
                target=root/name;raw=target.read_bytes();target.write_bytes(raw+b' ')
                with self.assertRaises(ValueError):load(root)
                target.write_bytes(raw)

    def test_english_copy_removes_only_the_stale_development_claim(self):
        import copy
        current=json.loads((ROOT/'assets/upcoming-editions.json').read_text())
        self.assertEqual(current['en']['product']['version'],'v0.1.1')
        self.assertNotIn('in development',current['en']['card']['en'][0])
        self.assertNotIn('開発中',current['en']['card']['ja'][0])
        old=copy.deepcopy(current);old['en']['product']['version']='v0.1.0'
        old['en']['card']['en'][0]=old['en']['card']['en'][0].replace('English typography that','English typography, in development from completed research, that',1)
        old['en']['card']['ja'][0]='調査を終えて開発中。'+old['en']['card']['ja'][0]
        raw=(json.dumps(old,ensure_ascii=False,indent=2)+'\n').encode()
        self.assertEqual(hashlib.sha256(raw).hexdigest(),'082f92121cb77f26cf9aacb7e15cbd6e5d90f0c0b40f05ce7ca8764059fc9140')
        for name in ('kumihan-en.html','kumihan-en.ja.html'):
            raw=(ROOT/name).read_bytes()
            self.assertNotIn(b'v0.1.0',raw)
            self.assertNotIn(b'45 English typography rules',raw)
            self.assertNotIn('英語文字組の45規則'.encode(),raw)
