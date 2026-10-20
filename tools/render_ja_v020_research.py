from pathlib import Path
import json,html,hashlib,unicodedata
from playwright.sync_api import sync_playwright
import fitz
r=Path(__file__).resolve().parents[1]; f=r/'tests/fixtures/ja_v020'; out=r/'docs/development/ja-v020-20261020/evidence';out.mkdir(exist_ok=True)
cases=json.loads((f/'cases.json').read_text())['cases']
C=cases[4]['fixture']['protectedSource'];E=cases[10]['fixture']['protectedSource'];R=cases[26]['fixture']['protectedSource']
page='''<!doctype html><html lang="ja"><meta charset="utf-8"><title>Synthetic JA v0.2.0 contrasts</title><style>
body{font-family:"Noto Sans CJK JP",sans-serif;font-size:18px;margin:16px;line-height:1.8}section{margin-bottom:20px;border:1px solid;padding:8px}button{font:inherit;width:240px;max-width:100%;white-space:normal}.badbutton{width:240px;white-space:nowrap;overflow:hidden}.hidden-info{height:26px;overflow:hidden}.paper{height:200px;overflow:hidden}.longrow{height:350px}.value{font-size:48px}.label{font-size:14px}.title{font-size:24px}@media print{section{break-inside:avoid}}
</style><h1>合成検証用／実績ではありません</h1>'''
for id_,body in [('PV-005','<button class="badbutton">'+html.escape(C)+'</button>'),('PV-006','<button>'+html.escape(C)+'</button>'),('PV-007','いつものAIツールからはじめよう'),('PV-011','<div class="hidden-info">'+html.escape(E)+'<br>日時・会場はこの領域の外</div>'),('PV-014','<div class="title">集計</div><span class="label">処理済み </span><span class="value">48件</span>'),('PV-016','<p lang="ja">申込条件を確認してください。</p><p lang="en">Please read the application requirements.</p>'),('PV-027','<div class="paper"><table><tr><td class="longrow">'+html.escape(R)+'<div style="margin-top:220px">末尾セルと注記</div></td></tr></table></div>'),('PV-028','<p>報告本文と集計表</p><table><tr><th>件数</th></tr><tr><td>120件</td></tr></table>'),('PV-029','<p>静的な本文のみを持つ記事領域です。</p>')]:
 page+=f'<section id="{id_}"><h2>{id_}</h2>{body}</section>'
page+='</html>';(f/'web-contrasts.html').write_text(page)
observations=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);pg=browser.new_page()
 pg.set_content(page);pg.evaluate('document.fonts.ready')
 for w in [1024,320]:
  pg.set_viewport_size({'width':w,'height':900});pg.screenshot(path=str(out/f'web-{w}.png'),full_page=True)
  for id_ in ['PV-005','PV-006','PV-011','PV-014','PV-027','PV-029']:
   obs=pg.locator('#'+id_).evaluate('''e=>({text:e.textContent,rect:{width:e.getBoundingClientRect().width,height:e.getBoundingClientRect().height},children:[...e.querySelectorAll('button,.hidden-info,.paper,.value,.label')].map(x=>({tag:x.tagName,scrollWidth:x.scrollWidth,clientWidth:x.clientWidth,scrollHeight:x.scrollHeight,clientHeight:x.clientHeight,font:getComputedStyle(x).fontFamily,size:getComputedStyle(x).fontSize})),controls:e.querySelectorAll('button,input,a,select').length})''')
   observations.append({'caseId':id_,'viewport':w,'observed':obs})
 pg.locator('#PV-006 button').click();observations.append({'caseId':'PV-006','method':'rendered','action':'actual button click completed; no application behavior claimed'})
 pg.add_style_tag(content='p{line-height:1.5!important;margin-bottom:2em!important;letter-spacing:.12em!important}p[lang=en]{word-spacing:.16em!important}')
 pg.screenshot(path=str(out/'spacing-320.png'),full_page=True)
 observations.append({'caseId':'PV-016','method':'rendered','overrides':'paragraph line-height1.5, margin2em, letter-spacing.12em, English word-spacing.16em','overflow':pg.locator('#PV-016').evaluate('e=>({scrollWidth:e.scrollWidth,clientWidth:e.clientWidth})')})
 pg.pdf(path=str(out/'preview.pdf'),format='A4',print_background=True)
 environment={'browser':browser.version,'executable':'/usr/bin/chromium','fontDeclaration':'Noto Sans CJK JP, sans-serif','nativeTextZoom':'not-checked','physicalProjection':'not-checked','nativeOffice':'not-checked'}
 browser.close()
doc=fitz.open(out/'preview.pdf')
for i,p in enumerate(doc):p.get_pixmap(matrix=fitz.Matrix(1,1)).save(str(out/f'pdf-page-{i+1}.png'))
(out/'rendered.json').write_text(json.dumps({'environment':environment,'observations':observations,'pdfPages':len(doc),'pdfRenderer':'PyMuPDF '+fitz.VersionBind,'limitations':'Browser HTML print fixture only; no native Office or physical performance evidence. Font family declaration is not proof of resolved glyphs.'},ensure_ascii=False,indent=2)+'\n')
print('rendered',len(observations),'observations;',len(doc),'PDF pages')
