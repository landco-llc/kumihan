from pathlib import Path
import importlib.util
import unittest

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("registry_builder_ziheng_v020", ROOT / "universal/tools/build_registry.py")
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)

class ZihengV020RegistryTests(unittest.TestCase):
    def test_v020_module_from_integrated_source(self):
        registry = builder.build()
        self.assertEqual(registry["module_count"], 21)
        module = registry["modules"]["zh-Hant"]
        self.assertEqual(module["version"], "0.2.0")
        self.assertEqual(module["name"], "KUMIHAN｜字衡")
        self.assertEqual(len(module["rules"]), 15)
        self.assertEqual({r["id"] for r in module["rules"]},
                         {"ZH-HANT-%03d" % n for n in range(1, 16)})
        self.assertEqual(set(module["locales"]), {"zh-Hant", "zh-Hant-TW", "zh-Hant-HK"})
        self.assertEqual(module["status"], "preview_unverified")
        self.assertEqual(len(module["module_sha256"]), 64)

    def test_version_and_digest_are_module_scoped(self):
        original = builder.build()["modules"]["zh-Hant"]
        self.assertTrue(all(p["path"].startswith("plugins/kumihan-ziheng/") for p in original["files"]))
        self.assertFalse("passed" in original.get("capabilities", []))
