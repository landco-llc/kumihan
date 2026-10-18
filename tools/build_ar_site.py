#!/usr/bin/env python3
"""Generate the 12 localized Arabic product pages; deterministic, no runtime translation."""
import argparse
from html import escape as e
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE='/kumihan/'
# KUMIHAN index in the page language; Arabic has no gateway yet, so it uses the Japanese index.
GATEWAY={'ar':'index.html','en':'top-en.html','ja':'index.html'}
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
# Landing copy follows the KUMIHAN index (kumihan.html) with Arabic-specific
# content kept (direction, mixed scripts, diacritics, Tatweel); see
# assets/ar-site-copy.json. Install-guide steps above stay product-specific.
import json
from importlib.util import module_from_spec, spec_from_file_location
def _load(name,file):
    spec=spec_from_file_location(name,Path(__file__).with_name(file));mod=module_from_spec(spec);spec.loader.exec_module(mod);return mod
SITE=_load('kumihan_product_site','product_site.py')
FRAME=_load('kumihan_install_frame','install_frame.py')
SITE_COPY=json.loads((ROOT/'assets/ar-site-copy.json').read_text(encoding='utf-8'))
LOGO='assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png'
LABELS=[('ar','العربية'),('en','English'),('ja','日本語')]
SYMBOLS=('ع','↗','¶','◎')
# kumihan-ar-web: semantic direction first; the canonical index CSS uses physical
# edges, so they are mirrored for dir="rtl". No letter-spacing on Arabic (it
# breaks cursive joining); fallback stacks only make Arabic glyphs available.
OVERRIDES=r"""
    html[lang="ar"] body { font-family: "Noto Naskh Arabic", "Noto Sans Arabic", "Geeza Pro", "Segoe UI", Tahoma, system-ui, sans-serif; line-height: 1.9; }
    html[lang="ar"] :is(h1, h2, h3, p, .eyebrow, .brand, .footer-mark, .skill-desc, .button, .feature-index, .section-number) { letter-spacing: 0; text-transform: none; }
    html[lang="ar"] .hero h1 { font-size: clamp(40px,4.8vw,68px); line-height: 1.55; }
    html[lang="ar"] :is(.intro-text h2, .section-heading h2, .idea-band h2, .install-intro h2, .cta-layout h2) { line-height: 1.7; }
    html[lang="ja"] body { line-break: strict; }
    html:is([lang="en"]) .hero h1 { font-size: clamp(40px,4.6vw,66px); letter-spacing: -.05em; line-height: 1.12; text-wrap: balance; }
    html[lang="en"] :is(h1, h2, h3, .eyebrow, .button, .feature p) { overflow-wrap: break-word; }
    .brand { min-width: 0; flex: 0 1 auto; }
    .brand > bdi { white-space: normal; }
    .language-switch a { display: inline-flex; align-items: center; justify-content: center; min-height: 38px; min-width: 38px; border-radius: 40px; color: var(--muted); padding: 7px 10px; font-size: 11px; font-weight: 800; letter-spacing: .02em; }
    .language-switch a[aria-current="page"] { background: var(--ink); color: white; }
    .language-switch a:hover:not([aria-current="page"]) { color: var(--red-dark); background: #ebe7df; }
    .hero-stage::after { content: "KUMIHAN / AR"; }
    .hero-foot, .header-content, .header-nav { flex-wrap: wrap; }
    .header-nav { min-width: 0; row-gap: 8px; }
    .hero-cta .button, .cta-layout .button { max-width: 100%; }
    .feature-motif { letter-spacing: 0 !important; }
    .skill-name, .platform-name { direction: ltr; text-align: start; }
    .status-meta { white-space: normal; }
    .status-meta a { color: var(--red-dark); }
    .skill-card, .platform-info, .status-box > *, .hero-copy, .hero-stage, .feature, .install-layout > *, .idea-layout > *, .card-top > *, .cta-layout > * { min-width: 0; }
    .feature-index, .skill-type { overflow-wrap: anywhere; }
    bdi { unicode-bidi: isolate; }
    /* Latin index labels such as "01 / TYPE" keep their reading order in RTL. */
    html[dir="rtl"] :is(.feature-index, .skill-type, .platform-index, .status-title) { direction: ltr; unicode-bidi: isolate; text-align: right; }
    html[dir="rtl"] .footer-links a { unicode-bidi: isolate; }
    html[dir="rtl"] .footer-sub { unicode-bidi: plaintext; text-align: right; }
    /* Right-to-left: mirror the canonical physical edges. */
    html[dir="rtl"] .header-nav { margin-left: 0; margin-right: auto; }
    html[dir="rtl"] .header-controls { margin-left: 0; margin-right: 16px; }
    html[dir="rtl"] .eyebrow .line { margin-right: 0; margin-left: 9px; }
    html[dir="rtl"] .arrow { margin-left: 0; margin-right: 12px; }
    html[dir="rtl"] :is(.arrow, .platform-arrow, .skill-end > span:last-child) { display: inline-block; transform: scaleX(-1); }
    html[dir="rtl"] .feature { padding: 32px 0 36px 24px; }
    html[dir="rtl"] .feature:not(:first-child) { padding-left: 24px; padding-right: 25px; border-left: 0; border-right: 1px solid var(--line); }
    html[dir="rtl"] .platform-row { padding: 20px 4px 20px 12px; }
    html[dir="rtl"] .platform-row:hover { padding-left: 12px; padding-right: 15px; }
    html[dir="rtl"] .status-meta { text-align: left; }
    html[dir="rtl"] .hero-stage::after { right: auto; left: -18px; }
    html[dir="rtl"] .stage-label { left: auto; right: 27px; }
    @media (max-width: 1080px) {
      html[dir="rtl"] .header-controls { margin-right: 0; }
      html[dir="rtl"] .feature { padding-left: 18px; }
      html[dir="rtl"] .feature:not(:first-child) { padding-right: 18px; }
    }
    @media (max-width: 790px) {
      .hero-layout, .intro-layout, .install-layout { grid-template-columns: minmax(0,1fr); }
      html[dir="rtl"] .header-nav { margin: 0; }
      html[dir="rtl"] .header-controls { margin-right: auto; margin-left: 0; }
      html[dir="rtl"] .feature:nth-child(3) { border-right: 0; padding-right: 0; }
      html[dir="rtl"] .hero-stage::after { left: 10px; right: auto; }
    }
    @media (max-width: 560px) {
      html[lang="ar"] .hero h1 { font-size: clamp(32px,8.6vw,44px); line-height: 1.6; }
      html[lang="en"] .hero h1 { font-size: clamp(33px,8.5vw,45px); }
      .header-nav { overflow: visible; gap: 12px 18px; }
      .header-nav a { white-space: normal; }
      .idea-layout { grid-template-columns: minmax(0,1fr); }
      html[dir="rtl"] .feature:not(:first-child) { padding-right: 14px; }
      html[dir="rtl"] .feature:nth-child(3) { padding-right: 0; }
      html[dir="rtl"] .status-meta { text-align: right; }
      html[dir="rtl"] .stage-label { right: 15px; }
    }
    /* Narrow phones: one principle per row instead of splitting Arabic words. */
    @media (max-width: 420px) {
      html[lang="ar"] .feature-grid { grid-template-columns: minmax(0,1fr); }
      html[lang="ar"] .feature, html[lang="ar"] .feature:not(:first-child), html[lang="ar"] .feature:nth-child(3) { padding: 22px 0; min-height: 0; border-right: 0; border-left: 0; border-bottom: 1px solid var(--line); }
      html[lang="ar"] .feature:last-child { border-bottom: 0; }
    }
"""
def head_links(lang,host=None):
    name=path(lang,host)
    alternates=''.join(f'<link rel="alternate" hreflang="{l}" href="{PUBLIC+path(l,host)}">' for l in COPY)
    return f'<link rel="canonical" href="{PUBLIC+name}">{alternates}<link rel="alternate" hreflang="x-default" href="{PUBLIC+path("ar",host)}">\n<link rel="icon" href="{BASE}favicon.ico">'
