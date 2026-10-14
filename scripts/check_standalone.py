#!/usr/bin/env python3
"""Read-only verifier for the fixed v0.1 standalone delivery, never a builder.

Supported inputs: UTF-8 regular LICENSE/Markdown/strict JSON, ASCII relative POSIX
paths, inline Markdown links/images, reference definitions, backticked resource
paths, HTML URL attributes and CSS url(). Every payload file is inspected, so
transitive local references must resolve too. JSON includes are unsupported.
Active scripts/frames/handlers, JS module/dependency syntax and CSS imports are
rejected, including in examples. HTML is a small element/attribute allowlist;
inline styles, style blocks and custom elements are unsupported. JS/CSS escaping
is conservatively unsupported.
This is a bounded admission grammar, not a general Markdown/JS/CSS interpreter.
The exact source/snapshot checks close syntax gaps for this fixed candidate.
No target input is executed/imported. No network retrieval, runtime security,
rights ownership, rendering, approval authentication or host acceptance is proved.
"""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import stat
import sys
from urllib.parse import urlsplit

SKILLS = ('kumihan', 'kumihan-web', 'kumihan-documents', 'kumihan-review')
FAMILIES = ('content', 'japanese-type', 'web', 'documents', 'design', 'evidence')
PROFILES = ('display-copy', 'presentation', 'report-document', 'web-editorial', 'web-marketing', 'web-ui')
SCHEMAS = ('rule', 'profile', 'report', 'design-contract')
CANONICAL_COMMIT = '41037860c44d65d6157cd30e1d9af40f3bf4dd38'
CANONICAL_TREE = 'a41c22245e38f5619d34a3a1120ecf0dfe3a45c0'
EXPECTED_IDS = {f'{family}-{i:03}' for family, count in
                [('CONTENT',5),('JA-TYPE',10),('WEB',8),('DOC',4),('DESIGN',6),('EVIDENCE',5)]
                for i in range(1, count + 1)}


def require(condition, code):
    if not condition:
        raise ValueError(code)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_path(path):
    require(isinstance(path, str) and bool(re.fullmatch(r'[A-Za-z0-9_-]+(?:[./][A-Za-z0-9_-]+)*', path)), 'unsafe-path')
    require(all(part not in ('', '.', '..') and not part.startswith('.') for part in path.split('/')), 'unsafe-path')
    return path


def read_files(folder):
    require(not folder.is_symlink() and folder.is_dir(), 'invalid-folder')
    result = {}
    aliases = set()
    for p in sorted(folder.rglob('*')):
        name = safe_path(p.relative_to(folder).as_posix())
        key = name.casefold()
        require(key not in aliases, 'case-alias')
        aliases.add(key)
        mode = p.lstat().st_mode
        require(stat.S_ISDIR(mode) or stat.S_ISREG(mode), 'nonregular-file')
        if stat.S_ISREG(mode):
            require(p.stat().st_size <= 1_000_000, 'file-size-limit')
            data = p.read_bytes()
            data.decode('utf-8', errors='strict')
            require(p.suffix in ('.json', '.md') or name == 'LICENSE', 'unsupported-file-type')
            result[name] = data
    return result


def json_data(text):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate-json-key')
            require(key.lower() not in ('include', '$include', 'imports', 'extends', 'require'), 'unsupported-json-include')
            result[key] = value
        return result
    def constant(_):
        raise ValueError('nonfinite-json')
    return json.loads(text, object_pairs_hook=pairs, parse_constant=constant)


def local_reference(value, names):
    require(isinstance(value, str), 'invalid-reference')
    path = value.split('#', 1)[0]
    if not path:
        return
    safe_path(path)
    require(path in names, 'missing-local-reference')


def reference(value, names, runtime=False):
    require(not any(c in value for c in ('%', '\\', '\n', '\r', '\t')), 'encoded-reference')
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc:
        require(not runtime and parsed.scheme in ('http', 'https') and bool(parsed.netloc)
                and parsed.username is None and parsed.password is None, 'remote-runtime-or-unsafe-url')
    else:
        local_reference(value, names)


