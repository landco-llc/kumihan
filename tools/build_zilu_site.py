#!/usr/bin/env python3
"""Generate 12 static, translated ZiLu pages; no runtime translation or JS."""
import argparse
import html
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PREFIX='/kumihan/'
SOURCE='https://github.com/landco-llc/kumihan/tree/main/plugins/kumihan-zilu'
C={
'':dict(lang='zh-Hans-CN',og='zh_CN',title='让简体中文的排版更有章法',h1='让文字有章法 也有呼吸',lead='KUMIHAN｜字律是一组面向简体中文的开源 Skills 与插件。它帮助 AI 在制作网页、文章、报告和演示文稿时更认真地处理文字结构、标点、换行与版面，同时尊重原稿和设计目的。',skip='跳转到正文',nav='主要导航',language='语言',concept='排版不是把字塞进框里',skills='四个独立 Skills 按任务选择',install='选择你使用的 AI 工具',cta='查看安装方法',source='查看源代码',principles=[('标点与换行','根据语义、句读与实际显示宽度检查行首行末，避免把禁则简单等同于强行改写。'),('中英混排','区分中文、英文字母、数字、符号与界面代码，让间距服从内容，而不改动原始字符。'),('原文保护','姓名、品牌、价格、数字、引用和批准过的文案不会因为“排版优化”被悄悄替换。'),('有证据的检查','明确区分静态检查、真实渲染和人工判断；尚未验证的结果不会被标成通过。')],roles=['确定语言、媒介、目标与修改范围','网页、文章、界面与响应式排版','报告、文档和演示文稿','不修改原文件的只读检查'],limits='这是面向内容设计的辅助工具，而不是自动保证排版质量的引擎。不同设备、字体及输出格式仍需要实际检查。',example='保留《书名》、“引号”、——、……与日期 2026年10月18日。显示调整与原文变更分开记录。',guide='安装指南',download='下载与核验',steps='安装步骤',verify='在 downloads 目录使用 sha256sum -c SHA256SUMS.txt（macOS 可用 shasum -a 256 -c）。只下载单个ZIP时对照 MANIFEST.json 对应项校验。',invoke='开始使用与更新',prompt='请使用 kumihan-zilu-review，在保留原文、数字和商标的前提下检查这个页面。',update='更新前备份定制，核验新版文件，再使用Host的更新或重新安装流程。若没有安装入口，可从GitHub读取SKILL.md作为人工指导；这不等于插件安装。',status='候选版本：等待最终公开批准。GitHub Release、Pages、各Host商店与原生调用分别验证；本页面不表示商店已上架。',hostnotes={
'chatgpt':['前提：账户与客户端需提供插件或Skills导入入口。完整插件与单个Skill不可混用。','下载完整插件，解压后用客户端支持的插件导入入口选择 kumihan-zilu 文件夹。只支持Skills时，从下方下载四个独立Skill ZIP并通过Skills入口安装。','仅把文件附到聊天不代表已安装。原生发现、图标显示与调用未验证；无入口时请使用源码手动指导。'],
'claude':['前提：Claude Code CLI；Claude chat 的Skills上传取决于账户功能。','解压完整插件，然后以 claude --plugin-dir /absolute/path/kumihan-zilu 启动。用 claude plugin validate /absolute/path/kumihan-zilu 验证目录（若当前版本支持）。','Claude chat 使用下方单个Skill ZIP，在真正的Skills上传入口导入。会话本地加载与官方商店上架是不同事实。'],
'gemini':['前提：支持Extensions的Gemini CLI。Gemini App 的Skills上传未验证。','把完整Extension ZIP解压到空目录，确认根部存在 gemini-extension.json，再运行 gemini extensions install /absolute/path/to/folder，并阅读安装器的权限提示。','单个Skill ZIP可解压为独立目录，通过CLI当前支持的Skills安装流程使用。不要把本仓库根URL当作字律Extension；根部属于其他产品。App导入只在实际账户提供入口时尝试。']}),
'.en':dict(lang='en',og='en_US',title='Thoughtful typography for Simplified Chinese',h1='Give every character room to make sense',lead='KUMIHAN｜字律 is an open-source set of skills and plugins for creating and reviewing Simplified Chinese websites, documents and presentations with AI. It focuses on punctuation, line breaks, mixed Chinese and Latin text, source preservation and evidence-based quality checks.',skip='Skip to content',nav='Main navigation',language='Language',concept='Typography starts with the content',skills='Four independent skills for your task',install='Choose your AI tool',cta='Installation guides',source='View source on GitHub',principles=[('Punctuation & line breaks','Review meaning, punctuation and actual line boundaries at the target width. Keep proposed edits separate.'),('Mixed-script typography','Distinguish Chinese prose, Latin text, numbers and code. Adjust visual spacing without changing source characters.'),('Protect the source','Preserve names, brands, prices, numbers, quotations and approved copy.'),('Review with evidence','Distinguish static checks, rendered evidence and human judgment. Untested results never become passed.')],roles=['Set language, medium, purpose and change scope','Websites, articles, interfaces and responsive typography','Reports, documents and presentations','Read-only review without editing the original'],limits='KUMIHAN｜字律 is guidance, not an automatic guarantee of typography quality. Check the rendered output in the target environment.',example='Preserve 《书名》, “引号”, ——, …… and 2026年10月18日. Record display adjustments separately from source changes.',guide='Installation guide',download='Downloads & checksums',steps='Installation steps',verify='From downloads/, run sha256sum -c SHA256SUMS.txt (or shasum -a 256 -c on macOS). For one ZIP, compare its hash with the matching MANIFEST.json entry.',invoke='Invoke & update',prompt='Use kumihan-zilu-review to review this Simplified Chinese page without changing source text, numbers or brands.',update='Back up customizations, verify the new package, then use the host update or reinstall workflow. If no installation interface is available, read SKILL.md from GitHub as manual guidance; that is not plugin installation.',status='Release candidate awaiting final publication approval. GitHub Release, Pages, marketplace listing and native invocation require separate verification. This page does not establish a marketplace listing.',hostnotes={
'chatgpt':['Prerequisite: an account and client with a plugin or Skills installation interface. A plugin bundle and individual skills are different packages.','Extract the full plugin and select the kumihan-zilu folder in the supported plugin import interface. For Skills-only clients, install the four individual skill ZIPs through the Skills interface.','Attaching a file to chat is not installation. Native discovery, icon display and invocation remain unverified. Without an import interface, use the source as manual guidance.'],
'claude':['Prerequisite: Claude Code CLI; Claude chat Skills upload depends on account availability.','Extract the full plugin and start claude --plugin-dir /absolute/path/kumihan-zilu. Validate with claude plugin validate /absolute/path/kumihan-zilu where supported.','For Claude chat, upload an individual skill ZIP through the actual Skills interface. Session-local plugin loading does not imply official marketplace listing.'],
'gemini':['Prerequisite: Gemini CLI with Extensions support. Gemini App Skills upload is NOT VERIFIED.','Extract the extension ZIP into an empty folder with gemini-extension.json at its root. Run gemini extensions install /absolute/path/to/folder and review its permission prompt.','Extract an individual skill ZIP into its own directory and use the CLI Skills workflow supported by your version. Do not install this monorepo root URL expecting ZiLu. App import is conditional on an actual account interface.']}),
'.ja':dict(lang='ja',og='ja_JP',title='簡体中国語の文字組を整える',h1='文字を整え 読むリズムをつくる',lead='KUMIHAN｜字律は、AIが簡体中国語のWebサイト・文書・プレゼンテーションを制作・レビューするためのオープンソースSkills／プラグインです。標点、改行、中英混植、原稿の保全、検証できる品質を大切にします。',skip='本文へ移動',nav='メインナビゲーション',language='言語',concept='内容から文字組を考える',skills='作業に合わせて選ぶ4つの独立Skills',install='利用するAIツールを選ぶ',cta='導入方法を見る',source='GitHubでソースを見る',principles=[('標点と改行','意味・句読・実際の表示幅から行頭行末を確認し、編集案と原文を分けます。'),('中英混植','中国語・英語・数字・コードを区別し、元の文字を変えずに表示上の間隔を検討します。'),('原文保護','姓名、ブランド、価格、数値、引用、承認済みコピーを保持します。'),('根拠のあるレビュー','静的検査・実描画・人の判断を分け、未検証を合格にしません。')],roles=['言語・媒体・目的・変更範囲を定める','Web・記事・UI・レスポンシブ組版','レポート・文書・スライド','原本を変更しない読取専用レビュー'],limits='KUMIHAN｜字律は自動組版の品質保証システムではありません。実際の描画と出力先の確認を必要とします。',example='《书名》、“引号”、——、……、2026年10月18日の原文を保持し、表示調整と文字列の変更を分けて記録します。',guide='導入ガイド',download='ダウンロードと検証',steps='導入手順',verify='downloads内で sha256sum -c SHA256SUMS.txt（macOSは shasum -a 256 -c）を実行します。単体ZIPのみならMANIFEST.jsonの該当SHA256と照合します。',invoke='起動と更新',prompt='kumihan-zilu-reviewで、原文・数字・商標を保持して簡体中国語ページをレビューしてください。',update='更新前に独自設定を保存し、新版のハッシュを照合してHostの更新・再インストール手順を使います。導入口がない場合はGitHubのSKILL.mdを手動の指針として参照できます。プラグインの導入済みとは扱いません。',status='最終公開承認待ちの候補版です。GitHub Release・Pages・各Hostの商店掲載・実呼出は別に検証します。このページは商店掲載を示しません。',hostnotes={
'chatgpt':['前提：プラグインまたはSkillsの導入口があるアカウントとクライアント。完全プラグインと単体Skillは別の配布物です。','完全ZIPを展開し、クライアントが提供するプラグイン導入口でkumihan-ziluフォルダを選びます。Skillsのみ対応する場合は、下の独立Skill ZIPをSkills導入口でインストールします。','会話への添付だけではインストールになりません。実Hostの発見・アイコン表示・呼出は未検証です。導入口がなければソースを手動参照してください。'],
'claude':['前提：Claude Code CLI。Claude chatのSkillsアップロードはアカウント機能に依存します。','完全プラグインを展開し、claude --plugin-dir /absolute/path/kumihan-ziluで起動します。対応版ではclaude plugin validate /absolute/path/kumihan-ziluで検証します。','Claude chatでは単体Skill ZIPを実際のSkills導入口からアップロードします。セッション単位の読込みと公式商店掲載は別です。'],
'gemini':['前提：Extensions対応のGemini CLI。Gemini AppのSkillsアップロードは未検証です。','Extension ZIPを空フォルダへ展開し、直下のgemini-extension.jsonを確認します。gemini extensions install /absolute/path/to/folderを実行し、権限確認を読んでください。','単体Skill ZIPは独立フォルダへ展開し、使用中CLIのSkills導入手順で利用します。リポジトリroot URLは別製品を選ぶため使いません。App導入は実際のアカウントに入口がある場合のみです。']})}
HOSTS={'chatgpt':'ChatGPT / Codex','claude':'Claude','gemini':'Gemini'}
ROLES=('entry','web','documents','review')

