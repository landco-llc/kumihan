"""Fail-closed acceptance for the Measure consumer source and distribution."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
from zipfile import ZipFile

SLUG = 'kumihan-measure'
ICON = 'KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png'
ICON_SHA = '1d1ae2cb4f7f69f7b5f54b050ff8c6fb2c315b75ded8003f8b605855d633f96e'
VERSION = '0.1.1'
LOCALES = {'en', 'en-US', 'en-GB', 'en-CA', 'en-AU', 'en-IN', 'en-SG', 'en-NZ', 'en-IE', 'en-MY', 'en-PH', 'en-HK', 'en-ZA', 'en-NG', 'en-KE', 'en-GH', 'en-JM'}
SKILLS = [SLUG + suffix for suffix in ('', '-web', '-documents', '-review')]
HOSTS = {'claude': 'Claude-Code-plugin', 'gpt-codex': 'GPT-Codex-plugin', 'gemini': 'Gemini-CLI-extension'}
FORBIDDEN = re.compile(r'(?i)(mcp[_-]?servers|WORK_ID|RUN_ID|INSTRUCTION_COMMIT|kumihan-internal|control/(?:10_instructions|20_results|30_design)|private\s+(?:candidate|(?:0\.1\.0\s+)?candidate|git checkout)|private候補|no publication|NEXT_GATE|BEGIN [A-Z ]*PRIVATE KEY|github_pat_[a-z0-9_]+|gh[pousr]_[a-z0-9]{20,}|mcp-kmhn\.landco\.co\.jp|(?:api[_-]?key|access[_-]?token|password)\s*[:=]\s*[\"\'][^\"\']{8,})')
# Byte scanning is extension independent, including binary and renamed payloads.
FORBIDDEN_BYTES = re.compile(FORBIDDEN.pattern.encode('utf-8'))
REQUIRED = {'SKILL.md', 'LICENSE', 'sources.json', 'inventory.json', 'runtime/check_source.py', 'rules/catalog.json', 'references/workflow.md', 'references/research-trace.json', 'profiles/mediums.json', 'locales/supported.json', 'locales/en.json', 'locales/en-US.json', 'locales/en-GB.json', 'references/regional-typography.md', 'profiles/house-styles.json', 'fixtures/regional-acceptance.json', 'fixtures/acceptance.json', 'schemas/report.schema.json', 'assets/' + ICON}


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def check_member(name, raw):
    path = PurePosixPath(name)
    parts = name.split('/')
    if not name or name.startswith('/') or '\\' in name or ':' in name or any(p in ('', '.', '..') for p in parts):
        raise ValueError('Unsafe consumer path: ' + name)
    for part in parts:
        lower = part.casefold()
        if (lower.startswith(('goal', 'result')) and lower.endswith('.md')) or any(x in lower for x in ('workgroup', 'next_gate', '__pycache__')) or lower in {'result', 'result.md', 'results', 'control', '.env', '.git', '.ssh', 'credentials', '.ds_store'}:
            raise ValueError('Forbidden consumer path: ' + name)
        if lower.startswith('.') and lower not in {'.codex-plugin', '.claude-plugin'}:
            raise ValueError('Hidden consumer path: ' + name)
    if path.name == ICON:
        if digest(raw) != ICON_SHA:
            raise ValueError('Modified official icon: ' + name)
        return  # Only this exact, verified binary asset is exempt from text scanning.
    if FORBIDDEN_BYTES.search(raw) or FORBIDDEN_BYTES.search(raw.replace(b'\x00', b'')):
        raise ValueError('Forbidden internal consumer content: ' + name)
    if path.suffix.casefold() == '.json':
        json.loads(raw.decode('utf-8'))


def check_entries(entries, standalone=False):
    names = list(entries)
    if len({n.casefold() for n in names}) != len(names):
        raise ValueError('Casefold collision')
    for name, raw in entries.items():
        check_member(name, raw)
    if standalone and {n.split('/')[0] for n in names} - set(SKILLS):
        raise ValueError('Unknown standalone Skill root')
    for skill in SKILLS:
        prefix = skill + '/' if standalone else SLUG + '/skills/' + skill + '/'
        if standalone and not any(n.startswith(prefix) for n in names):
            continue
        missing = {prefix + n for n in REQUIRED} - entries.keys()
        if missing:
            raise ValueError('Missing standalone dependency: ' + repr(sorted(missing)))
        locales = json.loads(entries[prefix + 'locales/supported.json'])
        if locales['language'] != 'en' or set(locales['locales']) != LOCALES:
            raise ValueError('Wrong Measure locale')
        inventory = json.loads(entries[prefix + 'inventory.json'])
        if inventory['language'] != 'en' or inventory['version'] != VERSION or inventory['rule_count'] != 51:
            raise ValueError('Wrong Measure identity')
        catalog = json.loads(entries[prefix + 'rules/catalog.json'])
        rules = catalog if isinstance(catalog, list) else catalog['rules']
        if len(rules) != 51 or len({r['id'] for r in rules}) != 51:
            raise ValueError('Wrong Measure rule set')
        source_data = json.loads(entries[prefix + 'sources.json'])
        source_ids = {r['ID'] for r in source_data['sources']} | set(source_data['research_synthesis'])
        for rule in rules:
            if not rule['source_ids'] or not set(rule['source_ids']) <= source_ids:
                raise ValueError('Unresolved rule source')
        for locale in LOCALES:
            if prefix + 'locales/' + locale + '.json' not in entries:
                raise ValueError('Missing regional locale file')
        skill_text = entries[prefix + 'SKILL.md'].decode()
        for target in re.findall(r'\]\(([^)]+)\)', skill_text):
            if '://' not in target and prefix + target not in entries:
                raise ValueError('Broken standalone reference: ' + target)
    if standalone and len({n.split('/')[0] for n in names}) != 1:
        raise ValueError('Standalone archive has multiple roots')


def check_source(product):
    entries = {}
    for path in sorted(product.rglob('*')):
        relative = path.relative_to(product)
        if relative.parts[0] == 'downloads':
            continue
        if path.is_symlink():
            raise ValueError('Consumer symlink: ' + str(relative))
        if path.is_file():
            entries[SLUG + '/' + relative.as_posix()] = path.read_bytes()
    check_entries(entries)
    for required in ('assets/' + ICON, 'inventory.json', 'plugin.json', '.codex-plugin/plugin.json', '.claude-plugin/plugin.json', 'gemini-extension.json', 'GEMINI.md'):
        if SLUG + '/' + required not in entries:
            raise ValueError('Missing product dependency: ' + required)
    return entries


def expected_packages():
    return {f'{skill}-{host}-skill-v{VERSION}.zip': host for host in HOSTS for skill in SKILLS} | {f'{SLUG}-{label}-v{VERSION}.zip': host for host, label in HOSTS.items()}


def check_archive(path):
    with ZipFile(path) as archive:
        names = archive.namelist()
        if len(names) != len(set(n.casefold() for n in names)):
            raise ValueError('Duplicate archive members')
        if archive.testzip():
            raise ValueError('CRC failure')
        for info in archive.infolist():
            if stat.S_ISLNK(info.external_attr >> 16):
                raise ValueError('Archive symlink')
        entries = {n: archive.read(n) for n in names}
    standalone = '-skill-v' in path.name
    check_entries(entries, standalone=standalone)
    if not standalone:
        metadata = {'Claude-Code-plugin': '.claude-plugin/plugin.json', 'GPT-Codex-plugin': '.codex-plugin/plugin.json', 'Gemini-CLI-extension': 'gemini-extension.json'}
        for label, filename in metadata.items():
            if label in path.name:
                key = SLUG + '/' + filename
                if key not in entries:
                    raise ValueError('Missing host metadata')
                identity = json.loads(entries[key])
                if identity['name'] != SLUG or identity['version'] != VERSION:
                    raise ValueError('Wrong host identity')
                if label == 'Gemini-CLI-extension' and SLUG + '/GEMINI.md' not in entries:
                    raise ValueError('Missing Gemini entrypoint')
    return entries


def check_distribution(product, destination):
    if destination.name.startswith('downloads ') or destination.parent.name.startswith('downloads '):
        raise ValueError('Measure must not use Japanese root downloads')
    expected = expected_packages()
    legacy_pins = json.loads(Path(__file__).with_name('measure_legacy_v010.json').read_text())
    historical = {p.name for p in destination.glob('*v0.1.0.zip')}
    for name in historical:
        if name not in legacy_pins or digest((destination / name).read_bytes()) != legacy_pins[name]:
            raise ValueError('Modified historical Measure archive')
    if {p.name for p in destination.glob('*.zip')} - historical != set(expected):
        raise ValueError('Expected exact 15 Measure packages')
    allowed = set(expected) | historical | {'manifest.json', 'SHA256SUMS'} | {'SHA256SUMS-' + h for h in HOSTS}
    if {p.name for p in destination.iterdir()} != allowed:
        raise ValueError('Unexpected distribution file')
    manifest = json.loads((destination / 'manifest.json').read_text())
    if manifest['slug'] != SLUG or manifest['language'] != 'en' or manifest['version'] != VERSION:
        raise ValueError('Wrong distribution identity')
    records = manifest['packages']
    if len(records) != 15 or {r['file'] for r in records} != set(expected):
        raise ValueError('Manifest package set mismatch')
    source = check_source(product)
    source_records = [{'path': n[len(SLUG) + 1:], 'sha256': digest(raw)} for n, raw in source.items()]
    source_sha = digest(json.dumps(source_records, sort_keys=True, separators=(',', ':')).encode())
    if manifest['source_files'] != source_records or manifest['source_sha256'] != source_sha:
        raise ValueError('Source fingerprint mismatch')
    for record in records:
        path = destination / record['file']
        if record['host'] != expected[record['file']] or record['source_sha256'] != source_sha or record['version'] != VERSION:
            raise ValueError('Package provenance mismatch')
        if digest(path.read_bytes()) != record['sha256'] or path.stat().st_size != record['bytes']:
            raise ValueError('Package checksum mismatch')
        entries = check_archive(path)
        for name, raw in entries.items():
            source_name = name if '-skill-v' not in path.name else SLUG + '/skills/' + name
            if source.get(source_name) != raw:
                raise ValueError('Archive/source mismatch: ' + name)
    aggregate = ''.join(f'{r["sha256"]}  {r["file"]}\n' for r in records)
    if (destination / 'SHA256SUMS').read_text() != aggregate:
        raise ValueError('Aggregate checksum manifest mismatch')
    for host in HOSTS:
        expected_text = ''.join(f'{r["sha256"]}  {r["file"]}\n' for r in records if r['host'] == host)
        if (destination / ('SHA256SUMS-' + host)).read_text() != expected_text:
            raise ValueError('Host checksum manifest mismatch')
    return manifest
