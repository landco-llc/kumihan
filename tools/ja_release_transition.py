"""Exact Japanese source transition; original preservation hashes stay immutable."""
import hashlib
import json
from pathlib import Path

RECORD = 'tests/contracts/ja-v020-transition.json'
HOSTS = ('downloads Claude', 'downloads GPT-Codex', 'downloads Gemini')
SKILLS = ('kumihan', 'kumihan-web', 'kumihan-documents', 'kumihan-review')
CHANGED = ('SKILL.md', 'inventory.json', 'references/web-recipes.md',
           'references/document-recipes.md', 'references/review-protocol.md')


def allowed(path):
    return path in {'plugin.json', '.codex-plugin/plugin.json',
                    '.claude-plugin/plugin.json', 'gemini-extension.json', 'README.md'} | {
        f'skills/{skill}/{name}' for skill in SKILLS for name in CHANGED
    } | {f'{host}/{name}' for host in HOSTS for name in ('MANIFEST.json', 'SHA256SUMS.txt', 'README.md')}


def admitted(root, path, before):
    root = Path(root)
    record = root / RECORD
    if not allowed(path) or not record.is_file() or not (root / path).is_file():
        return False
    row = json.loads(record.read_text())['paths'].get(path, {})
    return row.get('before') == before and row.get('after') == hashlib.sha256((root / path).read_bytes()).hexdigest()
