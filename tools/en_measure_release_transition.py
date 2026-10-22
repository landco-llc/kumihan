"""Bounded, exact-byte English Measure v0.1.0 public site admission.

Do not relax the immutable release-preservation baseline. New reviewed release
facts are admitted ONLY for the recorded README and 23 legacy gateway bodies.
"""
import hashlib
import json
from pathlib import Path

RECORD = "tests/contracts/en-measure-v010-transition.json"
TAG = "kumihan-measure-v0.1.0"

def admitted(root, path, before, raw):
    root = Path(root)
    if path != "README.md" and not (path == "index.html" or
            (path.startswith("top-") and path.endswith(".html"))):
        return False
    record = root / RECORD
    if not record.exists(): return False
    data = json.loads(record.read_text(encoding="utf-8"))
    if data.get("tag") != TAG: return False
    entry = data.get("paths", {}).get(path, {})
    if entry.get("before") != before: return False
    if path == "README.md":
        if entry.get("family") != "protected" or b"kumihan-measure-v0.1.0" not in raw: return False
    else:
        if entry.get("family") != "bodies" or b'aria-labelledby="language-en"' not in raw: return False
        if b"<bdi dir=\"ltr\">v0.1.0</bdi>" not in raw: return False
    return hashlib.sha256(raw).hexdigest() == entry.get("after")
