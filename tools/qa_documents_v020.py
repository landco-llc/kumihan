"""Create bounded QA deliverables; not a document service or native host test."""
from pathlib import Path
import argparse, hashlib, json, subprocess, html, zipfile, tempfile, xml.etree.ElementTree as ET
import fitz
from playwright.sync_api import sync_playwright
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.oxml.xmlchemy import OxmlElement

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output-dir', type=Path, required=True, help='New empty output directory; historical evidence is never overwritten')
parser.add_argument('--chromium', help='Explicit Chromium executable; otherwise use installed Playwright browser')
args = parser.parse_args()
OUT = args.output_dir.resolve()
if OUT.exists() and any(OUT.iterdir()):
    parser.error('refusing to overwrite a nonempty evidence directory')
OUT.mkdir(parents=True, exist_ok=True)

def keep_phrase(markup):
    # Only three short lexical groups identified in W09-V03; never entire cells.
    for phrase in ('ありません。', '継続欄', 'しない。'):
        markup = markup.replace(phrase, '<span class="keep-phrase">' + phrase + '</span>')
    return markup
PROTECTED = ['髙﨑さま／料金１,２００円／が', '2026年度・特別会員向けオンライン講座の受講登録を取り消す', '2026年11月3日／文字の広場（架空会場）']
brief = {'purpose':'架空の講座運営担当が案内と取消手続の確認点を理解する。実在事業の実績を示さない。', 'audience':'画面で報告書とスライドを読む運営担当。印刷・投影条件は未確認。', 'profiles':['report-document','presentation'], 'adapters':['report','slide-deck'], 'intensity':'Standard', 'roles':{'report_body':'Noto Sans CJK JP 11pt / 1.7','report_heading':'20pt / 14pt','slides':'Noto Sans CJK JP title 30pt, body 22pt, note 16pt'},'protected':PROTECTED,'source':'HOST_SMOKE H-02 exact protected strings. Other copy and table/chart values are explicitly fictional QA inputs, not measured performance.'}
(OUT/'brief.json').write_text(json.dumps(brief, ensure_ascii=False, indent=2)+'\n')
rows = [{'id':f'{i:02}', 'task':['原稿照合','会場確認','案内確認','取消案内'][i%4], 'note':'必須情報を原稿と照合し、未確認の条件を記録する。担当内で確認し、結果を継続欄に残す。'} for i in range(1,45)]
(OUT/'source.json').write_text(json.dumps({'protected':PROTECTED,'table_rows':rows,'chart':{'label':'架空の作業配分（比較用入力、実績ではない）','values':[4,3,2,1]},'notes':'表の番号は架空の点検項目。実施済み件数ではない。'}, ensure_ascii=False,indent=2)+'\n')
paragraph='この報告書は、講座案内の原稿と表示を別々に確認するための架空の業務資料です。日本語とEnglishが混在する説明でも、見出し・本文・注記の役割を保ちます。値の抽出が一致しても、表示の欠けや図形による隠れがないことは別に確認します。'
css='''@page{size:A4;margin:20mm}body{font-family:"Noto Sans CJK JP",sans-serif;font-size:11pt;line-height:1.7;color:#182d39;line-break:strict}h1{font-size:24pt;line-height:1.4}h2{font-size:16pt}h1,h2{break-after:avoid}p{orphans:2;widows:2}.page{break-before:page}table{width:100%;border-collapse:collapse;font-size:10pt}thead{display:table-header-group}th,td{border-bottom:1px solid #a7b7bf;padding:9px 7px;text-align:left}th{background:#e8f1f3}tr{break-inside:avoid}td:first-child{width:28px}td:nth-child(2){width:70px}.note{font-size:9pt;border-left:3px solid #127b80;padding-left:12px}.field{padding:12px;border:1px solid #b8c6cd;line-height:1.8}'''
content=f'''<!doctype html><html lang="ja"><meta charset="utf-8"><title>架空講座 運営確認報告書</title><style>{css}</style><h1>架空講座の案内と<br>運営確認報告書</h1><p>QA実成果物／2026年10月20日</p><h2>1. 案内の必須情報</h2><div class="field">{html.escape(PROTECTED[0])}<br>{html.escape(PROTECTED[2])}</div><p>{paragraph}</p><h2>読み手と確認の順序</h2><p>日時と場所、料金と宛名、操作の目的の順に確認します。案内文を読み終える前に別の場所を探さなくて済むよう、必須情報を同じページにまとめます。</p><p class="note">注記：会場と講座は架空です。この資料は実際の予約や支払を受け付けません。</p><section class="page"><h2>2. 点検台帳（次ページへ継続）</h2><p>凡例：番号は点検項目の識別子。以下の台帳は架空の入力であり、QAの合格件数ではありません。各ページで列見出しを繰り返します。</p><table><thead><tr><th>番号</th><th>点検項目</th><th>継続欄／確認内容</th></tr></thead><tbody>'''
content+=''.join(f'<tr><td>{r["id"]}</td><td>{r["task"]}</td><td>{r["note"]}</td></tr>' for r in rows)
content+='</tbody></table><p class="note">台帳末尾の注記：最終項目44までの内容と、継続ページの見出しを確認する。台帳の空欄は実施済みを意味しない。</p></section>'
content+=f'''<section class="page"><h2>3. 取消案内と判断の境界</h2><div class="field">{html.escape(PROTECTED[1])}</div><p>{paragraph}</p><h2>表示と原稿の確認を分ける</h2><p>PDFの文字抽出は原稿保存の限定的な証拠です。全ページの画像で表、注記、行末と行頭、必須情報の見え方を確認します。実際のOfficeでの表示・編集、印刷機、会場の投影距離はこの検証に含みません。</p><h2>担当者への引継ぎ</h2><p>元の原稿を保存し、実表示の問題は場所と条件を添えて記録します。条件不明のまま可読性を保証せず、実機で確認する項目を明示します。</p><p class="note">補足凡例：原稿一致＝抽出範囲の比較。画像確認＝このレンダラーの表示。実ホスト確認＝別の検証。</p></section></html>'''
content = keep_phrase(content.replace('</style>', '.keep-phrase{white-space:nowrap}</style>'))
(OUT/'report.html').write_text(content)
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=args.chromium,args=['--no-sandbox'])
    page=browser.new_page()
    page.set_content(content,wait_until='load')
    page.evaluate('document.fonts.ready')
    (OUT/'report-dom-text.txt').write_text(page.locator('body').text_content())
    page.pdf(path=str(OUT/'report.pdf'),print_background=True,prefer_css_page_size=True)
    chromium=browser.version
    browser.close()

