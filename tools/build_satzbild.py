#!/usr/bin/env python3
"""Deterministic offline Satzbild v0.1.0 distributions. --check never writes."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import zipfile

ROOT=Path(__file__).resolve().parents[1]
PRODUCT='plugins/kumihan-satzbild'
NAMES=tuple('kumihan-satzbild'+s for s in ('','-web','-documents','-review'))
LOGO='assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png'
LOGO_SHA='1d1ae2cb4f7f69f7b5f54b050ff8c6fb2c315b75ded8003f8b605855d633f96e'
HOSTS={'GPT-Codex':('GPT-Codex-plugin','GPT-Codex-skill'), 'Claude':('Claude-Code-plugin','Claude-skill'), 'Gemini':('Gemini-CLI-extension','Gemini-Apps-skill')}

def encode(value):return (json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode()
def digest(data):return hashlib.sha256(data).hexdigest()
def archive(files):
 stream=io.BytesIO()
 with zipfile.ZipFile(stream,'w') as z:
  for path,data in sorted(files.items()):
   if Path(path).is_absolute() or '..' in Path(path).parts or '\\' in path:raise ValueError('Unsafe archive member: '+path)
   info=zipfile.ZipInfo(path,(2026,10,19,0,0,0));info.create_system=3;info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
   z.writestr(info,data,compresslevel=9)
 return stream.getvalue()
def inventory(files,**identity):return encode(dict(**identity,files=[dict(path=p,bytes=len(b),sha256=digest(b)) for p,b in sorted(files.items())],self_digest='Inventory excludes itself; archive digest covers all bytes.'))
def bilingual(value):
 if ' | ' not in value or not all(x.strip() for x in value.split(' | ')):raise ValueError('German | English description required')

def plan_outputs(root=ROOT):
 root=Path(root);base=root/PRODUCT
 # Reject symlinks before selecting inputs or following any source directory.
 if base.is_symlink():raise ValueError('Symlink product root')
 for p in base.rglob('*'):
  if p.is_symlink():raise ValueError('Symlink source: '+str(p))
 manifest=json.loads((base/'plugin.json').read_bytes())
 if (manifest['name'],manifest['version'])!=('kumihan-satzbild','0.1.0'):raise ValueError('Identity mismatch')
 interface=manifest['extensions']['com.openai']['interface']
 if interface['displayName']!='KUMIHAN｜Satzbild':raise ValueError('Display identity mismatch')
 for field in ('shortDescription','longDescription'):bilingual(interface[field])
 bilingual(manifest['description'])
 for p in ('.claude-plugin/plugin.json','gemini-extension.json'):
  host=json.loads((base/p).read_bytes());bilingual(host['description'])
  if (host['name'],host['version'],host['displayName'])!=('kumihan-satzbild','0.1.0','KUMIHAN｜Satzbild'):raise ValueError('Host identity mismatch')
 rules=json.loads((base/'rules/catalog.json').read_bytes());sources=json.loads((base/'sources/public-sources.json').read_bytes())
 if len(rules)!=44 or len({r['id'] for r in rules})!=44:raise ValueError('44 unique rules required')
 if not {s for r in rules for s in r['source_refs']} <= {s['id'] for s in sources['sources']}:raise ValueError('Missing source')
 logo=(root/LOGO).read_bytes()
 if digest(logo)!=LOGO_SHA:raise ValueError('Logo mismatch')
 shared={LOGO:logo,'LICENSE':(root/'LICENSE').read_bytes(),'THIRD_PARTY_NOTICES.md':(base/'THIRD_PARTY_NOTICES.md').read_bytes()}
 for folder in ('rules','sources','references','profiles','schemas','locales','runtime','fixtures'):
  for p in sorted((base/folder).rglob('*')):
   if p.is_file() and '__pycache__' not in p.parts:shared[p.relative_to(base).as_posix()]=p.read_bytes()
 outputs={PRODUCT+'/LICENSE':shared['LICENSE'],PRODUCT+'/'+LOGO:logo}
 overlay={k:v for k,v in manifest.items() if k not in ('$schema','extensions')};overlay.update(manifest['extensions']['com.openai']);overlay['skills']='./skills/'
 outputs[PRODUCT+'/.codex-plugin/plugin.json']=encode(overlay)
 skills={}
 for name in NAMES:
  files=dict(shared);files['SKILL.md']=(base/'entrypoints'/f'{name}.md').read_bytes()
  match=re.search(r'^description: "(.+)"$',files['SKILL.md'].decode(),re.M)
  if not match:raise ValueError('Missing skill description')
  bilingual(match.group(1));files['agents/openai.yaml']=(f'interface:\n  display_name: "KUMIHAN｜Satzbild"\n  short_description: "Deutsche Typografie | German typography"\n  icon_small: "./{LOGO}"\n  icon_large: "./{LOGO}"\n').encode();files['inventory.json']=inventory(files,skill=name,version='0.1.0')
  skills[name]=files
  outputs.update({f'{PRODUCT}/skills/{name}/{p}':b for p,b in files.items()})
 common={p:(base/p).read_bytes() for p in ('README.md','INSTALL.md','UPDATES.md','THIRD_PARTY_NOTICES.md','RELEASE_NOTES.md')}
 common.update({'LICENSE':shared['LICENSE'],LOGO:logo})
 archives={};host_by_file={}
 for host,(plugin_suffix,skill_suffix) in HOSTS.items():
  package=dict(common)
  for name,files in skills.items():
   package.update({f'skills/{name}/{p}':b for p,b in files.items()})
   filename=f'{name}-{skill_suffix}-v0.1.0.zip'
   archives[filename]=archive({f'{name}/{p}':b for p,b in files.items()});host_by_file[filename]=host
  if host=='GPT-Codex':package.update({'plugin.json':(base/'plugin.json').read_bytes(),'.codex-plugin/plugin.json':encode(overlay)})
  elif host=='Claude':package['.claude-plugin/plugin.json']=(base/'.claude-plugin/plugin.json').read_bytes()
  else:package.update({p:(base/p).read_bytes() for p in ('gemini-extension.json','GEMINI.md')})
  package['inventory.json']=inventory(package,product='KUMIHAN｜Satzbild',host=host,version='0.1.0')
  prefix='' if host=='Gemini' else 'kumihan-satzbild/'
  filename=f'kumihan-satzbild-{plugin_suffix}-v0.1.0.zip';archives[filename]=archive({prefix+p:b for p,b in package.items()});host_by_file[filename]=host
 archives['MANIFEST.json']=encode(dict(product='KUMIHAN｜Satzbild',version='0.1.0',tag='kumihan-de-v0.1.0',logo_sha256=LOGO_SHA,native_host='not-checked',marketplace_listing='not-verified',archives=[dict(file=p,source_path=f'{PRODUCT}/downloads/{p}',host=host_by_file[p],version='0.1.0',bytes=len(b),sha256=digest(b)) for p,b in sorted(archives.items())]))
 archives['SHA256SUMS.txt']=''.join(f'{digest(b)}  {p}\n' for p,b in sorted(archives.items())).encode()
 outputs.update({f'{PRODUCT}/downloads/{p}':b for p,b in archives.items()})
 return outputs

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');args=p.parse_args()
 outputs=plan_outputs();changed=[p for p,b in outputs.items() if not (ROOT/p).is_file() or (ROOT/p).read_bytes()!=b]
 generated={p.relative_to(ROOT).as_posix() for folder in ('skills','downloads','assets','.codex-plugin') for p in (ROOT/PRODUCT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts}
 stale=generated-set(outputs)
 if args.check:
  for p in sorted(set(changed)|stale):print('out of date: '+p)
  if changed or stale:return 1
  print('OK: Satzbild outputs current; 15 ZIPs');return 0
 for p in changed:
  target=ROOT/p;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(outputs[p])
 for p in stale:(ROOT/p).unlink()
 print(f'Built {len(outputs)} outputs; 15 ZIPs');return 0
if __name__=='__main__':raise SystemExit(main())
