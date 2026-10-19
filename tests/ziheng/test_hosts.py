"""Independent Claude/Gemini package assertions (stdlib, read-only)."""
import hashlib
import io
import json
import sys
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PRODUCT = "plugins/kumihan-ziheng"
sys.path.insert(0, str(ROOT / "tools"))
import build_ziheng_hosts as host

NAMES = host.NAMES

def digest(b):
    return hashlib.sha256(b).hexdigest()

class HostPackagingTests(unittest.TestCase):
    def test_host_archives_self_contained_and_canonical(self):
        outs=host.plan_outputs(ROOT)
        manifest=json.loads((ROOT/PRODUCT/"plugin.json").read_text())
        version=manifest["version"]
        for platform,(folder,part,label,skill_kind) in host.HOSTS.items():
            with self.subTest(platform=platform):
                droot=PRODUCT+"/"+folder+"/"
                meta=json.loads(outs[droot+"MANIFEST.json"])
                self.assertEqual(meta["version"],version)
                self.assertEqual(meta["publisher"],"L&Co. LLC")
                self.assertEqual(len(meta["archives"]),5)
                sums=outs[droot+"SHA256SUMS.txt"].decode().splitlines()
                self.assertEqual(len(sums),6)
                for line in sums:
                    expected,rel=line.split("  ",1)
                    self.assertEqual(expected,digest(outs[droot+rel]))
                bundle=next(a for a in meta["archives"] if a["file"].startswith(part+"/"))
                with zipfile.ZipFile(io.BytesIO(outs[droot+bundle["file"]])) as z:
                    self.assertIsNone(z.testzip())
                    paths=z.namelist()
                    self.assertEqual(len(paths),len(set(paths)))
                    if platform=="Claude":
                        prefix="kumihan-ziheng/"
                        cfg=json.loads(z.read(prefix+".claude-plugin/plugin.json"))
                        self.assertEqual(cfg["name"],"kumihan-ziheng")
                    else:
                        prefix=""
                        cfg=json.loads(z.read("gemini-extension.json"))
                        self.assertEqual(cfg["name"],"kumihan-ziheng")
                    self.assertEqual(cfg["version"],version)
                    self.assertIn("繁體中文",cfg["description"])
                    for name in NAMES:
                        stem=f"skills/{name}/"
                        self.assertIn(prefix+stem+"SKILL.md",paths)
                        inv=json.loads(z.read(prefix+stem+"inventory.json"))
                        self.assertEqual(inv["skill"],name)
                        self.assertEqual(inv["version"],version)
                        for f in inv["files"]:
                            archive_file=z.read(prefix+stem+f["path"])
                            canonical=(ROOT/PRODUCT/stem/f["path"]).read_bytes()
                            self.assertEqual(archive_file,canonical)
                            self.assertEqual(digest(archive_file),f["sha256"])
                            self.assertEqual(len(archive_file),f["bytes"])
                        rules=json.loads(z.read(prefix+stem+"rules/catalog.json"))
                        self.assertFalse(any(r["id"].startswith("JA-TYPE") for r in rules))
                for name in NAMES:
                    item=next(a for a in meta["archives"] if a["file"].endswith(f"{name}-{skill_kind}-{version}.zip"))
                    with zipfile.ZipFile(io.BytesIO(outs[droot+item["file"]])) as z:
                        skill_prefix=name+"/" if platform=="Claude" else ""
                        self.assertIn(skill_prefix+"SKILL.md",z.namelist())
                        self.assertEqual(
                            z.read(skill_prefix+"SKILL.md"),
                            (ROOT/PRODUCT/"skills"/name/"SKILL.md").read_bytes(),
                        )
                        self.assertEqual(len(z.namelist()),len(host.skill_source_files(ROOT,name,version)))

    def test_generator_no_source_writes_in_check_and_determinism(self):
        before={p:p.read_bytes() for p in (ROOT/PRODUCT/"skills").rglob("*") if p.is_file()}
        first=host.plan_outputs(ROOT)
        self.assertEqual(first,host.plan_outputs(ROOT))
        self.assertEqual(before,{p:p.read_bytes() for p in before})
        self.assertTrue(all(path.startswith(PRODUCT+"/") for path in first))
        self.assertTrue(all(
            any(segment in path for segment in ("/downloads Claude/","/downloads Gemini/","/.claude-plugin/","/gemini-extension.json"))
            for path in first
        ))
        self.assertEqual({p for p,data in first.items() if not (ROOT/p).exists() or (ROOT/p).read_bytes()!=data},set())
        self.assertEqual(host.generated_files(ROOT),set(first))

    def test_host_package_locale_and_region_protection(self):
        output=host.plan_outputs(ROOT)
        bundle=output[f"{PRODUCT}/downloads Gemini/extensions/kumihan-ziheng-Gemini-CLI-extension-0.1.0.zip"]
        with zipfile.ZipFile(io.BytesIO(bundle)) as z:
            tw=json.loads(z.read("skills/kumihan-ziheng/locales/zh-Hant-TW.json"))
            hk=json.loads(z.read("skills/kumihan-ziheng/locales/zh-Hant-HK.json"))
            self.assertEqual(tw["quotation"]["default"],"corner")
            self.assertIsNone(hk["quotation"]["default"])
            rules=json.loads(z.read("skills/kumihan-ziheng/rules/catalog.json"))
            self.assertEqual(sum(bool(r.get("title_zh_hant")) for r in rules),15)

    def test_claude_marketplace_entry_preserves_japanese(self):
        path=ROOT/".claude-plugin/marketplace.json"
        if not path.exists():
            self.skipTest("Marketplace readback not materialized locally")
        m=json.loads(path.read_text())
        rows={x["name"]:x for x in m["plugins"]}
        self.assertEqual(rows["kumihan"]["source"],".")
        self.assertEqual(rows["kumihan-ziheng"]["source"],"./plugins/kumihan-ziheng")
        self.assertNotEqual(rows["kumihan"]["name"],rows["kumihan-ziheng"]["name"])

if __name__=="__main__":
    unittest.main()
