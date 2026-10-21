#!/usr/bin/env python3
"""Generate the three static, translated ZiLu landings; no runtime translation or JS.

Install guides come from build_install_guides.py.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from seo_adapter import seo_outputs
from version_display import version_outputs
import argparse
ROOT=Path(__file__).resolve().parents[1]
SUFFIXES=('','.en','.ja')

def name(suffix):return f'kumihan-zh-cn{suffix}.html'
def landing(suffix):
 # Every landing is authored with the KUMIHAN index hierarchy (see templates/).
 # Templates are the source of truth so --check verifies generated output.
 name={'':'zh','.en':'en','.ja':'ja'}[suffix]
 return (ROOT/'templates'/f'zilu-{name}-landing.html').read_text(encoding='utf-8')

@version_outputs
@seo_outputs
def outputs():return {name(s):landing(s) for s in SUFFIXES}
def main():
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args();out=outputs();changed=[n for n,b in out.items() if not (ROOT/n).exists() or (ROOT/n).read_text()!=b]
 if a.check:
  for n in changed:print('out of date: '+n)
  return int(bool(changed))
 for n in changed:(ROOT/n).write_text(out[n])
 print('Generated 3 ZiLu landings');return 0
if __name__=='__main__':raise SystemExit(main())
