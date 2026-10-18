#!/usr/bin/env python3
"""Generate the 12 localized Arabic product pages; deterministic, no runtime translation."""
import argparse
from html import escape as e
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE='/kumihan/'
PUBLIC='https://landco-llc.github.io'+BASE
REPO='https://github.com/landco-llc/kumihan'
RELEASE=REPO+'/releases/download/kumihan-ar-v0.1.0/'
HOSTS={'chatgpt':'ChatGPT / Codex','claude':'Claude','gemini':'Gemini'}
ROLES=['kumihan-ar','kumihan-ar-web','kumihan-ar-documents','kumihan-ar-review']
COPY={
'ar':dict(title='حين تنتظم الحروف يتضح المعنى',lead='مهارات مفتوحة المصدر لتنسيق النص العربي في الويب والمستندات والعروض. نبدأ بالمحتوى والسياق، ونحافظ على النص الأصلي، ونفصل الفحص النصي عن العرض الفعلي.',skip='انتقل إلى المحتوى',nav='التنقل الرئيسي',language='اللغة',intro='التنضيد يبدأ بالمعنى',introtext='الاتجاه الصحيح جزء من القراءة. نعالج العربية والنصوص المختلطة بحسب سياقها، دون عكس الحروف أو تغيير الأسماء والأرقام لتناسب القالب.',features='أربع أولويات للقراءة',principles=[('اتجاه واضح','نميّز لغة النص عن اتجاه الفقرة والمحاذاة، ونعزل الروابط والرموز اللاتينية عند الحاجة.'),('الأصل محفوظ','نحافظ على الحركات والتطويل والمحارف غير المرئية والأسماء والأسعار كما وردت.'),('تصميم من السياق','نختار التسلسل والمسافات والخطوط المتاحة بحسب المحتوى والجمهور، دون وصفة خط ثابتة.'),('مراجعة بالدليل','نفصل الفحص الثابت عن المشاهدة في المتصفح وعن الحكم التحريري. ما لم يُختبر يبقى غير مفحوص.')],idea='مساحة للنص ووضوح للقارئ',ideatext='لا نضيف زخرفة لملء الفراغ. لكل عنوان وفقرة ورابط وظيفة تخدم المحتوى. لا نغيّر ترتيب Unicode لإصلاح العرض.',skills='أربع مهارات مستقلة',roles=['تحديد اللغة والوسيط والهدف ونطاق التعديل.','صفحات الويب والواجهات والاتجاه والنصوص المختلطة.','المستندات والتقارير والعروض مع بيان حدود التحقق.','مراجعة للقراءة فقط دون تعديل الأصل.'],install='ابدأ من أداتك المعتادة',installtext='اختر حزمة أداتك أو مهارة مستقلة. تتوفر خمس حزم لكل منصة، مع بصمات للتحقق من الملفات.',cta='ابدأ الاستخدام',source='استعرض المصدر',status='حدود التحقق',limit='هذه إرشادات مساعدة، وليست شهادة لجودة التنضيد. التثبيت والاستدعاء في التطبيقات الأصلية غير مفحوصين. الصياغة العربية تحتاج مراجعة متحدث أصلي.',pending='الإصدار قيد النشر',available='حزم الإصدار',guide='دليل التثبيت',steps='التثبيت حسب المنصة',downloads='التنزيل والتحقق',verify='قارن بصمة SHA-256 بالملف المنشور. ضع الحزم الخمس المختارة في مجلد واحد ونفّذ أمر GNU التالي، وتحقق من ظهور OK لكل الملفات الخمسة. لملف واحد أو macOS قارن ناتج shasum -a 256 مع MANIFEST.json.',invoke='الاستخدام والتحديث',prompt='استخدم kumihan-ar-review لمراجعة هذه الصفحة دون تغيير النص الأصلي أو الأسماء أو الأرقام. افصل الملاحظات الثابتة عن العرض الذي شاهدته.',update='احتفظ بنسخة من تخصيصاتك، وتحقق من الإصدار الجديد قبل إعادة التثبيت. إرفاق ملف بالمحادثة لا يثبت تثبيت المهارة.',back='العودة إلى صفحة المنتج',free='مجاني ومفتوح المصدر',notes={
'chatgpt':['تحقق من وجود واجهة لتثبيت الإضافات أو المهارات في حسابك وعميلك. تختلف إتاحة ChatGPT عن Codex.','في Codex، فك أرشيف مهارة مستقلة وضع مجلدها في .agents/skills/ داخل مشروعك، ثم اطلب استخدام المهارة بالاسم. راجع وثائق نسختك للتثبيت الكامل.','في ChatGPT استخدم واجهة الاستيراد إن كانت متاحة. إن لم تكن متاحة، اقرأ SKILL.md كتوجيه يدوي؛ هذا ليس تثبيت إضافة.'],
'claude':['للاستخدام في Claude Code، فك أرشيف الإضافة في مجلد مستقل.','ابدأ جلسة محلية باستخدام الأمر أدناه. أما Claude chat فيستخدم أرشيف مهارة مستقلة عبر واجهة Skills إن كانت متاحة.','التحميل المحلي لا يعني الإدراج في متجر رسمي. اكتشاف المهارات واستدعاؤها على الحساب الفعلي غير مفحوصين.'],
'gemini':['يلزم Gemini CLI يدعم Extensions. فك الأرشيف وتأكد من وجود gemini-extension.json في جذر المجلد.','ثبّت المجلد المحلي باستخدام الأمر أدناه، وراجع مطالبة الصلاحيات.','أرشيفات المهارات مستقلة. الاستيراد في Gemini Apps يدوي وغير متحقق؛ لا تستخدم حزمة CLI على أنها حزمة تطبيق المحادثة.']}),
'en':dict(title='When letters fall into place, meaning comes through',lead='Open-source skills for Arabic websites, documents and presentations. Start with the content and context, preserve the original text, and distinguish source checks from observed rendering.',skip='Skip to content',nav='Main navigation',language='Language',intro='Typography starts with meaning',introtext='Direction is part of reading. Handle Arabic and mixed scripts in context without reversing characters or changing names and numbers to fit a layout.',features='Four priorities for readable text',principles=[('Clear direction','Distinguish language, paragraph direction and alignment. Isolate Latin links and identifiers where their context calls for it.'),('Source integrity','Preserve diacritics, intentional Tatweel, invisible controls, names and prices exactly as supplied.'),('Context-led design','Choose hierarchy, spacing and available typefaces for the content and audience. A fixed font recipe cannot replace that choice.'),('Evidence-based review','Separate static diagnostics, observed browser rendering and editorial judgment. Unchecked results remain unchecked.')],idea='Room for the text and clarity for the reader',ideatext='Every heading, paragraph and link serves the content. Do not add decoration to fill space or change Unicode order to repair display.',skills='Four independent skills',roles=['Set the language, medium, purpose and editing scope.','Websites, interfaces, direction and mixed scripts.','Documents, reports and slides with explicit verification limits.','Read-only review without modifying the original.'],install='Start with the tool you use',installtext='Choose your host bundle or a standalone skill. Each platform has five packages with file checksums.',cta='Get started',source='View the source',status='Verification limits',limit='These are assisted workflows, not typography certification. Native host installation and invocation are not checked. Arabic copy needs native-speaker review.',pending='Release pending',available='Release packages',guide='Installation guide',steps='Install for your platform',downloads='Downloads and verification',verify='Compare SHA-256 with the published checksum file. With your five selected ZIPs in one directory, run the GNU command below and confirm that all five are reported OK. For a single ZIP, compare its hash with MANIFEST.json; on macOS use shasum -a 256 and compare the matching entry.',invoke='Use and update',prompt='Use kumihan-ar-review to review this page without changing source text, names or numbers. Separate static findings from rendering you actually observed.',update='Back up customizations and verify the new version before reinstalling. Attaching a file to chat does not establish skill installation.',back='Back to the product',free='Free and open source',notes={
'chatgpt':['Check that your account and client offer a plugin or Skills installation interface. Availability differs between ChatGPT and Codex.','For Codex, extract an individual skill folder into your project’s .agents/skills/, then request the skill by name. Consult your client’s documentation for plugin installation.','In ChatGPT, use the actual import interface if available. Otherwise read SKILL.md as manual guidance; that is not plugin installation.'],
'claude':['For Claude Code, extract the full plugin into its own directory.','Start a local session with the command below. For Claude chat, use an individual skill ZIP through the Skills interface where available.','Local loading does not establish official marketplace listing. Discovery and invocation on a real account remain not checked.'],
'gemini':['Use Gemini CLI with Extensions support. Extract the archive and locate gemini-extension.json at the folder root.','Install the local folder with the command below and review the permission prompt.','Individual skill archives are separate. Gemini Apps import is manual and unverified; a CLI extension is not a chat-app import package.']}),
'ja':dict(title='文字が整うと意味が伝わる',lead='アラビア語のWebサイト・文書・プレゼンテーションを制作するための、オープンソースのスキル集です。内容と目的から設計し、原文を守り、静的検査と実際の表示を分けて確認します。',skip='本文へ移動',nav='メインナビゲーション',language='言語',intro='文字組は意味から考える',introtext='文章の方向は、読みやすさの一部です。アラビア語と欧文が混在する場面を捉え、文字の逆転や、枠に合わせた名前・数値の書き換えを避けます。',features='読みやすさを支える4つの観点',principles=[('文章の方向','言語・段落方向・右揃えを区別し、URLや製品コードは文脈に応じて分離します。'),('原文の保全','母音記号、意図的な伸ばし、不可視文字、姓名、価格を元の文字列のまま保持します。'),('目的に合う設計','内容と読者に合わせて情報の順序・余白・利用可能な書体を選びます。固定の書体を押し付けません。'),('根拠のあるレビュー','静的検査・ブラウザでの実表示・編集上の判断を分け、未確認を合格にしません。')],idea='文字のための余白を読む人のための明快さを',ideatext='見出し・段落・リンクには、それぞれ役割があります。空間を埋めるための装飾や、表示のためのUnicode順序の変更は行いません。',skills='作業に合わせて選ぶ4つのスキル',roles=['言語・媒体・目的・変更範囲を定める。','Webサイト・UI・文章方向・多言語混植を扱う。','文書・レポート・スライドと検証の限界を扱う。','原本を変更しない、読み取り専用のレビュー。'],install='いつものAIツールからはじめよう',installtext='ホスト別の一式、または独立したスキルを選べます。各ホスト5パッケージと、ファイル照合用のハッシュを用意しています。',cta='導入方法を見る',source='ソースコードを見る',status='検証範囲について',limit='制作を支援する指針であり、文字組の品質認証ではありません。各ホストでのインストール・呼び出しは未確認です。アラビア語のコピーは母語話者による校閲が必要です。',pending='Release公開準備中',available='Release配布物',guide='導入ガイド',steps='ホストに合わせて導入する',downloads='ダウンロードと照合',verify='公開されたチェックサムとSHA-256を照合します。選んだ5 ZIPを同じフォルダに置き、次のGNUコマンドで5件すべてのOKを確認します。単体ZIPやmacOSではshasum -a 256の結果をMANIFEST.jsonの該当項目と照合します。',invoke='使い方と更新',prompt='kumihan-ar-reviewを使い、原文・名前・数値を変更せずにこのページをレビューしてください。静的な指摘と、実際に確認した表示を分けてください。',update='カスタマイズを保存し、新版を照合してから再インストールします。チャットへの添付だけでは、スキルのインストールを確認したことにはなりません。',back='製品ページに戻る',free='無料のオープンソース',notes={
'chatgpt':['アカウントとクライアントにPluginまたはSkillsの導入画面があるか確認します。ChatGPTとCodexでは利用条件が異なります。','Codexでは独立スキルのフォルダをプロジェクトの.agents/skills/に展開し、名前を指定して使用を依頼します。Plugin一式の導入は利用中のクライアントの公式手順に従います。','ChatGPTでは実際のインポート画面を使います。画面がなければSKILL.mdを手動の指針として読みます。これはPluginのインストールとは区別します。'],
'claude':['Claude CodeではPlugin一式を独立したフォルダに展開します。','次のコマンドでローカルセッションを開始します。Claude chatでは、利用可能なSkills画面から独立スキルZIPを取り込みます。','ローカルでの読み込みと公式マーケットへの掲載は別です。実アカウントでの検出・呼び出しは未確認です。'],
'gemini':['Extensionsに対応するGemini CLIを使います。展開先のルートにgemini-extension.jsonがあることを確認します。','次のコマンドでローカルフォルダを導入し、権限の確認画面を読みます。','独立スキルZIPは別の配布形式です。Gemini Appsへの取り込みは手動・未検証です。CLI Extensionをチャット用パッケージとして扱いません。']})}