def check_text(text, names, name='input.md'):
    # Comments can separate JS tokens; replacing them with a space catches both
    # import/*c*/x and import x/*c*/from without evaluating the payload.
    plain = re.sub(r'/\*.*?\*/', ' ', text, flags=re.S)
    require(not re.search(r'\b(?:import\s*(?:[\'"({*]|[\w$]+\s+from\b)|export\s+(?:\*|\{)[^;]*\bfrom\b|require\s*\()', plain, re.I), 'executable-dependency')
    require(not re.search(r'\b(?:import|export|require)\\', text, re.I), 'unsupported-js-escape')
    require(not re.search(r'@import\b', plain, re.I), 'css-import')
    # Escaped CSS identifiers/URLs cannot be reliably interpreted by this grammar.
    require(not re.search(r'(?:style\s*=|<style\b)[^>]*\\', text, re.I), 'unsupported-css-escape')

    class Markup(HTMLParser):
        def handle_starttag(self, tag, attrs):
            require(tag in ('a','p','img','video','audio','source','div','span','br',
                            'strong','em','code','pre','ul','ol','li','name'), 'unsupported-html-element')
            seen = set()
            for key, val in attrs:
                require(key not in seen, 'duplicate-html-attribute'); seen.add(key)
                require(not key.startswith('on') and key not in ('srcdoc',), 'active-html-attribute')
                require(key in ('href','src','srcset','poster','title','alt','width','height',
                                'controls','class','id'), 'unsupported-html-attribute')
                if key == 'srcset':
                    require(bool(val), 'malformed-srcset')
                    descriptors = set()
                    for item in val.split(','):
                        match = re.fullmatch(r'\s*(\S+)\s+([1-9][0-9]*(?:\.[0-9]+)?x|[1-9][0-9]*w)\s*', item)
                        require(match is not None, 'malformed-srcset')
                        url, desc = match.groups()
                        require(desc not in descriptors, 'malformed-srcset'); descriptors.add(desc)
                        reference(url, names, runtime=True)
                    require(len({x[-1] for x in descriptors}) == 1, 'malformed-srcset')
                elif key in ('src','poster','data','action','formaction','background','href','xlink:href'):
                    require(bool(val), 'empty-html-url')
                    reference(val, names, runtime=(key != 'href' or tag != 'a'))
        handle_startendtag = handle_starttag

    Markup(convert_charrefs=True).feed(text)
    # Also reject malformed active-tag starts that HTMLParser might recover oddly.
    require(not re.search(r'<\s*/?\s*(?:script|iframe|object|embed|base)\b', text, re.I), 'active-html')
    for match in re.finditer(r'url\(\s*([^)]+)\)', plain, re.I):
        reference(match[1].strip().strip('\'"'), names, runtime=True)
    for match in re.finditer(r'(!?)\[[^\]\n]*\]\(([^)\n]+)\)', text):
        require(not any(c.isspace() for c in match[2]), 'unsupported-markdown-link')
        reference(match[2], names, runtime=bool(match[1]))
    definitions = {}
    for match in re.finditer(r'^\s*\[([^]\n]+)\]:\s*(\S+)\s*$', text, re.M):
        require(match[1].casefold() not in definitions, 'duplicate-markdown-definition')
        definitions[match[1].casefold()] = match[2]
        reference(match[2], names)
    for match in re.finditer(r'(!?)\[([^]\n]+)\]\[([^]\n]*)\]', text):
        target = definitions.get((match[3] or match[2]).casefold())
        require(target is not None, 'missing-markdown-definition')
        reference(target, names, runtime=bool(match[1]))
    for match in re.finditer(r'`([^`\n]+)`', text):
        value = match[1]
        if re.fullmatch(r'(?:[\w.-]+/)*[\w.-]+\.(?:json|md)', value):
            local_reference(value, names)


def walk_json(value):
    if isinstance(value, dict):
        yield value
        for v in value.values(): yield from walk_json(v)
    elif isinstance(value, list):
        for v in value: yield from walk_json(v)


