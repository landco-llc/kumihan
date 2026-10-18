#!/usr/bin/env python3
"""Build independent Thai product pages; --check verifies committed output.

Copy follows packet 03; authoring context/evidence is in docs/thai-site-authoring.md.
"""
from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec

_index_spec = spec_from_file_location("kumihan_th_japanese_index", Path(__file__).with_name("build_th_ja_index.py"))
_index_module = module_from_spec(_index_spec)
_index_spec.loader.exec_module(_index_module)
render_th_japanese_index = _index_module.render
_th_index_spec = spec_from_file_location("kumihan_th_thai_index", Path(__file__).with_name("build_th_th_index.py"))
_th_index_module = module_from_spec(_th_index_spec)
_th_index_spec.loader.exec_module(_th_index_module)
render_th_thai_index = _th_index_module.render
_en_index_spec = spec_from_file_location("kumihan_th_english_index", Path(__file__).with_name("build_th_en_index.py"))
_en_index_module = module_from_spec(_en_index_spec)
_en_index_spec.loader.exec_module(_en_index_module)
render_th_english_index = _en_index_module.render
import argparse
import html
import json

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://landco-llc.github.io/kumihan/'
SOURCE = 'https://github.com/landco-llc/kumihan/tree/main/plugins/kumihan-th'
RELEASE = 'https://github.com/landco-llc/kumihan/releases/tag/kumihan-th-v0.1.1'
DOWNLOAD = 'https://github.com/landco-llc/kumihan/releases/download/kumihan-th-v0.1.1/'
NAME = 'KUMIHAN｜ดุลอักษร'
SKILLS = ['kumihan-th', 'kumihan-th-web', 'kumihan-th-documents', 'kumihan-th-review']
HOSTS = {'chatgpt':'ChatGPT / Codex', 'claude':'Claude', 'gemini':'Gemini'}
COPY = json.loads((ROOT/'assets/thai-site-copy.json').read_text())
UI = {
 'th': dict(skip='ข้ามไปยังเนื้อหา',back='กลับหน้าแรก',download='ดาวน์โหลด',source='ดูซอร์สโค้ด',guide='คู่มือติดตั้ง',status='v0.1.1 · สถานะตาม GitHub Release',review='ข้อความภาษาไทยยังต้องตรวจทานโดยบรรณาธิการเจ้าของภาษา',sections=['เลือกวิธีติดตั้ง','ดาวน์โหลดไฟล์','ขั้นตอนการติดตั้ง','ตรวจสอบการทำงาน','การอัปเดต','ข้อจำกัด'],intro='เลือกไฟล์ปลั๊กอินอิสระ หรือ Skill เดี่ยวตามความสามารถของโฮสต์ ไม่ต้องติดตั้ง KUMIHAN ภาษาญี่ปุ่นหรือ字衡ก่อน ไฟล์ ZIP ของปลั๊กอินไม่ใช่ไฟล์ ZIP ของ Skill และการแนบไฟล์ในแชตไม่ใช่การติดตั้งปลั๊กอิน',candidate='ไฟล์ต่อไปนี้เป็นไฟล์สำหรับรุ่น v0.1.1 โปรดตรวจสอบสถานะใน GitHub Release และ SHA256SUMS ก่อนดาวน์โหลด หากยังไม่มี Release แสดงว่าเป็นรุ่นเตรียมเผยแพร่และไฟล์ยังไม่พร้อมใช้งาน',steps='ดาวน์โหลดและแตกไฟล์ Skill ที่ต้องการ อ่าน SKILL.md และไฟล์อ้างอิงที่ให้มาด้วย หากโฮสต์ไม่มีระบบติดตั้งที่รองรับ ให้ใช้เป็นคำแนะนำที่แนบในบริบทงานและระบุว่าเป็นการใช้งานตามเอกสาร ไม่ใช่การติดตั้งแบบเนทีฟ',codex='Codex: ใช้ระบบจัดการปลั๊กอินหรือ Skills ที่เวอร์ชันของคุณรองรับ หากรองรับปลั๊กอินในเครื่อง ให้เลือกโฟลเดอร์ปลั๊กอินที่แตกไฟล์แล้ว ChatGPT: ใช้การนำเข้า Skills เฉพาะเมื่อบัญชีและหน้าจอของคุณมีตัวเลือกนี้ ห้ามถือว่าการอัปโหลด ZIP เข้าแชตเป็นการติดตั้ง',claude='Claude: ใช้การนำเข้า Skills เฉพาะเมื่อบัญชีและเวอร์ชันของคุณรองรับ สำหรับ Claude Code ให้ใช้ระบบ Skills ตามเอกสารของเวอร์ชันที่ติดตั้ง ไฟล์ปลั๊กอิน ChatGPT/Codex ไม่ใช่ปลั๊กอิน Claude',gemini='Gemini: ชุดนี้ไม่มีส่วนขยาย Gemini แบบเนทีฟ ใช้ SKILL.md และไฟล์อ้างอิงเป็นคำแนะนำในบริบทงานเท่านั้น อย่านำไฟล์ปลั๊กอิน ChatGPT/Codex ไปลงทะเบียนเป็นส่วนขยาย Gemini',sample='ช่วยตรวจทานการขึ้นบรรทัดและเครื่องหมายวรรณยุกต์ในข้อความ “น้ำชา เก่ง ภาษาไทย” โดยไม่แก้ไขต้นฉบับ และแยกสิ่งที่ตรวจจริงออกจากข้อสังเกตที่ต้องตรวจต่อ',update='เก็บรุ่นเดิมไว้ก่อนอัปเดต ตรวจสอบแท็กและ SHA256SUMS ของรุ่นใหม่ แล้วแทนที่เฉพาะโฟลเดอร์ผลิตภัณฑ์นี้ หากต้องการย้อนกลับให้ใช้ไฟล์รุ่นเดิม หากต้องการถอนการติดตั้งให้ลบ Skill หรือปลั๊กอินผ่านระบบของโฮสต์ หรือเอาเอกสารออกจากบริบทงาน',limits='การติดตั้งและการเรียกใช้แบบเนทีฟบนทุกโฮสต์: not-checked การแบ่งคำและการแสดงผลขึ้นอยู่กับเอนจิน ฟอนต์ และสภาพแวดล้อม ต้องตรวจภาพที่แสดงจริงและความหมายโดยคน ไม่รับรองการแก้จัดหน้าอัตโนมัติ',copy='คัดลอก',copied='คัดลอกแล้ว',failure='คัดลอกไม่ได้ — เลือกข้อความแล้วคัดลอก',format='ปลั๊กอินอิสระ',single='Skill เดี่ยว',read='อ่านเอกสารต้นฉบับ'),
 'en': dict(skip='Skip to content',back='Back to home',download='Download',source='View source',guide='Installation guide',status='v0.1.1 · Check GitHub Release status',review='Native Thai editorial review: needs-review',sections=['Choose a delivery format','Download','Installation steps','Test without editing','Updates','Known limits'],intro='Choose the independent plugin or an individual skill for your host. Neither Japanese KUMIHAN nor ZiHeng is required. A plugin ZIP is not a skill ZIP; attaching a ZIP to a chat does not install a plugin.',candidate='These links target v0.1.1. Check GitHub Release and SHA256SUMS before downloading. If no release exists, this is a release candidate and the assets are not yet available.',steps='Download and extract the desired skill. Read SKILL.md and its bundled references. If your host has no supported installation flow, provide those files as task context and describe this as instruction-guided use, rather than native installation.',codex='Codex: use the plugin or skill manager supported by your version. If local plugin loading is supported, select the extracted plugin directory. ChatGPT: use skill import only when your account and interface expose that feature. Uploading a ZIP to a chat does not install it.',claude='Claude: use skill import only if supported by your account and version. For Claude Code, follow the skill mechanism documented for your installed version. The ChatGPT/Codex plugin ZIP is not a Claude plugin.',gemini='Gemini: this package has no native Gemini extension. Use SKILL.md and its bundled references as task context only. Do not register the ChatGPT/Codex plugin as a Gemini extension.',sample='Review line breaks and Thai vowel/tone marks in “น้ำชา เก่ง ภาษาไทย” without modifying the source. Separate observed checks from items that need manual review.',update='Keep the previous version before updating. Verify the new tag and SHA256SUMS, then replace only this product’s directory. Restore the previous package to roll back. Uninstall through your host’s skill/plugin manager, or remove the instructions from task context.',limits='Native installation and invocation across all hosts: not-checked. Segmentation and rendering depend on the engine, fonts and environment. Actual rendering and meaning need human review. No universal automatic typesetting correction is promised.',copy='Copy',copied='Copied',failure='Copy failed — select and copy the text',format='Independent plugin',single='Individual skill',read='Read source documentation'),
 'ja': dict(skip='本文へスキップ',back='ホームへ戻る',download='ダウンロード',source='ソースを見る',guide='導入ガイド',status='v0.1.1 · 公開状況はGitHub Releaseで確認',review='タイ語母語話者による校閲：needs-review',sections=['導入形式を選ぶ','ダウンロード','導入手順','原稿を変更しないテスト','更新','対応範囲と限界'],intro='ホストの対応に合わせて独立プラグイン、または単体Skillを選びます。日本語版KUMIHANや字衡の事前導入は不要です。プラグインZIPとSkill ZIPは異なります。チャットへの添付はプラグインのインストールではありません。',candidate='以下はv0.1.1の配布先です。ダウンロード前にGitHub Releaseの公開状況とSHA256SUMSを確認してください。Releaseがない場合は公開前の候補版であり、ファイルは未提供です。',steps='必要なSkillをダウンロードして展開し、SKILL.mdと同梱資料を読みます。対応する導入機能がない場合は作業の文脈として資料を渡し、ネイティブ導入ではなく指示文に沿った利用であると明示します。',codex='Codex：利用バージョンが対応するプラグイン／Skills管理機能を使います。ローカルプラグイン読み込みに対応する場合は展開したプラグインのフォルダーを選びます。ChatGPT：アカウントと画面にSkillsのインポート機能がある場合のみ利用します。チャットにZIPを添付しただけでは導入されません。',claude='Claude：アカウントとバージョンが対応する場合のみSkillsをインポートします。Claude Codeでは利用バージョンの公式資料にあるSkillsの仕組みに従います。ChatGPT/Codex用ZIPはClaudeプラグインではありません。',gemini='Gemini：本製品にはGeminiネイティブ拡張は含まれません。SKILL.mdと同梱資料を作業の文脈として利用します。ChatGPT/Codex用プラグインをGemini拡張として登録しないでください。',sample='「น้ำชา เก่ง ภาษาไทย」の改行と声調記号の表示を、元の原稿を変更せずにレビューしてください。実際に検査した項目と未検証事項を分けてください。',update='更新前に旧版を保存してください。新しいタグとSHA256SUMSを確認し、本製品のフォルダーのみ置き換えます。旧版への差し戻しでロールバックできます。削除はホストの管理機能で行うか、作業の文脈から資料を取り除きます。',limits='各ホストでのネイティブ導入・呼び出し：not-checked。語分割と表示はエンジン・フォント・環境に依存します。実描画と意味は人による確認が必要です。すべての組版を自動修正する保証はありません。',copy='コピー',copied='コピーしました',failure='コピーできません — テキストを選択してコピー',format='独立プラグイン',single='単体Skill',read='ソースの導入資料を読む')}

