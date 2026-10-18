"""Bounded Chromium inspection. CSS text enlargement is not native browser text zoom."""
import json,threading,http.server,functools
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]; OUT=Path('/tmp/kumihan-th-browser-evidence'); OUT.mkdir(parents=True,exist_ok=True)
handler=functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT.parent))
class Quiet(handler.func):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT.parent)))
threading.Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}/{ROOT.name}/'
paths=['kumihan-th.html','kumihan-th-en.html','kumihan-th-ja.html']+[f'docs/install-kumihan-th-{host}{suffix}.html' for host in ['chatgpt','claude','gemini'] for suffix in ['','.en','.ja']]
results=[]; fonts=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 for path in paths:
  for width in [320,375,768,1280]:
   for scale in [1,2]:
    page=browser.new_page(locale='th-TH',viewport={'width':width,'height':960},device_scale_factor=1)
    errors=[]; page.on('pageerror',lambda e:errors.append(str(e)))
    response=page.goto(base+path); page.evaluate('document.fonts.ready')
    before=page.locator('body').inner_text()
    if scale==2:
     page.evaluate('''() => {const sizes=[...document.querySelectorAll('body,body *')].map(el=>{const s=getComputedStyle(el);return [el,parseFloat(s.fontSize),s.lineHeight]});for(const [el,size,line]of sizes){el.style.fontSize=(size*2)+'px';if(line!=='normal')el.style.lineHeight=(parseFloat(line)*2)+'px';}}''')
    measures=page.evaluate('''() => ({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,lang:document.documentElement.lang,browserLocale:navigator.language,title:document.title,headings:[...document.querySelectorAll('h1')].map(x=>x.textContent),clipped:[...document.querySelectorAll('h1,h2,h3,p,li,a,pre')].filter(x=>x.clientWidth>0&&(x.scrollWidth>x.clientWidth+2||x.scrollHeight>x.clientHeight+2)&&['hidden','clip'].includes(getComputedStyle(x).overflow)).map(x=>x.tagName+':'+x.textContent.slice(0,60))})''')
    checks={'http':response.status,'no_horizontal_overflow':measures['scrollWidth']<=width+1,'text_preserved':before==page.locator('body').inner_text(),'no_js_errors':not errors,'no_clipped_text':not measures['clipped']}
    results.append({'path':path,'width':width,'css_text_scale':scale,'checks':checks,'measurements':measures,'errors':errors})
    if path=='kumihan-th.html' or (path=='docs/install-kumihan-th-chatgpt.html' and width in [320,1280] and scale==1):
     page.screenshot(path=str(OUT/f"{Path(path).stem}-{width}-{scale}x.png"),full_page=True)
    if path=='kumihan-th.html' and width==1280 and scale==1:
     cdp=page.context.new_cdp_session(page); cdp.send('DOM.enable');cdp.send('CSS.enable');root=cdp.send('DOM.getDocument')['root']['nodeId']
     for selector in ['h1','p']:
      node=cdp.send('DOM.querySelector',{'nodeId':root,'selector':selector})['nodeId'];fonts.append({'selector':selector,'fonts':cdp.send('CSS.getPlatformFontsForNode',{'nodeId':node})['fonts']})
    page.close()
 browser.close()
server.shutdown()
report={'engine':'system Chromium via Playwright','scope':'96 page/viewport/text-scale combinations; CSS enlargement is not native text zoom or WCAG certification','results':results,'actual_fonts':fonts}
(OUT/'browser-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
fails=[x for x in results if x['checks']['http']!=200 or not all(v for k,v in x['checks'].items() if k!='http')]
print(json.dumps({'cases':len(results),'failures':len(fails),'failed_cases':[{'path':x['path'],'width':x['width'],'scale':x['css_text_scale'],'checks':x['checks'],'scrollWidth':x['measurements']['scrollWidth']}for x in fails],'fonts':fonts},ensure_ascii=False,indent=2))
if fails:
    raise SystemExit(1)
