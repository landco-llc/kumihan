#!/usr/bin/env python3
"""Build independent Thai product pages; --check verifies committed output.

Copy follows packet 03; authoring context/evidence is in docs/thai-site-authoring.md.
"""
from pathlib import Path
import argparse
import html
import json

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://landco-llc.github.io/kumihan/'
SOURCE = 'https://github.com/landco-llc/kumihan/tree/feat/kumihan-th-host-parity-20261018/plugins/kumihan-th'
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

# Source candidates remain separate from the existing immutable v0.1.0 tag; v0.1.1 is not yet tagged.
CANDIDATE_BASE = 'https://github.com/landco-llc/kumihan/raw/refs/heads/feat/kumihan-th-host-parity-20261018/plugins/kumihan-th/downloads/'
DOWNLOAD = CANDIDATE_BASE
for language, texts in {
 'th': dict(status='v0.1.1 · ไฟล์ซอร์ส候補 ยังไม่เผยแพร่', candidate='ไฟล์ซอร์สสำหรับตรวจสอบ 15 ชุด ยังไม่มีไฟล์แนบ Release ต้องอนุมัติรุ่นและแท็กก่อนเผยแพร่ ตรวจ SHA256SUMS และ MANIFEST ก่อนใช้', claude='Claude Code: แตกไฟล์ปลั๊กอินและโหลดด้วย claude --plugin-dir /absolute/path/kumihan-th โดยมีชื่อเทคนิค kumihan-th ส่วน Claude Apps ให้นำเข้า Skill เดี่ยวเมื่อบัญชีรองรับ การยอมรับบนโฮสต์จริง: not-checked', gemini='Gemini CLI: แตกไฟล์ส่วนขยายแล้วใช้ gemini extensions link /absolute/path/kumihan-th ชื่อเทคนิคคือ kumihan-th ส่วน Gemini Apps ให้นำเข้า Skill เฉพาะเมื่อมีฟังก์ชันรองรับ มิฉะนั้นใช้เป็นบริบทงานและระบุข้อจำกัด การนำเข้าจริง: not-checked'),
 'en': dict(status='v0.1.1 · Source candidate; unpublished', candidate='15 source candidate archives are available for review. Release assets are not attached. Version/tag approval is required before publication; verify SHA256SUMS and MANIFEST.', claude='Claude Code: extract the plugin and load with claude --plugin-dir /absolute/path/kumihan-th. Technical installed ID: kumihan-th. Claude Apps: import individual Skill ZIPs only when your account supports this. Native acceptance: not-checked.', gemini='Gemini CLI: extract the extension and run gemini extensions link /absolute/path/kumihan-th. Technical installed ID: kumihan-th. Gemini Apps: use individual Skill ZIPs only if an import feature exists; otherwise use as task context. Native import acceptance: not-checked.'),
 'ja': dict(status='v0.1.1 · ソース候補・未公開', candidate='レビュー用ソース候補15本です。Release添付は未実施で、公開には版とタグの承認が必要です。SHA256SUMSとMANIFESTを確認してください。', claude='Claude Code：プラグインを展開し、claude --plugin-dir /absolute/path/kumihan-th で読み込みます。技術IDはkumihan-thです。Claude Apps：アカウントが対応する場合のみ単体Skillをインポートします。実ホスト受入：not-checked。', gemini='Gemini CLI：拡張を展開して gemini extensions link /absolute/path/kumihan-th を実行します。技術IDはkumihan-thです。Gemini Apps：対応するインポート機能がある場合のみ単体Skillを利用し、なければ作業文脈として利用します。実インポート受入：not-checked。')
}.items():
 UI[language].update(texts)
UI['th']['status']='v0.1.1 · ไฟล์ซอร์สสำหรับตรวจสอบ ยังไม่เผยแพร่'

def host_assets(host):
 prefix={'chatgpt':'','claude':'claude/','gemini':'gemini/'}[host]
 plugin={'chatgpt':'kumihan-th-plugin','claude':'kumihan-th-Claude-Code-plugin','gemini':'kumihan-th-Gemini-CLI-extension'}[host]
 suffix={'chatgpt':'','claude':'-Claude-skill','gemini':'-Gemini-Apps-skill'}[host]
 return [prefix+'plugins/'+plugin+'-v0.1.1.zip']+[prefix+'skills/'+name+suffix+'-v0.1.1.zip' for name in SKILLS]

