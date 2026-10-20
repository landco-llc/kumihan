"""Read exact document bytes only to reproduce already committed legacy archives.

New versions have no registry entry and receive no development documents.
Use public_boundary.py for clean prospective archives. Never rewrite a release.
"""
import hashlib
import io
import json
import zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REGISTRY=json.loads((Path(__file__).with_name('legacy-release-archives.json')).read_text())

class ArchivedDocument:
    def __init__(self, raw): self.raw=raw
    def read_bytes(self): return self.raw

def entries(root, archive_name):
    found=[]
    for path,row in REGISTRY.items():
        if Path(path).name!=archive_name: continue
        raw=(Path(root)/path).read_bytes()
        if hashlib.sha256(raw).hexdigest()!=row['sha256']:
            raise ValueError('Legacy archive bytes changed: '+path)
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            for member,expected in row['documents'].items():
                data=z.read(member)
                if hashlib.sha256(data).hexdigest()!=expected:raise ValueError('Legacy document changed')
                found.append((ArchivedDocument(data),member))
    return found

def documents(root, archive_name):
    return {name:source.read_bytes() for source,name in entries(root,archive_name)}