def schema_registry(files):
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource
    schemas = {json_data(files[f'schemas/{n}.schema.json'])['$id']:
               json_data(files[f'schemas/{n}.schema.json']) for n in SCHEMAS}
    require(len(schemas) == 4, 'duplicate-schema-id')
    for schema in schemas.values():
        Draft202012Validator.check_schema(schema)
        for obj in walk_json(schema):
            if '$ref' in obj:
                base, _, fragment = obj['$ref'].partition('#')
                require(not base or base in schemas, 'unresolved-schema-reference')
                dest = schemas.get(base, schema)
                for key in fragment.split('/')[1:]:
                    require(isinstance(dest, dict) and key in dest, 'unresolved-schema-fragment')
                    dest = dest[key]
    def no_retrieve(_): raise ValueError('offline-schema-only')
    registry = Registry(retrieve=no_retrieve).with_resources(
        (uri, Resource.from_contents(schema)) for uri, schema in schemas.items())
    return {name: Draft202012Validator(schemas[f'urn:kumihan:schema:{name}:0.1.0'], registry=registry)
            for name in SCHEMAS}


def check_catalog(files):
    validators = schema_registry(files)
    catalog = json_data(files['rules/catalog.json'])
    require(isinstance(catalog, list), 'invalid-catalog')
    ids = [r['id'] for r in catalog]
    require(len(ids) == 38 and set(ids) == EXPECTED_IDS, 'rule-id-set-or-duplicates')
    for rule in catalog:
        require(validators['rule'].is_valid(rule), 'rule-schema')
        require(rule['verification']['coverage'] != 'implemented', 'unimplemented-detector-claim')
    registry = json_data(files['sources/public-sources.json'])
    records = registry['sources']
    sources = {s['id']: s for s in records}
    require(len(sources) == len(records) == 57, 'source-id-set-or-duplicates')
    rules = {r['id']: r for r in catalog}
    for rule in catalog:
        for source_id in rule['source_refs']:
            require(source_id in sources, 'unresolved-source')
            source = sources[source_id]
            require(source['classification'] == 'adopted' and source['type'] in
                    ('expert-practice', 'implementation-reference', 'standard-reference', 'project-policy')
                    and rule['id'] in source['rule_ids'], 'source-relationship')
            if source['type'] == 'project-policy':
                require(bool(source['statement']) and bool(source['adopted_principle']), 'missing-policy-statement')
    for source in records:
        require(len(set(source['rule_ids'])) == len(source['rule_ids']), 'duplicate-source-rule')
        for rule_id in source['rule_ids']:
            require(rule_id in rules and source['id'] in rules[rule_id]['source_refs'], 'reverse-source-relationship')
    for name in PROFILES:
        profile = json_data(files[f'profiles/{name}.json'])
        require(validators['profile'].is_valid(profile) and profile['id'] == name, 'profile-schema')
        selected = {r['id'] for r in catalog if name in r['media']}
        require(set(profile['rule_ids']) == selected, 'profile-media-relationship')
    cases = [case for r in catalog for case in r['case_ids']]
    require(len(cases) == len(set(cases)) == 57, 'declared-case-ids')
    return {'rules': 38, 'profiles': 6, 'sources': 57, 'declared_case_ids': 57,
            'integrated_rule_detectors': 0}


def replace_once(text, old, new):
    require(text.count(old) == 1, 'adaptation-source-anchor')
    return text.replace(old, new, 1)