def landing(lang):
    c=dict(SITE_COPY[lang]);c['skills']=[[r,d] for r,(_,d) in zip(ROLES,c['skills'])]
    head=(f"<title>{e(c['title'])}</title>\n<meta name=\"description\" content=\"{e(c['description'],quote=True)}\">\n"
          f'<meta property="og:type" content="website"><meta property="og:title" content="{e(c["title"],quote=True)}"><meta property="og:url" content="{PUBLIC+path(lang)}"><meta property="og:image" content="{PUBLIC+LOGO}">\n'
          +head_links(lang)+f'\n<link rel="stylesheet" href="{BASE}assets/kumihan-ar.css">')
    return SITE.landing(dict(
        lang=lang,dir='rtl' if lang=='ar' else 'ltr',head=head,brand=brand(),home_label='KUMIHAN｜نضيد',
        languages=[(l,label,BASE+path(l),l==lang) for l,label in LABELS],
        logo=BASE+LOGO,repo=REPO,release=REPO+'/releases/tag/kumihan-ar-v0.1.0',license=REPO+'/blob/main/LICENSE',
        skills=[(r,REPO+'/tree/main/plugins/kumihan-ar/skills/'+r,SYMBOLS[i]) for i,r in enumerate(ROLES)],
        hosts=[('Claude / Claude Code' if h=='claude' else t,BASE+path(lang,h)) for h,t in HOSTS.items()],
        gateway=(BASE+GATEWAY[lang],c['gateway_label']),family=(c['family'][0],BASE+c['family'][1])),c)
