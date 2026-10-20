"""Bounded JA source transition, independent of immutable SEO snapshots.

Exact before/after hashes are reviewable in the workgroup record. No wildcard
language paths or automatic baseline refresh is accepted.
"""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RECORD='docs/development/ja-v020-20261020/source-transition.json'
HOSTS=('downloads Claude','downloads GPT-Codex','downloads Gemini')
MANIFESTS={'.claude-plugin/plugin.json','.codex-plugin/plugin.json','plugin.json','gemini-extension.json'}
def allowed(path):
 if path in MANIFESTS:return True
 if path in {f'skills/{skill}/{file}' for skill in ('kumihan','kumihan-web','kumihan-documents','kumihan-review') for file in ('SKILL.md','inventory.json','references/web-recipes.md','references/document-recipes.md','references/review-protocol.md')}: return True
 for host in HOSTS:
  if path in {host+'/'+name for name in ('MANIFEST.json','SHA256SUMS.txt','README.md')}:return True
  p=Path(path)
  if p.parent.as_posix() in {host+'/skills',host+'/plugins',host+'/extensions'} and p.name.startswith('kumihan-') and p.name.endswith(('-0.1.8.zip','-0.2.0.zip')):return True
 return False

def admitted(root,path,before):
 root=Path(root)
 if not allowed(path):return False
 record_path=root/RECORD
 if not record_path.is_file():return False
 record=json.loads(record_path.read_text())
 if record.get('authority')!='KUMI-JA-V020-RESEARCH-WG-20261020-01':return False
 row=record.get('paths',{}).get(path,{})
 if row.get('before')!=before:return False
 target=root/path
 if not target.is_file() and not path.endswith('-0.1.8.zip'): return False
 actual=hashlib.sha256(target.read_bytes()).hexdigest() if target.is_file() else None
 return row.get('after')==actual and 'after' in row