def adapted_text(path, source):
    text = source.decode('utf-8')
    if path == 'sources/public-sources.json':
        return text.replace('docs/architecture.md', 'references/architecture.md').encode()
    if path == 'SKILL.md':
        for old, new in (
            ('This source workflow alone does not prove bundle validation.',
             'This workflow alone does not prove standalone folder validation.'),
            ('Actual standalone package admission requires separate bundle validation.',
             'Actual standalone folder admission requires separate inventory and closure validation.')):
            if old in text: text = replace_once(text, old, new)
    elif path == 'references/design-contract.md':
        for old, new in (
            ('`design-contract.schema.json`', '`schemas/design-contract.schema.json`'),
            ('`docs/architecture.md`', '`references/architecture.md`'),
            ('by the package builder and catalog checks before claiming a complete bundle.',
             'by standalone folder inventory and catalog checks before claiming complete local resources.')):
            text = replace_once(text, old, new)
    elif path == 'references/architecture.md':
        # Keep the pre-module guidance byte-for-byte except these bounded changes.
        text = text.split('## Module and CLI ownership\n', 1)[0]
        require('## Module and CLI ownership\n' in source.decode(), 'architecture-cut-anchor')
        start = text.index('Release manifests contain ')
        end = text.index('### Referenced exception and waiver approvals')
        text = text[:start] + text[end:]
        start = text.index('The report CLI owns report-waiver lookup')
        end = text.index('\nThe following case expectations', start)
        text = text[:start] + HOST_ADMISSION + text[end:]
        for old, new in (
            ('The five schemas', 'The four consumer schemas'),
            ('in `rule.schema.json`', 'in `schemas/rule.schema.json`'),
            ('register all five local schema', 'register all four local schema'),
            ('### Reports and release metadata', '### Reports')):
            text = replace_once(text, old, new)
        text += DELIVERY
    return text.encode('utf-8')


HOST_ADMISSION = '''The trusted host report-admission workflow owns report-waiver lookup and
validation, including catalog exception bounds and exact report/check/artifact
binding. Structural schema validation cannot authenticate external records.
The host independently rechecks required approvals at each use and admission.
Missing, invalid, stale or unverifiable evidence rejects admission; disallowed
exceptions fail. Neither outcome converts a waiver into a pass or permits
editing the reviewed target. Further edits require refine authorization.
'''
DELIVERY = '''## Standalone folder delivery — v0.1.0

This complete folder is a Git-tracked standalone Agent Skill. Copy the whole
folder, including LICENSE and inventory.json. All consumer paths in guidance
are relative to this folder root, even inside references or JSON records.
The local rules/catalog.json is the complete 38-rule catalog; its six family
snapshots retain canonical bytes. All six profiles remain available for mixed
media and rule resolution. The public registry retains 57 source records.
Four consumer schemas resolve their versioned URNs locally; source URLs and
JSON Schema dialect URLs identify provenance, not network requirements.

inventory.json identifies canonical inputs, exact-byte snapshots and deliberate
consumer prose/path adaptations. It inventories every other file; its own hash
belongs to the external candidate evidence to avoid a recursive self-digest.
Canonical sources remain authoritative; do not maintain independent rule copies.

Historical module/CLI, generated archive and release-manifest contracts are
excluded from consumer delivery. No builder, ZIP, runtime validator, detector,
renderer, Python/npm package, private resource or sibling is required. Existing
authorized host tools perform production and evidence review. Folder closure
and byte stability do not establish host discovery or invocation, rendering,
native Office acceptance, source truth or approval authenticity. Independent
review and separate exact-candidate publication authorization remain required.
'''


def mapping(skill):
    result = {'LICENSE': ['LICENSE'], 'SKILL.md': [f'skill-src/{skill}/SKILL.md'],
              'references/architecture.md': ['docs/architecture.md'],
              'references/design-contract.md': ['skill-src/shared/design-contract.md'],
              'references/review-protocol.md': ['skill-src/shared/review-protocol.md'],
              'sources/public-sources.json': ['sources/public-sources.json'],
              'rules/catalog.json': [f'rules/{f}.json' for f in FAMILIES]}
    for group, names, suffix in (('profiles', PROFILES, '.json'), ('rules', FAMILIES, '.json'),
                                 ('schemas', SCHEMAS, '.schema.json')):
        result.update({f'{group}/{n}{suffix}': [f'{group}/{n}{suffix}'] for n in names})
    return result


