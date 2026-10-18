import json
from pathlib import Path
import unittest
import jsonschema
import importlib.util
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'plugins/kumihan-grafia'
class CatalogTests(unittest.TestCase):
 def test_coverage_and_source_closure(self):
  rules=json.loads((BASE/'rules/catalog.json').read_bytes());self.assertEqual(len(rules),48)
  self.assertEqual(len({r['id'] for r in rules}),48)
  sources=json.loads((BASE/'sources/public-sources.json').read_bytes())['sources']
  for r in rules:
   self.assertTrue({'id','locale','region_scope','media','classification','severity','automation_scope','source_refs','exceptions','positive_example','negative_example','status'}<=r.keys())
   self.assertTrue(set(r['source_refs'])<={s['id'] for s in sources})
  self.assertEqual(sum(r['automation_scope']=='bounded-static-candidate' for r in rules),5)
  ledger=json.loads((BASE/'fixtures/acceptance-ledger.json').read_bytes())['fixtures'];self.assertEqual(len(ledger),60)
  self.assertEqual({f['id'] for f in ledger},{f'ES-{kind}{i:02d}' for kind in ('W','F') for i in range(1,31)})
  self.assertEqual({f['status'] for f in ledger},{'not-checked'})
  self.assertFalse(any('drive.google' in s['url'] or 'docs.google' in s['url'] for s in sources))
 def test_report_schema_and_cli_nonmutation(self):
  import subprocess,tempfile,hashlib
  with tempfile.TemporaryDirectory() as directory:
   path=Path(directory)/'source.txt';data='¿Vienes?.\r\nñ n\u0303 « Té » 15\u00a0%'.encode();path.write_bytes(data)
   result=subprocess.run(['python',str(BASE/'runtime/checks.py'),str(path),'--locale','es-AR'],capture_output=True,text=True,check=True)
   report=json.loads(result.stdout);jsonschema.validate(report,json.loads((BASE/'schemas/report.schema.json').read_bytes()))
   self.assertEqual(path.read_bytes(),data);self.assertEqual(report['original_hash'],hashlib.sha256(data).hexdigest())
