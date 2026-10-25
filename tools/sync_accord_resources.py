#!/usr/bin/env python3
"""Synchronize Accord's canonical consumer resources into its four standalone skills."""
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "plugins/kumihan-accord"
TREES = ("runtime", "rules", "schemas", "locales", "references")
FILES = ("sources.json", "LICENSE", "THIRD_PARTY_NOTICES.md")
SKILLS = ("kumihan-accord", "kumihan-accord-web", "kumihan-accord-documents", "kumihan-accord-review")


def sync(check=False):
    expected = {}
    for tree in TREES:
        for path in (ROOT / tree).rglob("*"):
            if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc":
                if path.is_symlink():
                    raise ValueError("Symlink consumer resource")
                expected[path.relative_to(ROOT)] = path.read_bytes()
    for name in FILES:
        expected[Path(name)] = (ROOT / name).read_bytes()
    for skill in SKILLS:
        target = ROOT / "skills" / skill
        for rel, raw in expected.items():
            path = target / rel
            if check:
                if not path.exists() or path.read_bytes() != raw:
                    raise ValueError("Stale resource: " + str(path))
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(raw)
        for tree in TREES:
            for path in (target / tree).rglob("*"):
                if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc" and path.relative_to(target) not in expected:
                    raise ValueError("Noncanonical resource: " + str(path))
    print(f"PASS: {len(expected)} canonical resources synchronized across four skills")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    sync(parser.parse_args().check)
