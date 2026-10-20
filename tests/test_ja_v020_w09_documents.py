"""W09 bounded document safeguards; visual decisions remain evidence, not regex."""
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
class DocumentIsolation(unittest.TestCase):
    def test_output_requires_new_destination(self):
        source = (ROOT / 'tools/qa_documents_v020.py').read_text()
        self.assertIn("'--output-dir'", source)
        self.assertIn('refusing to overwrite', source)
    def test_local_lexical_groups_and_content(self):
        source = (ROOT / 'tools/qa_documents_v020.py').read_text()
        self.assertIn('def keep_phrase(', source)
        self.assertIn("('ありません。', '継続欄', 'しない。')", source)
        self.assertNotIn('table{white-space:nowrap', source)
if __name__ == '__main__': unittest.main()

class DocumentEvidence(unittest.TestCase):
    evidence = ROOT / 'docs/development/ja-v020-20261020/qa/w09/evidence'
    def test_report_source_and_all_pages(self):
        import json
        before = self.evidence / 'report/before'
        after = self.evidence / 'report/font-configured'
        self.assertEqual((before/'source.json').read_bytes(), (after/'source.json').read_bytes())
        data = json.loads((after/'source.json').read_text())
        self.assertEqual([r['id'] for r in data['table_rows']], [f'{i:02}' for i in range(1,45)])
        m = json.loads((after/'measurements.json').read_text())
        self.assertEqual(len(m['report']['pages']), 6)
        self.assertTrue(all(m['report']['protected_exact_substring_extraction'].values()))
        for page in m['report']['pages']:
            self.assertTrue((after/page['image']).is_file())
        # Browser DOM text saved before PDF export, without whitespace normalization.
        self.assertTrue(all(s in (after/'report-dom-text.txt').read_text() for s in data['protected']))
    def test_saved_slide_source_exact_and_extraction_scopes(self):
        import json, zipfile
        b = self.evidence/'presentation/before/presentation.pptx'
        a = self.evidence/'presentation/after/presentation.pptx'
        with zipfile.ZipFile(b) as before, zipfile.ZipFile(a) as after:
            self.assertIsNone(after.testzip())
            for i in range(1,9):
                path=f'ppt/slides/slide{i}.xml'
                self.assertEqual(before.read(path), after.read(path))
                self.assertTrue((self.evidence/f'presentation/after/presentation-{i:02}.png').is_file())
        observed=json.loads((self.evidence/'report/documents-observations.json').read_text())
        self.assertTrue(observed['source_html_text_codepoints_equal'])
        self.assertEqual(observed['presentation']['native_powerpoint'], 'NOT_CHECKED')
        self.assertEqual(observed['presentation']['actual_copy_paste'], 'NOT_CHECKED')
        self.assertTrue(all(observed['presentation']['after']['pymupdf_exact'].values()))
        self.assertTrue(all(observed['presentation']['after']['pypdf_exact'].values()))