def path(lang,host=None):
    suffix='' if lang=='ar' else '.'+lang
    return ('docs/install-kumihan-ar-'+host if host else 'kumihan-ar')+suffix+'.html'
def link(url,label,attrs=''):
    return f'<a href="{e(url,quote=True)}" {attrs}>{e(label)}</a>'
def brand():return '<bdi dir="ltr">KUMIHAN｜نضيد</bdi>'
def files(host):
    if host=='chatgpt':return ['kumihan-ar-GPT-Codex-plugin-v0.1.0.zip']+[r+'-v0.1.0.zip' for r in ROLES]
    if host=='claude':return ['kumihan-ar-Claude-Code-plugin-v0.1.0.zip']+[r+'-Claude-skill-v0.1.0.zip' for r in ROLES]
    return ['kumihan-ar-Gemini-CLI-extension-v0.1.0.zip']+[r+'-Gemini-Apps-skill-v0.1.0.zip' for r in ROLES]
def published():
    return (ROOT/'_data/ar-release-published').exists()
def frame(lang,body,host=None):
    c=COPY[lang];name=path(lang,host)
    alternates=''.join(f'<link rel="alternate" hreflang="{l}" href="{PUBLIC+path(l,host)}">' for l in COPY)
    languages=''.join(link(BASE+path(l,host),label,f'lang="{l}" hreflang="{l}"'+(' aria-current="page"' if l==lang else '')) for l,label in [('ar','العربية'),('en','English'),('ja','日本語')])
    return f'''<!doctype html>
<html lang="{lang}" dir="{'rtl' if lang=='ar' else 'ltr'}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>KUMIHAN｜نضيد {e(c['guide'] if host else c['title'])}</title>
<meta name="description" content="{e(c['lead'],quote=True)}"><meta name="theme-color" content="#f5f3ee">
<link rel="canonical" href="{PUBLIC+name}">{alternates}<link rel="alternate" hreflang="x-default" href="{PUBLIC+path('ar',host)}">
<link rel="icon" href="{BASE}favicon.ico"><link rel="stylesheet" href="{BASE}assets/kumihan-install.css"><link rel="stylesheet" href="{BASE}assets/kumihan-ar.css">
</head><body><a class="skip-link" href="#main">{c['skip']}</a>
<header class="site-header"><div class="shell header-content"><a class="brand" href="{BASE+path(lang)}">{brand()}</a>
<nav class="header-nav" aria-label="{c['nav']}">{link(BASE,c['free'])}{link(BASE+path(lang)+'#skills',c['skills'])}{link(BASE+path(lang)+'#install',c['cta'])}</nav>
<nav class="language-switch" aria-label="{c['language']}">{languages}</nav></div></header>
<main id="main">{body}</main>
<footer class="footer"><div class="shell footer-layout"><div><p class="footer-mark">{brand()}</p><p class="footer-sub">{c['free']} · Apache-2.0<br>© 2026 <a href="https://www.landco.jp/" target="_blank" rel="noopener noreferrer">L&amp;Co. LLC</a></p></div><nav class="footer-links" aria-label="Footer">{link(BASE,'KUMIHAN')}{link(REPO,c['source'])}{link(REPO+'/blob/main/LICENSE','Apache-2.0')}{link(BASE+path(lang),c['back'])}</nav></div></footer></body></html>
'''
def landing(lang):
    c=COPY[lang]
    b=f'<section class="hero"><div class="shell hero-layout"><div class="hero-copy"><p class="eyebrow">{brand()} · <bdi dir="ltr">v0.1.0</bdi></p><h1>{c["title"]}</h1><p class="hero-desc">{c["lead"]}</p><div class="hero-cta">{link("#install",c["cta"],"class=\"button button-primary\"")}{link(REPO+"/tree/main/plugins/kumihan-ar",c["source"],"class=\"button\"")}</div><p class="hero-foot">Apache-2.0 · L&amp;Co. LLC</p></div><div class="hero-stage"><div class="logo-card"><img src="{BASE}assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png" alt="KUMIHAN" width="1024" height="1024"></div></div></div></section>'
    b+=f'<section class="intro-strip"><div class="shell intro-layout"><p class="section-number">01 / CONTEXT</p><div class="intro-text"><h2>{c["intro"]}</h2><p>{c["introtext"]}</p></div></div></section>'
    b+=f'<section class="features"><div class="shell"><div class="section-heading"><div><p class="section-number">02 / PRINCIPLES</p><h2>{c["features"]}</h2></div></div><div class="feature-grid">'
    for i,(title,text) in enumerate(c['principles'],1):b+=f'<article class="feature"><span class="feature-index">0{i}</span><h3>{title}</h3><p>{text}</p></article>'
    b+='</div></div></section>'
    b+=f'<section class="idea-band"><div class="shell idea-layout"><div><p class="eyebrow">KUMIHAN / DESIGN</p><h2>{c["idea"]}</h2><p>{c["ideatext"]}</p></div><div class="idea-art" aria-hidden="true"><span></span><span></span><span></span><span></span></div></div></section>'
    b+=f'<section class="skills-section" id="skills"><div class="shell"><div class="section-heading"><div><p class="section-number">03 / SKILLS</p><h2>{c["skills"]}</h2></div></div><div class="skills-grid">'
    for i,r in enumerate(ROLES):b+=f'<article class="skill-card"><p class="skill-type">0{i+1}</p><h3 class="skill-name"><bdi dir="ltr">{r}</bdi></h3><p class="skill-desc">{c["roles"][i]}</p>{link(REPO+"/tree/main/plugins/kumihan-ar/skills/"+r,c["source"],"class=\"skill-end\"")}</article>'
    b+='</div></div></section>'
    b+=f'<section class="install-section" id="install"><div class="shell install-layout"><div class="install-intro"><p class="section-number">04 / INSTALLATION</p><h2>{c["install"]}</h2><p>{c["installtext"]}</p></div><div class="install-links">'
    for i,(h,t) in enumerate(HOSTS.items(),1):b+=f'<a class="platform-row" href="{BASE+path(lang,h)}"><span class="platform-index">0{i}</span><span class="platform-info"><bdi dir="ltr" class="platform-name">{t}</bdi><span class="platform-note"> · {c["cta"]}</span></span><span class="platform-arrow" aria-hidden="true">→</span></a>'
    b+='</div></div></section>'
    b+=f'<section class="status-section"><div class="shell status-box"><div><h2 class="status-title">{c["status"]}</h2><p>{c["limit"]}</p></div><p class="status-meta">{c["available"] if published() else c["pending"]}<br><bdi dir="ltr">v0.1.0</bdi></p></div></section>'
    b+=f'<section class="cta-section"><div class="shell cta-layout"><div><h2>{c["cta"]}</h2><p>{c["installtext"]}</p></div>{link("#install",c["cta"],"class=\"button\"")}</div></section>'
    return frame(lang,b)
