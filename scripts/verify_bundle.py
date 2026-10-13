"""Bounded data-only ZIP inspection. Does not execute content or fetch references."""
import hashlib
from html.parser import HTMLParser
from urllib.parse import urlsplit
import struct
from pathlib import Path, PurePosixPath
import posixpath
import re
import stat
import sys
import zipfile
import zlib

try:
    from .validate_catalog import MAX_FILE, VERSION, safe_name, read_bytes, parse_json, emit, SCHEMA_HASHES, validators_from_bytes, schema_errors, ResultParser, source_errors, implemented_errors
except ImportError:
    from validate_catalog import MAX_FILE, VERSION, safe_name, read_bytes, parse_json, emit, SCHEMA_HASHES, validators_from_bytes, schema_errors, ResultParser, source_errors, implemented_errors

SKILLS = ("kumihan", "kumihan-web", "kumihan-documents", "kumihan-review")
MAX_MEMBERS = 2048
MAX_TOTAL = 64 * 1024 * 1024
MAX_ARCHIVE = 64 * 1024 * 1024
DIGEST = re.compile(r"sha256:[0-9a-f]{64}")


def allowed_file(name):
    safe_name(name)
    parts = name.split("/")
    if any(re.search(r"(?:^|[-_.])(?:raw-log|command-log|transcript|maintainer-routing|approvals|credentials|secrets)(?:[-_.]|$)", part, re.I) for part in parts):
        return False
    if name in {"SKILL.md", "LICENSE", "inventory.json"}:
        return True
    if parts[0] == "schemas":
        return name in {f"schemas/{schema}.schema.json" for schema in SCHEMA_HASHES}
    if parts[0] == "rules":
        return name == "rules/catalog.json"
    if parts[0] == "sources":
        return name == "sources/public-sources.json"
    if parts[0] == "profiles":
        return len(parts) == 2 and PurePosixPath(name).suffix == ".json"
    return len(parts) >= 2 and parts[0] == "references" and PurePosixPath(name).suffix in {".md", ".json"}



# Supported declarative syntax: Markdown links/images/definitions, qualified
# backtick resource paths, HTML resource attributes, CSS url/@import, and JSON
# $ref/include. Public HTTP(S)/mailto citations are not runtime dependencies.
# Active imports/scripts and undeclared resource forms fail closed; no execution,
# retrieval, arbitrary schema registration or universal prose analysis occurs.
KNOWN_URNS={f'urn:kumihan:schema:{name}:0.1.0':f'schemas/{name}.schema.json' for name in SCHEMA_HASHES}


class _HTMLDependencies(HTMLParser):
    def __init__(self): super().__init__(convert_charrefs=True); self.refs=[]; self.active=False
    def handle_starttag(self,tag,attrs):
        values=dict(attrs)
        if tag in {'script','iframe','object','embed','base'} or any(key.startswith('on') for key in values): self.active=True
        for key in ('src','poster','data'):
            if values.get(key): self.refs.append((values[key],True))
        if values.get('href'): self.refs.append((values['href'],tag!='a'))
        if values.get('srcset'):
            for item in values['srcset'].split(','): self.refs.append((item.strip().split()[0],True))
        if values.get('style'):
            for target in re.findall(r'url\(\s*["\']?([^\)"\']+)',values['style'],re.I): self.refs.append((target.strip(),True))
    handle_startendtag=handle_starttag


def dependency_references(name,data):
    """Return (literal, runtime-required, project-root-qualified) declarations."""
    refs=[]
    if name.endswith('.json'):
        value=parse_json(data)
        def visit(node):
            if isinstance(node,dict):
                if 'approver_ref' in node or node.get('format')=='kumihan-host-authority-1':
                    raise ValueError('restricted host control data')
                for key,child in node.items():
                    if key in ('$ref','include'):
                        entries=child if isinstance(child,list) else [child]
                        if any(not isinstance(entry,str) for entry in entries): raise ValueError('unsupported JSON dependency')
                        refs.extend((entry,True,False) for entry in entries)
                    else: visit(child)
            elif isinstance(node,list):
                for child in node: visit(child)
        visit(value)
        return refs
    if not name.endswith('.md'): return refs
    text=data.decode('utf-8','strict')
    if re.search(r'(?m)^\s*(?:import\s+[\w.]+(?:\s+as\s+\w+)?(?:\s*,\s*[\w.]+(?:\s+as\s+\w+)?)*|from\s+[\w.]+\s+import\s+[\w*, ]+)\s*(?:#.*|;.*)?$|\b(?:import|require|__import__)\s*\(',text):
        raise ValueError('unsupported active dependency')
    parser=_HTMLDependencies(); parser.feed(text)
    if parser.active or re.search(r'@import\b',text,re.I): raise ValueError('unsupported active dependency')
    refs.extend((target,required,False) for target,required in parser.refs)
    refs.extend((target.strip(),True,False) for target in re.findall(r'url\(\s*["\']?([^\)"\']+)',text,re.I))
    refs.extend((match.group(2).strip('<>'),bool(match.group(1)),False)
                for match in re.finditer(r'(!?)\[[^\]]*\]\(\s*([^\s)]+)',text))
    refs.extend((target.strip('<>'),False,False) for target in re.findall(r'(?m)^\s*\[[^\]]+\]:\s*(\S+)',text))
    for target in re.findall(r'`([^`\s]+)`',text):
        if target in {'references/','rules/','profiles/','schemas/','sources/','docs/'}: continue
        if target.startswith(('references/','rules/','profiles/','schemas/','sources/','docs/')) or target in {name+'.schema.json' for name in SCHEMA_HASHES}:
            refs.append((target,True,True))
    return refs


