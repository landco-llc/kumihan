"""Exact Grafía v0.1.1 source-byte admission; historical ZIPs remain frozen."""
import hashlib
import json
from pathlib import Path
import re

CONTRACT = 'tests/contracts/grafia-v011-source-transition.json'
CONTRACT_SHA = '427c4708e778c5c27212b35de844f028b10b057629b2d5ffd0663690385d10d9'
FROZEN_INPUTS = ('tests/contracts/release-preservation.json',)


def load(root):
    try:
        root = Path(root)
        raw = (root/CONTRACT).read_bytes()
        if hashlib.sha256(raw).hexdigest() != CONTRACT_SHA:
            return None
        data = json.loads(raw)
        if data.get('scope') != 'grafia-v011-source-only' or set(data['frozen_inputs']) != set(FROZEN_INPUTS):
            return None
        for path, expected in data['frozen_inputs'].items():
            if hashlib.sha256((root/path).read_bytes()).hexdigest() != expected:
                return None
        return data
    except (OSError, ValueError, KeyError, TypeError):
        return None


def allowed(path, family, root, expected_preimage=None):
    if family == 'protected':
        if path != 'README.md' and (not path.startswith('plugins/kumihan-grafia/') or path.endswith('.zip')):
            return False
    elif family == 'bodies':
        if not re.fullmatch(r'(?:kumihan-es|docs/install-grafia-(?:chatgpt|claude|gemini))(?:\.en|\.ja)?\.html', path):
            return False
    else:
        return False
    data = load(root)
    if data is None:
        return False
    row = data.get('changes', {}).get(family, {}).get(path)
    if row is None or path.endswith('.zip'):
        return False
    if expected_preimage is not None and expected_preimage != row['snapshot_before']:
        return False
    try:
        raw = (Path(root)/path).read_bytes()
        if family == 'bodies':
            body = re.search(rb'<body\b[\s\S]*', raw, re.I)
            raw = body[0] if body else b''
        return hashlib.sha256(raw).hexdigest() == row['after']
    except OSError:
        return False


def predecessor_readme(raw, root):
    """Recover only the exact previous ES source cell for historical checks."""
    data = load(root)
    if data is None: raise ValueError('Changed Grafía source admission')
    row = data['readme']
    if hashlib.sha256(raw).hexdigest() not in (row['before_sha256'], row['after_sha256']):
        try:
            from grafia_v011_published_transition import predecessor_readme as published_predecessor
            raw = published_predecessor(raw, root)
        except (ImportError, OSError, ValueError, KeyError, TypeError) as error:
            raise ValueError('Unrecognized Grafía README successor') from error
    if hashlib.sha256(raw).hexdigest() == row['before_sha256']: return raw
    if hashlib.sha256(raw).hexdigest() != row['after_sha256']: raise ValueError('Changed current README')
    before, after = row['before_line'].encode(), row['after_line'].encode()
    if raw.count(after) != 1 or after != before.replace(b'| v0.1.0 |', b'| v0.1.1 |', 1):
        raise ValueError('Changed ES source cell')
    previous = raw.replace(after, before, 1)
    if hashlib.sha256(previous).hexdigest() != row['before_sha256']: raise ValueError('Changed predecessor README')
    return previous


def predecessor_facts(raw, root):
    """Recover exact preceding facts; changes outside ES are rejected."""
    data = load(root)
    if data is None: raise ValueError('Changed Grafía source admission')
    row = data['facts']
    if hashlib.sha256(raw).hexdigest() not in (row['before_sha256'], row['after_sha256']):
        try:
            from grafia_v011_published_transition import predecessor_facts as published_predecessor
            raw = published_predecessor(raw, root)
        except (ImportError, OSError, ValueError, KeyError, TypeError) as error:
            raise ValueError('Unrecognized Grafía facts successor') from error
    if hashlib.sha256(raw).hexdigest() == row['before_sha256']: return raw
    if hashlib.sha256(raw).hexdigest() != row['after_sha256']: raise ValueError('Changed current edition facts')
    facts = json.loads(raw)
    before, after = row['before_es'], row['after_es']
    expected = dict(before, source_version='0.1.1')
    if before['source_version'] != '0.1.0' or after != expected or facts['editions']['es'] != after:
        raise ValueError('Changed ES source-only facts')
    facts['editions']['es'] = before
    previous = (json.dumps(facts, ensure_ascii=False, indent=2)+'\n').encode()
    if hashlib.sha256(previous).hexdigest() != row['before_sha256']: raise ValueError('Changed predecessor edition facts')
    return previous
