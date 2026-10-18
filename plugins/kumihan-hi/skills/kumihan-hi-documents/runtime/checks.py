#!/usr/bin/env python3
"""Offline read-only source integrity. No grammar, segmentation or rendering claim."""
import argparse, hashlib, json, unicodedata
from pathlib import Path
def compare(source, candidate):
 source_text=source.decode('utf-8');candidate_text=candidate.decode('utf-8')
 equal=source==candidate
 return dict(rule_id='HI-C01',status='passed' if equal else 'failed',bytes_equal=equal,source_sha256=hashlib.sha256(source).hexdigest(),candidate_sha256=hashlib.sha256(candidate).hexdigest(),derived_nfc_equal=unicodedata.normalize('NFC',source_text)==unicodedata.normalize('NFC',candidate_text),unicode_database=unicodedata.unidata_version,evidence_kind='static byte comparison',rendering='NOT_CHECKED',grammar='NOT_CHECKED',remediation='Preserve original bytes; review explicitly authorized edits separately.')
def inspect(source):
 text=source.decode('utf-8')
 return dict(source_sha256=hashlib.sha256(source).hexdigest(),bytes=len(source),join_controls=[dict(offset=i,codepoint=f'U+{ord(c):04X}') for i,c in enumerate(text) if c in '\u200c\u200d'],normalization='derived only; no source changes',rendering='NOT_CHECKED',segmentation='NOT_CHECKED',grammar='NOT_CHECKED')
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('source',type=Path);p.add_argument('--candidate',type=Path);a=p.parse_args()
 raw=a.source.read_bytes();r=compare(raw,a.candidate.read_bytes()) if a.candidate else inspect(raw)
 print(json.dumps(r,ensure_ascii=False,indent=2));return int(r.get('status')=='failed')
if __name__=='__main__':raise SystemExit(main())
