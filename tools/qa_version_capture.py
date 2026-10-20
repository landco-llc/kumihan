#!/usr/bin/env python3
"""Capture real locally Jekyll-built version panels plus CSS-disabled fallback."""
import argparse, json
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/development/ja-v020-20261020/qa/evidence/version'
def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--phase',choices=('before','after'),required=True); parser.add_argument('--url',required=True); args=parser.parse_args()
    OUT.mkdir(exist_ok=True,parents=True); records=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
        for width in (320,1024):
            page=browser.new_page(viewport={'width':width,'height':900},device_scale_factor=1)
            for lang in ('ja','en','zh-Hant-TW'):
                page.goto(args.url); page.wait_for_load_state('networkidle')
                button=page.locator(f'button[data-set-lang="{lang}"]')
                button.click(); page.wait_for_timeout(100)
                panels=page.locator('.edition-version:visible'); panel=panels.first
                stem=f'{args.phase}-{lang}-{width}'
                page.screenshot(path=str(OUT/(stem+'-page.png')),full_page=True)
                panel.screenshot(path=str(OUT/(stem+'-styled.png')))
                styled=panels.evaluate_all('(els)=>els.map(e=>({text:e.textContent,innerText:e.innerText,width:e.clientWidth,scrollWidth:e.scrollWidth,html:e.outerHTML}))')
                (OUT/(stem+'.html')).write_text(page.content())
                ax=page.locator('body').aria_snapshot(); (OUT/(stem+'-accessibility.yml')).write_text(ax)
                page.evaluate("""()=>{document.querySelectorAll('style,link[rel=stylesheet]').forEach(e=>e.remove());document.querySelectorAll('.version-locale').forEach(e=>e.hidden=!e.classList.contains('version-'+({ja:'ja',en:'en','zh-Hant-TW':'zh'}[document.documentElement.lang])))}""")
                rawpanel=page.locator('.edition-version:visible').first
                rawpanel.screenshot(path=str(OUT/(stem+'-no-css.png')))
                records.append(dict(phase=args.phase,width=width,requestedLang=lang,actualLang=page.locator('html').get_attribute('lang'),togglePressed=button.get_attribute('aria-pressed'),styled=styled,rawText=rawpanel.text_content(),rawHTML=rawpanel.evaluate('(e)=>e.outerHTML')))
            page.close()
        browser.close()
    (OUT/(args.phase+'-measurements.json')).write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
