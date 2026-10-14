#!/usr/bin/env python3
"""Read-only public-boundary heuristic over EVERY tracked file and tracked path.

There are no fixture/content exemptions. Tests assemble synthetic negative values
at run time; tracked test source is scanned like all other UTF-8 text. Diagnostics
contain a category and ordinal only, never matched text or untrusted filenames.
Detects common credential forms, private storage locations/IDs, local home paths,
labelled customer data and raw conversation/log signatures. This is not exhaustive
DLP, ownership verification, or proof that every possible disclosure is absent.
Ordinary public citations are accepted. No target content is executed or imported.
"""
import argparse
import json
from pathlib import Path
import re
import stat
import subprocess
import sys

PATTERNS = {
    'credential': r'(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|sk-(?:proj-)?[A-Za-z0-9_-]{20,}|xox[baprs]-[A-Za-z0-9-]{16,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|(?:api[_-]?key|password|client_secret|access_token)\s*[:=]\s*[\'\"]?[A-Za-z0-9_/+.-]{12,})',
    'private-storage': r'(?:s3|gs|az)://[^\s\'\"<>]+|https?://(?:[^/\s]+\.)?(?:drive\.google\.com|docs\.google\.com|dropbox\.com|box\.com|sharepoint\.com|blob\.core\.windows\.net)/[^\s\'\"<>]+|[?&](?:X-Amz-Signature|X-Goog-Signature|access_token|sig)=|(?:private[_-]?storage[_-]?id|conversation[_-]?id|thread[_-]?id)\s*[:=]\s*[\'\"]?[A-Za-z0-9_-]{6,}',
    'local-private-path': r'(?:/(?:Users|home)/[A-Za-z0-9_.-]+/[^\s\'\"<>]+|[A-Za-z]:\\Users\\[A-Za-z0-9_.-]+\\[^\s\'\"<>]+|/(?:workspace|tmp)/[^\s\'\"<>]*(?:private|transcript|raw[-_]log)[^\s\'\"<>]*)',
    'customer-information': r'(?:customer|client)[_-]?(?:name|email|phone|address|id)\s*[:=]\s*[\'\"]?[A-Za-z0-9][^\n\'\"]{2,}|[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}|\b(?:\+\d{1,3}[- .])?\d{3}[- .]\d{3}[- .]\d{4}\b',
    'raw-conversation': r'(?:^|\n)\s*(?:user|assistant|system|developer)\s*:\s*[^\n]+\n\s*(?:user|assistant|system|developer)\s*:|"role"\s*:\s*"(?:user|assistant|system|developer)"|(?:^|\n)\d{4}-\d\d-\d\d[T ][0-9:.]+Z?\s+(?:DEBUG|INFO|ERROR)\s+',
}


def check_text(text):
    for category, pattern in PATTERNS.items():
        if re.search(pattern, text, re.I):
            raise ValueError(category)


def check_repository(root):
    require_regular_root = not root.is_symlink() and root.is_dir()
    if not require_regular_root: raise ValueError('invalid-root')
    run = subprocess.run(['git','-C',str(root),'ls-files','--stage','-z'],
                         capture_output=True, check=True)
    count = 0
    for ordinal, item in enumerate(run.stdout.split(b'\0')):
        if not item: continue
        header, raw = item.split(b'\t', 1)
        mode, _, stage = header.split()
        # Gitlinks, executable-bit files, symlinks and merge stages are inadmissible.
        if mode != b'100644' or stage != b'0': raise ValueError('tracked-mode')
        name = raw.decode('utf-8', errors='strict')
        if any(part in ('', '.', '..') for part in name.split('/')): raise ValueError('tracked-path')
        if re.search(r'(?:^|/)(?:private|raw[-_]logs?|transcripts?)(?:/|\.|$)', name, re.I):
            raise ValueError('private-file-category')
        p = root
        for part in name.split('/'):
            p = p / part
            if p.is_symlink(): raise ValueError('tracked-symlink')
        if not stat.S_ISREG(p.lstat().st_mode): raise ValueError('tracked-nonregular')
        if p.stat().st_size > 2_000_000: raise ValueError('tracked-size-limit')
        try:
            check_text(name)
            check_text(p.read_bytes().decode('utf-8', errors='strict'))
        except (ValueError, UnicodeError):
            raise ValueError('public-boundary-rejected-file-' + str(ordinal)) from None
        count += 1
    if not count: raise ValueError('empty-tracked-set')
    return {'tracked_files': count, 'fixture_exemptions': 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        result = check_repository(args.root)
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        print(json.dumps({'status':'failed','code':'public-boundary-or-invalid-input','type':type(exc).__name__}))
        return 1
    print(json.dumps({'status':'passed', **result}, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