def e(s):return html.escape(s,quote=True)
def link(path,label,**attrs):
    return '<a href="'+e(path)+'"'+''.join(' '+k.rstrip('_').replace('_','-')+'="'+e(v)+'"' for k,v in attrs.items())+'>'+e(label)+'</a>'
def name(suffix,host=None):return f'docs/install-zilu-{host}{suffix}.html' if host else f'kumihan-zh-cn{suffix}.html'
def frame(suffix,body,host=None):
    c=C[suffix];path=name(suffix,host);title='KUMIHAN｜字律 — '+(c['guide']+' · '+HOSTS[host] if host else c['title'])
    head=''.join(f'<link rel="alternate" hreflang="{v["lang"]}" href="https://landco-llc.github.io/kumihan/{name(s,host)}">' for s,v in C.items())
    langs=''.join(link(PREFIX+name(s,host),label,lang=C[s]['lang'],hreflang=C[s]['lang'],**({'aria_current':'page'} if s==suffix else {})) for s,label in [('','简体中文'),('.en','English'),('.ja','日本語')])
    nav=''.join(link(PREFIX+name(suffix)+'#'+anchor,c[key]) for anchor,key in [('concept','concept'),('skills','skills'),('install','cta')])
    return f'''<!doctype html>
<html lang="{c['lang']}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(c['lead'])}">
<link rel="canonical" href="https://landco-llc.github.io/kumihan/{path}">{head}<link rel="alternate" hreflang="x-default" href="https://landco-llc.github.io/kumihan/{name('',host)}">
<meta property="og:locale" content="{c['og']}"><meta property="og:title" content="{e(title)}"><meta property="og:type" content="website"><meta property="og:url" content="https://landco-llc.github.io/kumihan/{path}"><meta property="og:image" content="https://landco-llc.github.io/kumihan/assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png">
<link rel="icon" href="{PREFIX}favicon.ico"><link rel="stylesheet" href="{PREFIX}assets/zilu-site.css"></head><body>
<a class="skip" href="#main">{c['skip']}</a><header class="shell"><a class="brand" href="{PREFIX+name(suffix)}">KUMIHAN｜字律</a><nav aria-label="{c['nav']}">{nav}</nav><nav class="languages" aria-label="{c['language']}">{langs}</nav></header>
<main id="main" class="shell" tabindex="-1">{body}</main><footer class="shell"><p>{e(c['limits'])}</p><p>v0.1.0 · Apache-2.0 · L&amp;Co. LLC</p><p>{link(PREFIX+'index.html','KUMIHAN')} · {link(SOURCE,c['source'])} · {link(SOURCE+'/downloads/SHA256SUMS.txt','SHA256')}</p></footer></body></html>
'''

