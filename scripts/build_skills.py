"""Deterministic consumer data packaging; development-only builder."""
from datetime import datetime, timezone
import hashlib
import json
import os
import posixpath
import re
from pathlib import Path
import stat
import sys
import zipfile

try:
    from .validate_catalog import load_catalog, rule_profile_data, read_bytes, safe_name, VERSION, SCHEMA_HASHES, emit, ResultParser, InputContentError, PinnedDirectory, MAX_FILE
    from .verify_bundle import SKILLS, MAX_MEMBERS, MAX_TOTAL, verify_skill_files, local_targets, dependency_references, dependency_target
except ImportError:
    from validate_catalog import load_catalog, rule_profile_data, read_bytes, safe_name, VERSION, SCHEMA_HASHES, emit, ResultParser, InputContentError, PinnedDirectory, MAX_FILE
    from verify_bundle import SKILLS, MAX_MEMBERS, MAX_TOTAL, verify_skill_files, local_targets, dependency_references, dependency_target


def canonical(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")


def build_arguments(root, output_dir, version, source_epoch):
    if not isinstance(version, str) or not VERSION.fullmatch(version):
        raise ValueError("builder: invalid version")
    # ZIP's representable UTC range. Odd seconds are deterministically truncated
    # by the ZIP DOS timestamp, while the exact epoch is preserved in provenance.
    if type(source_epoch) is not int or not 0 <= source_epoch <= 4354819198:
        raise ValueError("builder: epoch outside supported ZIP UTC range")
    root = Path(root).absolute(); output = Path(output_dir).absolute()
    for component in [*reversed(output.parents), output]:
        if component.is_symlink():
            raise ValueError("builder: symlink output rejected")
    if output.exists():
        raise ValueError("builder: output directory already exists")
    if not root.is_dir() or root.is_symlink():
        raise ValueError("builder: invalid source root")
    if any(output.resolve().is_relative_to((root / name).resolve()) for name in ("rules", "profiles", "sources", "schemas", "skill-src")):
        raise ValueError("builder: output directory overlaps consumer inputs")
    if not output.parent.is_dir():
        raise ValueError("builder: output parent directory missing")
    return root, output, datetime.fromtimestamp(max(source_epoch, 315532800), timezone.utc).timetuple()[:6]



class _Budget:
    def __init__(self): self.used=0; self.members=0
    def add(self,data):
        if len(data)>MAX_FILE or self.used+len(data)>MAX_TOTAL or self.members+1>MAX_MEMBERS:
            raise InputContentError('builder: cumulative byte/member budget exceeded')
        self.used+=len(data); self.members+=1
    def read(self,path):
        remaining=min(MAX_FILE,MAX_TOTAL-self.used)
        try: return read_bytes(path,remaining)
        except ValueError: raise InputContentError('builder: unsafe or over-budget source input') from None


def _source_files(directory):
    """Stream bounded metadata through pinned descriptors; never follow links."""
    files=[]; seen=0
    with PinnedDirectory(directory) as base:
        stack=[(os.dup(base.fd),'')]
        try:
            while stack:
                fd,prefix=stack.pop()
                try:
                    with os.scandir(fd) as entries:
                        for entry in entries:
                            seen+=1
                            if seen>MAX_MEMBERS: raise InputContentError('builder: source inventory budget exceeded')
                            name=prefix+entry.name; safe_name(name)
                            if len(name.encode('ascii'))>512: raise InputContentError('builder: source name budget exceeded')
                            mode=entry.stat(follow_symlinks=False).st_mode
                            if stat.S_ISLNK(mode): raise ValueError('builder: symlink input rejected')
                            if stat.S_ISDIR(mode):
                                if name!='references' and not name.startswith('references/'): raise InputContentError('builder: unlisted source directory')
                                child=os.open(entry.name,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd)
                                stack.append((child,name+'/'))
                            elif stat.S_ISREG(mode):
                                if name!='SKILL.md' and not (name.startswith('references/') and Path(name).suffix in {'.md','.json'}):
                                    raise InputContentError('builder: forbidden source file')
                                files.append(name)
                            else: raise ValueError('builder: nonregular source input')
                finally: os.close(fd)
            base.check()
        finally:
            for fd,_ in stack: os.close(fd)
    return sorted(files)


def _rewrite_material(name,data,resolve):
    """Rewrite only supported declared dependencies; preserve other source text."""
    declarations=dependency_references(name,data)
    mappings={}
    for literal,required,qualified in declarations:
        installed=resolve(literal,required,qualified)
        if installed is None: continue
        relative=posixpath.relpath(installed,posixpath.dirname(name) or '.')
        fragment=literal.split('#',1)[1] if '#' in literal else ''
        mappings[literal]=relative+('#'+fragment if fragment else '')
    if not mappings or all(literal==relative for literal,relative in mappings.items()): return data
    if name.endswith('.json'):
        from_json=__import__('json').loads(data.decode('utf-8'))
        def replace(node):
            if isinstance(node,dict):
                for key,value in node.items():
                    if key in ('$ref','include'):
                        node[key]=[mappings.get(item,item) for item in value] if isinstance(value,list) else mappings.get(value,value)
                    else: replace(value)
            elif isinstance(node,list):
                for value in node: replace(value)
        replace(from_json)
        return canonical(from_json)
    text=data.decode('utf-8')
    for literal,relative in sorted(mappings.items(),key=lambda pair:(-len(pair[0]),pair[0])):
        text=text.replace(literal,relative)
    return text.encode('utf-8')


def _package_validated_inputs(root, output_dir, version, source_epoch, destination):
    root,output,timestamp=build_arguments(root,output_dir,version,source_epoch)
    rules,profiles=rule_profile_data(root); budget=_Budget()
    common={'LICENSE':read_bytes(root/'LICENSE'),'rules/catalog.json':canonical(rules),
            'sources/public-sources.json':read_bytes(root/'sources/public-sources.json')}
    for name in SCHEMA_HASHES: common[f'schemas/{name}.schema.json']=read_bytes(root/f'schemas/{name}.schema.json')
    for profile in profiles: common[f"profiles/{profile['id']}.json"]=canonical(profile)
    provenance=canonical({'builder_version':'0.1.0','version':version,'source_epoch':source_epoch,
        'license':'LICENSE','sources':'sources/public-sources.json',
        'limitations':['Structural packaging does not authenticate approvals, source authority or Japanese visual quality.']})
    source=root/'skill-src'
    with PinnedDirectory(source) as directory:
        names=set()
        with os.scandir(directory.fd) as entries:
            for entry in entries:
                names.add(entry.name)
                if len(names)>len(SKILLS)+1: raise InputContentError('builder: unlisted skill source directory')
        directory.check()
    if not set(SKILLS)<=names or names-set(SKILLS)-{'shared'}:
        raise ValueError('builder: missing or unlisted skill source directory')
    archive_files={'bundle.json':canonical({'format':'kumihan-bundle-1','version':version,'skills':list(SKILLS)})}
    budget.add(archive_files['bundle.json'])
    for skill in SKILLS:
        directory=source/skill; source_names=_source_files(directory)
        files=dict(common); files['references/provenance.json']=provenance
        for data in files.values(): budget.add(data)
        pending=['SKILL.md']; selected=set(); installed_sources={}; local_selected=set()
        def locate(target):
            if target in common: return ('common',target,target)
            if target=='references/architecture.md':
                if (directory/target).exists(): raise InputContentError('builder: authored duplicate of generated architecture')
                return ('architecture','docs/architecture.md',target)
            if target.startswith('shared/'):
                relative=target[len('shared/'):]; safe_name(relative)
                installed='references/'+relative
                if (directory/installed).exists(): raise InputContentError('builder: local/shared source collision')
                return ('shared',relative,installed)
            if target.startswith('references/'):
                relative=target[len('references/'):]
                local=target in source_names; shared='shared' in names and (source/'shared'/relative).exists()
                if local and shared: raise InputContentError('builder: local/shared source collision')
                if shared: return ('shared',relative,target)
            if target not in source_names: raise InputContentError('builder: missing or unsupported source reference')
            return ('local',target,target)
        while pending:
            token=pending.pop()
            kind,relative,installed=locate(token)
            if kind=='common': continue
            identity=(kind,relative)
            if installed in installed_sources and installed_sources[installed]!=identity:
                raise InputContentError('builder: installed source collision')
            installed_sources[installed]=identity
            if identity in selected: continue
            if kind=='local': path=directory/relative; local_selected.add(relative); source_key=skill+'/'+relative
            elif kind=='shared': path=source/'shared'/relative; source_key='shared/'+relative
            else: path=root/relative; source_key=relative
            if Path(relative).suffix not in {'.md','.json'}: raise InputContentError('builder: unsupported consumer source role')
            raw=budget.read(path); selected.add(identity)
            def resolve(literal,required,qualified):
                if literal.startswith(('http://','https://','mailto:')):
                    if required: raise InputContentError('builder: network dependency')
                    return None
                if literal.startswith('#'): return None
                if literal.startswith('urn:'):
                    target=dependency_target(installed,literal,required,qualified)
                elif literal.split('#',1)[0] in {schema+'.schema.json' for schema in SCHEMA_HASHES}:
                    target='schemas/'+literal.split('#',1)[0]
                elif qualified and literal.split('#',1)[0]=='docs/architecture.md': target='references/architecture.md'
                elif qualified and literal.startswith(('schemas/','profiles/','rules/','sources/')): target=literal.split('#',1)[0]
                else:
                    head=literal.split('#',1)[0]
                    if not head or head.startswith('/') or any(char in head for char in ('\\',':','%','?')):
                        raise InputContentError('builder: unsafe dependency')
                    resolved=posixpath.normpath(posixpath.join(posixpath.dirname(source_key),head))
                    if resolved.startswith(skill+'/'): target=resolved[len(skill)+1:]
                    elif resolved.startswith('shared/'): target=resolved
                    elif resolved=='docs/architecture.md': target='references/architecture.md'
                    else: raise InputContentError('builder: sibling or ambient dependency')
                route=locate(target); pending.append(target)
                return route[2]
            try: data=_rewrite_material(installed,raw,resolve)
            except (ValueError,UnicodeError,TypeError,KeyError) as error:
                message='builder: restricted host control material' if str(error)=='restricted host control data' else 'builder: invalid or unsupported declared dependency'
                raise InputContentError(message) from None
            budget.add(data); files[installed]=data
        if set(source_names)-local_selected: raise InputContentError('builder: unreferenced skill source file')
        inv=canonical({'format':'kumihan-skill-1','version':version,
            'files':{name:'sha256:'+hashlib.sha256(data).hexdigest() for name,data in sorted(files.items())}})
        budget.add(inv); files['inventory.json']=inv
        errors=verify_skill_files(files,version)
        if errors: raise InputContentError('builder: '+ '; '.join(errors))
        archive_files.update({skill+'/'+name:data for name,data in files.items()})
    # Exclusive creation is relative to a retained no-follow parent, not a
    # previously checked pathname. A substituted ancestor cannot redirect writes.
    destination.check(); created=False; outfd=None; archive_name=f'kumihan-{version}.zip'
    try:
        os.mkdir(output.name,mode=0o755,dir_fd=destination.fd); created=True
        destination.check()
        outfd=os.open(output.name,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=destination.fd)
        with os.fdopen(os.open(archive_name,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644,dir_fd=outfd),'wb') as handle:
            with zipfile.ZipFile(handle,'w',compression=zipfile.ZIP_STORED,allowZip64=False) as bundle:
                for name,data in sorted(archive_files.items()):
                    info=zipfile.ZipInfo(name,timestamp); info.create_system=3; info.external_attr=(stat.S_IFREG|0o644)<<16
                    info.compress_type=zipfile.ZIP_STORED; bundle.writestr(info,data)
        destination.check()
        entry=os.stat(output.name,dir_fd=destination.fd,follow_symlinks=False); actual=os.fstat(outfd)
        if not stat.S_ISDIR(entry.st_mode) or (entry.st_dev,entry.st_ino)!=(actual.st_dev,actual.st_ino):
            raise ValueError('builder: output namespace changed')
    except BaseException:
        if created and outfd is None:
            try: os.rmdir(output.name,dir_fd=destination.fd)
            except OSError: pass
        raise
    finally:
        if outfd is not None: os.close(outfd)
    return output/archive_name


def build_skills(root: Path, output_dir: Path, version: str, source_epoch: int) -> Path:
    build_arguments(root,output_dir,version,source_epoch)
    with PinnedDirectory(Path(output_dir).absolute().parent) as destination:
        load_catalog(root)
        return _package_validated_inputs(root,output_dir,version,source_epoch,destination)


def main():
    parser = ResultParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--version", required=True)
    parser.add_argument("--source-epoch", required=True, type=int)
    args = parser.parse_args()
    try:
        archive = build_skills(args.root, args.output_dir, args.version, args.source_epoch)
        emit("passed", [], archive=archive.name, digest="sha256:" + hashlib.sha256(read_bytes(archive, MAX_TOTAL)).hexdigest())
        return 0
    except InputContentError:
        emit("failed", ["builder: verified input-content failure"])
        print("Build rejected; input content violates a verified invariant.", file=sys.stderr)
        return 1
    except (ValueError, OSError, MemoryError):
        emit("incomplete", ["builder: invalid arguments, conflicting output, I/O or unavailable/invalid input content"])
        print("Build rejected; see sanitized diagnostics.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
