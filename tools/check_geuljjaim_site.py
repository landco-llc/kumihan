#!/usr/bin/env python3
"""Check built Korean pages in a real Chromium browser. Requires Playwright.
Run a Jekyll-built site at BASE_URL, including its /kumihan prefix.
Outputs machine-readable observations, not a native host/zoom certification.
"""
import argparse
import json
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen
from playwright.sync_api import sync_playwright

PAGES=[f'kumihan-ko{s}.html' for s in ('','.en','.ja')]+[
    f'docs/install-ko-{p}{s}.html' for p in ('chatgpt','claude','gemini') for s in ('','.en','.ja')]

def check(base, output, executable):
    output.mkdir(parents=True,exist_ok=True)
    observations=[]; failures=[]; links=set();errors=[]; wrap_comparisons=[]
    for attempt in range(30):
        try:
            with urlopen(base,timeout=2) as response:
                if response.status==200: break
        except OSError:
            if attempt==29: raise
            time.sleep(.1)
    with sync_playwright() as pw:
        browser=pw.chromium.launch(executable_path=executable or None,headless=True,args=['--no-sandbox'])
        context=browser.new_context(permissions=['clipboard-read','clipboard-write'],reduced_motion='reduce')
        page=context.new_page()
        page.on('pageerror',lambda err:errors.append(str(err)))
        page.on('console',lambda msg:errors.append(msg.text) if msg.type=='error' else None)
        for rel in PAGES:
            for width,zoom in [(320,1),(375,1),(768,1),(1440,1),(320,2)]:
                page.set_viewport_size(dict(width=width,height=1000))
                response=page.goto(urljoin(base,rel),wait_until='networkidle')
                if response.status!=200: failures.append(f'{rel}: HTTP {response.status}')
                page.evaluate('(zoom)=>document.documentElement.style.fontSize=`${zoom*100}%`',zoom)
                page.evaluate('()=>document.fonts.ready')
                result=page.evaluate('''()=>({
                    width:innerWidth, documentWidth:document.documentElement.scrollWidth,
                    lang:document.documentElement.lang, title:document.title,
                    h1:document.querySelectorAll('h1').length,
                    logo:document.querySelectorAll('img').length,
                    missingAlt:[...document.images].filter(x=>!x.hasAttribute('alt')).length,
                    brokenImages:[...document.images].filter(x=>!x.complete||!x.naturalWidth).length,
                    canonical:document.querySelector('link[rel=canonical]').href,
                    alternates:[...document.querySelectorAll('link[rel=alternate]')].map(x=>[x.hreflang,x.href]),
                    overflowElements:[...document.querySelectorAll('body *')].filter(x=>x.getBoundingClientRect().right>innerWidth+1).map(x=>({tag:x.tagName,class:x.className,right:x.getBoundingClientRect().right})),
                    clip:[...document.querySelectorAll('main *')].filter(x=>['hidden','clip'].includes(getComputedStyle(x).overflowY)&&x.scrollHeight>x.clientHeight+1).map(x=>x.tagName),
                    links:[...document.querySelectorAll('a[href],link[rel=stylesheet],script[src],img[src]')].map(x=>x.href||x.src)
                })''')
                observations.append(dict(page=rel,viewport=width,text_scale=zoom,method='Chromium; CSS root-font-size simulation' if zoom==2 else 'Chromium',**{k:v for k,v in result.items() if k!='links'}))
                if result['documentWidth']>width: failures.append(f'{rel} {width}/{zoom}: horizontal overflow {result["documentWidth"]}: {result["overflowElements"]}')
                if result['clip'] or result['missingAlt'] or result['brokenImages'] or result['h1']!=1: failures.append(f'{rel}: structure/images/clip {result}')
                expected='ko-KR' if not any(s in rel for s in ['.en.','.ja.']) else ('en' if '.en.' in rel else 'ja')
                if result['lang']!=expected: failures.append(f'{rel}: wrong lang')
                if result['canonical']!='https://landco-llc.github.io/kumihan/'+rel: failures.append(f'{rel}: canonical')
                if len(result['alternates'])!=4: failures.append(f'{rel}: hreflang')
                links.update(result['links'])
                if zoom==1 and width in (320,1440) and rel=='kumihan-ko.html': page.screenshot(path=str(output/f'ko-{width}.png'),full_page=True)
                if zoom==1 and width==375 and rel in ('kumihan-ko.en.html','kumihan-ko.ja.html'): page.screenshot(path=str(output/f'{expected}-375.png'),full_page=True)
            # Keyboard focus, locale preserving guide family, and clipboard content.
            page.evaluate('()=>document.documentElement.style.fontSize="100%"')
            page.goto(urljoin(base,rel),wait_until='networkidle')
            page.keyboard.press('Tab')
            if page.locator(':focus').count()!=1 or page.locator(':focus').get_attribute('href')!='#main': failures.append(f'{rel}: skip focus')
            # Landings (Jekyll) and guides (tools/build_install_guides.py) share the .language-switch nav.
            lang_links=page.locator('.language-switch a')
            if lang_links.count()!=3 or page.locator('.language-switch [aria-current=page]').count()!=1: failures.append(f'{rel}: locale navigation')
            if rel.startswith('docs/'):
                platform=rel.split('install-ko-')[1].split('.')[0]
                if not all(f'install-ko-{platform}' in x for x in lang_links.evaluate_all('(xs)=>xs.map(x=>x.href)')): failures.append(f'{rel}: platform lost')
                # assets/kumihan-install.js adds a Copy button to every command block.
                shell=page.locator('main .code-shell').first
                if page.locator('main .code-shell').count()!=page.locator('main pre').count() or shell.count()==0:
                    failures.append(f'{rel}: command blocks without copy button')
                else:
                    command=shell.locator('pre').inner_text().rstrip('\n')
                    shell.locator('button.copy-code').click()
                    page.wait_for_function('()=>document.querySelector("main .copy-status-live").textContent.length>0')
                    if page.evaluate('()=>navigator.clipboard.readText()')!=command: failures.append(f'{rel}: clipboard mismatch')
        for width in (320,375,768,1440):
            page.set_viewport_size(dict(width=width,height=1000))
            page.goto(urljoin(base,'kumihan-ko.html'),wait_until='networkidle')
            for mode in ('normal','keep-all'):
                wrap_comparisons.append(dict(width=width,word_break=mode,**page.evaluate('''(mode)=>{
                    const el=document.querySelector('h1');el.style.wordBreak=mode;
                    return {height:el.getBoundingClientRect().height,element_width:el.getBoundingClientRect().width,
                            text:el.textContent,font:getComputedStyle(el).fontFamily,
                            font_size:getComputedStyle(el).fontSize,overflow:el.scrollWidth>el.clientWidth};
                }''',mode)))
        for link in sorted(links):
            target=urlparse(link)
            if target.netloc!=urlparse(base).netloc: continue
            try:
                with urlopen(link.split('#')[0]) as response:
                    if response.status!=200:failures.append(f'link {link}: {response.status}')
                if target.fragment and target.path.endswith('.html'):
                    page.goto(link.split('#')[0],wait_until='domcontentloaded')
                    if page.locator(f'[id="{target.fragment}"]').count()==0: failures.append(f'missing fragment {link}')
            except Exception as err: failures.append(f'link {link}: {err}')
        browser.close()
    failures.extend(errors)
    report=dict(observations=observations,wrap_comparisons=wrap_comparisons,unique_local_links=sum(urlparse(x).netloc==urlparse(base).netloc for x in links),failures=failures,
                limitations=['Native browser text zoom not checked; root-font-size CSS simulation only.','Chromium/Linux installed fallback fonts only; native Korean editing not checked.'])
    (output/'site-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(f'{len(observations)} browser observations; {report["unique_local_links"]} local links; {len(failures)} failures')
    for failure in failures: print(failure)
    return bool(failures)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--base-url',default='http://127.0.0.1:8765/kumihan/')
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--chromium',default='/usr/bin/chromium')
    args=p.parse_args()
    raise SystemExit(check(args.base_url,args.output,args.chromium))
