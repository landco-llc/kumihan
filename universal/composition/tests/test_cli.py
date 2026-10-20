import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from fixtures import request

ROOT=Path(__file__).resolve().parents[1]

class CliTests(unittest.TestCase):
    def test_cli_exists(self):self.assertTrue((ROOT/'cli.py').exists(),'Offline CLI missing')
    def test_validate_exit_and_named_error_no_source_log(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'request.json';r=request();p.write_text(json.dumps(r))
            proc=subprocess.run([sys.executable,str(ROOT/'cli.py'),'validate',str(p)],capture_output=True,text=True)
            self.assertEqual(proc.returncode,0,proc.stderr)
            self.assertEqual(json.loads(proc.stdout)['validated_kind'],'request')
            r['sources'][0]['text_digest']='sha256:'+'0'*64;p.write_text(json.dumps(r))
            proc=subprocess.run([sys.executable,str(ROOT/'cli.py'),'validate',str(p)],capture_output=True,text=True)
            self.assertEqual(proc.returncode,2)
            self.assertEqual(json.loads(proc.stdout)['code'],'E_SOURCE_DIGEST')
            self.assertNotIn('原稿',proc.stdout+proc.stderr)

if __name__=='__main__':unittest.main()