def esc(s): return html.escape(str(s), quote=True)
def home(lang): return 'kumihan-th' + ('' if lang=='th' else '-'+lang) + '.html'
def guide(host,lang): return 'docs/install-kumihan-th-'+host+('' if lang=='th' else '.'+lang)+'.html'
def link(url,label,attrs=''): return f'<a href="{esc(url)}" {attrs}>{label}</a>'
def languages(lang,path,relative):
 return '<nav class="languages" aria-label="Language">'+''.join(link(relative+path(l),name,f'data-language lang="{l}" hreflang="{l}"'+(' aria-current="page"' if l==lang else '')) for l,name in [('th','ไทย'),('en','EN'),('ja','日本語')])+'</nav>'
def head(lang,path,title,description,pathfn):
 rel='../' if path.startswith('docs/') else ''
 alternates=''.join(f'<link rel="alternate" hreflang="{code}" href="{BASE+pathfn(l)}">' for l,code in [('th','th-TH'),('en','en'),('ja','ja'),('th','x-default')])
 return f'<!doctype html>\n<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#f5f3ee"><title>{esc(title)}</title><meta name="description" content="{esc(description)}"><link rel="canonical" href="{BASE+path}">{alternates}<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{BASE+path}"><meta property="og:locale" content="{dict(th="th_TH",en="en_US",ja="ja_JP")[lang]}"><meta property="og:image" content="{BASE}assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png"><meta property="og:image:alt" content="{NAME}"><link rel="icon" href="{rel}favicon.ico"><link rel="stylesheet" href="{rel}assets/thai-site.css"><script src="{rel}assets/thai-site.js" defer></script></head><body><a class="skip" href="#main">{UI[lang]["skip"]}</a>'
def footer(lang,rel=''):
 u=UI[lang]
 return '<footer><div class="shell">'+link(rel+home(lang),NAME)+link(SOURCE,u['source'])+link('https://github.com/landco-llc/kumihan/blob/main/LICENSE','Apache-2.0')+'<span>L&amp;Co. LLC</span></div></footer></body></html>\n'
def section(id,num,title,body):
 return f'<section class="section" id="{id}"><div class="shell"><div class="section-title"><span class="index">{num}</span><div><h2>{esc(title)}</h2>{body}</div></div></div></section>'
def landing(lang):
 c,u=COPY[lang],UI[lang]
 def get(*keys): return next(c[k] for k in keys if k in c)
 out=head(lang,home(lang),c['meta title'],c['meta description'],home)
 out+='<header><div class="shell header">'+link(home(lang),'KUMIHAN', 'class="brand"')+'<nav>'+''.join(link('#'+id,esc(get(*keys))) for id,keys in [('concept',('nav concept','concept H2','concept heading')),('skills',('nav skills','skills heading','skills title')),('install',('nav install','CTA 1'))])+'</nav>'+languages(lang,home,'')+'</div></header>'
 out+='<main id="main"><section class="hero"><div class="shell hero-grid"><div><p class="eyebrow">'+esc(c['eyebrow'])+'</p><h1><small>'+NAME+'</small>'+esc(c['hero H1'])+'</h1><p class="lead">'+esc(c['hero lead'])+'</p><div class="actions">'+link('#install',esc(c['CTA 1']),'class="button primary"')+link(SOURCE,esc(c['CTA 2']),'class="button"')+'</div><p class="note">'+esc(get('hero footnote','hero note'))+'</p></div><div class="hero-art"><img src="assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png" width="600" height="600" alt="'+NAME+'"><p>'+esc(u['status'])+'<br>th-TH · Apache-2.0</p></div></div></section>'
 out+=section('concept','01',get('concept heading','concept H2'),'<p class="lead">'+esc(c['concept body'])+'</p>')
 cards=''
 for i in range(1,5):
  title,_,desc=c[f'feature {i}'].partition(' — ')
  cards+=f'<article class="card"><p class="eyebrow">0{i}</p><h3>{esc(title)}</h3><p>{esc(desc)}</p></article>'
 out+=section('features','02',get('features title','feature title'),'<div class="grid">'+cards+'</div>')
 out+='<section class="band"><div class="shell"><p class="eyebrow">KUMIHAN / THAI</p><h2>'+esc(get('philosophy H2','idea H2'))+'</h2><p>'+esc(get('philosophy body','idea body'))+'</p></div></section>'
 cards=''
 for i,skill in enumerate(SKILLS,1):
  desc=c[f'skill {i}'].partition(' — ')[2]
  cards+='<article class="card"><h3>'+skill+'</h3><p>'+esc(desc)+'</p>'+link(guide('chatgpt',lang)+'#download',esc(u['download'])+' ↗')+'</article>'
 out+=section('skills','03',get('skills title','skills heading'),'<div class="grid">'+cards+'</div>')
 out+=section('install','04',c['install heading'],'<p class="lead">'+esc(c['install lead'])+'</p>'+''.join(link(guide(host,lang),'<strong>'+name+'</strong><span>'+u['guide']+' ↗</span>','class="host"') for host,name in HOSTS.items()))
 out+=section('status','05',get('release status heading','status heading'),'<div class="status"><strong>'+esc(u['status'])+'</strong><p>'+esc(get('release status body','status body'))+'</p><p>'+esc(u['candidate'])+'</p><p class="host-status">ChatGPT / Codex · Claude · Gemini: not-checked</p><p>'+esc(u['review'])+'</p>'+link(RELEASE,'Release Notes ↗')+'</div>')
 out+='<section class="final"><div class="shell"><h2>'+esc(c['final CTA'])+'</h2>'+link('#install',esc(c['CTA 1']),'class="button primary"')+'</div></section></main>'+footer(lang)
 return out

