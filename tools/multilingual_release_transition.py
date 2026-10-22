"""Strict hash-based admission of 17 already published language-edition release transitions."""
import hashlib,json
from pathlib import Path
RECORD="tests/contracts/multilingual-v010-release-transition.json"
def admitted(root,path,before,raw,family):
    root=Path(root)
    if not (path=="README.md" or path=="index.html" or path.startswith("top-") or
            path.startswith("kumihan-zh-cn") or path.startswith("docs/install-zilu-")):return False
    data=json.loads((root/RECORD).read_text())
    row=data["paths"].get(path,{})
    if row.get("before")!=before or row.get("family")!=family:return False
    return hashlib.sha256(raw).hexdigest()==row.get("after")
