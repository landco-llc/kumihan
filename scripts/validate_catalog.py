"""Offline frozen schema support and catalog validation (development only)."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import stat

from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.exceptions import NoSuchResource

SCHEMA_HASHES = {
    "design-contract": "a38b3720b0b1a113a53bba4552bcc866f44f900db94b8187962038fe7a7555b9",
    "profile": "dc2e9397d380f3260b0a69f6dd8b72980e3eb2b326a02ba343537f744b6ccbce",
    "release-manifest": "1bda6b026d34932a66060c8435d8d5e31a20791c410971acc063192581ab1b36",
    "report": "4396bcbc1f709f6d451319ad93dbd891436ab367865969bcd958c1cdad998d7a",
    "rule": "132eda194cd883d32dd833714b75fee5da0d6a254c5d30459cccb1528538afb5",
}
MAX_FILE = 2 * 1024 * 1024
VERSION = re.compile(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-[0-9A-Za-z.-]+)?", re.ASCII)


def safe_name(name):
    """Portable relative data path; avoid platform aliases and Unicode ambiguity."""
    if not isinstance(name, str) or not name or not re.fullmatch(r"[A-Za-z0-9_./-]+", name):
        raise ValueError("invalid portable path")
    for part in name.split("/"):
        if (part in ("", ".", "..") or part.endswith(".") or
                part.split(".")[0].upper() in {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}):
            raise ValueError("invalid portable path")
    return name



class PinnedDirectory:
    """POSIX no-follow walk; retained ancestors prevent pathname redirection."""
    def __init__(self, path, *, anchor_fd=None):
        self.path=Path(path) if anchor_fd is not None else Path(path).absolute(); self.fds=[]; self.chain=[]
        if '..' in self.path.parts or os.name!='posix' or not hasattr(os,'O_NOFOLLOW'):
            raise ValueError('unsupported safe directory access')
        if anchor_fd is not None and self.path.is_absolute():
            raise ValueError('absolute capability-relative path rejected')
        flags=os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW
        try:
            current=os.dup(anchor_fd) if anchor_fd is not None else os.open('/',flags); self.fds.append(current)
            components=self.path.parts if anchor_fd is not None else self.path.parts[1:]
            for name in components:
                child=os.open(name,flags,dir_fd=current); self.fds.append(child)
                entry=os.stat(name,dir_fd=current,follow_symlinks=False); actual=os.fstat(child)
                if not stat.S_ISDIR(entry.st_mode) or (entry.st_dev,entry.st_ino)!=(actual.st_dev,actual.st_ino):
                    raise ValueError('directory namespace changed')
                self.chain.append((current,name,(actual.st_dev,actual.st_ino))); current=child
            self.fd=current; self.check()
        except BaseException:
            self.close(); raise
    def check(self):
        for parent,name,identity in self.chain:
            entry=os.stat(name,dir_fd=parent,follow_symlinks=False)
            if not stat.S_ISDIR(entry.st_mode) or (entry.st_dev,entry.st_ino)!=identity:
                raise ValueError('directory namespace changed')
    def close(self):
        for fd in reversed(self.fds): os.close(fd)
        self.fds=[]
    def __enter__(self): return self
    def __exit__(self,*args): self.close()


def read_bytes(path, limit=MAX_FILE, *, anchor_fd=None):
    """Read a consistent regular file through pinned no-follow ancestors."""
    path=Path(path) if anchor_fd is not None else Path(path).absolute()
    with PinnedDirectory(path.parent,anchor_fd=anchor_fd) as parent:
        flags=os.O_RDONLY|os.O_NONBLOCK|os.O_NOFOLLOW
        with os.fdopen(os.open(path.name,flags,dir_fd=parent.fd),'rb') as handle:
            before=os.fstat(handle.fileno())
            if not stat.S_ISREG(before.st_mode): raise ValueError('nonregular input rejected')
            if before.st_size>limit: raise ValueError('input exceeds size limit')
            data=handle.read(before.st_size+1)
            after=os.fstat(handle.fileno()); entry=os.stat(path.name,dir_fd=parent.fd,follow_symlinks=False)
            signature=lambda item:(item.st_dev,item.st_ino,item.st_mode,item.st_size,item.st_mtime_ns,item.st_ctime_ns)
            if signature(before)!=signature(after) or signature(after)!=signature(entry) or len(data)!=after.st_size:
                raise ValueError('input changed during read')
        parent.check()
    return data


class StableInputs:
    """Retain data and file/ancestor handles for one admission operation.

    Check each retained identity/signature again at the decision boundary.
    This detects concurrent replacement/editing; it is not a kernel write lock.
    The host must protect writers during admission and subsequent artifact use.
    """
    def __init__(self): self.records={}; self.used=0
    @staticmethod
    def signature(info):
        return (info.st_dev,info.st_ino,info.st_mode,info.st_size,info.st_mtime_ns,info.st_ctime_ns)
    def read(self,path):
        path=Path(path).absolute()
        if path in self.records: return self.records[path][3]
        if len(self.records)>=1024: raise ValueError('admission inventory budget exceeded')
        parent=PinnedDirectory(path.parent); fd=None
        try:
            fd=os.open(path.name,os.O_RDONLY|os.O_NONBLOCK|os.O_NOFOLLOW,dir_fd=parent.fd)
            info=os.fstat(fd)
            if not stat.S_ISREG(info.st_mode) or info.st_size>MAX_FILE or self.used+info.st_size>64*1024*1024:
                raise ValueError('admission input budget/type rejected')
            with os.fdopen(os.dup(fd),'rb') as handle: data=handle.read(info.st_size+1)
            if len(data)!=info.st_size: raise ValueError('input changed during admission')
            self.records[path]=(parent,fd,self.signature(info),data); self.used+=len(data)
            parent=None; fd=None; self.check()
            return data
        finally:
            if fd is not None: os.close(fd)
            if parent is not None: parent.close()
    def check(self):
        for path,(parent,fd,signature,_) in self.records.items():
            parent.check()
            current=os.stat(path.name,dir_fd=parent.fd,follow_symlinks=False)
            if self.signature(os.fstat(fd))!=signature or self.signature(current)!=signature:
                raise ValueError('input changed during admission')
    def __enter__(self): return self
    def __exit__(self,*args):
        for parent,fd,_,_ in self.records.values(): os.close(fd); parent.close()
        self.records={}


def _pairs(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError("duplicate JSON key")
        value[key] = item
    return value


def parse_json(data):
    try:
        if isinstance(data, bytes):
            data = data.decode("utf-8", "strict")
        return json.loads(data, object_pairs_hook=_pairs,
                          parse_float=_finite_float,
                          parse_constant=lambda _: (_ for _ in ()).throw(ValueError("nonfinite JSON")))
    except (UnicodeError, json.JSONDecodeError, RecursionError):
        raise ValueError("invalid UTF-8 JSON") from None


def _finite_float(value):
    parsed = float(value)
    if not math.isfinite(parsed):
        raise ValueError("nonfinite JSON")
    return parsed


def read_json(path):
    return parse_json(read_bytes(path))


def _offline(uri):
    raise NoSuchResource(ref=uri)


def validators(root=None):
    root = Path(root) if root is not None else Path(__file__).resolve().parents[1]
    try:
        return validators_from_bytes({name: read_bytes(root / "schemas" / (name + ".schema.json"))
                                      for name in SCHEMA_HASHES})
    except (OSError, ValueError) as error:
        raise ValueError("missing, invalid or unsupported local schemas") from error


def validators_from_bytes(resources):
    """Register exact frozen resources without any repository or network lookup."""
    schemas = {}
    for name, digest in SCHEMA_HASHES.items():
        data = resources.get(name)
        if data is None or hashlib.sha256(data).hexdigest() != digest:
            raise ValueError("missing or unsupported frozen schema")
        schema = parse_json(data)
        Draft202012Validator.check_schema(schema)
        schemas[name] = schema
    registry = Registry(retrieve=_offline).with_resources(
        (schema["$id"], Resource.from_contents(schema)) for schema in schemas.values())
    return {name: Draft202012Validator(schema, registry=registry) for name, schema in schemas.items()}


def schema_errors(validator, value, label):
    # Do not echo untrusted instance values, schema messages or operating paths.
    # Dynamic map keys (e.g. environment.tools) are instance content too.
    return sorted({f"{label}: schema violation ({error.validator})"
                   for error in validator.iter_errors(value)})


def emit(status, errors, **details):
    print(json.dumps({"status": status, "errors": sorted(set(errors)), **details}, sort_keys=True))


class ResultParser(argparse.ArgumentParser):
    def error(self, message):
        # argparse includes untrusted argument values in its default diagnostics.
        emit("incomplete", ["CLI: missing or invalid arguments"])
        self.exit(2, "Invalid arguments; use --help for the contract.\n")


class InputContentError(ValueError):
    """Readable local product input violates a verified data invariant."""


def binding_digest(value):
    data=json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode('utf-8')
    return 'sha256:'+hashlib.sha256(data).hexdigest()


def utc_now():
    from datetime import datetime, timezone
    return datetime.now(timezone.utc)


def utc_stamp(value):
    from datetime import datetime, timezone
    if not isinstance(value,str) or not re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z',value):
        raise ValueError('invalid canonical UTC timestamp')
    try: return datetime.strptime(value,'%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
    except ValueError: raise ValueError('invalid canonical UTC timestamp') from None


def nonblank(value): return isinstance(value,str) and bool(value.strip())


class HostAuthority:
    """Explicit host-inherited read-only capability, never an instance locator.

    KUMIHAN_HOST_CONTEXT_FD designates the host's private authority directory;
    authority.json is read freshly at every decision, including atomic updates. The host must control process environment/descriptors and maintain
    this ledger as its latest identity, policy, state and observed-proof source.
    It is re-read at every admission within the retained directory inode.
    The protected writer must update authority.json in that inode, or invalidate
    and reissue capabilities when rotating directories. A read-only FD alone
    does not freeze descendants or establish the latest state at another path.
    These checks do not turn arbitrary JSON or synthetic fixtures into real
    identity/approval evidence. No referenced code is executed or fetched.
    """
    def __init__(self, untrusted_root=None):
        if os.name!='posix': raise ValueError('host capability unsupported on this platform')
        import fcntl
        from datetime import timedelta
        raw=os.environ.get('KUMIHAN_HOST_CONTEXT_FD','')
        if not re.fullmatch(r'[0-9]{1,9}',raw) or int(raw)<3: raise ValueError('trusted host capability unavailable')
        fd=int(raw); info=os.fstat(fd)
        if fcntl.fcntl(fd,fcntl.F_GETFL)&os.O_ACCMODE != os.O_RDONLY or not stat.S_ISDIR(info.st_mode):
            raise ValueError('host capability must be a read-only directory')
        if info.st_uid!=os.getuid() or info.st_mode&0o077: raise ValueError('invalid private host capability')
        target=os.readlink('/proc/self/fd/'+str(fd)); path=Path(target)
        if not path.is_absolute() or target.endswith(' (deleted)'): raise ValueError('stale host capability')
        if untrusted_root is not None and path.is_relative_to(Path(untrusted_root).absolute()):
            raise ValueError('host authority is inside untrusted inputs')
        self.fd=fd; self.directory=path; self.intervals=[]
        self.data=self.read_ledger(); self.now=utc_now()
        if self.now is None or self.now.tzinfo is None or self.now.utcoffset()!=timedelta(0):
            raise ValueError('trusted UTC decision time unavailable')
        keys={'format','generation','principals','grants','observations','approvals','approval_states','procedures','chronologies'}
        if not isinstance(self.data,dict) or set(self.data)!=keys or self.data['format']!='kumihan-host-authority-1':
            raise ValueError('invalid host authority format')
        if type(self.data['generation']) is not int or self.data['generation']<1 or not isinstance(self.data['principals'],dict):
            raise ValueError('invalid host authority generation')
        if any(not isinstance(self.data[key],list) or len(self.data[key])>1024 for key in keys-{'format','generation','principals'}):
            raise ValueError('invalid host authority inventory')

    def read_ledger(self):
        with os.fdopen(os.open('authority.json',os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=self.fd),'rb') as handle:
            info=os.fstat(handle.fileno())
            if not stat.S_ISREG(info.st_mode) or info.st_uid!=os.getuid() or info.st_mode&0o077 or info.st_size>MAX_FILE:
                raise ValueError('invalid private authority ledger')
            data=handle.read(info.st_size+1); after=os.fstat(handle.fileno())
        signature=lambda item:(item.st_dev,item.st_ino,item.st_size,item.st_mtime_ns,item.st_ctime_ns)
        current=os.stat('authority.json',dir_fd=self.fd,follow_symlinks=False)
        if signature(info)!=signature(after) or signature(after)!=signature(current):
            raise ValueError('authority ledger changed during read')
        self.signature=signature(after)
        return parse_json(data)

    def finish(self):
        from datetime import timedelta
        decision=utc_now()
        if decision is None or decision.tzinfo is None or decision.utcoffset()!=timedelta(0):
            raise ValueError('trusted decision clock unavailable')
        for record in self.intervals:
            if not utc_stamp(record['issued_at'])<=decision<utc_stamp(record['expires_at']):
                raise ValueError('authority expired at admission')
        directory=os.fstat(self.fd)
        if directory.st_uid!=os.getuid() or directory.st_mode&0o077:
            raise ValueError('host directory protection changed during admission')
        current=os.stat('authority.json',dir_fd=self.fd,follow_symlinks=False)
        if current.st_uid!=os.getuid() or current.st_mode&0o077 or not stat.S_ISREG(current.st_mode):
            raise ValueError('host ledger protection changed during admission')
        if (current.st_dev,current.st_ino,current.st_size,current.st_mtime_ns,current.st_ctime_ns)!=self.signature:
            raise ValueError('host ledger changed during admission')

    def lookup(self,group,predicate):
        matches=[row for row in self.data[group] if isinstance(row,dict) and predicate(row)]
        if len(matches)!=1: raise ValueError('missing or ambiguous trusted record')
        return matches[0]

    def interval(self, record, at=None):
        issued=utc_stamp(record.get('issued_at')); expires=utc_stamp(record.get('expires_at')); at=self.now if at is None else at
        if not issued<expires or not issued<=at<expires: raise ValueError('expired or not-yet-issued authority')
        if at is self.now: self.intervals.append(record)
        return issued

    def principal(self, reference, purpose, rule_id, scope, bounds, issued=None, at=None):
        principal=self.data['principals'].get(reference)
        if not nonblank(reference) or not isinstance(principal,dict) or not nonblank(principal.get('identity_ref')) or principal.get('state')!='active':
            raise ValueError('unresolved trusted principal')
        grant=self.lookup('grants',lambda row:all(row.get(key)==value for key,value in
            {'principal_ref':reference,'purpose':purpose,'rule_id':rule_id,'scope':scope,'bounds':bounds}.items()))
        if grant.get('state')!='current': raise ValueError('authority revoked')
        self.interval(grant,at)
        if issued is not None: self.interval(grant,issued)

    def record_file(self, reference):
        if not isinstance(reference,dict) or set(reference)!={'path','digest'}: raise ValueError('invalid trusted proof locator')
        data=read_bytes(safe_name(reference['path']),anchor_fd=self.fd)
        if 'sha256:'+hashlib.sha256(data).hexdigest()!=reference['digest']: raise ValueError('trusted proof digest mismatch')
        return data

    def observation(self, report, check, reference, data, item):
        binding={key:report[key] for key in ('report_id','artifact_ref','artifact_digest')}
        binding.update(reference=reference,rule_id=check['rule_id'],scope=check['scope'],method=check['method'])
        record=self.lookup('observations',lambda row:all(row.get(key)==value for key,value in binding.items()))
        if record.get('status')!='passed' or record.get('evidence_digest')!='sha256:'+hashlib.sha256(data).hexdigest():
            raise ValueError('observation is not an exact observed pass')
        observed=utc_stamp(record.get('observed_at'))
        if observed>self.now: raise ValueError('observation is from the future')
        self.principal(record.get('observer_ref'),'observation',check['rule_id'],check['scope'],report['artifact_digest'],observed)
        value=self.design_evidence(data,item)
        if value is not None:
            generation=self.design_chronology(value,data,report,check,item)
            if observed<generation: raise ValueError('design observation predates generation')

    @staticmethod
    def design_evidence(data,item):
        # DESIGN-001 is the frozen pre-generation contract rule. Its evidence
        # role is required regardless of an instance-controlled filename suffix.
        required=item['id']=='DESIGN-001'
        try: value=parse_json(data)
        except ValueError:
            if required or data.lstrip().startswith((b'{',b'[')): raise
            return None
        if required and (not isinstance(value,dict) or 'brief_id' not in value):
            raise ValueError('missing required design-contract evidence')
        return value if isinstance(value,dict) and 'brief_id' in value else None

    def approval(self, requesting, purpose, subject, item, at=None):
        record=self.lookup('approvals',lambda row:row.get('approval_ref')==requesting['approval_ref'])
        required={'approval_ref','purpose','approver_ref','issued_at','expires_at','scope','reason','subject','state','revision'}
        if set(record)!=required or type(record.get('revision')) is not int or record['revision']<1:
            raise ValueError('incomplete trusted approval')
        state=self.lookup('approval_states',lambda row:row.get('approval_ref')==record['approval_ref'])
        if type(state.get('revision')) is not int or state['revision']<1 or state.get('revision')!=record['revision'] or state.get('state')!='current' or record['state']!='current':
            raise ValueError('approval revoked or superseded')
        if (record['purpose']!=purpose or record['subject']!=subject or record['scope']!=requesting['scope'] or
                record['reason']!=requesting['reason'] or not nonblank(record['reason']) or not item['exception_policy']['allowed']):
            raise ValueError('approval binding or catalog bounds mismatch')
        issued=self.interval(record,at)
        self.principal(record['approver_ref'],purpose,item['id'],record['scope'],item['exception_policy']['bounds'],issued,at)

    def design_chronology(self, contract, data, report, check, item):
        if schema_errors(validators()['design-contract'],contract,'design'): raise ValueError('invalid design evidence')
        digest='sha256:'+hashlib.sha256(data).hexdigest()
        record=self.lookup('chronologies',lambda row:row.get('brief_id')==contract['brief_id'] and
            row.get('design_contract_digest')==digest and row.get('artifact_digest')==report['artifact_digest'])
        created=utc_stamp(record.get('created_at')); generation=utc_stamp(record.get('generation_started_at'))
        if not created<generation<=self.now: raise ValueError('design contract was not recorded before generation')
        brief=parse_json(self.record_file(record.get('brief')))
        if not isinstance(brief,dict) or brief.get('brief_id')!=contract['brief_id']: raise ValueError('retained brief mismatch')
        mode=record.get('mode')
        if mode not in ('generate','refine') or record.get('scope')!=check['scope']: raise ValueError('missing bounded production permission')
        self.principal(record.get('owner_ref'),mode,check['rule_id'],check['scope'],digest,created,generation)
        # This verifies retained host evidence, and never performs or retroactively
        # authorizes generation/refinement. Design-exception ownership stays host-side.
        subject={'brief_id':contract['brief_id'],'design_contract_digest':digest}
        for request in contract['exceptions']:
            self.approval(request,'design-exception',subject,item,generation)
            self.approval(request,'design-exception',subject,item)
        return generation

    def procedure(self, item):
        digest=binding_digest(item)
        proof=self.lookup('procedures',lambda row:row.get('rule_id')==item['id'] and row.get('rule_digest')==digest)
        method=item['verification']['method']; expected='detector' if method=='static' else 'review-procedure'
        if proof.get('method')!=method or proof.get('kind')!=expected or proof.get('state')!='current':
            raise ValueError('unverified procedure kind/state')
        definition=self.record_file(proof.get('definition')); tests=proof.get('tests')
        if not isinstance(tests,list) or not tests or len(tests)>128: raise ValueError('missing relevant procedure tests')
        for test in tests: self.record_file(test)
        result=parse_json(self.record_file(proof.get('result')))
        binding={'rule_id':item['id'],'rule_digest':digest,'method':method,'definition_digest':proof['definition']['digest'],
                 'test_digests':[test['digest'] for test in tests],'case_ids':item['case_ids'],'status':'passed'}
        if not isinstance(result,dict) or any(result.get(key)!=value for key,value in binding.items()) or not item['case_ids']:
            raise ValueError('test result does not bind relevant procedure/tests')
        tested=utc_stamp(result.get('tested_at'))
        if tested>self.now: raise ValueError('procedure test is from the future')
        self.principal(proof.get('reviewer_ref'),'procedure-admission',item['id'],'catalog',digest,tested)


def implemented_errors(rules, untrusted_root=None):
    implemented=[item for item in rules if item['verification']['coverage']=='implemented']
    if not implemented: return []
    try:
        authority=HostAuthority(untrusted_root)
        for item in implemented: authority.procedure(item)
        authority.finish(); return []
    except (OSError,ValueError,KeyError,TypeError,MemoryError):
        return ['catalog: implemented coverage lacks verified procedure/tests']


def json_inputs(directory):
    """Flat, explicit JSON input directory; no recursive or extension-based surprises."""
    directory = Path(directory)
    if not directory.is_dir() or directory.is_symlink():
        raise ValueError("catalog: missing or unsafe input directory")
    paths = sorted(directory.iterdir())
    if not paths or len(paths) > 128:
        raise ValueError("catalog: missing or excessive input inventory")
    aliases = set()
    for path in paths:
        safe_name(path.name)
        if path.name.casefold() in aliases:
            raise ValueError("catalog: case-colliding input names")
        aliases.add(path.name.casefold())
        if path.suffix != ".json" or path.is_symlink() or not path.is_file():
            raise ValueError("catalog: symlink, unlisted or non-JSON input")
    return paths


def rule_profile_data(root):
    """Frozen rule/profile structure only; not source/fixture catalog admission."""
    root = Path(root)
    checks = validators(root)
    expected = checks["rule"].schema["$defs"]["rule_id"]["enum"]
    profile_ids = checks["rule"].schema["$defs"]["media_profile"]["enum"]
    errors = []; index = {}
    for path in json_inputs(root / "rules"):
        values = read_json(path)
        if not isinstance(values, list):
            errors.append("catalog: rule files must be JSON arrays")
            continue
        if len(values) > 256:
            errors.append("catalog: excessive rule inventory")
            continue
        for value in values:
            invalid = schema_errors(checks["rule"], value, "catalog rule")
            errors.extend(invalid)
            if invalid:
                continue
            if value["id"] in index:
                errors.append("catalog: duplicate rule ID")
            index[value["id"]] = value
    if set(expected) - index.keys():
        errors.append("catalog: missing rule IDs")
    profiles = {}
    for path in json_inputs(root / "profiles"):
        value = read_json(path)
        invalid = schema_errors(checks["profile"], value, "catalog profile")
        errors.extend(invalid)
        if invalid:
            continue
        if value["id"] in profiles:
            errors.append("catalog: duplicate profile ID")
        profiles[value["id"]] = value
        for identity in value["rule_ids"]:
            if identity not in index:
                errors.append("catalog: unresolved profile rule")
            elif value["id"] not in index[identity]["media"]:
                errors.append("catalog: profile rule media mismatch")
    if set(profile_ids) - profiles.keys():
        errors.append("catalog: missing profile IDs")
    errors.extend(implemented_errors(list(index.values()),root))
    if errors:
        raise InputContentError("; ".join(sorted(set(errors))))
    return [index[identity] for identity in expected], [profiles[identity] for identity in profile_ids]


def source_errors(registry, rules, checks):
    """Coordinated W02 registry shape; declarations are not source authority."""
    from datetime import date
    import ipaddress
    from urllib.parse import urlsplit
    text = {"type": "string", "pattern": r"\S", "minLength": 1}
    nullable = {"anyOf": [text, {"type": "null"}]}
    properties = {"id": text, "type": {"enum": checks["rule"].schema["properties"]["kind"]["enum"]},
        "classification": {"enum": ["adopted", "comparison-only", "deferred"]},
        "title": text, "url": nullable, "version": nullable, "accessed_at": nullable,
        "context": text, "adopted_principle": nullable, "limits": text, "statement": nullable,
        "rule_ids": {"type": "array", "uniqueItems": True, "items": checks["rule"].schema["$defs"]["rule_id"]}}
    shape = {"type": "object", "properties": {"registry_version": {"const": "0.1.0"},
        "sources": {"type": "array", "maxItems": 256, "items": {"type": "object", "properties": properties,
        "required": list(properties), "additionalProperties": False}}},
        "required": ["registry_version", "sources"], "additionalProperties": False}
    if schema_errors(Draft202012Validator(shape), registry, "source schema"):
        return ["catalog: source schema violation"]
    errors = []; sources = {}; index = {rule["id"]: rule for rule in rules}
    for source in registry["sources"]:
        identity = source["id"]
        if identity in sources:
            errors.append("catalog: duplicate source ID")
        sources[identity] = source
        if identity.startswith("policy:"):
            if source["type"] != "project-policy":
                errors.append("catalog: declared source kind mismatch")
            if source["url"] is not None or not isinstance(source["statement"], str) or not source["statement"].strip():
                errors.append("catalog: source schema missing authored policy statement/location")
        else:
            try:
                url = urlsplit(source["url"] or "")
                public = (url.scheme in ("http", "https") and url.hostname and not url.username and not url.password
                          and url.hostname not in {"localhost", "127.0.0.1", "::1"}
                          and not re.search(r"\s", source["url"] or ""))
                if public:
                    host = url.hostname.lower().rstrip(".")
                    if url.port is not None and not 1 <= url.port <= 65535:
                        public = False
                    try:
                        public = public and ipaddress.ip_address(host).is_global
                    except ValueError:
                        numeric = re.fullmatch(r"(?:0x[0-9a-f]+|[0-9]+)(?:\.(?:0x[0-9a-f]+|[0-9]+))*", host)
                        public = (public and not numeric and host not in {"localhost", "local", "internal"}
                                  and not host.endswith((".internal", ".local", ".localhost"))
                                  and bool(re.fullmatch(r"[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?", host))
                                  and ".." not in host)
            except ValueError:
                public = False
            if not public:
                errors.append("catalog: missing or unsupported public source URL")
            if source["type"] == "project-policy" or source["statement"] is not None:
                errors.append("catalog: declared source kind mismatch")
        if source["classification"] == "adopted":
            if any(not isinstance(source[field], str) or not source[field].strip() for field in ("version", "accessed_at", "adopted_principle")):
                errors.append("catalog: source schema missing adopted attribution")
            try:
                stamp = source["accessed_at"]
                if not isinstance(stamp, str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", stamp):
                    raise ValueError("invalid date")
                date.fromisoformat(stamp)
            except ValueError:
                errors.append("catalog: invalid source access date")
        elif source["rule_ids"] or source["adopted_principle"] is not None or source["statement"] is not None:
            errors.append("catalog: non-adopted source claims adopted coverage")
        for identity_rule in source["rule_ids"]:
            if identity_rule not in index or identity not in index[identity_rule]["source_refs"]:
                errors.append("catalog: unresolved or inconsistent source rule reference")
    for rule in rules:
        resolved = []
        for identity in rule["source_refs"]:
            source = sources.get(identity)
            if source is None:
                errors.append("catalog: unresolved source reference")
                continue
            if source["classification"] != "adopted":
                errors.append("catalog: non-adopted source reference")
            if rule["id"] not in source["rule_ids"]:
                errors.append("catalog: inconsistent source rule coverage")
            resolved.append(source)
        if resolved and not any(source["type"] == rule["kind"] for source in resolved):
            errors.append("catalog: declared source kind mismatch")
    return sorted(set(errors))



PRIORITY_IDS = ("CONTENT-001", "CONTENT-002", "CONTENT-004", "JA-TYPE-002", "JA-TYPE-004", "JA-TYPE-005", "JA-TYPE-006", "JA-TYPE-008", "JA-TYPE-009", "WEB-001", "WEB-004", "WEB-005", "DESIGN-001", "DESIGN-002", "EVIDENCE-001")


def case_errors(dataset, rules, profiles, checks):
    """Check fixture declarations/relationships; never run or upgrade assertions."""
    text = {"type": "string", "pattern": r"\S", "minLength": 1}
    properties = {"id": text, "rule_id": checks["rule"].schema["$defs"]["rule_id"],
        "kind": {"enum": ["positive", "negative", "exception"]},
        "profile": checks["rule"].schema["$defs"]["media_profile"],
        "input": {"type": "object", "minProperties": 1},
        "expected_status": checks["report"].schema["$defs"]["status"],
        "method": checks["rule"].schema["$defs"]["method"],
        "assertions": {"type": "array", "minItems": 1, "items": text},
        "assertion_types": {"type": "array", "items": {"enum": ["schema", "fixture-content", "assisted", "manual-render"]}},
        "limitations": {"type": "array", "items": text}}
    shape = {"type": "object", "properties": {"fixture_version": {"const": "0.1.0"},
        "cases": {"type": "array", "maxItems": 1024, "items": {"type": "object", "properties": properties,
        "required": list(properties), "additionalProperties": False}}},
        "required": ["fixture_version", "cases"], "additionalProperties": False}
    if schema_errors(Draft202012Validator(shape), dataset, "case schema"):
        return ["catalog: case schema violation"]
    errors = []; cases = {}; triads = {identity: set() for identity in PRIORITY_IDS}
    index = {rule["id"]: rule for rule in rules}; profile_index = {p["id"]: p for p in profiles}
    for case in dataset["cases"]:
        if len(case["assertion_types"]) != len(case["assertions"]):
            errors.append("catalog: assertion label count mismatch")
        if case["id"] in cases:
            errors.append("catalog: duplicate case ID")
        cases[case["id"]] = case
        rule = index.get(case["rule_id"])
        if rule is None or case["id"] not in rule["case_ids"]:
            errors.append("catalog: case rule binding mismatch")
            continue
        if case["method"] != rule["verification"]["method"]:
            errors.append("catalog: case method mismatch")
        if (case["profile"] not in rule["media"] or case["profile"] not in profile_index or
                case["rule_id"] not in profile_index[case["profile"]]["rule_ids"]):
            errors.append("catalog: case profile mismatch")
        if case["rule_id"] in triads:
            triads[case["rule_id"]].add(case["kind"])
    for rule in rules:
        for identity in rule["case_ids"]:
            if identity not in cases:
                errors.append("catalog: unresolved case reference")
            elif cases[identity]["rule_id"] != rule["id"]:
                errors.append("catalog: case rule binding mismatch")
    if any(kinds != {"positive", "negative", "exception"} for kinds in triads.values()):
        errors.append("catalog: incomplete priority triad")
    return sorted(set(errors))


def load_catalog(root: Path) -> list[dict]:
    """Admit coordinated local catalog/source/profile/fixture declarations.

    This does not execute fixture assertions, authenticate approvals or assess
    Japanese visual quality. Implemented coverage requires the independently
    trusted host's current, digest-bound procedure and test-result evidence.
    """
    try:
        rules, profiles = rule_profile_data(root)
        checks = validators(root)
        registry = Path(root) / "sources" / "public-sources.json"
        if not registry.exists():
            raise ValueError("catalog: missing source registry")
        errors = source_errors(read_json(registry), rules, checks)
        cases = Path(root) / "tests" / "fixtures" / "priority-cases.json"
        if not cases.exists():
            raise ValueError("catalog: missing priority cases")
        errors.extend(case_errors(read_json(cases), rules, profiles, checks))
        if errors:
            raise InputContentError("; ".join(sorted(set(errors))))
        return rules
    except OSError:
        raise ValueError("catalog: missing or unreadable local input") from None


def main():
    import sys
    parser = ResultParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    args = parser.parse_args()
    try:
        catalog = load_catalog(args.root)
        emit("passed", [], rule_count=len(catalog))
        return 0
    except ValueError as error:
        # Every diagnostic above is producer-authored, never raw source values.
        emit("incomplete", [str(error)])
        print("Catalog admission rejected; see sanitized diagnostics.", file=sys.stderr)
        return 2
    except MemoryError:
        emit("incomplete", ["catalog: resource budget unavailable"])
        return 2


if __name__ == "__main__":
    __import__("sys").exit(main())
