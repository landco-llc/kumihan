"""Original synthetic catalog fixtures exercise coordinated data interfaces."""
import copy
import importlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from test_report import rule


def structural_root(root):
    shutil.copytree(ROOT / "schemas", root / "schemas")
    schema = json.loads((ROOT / "schemas/rule.schema.json").read_text())
    rules = []
    for identity in schema["$defs"]["rule_id"]["enum"]:
        item = rule(); item["id"] = identity; item["media"] = schema["$defs"]["media_profile"]["enum"]
        rules.append(item)
    (root / "rules").mkdir(); (root / "rules/catalog.json").write_text(json.dumps(rules))
    (root / "profiles").mkdir()
    for identity in schema["$defs"]["media_profile"]["enum"]:
        (root / f"profiles/{identity}.json").write_text(json.dumps({"id": identity, "revision": 1,
            "title": "Synthetic profile", "description": "Original synthetic selection.",
            "rule_ids": [item["id"] for item in rules], "guidance": ["Observe supplied original text."]}))
    return rules


def registry(rules):
    """Original fixture matching the coordinated W02 registry envelope."""
    return {"registry_version": "0.1.0", "sources": [{"id": "policy:synthetic", "type": "project-policy",
        "classification": "adopted", "title": "Original synthetic policy", "url": None,
        "version": "Synthetic policy revision 1", "accessed_at": "2026-10-13",
        "context": "Authored statement in this registry entry.", "adopted_principle": "Preserve supplied original text.",
        "limits": "Structural fixture only; no external authority claim.",
        "statement": "Compare the supplied original text within the declared scope.",
        "rule_ids": [value["id"] for value in rules]}]}


PRIORITY = ("CONTENT-001", "CONTENT-002", "CONTENT-004", "JA-TYPE-002", "JA-TYPE-004", "JA-TYPE-005", "JA-TYPE-006", "JA-TYPE-008", "JA-TYPE-009", "WEB-001", "WEB-004", "WEB-005", "DESIGN-001", "DESIGN-002", "EVIDENCE-001")