def installation(host,lang):
 u=UI[lang]; title={'th':f'ติดตั้ง {NAME} สำหรับ {HOSTS[host]}','en':f'Install {NAME} for {HOSTS[host]}','ja':f'{NAME}を{HOSTS[host]}へ導入'}[lang]
 path=guide(host,lang); pathfn=lambda l:guide(host,l)
 out=head(lang,path,title,u['intro'],pathfn)
 out+='<header><div class="shell header">'+link('../'+home(lang),'KUMIHAN','class="brand"')+languages(lang,pathfn,'../')+'</div></header><main id="main" class="shell guide">'+link('../'+home(lang),esc(u['back']))+'<p class="eyebrow">THAI / INSTALLATION</p><h1>'+esc(title)+'</h1><p class="host-label">'+esc(u['status'])+'</p><nav aria-label="Platform">'+''.join(link('../'+guide(h,lang),name,'aria-current="page"' if h==host else '') for h,name in HOSTS.items())+'</nav>'
 ids=['format','download','steps','test','updates','limits']
 bodies=['<p>'+esc(u['intro'])+'</p>',  '<p>'+esc(u['candidate'])+'</p><ul class="download-list">'+''.join('<li>'+link(DOWNLOAD+asset,esc(u['format'] if i==0 else u['single'])+': '+asset.rsplit('/',1)[-1])+'</li>' for i,asset in enumerate(host_assets(host)))+'</ul><p>'+link(DOWNLOAD+'SHA256SUMS.txt','SHA256SUMS')+' · '+link(DOWNLOAD+'MANIFEST.json','MANIFEST')+' · '+link(RELEASE,'Release Notes')+'</p>' , '<p>'+esc(u['steps'])+'</p><p>'+esc(u[{'chatgpt':'codex','claude':'claude','gemini':'gemini'}[host]])+'</p><p>'+link(SOURCE+'/INSTALL.md',esc(u['read']))+'</p>', '<pre class="sample" id="sample">'+esc(u['sample'])+'</pre><button type="button" class="copy" data-copy="sample" data-success="'+esc(u['copied'])+'" data-failure="'+esc(u['failure'])+'">'+esc(u['copy'])+'</button><p class="host-status">native installation: not-checked · native invocation: not-checked</p>', '<p>'+esc(u['update'])+'</p>', '<p>'+esc(u['limits'])+'</p><p>'+esc(u['review'])+'</p>']
 out+='<nav aria-label="Contents">'+''.join(link('#'+id,esc(name)) for id,name in zip(ids,u['sections']))+'</nav>'
 out+=''.join(f'<section id="{id}"><p class="eyebrow">0{i+1}</p><h2>{esc(name)}</h2>{body}</section>' for i,(id,name,body) in enumerate(zip(ids,u['sections'],bodies)))
 return out+'</main>'+footer(lang,'../')

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
 files={home(l):landing(l) for l in COPY}
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