def dependency_target(name,target,required,qualified=False):
    target=target.strip('<>')
    if target.startswith(('https://','http://','mailto:')):
        if required: raise ValueError('network runtime dependency rejected')
        return None
    if target.startswith('#'): return None
    head=target.split('#',1)[0]
    if head.startswith('urn:'):
        if head not in KNOWN_URNS: raise ValueError('unknown schema resource')
        return KNOWN_URNS[head]
    if not head or head.startswith('/') or any(char in head for char in ('\\',':','%','?')):
        raise ValueError('unsafe local reference')
    for schema in SCHEMA_HASHES:
        if head==schema+'.schema.json': return 'schemas/'+head
    if qualified and head.startswith(('schemas/','profiles/','rules/','sources/')): result=head
    elif qualified and head=='docs/architecture.md': result='references/architecture.md'
    else: result=posixpath.normpath(posixpath.join(posixpath.dirname(name),head))
    return safe_name(result)


def local_targets(name,data):
    return [resolved for target,required,qualified in dependency_references(name,data)
            if (resolved:=dependency_target(name,target,required,qualified)) is not None]


def reference_errors(files):
    errors=[]
    for name,data in sorted(files.items()):
        if not name.endswith(('.md','.json')): continue
        try:
            if any(target not in files for target in local_targets(name,data)): raise ValueError('missing dependency')
        except (ValueError,UnicodeError,KeyError,TypeError):
            errors.append('bundle: missing, stale or unsafe local reference')
    return sorted(set(errors))


def prefix_conflicts(names):
    folded={name.casefold() for name in names}
    return any('/'.join(parts[:index]).casefold() in folded for name in names
               for parts in [name.split('/')] for index in range(1,len(parts)))


def provenance_errors(files,expected_version):
    try:
        value=parse_json(files['references/provenance.json'])
        expected={'builder_version','version','source_epoch','license','sources','limitations'}
        if (not isinstance(value,dict) or set(value)!=expected or value['builder_version']!='0.1.0' or value['version']!=expected_version or
                type(value['source_epoch']) is not int or not 0<=value['source_epoch']<=4354819198 or value['license']!='LICENSE' or
                value['sources']!='sources/public-sources.json' or not isinstance(value['limitations'],list) or
                any(not isinstance(item,str) or not item.strip() for item in value['limitations'])):
            raise ValueError('invalid provenance')
        if not files[value['license']] or not files[value['sources']]: raise ValueError('missing provenance binding')
        return []
    except (KeyError,ValueError,TypeError): return ['bundle: missing or invalid bound provenance']


def reference_closure(files):
    reached = {"SKILL.md", "references/provenance.json"}; pending = ["SKILL.md"]
    while pending:
        name = pending.pop()
        if name not in files:
            raise ValueError("missing local reference")
        if name.endswith((".md", ".json")):
            for target in local_targets(name, files[name]):
                if target not in reached:
                    reached.add(target); pending.append(target)
    return reached