def guide(lang,host):
    c=COPY[lang];s=SITE_COPY[lang];g=dict(s['guide'])
    title=f"{c['guide']} · {HOSTS[host]}"
    head=(f"<title>KUMIHAN｜نضيد — {e(title)}</title>\n<meta name=\"description\" content=\"{e(g['lead'],quote=True)}\">\n"+head_links(lang,host))
    b=f'<section id="steps"><h2>01 / {e(c["steps"])}</h2><ol>'+''.join('<li>'+e(x)+'</li>' for x in c['notes'][host])+'</ol>'
    if host=='claude':b+='<pre><code>claude --plugin-dir /absolute/path/kumihan-ar</code></pre>'
    if host=='gemini':b+='<pre><code>gemini extensions install /absolute/path/kumihan-ar</code></pre>'
    docs={'chatgpt':[('https://developers.openai.com/codex/skills/','Codex Skills'),('https://developers.openai.com/codex/plugins/','Codex Plugins')],'claude':[('https://code.claude.com/docs/en/plugins','Claude Code plugins'),('https://support.claude.com/en/articles/12512180-using-skills-in-claude','Claude Skills')],'gemini':[('https://geminicli.com/docs/extensions/','Gemini CLI Extensions'),('https://geminicli.com/docs/cli/skills/','Gemini CLI Skills')]}[host]
    b+='<p>'+' · '.join(link(u,t) for u,t in docs)+'</p></section>'
    b+=f'<section id="download"><h2>02 / {e(c["downloads"])}</h2><p>{e(c["available"] if published() else c["pending"])}</p><ul class="download-list">'
    for f in files(host):
        b+='<li>'+(link(RELEASE+f,f) if published() else e(f))+'</li>'
    b+=f'</ul><p>{e(c["verify"])}</p><pre><code>sha256sum --ignore-missing -c SHA256SUMS.txt</code></pre><p>'+(link(RELEASE+'SHA256SUMS.txt','SHA256SUMS.txt') if published() else 'SHA256SUMS.txt')+' · '+link(BASE+'plugins/kumihan-ar/downloads/MANIFEST.json','MANIFEST.json')+'</p></section>'
    b+=f'<section id="use"><h2>03 / {e(c["invoke"])}</h2><blockquote><p>{e(c["prompt"])}</p></blockquote><p>{e(c["update"])}</p><p class="note">{e(c["limit"])}</p></section>'
    g.update(skip=s['skip'],language=s['lang_label'],source_href=REPO+'/tree/main/plugins/kumihan-ar/INSTALL.md')
    return FRAME.render(FRAME.Frame(lang=lang,dir='rtl' if lang=='ar' else 'ltr',head=head,css=BASE+'assets/kumihan-install.css',asset_root=BASE,
        brand=brand(),home=BASE+path(lang),hosts=[(t,BASE+path(lang,h),h==host) for h,t in HOSTS.items()],
        languages=[(l,label,BASE+path(l,host),l==lang) for l,label in LABELS],number=f'0{list(HOSTS).index(host)+1}',
        title=e(title),description=e(g['lead']),toc=[('steps',c['steps']),('download',c['downloads']),('use',c['invoke'])],
        content=b,platform=HOSTS[host],ui=g,footer_sub=e(s['footer_sub'])+'<br>v0.1.0 · Apache-2.0 · Developed by L&amp;Co. LLC',
        footer_links=[('GitHub',REPO+'/tree/main/plugins/kumihan-ar',True),('Apache-2.0',REPO+'/blob/main/LICENSE',True)],
        gateway=(BASE+GATEWAY[lang],s['gateway_label'])))
def outputs():
    out={path(l,h):guide(l,h) if h else landing(l) for l in COPY for h in (None,*HOSTS)}
    out['assets/kumihan-ar.css']=SITE.canonical_css('KUMIHAN｜نضيد index: canonical KUMIHAN index CSS + Arabic RTL settings.',OVERRIDES)
    return out
def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args();out=outputs()
    changed=[n for n,s in out.items() if not (ROOT/n).exists() or (ROOT/n).read_text()!=s]
    if a.check:
        for n in changed:print('out of date: '+n)
        return int(bool(changed))
    for n in changed:(ROOT/n).write_text(out[n])
    print('Generated 12 Arabic product pages and kumihan-ar.css');return 0
if __name__=='__main__':raise SystemExit(main())
