#!/usr/bin/env python3
"""Local Satzbild browser measurements; writes evidence only to --output."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
from playwright.sync_api import sync_playwright
from build_satzbild_site import outputs

def main():
 p=argparse.ArgumentParser();p.add_argument('--base',default='http://127.0.0.1:8765/kumihan/');p.add_argument('--output',type=Path,required=True);p.add_argument('--chromium',default='/usr/bin/chromium');a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
 observations=[]
 with sync_playwright() as playwright:
  browser=playwright.chromium.launch(executable_path=a.chromium or None,args=['--no-sandbox'])
  page=browser.new_page();page.route('https://**/*',lambda route:route.abort())
  for path in outputs():
   print('measuring '+path,flush=True)
   for width in (320,375,768,1280):
    for scale in (1,2):
     for spacing in (False,True):
      page.set_viewport_size({'width':width,'height':1000});response=page.goto(a.base+path,wait_until='domcontentloaded');page.evaluate('document.fonts.ready')
      if scale==2:page.evaluate("() => {const values=[...document.querySelectorAll('body,body *')].map(e=>[e,parseFloat(getComputedStyle(e).fontSize)]);values.forEach(([e,v])=>e.style.setProperty('font-size',v*2+'px','important'));}")
      page.add_style_tag(content='/* measurement */'+('*{line-height:1.5!important;letter-spacing:.12em!important;word-spacing:.16em!important}p{margin-bottom:2em!important}' if spacing else ''))
      observed=page.evaluate('''() => ({width:innerWidth,scroll:document.documentElement.scrollWidth,lang:document.documentElement.lang,images:[...document.images].every(i=>i.complete&&i.naturalWidth>0),clipped:[...document.querySelectorAll('main *,header *,footer *')].filter(e=>{const s=getComputedStyle(e);return ['hidden','clip'].includes(s.overflowY)&&e.scrollHeight>e.clientHeight+1}).map(e=>e.tagName),links:[...document.querySelectorAll('a[href]')].every(e=>e.textContent.trim().length>0 || e.getAttribute('aria-label')),focus:!!document.querySelector('a.skip, a.skip-link')})''')
      passed=response.status==200 and observed['scroll']<=width+1 and observed['images'] and not observed['clipped'] and observed['links'] and observed['focus']
      observations.append(dict(path=path,width=width,text_scale=scale,spacing=spacing,status='passed' if passed else 'failed',observed=observed))
      if width==1280 and scale==1 and not spacing and path.startswith('kumihan-de'):page.screenshot(path=str(a.output/(path+'.png')),full_page=True)
      if width==320 and scale==2 and spacing and path=='kumihan-de.html':page.screenshot(path=str(a.output/'de-mobile-200-spacing.png'),full_page=True)

  version=browser.version;browser.close()
 result=dict(browser=version,method='Chromium local HTTP; all computed element font sizes doubled (CSS simulation, not native text zoom); external font requests blocked to exercise fallback; 12 pages × 4 widths × 2 text scales × 2 spacing states. Overflow and DOM clipping measurements; not universal accessibility certification.',observations=observations,failures=sum(o['status']=='failed' for o in observations),rules=['DE-WEB-001','DE-WEB-004','DE-WEB-007'],not_checked=['Safari','Windows fonts','screen reader','font file cmap','native host invocation','Office/PDF'])
 (a.output/'browser.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(f"{len(observations)} observations; {result['failures']} failures")
 return int(bool(result['failures']))
if __name__=='__main__':sys.exit(main())
