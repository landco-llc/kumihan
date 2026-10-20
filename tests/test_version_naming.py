"""Current package names across KUMIHAN languages use numeric SemVer only.

Historical releases are immutable and intentionally excluded from this rule.
"""
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
SEMVER = re.compile(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\Z")


def version_of(path):
    obj=json.loads(path.read_text(encoding="utf-8"))
    return obj.get("version")


class VersionNamingPolicyTests(unittest.TestCase):
    def test_current_21_product_versions_have_no_preview_suffix(self):
        products = [ROOT] + sorted(p for p in (ROOT/"plugins").iterdir() if p.is_dir() and (p/"plugin.json").is_file())
        self.assertEqual(len(products), 21)
        for product in products:
            with self.subTest(product=product.name):
                manifest=product/"plugin.json"
                version=version_of(manifest)
                self.assertRegex(version, SEMVER)
                for rel in ["gemini-extension.json", ".codex-plugin/plugin.json", ".claude-plugin/plugin.json"]:
                    p=product/rel
                    if p.exists():
                        self.assertEqual(version_of(p),version, (p, version))

    def test_current_distribution_manifest_versions_match_their_products(self):
        products = [ROOT] + sorted(p for p in (ROOT/"plugins").iterdir() if p.is_dir() and (p/"plugin.json").exists())
        for product in products:
            ver=version_of(product/"plugin.json")
            manifests=list(product.glob("downloads*/MANIFEST.json"))+list(product.glob("downloads/**/MANIFEST.json"))
            for m in manifests:
                from ziheng_retention import is_retained_manifest
                if is_retained_manifest(ROOT, m): continue  # exact validated Ziheng historical manifest only
                with self.subTest(path=str(m.relative_to(ROOT))):
                    data=json.loads(m.read_text(encoding="utf-8"))
                    v=data.get("version")
                    if v is None: continue
                    self.assertEqual(str(v).removeprefix("v"), ver)
                    self.assertNotIn("preview",str(v).lower())

    def test_japanese_15_active_distribution_names_and_sizes(self):
        source=ROOT
        for dr in ("downloads Claude","downloads GPT-Codex","downloads Gemini"):
            with self.subTest(platform=dr):
                folder=ROOT/dr
                obj=json.loads((folder/"MANIFEST.json").read_text())
                self.assertEqual(obj["version"], version_of(ROOT/"plugin.json"))
                self.assertEqual(len(obj["archives"]), 5)
                self.assertTrue(all("preview" not in a["file"].lower() for a in obj["archives"]))
                self.assertTrue(all(a["file"].endswith('-'+obj["version"]+'.zip') for a in obj["archives"]))
                for a in obj["archives"]:
                    self.assertTrue((folder/a["file"]).is_file())

    def test_ziheng_active_distribution_and_site_names(self):
        z=ROOT/"plugins/kumihan-ziheng"
        self.assertEqual(version_of(z/"plugin.json"),"0.2.0")
        for dr in ("downloads","downloads Claude","downloads Gemini"):
            with self.subTest(platform=dr):
                folder=z/dr
                obj=json.loads((folder/"MANIFEST.json").read_text())
                self.assertEqual(obj["version"], "0.2.0")
                self.assertEqual(len(obj["archives"]), 5)
                for a in obj["archives"]:
                    self.assertNotIn("preview",a["file"].lower())
                    self.assertIn("0.2.0.zip",a["file"])
                    self.assertTrue((folder/a["file"]).is_file())
        live_sources=[
            z/"README.md",z/"INSTALL.md",z/"UPDATES.md",
            ROOT/"assets/ziheng-site-copy.json",ROOT/"tools/build_ziheng_site.py",
            *list((ROOT/"docs").glob("install-ziheng*.html")),
            *list((z/"docs").glob("installation-*.md")),
            *list(ROOT.glob("kumihan-zh-han*.html")),
        ]
        self.assertGreaterEqual(len(live_sources),23)
        for p in live_sources:
            with self.subTest(file=str(p.relative_to(ROOT))):
                s=p.read_text(encoding="utf-8")
                self.assertNotIn("0.1.0-preview",s)
                self.assertNotIn("PREVIEW / 0.1.0",s)

    def test_current_site_status_uses_suffix_free_version(self):
        landing=(ROOT/'_layouts/landing.html').read_text(encoding='utf-8')
        installation=(ROOT/'_layouts/installation.html').read_text(encoding='utf-8')
        self.assertIn('SOURCE PACKAGE / {% include version/ja-source-version.html %}',landing)
        self.assertIn('releases/tag/v0.1.8-preview',landing)
        self.assertNotIn('PREVIEW /',installation)
        self.assertNotIn('preview version',installation.lower())

    def test_publication_status_comes_from_verified_facts(self):
        landing=(ROOT/"_layouts/landing.html").read_text()
        self.assertIn("{% include version/ja-hero.html %}",landing)
        import json
        facts=json.loads((ROOT/"assets/edition-versions.json").read_text())["editions"]
        hero=(ROOT/"_includes/version/ja-hero.html").read_text()
        self.assertIn(facts["ja"]["release_url"],hero)
        self.assertIn('data-release-status="published"',hero)
        self.assertIn("過去版",landing)
        for name in ("index.html", "top-ja.html"):
            text=(ROOT/name).read_text()
            self.assertNotIn("v0.1.8 preview",text)
            self.assertNotIn("v0.1.0 preview",text)

    def test_naming_contract_has_examples(self):
        text=(ROOT/"docs/versioning.md").read_text(encoding="utf-8")
        self.assertIn("v0.1.8",text)
        self.assertIn("kumihan-ziheng-v0.1.0",text)
        self.assertIn("Historical immutability",text)


if __name__ == "__main__":
    unittest.main()