def guide(lang,host):
    c=COPY[lang]
    b=f'<div class="guide-hero"><div class="shell"><p class="eyebrow"><bdi dir="ltr">{HOSTS[host]} · v0.1.0</bdi></p><h1>{c["guide"]}</h1><p>{brand()}</p><nav class="host-nav" aria-label="Host">'+''.join(link(BASE+path(lang,h),t,'aria-current="page"' if h==host else '') for h,t in HOSTS.items())+'</nav></div></div>'
    b+=f'<div class="shell"><div class="guide-body"><section><h2>{c["steps"]}</h2><ol>'+''.join('<li>'+e(s)+'</li>' for s in c['notes'][host])+'</ol>'
    if host=='claude':b+='<pre><code>claude --plugin-dir /absolute/path/kumihan-ar</code></pre>'
    if host=='gemini':b+='<pre><code>gemini extensions install /absolute/path/kumihan-ar</code></pre>'
    docs={'chatgpt':[('https://developers.openai.com/codex/skills/','Codex Skills'),('https://developers.openai.com/codex/plugins/','Codex Plugins')],'claude':[('https://code.claude.com/docs/en/plugins','Claude Code plugins'),('https://support.claude.com/en/articles/12512180-using-skills-in-claude','Claude Skills')],'gemini':[('https://geminicli.com/docs/extensions/','Gemini CLI Extensions'),('https://geminicli.com/docs/cli/skills/','Gemini CLI Skills')]}[host]
    b+='<p>'+ ' · '.join(link(u,t) for u,t in docs)+'</p></section>'
    b+=f'<section><h2>{c["downloads"]}</h2><p>{c["available"] if published() else c["pending"]}</p>'
    for f in files(host):
        b+=link(RELEASE+f,f,'class="download-row"') if published() else '<p class="download-row">'+e(f)+'</p>'
    b+=f'<p>{c["verify"]}</p><pre><code>sha256sum --ignore-missing -c SHA256SUMS.txt</code></pre><p>'+(link(RELEASE+'SHA256SUMS.txt','SHA256SUMS.txt') if published() else 'SHA256SUMS.txt')+' · '+link(BASE+'plugins/kumihan-ar/downloads/MANIFEST.json','MANIFEST.json')+'</p></section>'
    b+=f'<section><h2>{c["invoke"]}</h2><blockquote>{c["prompt"]}</blockquote><p>{c["update"]}</p><p>{c["limit"]}</p></section><p>'+link(BASE+path(lang),c['back'])+'</p></div></div>'
    return frame(lang,b,host)
def outputs():return {path(l,h):guide(l,h) if h else landing(l) for l in COPY for h in (None,*HOSTS)}
def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args();out=outputs()
    changed=[n for n,s in out.items() if not (ROOT/n).exists() or (ROOT/n).read_text()!=s]
    if a.check:
        for n in changed:print('out of date: '+n)
        return int(bool(changed))
    for n in changed:(ROOT/n).write_text(out[n])
    print('Generated 12 Arabic product pages');return 0
if __name__=='__main__':raise SystemExit(main())
