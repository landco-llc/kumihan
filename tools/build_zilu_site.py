#!/usr/bin/env python3
"""Generate 12 static, translated ZiLu pages; no runtime translation or JS."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from seo_adapter import seo_outputs
from version_display import version_outputs
import argparse
import html
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PREFIX='/kumihan/'
SOURCE='https://github.com/landco-llc/kumihan/tree/main/plugins/kumihan-zilu'
C={
'':dict(lang='zh-Hans-CN',og='zh_CN',title='让简体中文的排版更有章法',h1='让文字有章法 也有呼吸',lead='KUMIHAN｜字律是一组面向简体中文的开源 Skills 与插件。它帮助 AI 在制作网页、文章、报告和演示文稿时更认真地处理文字结构、标点、换行与版面，同时尊重原稿和设计目的。',skip='跳转到正文',nav='主要导航',language='语言',concept='排版不是把字塞进框里',skills='四个独立 Skills 按任务选择',install='选择你使用的 AI 工具',cta='查看安装方法',source='查看源代码',principles=[('标点与换行','根据语义、句读与实际显示宽度检查行首行末，避免把禁则简单等同于强行改写。'),('中英混排','区分中文、英文字母、数字、符号与界面代码，让间距服从内容，而不改动原始字符。'),('原文保护','姓名、品牌、价格、数字、引用和批准过的文案不会因为“排版优化”被悄悄替换。'),('有证据的检查','明确区分静态检查、真实渲染和人工判断；尚未验证的结果不会被标成通过。')],roles=['确定语言、媒介、目标与修改范围','网页、文章、界面与响应式排版','报告、文档和演示文稿','不修改原文件的只读检查'],limits='这是面向内容设计的辅助工具，而不是自动保证排版质量的引擎。不同设备、字体及输出格式仍需要实际检查。',example='保留《书名》、“引号”、——、……与日期 2026年10月18日。显示调整与原文变更分开记录。',guide='安装指南',download='下载与核验',steps='安装步骤',verify='在 downloads 目录使用 sha256sum -c SHA256SUMS.txt（macOS 可用 shasum -a 256 -c）。只下载单个ZIP时对照 MANIFEST.json 对应项校验。',invoke='开始使用与更新',prompt='请使用 kumihan-zilu-review，在保留原文、数字和商标的前提下检查这个页面。',update='更新前备份定制，核验新版文件，再使用Host的更新或重新安装流程。若没有安装入口，可从GitHub读取SKILL.md作为人工指导；这不等于插件安装。',status='源代码与网页已公开。各 AI 工具中的原生插件调用、商店上架以及 Office・PDF 的显示质量需要另行验证。',hostnotes={
'chatgpt':['前提：账户与客户端需提供插件或Skills导入入口。完整插件与单个Skill不可混用。','下载完整插件，解压后用客户端支持的插件导入入口选择 kumihan-zilu 文件夹。只支持Skills时，从下方下载四个独立Skill ZIP并通过Skills入口安装。','仅把文件附到聊天不代表已安装。原生发现、图标显示与调用未验证；无入口时请使用源码手动指导。'],
'claude':['前提：Claude Code CLI；Claude chat 的Skills上传取决于账户功能。','解压完整插件，然后以 claude --plugin-dir /absolute/path/kumihan-zilu 启动。用 claude plugin validate /absolute/path/kumihan-zilu 验证目录（若当前版本支持）。','Claude chat 使用下方单个Skill ZIP，在真正的Skills上传入口导入。会话本地加载与官方商店上架是不同事实。'],
'gemini':['前提：支持Extensions的Gemini CLI。Gemini App 的Skills上传未验证。','把完整Extension ZIP解压到空目录，确认根部存在 gemini-extension.json，再运行 gemini extensions install /absolute/path/to/folder，并阅读安装器的权限提示。','单个Skill ZIP可解压为独立目录，通过CLI当前支持的Skills安装流程使用。不要把本仓库根URL当作字律Extension；根部属于其他产品。App导入只在实际账户提供入口时尝试。']}),
'.en':dict(lang='en',og='en_US',title='Thoughtful typography for Simplified Chinese',h1='Give every character room to make sense',lead='KUMIHAN｜字律 is an open-source set of skills and plugins for creating and reviewing Simplified Chinese websites, documents and presentations with AI. It focuses on punctuation, line breaks, mixed Chinese and Latin text, source preservation and evidence-based quality checks.',skip='Skip to content',nav='Main navigation',language='Language',concept='Typography starts with the content',skills='Four independent skills for your task',install='Choose your AI tool',cta='Installation guides',source='View source on GitHub',principles=[('Punctuation & line breaks','Review meaning, punctuation and actual line boundaries at the target width. Keep proposed edits separate.'),('Mixed-script typography','Distinguish Chinese prose, Latin text, numbers and code. Adjust visual spacing without changing source characters.'),('Protect the source','Preserve names, brands, prices, numbers, quotations and approved copy.'),('Review with evidence','Distinguish static checks, rendered evidence and human judgment. Untested results never become passed.')],roles=['Set language, medium, purpose and change scope','Websites, articles, interfaces and responsive typography','Reports, documents and presentations','Read-only review without editing the original'],limits='KUMIHAN｜字律 is guidance, not an automatic guarantee of typography quality. Check the rendered output in the target environment.',example='Preserve 《书名》, “引号”, ——, …… and 2026年10月18日. Record display adjustments separately from source changes.',guide='Installation guide',download='Downloads & checksums',steps='Installation steps',verify='From downloads/, run sha256sum -c SHA256SUMS.txt (or shasum -a 256 -c on macOS). For one ZIP, compare its hash with the matching MANIFEST.json entry.',invoke='Invoke & update',prompt='Use kumihan-zilu-review to review this Simplified Chinese page without changing source text, numbers or brands.',update='Back up customizations, verify the new package, then use the host update or reinstall workflow. If no installation interface is available, read SKILL.md from GitHub as manual guidance; that is not plugin installation.',status='The source and website are public. Native plugin invocation in each AI tool, marketplace listing and Office/PDF rendering quality are verified separately.',hostnotes={
'chatgpt':['Prerequisite: an account and client with a plugin or Skills installation interface. A plugin bundle and individual skills are different packages.','Extract the full plugin and select the kumihan-zilu folder in the supported plugin import interface. For Skills-only clients, install the four individual skill ZIPs through the Skills interface.','Attaching a file to chat is not installation. Native discovery, icon display and invocation remain unverified. Without an import interface, use the source as manual guidance.'],
'claude':['Prerequisite: Claude Code CLI; Claude chat Skills upload depends on account availability.','Extract the full plugin and start claude --plugin-dir /absolute/path/kumihan-zilu. Validate with claude plugin validate /absolute/path/kumihan-zilu where supported.','For Claude chat, upload an individual skill ZIP through the actual Skills interface. Session-local plugin loading does not imply official marketplace listing.'],
'gemini':['Prerequisite: Gemini CLI with Extensions support. Gemini App Skills upload is NOT VERIFIED.','Extract the extension ZIP into an empty folder with gemini-extension.json at its root. Run gemini extensions install /absolute/path/to/folder and review its permission prompt.','Extract an individual skill ZIP into its own directory and use the CLI Skills workflow supported by your version. Do not install this monorepo root URL expecting ZiLu. App import is conditional on an actual account interface.']}),
'.ja':dict(lang='ja',og='ja_JP',title='簡体中国語の文字組を整える',h1='文字を整え 読むリズムをつくる',lead='KUMIHAN｜字律は、AIが簡体中国語のWebサイト・文書・プレゼンテーションを制作・レビューするためのオープンソースSkills／プラグインです。標点、改行、中英混植、原稿の保全、検証できる品質を大切にします。',skip='本文へ移動',nav='メインナビゲーション',language='言語',concept='内容から文字組を考える',skills='作業に合わせて選ぶ4つの独立Skills',install='利用するAIツールを選ぶ',cta='導入方法を見る',source='GitHubでソースを見る',principles=[('標点と改行','意味・句読・実際の表示幅から行頭行末を確認し、編集案と原文を分けます。'),('中英混植','中国語・英語・数字・コードを区別し、元の文字を変えずに表示上の間隔を検討します。'),('原文保護','姓名、ブランド、価格、数値、引用、承認済みコピーを保持します。'),('根拠のあるレビュー','静的検査・実描画・人の判断を分け、未検証を合格にしません。')],roles=['言語・媒体・目的・変更範囲を定める','Web・記事・UI・レスポンシブ組版','レポート・文書・スライド','原本を変更しない読取専用レビュー'],limits='KUMIHAN｜字律は自動組版の品質保証システムではありません。実際の描画と出力先の確認を必要とします。',example='《书名》、“引号”、——、……、2026年10月18日の原文を保持し、表示調整と文字列の変更を分けて記録します。',guide='導入ガイド',download='ダウンロードと検証',steps='導入手順',verify='downloads内で sha256sum -c SHA256SUMS.txt（macOSは shasum -a 256 -c）を実行します。単体ZIPのみならMANIFEST.jsonの該当SHA256と照合します。',invoke='起動と更新',prompt='kumihan-zilu-reviewで、原文・数字・商標を保持して簡体中国語ページをレビューしてください。',update='更新前に独自設定を保存し、新版のハッシュを照合してHostの更新・再インストール手順を使います。導入口がない場合はGitHubのSKILL.mdを手動の指針として参照できます。プラグインの導入済みとは扱いません。',status='ソースとWebページを公開しています。各AIツールでのネイティブなプラグイン呼出、アプリストア掲載、Office・PDFの表示品質は別の検証事項です。',hostnotes={
'chatgpt':['前提：プラグインまたはSkillsの導入口があるアカウントとクライアント。完全プラグインと単体Skillは別の配布物です。','完全ZIPを展開し、クライアントが提供するプラグイン導入口でkumihan-ziluフォルダを選びます。Skillsのみ対応する場合は、下の独立Skill ZIPをSkills導入口でインストールします。','会話への添付だけではインストールになりません。実Hostの発見・アイコン表示・呼出は未検証です。導入口がなければソースを手動参照してください。'],
'claude':['前提：Claude Code CLI。Claude chatのSkillsアップロードはアカウント機能に依存します。','完全プラグインを展開し、claude --plugin-dir /absolute/path/kumihan-ziluで起動します。対応版ではclaude plugin validate /absolute/path/kumihan-ziluで検証します。','Claude chatでは単体Skill ZIPを実際のSkills導入口からアップロードします。セッション単位の読込みと公式商店掲載は別です。'],
'gemini':['前提：Extensions対応のGemini CLI。Gemini AppのSkillsアップロードは未検証です。','Extension ZIPを空フォルダへ展開し、直下のgemini-extension.jsonを確認します。gemini extensions install /absolute/path/to/folderを実行し、権限確認を読んでください。','単体Skill ZIPは独立フォルダへ展開し、使用中CLIのSkills導入手順で利用します。リポジトリroot URLは別製品を選ぶため使いません。App導入は実際のアカウントに入口がある場合のみです。']})}
HOSTS={'chatgpt':'ChatGPT / Codex','claude':'Claude','gemini':'Gemini'}
ROLES=('entry','web','documents','review')

def e(s):return html.escape(s,quote=True)
def link(path,label,**attrs):
    return '<a href="'+e(path)+'"'+''.join(' '+k.rstrip('_').replace('_','-')+'="'+e(v)+'"' for k,v in attrs.items())+'>'+e(label)+'</a>'
def name(suffix,host=None):return f'docs/install-zilu-{host}{suffix}.html' if host else f'kumihan-zh-cn{suffix}.html'
def landing(suffix):
 # Every landing is authored with the KUMIHAN index hierarchy (see templates/).
 # Templates are the source of truth so --check verifies generated output.
 name={'':'zh','.en':'en','.ja':'ja'}[suffix]
 return (ROOT/'templates'/f'zilu-{name}-landing.html').read_text(encoding='utf-8')

from importlib.util import spec_from_file_location, module_from_spec
_frame_spec=spec_from_file_location('kumihan_install_frame',Path(__file__).with_name('install_frame.py'))
FRAME=module_from_spec(_frame_spec);_frame_spec.loader.exec_module(FRAME)
GUIDE_UI={
'':dict(breadcrumb='安装指南',toc_title='本页目录',toc_summary='展开本页目录',platforms='选择 AI 平台',note_title='SOURCE & WEBSITE / v0.1.0',note='各 AI 工具中的原生安装与调用尚未验证。部分操作可能无法在你的使用环境中执行。',source='查看安装说明原文',lead='选择适合你的安装方式：完整插件或四个独立 Skills。',top='返回字律首页',footer='面向 AI 辅助设计的简体中文排版 Skills'),
'.en':dict(breadcrumb='Installation guide',toc_title='On this page',toc_summary='Show page contents',platforms='Select an AI platform',note_title='SOURCE & WEBSITE / v0.1.0',note='Native installation and invocation in each AI tool remain unverified. Some steps may be unavailable in your environment.',source='View source README',lead='Choose the full plugin or the four individual skills, depending on what your host supports.',top='Back to ZiLu home',footer='Simplified Chinese typography skills for AI-assisted design'),
'.ja':dict(breadcrumb='導入ガイド',toc_title='このページの目次',toc_summary='このページの目次を表示',platforms='AIプラットフォームを選ぶ',note_title='SOURCE & WEBSITE / v0.1.0',note='各AIツールでのネイティブな導入・呼出は未検証です。利用環境によっては掲載した操作が利用できない場合があります。',source='元の導入資料を開く',lead='完全プラグインか4つの独立Skillsか、ホストの対応に合わせて選べます。',top='字律のトップへ',footer='Simplified Chinese typography skills for AI-assisted design')}

def guide(suffix,host):
 c=C[suffix];g=dict(GUIDE_UI[suffix]);path=name(suffix,host)
 title='KUMIHAN｜字律 — '+c['guide']+' · '+HOSTS[host]
 alternates=''.join(f'<link rel="alternate" hreflang="{v["lang"]}" href="https://landco-llc.github.io/kumihan/{name(s,host)}">' for s,v in C.items())
 head=(f'<title>{e(title)}</title>\n<meta name="description" content="{e(g["lead"])}">\n<link rel="canonical" href="https://landco-llc.github.io/kumihan/{path}">{alternates}<link rel="alternate" hreflang="x-default" href="https://landco-llc.github.io/kumihan/{name("",host)}">\n'
       f'<meta property="og:type" content="website"><meta property="og:locale" content="{c["og"]}"><meta property="og:title" content="{e(title)}"><meta property="og:url" content="https://landco-llc.github.io/kumihan/{path}"><meta property="og:image" content="https://landco-llc.github.io/kumihan/assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png">\n<link rel="icon" href="{PREFIX}favicon.ico">')
 body=f'<section id="steps"><h2>01 / {c["steps"]}</h2><ol>'+''.join('<li>'+e(p)+'</li>' for p in c['hostnotes'][host])+'</ol>'
 official={'chatgpt':[('https://developers.openai.com/codex/skills/','Codex Skills'),('https://developers.openai.com/codex/plugins/','Codex Plugins')],'claude':[('https://code.claude.com/docs/en/plugins-reference','Claude Code plugins'),('https://support.claude.com/en/articles/12512180-using-skills-in-claude','Claude Skills')],'gemini':[('https://geminicli.com/docs/extensions/','Gemini CLI extensions'),('https://geminicli.com/docs/cli/skills/','Gemini CLI Skills')]}[host]
 body+='<p>'+ ' · '.join(link(u,t) for u,t in official)+'</p></section>'
 body+=f'<section id="download"><h2>02 / {c["download"]}</h2><p>{c["verify"]}</p><ul class="downloads">'
 folder=host if host!='chatgpt' else 'plugins';kind={'chatgpt':'plugin','claude':'claude-plugin','gemini':'gemini-extension'}[host]
 files=[folder+'/kumihan-zilu-'+kind+'-v0.1.0.zip']
 for role in ROLES:files.append(('skills' if host=='chatgpt' else host)+'/kumihan-zilu-'+role+('' if host=='chatgpt' else '-'+host)+'-skill-v0.1.0.zip')
 for f in files:body+='<li>'+link(PREFIX+'plugins/kumihan-zilu/downloads/'+f,f.split('/')[-1])+'</li>'
 body+='</ul><p>'+link(PREFIX+'plugins/kumihan-zilu/downloads/MANIFEST.json','MANIFEST.json')+' · '+link(PREFIX+'plugins/kumihan-zilu/downloads/SHA256SUMS.txt','SHA256SUMS.txt')+'</p></section>'
 body+=f'<section id="invoke"><h2>03 / {c["invoke"]}</h2><blockquote><p>{c["prompt"]}</p></blockquote><p lang="zh-Hans-CN">请保留原文与数字，使用 kumihan-zilu-web 检查页面。</p><p lang="en">Use kumihan-zilu-documents to review a report while preserving its source text.</p><p>{c["update"]}</p><p class="note">{c["status"]}</p></section>'
 body+='<aside class="note"><p lang="zh-Hans-CN">四个独立Skills：入口与范围、网页与界面、文档与演示、只读审查。</p><p lang="en">Four independent skills: start and scope, web and interfaces, documents and slides, read-only review.</p></aside>'
 g.update(skip=c['skip'],nav=c['nav'],language=c['language'],source_href=SOURCE,steps=c['steps'])
 frame=FRAME.Frame(lang=c['lang'],head=head,css=PREFIX+'assets/kumihan-install.css',asset_root=PREFIX,
  brand='KUMIHAN<span class="brand-sub" lang="zh-Hans-CN">｜字律</span>',home=PREFIX+name(suffix),
  hosts=[(t,PREFIX+name(suffix,h),h==host) for h,t in HOSTS.items()],
  languages=[(C[s]['lang'],label,PREFIX+name(s,host),s==suffix) for s,label in [('','简体中文'),('.en','English'),('.ja','日本語')]],
  number=f'{list(HOSTS).index(host)+1:02d}',title=e(c['guide']+' · '+HOSTS[host]),description=e(g['lead']),
  toc=[('steps',c['steps']),('download',c['download']),('invoke',c['invoke'])],content=body,platform=HOSTS[host],ui=g,
  footer_sub=e(g['footer'])+'<br>v0.1.0 · Apache-2.0 · Developed by L&amp;Co. LLC',
  footer_links=[('GitHub',SOURCE,True),('SHA256',SOURCE+'/downloads/SHA256SUMS.txt',True)],
  gateway=(PREFIX+FRAME.GATEWAYS[c['lang']][0],FRAME.GATEWAYS[c['lang']][1]))
 return FRAME.render(frame)

@version_outputs
@seo_outputs
def outputs():return {name(s,h):guide(s,h) if h else landing(s) for s in C for h in (None,*HOSTS)}
def main():
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args();out=outputs();changed=[n for n,b in out.items() if not (ROOT/n).exists() or (ROOT/n).read_text()!=b]
 if a.check:
  for n in changed:print('out of date: '+n)
  return int(bool(changed))
 for n in changed:(ROOT/n).write_text(out[n])
 print('Generated 12 ZiLu pages');return 0
if __name__=='__main__':raise SystemExit(main())
