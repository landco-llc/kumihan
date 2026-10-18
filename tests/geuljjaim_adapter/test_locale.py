"""Korean adapter must not redirect existing Japanese/Chinese contexts."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools'))
from locale_resolver import resolve_context

class KoreanContext(unittest.TestCase):
    def test_korean_explicit_context(self):
        self.assertEqual(resolve_context('ko-KR','web-marketing'),dict(locale='ko-KR',language='ko',script='Hang',region='KR',medium='web-marketing'))
    def test_korean_region_not_inferred(self):
        for tag in ['ko','ko-KP','kr','한국어',None]:
            with self.subTest(tag=tag), self.assertRaises(ValueError): resolve_context(tag,'web-ui')
