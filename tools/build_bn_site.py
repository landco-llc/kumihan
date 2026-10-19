#!/usr/bin/env python3
"""Build Bengali static pages from paired authored templates; --check is read-only."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from seo_adapter import seo_outputs
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


@seo_outputs
def outputs():
    base = ROOT / 'templates/bn'
    return {p.relative_to(base).as_posix(): p.read_text(encoding='utf-8')
            for p in sorted(base.rglob('*.html'))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    stale = []
    files = outputs()
    for name, content in files.items():
        path = ROOT / name
        if args.check:
            if not path.exists() or path.read_text(encoding='utf-8') != content:
                stale.append(name)
        else:
            path.write_text(content, encoding='utf-8')
    if stale:
        raise SystemExit('Stale Bengali pages: ' + ', '.join(stale))
    print(f'Bengali site: {len(files)} pages ' + ('verified' if args.check else 'built'))


if __name__ == '__main__':
    main()
