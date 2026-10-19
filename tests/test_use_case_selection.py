"""Use-case routing acceptance and compatibility checks (design v0.1/v0.1a).

These are routing/static regression tests, NOT AI semantics or rendering tests.
Run: python3 -m unittest tests.test_use_case_selection -v
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "kumihan"
SELECTOR = SKILL / "scripts" / "use_case_selector.py"
SPEC_PATH = SKILL / "references" / "use-case-adapters.json"
spec = importlib.util.spec_from_file_location("kumihan_use_case_selector", SELECTOR)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)
route = module.route


class UseCaseRoutingTests(unittest.TestCase):
    def test_uca01_social_static_auto(self):
        a = route("Instagram用の広告画像を作って")
        self.assertEqual((a["medium"], a["adapter"]), ("display-copy", "social-static"))
        self.assertEqual(a["review_intensity"], "standard")
        self.assertFalse(a["needs_confirmation"])

    def test_uca02_landing_page_auto(self):
        a = route("新商品のランディングページを作って")
        self.assertEqual((a["medium"], a["adapter"]), ("web-marketing", "landing-page"))
        self.assertFalse(a["needs_confirmation"])

    def test_uca03_generic_copy_not_forced_into_an_adapter(self):
        a = route("短いコピーを考えて")
        self.assertEqual((a["medium"], a["adapter"]), ("display-copy", None))
        self.assertFalse(a["needs_confirmation"])

    def test_uca04_compatible_manual_override(self):
        a = route("文字中心の静止画像を作って", manual_adapter="poster")
        self.assertEqual((a["medium"], a["adapter"]), ("display-copy", "poster"))
        self.assertEqual(a["selection_source"], "manual")

    def test_manual_profile_match_but_surface_conflict_confirms(self):
        a = route("Instagram用の広告画像を作って", manual_adapter="poster")
        self.assertTrue(a["needs_confirmation"])
        self.assertEqual(a["status"], "needs-clarification")

    def test_uca05_incompatible_manual_override_confirms(self):
        a = route("ランディングページを制作", manual_adapter="social-static")
        self.assertEqual(a["status"], "needs-clarification")
        self.assertEqual(a["confirmation_question"].count("？"), 1)
        self.assertIsNone(a["adapter"])

    def test_uca06_minor_unknown_details_no_question(self):
        a = route("Instagram用の広告画像を作って。配色は後ほど決定")
        self.assertEqual(a["adapter"], "social-static")
        self.assertFalse(a["needs_confirmation"])

    def test_uca07_ambiguous_banner_asks_once(self):
        a = route("バナーを作って")
        self.assertEqual(a["status"], "needs-clarification")
        self.assertTrue(a["needs_confirmation"])
        self.assertEqual(a["confirmation_question"].count("？"), 1)
        self.assertIsNone(a["medium"])

    def test_uca08_strict_not_inferred_from_use_case(self):
        a = route("AIっぽくないポスターを作って")
        self.assertEqual(a["adapter"], "poster")
        self.assertEqual(a["review_intensity"], "standard")
        self.assertFalse(a["prior_strict_policy_verified"])

    def test_uca09_post_production_strict_is_not_retroactive(self):
        a = route("ポスターをレビュー", stage="after-production", strict_explicit=True, mode="audit")
        self.assertEqual(a["review_intensity"], "strict")
        self.assertFalse(a["prior_strict_policy_verified"])
        self.assertTrue(any("not retroactive" in m for m in a["limitations"]))

    def test_uca10_audit_does_not_edit(self):
        original = SELECTOR.read_bytes()
        digest = hashlib.sha256(original).hexdigest()
        a = route("ポスターをレビュー", mode="audit")
        self.assertEqual(a["workflow_mode"], "audit")
        self.assertTrue(any("read-only" in m for m in a["limitations"]))
        self.assertEqual(hashlib.sha256(SELECTOR.read_bytes()).hexdigest(), digest)
        self.assertNotIn("authorized", a)
        self.assertNotIn("passed", a)

    def test_presentation_routes_to_existing_medium(self):
        self.assertEqual((route("プレゼンテーション資料を作って")["medium"], route("プレゼンテーション資料を作って")["adapter"]), ("presentation", "slide-deck"))

    def test_report_routes_to_existing_medium(self):
        a = route("A4の報告書を作って")
        self.assertEqual((a["medium"], a["adapter"]), ("report-document", "report"))

    def test_static_banner_routes_to_display_copy(self):
        a = route("1600×900のバナー画像を作って")
        self.assertEqual((a["medium"], a["adapter"]), ("display-copy", "digital-banner"))

    def test_interactive_html_banner_is_not_static(self):
        a = route("HTMLでクリックできるバナーを作って")
        self.assertEqual((a["medium"], a["adapter"]), ("web-marketing", None))
        self.assertFalse(a["needs_confirmation"])

    def test_image_and_html_banner_is_ambiguous(self):
        a = route("画像かHTMLのバナーを作って")
        self.assertEqual(a["status"], "needs-clarification")

    def test_article_and_ui_keep_profiles_without_adapters(self):
        self.assertEqual((route("ブログ記事を制作")["medium"],route("ブログ記事を制作")["adapter"]),("web-editorial",None))
        self.assertEqual((route("アプリ画面のUIを作成")["medium"],route("アプリ画面のUIを作成")["adapter"]),("web-ui",None))

    def test_multiple_output_media_requires_one_question(self):
        a = route("報告書とプレゼン資料のどちらかを作りたい")
        self.assertTrue(a["needs_confirmation"])
        self.assertIsNone(a["medium"])

    def test_unknown_adapter_and_medium_rejected(self):
        with self.assertRaisesRegex(ValueError,"Unknown adapter"):
            route("ポスター",manual_adapter="graphic-design")
        with self.assertRaisesRegex(ValueError,"Unknown medium"):
            route("ポスター",manual_medium="graphic-design")

    def test_manual_medium_compatible_or_conflicting(self):
        ok=route("SNS画像を作って", manual_medium="display-copy")
        self.assertEqual(ok["adapter"],"social-static")
        bad=route("SNS画像を作って", manual_medium="presentation")
        self.assertTrue(bad["needs_confirmation"])

    def test_unknown_media_not_assumed(self):
        a=route("デザインをよろしく")
        self.assertEqual(a["status"],"needs-clarification")
        self.assertIsNone(a["medium"])

    def test_no_forced_language_conversion(self):
        a=route("日本語と韓国語のポスターを作って")
        self.assertIsNone(a["locale"])
        self.assertTrue(any("Mixed/ambiguous locale" in x for x in a["limitations"]))
        b=route("日本語と韓国語のポスターを作って", locale="ko-KR")
        self.assertEqual(b["locale"],"ko-KR")
        self.assertFalse(any("Mixed/ambiguous locale" in x for x in b["limitations"]))

    def test_valid_workflow_modes_do_not_grant_edit_authority(self):
        for mode in module.MODES:
            a=route("新製品のランディングページ", mode=mode)
            self.assertTrue(any("no editing" in x for x in a["limitations"]))

    def test_reference_catalog_and_profiles_intact(self):
        data=json.loads(SPEC_PATH.read_text(encoding="utf-8"))
        self.assertEqual(len(data["primary_profiles"]),6)
        self.assertEqual(len(data["adapters"]),6)
        catalog=json.loads((SKILL/"rules/catalog.json").read_text())
        self.assertEqual(len(catalog),39)
        self.assertEqual(len({x["id"] for x in catalog}),39)
        self.assertEqual(set(data["primary_profiles"]),{p.stem for p in (SKILL/"profiles").glob("*.json")})

    def test_original_design_contract_and_report_not_extended(self):
        c=json.loads((SKILL/"schemas/design-contract.schema.json").read_text())
        r=json.loads((SKILL/"schemas/report.schema.json").read_text())
        self.assertFalse(c["additionalProperties"])
        self.assertFalse(r["additionalProperties"])
        self.assertNotIn("review_intensity",c["properties"])
        self.assertNotIn("adapter",r["properties"])

    def test_cli_outputs_json_and_no_quality_pass(self):
        p=subprocess.run([sys.executable,str(SELECTOR),"--brief","Instagram用の広告画像を作って"],capture_output=True,text=True,check=True)
        data=json.loads(p.stdout)
        self.assertEqual(data["adapter"],"social-static")
        self.assertFalse(data["prior_strict_policy_verified"])
        self.assertNotIn("quality_score",data)
        self.assertNotIn("passed",data)

    def test_distribution_archives_exclude_python_bytecode(self):
        import zipfile
        zips = sorted(p for folder in ('downloads GPT-Codex', 'downloads Claude', 'downloads Gemini')
                      for p in (ROOT / folder).rglob('*.zip'))
        self.assertEqual(len(zips), 15)
        for path in zips:
            with zipfile.ZipFile(path) as z:
                self.assertFalse(any('__pycache__' in x or x.endswith('.pyc') for x in z.namelist()), path)
                self.assertTrue(any(x.endswith('scripts/use_case_selector.py') for x in z.namelist()), path)

    def test_script_data_standalone_relative_paths(self):
        data=json.loads(SPEC_PATH.read_text())
        self.assertEqual(data["source_decision"],"KUMI-USECASE-ADAPTER-SELECTION-20261019-01")
        self.assertEqual(SELECTOR.parent.parent,SKILL)


if __name__=="__main__":
    unittest.main()
