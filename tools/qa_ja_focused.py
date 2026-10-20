"""Bounded synthetic diagnostics; no native host or reader-performance claim."""
from pathlib import Path
import json, hashlib
from fontTools.ttLib import TTCollection
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/development/ja-v020-20261020/qa/evidence/focused'
OUT.mkdir(parents=True,exist_ok=True)
font=Path('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
collection=TTCollection(font)
f=next(f for f in collection.fonts if any(n.nameID==1 and n.toUnicode()=='Noto Sans CJK JP' for n in f['name'].names))
features=sorted({r.FeatureTag for r in f['GPOS'].table.FeatureList.FeatureRecord})
source='''<!doctype html><html lang="ja"><meta charset="utf-8"><title>Focused QA diagnostics</title><style>
body{font:18px/1.8 "Noto Sans CJK JP",sans-serif;margin:20px;color:#182536;background:#fff}section{border:1px solid #aaa;padding:16px;margin-bottom:20px}h1{font-size:24px}h2{font-size:20px}.display{display:inline-block;font-size:30px}.palt{font-feature-settings:"palt" 1}.vertical{writing-mode:vertical-rl;height:210px;width:200px;line-break:strict;margin:20px auto}.viewport{height:300px;overflow-y:auto;overflow-x:hidden;border:2px solid #345}.sheet{height:250px;border-bottom:1px solid #aaa}p{line-break:strict}</style>
<h1>用途別の限定診断（合成入力）</h1><section><h2>PV-019／縦書き・下へ続く頁</h2><div class="viewport" id="scroll"><div class="sheet"><p class="vertical">縦書きの短い頁が下へ続く記事</p></div><div class="sheet"><p class="vertical">本文の続き。次の頁を下へ送って読みます。</p></div><div class="sheet"><p class="vertical">終わりの頁。主な移動軸は縦です。</p></div></div></section>
<section><h2>PV-021/022／任意のdisplay比較</h2><div class="display" id="normal">文字と余白の時間</div><br><div class="display palt" id="palt">文字と余白の時間</div><p id="body">道具の使い方を本文で説明します。</p><p>元の保護入力：<span id="original">文字と余白の時間／道具の使い方を本文で説明します。</span></p></section>
<section><h2>PV-030／文脈未確定の引用</h2><p id="quote">明日、こっちは17時で閉めます。</p><p>引用元の発話日、店舗、単独告知への転用権限は未確認です。日付や店舗を推測して補いません。</p><p>別の架空QA対照：2026年11月3日、文字の広場（架空会場）の案内窓口は17時で閉まります。</p></section></html>'''
(OUT/'diagnostics.html').write_text(source)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=b.new_page(viewport={'width':768,'height':900});page.set_content(source);page.evaluate('document.fonts.ready')
 obs=page.evaluate('''()=>({scroll:{width:scroll.clientWidth,scrollWidth:scroll.scrollWidth,height:scroll.clientHeight,scrollHeight:scroll.scrollHeight},normalWidth:normal.getBoundingClientRect().width,paltWidth:palt.getBoundingClientRect().width,bodyFeature:getComputedStyle(document.querySelector('#body')).fontFeatureSettings,source:original.textContent,quote:quote.textContent})'''.replace('scroll.client','document.querySelector("#scroll").client').replace('scroll.scroll','document.querySelector("#scroll").scroll'))
 session=page.context.new_cdp_session(page);session.send('DOM.enable');node=session.send('DOM.getDocument')['root']['nodeId']; fonts={}
 for selector in ['#normal','#palt','#body']:
  nid=session.send('DOM.querySelector',{'nodeId':node,'selector':selector})['nodeId'];fonts[selector]=None
 session.send('CSS.enable')
 for selector in fonts:
  nid=session.send('DOM.querySelector',{'nodeId':node,'selector':selector})['nodeId'];fonts[selector]=session.send('CSS.getPlatformFontsForNode',{'nodeId':nid})
 page.screenshot(path=str(OUT/'before-scroll.png'),full_page=True)
 page.locator('#scroll').evaluate('e=>e.scrollTop=350');obs['afterScrollTop']=page.locator('#scroll').evaluate('e=>e.scrollTop');page.screenshot(path=str(OUT/'after-scroll.png'),full_page=True)
 obs.update(browser=b.version,fonts=fonts,fontFile=str(font),fontSha256=hashlib.sha256(font.read_bytes()).hexdigest(),gposFeatures=features,nativeTextZoom='not-checked',physicalReading='not-checked')
 assert obs['afterScrollTop']>0 and obs['paltWidth']!=obs['normalWidth'] and obs['bodyFeature']=='normal' and 'palt' in features
 (OUT/'measurements.json').write_text(json.dumps(obs,ensure_ascii=False,indent=2)+'\n');b.close()
print('Focused scroll, resolved font/palt, static quote preservation diagnostics recorded')
