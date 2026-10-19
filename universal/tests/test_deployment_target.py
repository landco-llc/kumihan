#!/usr/bin/env python3
"""Ensure the designated production hostname is recorded without treating it as live."""
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "universal" / "deployment" / "target.json"

class DeploymentTargetTests(unittest.TestCase):
    def test_deployment_target_is_planned_not_live(self):
        d = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(d["schema_version"], "1.0")
        self.assertEqual(d["hostname"], "mcp-kmhn.landco.co.jp")
        self.assertEqual(d["endpoint"], "https://" + d["hostname"] + "/mcp")
        self.assertEqual(d["status"], "tls_verified_pending_mcp_deployment")
        self.assertEqual(d["provisioning"]["verification_type"], "owner_report_plus_independent_github_tls_probe")
        self.assertTrue(d["provisioning"]["subdomain_created"])
        self.assertTrue(d["provisioning"]["ssl_configured"])
        gates = d["flags"]
        self.assertTrue(gates["subdomain_created"])
        self.assertTrue(gates["ssl_configured_owner_reported"])
        self.assertTrue(gates["ssl_verified"])
        self.assertTrue(gates["dns_verified"])
        self.assertFalse(gates["php85_verified_on_target"])
        self.assertFalse(gates["host_end_to_end_verified"])
        self.assertFalse(gates["host_end_to_end_verified"])
        self.assertFalse(gates["public_release_authorized"])

    def test_production_template_matches_target_and_local_example_is_local(self):
        d = json.loads(MANIFEST.read_text(encoding="utf-8"))
        p = ROOT / d["runtime_config_template"]
        template = p.read_text(encoding="utf-8")
        self.assertIn("'host' => '" + d["hostname"] + "'", template)
        self.assertIn("NOT yet provisioned", template)
        local = (ROOT / "universal" / "server" / "runtime" / "config.example.php").read_text(encoding="utf-8")
        self.assertIn("'host' => '127.0.0.1'", local)
        self.assertNotIn(d["hostname"], local)

    def test_runbook_uses_exact_target(self):
        d = json.loads(MANIFEST.read_text(encoding="utf-8"))
        guide = (ROOT / "universal" / "LOLLIPOP_SETUP.md").read_text(encoding="utf-8")
        self.assertIn(d["endpoint"], guide)
        self.assertIn("PUBLIC DNS+TLS VERIFIED", guide)

if __name__ == "__main__":
    unittest.main()
