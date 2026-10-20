#!/usr/bin/env python3
"""Check public source/site boundaries and export clean prospective ZIPs."""
import argparse
import hashlib
import io
import json
import re
import subprocess
import zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CONTRACT='tests/contracts/public-allowlist.json'
INTERNAL=re.compile(r'(^|/)(?:GOAL(?:_[^/]*)?|LIGHT_REVIEW|TEST_REPORT|ZILU_V010_CANDIDATE_REPORT|RESULT|NEXT_GATE|WORKGROUP)\.md$|(^|/)docs/development\.md$',re.I)
MCP_NAME=re.compile(r'(^|/)(?:\.?mcp\.json|[^/]*server[^/]*\.php)$',re.I)
MCP_CONFIG=re.compile(rb'''["']mcpServers["']\s*:|(?m:^\s*\[\[?\s*(?:mcp_servers|mcpServers)(?:[.\]\s]))''')
INTERNAL_TEXT=re.compile(rb'(?m)^\s*(?:WORK_ID|NEXT_GATE|RUN_ID|INSTRUCTION_COMMIT)\s*:')

def digest(raw):return hashlib.sha256(raw).hexdigest()

def forbidden(name, raw):
    return bool(INTERNAL.search(name) or MCP_NAME.search(name) or MCP_CONFIG.search(raw) or INTERNAL_TEXT.search(raw))

def clean_archive(raw):
    out=io.BytesIO()
    with zipfile.ZipFile(io.BytesIO(raw)) as src, zipfile.ZipFile(out,'w') as dst:
        for info in src.infolist():
            name=info.filename
            if name.startswith('/') or '..' in Path(name).parts:raise ValueError('Unsafe archive member: '+name)
            data=src.read(info)
            if INTERNAL.search(name):continue
            if forbidden(name,data):raise ValueError('Forbidden archive member: '+name)
            dst.writestr(info,data)
    return out.getvalue()

def source_paths(root):
    root=Path(root)
    if (root/'.git').exists():
        paths=subprocess.check_output(['git','-C',str(root),'ls-files','--cached','--others','--exclude-standard','-z']).decode().split('\0')
        return {p for p in paths if p and (root/p).is_file()}
    return {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}

def audit(root=ROOT, contract=None):
    root=Path(root)
    if contract is None:contract=json.loads((ROOT/CONTRACT).read_text())
    errors=[];actual=source_paths(root);expected=set(contract['files'])
    for name in sorted(actual-expected-{CONTRACT}):errors.append('Unlisted public path: '+name)
    for name,expected_hash in contract['files'].items():
        path=root/name
        if not path.is_file():errors.append('Missing public path: '+name);continue
        raw=path.read_bytes()
        if digest(raw)!=expected_hash:errors.append('Public bytes changed: '+name)
        # Source tests/tools contain literal negative examples; their bytes are fixed above.
        if not name.startswith(('tools/','tests/')) and not name.endswith('.zip') and forbidden('' if name=='docs/development.md' else name,raw):
            errors.append('Forbidden public content: '+name)
        if name.endswith('.zip'):
            if name in contract.get('legacy_archives',{}):
                if digest(raw)!=contract['legacy_archives'][name]:errors.append('Legacy ZIP changed: '+name)
            else:
                try:
                    with zipfile.ZipFile(io.BytesIO(raw)) as z:
                        for member in z.infolist():
                            if forbidden(member.filename,z.read(member)):errors.append('Forbidden ZIP member: '+name+':'+member.filename)
                except (ValueError,zipfile.BadZipFile):errors.append('Invalid ZIP: '+name)
    return errors

def audit_site(root, contract=None):
    if contract is None:contract=json.loads((ROOT/CONTRACT).read_text())
    errors=[]
    for p in Path(root).rglob('*'):
        if not p.is_file():continue
        name=p.relative_to(root).as_posix()
        if name.endswith('.zip'):
            if name not in contract['files'] or digest(p.read_bytes())!=contract['files'][name]:
                errors.append('Unlisted or changed site ZIP: '+name)
            continue
        if name.startswith(('tools/','tests/','control/','docs/development/','docs/seo/','docs/version-automation/')) or forbidden('' if name=='docs/development.md' else name,p.read_bytes()):errors.append('Forbidden site output: '+name)
    return errors

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site-dir',type=Path)
    parser.add_argument('--candidate-dir',type=Path)
    args=parser.parse_args()
    errors=audit()
    if args.site_dir:errors+=audit_site(args.site_dir)
    if errors:raise SystemExit('\n'.join(errors))
    if args.candidate_dir:
        target=args.candidate_dir.resolve()
        if target==ROOT or ROOT in target.parents:raise SystemExit('Candidate output must be outside public checkout')
        target.mkdir(parents=True,exist_ok=True);receipt=[]
        for name in sorted(source_paths(ROOT)):
            if not name.endswith('.zip'):continue
            raw=(ROOT/name).read_bytes();clean=clean_archive(raw)
            if clean!=raw:
                dest=target/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(clean)
            receipt.append(dict(path=name,before=digest(raw),candidate=digest(clean),bytes=len(clean)))
        (target/'CANDIDATE_MANIFEST.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('Public source boundary: PASS')

if __name__=='__main__':main()
