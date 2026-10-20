"""Independent Chromium artifact QA; never native-host installation acceptance."""
from pathlib import Path
import json, hashlib, re, subprocess
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/development/ja-v020-20261020/qa/evidence'
OUT.mkdir(parents=True,exist_ok=True)
LABEL='2026年度・特別会員向けオンライン講座の受講登録を取り消す'
PROTECTED='髙﨑さま／料金１,２００円／が'
GROUPED='2026年度・<span class="term">特別会員向け</span><span class="term">オンライン</span><span class="term">講座</span>の<span class="term">受講登録</span>を<span class="term">取り消す</span>'
BASE=(ROOT/'tests/fixtures/ja_v020/web-contrasts.html').read_text()
# The historic fixture is retained in the previous commit and prior evidence.
BASE=re.sub(r'#PV-006 button\{[^}]*\}\.term\{[^}]*\}', '', BASE)
BASE=BASE.replace(GROUPED,LABEL).replace('2026年度・<span class="term">特別会員</span>向け<span class="term">オンライン</span><span class="term">講座</span>の<span class="term">受講登録</span>を<span class="term">取り消す</span>',LABEL)
FIXED=BASE.replace('</style>','#PV-006 button{width:270px;text-wrap:balance}.term{white-space:nowrap}</style>')
FIXED=FIXED.replace('<section id="PV-006"><h2>PV-006</h2><button>'+LABEL,'<section id="PV-006"><h2>PV-006</h2><button>'+GROUPED)
# Brief precedes the authored artifact; input is deliberately fictional, no conversion claims.
brief='''# Web artifact brief (recorded before authoring)\nMode build, standard review. Primary web-marketing with web-ui and editorial regions. Fictional event information prototype, not an offer or backend. Reader must find date/place/price and exercise a local cancellation demo. Information order: event, required information, registration action, reading guidance, font comparison. Supplied special characters and long label are exact-repeat fields. Heading/body/UI use available Noto Sans CJK JP, 32/18/18px and 1.4/1.85/1.5 leading; notes 16px. Green action and white content have measured contrast. Fonts are system fonts, with a separately rendered serif fallback. No external assets, web fonts, testimonials or invented performance metrics.\n'''
(OUT/'web-brief.md').write_text(brief)
positive='''<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>文字の庭｜受講案内の検証用プロトタイプ</title><style>
*{box-sizing:border-box}html{font-size:18px}body{margin:0;color:#172d29;background:#f1f5f2;font-family:"Noto Sans CJK JP",sans-serif;line-height:1.85;line-break:strict}main{max-width:760px;margin:auto;padding:24px 16px 48px}header{border-top:6px solid #235d4c;padding-top:20px}h1{font-size:1.8rem;line-height:1.4;margin:.4em 0}h2{font-size:1.3rem;line-height:1.5}p{margin:1em 0}.eyebrow,small{font-size:.89rem}section{background:white;border:1px solid #bccbc4;padding:16px;margin:24px 0}dl{margin:0}dt{font-weight:700}dd{margin:0 0 .8em}button{display:block;width:100%;max-width:34rem;font:inherit;line-height:1.5;padding:16px 12px;border:2px solid #235d4c;background:#235d4c;color:white;text-wrap:balance;cursor:pointer}.term{white-space:nowrap}button:focus-visible{outline:4px solid #a24b00;outline-offset:4px}a{color:#164f85}a:focus-visible{outline:3px solid #a24b00}#status{border-left:4px solid #235d4c;padding-left:12px;min-height:3em}.note{font-size:.89rem}.glyph{font-size:2rem}.palt{font-feature-settings:"palt" 1}footer{border-top:1px solid #bccbc4;padding-top:16px}
</style><main><header><p class="eyebrow">検証用・架空のイベント案内</p><h1>文字の庭</h1><p>オンライン講座の受講案内</p><p>原稿と必須情報を保ちながら、読む順序と操作を確かめるプロトタイプです。</p></header>
<section aria-labelledby="details"><h2 id="details">開催と料金</h2><p id="event-source">文字の庭／2026年11月3日／文字の広場（架空会場）</p><dl><dt>日時</dt><dd id="date">2026年11月3日</dd><dt>会場</dt><dd id="place">文字の広場（架空会場）</dd><dt>宛名と料金</dt><dd id="protected">'''+PROTECTED+'''</dd></dl><p class="note">架空の案内です。実際の申込や決済はできません。</p></section>
<section aria-labelledby="registration"><h2 id="registration">受講登録の確認</h2><p>以下のボタンで、この画面内の操作デモを実行できます。</p><button id="cancel" type="button">'''+GROUPED+'''</button><p id="status" role="status">操作デモはまだ実行していません。</p></section>
<article aria-labelledby="reading"><h2 id="reading">資料を読む前に</h2><p>日本語の本文では、見出しから説明、注記へと順に読めることを確かめます。文字を小さくして押し込めるのではなく、必要な情報が見える配置を選びます。長い文章は段落ごとに話題を分け、画面の幅に合わせて自然に折り返します。日付や料金などの保護された値は、見た目の都合で書き換えません。</p><p>本文中の<span lang="en">OpenType features and accessible controls</span>は、日本語との混在を比較するための英語です。ここで示す文字の間隔や改行は、実際のフォントと画面の条件に依存します。表示を確認できなかった環境について、合格したとは報告しません。</p></article>
<section aria-labelledby="fonts"><h2 id="fonts">言語と字形の比較</h2><p class="glyph"><span id="ja-glyph" lang="ja">日本語：骨</span>／<span id="tw-glyph" lang="zh-Hant-TW" style="font-family:'Noto Sans CJK TC',sans-serif">繁體中文：骨</span></p><p class="note">この比較だけで地域字形の正しさを認定しません。</p><p id="normal-display">「文字の庭」で、読む時間を。</p><p id="palt-display" class="palt">「文字の庭」で、読む時間を。</p></section>
<footer><a href="#details">開催と料金に戻る</a><p class="note">ブラウザー内の検証用成果物。実ホストへのスキル導入確認とは別の記録です。</p></footer></main><script>document.querySelector('#cancel').addEventListener('click',()=>{document.querySelector('#status').textContent='操作デモを実行しました。実際の受講登録は変更していません。'})</script></html>'''
negative='''<!doctype html><html lang="ja"><meta charset="utf-8"><title>Deliberate negative, not accepted</title><style>body{font:18px "Noto Sans CJK JP"}button{width:160px;white-space:nowrap;overflow:hidden}div{height:20px;overflow:hidden}</style><h1>意図した失敗対照</h1><button>'''+LABEL+'''</button><div>2026年11月3日<br>文字の広場（架空会場）</div></html>'''
(OUT/'web-positive.html').write_text(positive)
(OUT/'web-negative.html').write_text(negative)
(OUT/'v01-before.html').write_text(BASE)
(OUT/'v01-after.html').write_text(FIXED)
LINE_JS='''e=>{let w=document.createTreeWalker(e,NodeFilter.SHOW_TEXT),t,m={};while(t=w.nextNode())for(let i=0;i<t.length;i++){let r=new Range;r.setStart(t,i);r.setEnd(t,i+1);let q=r.getBoundingClientRect();if(q.width){let key=q.y.toFixed(2);if(!m[key])m[key]={text:"",x:q.x,right:q.right,y:q.y};m[key].text+=t.textContent[i];m[key].right=q.right}}let c=getComputedStyle(e);return {text:e.textContent,lines:Object.values(m),clientWidth:e.clientWidth,scrollWidth:e.scrollWidth,clientHeight:e.clientHeight,scrollHeight:e.scrollHeight,font:c.fontFamily,fontSize:c.fontSize,rect:e.getBoundingClientRect().toJSON()}}'''
results={'environment':{},'v01':[],'web':[],'limits':['Native browser text zoom not-checked; 200% shown by CSS root-font enlargement only.','No native skill installation/invocation; local source-guided artifact only.','Regional glyph correctness needs authorized glyph reference; font resolution alone is not certification.','Local cancellation demo has no backend.']}
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 results['environment']={'browser':b.version,'executable':'/usr/bin/chromium','fonts':subprocess.check_output(['fc-match','Noto Sans CJK JP'],text=True).strip()}
 pg=b.new_page(viewport={'width':320,'height':900})
 for stage,content in [('before',BASE),('width270',BASE.replace('</style>','#PV-006 button{width:270px;text-wrap:balance}</style>')),('group240',FIXED.replace('width:270px','width:240px')),('after',FIXED)]:
  for width in [320,375,768,1024]:
   for scale in [1,2]:
    pg.set_viewport_size({'width':width,'height':900});pg.set_content(content);pg.evaluate('document.fonts.ready')
    if scale==2:pg.add_style_tag(content='body{font-size:36px}')
    pg.locator('#PV-006 button').focus();pg.keyboard.press('Enter')
    pg.locator('#PV-006').screenshot(path=str(OUT/f'v01-{stage}-{width}-css{scale*100}.png'))
    obs=pg.locator('#PV-006 button').evaluate(LINE_JS)
    obs.update(stage=stage,width=width,cssScale=scale,focus=pg.locator('#PV-006 button').evaluate('e=>e===document.activeElement'),exactText=obs['text']==LABEL)
    results['v01'].append(obs)
 for width in [320,375,768,1024,1440]:
  for state in ['normal','css200','spacing','fallback']:
   pg.set_viewport_size({'width':width,'height':1000});pg.set_content(positive);pg.evaluate('document.fonts.ready')
   if state=='css200':pg.add_style_tag(content='html{font-size:36px}')
   if state=='spacing':pg.add_style_tag(content='*{line-height:1.5!important;letter-spacing:.12em!important}p{margin-bottom:2em!important}[lang=en]{word-spacing:.16em!important}')
   if state=='fallback':pg.add_style_tag(content='body{font-family:"Nonexistent Webfont", "Noto Serif CJK JP",serif}')
   pg.locator('#cancel').focus();pg.keyboard.press('Enter');pg.locator('#cancel').click()
   pg.screenshot(path=str(OUT/f'web-{width}-{state}.png'),full_page=True)
   obs=pg.locator('#cancel').evaluate(LINE_JS)
   cdp=pg.context.new_cdp_session(pg);cdp.send('DOM.enable');cdp.send('CSS.enable');root=cdp.send('DOM.getDocument')['root']['nodeId']
   font_runs={}
   for selector in ['#cancel','#protected','#ja-glyph','#tw-glyph']:
    node=cdp.send('DOM.querySelector',{'nodeId':root,'selector':selector})['nodeId']
    font_runs[selector]=cdp.send('CSS.getPlatformFontsForNode',{'nodeId':node})
   ax=cdp.send('Accessibility.getFullAXTree')
   if width==320 and state=='normal':(OUT/'web-accessibility-tree.json').write_text(json.dumps(ax,ensure_ascii=False,indent=2))
   obs.update(width=width,state=state,fonts=font_runs,document=pg.evaluate('({width:innerWidth,scrollWidth:document.documentElement.scrollWidth})'),protectedExact=pg.locator('#protected').text_content()==PROTECTED,labelExact=pg.locator('#cancel').text_content()==LABEL,dateExact=pg.locator('#date').text_content()=='2026年11月3日',placeExact=pg.locator('#place').text_content()=='文字の広場（架空会場）',eventExact=pg.locator('#event-source').text_content()=='文字の庭／2026年11月3日／文字の広場（架空会場）',mandatoryBounds=pg.locator('#event-source').evaluate(LINE_JS),status=pg.locator('#status').text_content(),focus=pg.locator('#cancel').evaluate('e=>e===document.activeElement'),bodyFont=pg.locator('article p').first.evaluate('e=>getComputedStyle(e).fontFamily'))
   obs['regionLines']={}
   for selector in ['h1','#event-source','#protected','article p','#status']:
    obs['regionLines'][selector]=[x.evaluate(LINE_JS) for x in pg.locator(selector).all()]
   assert all(obs[k] for k in ['protectedExact','labelExact','dateExact','placeExact','eventExact','focus'])
   assert obs['document']['scrollWidth']==width and obs['scrollWidth']<=obs['clientWidth']
   assert '操作デモを実行しました。' in obs['status']
   results['web'].append(obs)
 pg.set_content(negative);pg.set_viewport_size({'width':320,'height':900});pg.screenshot(path=str(OUT/'web-negative-320.png'),full_page=True)
 results['negative']={'button':pg.locator('button').evaluate(LINE_JS),'expectation':'failed visual artifact: clipped label and hidden venue; negative regression is not positive acceptance'}
 b.close()
assert all(x['exactText'] and x['focus'] for x in results['v01'])
assert all(x['scrollWidth']<=x['clientWidth'] for x in results['v01'])
assert any(x['stage']=='before' and x['cssScale']==1 and x['lines'][0]['text'].endswith('オ') for x in results['v01'])
assert all(not any(l['text'].endswith('オ') for l in x['lines']) for x in results['v01'] if x['stage']=='after')
results['protectedInputs']={k:{'text':v,'codepoints':['U+%04X'%ord(c) for c in v],'utf8sha256':hashlib.sha256(v.encode()).hexdigest()} for k,v in {'label':LABEL,'special':PROTECTED,'event':'文字の庭／2026年11月3日／文字の広場（架空会場）'}.items()}
(OUT/'web-observations.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
(ROOT/'tests/fixtures/ja_v020/web-contrasts.html').write_text(FIXED)
print('Wrote',len(results['v01']),'V01 states and',len(results['web']),'positive artifact states')