prs=Presentation(); prs.slide_width= Inches(13.333); prs.slide_height= Inches(7.5)
INK='183542'; TEAL='087F85'; PALE='E7F1F3'
def box(slide,x,y,w,h,text,size=22,color=INK,bold=False,fill=None):
    shape=slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    if fill:
        shape.fill.solid();shape.fill.fore_color.rgb=RGBColor.from_string(fill)
    tf=shape.text_frame;tf.word_wrap=True
    tf.margin_left=Inches(.12);tf.margin_right=Inches(.12)
    for i,line in enumerate(text.split('\n')):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph(); p.space_after=Pt(12)
        p._p.get_or_add_pPr().set('eaLnBrk','1');p._p.get_or_add_pPr().set('latinLnBrk','0')
        r=p.add_run();r.text=line;r.font.name='Noto Sans CJK JP';r.font.size=Pt(size);r.font.bold=bold;r.font.color.rgb=RGBColor.from_string(color)
        rp=r._r.get_or_add_rPr();rp.set('lang','ja-JP');ea=OxmlElement('a:ea');ea.set('typeface','Noto Sans CJK JP');rp.append(ea)
    return shape
def slide(title, note):
    s=prs.slides.add_slide(prs.slide_layouts[6]); box(s,.55,.35,12.2,.85,title,30,bold=True)
    box(s,.65,6.95,11,.3,'架空講座／受入QA用資料・実績値ではない',12,color='526B75')
    box(s,12,6.95,.7,.3,str(len(prs.slides)),12)
    s.notes_slide.notes_text_frame.text=note
    return s