def landing(suffix):
 c=C[suffix]
 heading='<span>让文字有章法</span> <span>也有呼吸</span>' if suffix=='' else c['h1']
 body=f'<section class="hero"><div><p class="eyebrow" lang="en">OPEN SOURCE · SIMPLIFIED CHINESE TYPOGRAPHY</p><h1>{heading}</h1><p class="lead">{c["lead"]}</p><div class="actions">{link("#install",c["cta"],class_="button")}{link(SOURCE,c["source"])}</div></div><figure><img src="{PREFIX}assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png" width="1254" height="1254" alt="KUMIHAN"><figcaption>KUMIHAN｜字律 · zh-Hans-CN</figcaption></figure></section>'
 body+=f'<section id="concept"><p class="eyebrow">01 / PRINCIPLES</p><h2>{c["concept"]}</h2><dl class="principles">'+''.join(f'<div><dt>{t}</dt><dd>{p}</dd></div>' for t,p in c['principles'])+'</dl><p class="example">'+c['example']+'</p></section>'
 body+=f'<section id="skills"><p class="eyebrow">02 / SKILLS</p><h2>{c["skills"]}</h2>'
 for i,role in enumerate(ROLES):
  skill='kumihan-zilu'+('' if role=='entry' else '-'+role)
  body+=f'<article class="row"><h3>{link(SOURCE+"/skills/"+skill,skill)}</h3><p>{c["roles"][i]}</p></article>'
 body+=f'</section><section id="install"><p class="eyebrow">03 / INSTALLATION</p><h2>{c["install"]}</h2>'
 for h,title in HOSTS.items():body+=f'<article class="row"><h3>{title}</h3>{link(PREFIX+name(suffix,h),c["cta"])}</article>'
 body+=f'</section><aside><p>{c["status"]}</p></aside>'
 return frame(suffix,body)