def verify_skill_files(files, expected_version):
    errors = []
    if prefix_conflicts(files): return ["bundle: file/directory prefix conflict"]
    if not {"SKILL.md", "LICENSE", "inventory.json", "references/provenance.json"} <= files.keys():
        return ["bundle: missing skill entry, license or inventory"]
    try:
        inv = parse_json(files["inventory.json"])
        if (not isinstance(inv, dict) or set(inv) != {"format", "version", "files"} or
                inv["format"] != "kumihan-skill-1" or inv["version"] != expected_version or
                not isinstance(inv["files"], dict)):
            return ["bundle: invalid skill inventory"]
        if set(inv["files"]) != set(files) - {"inventory.json"}:
            errors.append("bundle: unlisted or missing skill file")
        names = set()
        for name, data in sorted(files.items()):
            if not allowed_file(name):
                errors.append("bundle: forbidden skill file")
            if name.casefold() in names:
                errors.append("bundle: case-colliding skill names")
            names.add(name.casefold())
            if len(data) > MAX_FILE:
                errors.append("bundle: skill file size limit exceeded")
            if b'"approver_ref"' in data or re.search(rb"(?:sk-proj-[A-Za-z0-9_-]{20,}|AKIA[A-Z0-9]{16}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)", data):
                errors.append("bundle: restricted approval/credential material")
            if name != "inventory.json":
                digest = inv["files"].get(name)
                if not isinstance(digest, str) or not DIGEST.fullmatch(digest) or digest != "sha256:" + hashlib.sha256(data).hexdigest():
                    errors.append("bundle: skill digest mismatch")
        errors.extend(provenance_errors(files,expected_version))
        errors.extend(reference_errors(files))
        try:
            reached = reference_closure(files)
            if any(name.startswith("references/") and name not in reached for name in files):
                errors.append("bundle: unreferenced skill file")
        except (ValueError, UnicodeError):
            errors.append("bundle: missing, stale or unsafe local reference")
        errors.extend(resource_errors(files))
        return sorted(set(errors))
    except (ValueError, TypeError, KeyError, RecursionError):
        return ["bundle: invalid skill data"]


def resource_errors(files):
    try:
        checks = validators_from_bytes({name: files.get(f"schemas/{name}.schema.json") for name in SCHEMA_HASHES})
        values = parse_json(files.get("rules/catalog.json", b"null"))
        if not isinstance(values, list):
            return ["bundle: missing or invalid local catalog"]
        ids = []
        for value in values:
            if schema_errors(checks["rule"], value, "rule"):
                return ["bundle: invalid local rule"]
            ids.append(value["id"])
        expected = checks["rule"].schema["$defs"]["rule_id"]["enum"]
        if len(ids) != len(set(ids)) or set(ids) != set(expected):
            return ["bundle: incomplete or duplicate local rule IDs"]
        index = {value["id"]: value for value in values}
        profile_ids = checks["rule"].schema["$defs"]["media_profile"]["enum"]
        if {name for name in files if name.startswith("profiles/")} != {f"profiles/{identity}.json" for identity in profile_ids}:
            return ["bundle: missing or unlisted local profiles"]
        for identity in profile_ids:
            profile = parse_json(files.get(f"profiles/{identity}.json", b"null"))
            if schema_errors(checks["profile"], profile, "profile") or profile["id"] != identity:
                return ["bundle: missing or invalid local profile"]
            if any(rule_id not in index or identity not in index[rule_id]["media"] for rule_id in profile["rule_ids"]):
                return ["bundle: unresolved local profile rule"]
        if "sources/public-sources.json" not in files:
            return ["bundle: missing local provenance registry"]
        return sorted(set(source_errors(parse_json(files["sources/public-sources.json"]), values, checks) + implemented_errors(values)))
    except (ValueError, TypeError, KeyError, RecursionError):
        return ["bundle: missing, invalid or unsupported local resources"]


def verify_skill_directory(directory, expected_version):
    """Same inventory validation on a copied skill, with no repository lookup."""
    try:
        files = {}
        for path in sorted(Path(directory).rglob("*")):
            if path.is_symlink():
                return ["bundle: symlink rejected"]
            if path.is_dir():
                continue
            name = path.relative_to(directory).as_posix()
            safe_name(name)
            files[name] = read_bytes(path)
            if len(files) > MAX_MEMBERS or sum(map(len, files.values())) > MAX_TOTAL:
                return ["bundle: directory size/inventory limit exceeded"]
        return verify_skill_files(files, expected_version)
    except (OSError, ValueError):
        return ["bundle: missing or invalid skill directory"]