s=slide('架空講座の案内と運営確認','目的：必須情報の確認手順を説明する。実会場での投影は未確認。')
box(s,.8,1.7,11.8,1.2,'原稿・表示・実ホストを分けて確認する',28,color=TEAL,bold=True)
box(s,.8,3.2,11.8,2.6,PROTECTED[2]+'\n'+PROTECTED[0],24)
s=slide('原稿から表示確認までの流れ','図の順番は確認手順。製品の自動処理能力を表していない。')
for x,t in [(1,'原稿の保存'),(4.9,'表示の確認'),(8.8,'条件の記録')]: box(s,x,2.2,3.3,1.2,t,25,bold=True,fill=PALE)
box(s,4.35,2.35,.6,.8,'→',28);box(s,8.25,2.35,.6,.8,'→',28)
box(s,1,4.2,11.4,1.3,'抽出一致だけでは、図形の隠れや行の欠けを保証できません。',24)
s=slide('確認方法の比較','表は方法の範囲を比較。すべての環境での合格を示さない。')
for y,cells in [(1.65,['方法','確認する範囲','残る確認']),(2.7,['原稿照合','文字と数値の保存','実表示']),(3.7,['画像確認','ページ・図表の見え方','実ホスト']),(4.7,['実機確認','対象アプリでの表示','実会場'])]:
    for x,w,text in zip([.8,3.4,9.3],[2.4,5.5,3.1],cells):
        box(s,x,y,w,.85,text,22,fill=PALE if y==1.65 else None)
s=slide('架空の作業配分（比較用入力）','値4、3、2、1は作図を確認するための架空入力であり、実績や測定結果ではない。')
for i,(name,value) in enumerate(zip(['原稿照合','表示確認','台帳確認','引継ぎ'],[4,3,2,1])):
    y=1.7+i*1.05;box(s,.8,y,2.3,.7,name,22);box(s,3.1,y,value*1.6,.65,'',fill=TEAL);box(s,3.3+value*1.6,y,.8,.7,str(value),22)
