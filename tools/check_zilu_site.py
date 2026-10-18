#!/usr/bin/env python3
"""Local Chromium evidence for 12 static ZiLu pages. Does not certify WCAG/GB."""
import argparse
import json
from pathlib import Path
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--base',default='http://127.0.0.1:8765/kumihan/');p.add_argument('--output',default='/tmp/zilu-browser');p.add_argument('--chromium',default='/usr/bin/chromium');a=p.parse_args()
    out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
    paths=[f'kumihan-zh-cn{s}.html' for s in ('','.en','.ja')]+[f'docs/install-zilu-{h}{s}.html' for h in ('chatgpt','claude','gemini') for s in ('','.en','.ja')]
    results=[];failures=[];checked=set()
    with sync_playwright() as pw:
        browser=pw.chromium.launch(executable_path=a.chromium or None,args=['--no-sandbox'])
        page=browser.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        for path in paths:
            for width in (320,375,768,1440):
                page.set_viewport_size({'width':width,'height':1000});response=page.goto(a.base+path,wait_until='load')
                assert response.status==200,(path,response.status)
                assert page.locator('h1').count()==1
                for condition in ('normal','text-200','spacing'):
                    if condition=='text-200':
                        page.evaluate("""() => {for (const el of document.querySelectorAll('body *')) el.dataset.originalSize=getComputedStyle(el).fontSize;for(const el of document.querySelectorAll('body *')) el.style.fontSize=(parseFloat(el.dataset.originalSize)*2)+'px';}""")
                    if condition=='spacing':
                        page.reload(wait_until='load');page.add_style_tag(content='* {line-height:1.5 !important;letter-spacing:.12em !important;word-spacing:.16em !important} p {margin-bottom:2em !important}')
                    metrics=page.evaluate("""() => ({width:innerWidth, scroll:document.documentElement.scrollWidth, clipped:[...document.querySelectorAll('main *,header *,footer *')].filter(e=>{let r=e.getBoundingClientRect();return r.width>0&&(r.left < -1 || r.right > innerWidth+1)}).map(e=>e.tagName+':'+e.textContent.slice(0,60))})""")
                    ok=metrics['scroll']<=width+1 and not metrics['clipped']
                    row=dict(path=path,width=width,condition=condition,passed=ok,metrics=metrics);results.append(row)
                    if not ok:failures.append(row)
                    if condition=='normal' and width in (375,1440) and path.startswith('kumihan-zh-cn'):
                        page.screenshot(path=str(out/(path+f'-{width}.png')),full_page=True)
                    page.reload(wait_until='load')
                # Keyboard skip link must focus and move to the main region.
                page.keyboard.press('Tab');assert page.locator('.skip').evaluate('(e)=>e===document.activeElement'),path
                page.keyboard.press('Enter');assert page.evaluate('document.activeElement.id')=='main',path
            for href in page.locator('a[href]').evaluate_all('(els)=>els.map(e=>e.href)'):
                if urlparse(href).netloc==urlparse(a.base).netloc:
                    url=href.split('#')[0]
                    if url not in checked:
                        r=page.request.get(url);assert r.status==200,(path,url,r.status);checked.add(url)
        assert not errors,errors
        version=browser.version;browser.close()
    report=dict(renderer='Chromium '+version,scope='Local source static HTML; 200% computed text resize is not native browser zoom; overflow geometry and keyboard skip only, no full accessibility or glyph certification.',results=results,local_links_checked=len(checked),failures=failures)
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(f'Chromium {version}: {len(results)} layout checks, {len(checked)} links, {len(failures)} failures')
    return int(bool(failures))
if __name__=='__main__':raise SystemExit(main())
