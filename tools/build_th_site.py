#!/usr/bin/env python3
"""Build independent Thai product pages; --check verifies committed output.

Build the committed Thai landings; install guides come from build_install_guides.py.
"""
from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec

_index_spec = spec_from_file_location("kumihan_th_japanese_index", Path(__file__).with_name("build_th_ja_index.py"))
_index_module = module_from_spec(_index_spec)
_index_spec.loader.exec_module(_index_module)
render_th_japanese_index = _index_module.render
_th_index_spec = spec_from_file_location("kumihan_th_thai_index", Path(__file__).with_name("build_th_th_index.py"))
_th_index_module = module_from_spec(_th_index_spec)
_th_index_spec.loader.exec_module(_th_index_module)
render_th_thai_index = _th_index_module.render
_en_index_spec = spec_from_file_location("kumihan_th_english_index", Path(__file__).with_name("build_th_en_index.py"))
_en_index_module = module_from_spec(_en_index_spec)
_en_index_spec.loader.exec_module(_en_index_module)
render_th_english_index = _en_index_module.render
import argparse
import json

ROOT = Path(__file__).resolve().parents[1]
HOSTS = {'chatgpt':'ChatGPT / Codex', 'claude':'Claude', 'gemini':'Gemini'}
COPY = json.loads((ROOT/'assets/thai-site-copy.json').read_text())

def home(lang): return 'kumihan-th' + ('' if lang=='th' else '-'+lang) + '.html'
def guide(host,lang): return 'docs/install-kumihan-th-'+host+('' if lang=='th' else '.'+lang)+'.html'

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from seo_metadata import enrich_html
from version_display import apply_html

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
 index={'th':render_th_thai_index,'en':render_th_english_index,'ja':render_th_japanese_index}
 files={home(l):index[l](ROOT, COPY[l]) for l in COPY}
 stale=[]
 for name,content in files.items():
  content=apply_html(enrich_html(content,name),name)
  path=ROOT/name
  if args.check:
   if not path.exists() or path.read_text()!=content:stale.append(name)
  else:path.write_text(content)
 if stale:raise SystemExit('Stale Thai site pages: '+', '.join(stale))
 print(f'Thai site: {len(files)} pages '+('verified' if args.check else 'built'))
if __name__=='__main__':main()