# Download links target the versioned Release; the v0.1.0 tag remains immutable.
for language, texts in {
 'th': dict(status='v0.1.1 · ตรวจสอบไฟล์ที่ GitHub Release', candidate='ดาวน์โหลดไฟล์ ZIP ทั้ง 15 ชุดจาก GitHub Release v0.1.1 และตรวจ SHA256SUMS กับ MANIFEST ก่อนติดตั้ง การเรียกใช้บนโฮสต์จริงยังไม่ได้ทดสอบ', claude='Claude Code: แตกไฟล์ปลั๊กอินและโหลดด้วย claude --plugin-dir /absolute/path/kumihan-th โดยมีชื่อเทคนิค kumihan-th ส่วน Claude Apps ให้นำเข้า Skill เดี่ยวเมื่อบัญชีรองรับ การยอมรับบนโฮสต์จริง: not-checked', gemini='Gemini CLI: แตกไฟล์ส่วนขยายแล้วใช้ gemini extensions link /absolute/path/kumihan-th ชื่อเทคนิคคือ kumihan-th ส่วน Gemini Apps ให้นำเข้า Skill เฉพาะเมื่อมีฟังก์ชันรองรับ มิฉะนั้นใช้เป็นบริบทงานและระบุข้อจำกัด การนำเข้าจริง: not-checked'),
 'en': dict(status='v0.1.1 · GitHub Release', candidate='Download the 15 versioned ZIP archives from GitHub Release v0.1.1 and verify SHA256SUMS and MANIFEST. Native installation and invocation remain unverified.', claude='Claude Code: extract the plugin and load with claude --plugin-dir /absolute/path/kumihan-th. Technical installed ID: kumihan-th. Claude Apps: import individual Skill ZIPs only when your account supports this. Native acceptance: not-checked.', gemini='Gemini CLI: extract the extension and run gemini extensions link /absolute/path/kumihan-th. Technical installed ID: kumihan-th. Gemini Apps: use individual Skill ZIPs only if an import feature exists; otherwise use as task context. Native import acceptance: not-checked.'),
 'ja': dict(status='v0.1.1 · GitHub Release', candidate='15本のZIPはGitHub Release v0.1.1から取得できます。導入前にSHA256SUMS・MANIFESTを照合してください。実ホストでの導入・呼び出しは未検証です。', claude='Claude Code：プラグインを展開し、claude --plugin-dir /absolute/path/kumihan-th で読み込みます。技術IDはkumihan-thです。Claude Apps：アカウントが対応する場合のみ単体Skillをインポートします。実ホスト受入：not-checked。', gemini='Gemini CLI：拡張を展開して gemini extensions link /absolute/path/kumihan-th を実行します。技術IDはkumihan-thです。Gemini Apps：対応するインポート機能がある場合のみ単体Skillを利用し、なければ作業文脈として利用します。実インポート受入：not-checked。')
}.items():
 UI[language].update(texts)