def preflight_zip(data):
    """Bound central-directory metadata before ZipFile allocates member objects.

    ZIP64, spanning and archive comments are deliberately unsupported: admitted
    inventories/byte sizes fit ordinary ZIP and the deterministic builder emits
    this subset. No archive data is executed or extracted.
    """
    if len(data)<22 or data[-22:-18]!=b'PK\x05\x06': raise ValueError('unsupported ZIP envelope')
    _,disk,start_disk,disk_count,count,size,offset,comment=struct.unpack_from('<4s4H2LH',data,len(data)-22)
    if (disk or start_disk or comment or disk_count!=count or not 1<=count<=MAX_MEMBERS or
            size>4*1024*1024 or offset+size!=len(data)-22 or offset>len(data) or
            count==65535 or size==0xffffffff or offset==0xffffffff):
        raise ValueError('unsafe central directory envelope')
    position=offset; names=[]; expanded=0
    for _ in range(count):
        if position+46>offset+size or data[position:position+4]!=b'PK\x01\x02': raise ValueError('invalid central directory')
        flags,method=struct.unpack_from('<HH',data,position+8)
        packed,unpacked=struct.unpack_from('<LL',data,position+20)
        name_len,extra_len,comment_len,disk_start=struct.unpack_from('<4H',data,position+28)
        local=struct.unpack_from('<L',data,position+42)[0]
        if (not 1<=name_len<=512 or extra_len>1024 or comment_len>1024 or disk_start or
                local>=offset or flags&1 or method not in (0,8) or unpacked>MAX_FILE or
                unpacked>max(packed,1)*200): raise ValueError('unsafe central member metadata')
        end=position+46+name_len+extra_len+comment_len
        if end>offset+size: raise ValueError('truncated central metadata')
        name=data[position+46:position+46+name_len].decode('utf-8' if flags&0x800 else 'cp437','strict')
        safe_name(name); names.append(name); expanded+=unpacked
        if expanded>MAX_TOTAL: raise ValueError('unsafe expanded inventory size')
        extra=position+46+name_len; extra_end=extra+extra_len
        while extra<extra_end:
            if extra+4>extra_end: raise ValueError('invalid central extra field')
            key,length=struct.unpack_from('<HH',data,extra)
            if key==1 or extra+4+length>extra_end: raise ValueError('unsupported ZIP64 or truncated extra field')
            extra+=4+length
        position=end
    if position!=offset+size or len({name.casefold() for name in names})!=len(names) or prefix_conflicts(names):
        raise ValueError('ambiguous central inventory')


def verify_bundle(archive: Path, expected_version: str) -> list[str]:
    if not isinstance(expected_version, str) or not VERSION.fullmatch(expected_version):
        return ["bundle: invalid expected version"]
    try:
        # Verify the actual opened archive is regular and bound its compressed bytes.
        data = read_bytes(archive, MAX_ARCHIVE)
        preflight_zip(data)
        import io
        with zipfile.ZipFile(io.BytesIO(data)) as bundle:
            members = bundle.infolist()
            if not members or len(members) > MAX_MEMBERS:
                return ["bundle: unsafe member inventory"]
            names = set(); aliases = set(); total = 0
            for member in members:
                safe_name(member.filename)
                # NUL names can be truncated by ZipInfo; reject original spelling too.
                if member.orig_filename != member.filename:
                    return ["bundle: ambiguous member name"]
                if member.filename in names or member.filename.casefold() in aliases:
                    return ["bundle: duplicate or case-colliding entry"]
                names.add(member.filename); aliases.add(member.filename.casefold())
                kind = stat.S_IFMT(member.external_attr >> 16)
                if member.is_dir() or kind not in (0, stat.S_IFREG) or member.flag_bits & 1:
                    return ["bundle: nonregular or encrypted member rejected"]
                if member.compress_type not in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED):
                    return ["bundle: unsupported compression"]
                total += member.file_size
                if (member.file_size > MAX_FILE or total > MAX_TOTAL or
                        member.file_size > max(member.compress_size, 1) * 200):
                    return ["bundle: unsafe archive sizes"]
                if member.filename != "bundle.json":
                    parts = member.filename.split("/", 1)
                    if len(parts) != 2 or parts[0] not in SKILLS or not allowed_file(parts[1]):
                        return ["bundle: unlisted or forbidden archive entry"]
            if prefix_conflicts(names): return ["bundle: file/directory prefix conflict"]
            # Read only after the complete central-directory inventory is admitted.
            files = {}
            for member in members:
                with bundle.open(member) as handle:
                    item = handle.read(MAX_FILE + 1)
                if len(item) != member.file_size or len(item) > MAX_FILE:
                    return ["bundle: inconsistent member size"]
                files[member.filename] = item
            metadata = parse_json(files.get("bundle.json", b"null"))
            if metadata != {"format": "kumihan-bundle-1", "version": expected_version, "skills": list(SKILLS)}:
                return ["bundle: missing or invalid bundle metadata"]
            errors = []
            for skill in SKILLS:
                prefix = skill + "/"
                errors.extend(verify_skill_files({name[len(prefix):]: item for name, item in files.items()
                                                 if name.startswith(prefix)}, expected_version))
            return sorted(set(errors))
    except (OSError, ValueError, TypeError, zipfile.BadZipFile, zlib.error, EOFError, RuntimeError, NotImplementedError, RecursionError, MemoryError):
        return ["bundle: missing, invalid or unsafe archive"]


def main():
    parser = ResultParser(description=__doc__)
    parser.add_argument("--archive", required=True, type=Path)
    parser.add_argument("--expected-version", required=True)
    args = parser.parse_args()
    errors = verify_bundle(args.archive, args.expected_version)
    emit("incomplete" if errors else "passed", errors,
         limitations=["Inventory/digest/reference validation is not authenticity, Japanese visual quality or release approval."])
    if errors:
        print("Bundle rejected; see sanitized diagnostics.", file=sys.stderr)
    return 2 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