box(s,.8,6.1,11.6,.6,'単位：架空の作業単位。実施済み件数ではありません。',16)
s=slide('注意事項を図形で隠さない','注意枠はテキストの背景として先に配置。すべての必須情報は本文にも表示。')
box(s,.8,1.7,11.7,3.3,'',fill=PALE)
box(s,1.05,2,11.2,2.7,'必須情報を注記や図形の背面に移動しない\n文字と背景を同じ領域で確認する\n条件が不明な投影可読性は未確認とする',24,bold=True)
box(s,.9,5.45,11.7,.8,'日時・場所・料金は、読者が利用できる位置に残します。',22)
s=slide('長い取消案内をそのまま保つ','保護された文言は空白挿入や正規化を行わず保存。行の見え方を別に確認。')
box(s,.9,1.9,11.6,2.4,PROTECTED[1],28,bold=True,fill=PALE)
box(s,.9,4.8,11.5,1.4,'図の説明：取消案内の全文を独立した領域に置き、本文と注記の階層を保つ。操作を実行する画面ではありません。',20)
s=slide('注記と引継ぎの条件','注記は本文に表示。スピーカーノートだけに必須条件を移していない。')
box(s,.9,1.8,11.5,3.6,'・PDFの抽出一致と画像確認は別の証拠です。\n・Officeでの編集、印刷、実会場の投影は未確認です。\n・架空の講座と会場を利用したQA資料です。',24)
box(s,1,5.55,11.3,.7,'補足：元の文字列と入力JSONを成果物と一緒に保存する。',18,color=TEAL)
s=slide('まとめ：確認した範囲を引き継ぐ','このスライドは確認方針のまとめであり、リリース承認ではない。')
box(s,.9,1.7,11.5,3.5,'1. 原稿の文字と数値を変えない\n2. 全ページ・全スライドを見る\n3. 未確認の環境を明示する',27,bold=True)
box(s,.9,5.7,11.5,.7,'公開・本番更新にはOwner Gateが必要です。',21,color=TEAL)
prs.save(OUT/'presentation.pptx')
conversion=subprocess.run(['soffice','--headless','-env:UserInstallation=' + Path(tempfile.mkdtemp(prefix='kumihan-w09-lo-')).as_uri(),'--convert-to','pdf','--outdir',str(OUT),str(OUT/'presentation.pptx')],capture_output=True,text=True)
(OUT/'conversion.log').write_text(conversion.stdout+conversion.stderr)
results={'chromium':chromium,'libreoffice':subprocess.run(['soffice','--version'],capture_output=True,text=True).stdout.strip(),'conversion_returncode':conversion.returncode,'native_office':'not-checked','projection':'not-checked','files':{}}
for stem in ['report','presentation']:
    doc=fitz.open(OUT/f'{stem}.pdf');texts=[];pages=[]
    for i,page in enumerate(doc):
        page.get_pixmap(matrix=fitz.Matrix(1.25,1.25)).save(OUT/f'{stem}-{i+1:02}.png')
        t=page.get_text();texts.append(t)
        pages.append({'page':i+1,'dimensions_pt':list(page.rect),'text_length':len(t),'image':f'{stem}-{i+1:02}.png','text':t})
    all_text='\n'.join(texts);(OUT/f'{stem}-extracted.txt').write_text(all_text)
    results[stem]={'pages':pages,'pdf_fonts':[list(f) for page in doc for f in page.get_fonts()],'protected_exact_substring_extraction':{v:v in all_text for v in PROTECTED},'note':'Extraction can insert line breaks or renderer-specific Unicode mappings. No normalization is used for exact test.'}
pptx_text='\n'.join(shape.text for s in prs.slides for shape in s.shapes if shape.has_text_frame)
(OUT/'pptx-extracted.txt').write_text(pptx_text)
results['pptx_protected_exact']={v:v in pptx_text for v in PROTECTED}
results['pptx_slides']=len(prs.slides)
results['pptx_notes']=[s.notes_slide.notes_text_frame.text for s in prs.slides]
results['converter_fidelity']={'status':'passed' if all(results['presentation']['protected_exact_substring_extraction'].values()) else 'failed','priority':'P1','scope':'LibreOffice-export PDF exact PyMuPDF extraction; actual copy/paste not-checked','reason':'All protected exact substrings are present in PyMuPDF extraction.' if all(results['presentation']['protected_exact_substring_extraction'].values()) else 'At least one protected string is not an exact substring in PyMuPDF extraction; see extracted text.', 'visual':'not-checked', 'actual_copy_paste':'not-checked', 'native_office':'not-checked'}
with zipfile.ZipFile(OUT/'presentation.pptx') as z:
    texts=[]
    for i in range(1,9):
        root=ET.fromstring(z.read(f'ppt/slides/slide{i}.xml'))
        texts.extend(n.text or '' for n in root.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/main}t'))
    results['pptx_saved_xml_protected_exact']={v:any(v in t for t in texts) for v in PROTECTED}
    results['pptx_crc']=z.testzip()
for p in sorted(OUT.iterdir()):
    if p.is_file() and p.name != 'measurements.json':
        results['files'][p.name]={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
(OUT/'measurements.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:len(results[k]['pages']) for k in ['report','presentation']}))
