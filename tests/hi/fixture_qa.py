"""Manual Chromium/Poppler fixture runner; run with local HTTP server on 8765."""
import json,hashlib,sys,subprocess
from pathlib import Path
from html import escape
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'plugins/kumihan-hi/runtime'));import checks
cases=json.loads((R/'plugins/kumihan-hi/fixtures/qa.json').read_text())
texts=['कि की कु कू कृ के कै को कौ','क्षि क्षी त्रि ज्ञ श्र स्त्री','प्रार्थना संस्कृति दृष्टि राष्ट्र','र्क / क्र','क़ / क़','ज़ फ़ ड़ ढ़','हंस हँस माँ यहाँ नहीं लड़कियाँ','क्\u200dष','क्\u200cष','र्\u200dय','हिंदी / हिन्दी','निःशुल्क / समय: 10:30','नमस्ते। “स्वागत है!” (नई जानकारी)','माता-पिता','₹1,23,456.78 / ₹१,२३,४५६.७८','250 ग्राम / 250 g / 12.5%','KUMIHAN के साथ हिंदी में लिखें','विश्वविद्यालय','क्षि']
body=''.join(f'<p id="Q{i:02}" lang="hi">{escape(t)}</p>' for i,t in enumerate(texts,1))
html='<html lang="hi"><meta charset="utf-8"><style>@font-face{font-family:Test;src:url(http://127.0.0.1:8765/assets/fonts/NotoSansDevanagari.ttf)}body{font-family:Test,"Noto Sans Devanagari";font-size:22px;line-height:1.8}p{padding:.2em}</style>'+body+'</html>'
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=b.new_page(viewport={'width':768,'height':1400});page.set_content(html);page.evaluate('document.fonts.ready')
 for i,t in enumerate(texts,1):
  q=cases[i-1];actual=page.locator(f'#Q{i:02}').text_content();assert actual==t
  q['text']=t;q['codepoints']=[f'U+{ord(c):04X}' for c in t];q['static_status']='passed: exact UTF-8 DOM text round-trip';q['source_sha256']=hashlib.sha256(t.encode()).hexdigest();q['render_status']='Observed in Chromium screenshot; glyph interpretation requires separate review'
 page.screenshot(path='/tmp/hi-fixtures.png',full_page=True)
 # Same-style/changed-style boundaries compared, not assumed to be universal violations.
 page.set_content(html+'<p id="same">क्<span>षि</span></p><p id="different">क्<span style="font-weight:bold">षि</span></p><p id="block">क्<span style="display:inline-block">षि</span></p>');page.evaluate('document.fonts.ready');page.screenshot(path='/tmp/hi-boundaries.png',full_page=True)
 cases[18]['operation_status']='Observed same-style, changed-weight and inline-block variants; no editing/shaping guarantee'
 # Segmenter observation is version-scoped, not a correctness oracle.
 seg=page.evaluate('''() => Object.fromEntries(['क्षि','स्त्री','क्‍ष','क्‌ष'].map(t=>[t,[...new Intl.Segmenter('hi',{granularity:'grapheme'}).segment(t)].map(x=>x.segment)]))''')
 # Language comparison Q10.
 langs={}
 for lang in ['hi','mr','ne']:
  page.locator('#Q10').evaluate('(e,l)=>e.lang=l',lang);langs[lang]=page.locator('#Q10').text_content()
 cases[9]['operation_status']='Observed DOM language hi/mr/ne preserves source; language-specific glyph differences NOT_CHECKED'
 page.pdf(path='/tmp/hi-fixture.pdf',print_background=True)
 b.close()
subprocess.run(['pdftotext','-layout','/tmp/hi-fixture.pdf','/tmp/hi-fixture-extracted.txt'],check=True)
extracted=Path('/tmp/hi-fixture-extracted.txt').read_text();matches={f'Q{i:02}':t in extracted for i,t in enumerate(texts,1)}
cases[19]['static_status']='PDF extraction measured separately';cases[19]['extraction_exact_substring']=matches;cases[19]['render_status']='PDF visual NOT_CHECKED; extraction misses some exact strings, do not use PDF as text master'
for n in [20,21,22]:cases[n]['render_status']='See browser-results.json for webfont failure, viewport, text200 and spacing observations; no universal PASS'
cases[23]['operation_status']='NOT_CHECKED: IME, deletion and screen reader unavailable'
report={'method':'Chromium rendered fixture; exact DOM text; optional read-only Python comparison; Poppler extraction', 'cases':cases,'segmenter_observed':seg,'language_comparison_text':langs,'pdf_exact_matches':matches,'not_checked':['native speaker','full Hindi glyph correctness','native devices','Office','IME','screen reader']}
(Path('/tmp/kumihan-hi-qa-results.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('19 exact DOM source round-trips; PDF exact substrings',sum(matches.values()),'/',len(matches));print('segmenter',seg)