def guide(suffix,host):
 c=C[suffix]
 body=f'<section class="guide-hero"><p class="eyebrow">INSTALLATION / {HOSTS[host]}</p><h1>{c["guide"]} · {HOSTS[host]}</h1><p class="lead">KUMIHAN｜字律 · v0.1.0</p><nav class="hosts" aria-label="Host">'+''.join(link(PREFIX+name(suffix,h),t,**({'aria_current':'page'} if host==h else {})) for h,t in HOSTS.items())+'</nav></section>'
 body+=f'<section class="guide"><h2>{c["steps"]}</h2><ol>'+''.join('<li>'+e(p)+'</li>' for p in c['hostnotes'][host])+'</ol>'
 official={'chatgpt':[('https://developers.openai.com/codex/skills/','Codex Skills'),('https://developers.openai.com/codex/plugins/','Codex Plugins')],'claude':[('https://code.claude.com/docs/en/plugins-reference','Claude Code plugins'),('https://support.claude.com/en/articles/12512180-using-skills-in-claude','Claude Skills')],'gemini':[('https://geminicli.com/docs/extensions/','Gemini CLI extensions'),('https://geminicli.com/docs/cli/skills/','Gemini CLI Skills')]}[host]
 body+='<p>'+ ' · '.join(link(u,t) for u,t in official)+'</p></section>'
 body+=f'<section class="guide"><h2>{c["download"]}</h2><p>{c["verify"]}</p><ul class="downloads">'
 folder=host if host!='chatgpt' else 'plugins';kind={'chatgpt':'plugin','claude':'claude-plugin','gemini':'gemini-extension'}[host]
 files=[folder+'/kumihan-zilu-'+kind+'-v0.1.0.zip']
 for role in ROLES:files.append(('skills' if host=='chatgpt' else host)+'/kumihan-zilu-'+role+('' if host=='chatgpt' else '-'+host)+'-skill-v0.1.0.zip')
 for f in files:body+='<li>'+link(PREFIX+'plugins/kumihan-zilu/downloads/'+f,f.split('/')[-1])+'</li>'
 body+='</ul><p>'+link(PREFIX+'plugins/kumihan-zilu/downloads/MANIFEST.json','MANIFEST.json')+' · '+link(PREFIX+'plugins/kumihan-zilu/downloads/SHA256SUMS.txt','SHA256SUMS.txt')+'</p></section>'
 body+=f'<section class="guide"><h2>{c["invoke"]}</h2><blockquote>{c["prompt"]}</blockquote><p lang="zh-Hans-CN">请保留原文与数字，使用 kumihan-zilu-web 检查页面。</p><p lang="en">Use kumihan-zilu-documents to review a report while preserving its source text.</p><p>{c["update"]}</p><p>{c["status"]}</p></section>'
 body+='<aside><p lang="zh-Hans-CN">四个独立Skills：入口与范围、网页与界面、文档与演示、只读审查。</p><p lang="en">Four independent skills: start and scope, web and interfaces, documents and slides, read-only review.</p></aside>'
 return frame(suffix,body,host)

def outputs():return {name(s,h):guide(s,h) if h else landing(s) for s in C for h in (None,*HOSTS)}
def main():
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args();out=outputs();changed=[n for n,b in out.items() if not (ROOT/n).exists() or (ROOT/n).read_text()!=b]
 if a.check:
  for n in changed:print('out of date: '+n)
  return int(bool(changed))
 for n in changed:(ROOT/n).write_text(out[n])
 print('Generated 12 ZiLu pages');return 0
if __name__=='__main__':raise SystemExit(main())
