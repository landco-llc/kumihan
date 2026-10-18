import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/"plugins/kumihan-nhip-chu"
spec=importlib.util.spec_from_file_location("vi_checker",BASE/"runtime/checks.py")
checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)
class VietnameseTests(unittest.TestCase):
    def test_catalog(self):
        rules=json.loads((BASE/"rules/catalog.json").read_text(encoding="utf-8"))["rules"]
        self.assertEqual(len(rules),36)
        self.assertEqual(len({r["id"] for r in rules}),36)
        self.assertTrue(all(not r["autofix"] for r in rules))
    def test_preserve_nfc_nfd(self):
        src="Tiếng Việt. Nguyễn Ắ Ệ Ễ Ở ự".encode()
        self.assertEqual(checker.inspect(src,candidate=src)["preservation"]["status"],"passed")
        decomposed="Tiếng Việt".encode().decode().replace("ế","e\u0302\u0301").encode()
        r=checker.inspect(decomposed,candidate=decomposed)
        self.assertEqual(r["preservation"]["status"],"passed")
        self.assertIn("VI-03", [x["rule_id"] for x in r["findings"]])
        self.assertEqual(checker.inspect(src,candidate=b"changed")["preservation"]["status"],"failed")
    def test_css_candidate(self):
        r=checker.inspect("cà phê".encode(),style_text="body { word-break: break-all; hyphens: auto; }")
        self.assertEqual([x["rule_id"] for x in r["findings"]],["VI-15","VI-13"])
    def test_host_manifests(self):
        for p in ("plugin.json",".codex-plugin/plugin.json",".claude-plugin/plugin.json","gemini-extension.json"):
            m=json.loads((BASE/p).read_text(encoding="utf-8"))
            self.assertEqual(m["name"],"kumihan-nhip-chu")
            self.assertEqual(m["version"],"0.1.0")
            self.assertIn(" | ",m["description"])
        for suffix in ("","-web","-documents","-review"):
            p=BASE/"skills"/("kumihan-nhip-chu"+suffix)
            self.assertTrue((p/"SKILL.md").is_file())
            self.assertTrue((p/"assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png").is_file())
            self.assertTrue((p/"agents/openai.yaml").is_file())
if __name__=="__main__":unittest.main()