UI['th']['status']='v0.1.1 · GitHub Release'

def host_assets(host):
 prefix={'chatgpt':'','claude':'claude/','gemini':'gemini/'}[host]
 plugin={'chatgpt':'kumihan-th-plugin','claude':'kumihan-th-Claude-Code-plugin','gemini':'kumihan-th-Gemini-CLI-extension'}[host]
 suffix={'chatgpt':'','claude':'-Claude-skill','gemini':'-Gemini-Apps-skill'}[host]
 return [prefix+'plugins/'+plugin+'-v0.1.1.zip']+[prefix+'skills/'+name+suffix+'-v0.1.1.zip' for name in SKILLS]

def esc(s): return html.escape(str(s), quote=True)
def home(lang): return 'kumihan-th' + ('' if lang=='th' else '-'+lang) + '.html'
def guide(host,lang): return 'docs/install-kumihan-th-'+host+('' if lang=='th' else '.'+lang)+'.html'
def link(url,label,attrs=''): return f'<a href="{esc(url)}" {attrs}>{label}</a>'
# GitHub Release assets are flat; host_assets() retains repo-relative folders only
# for distribution inventory. The published URL must use the asset basename.
_frame_spec = spec_from_file_location("kumihan_install_frame", Path(__file__).with_name("install_frame.py"))
FRAME = module_from_spec(_frame_spec)
_frame_spec.loader.exec_module(FRAME)
GUIDE_UI={
 'th':dict(nav='คู่มือติดตั้ง',language='เลือกภาษา',breadcrumb='คู่มือติดตั้ง',toc_title='ในหน้านี้',toc_summary='แสดงสารบัญของหน้านี้',platforms='เลือกแพลตฟอร์ม AI',note_title='v0.1.1 / GitHub Release',note='การติดตั้งและเรียกใช้จริงบนโฮสต์ยังไม่ได้ทดสอบ (not-checked) ขั้นตอนบางอย่างอาจไม่มีในสภาพแวดล้อมของคุณ',source='อ่าน INSTALL.md ต้นฉบับ',steps='ขั้นตอนและข้อควรทราบ',top='กลับหน้าแรก',footer='Thai typography skills for AI-assisted design'),
 'en':dict(nav='Installation guides',language='Language',breadcrumb='Installation guide',toc_title='On this page',toc_summary='Show page contents',platforms='Select an AI platform',note_title='v0.1.1 / GitHub Release',note='Native installation and invocation are not-checked. Some steps may be unavailable in your environment.',source='View source INSTALL.md',steps='Steps & guidance',top='Back to home',footer='Thai typography skills for AI-assisted design'),
 'ja':dict(nav='導入ページ',language='表示言語',breadcrumb='導入ガイド',toc_title='このページの目次',toc_summary='このページの目次を表示',platforms='AIプラットフォームを選ぶ',note_title='v0.1.1 / GitHub Release',note='各ホストでの導入・呼び出しは未検証（not-checked）です。利用環境によっては掲載した操作が利用できない場合があります。',source='元のINSTALL.mdを開く',steps='手順と注意事項',top='ホームへ戻る',footer='Thai typography skills for AI-assisted design')}

