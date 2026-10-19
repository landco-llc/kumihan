#!/usr/bin/env python3
"""Verify published Releases and atomically replace facts; no remote writes or site publishing."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import tempfile
from urllib.request import Request, urlopen
import edition_versions as v


def fetch(url):
    with urlopen(Request(url, headers={'User-Agent': 'kumihan-version-sync', 'Accept': 'application/vnd.github+json'}), timeout=90) as response:
        return response.read()


def releases():
    result = []
    for page in range(1, 11):
        batch = json.loads(fetch(f'https://api.github.com/repos/landco-llc/kumihan/releases?per_page=100&page={page}'))
        if not isinstance(batch, list): raise ValueError('Invalid Release API response')
        result.extend(batch)
        if len(batch) < 100: return result
    raise ValueError('Release pagination limit exceeded; snapshot unchanged')


def synchronize(current, published, fetcher=fetch, read_source=v.git_source):
    def one(item):
        code, spec = item
        old = dict(current['editions'][code], source_version=v.source_version(spec))
        return code, v.select_release(spec, old, published, fetcher, read_source)
    with ThreadPoolExecutor(max_workers=4) as pool:
        editions = dict(pool.map(one, v.catalogue().items()))
    return dict(schema_version=1, editions=editions)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='verify API/assets without writing')
    args = parser.parse_args()
    current = v.load()
    updated = synchronize(current, releases())
    content = json.dumps(updated, ensure_ascii=False, indent=2)+'\n'
    if args.check:
        if updated != current: raise SystemExit('Verified Release facts changed; run synchronization')
    elif updated != current:
        # Nothing is written until ALL edition/network/hash checks succeed.
        handle, name = tempfile.mkstemp(dir=v.FACTS.parent, prefix='.edition-versions-')
        try:
            with os.fdopen(handle, 'w', encoding='utf-8') as out: out.write(content)
            os.replace(name, v.FACTS)
        finally:
            Path(name).unlink(missing_ok=True)
    print('21 editions verified; '+('unchanged' if updated == current else 'updated'))


if __name__ == '__main__': main()
