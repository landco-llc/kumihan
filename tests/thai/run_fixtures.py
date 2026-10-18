"""Run bounded actual checks, recording unexercised proposal scenarios individually."""
import importlib.util
import json
from pathlib import Path
import unicodedata
ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('source_check', ROOT/'plugins/kumihan-th/runtime/check_source.py')
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)

def run():
    results=[]
    for case in json.loads((Path(__file__).parent/'fixtures.json').read_text()):
        cid=case['id']; text=case['input'].get('text')
        result={'id':cid,'rule_ids':case['rule_ids'],'status':'not-checked','evidence':'Proposed scenario requires host, rendering, segmentation or semantic evidence not run by this source-integrity suite.'}
        if cid in ('TH-F001','TH-F002','TH-F003'):
            mutation={'TH-F001':'กเ','TH-F002':unicodedata.normalize('NFKC',text),'TH-F003':'กํ่'}[cid]
            positive=helper.compare(text,text); negative=helper.compare(text,mutation)
            assert positive['status']=='passed' and negative['status']=='failed'
            result.update(status='passed',evidence='Exact source identity passed and deliberate source mutation was detected. Scope: byte preservation only; proposed linguistic/rendering scenario not-checked.',negative_observation=negative['status'])
        elif cid=='TH-F006':
            observed=helper.inspect('😀ไทย'); assert observed['utf16_units']==5 and observed['code_points']==4
            result.update(status='passed',evidence='Bounded emoji+Thai offset probe: 😀ไทย = 5 UTF-16 units, 4 code points. Grapheme mapping and full proposed scenario not-checked.')
        elif cid=='TH-F027':
            text='\u200b\u2060\u00a0\ufeff'; observed=helper.compare(text,text)
            assert observed['status']=='passed' and len(observed['original']['controls'])==4
            result.update(status='passed',evidence='Four explicit controls preserved and positions reported: U+200B U+2060 U+00A0 U+FEFF. Intent and visual effects not-checked.')
        results.append(result)
    return {'scope':'40 individually classified proposal cases; five bounded static subchecks only. A passed subcheck is not full proposed scenario acceptance.','results':results,'counts':{s:sum(r['status']==s for r in results) for s in ('passed','failed','not-checked')}}
if __name__=='__main__':
    print(json.dumps(run(),ensure_ascii=False,indent=2))