def complete_root(root):
    rules = structural_root(root)
    cases = []
    for item in rules:
        if item["id"] not in PRIORITY:
            continue
        for kind in ("positive", "negative", "exception"):
            identity = item["id"] + "-" + kind
            item["case_ids"].append(identity)
            observed = "合成例：価格120円・単位cm" if kind == "positive" else "合成差：価格121円・単位mm"
            fixture = {"original_text": "合成例：価格120円・単位cm", "observed_text": observed}
            if kind == "exception":
                fixture["exception_request"] = {"scope": "whole", "reason": "Original synthetic bounded request.", "approval_ref": "synthetic-unverified"}
            cases.append({"id": identity, "rule_id": item["id"], "kind": kind,
                "profile": "web-editorial", "input": fixture,
                "expected_status": {"positive": "passed", "negative": "failed", "exception": "needs-review"}[kind],
                "method": "manual", "assertions": ["Compare supplied original sequences; a request is not approval."],
                "assertion_types": ["fixture-content"], "limitations": ["Original structural fixture; no real approval or visual-quality evidence."]})
    (root / "rules/catalog.json").write_text(json.dumps(rules))
    (root / "sources").mkdir()
    (root / "sources/public-sources.json").write_text(json.dumps(registry(rules)))
    path = root / "tests/fixtures"; path.mkdir(parents=True)
    (path / "priority-cases.json").write_text(json.dumps({"fixture_version": "0.1.0", "cases": cases}))
    return rules


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.module = importlib.import_module("scripts.validate_catalog")
        if not hasattr(self.module, "load_catalog"):
            self.fail("Frozen load_catalog callable is not implemented")
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name); self.rules = structural_root(self.root)

    def write_rules(self, values):
        (self.root / "rules/catalog.json").write_text(json.dumps(values))

    def test_structural_order_is_frozen_family_numeric_order(self):
        self.write_rules(list(reversed(self.rules)))
        actual, _ = self.module.rule_profile_data(self.root)
        self.assertEqual([r["id"] for r in actual], [r["id"] for r in self.rules])
        self.assertEqual(len(actual), 38)

    def test_coordinated_registry_shape_and_unresolved_sources(self):
        value = registry(self.rules)
        checks = self.module.validators(self.root)
        self.assertEqual(self.module.source_errors(value, self.rules, checks), [])
        for change, diagnostic in [("missing", "unresolved source"), ("duplicate", "duplicate source"),
                                   ("deferred", "non-adopted source"), ("blank", "source schema"),
                                   ("wrong-kind", "declared source kind")]:
            changed = copy.deepcopy(value)
            if change == "missing": changed["sources"] = []
            elif change == "duplicate": changed["sources"].append(copy.deepcopy(changed["sources"][0]))
            elif change == "deferred": changed["sources"][0]["classification"] = "deferred"
            elif change == "blank": changed["sources"][0]["statement"] = " "
            elif change == "wrong-kind": changed["sources"][0]["type"] = "expert-practice"
            with self.subTest(change=change):
                self.assertIn(diagnostic, " ".join(self.module.source_errors(changed, self.rules, checks)))

    def test_duplicate_missing_and_extra_rules(self):
        for items, diagnostic in [(self.rules + [self.rules[0]], "duplicate rule ID"),
                                  (self.rules[1:], "missing rule IDs"),
                                  (self.rules + [{**self.rules[0], "id": "EXTRA-001"}], "schema violation")]:
            self.write_rules(items)
            with self.subTest(diagnostic=diagnostic), self.assertRaisesRegex(ValueError, diagnostic):
                self.module.load_catalog(self.root)

    def test_profile_references_and_missing_profiles(self):
        path = self.root / "profiles/web-editorial.json"
        value = json.loads(path.read_text()); value["rule_ids"] = ["EXTRA-001"]
        path.write_text(json.dumps(value))
        with self.assertRaisesRegex(ValueError, "schema violation"):
            self.module.load_catalog(self.root)
        path.unlink()
        with self.assertRaisesRegex(ValueError, "missing profile IDs"):
            self.module.load_catalog(self.root)

    def test_honest_coverage_retains_other_rules_and_rejects_unverified_implementation(self):
        for coverage in ["planned", "unsupported", "guidance-only"]:
            self.rules[0]["verification"]["coverage"] = coverage; self.write_rules(self.rules)
            values, _ = self.module.rule_profile_data(self.root)
            self.assertEqual(len(values), 38)
        self.rules[0]["verification"]["coverage"] = "implemented"; self.write_rules(self.rules)
        with self.assertRaisesRegex(ValueError, "implemented coverage lacks verified procedure/tests"):
            self.module.load_catalog(self.root)

    def test_missing_sources_and_cases_are_not_fabricated(self):
        with self.assertRaisesRegex(ValueError, "missing source registry"):
            self.module.load_catalog(self.root)
        (self.root / "sources").mkdir()
        (self.root / "sources/public-sources.json").write_text(json.dumps(registry(self.rules)))
        with self.assertRaisesRegex(ValueError, "missing priority cases"):
            self.module.load_catalog(self.root)

    def test_complete_catalog_with_original_priority_triads(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); rules = complete_root(root)
            actual = self.module.load_catalog(root)
            self.assertEqual(actual, rules)
            self.assertEqual(len(actual), 38)
            self.assertEqual(sum(len(r["case_ids"]) for r in actual), 45)

    def test_priority_triads_labels_and_case_references(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); rules = complete_root(root)
            path = root / "tests/fixtures/priority-cases.json"
            original = json.loads(path.read_text())
            variants = []
            missing = copy.deepcopy(original); missing["cases"].pop(); variants.append((missing, "incomplete priority triad"))
            duplicate = copy.deepcopy(original); duplicate["cases"].append(duplicate["cases"][0]); variants.append((duplicate, "duplicate case ID"))
            wrong = copy.deepcopy(original); wrong["cases"][0]["rule_id"] = "CONTENT-005"; variants.append((wrong, "case rule binding"))
            wrong = copy.deepcopy(original); wrong["cases"][0]["method"] = "static"; variants.append((wrong, "case method mismatch"))
            for field, replacement in [("assertion_types", ["automatic-render"]), ("assertions", [" "]), ("input", "external-path"), ("expected_status", "PASS"), ("extra", True)]:
                wrong = copy.deepcopy(original); wrong["cases"][0][field] = replacement; variants.append((wrong, "case schema"))
            for dataset, diagnostic in variants:
                path.write_text(json.dumps(dataset))
                with self.subTest(diagnostic=diagnostic), self.assertRaisesRegex(ValueError, diagnostic):
                    self.module.load_catalog(root)
            path.write_text(json.dumps(original))
            rules[0]["case_ids"].append("missing-case")
            (root / "rules/catalog.json").write_text(json.dumps(rules))
            with self.assertRaisesRegex(ValueError, "unresolved case reference"):
                self.module.load_catalog(root)


    def test_each_assertion_has_its_own_label(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); complete_root(root)
            path = root / "tests/fixtures/priority-cases.json"
            dataset = json.loads(path.read_text())
            case = dataset["cases"][0]
            case["assertions"].append("The case record has the required fields.")
            case["assertion_types"] = ["fixture-content", "schema"]
            path.write_text(json.dumps(dataset))
            self.assertEqual(len(self.module.load_catalog(root)), 38)
            for labels in [[], ["fixture-content"], ["fixture-content", "schema", "assisted"]]:
                case["assertion_types"] = labels
                path.write_text(json.dumps(dataset))
                with self.subTest(labels=labels), self.assertRaisesRegex(ValueError, "assertion label"):
                    self.module.load_catalog(root)
            case["assertion_types"] = ["manual-render", "assisted"]
            path.write_text(json.dumps(dataset))
            self.assertEqual(len(self.module.load_catalog(root)), 38)
            del case["assertion_types"]
            path.write_text(json.dumps(dataset))
            with self.assertRaisesRegex(ValueError, "case schema"):
                self.module.load_catalog(root)

    def test_public_loader_resolves_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); complete_root(root)
            path = root / "sources/public-sources.json"
            data = json.loads(path.read_text()); data["sources"] = []
            path.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, "unresolved source"):
                self.module.load_catalog(root)

    def test_malformed_public_url_has_sanitized_diagnostics(self):
        value = registry(self.rules)
        extra = copy.deepcopy(value["sources"][0])
        extra.update(id="SYNTHETIC", type="expert-practice", classification="deferred",
                     url="https://[UNTRUSTED-CONTROL]/", version=None, accessed_at=None,
                     adopted_principle=None, statement=None, rule_ids=[])
        value["sources"].append(extra)
        errors = self.module.source_errors(value, self.rules, self.module.validators(self.root))
        self.assertTrue(errors)
        self.assertNotIn("UNTRUSTED-CONTROL", " ".join(errors))

    def test_private_source_urls_are_not_public_references(self):
        for url in ["http://10.0.0.1/reference", "http://192.168.1.1/reference", "https://source.internal/reference"]:
            value = registry(self.rules); extra = copy.deepcopy(value["sources"][0])
            extra.update(id="SYNTHETIC", type="expert-practice", classification="deferred", url=url,
                         version=None, accessed_at=None, adopted_principle=None, statement=None, rule_ids=[])
            value["sources"].append(extra)
            with self.subTest(url=url):
                self.assertTrue(self.module.source_errors(value, self.rules, self.module.validators(self.root)))

    def test_arbitrary_schemas_duplicate_json_and_symlinks_rejected(self):
        schema = self.root / "schemas/rule.schema.json"
        original = schema.read_bytes()
        schema.write_text('{"$ref":"https://invalid.example/remote-schema"}')
        with self.assertRaisesRegex(ValueError, "local schemas"):
            self.module.load_catalog(self.root)
        schema.write_bytes(original)
        path = self.root / "rules/catalog.json"
        path.write_text('[{"id":"CONTENT-001","id":"CONTENT-002"}]')
        with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
            self.module.load_catalog(self.root)
        path.unlink(); path.symlink_to(self.root / "schemas/rule.schema.json")
        with self.assertRaisesRegex(ValueError, "symlink"):
            self.module.load_catalog(self.root)

    def test_schema_required_fields_and_unknown_fields(self):
        checks = self.module.validators(self.root)
        for value, name in [(self.rules[0], "rule"), (json.loads((self.root / "profiles/web-ui.json").read_text()), "profile")]:
            self.assertEqual(self.module.schema_errors(checks[name], value, name), [])
            for key in value:
                missing = copy.deepcopy(value); del missing[key]
                self.assertTrue(self.module.schema_errors(checks[name], missing, name), key)
            extra = {**value, "unknown": "synthetic"}
            self.assertTrue(self.module.schema_errors(checks[name], extra, name))


if __name__ == "__main__":
    unittest.main()
