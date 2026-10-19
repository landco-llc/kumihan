import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
class Site(unittest.TestCase):
    def test_copy_and_terminology(self):
        d=json.loads((ROOT/"assets/lad-site-copy.json").read_text(encoding="utf-8"))
        self.assertEqual(set(d),{"ru","en","ja"})
        for key in d:
            copy=d[key]
            self.assertIn("KUMIHAN｜Лад",copy["title"])
            self.assertEqual(len(copy["features"]),4)
            self.assertEqual(len(copy["skills"]),4)
            self.assertEqual(len(copy["guide"]["sections"]),6)
            self.assertNotIn("Compasso",json.dumps(copy,ensure_ascii=False))
            self.assertNotIn("Portuguese",json.dumps(copy,ensure_ascii=False))
        self.assertTrue(d["en"]["h1"][0].startswith("Natural Russian"))
        self.assertIn("ロシア語",d["ja"]["h1"][0])
    def test_generated_canonical_files(self):
        files=(["kumihan-ru.html","kumihan-ru.en.html","kumihan-ru.ja.html","assets/lad-site.css"]
        +[f"docs/install-lad-{host}{suffix}.html" for host in ("chatgpt","claude","gemini") for suffix in ("",".en",".ja")])
        for path in files:
            text=(ROOT/path).read_text(encoding="utf-8")
            self.assertIn("KUMIHAN",text)
            self.assertIn("Лад",text) if not path.endswith(".css") else None
        self.assertEqual(len(files),13)
        self.assertIn("lang=\"ru\"",(ROOT/"kumihan-ru.html").read_text(encoding="utf-8"))
        self.assertIn("lang=\"en\"",(ROOT/"kumihan-ru.en.html").read_text(encoding="utf-8"))
        self.assertIn("lang=\"ja\"",(ROOT/"kumihan-ru.ja.html").read_text(encoding="utf-8"))
        css=(ROOT/"assets/lad-site.css").read_text(encoding="utf-8")
        self.assertIn("html[lang=\"ru\"]",css)
if __name__=="__main__": unittest.main()