def check_folder(folder, canonical):
    files = read_files(folder)
    inventory = json_data(files['inventory.json'])
    skill = inventory['skill']
    require(skill in SKILLS, 'unknown-skill')
    expected = mapping(skill)
    require(set(files) == set(expected) | {'inventory.json'} and len(files) == 24, 'folder-membership')
    require(digest(files['inventory.json']) == INVENTORIES[skill], 'inventory-snapshot')
    require(inventory['format'] == 'kumihan-standalone-inventory-1'
            and inventory['canonical_commit'] == CANONICAL_COMMIT
            and inventory['canonical_tree'] == CANONICAL_TREE
            and inventory['path_base'] == 'skill-folder-root', 'inventory-identity')
    rows = inventory['files']
    require(len(rows) == len(expected) and {r['path'] for r in rows} == set(expected), 'inventory-membership')
    names = set(files)
    for name, data in files.items():
        if name.endswith('.json'): json_data(data)
        if name.endswith('.md'): check_text(data.decode(), names, name)
    result = check_catalog(files)
    for row in rows:
        path = safe_path(row['path'])
        require(row['bytes'] == len(files[path]) and row['sha256'] == digest(files[path]), 'inventory-file-digest')
        require([s['path'] for s in row['canonical']] == expected[path], 'source-mapping')
        inputs = []
        for src in row['canonical']:
            source_path = safe_path(src['path'])
            # Read components without following symlinks, including parent directories.
            p = canonical
            for part in source_path.split('/'):
                p = p / part
                require(not p.is_symlink(), 'canonical-symlink')
            require(stat.S_ISREG(p.lstat().st_mode), 'canonical-nonregular')
            data = p.read_bytes()
            require(digest(data) == src['sha256'], 'canonical-digest')
            inputs.append(data)
        if path == 'rules/catalog.json':
            combined = [r for data in inputs for r in json_data(data)]
            require(json_data(files[path]) == combined, 'catalog-concatenation')
        else:
            require(files[path] == adapted_text(path, inputs[0]), 'snapshot-or-adaptation')
    result['files'] = len(files)
    return result


def check_repository(root):
    require(not root.is_symlink(), 'repository-symlink')
    folders = root / 'skills'
    require(not folders.is_symlink() and folders.is_dir(), 'invalid-skills-root')
    require({p.name for p in folders.iterdir()} == set(SKILLS), 'skill-set')
    result = {skill: check_folder(folders / skill, root) for skill in SKILLS}
    for name, expected in CANONICAL_EXTRAS.items():
        p = root / name
        require(not p.is_symlink() and digest(p.read_bytes()) == expected, 'canonical-extra-digest')
    # The fifth schema is a retained canonical historical contract, not consumer input.
    from jsonschema import Draft202012Validator
    Draft202012Validator.check_schema(json_data((root/'schemas/release-manifest.schema.json').read_bytes()))
    return result


# Only fixed source contracts outside the consumer mapping belong here.
# README.md is mutable public documentation, not a canonical consumer input.
# check_public_boundary.py continues to scan it with every tracked file.
CANONICAL_EXTRAS = {'schemas/release-manifest.schema.json': '1bda6b026d34932a66060c8435d8d5e31a20791c410971acc063192581ab1b36'}


# Inventory bytes are fixed independently from their self-declared file hashes.
# Update only after a separately reviewed source/consumer candidate is authorized.
INVENTORIES = {
    'kumihan': '192aa4253f3b32eb083d8c83fe5b6101167c11c58791cc045e87b3dbfe4fc6b6',
    'kumihan-web': 'dd841e0beade64923aceb8a52490e7b832d82b55768366e9adb6eaabc5ed6410',
    'kumihan-documents': '4bf3d747494387569faa34facd431dead60d9e83492c6033e3c8e7928d5b0d81',
    'kumihan-review': 'cba78712856d17047a17823895509ae89167c953ca51699ff2c22593c4bdb9f9',
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        result = check_repository(args.root)
    except Exception as exc:
        # Library schema/resolution exceptions can embed whole untrusted records.
        # All verifier errors fail closed; never expose their values or tracebacks.
        print(json.dumps({'status':'failed','code':'invalid-or-unsupported-input','type':type(exc).__name__}))
        return 1
    print(json.dumps({'status':'passed','folders':result}, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
