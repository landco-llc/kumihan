#!/usr/bin/env python3
"""Local Equilibrio browser measurements; writes evidence only to --output."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
from playwright.sync_api import sync_playwright
from build_equilibrio_site import outputs
import build_install_guides


def pages():
 """The 3 landings (build_equilibrio_site.py) and the 9 installation guides (build_install_guides.py)."""
 return list(outputs())+[build_install_guides.guide_path('it',h,l) for h in build_install_guides.HOSTS for l in ('it','en','ja')]

def main():
 p=argparse.ArgumentParser();p.add_argument('--base',default='http://127.0.0.1:8765/kumihan/');p.add_argument('--output',type=Path,required=True);p.add_argument('--chromium',default='/usr/bin/chromium');a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
 observations=[]
 with sync_playwright() as playwright:
  browser=playwright.chromium.launch(executable_path=a.chromium or None,args=['--no-sandbox'])
  page=browser.new_page();page.route('https://**/*',lambda route:route.abort())
  for path in pages():
   print('measuring '+path,flush=True)
   for width in (320,375,768,1280):
    for scale in (1,2):
     for spacing in (False,True):
      page.set_viewport_size({'width':width,'height':1000});response=page.goto(a.base+path,wait_until='load');page.evaluate('document.fonts.ready')
      if scale==2:page.evaluate("() => {const values=[...document.querySelectorAll('body,body *')].map(e=>[e,parseFloat(getComputedStyle(e).fontSize)]);values.forEach(([e,v])=>e.style.setProperty('font-size',v*2+'px','important'));}")
      page.add_style_tag(content='/* measurement */'+('*{line-height:1.5!important;letter-spacing:.12em!important;word-spacing:.16em!important}p{margin-bottom:2em!important}' if spacing else ''))
      page.evaluate('() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))')
      observed=page.evaluate('''() => ({width:innerWidth,scroll:document.documentElement.scrollWidth,lang:document.documentElement.lang,images:[...document.images].every(i=>i.complete&&i.naturalWidth>0),clipped:[...document.querySelectorAll('main *,header *,footer *')].filter(e=>{const s=getComputedStyle(e);return ['hidden','clip'].includes(s.overflowY)&&e.scrollHeight>e.clientHeight+1}).map(e=>e.tagName),links:[...document.querySelectorAll('a[href]')].every(e=>e.textContent.trim().length>0 || e.getAttribute('aria-label')),focus:!!document.querySelector('a.skip, a.skip-link')})''')
      passed=response.status==200 and observed['scroll']<=width+1 and observed['images'] and not observed['clipped'] and observed['links'] and observed['focus']
      observations.append(dict(path=path,width=width,text_scale=scale,spacing=spacing,status='passed' if passed else 'failed',observed=observed))
      if width==1280 and scale==1 and not spacing and path.startswith('kumihan-it'):page.screenshot(path=str(a.output/(path+'.png')),full_page=True)
      if width==320 and scale==2 and spacing and path=='kumihan-it.html':page.screenshot(path=str(a.output/'it-mobile-200-spacing.png'),full_page=True)

  page.set_viewport_size({'width':375,'height':850})
  page.goto(a.base+'kumihan-it.html',wait_until='domcontentloaded');page.evaluate('document.fonts.ready')
  page.keyboard.press('Tab');focus=page.locator(':focus').evaluate('(e) => ({text:e.textContent,visible:e.getBoundingClientRect().width>0,outline:getComputedStyle(e).outlineStyle})')
  page.keyboard.press('Enter');keyboard_target=page.evaluate('location.hash')
  page.screenshot(path=str(a.output/'it-mobile-keyboard.png'))
  page.set_content('<html lang="it"><meta charset="utf-8"><style>body{font:24px/1.6 Arial,sans-serif;max-width:340px;margin:16px}p{margin:0 0 16px}</style><p>à è é ì ò ù À È É Ì Ò Ù</p><p><b>à è é ì ò ù À È É Ì Ò Ù</b></p><p><i>à è é ì ò ù À È É Ì Ò Ù</i></p><p>Caffè e tè perché ogni parola è diversa</p><p>L’acqua dell’architettura «Forma» “Spazio” ‘voce’</p><p>€ CHF 0123456789 1º 1° 20 °C</p></html>')
  page.screenshot(path=str(a.output/'it-accent-fallback.png'),full_page=True)
  version=browser.version;browser.close()
 result=dict(browser=version,keyboard=dict(first_focus=focus,skip_target=keyboard_target),method='Chromium local HTTP; all computed element font sizes doubled (CSS simulation, not native text zoom); external font requests blocked to exercise fallback; 12 pages × 4 widths × 2 text scales × 2 spacing states. Overflow and DOM clipping measurements; not universal accessibility certification.',observations=observations,failures=sum(o['status']=='failed' for o in observations),rules=['R21','R24','R37','R38','R39'],not_checked=['Safari','Windows fonts','screen reader','font file cmap','native host invocation','Office/PDF'])
 (a.output/'browser.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(f"{len(observations)} observations; {result['failures']} failures")
 return int(bool(result['failures']))
if __name__=='__main__':sys.exit(main())
