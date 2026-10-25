import importlib.util
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
loc=ROOT/"plugins/kumihan-accord/runtime/checks.py"
spec=importlib.util.spec_from_file_location("accord",loc)
mod=importlib.util.module_from_spec(spec)
sys.modules["accord"]=mod
spec.loader.exec_module(mod)

class TestAccord(unittest.TestCase):
    def test_fr_fr_candidate(self):
        self.assertEqual(len(mod.inspect("Bonjour! Vous venez?","fr-FR","fr-fr-editorial")["findings"]),2)
    def test_fr_fr_correct(self):
        self.assertEqual(mod.inspect("Bonjour\u202f! Vous venez\u202f?","fr-FR","fr-fr-editorial")["findings"],[])
    def test_ca_zero_space(self):
        self.assertEqual(mod.inspect("Bonjour! Venez? Oui;","fr-CA","fr-ca-oqlf")["findings"],[])
    def test_ca_colon(self):
        self.assertEqual(len(mod.inspect("Sujet: réponse","fr-CA","fr-ca-oqlf")["findings"]),1)
    def test_eu_zero(self):
        self.assertEqual(len(mod.inspect("Bonjour\u202f! Oui\u00a0:","fr-FR","eu-interinstitutional")["findings"]),2)
    def test_no_style(self):
        self.assertEqual(mod.inspect("Bonjour!")["house_style_status"],"unresolved")
    def test_be(self):
        self.assertEqual(mod.inspect("Bonjour!","fr-BE")["findings"],[])
    def test_ch(self):
        self.assertEqual(mod.inspect("Bonjour!","fr-CH")["findings"],[])
    def test_bad_locale(self):
        with self.assertRaises(ValueError):mod.inspect("Bonjour!","fr-XX")
    def test_bad_style(self):
        with self.assertRaises(ValueError):mod.inspect("Bonjour!","fr-FR","other")
    def test_preserve_exact(self):
        self.assertEqual(mod.inspect("Été œ Œ\u202f!",candidate="Été œ Œ\u202f!")["preservation"]["status"],"passed")
    def test_preserve_diff(self):
        self.assertEqual(mod.inspect("A\u00a0:",candidate="A :")["preservation"]["status"],"failed")
    def test_protect_url(self):
        self.assertEqual(len(mod.inspect("https://example.fr/x?p=1 Bonjour!","fr-FR","fr-fr-editorial")["findings"]),1)
    def test_protect_html(self):
        self.assertEqual(len(mod.inspect("<div title='Bonjour!'>Oui!</div>","fr-FR","fr-fr-editorial")["findings"]),1)
    def test_quotes_candidate(self):
        self.assertEqual(len(mod.inspect("«bonjour»","fr-FR","fr-fr-editorial")["findings"]),1)
    def test_quotes_correct(self):
        self.assertEqual(mod.inspect("«\u202fbonjour\u202f»","fr-FR","fr-fr-editorial")["findings"],[])
    def test_quotes_eu(self):
        self.assertEqual(mod.inspect("«bonjour»","fr-FR","eu-interinstitutional")["findings"],[])
    def test_generated_fr(self):
        self.assertEqual(mod.propose_generated_plain("Bonjour! Vous venez? «salut»","fr-fr-editorial"),"Bonjour\u202f! Vous venez\u202f? «\u202fsalut\u202f»")
    def test_generated_ca(self):
        self.assertEqual(mod.propose_generated_plain("Bonjour! Sujet: «salut»","fr-ca-oqlf"),"Bonjour! Sujet\u00a0: «\u00a0salut\u00a0»")
    def test_generated_eu(self):
        self.assertEqual(mod.propose_generated_plain("Oui\u202f! Sujet\u00a0: «\u202fbonjour\u202f»","eu-interinstitutional"),"Oui! Sujet: «bonjour»")
    def test_structured_rejected(self):
        for s in ("https://example.fr","<em>Bonjour!</em>","Bonjour!\nSalut?"):
            with self.subTest(text=s):
                with self.assertRaises(ValueError):mod.propose_generated_plain(s,"fr-fr-editorial")
    def test_requires_style(self):
        with self.assertRaises(ValueError):mod.propose_generated_plain("Bonjour!","unknown")
    def test_no_mutation(self):
        s="Été!"
        mod.inspect(s,"fr-FR","fr-fr-editorial")
        self.assertEqual(s,"Été!")
class TestAccordIcons(unittest.TestCase):
    def test_logo_dimensions(self):
        import struct
        logo = ROOT / "plugins/kumihan-accord/assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png"
        data = logo.read_bytes()
        self.assertTrue(data.startswith(bytes.fromhex("89504e470d0a1a0a")))
        self.assertLess(len(data), 5 * 1024 * 1024)
        self.assertEqual(data[12:16], b"IHDR")
        width, height = struct.unpack(">II", data[16:24])
        self.assertEqual(width, height)
        self.assertGreaterEqual(width, 48)
        self.assertLessEqual(width, 4096)

    def test_icon_paths_and_skill_assets(self):
        import hashlib
        import json
        plugin = ROOT / "plugins/kumihan-accord"
        logo = "KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png"
        master = (plugin / "assets" / logo).read_bytes()
        for sid in ("kumihan-accord", "kumihan-accord-web", "kumihan-accord-documents", "kumihan-accord-review"):
            with self.subTest(skill=sid):
                path = plugin / "skills" / sid
                meta = (path / "agents" / "openai.yaml").read_text(encoding="utf-8")
                self.assertIn("display_name:", meta)
                self.assertIn('icon_small: "./assets/' + logo + '"', meta)
                self.assertIn('icon_large: "./assets/' + logo + '"', meta)
                self.assertEqual(hashlib.sha256((path / "assets" / logo).read_bytes()).digest(), hashlib.sha256(master).digest())
        openai = json.loads((plugin / "plugin.json").read_text(encoding="utf-8"))
        overlay = json.loads((plugin / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        for ui in (openai["extensions"]["com.openai"]["interface"], overlay["interface"]):
            self.assertEqual(ui["displayName"], "KUMIHAN｜Accord")
            self.assertEqual(ui["logo"], "./assets/" + logo)
            self.assertEqual(ui["composerIcon"], "./assets/" + logo)

    def test_host_manifest_versions(self):
        import json
        plugin = ROOT / "plugins/kumihan-accord"
        for name in ("plugin.json", ".codex-plugin/plugin.json", ".claude-plugin/plugin.json", "gemini-extension.json"):
            with self.subTest(manifest=name):
                d = json.loads((plugin / name).read_text(encoding="utf-8"))
                self.assertEqual(d["version"], "0.1.2")
                self.assertEqual(d["name"], "kumihan-accord")
        claude = json.loads((plugin / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(claude["icon"], "./assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png")


if __name__=="__main__":unittest.main()
