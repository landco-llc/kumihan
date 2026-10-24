#!/usr/bin/env python3
"""Bounded offline Spanish review. Reads UTF-8 bytes; never edits inputs."""
import argparse
import hashlib
import json
from pathlib import Path
import re

LOCALES=('es','es-ES','es-MX','es-AR','es-CO','es-CL','es-PE','es-419','es-US')
PATTERNS=(
 ('ES-T06',r'[?!]\.', 'Revisar el punto tras el cierre; distinguir citas y usos especiales.'),
 ('ES-T07',r'«[ \u00a0\u202f]|[ \u00a0\u202f]»', 'Revisar espacios interiores; conservar citas y excepciones aprobadas.'),
 ('ES-T17',r'\d%', 'Confirmar si es texto editorial o salida de Intl antes de proponer espacio.'),
 ('ES-X03',r'word-break\s*:\s*break-all', 'Revisar el alcance CSS y observar los saltos reales antes de cambiarlo.'),
 ('ES-L09',r'hreflang\s*=\s*[\"\x27]es-419[\"\x27]', 'Usar alternantes reales aceptados por el buscador; lang y hreflang son distintos.'),
)

def review(data,locale='es',candidate=None):
    if locale not in LOCALES:
        raise ValueError('Unsupported locale; choose explicitly: '+', '.join(LOCALES))
    text=data.decode('utf-8')
    original_hash=hashlib.sha256(data).hexdigest()
    compared=data if candidate is None else candidate
    compared.decode('utf-8')
    findings=[]
    for rule,pattern,proposal in PATTERNS:
        for match in re.finditer(pattern,text):
            findings.append(dict(rule_id=rule,status='needs-review',test_method='bounded-static-candidate',
                evidence=dict(character_offset=match.start(),match=match.group()),original_hash=original_hash,
                proposal=proposal,edits_authorized=False))
    return dict(original_hash=original_hash,original_bytes=len(data),locale=locale,
        context=dict(currency=None,timeZone=None,market=None,pronoun='inherit',verb_paradigm='inherit',plural='inherit',date_value_kind='inherit'),
        preservation=dict(status='passed' if data==compared else 'failed',candidate_hash=hashlib.sha256(compared).hexdigest(),
                          candidate_bytes=len(compared),test_method='exact-byte-comparison'),
        findings=findings,rendering='not-checked',editorial_review='needs-review',native_host='not-checked')

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('original',type=Path);p.add_argument('--candidate',type=Path);p.add_argument('--locale',default='es')
    args=p.parse_args()
    try:r=review(args.original.read_bytes(),args.locale,args.candidate.read_bytes() if args.candidate else None)
    except (ValueError,OSError) as error:p.error(str(error))
    print(json.dumps(r,ensure_ascii=False,indent=2))
    return int(r['preservation']['status']=='failed')
if __name__=='__main__':raise SystemExit(main())
