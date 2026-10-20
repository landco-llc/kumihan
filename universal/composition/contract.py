"""Offline development validation. No PHP JSON Schema conformance claim."""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
from jsonschema import Draft202012Validator

VERSION = '0.1.0-design.1'
SCHEMA_DIGEST = '14d9226833c8ff1af8a92f8da56de4c852f003e87803f78c3ec8bf45c8c75cda'
SCHEMA_PATH = Path(__file__).parent / 'schemas/composition-0.1.0-design.1.schema.json'
raw = SCHEMA_PATH.read_bytes()
if hashlib.sha256(raw).hexdigest() != SCHEMA_DIGEST:
    raise RuntimeError('Approved schema integrity failure')
SCHEMA = json.loads(raw)
Draft202012Validator.check_schema(SCHEMA)
VALIDATOR = Draft202012Validator(SCHEMA)

class CompositionError(ValueError):
    """Named, source-free error with a JSON pointer-like location."""
    def __init__(self, code, scope, message):
        self.code, self.scope, self.message = code, scope, message
        super().__init__(f'{code} at {scope}: {message}')

    def record(self, request_id='unbound'):
        return dict(contract_version=VERSION, kind='error', id='error-'+self.code,
                    request_id=request_id, code=self.code, scope=self.scope,
                    message=self.message, recoverable=True,
                    resume_hint='Reload exact source and correct the named field; no partial success.')

def unicode_check(value, scope='/'):
    if isinstance(value, str):
        try: value.encode('utf-8', errors='strict')
        except UnicodeError: raise CompositionError('E_INVALID_UNICODE', scope, 'Unpaired surrogate') from None
    elif isinstance(value, dict):
        for key, item in value.items():
            unicode_check(key, scope)
            unicode_check(item, scope.rstrip('/')+'/'+str(key))
    elif isinstance(value, list):
        for i, item in enumerate(value): unicode_check(item, scope.rstrip('/')+'/'+str(i))

def validate_record(value):
    unicode_check(value)
    if not isinstance(value, dict):
        raise CompositionError('E_REFERENCE', '/', 'Expected record object')
    if value.get('contract_version') != VERSION:
        raise CompositionError('E_CONTRACT_VERSION', '/contract_version', 'Unsupported design version')
    # Selecting a definition improves diagnostic paths; the root union is checked too.
    kind = value.get('kind')
    if kind not in ('request','plan','module','observation','audit','error'):
        raise CompositionError('E_REFERENCE', '/kind', 'Unknown record kind')
    validator = Draft202012Validator(dict(SCHEMA, oneOf=[{'$ref': '#/$defs/'+kind}]))
    issue = next(validator.iter_errors(value), None)
    if issue:
        # Do not echo source values or the validator's verbose message.
        raise CompositionError('E_REFERENCE', '/'+'/'.join(map(str, issue.absolute_path)), 'Schema structure rejected')
    return copy.deepcopy(value)

def legacy_snapshot(report):
    """Local adapter envelope, NOT a composition record and NOT a legacy report extension."""
    if report.get('checked'):
        raise CompositionError('E_REFERENCE','/checked','Legacy claimed checks require external evidence validation')
    return {'adapter_version':'legacy-readonly-1', 'legacy':copy.deepcopy(report),
            'mapping':{'status':report.get('status'), 'not_checked':copy.deepcopy(report.get('not_checked',[]))},
            'limitations':['Legacy guidance does not prove composition checks; no new legacy fields emitted.']}

def restore_legacy(snapshot):
    if snapshot.get('adapter_version') != 'legacy-readonly-1':
        raise CompositionError('E_CONTRACT_VERSION','/adapter_version','Unsupported adapter')
    return copy.deepcopy(snapshot['legacy'])
