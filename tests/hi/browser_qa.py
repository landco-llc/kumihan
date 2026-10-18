"""Bounded real Chromium observations; native/editorial checks stay separate."""
import hashlib,json,platform
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/hi/browser-results.json'
PAGES=[f'kumihan-hi{s}.html' for s in ('','.en','.ja')]+[f'docs/install-kumihan-hi-{h}{s}.html' for h in ('chatgpt','claude','gemini') for s in ('','.en','.ja')]
def main():
 rows=[];hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in PAGES}
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  for path in PAGES:
   for width in [320,768,1280]:
    for mode in ['normal','text200','spacing','fallback']:
     page=browser.new_page(viewport={'width':width,'height':960})
     if mode=='fallback':page.route('**/*.ttf',lambda route:route.abort())
     page.goto('http://127.0.0.1:8765/'+path,wait_until='networkidle')
     page.evaluate('document.fonts.ready')
     if mode=='text200':
      page.evaluate('''() => { const els=[...document.querySelectorAll('body,body *')]; const sizes=els.map(e=>getComputedStyle(e).fontSize); els.forEach((e,i)=>e.style.setProperty('font-size',(parseFloat(sizes[i])*2)+'px','important')); }''')
     if mode=='spacing':page.add_style_tag(content='* {line-height:1.5 !important;letter-spacing:.12em !important;word-spacing:.16em !important} p {margin-bottom:2em !important}')
     result=page.evaluate('''() => ({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,overflow:[...document.querySelectorAll('main *,header *,footer *')].filter(e=> {const r=e.getBoundingClientRect();return r.width>0&&(r.right>innerWidth+1||r.left < -1)}).slice(0,10).map(e=>({tag:e.tagName,cls:e.className,text:e.textContent.slice(0,70),right:e.getBoundingClientRect().right})),font:document.fonts.check('16px "Kumihan Devanagari"'),h1:getComputedStyle(document.querySelector('h1')).fontFamily,lang:document.documentElement.lang})''')
     result.update(page=path,viewport=width,mode=mode,status='passed' if result['scrollWidth']<=width+1 and not result['overflow'] else 'failed')
     rows.append(result)
     if path=='kumihan-hi.html' and mode=='normal':page.screenshot(path=f'/tmp/hi-{width}.png',full_page=True)
     page.close()
  version=browser.version;browser.close()
 assert hashes=={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in PAGES}
 report=dict(browser=version,method='Chromium headless; text200 doubles computed font sizes, not browser UI zoom; fallback aborts webfont requests; spacing overrides all four simultaneously',source_hashes_before_after=hashes,observations=rows,not_checked=['Native host installation','Native speaker proofreading','Office','Android/iOS','IME/backspace/delete','Screen reader','Safari/Firefox','Browser UI zoom'],visual_shaping='Screenshots reviewed separately; geometry is not proof of shaping or grammar')
 OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 failures=[r for r in rows if r['status']=='failed'];print(f'{len(rows)} browser observations; {len(failures)} overflow failures')
 for r in failures[:15]:print(r['page'],r['viewport'],r['mode'],r['scrollWidth'],r['overflow'])
 return bool(failures)
if __name__=='__main__':raise SystemExit(main())