def installation(host,lang):
 u=UI[lang]; g=dict(GUIDE_UI[lang]); title={'th':f'ติดตั้ง {NAME} สำหรับ {HOSTS[host]}','en':f'Install {NAME} in {HOSTS[host]}','ja':f'{HOSTS[host]}に{NAME}を導入'}[lang]
 path=guide(host,lang); pathfn=lambda l:guide(host,l)
 alternates=''.join(f'<link rel="alternate" hreflang="{code}" href="{BASE+pathfn(l)}">' for l,code in [('th','th-TH'),('en','en'),('ja','ja'),('th','x-default')])
 head=(f'<title>{esc(title)}</title>\n<meta name="description" content="{esc(u["intro"])}">\n<link rel="canonical" href="{BASE+path}">{alternates}\n'
       f'<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(u["intro"])}"><meta property="og:url" content="{BASE+path}"><meta property="og:locale" content="{dict(th="th_TH",en="en_US",ja="ja_JP")[lang]}"><meta property="og:image" content="{BASE}assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png"><meta property="og:image:alt" content="{NAME}">\n<link rel="icon" href="../favicon.ico">')
 ids=['format','download','steps','test','updates','limits']
 bodies=['<p>'+esc(u['intro'])+'</p>',  '<p>'+esc(u['candidate'])+'</p><ul class="download-list">'+''.join('<li>'+link(DOWNLOAD+asset.rsplit('/',1)[-1],esc(u['format'] if i==0 else u['single'])+': '+asset.rsplit('/',1)[-1])+'</li>' for i,asset in enumerate(host_assets(host)))+'</ul><p>'+link(DOWNLOAD+'SHA256SUMS.txt','SHA256SUMS')+' · '+link(DOWNLOAD+'MANIFEST.json','MANIFEST')+' · '+link(RELEASE,'Release Notes')+'</p>' , '<p>'+esc(u['steps'])+'</p><p>'+esc(u[{'chatgpt':'codex','claude':'claude','gemini':'gemini'}[host]])+'</p><p>'+link(SOURCE+'/INSTALL.md',esc(u['read']))+'</p>', '<pre class="sample" id="sample">'+esc(u['sample'])+'</pre><button type="button" class="copy" data-copy="sample" data-success="'+esc(u['copied'])+'" data-failure="'+esc(u['failure'])+'">'+esc(u['copy'])+'</button><p class="host-status">native installation: not-checked · native invocation: not-checked</p>', '<p>'+esc(u['update'])+'</p>', '<p>'+esc(u['limits'])+'</p><p>'+esc(u['review'])+'</p>']
 content=''.join(f'<section id="{id}"><h2>{i+1:02d} / {esc(name)}</h2>{body}</section>' for i,(id,name,body) in enumerate(zip(ids,u['sections'],bodies)))
 g.update(skip=u['skip'],source_href=SOURCE+'/INSTALL.md')
 frame=FRAME.Frame(lang=lang,head=head,css='../assets/kumihan-install.css',asset_root='../',
  brand='KUMIHAN<span class="brand-sub" lang="th">｜ดุลอักษร</span>',home='../'+home(lang),
  hosts=[(name,guide(h,lang).removeprefix('docs/'),h==host) for h,name in HOSTS.items()],
  languages=[(l,label,pathfn(l).removeprefix('docs/'),l==lang) for l,label in [('th','ไทย'),('en','English'),('ja','日本語')]],
  number=f'{list(HOSTS).index(host)+1:02d}',title=esc(title),description=esc(u['intro']),
  toc=list(zip(ids,u['sections'])),content=content,platform=HOSTS[host],ui=g,
  footer_sub=esc(g['footer'])+'<br>'+esc(u['status'])+' · Developed by L&amp;Co. LLC',
  footer_links=[('GitHub',SOURCE,True),('Apache-2.0','https://github.com/landco-llc/kumihan/blob/main/LICENSE',True)],
  scripts='\n<script src="../assets/thai-site.js" defer></script>',
  gateway=('../'+FRAME.GATEWAYS[lang][0],FRAME.GATEWAYS[lang][1]))
 return FRAME.render(frame)

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
 index={'th':render_th_thai_index,'en':render_th_english_index,'ja':render_th_japanese_index}
 files={home(l):index[l](ROOT, COPY[l]) for l in COPY}
 files.update({guide(h,l):installation(h,l) for h in HOSTS for l in COPY})
 stale=[]
 for name,content in files.items():
  path=ROOT/name
  if args.check:
   if not path.exists() or path.read_text()!=content:stale.append(name)
  else:path.write_text(content)
 if stale:raise SystemExit('Stale Thai site pages: '+', '.join(stale))
 print(f'Thai site: {len(files)} pages '+('verified' if args.check else 'built'))
if __name__=='__main__':main()
