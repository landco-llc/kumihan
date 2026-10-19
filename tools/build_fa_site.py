#!/usr/bin/env python3
"""Generate the 12 localized Arabic product pages; deterministic, no runtime translation."""
from seo_adapter import seo_outputs
from version_display import version_outputs
import argparse
from html import escape as e
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE='/kumihan/'
# KUMIHAN index (language gateway) for each page language.
GATEWAY={'fa':'top-fa.html','en':'index.html','ja':'top-ja.html'}
PUBLIC='https://landco-llc.github.io'+BASE
REPO='https://github.com/landco-llc/kumihan'
RELEASE=REPO+'/releases/download/kumihan-fa-v0.1.0/'
HOSTS={'chatgpt':'ChatGPT / Codex','claude':'Claude','gemini':'Gemini'}
ROLES=['kumihan-fa','kumihan-fa-web','kumihan-fa-documents','kumihan-fa-review']
COPY={
"fa": __import__("json").loads("{\"title\":\"وقتی حروف درست کنار هم می‌نشینند، معنا روشن می‌شود\",\"lead\":\"مهارت‌های متن‌باز برای طراحی وب‌سایت، سند و ارائهٔ فارسی. کار را از محتوا آغاز می‌کنیم، متن اصلی را نگه می‌داریم و بررسی فنی را از نمایش واقعی جدا می‌کنیم.\",\"skip\":\"رفتن به محتوای اصلی\",\"nav\":\"ناوبری اصلی\",\"language\":\"زبان\",\"intro\":\"حروف‌چینی با معنا آغاز می‌شود\",\"introtext\":\"جهت نوشتار بخشی از خواندن است. متن فارسی و بخش‌های لاتین را بدون وارونه‌کردن حروف یا دست‌کاری نام‌ها و اعداد، با توجه به بافت نمایش می‌دهیم.\",\"features\":\"چهار نکته برای خوانایی\",\"principles\":[[\"جهت روشن\",\"زبان، جهت بند و ترازبندی را جدا کنید؛ نشانی‌ها و شناسه‌های لاتین را در جای مناسب از متن جدا نگه دارید.\"],[\"حفظ متن اصلی\",\"نیم‌فاصله، ک و ی فارسی، نشانه‌ها، نام‌ها و قیمت‌ها را دقیقاً نگه دارید.\"],[\"طراحی متناسب\",\"ساختار، فاصله و قلم را با توجه به محتوا و مخاطب انتخاب کنید؛ نسخه‌ای ثابت برای همه وجود ندارد.\"],[\"بازبینی مستند\",\"بررسی متن، نمایش واقعی و داوری ویراستاری را از هم جدا ثبت کنید. نتیجهٔ بررسی‌نشده، تأییدشده نیست.\"]],\"idea\":\"فضای مناسب برای حروف و وضوح برای خواننده\",\"ideatext\":\"هر تیتر، بند و پیوند نقشی دارد. برای پرکردن فضای خالی، آرایهٔ بی‌دلیل اضافه نکنید و ترتیب نویسه‌ها را برای اصلاح ظاهر تغییر ندهید.\",\"skills\":\"چهار مهارت مستقل\",\"roles\":[\"مشخص‌کردن زبان، رسانه، هدف و محدودهٔ تغییر.\",\"طراحی وب و رابط، متن راست‌به‌چپ و بخش‌های چندزبانه.\",\"اسناد و ارائه‌ها همراه با بیان محدودیت‌های بررسی.\",\"بازبینی فقط‌خواندنی بدون تغییر فایل اصلی.\"],\"install\":\"از ابزاری که دارید شروع کنید\",\"installtext\":\"بستهٔ کامل ابزار خود یا یک مهارت مستقل را دریافت کنید. برای هر ابزار پنج بستهٔ کنترل‌شده ارائه می‌شود.\",\"cta\":\"شروع\",\"source\":\"مشاهدهٔ کد منبع\",\"status\":\"دامنهٔ بررسی\",\"limit\":\"این مهارت‌ها گواهی کیفیت حروف‌چینی نیستند. نصب و اجرا در ابزار مقصد جداگانه باید تأیید شود و متن فارسی برای انتشار نهایی به بازبینی انسانی نیاز دارد.\",\"pending\":\"نسخه هنوز در حال انتشار است\",\"available\":\"بسته‌های منتشرشده\",\"guide\":\"راهنمای نصب\",\"steps\":\"نصب بر پایهٔ ابزار\",\"downloads\":\"دریافت و تأیید فایل\",\"verify\":\"هر فایل ZIP را با SHA-256 منتشرشده تطبیق دهید. در صورت قرار دادن هر پنج فایل انتخابی در یک پوشه، با دستور زیر نتیجهٔ OK همهٔ آن‌ها را بررسی کنید. در macOS می‌توان از shasum -a 256 استفاده کرد.\",\"invoke\":\"استفاده و به‌روزرسانی\",\"prompt\":\"با استفاده از kumihan-fa-review این صفحه را بدون تغییر متن اصلی یا نام‌ها و عددها بازبینی کن. نتیجهٔ بررسی متن را از نمایش مشاهده‌شده جدا گزارش کن.\",\"update\":\"پیش از نصب دوباره، از تغییرات اختصاصی خود پشتیبان بگیرید و فایل جدید را بررسی کنید. فرستادن ZIP در گفت‌وگو به معنی نصب مهارت نیست.\",\"back\":\"بازگشت به صفحهٔ محصول\",\"free\":\"رایگان و متن‌باز\",\"notes\":{\"chatgpt\":[\"بررسی کنید که نسخهٔ ChatGPT یا Codex شما امکان واردکردن Plugin یا Skills را دارد.\",\"برای Codex، پوشهٔ یک مهارت مستقل را در مسیر .agents/skills/ پروژه استخراج کنید و نام مهارت را صدا بزنید.\",\"ارسال یک فایل ZIP در گفتگو با نصب واقعی یک پلاگین تفاوت دارد؛ از راهنمای رسمی ابزار خود پیروی کنید.\"],\"claude\":[\"در Claude Code بستهٔ کامل پلاگین را در یک پوشهٔ مستقل استخراج کنید.\",\"برای اجرای محلی از دستور زیر استفاده کنید. در Claude chat، مهارت مستقل را از رابط Skills و در صورت پشتیبانی وارد کنید.\",\"اجرای محلی به معنی انتشار در بازار رسمی نیست. بررسی فراخوانی در حساب واقعی هنوز انجام نشده است.\"],\"gemini\":[\"به Gemini CLI با پشتیبانی از Extensions نیاز دارید. بسته را استخراج کنید و وجود gemini-extension.json در ریشهٔ پوشه را بررسی کنید.\",\"پوشهٔ محلی را با دستور زیر نصب کنید و درخواست دسترسی را بررسی کنید.\",\"فایل‌های ZIP مهارت‌های مستقل جداگانه‌اند. بستهٔ CLI را به‌عنوان واردکردن مهارت در Gemini Apps تلقی نکنید.\"]}}"),
'en':dict(title='When letters fall into place, meaning comes through',lead='Open-source skills for Persian websites, documents and presentations. Start with the content and context, preserve the original text, and distinguish source checks from observed rendering.',skip='Skip to content',nav='Main navigation',language='Language',intro='Typography starts with meaning',introtext='Direction is part of reading. Handle Persian and mixed scripts in context without reversing characters or changing names and numbers to fit a layout.',features='Four priorities for readable text',principles=[('Clear direction','Distinguish language, paragraph direction and alignment. Isolate Latin links and identifiers where their context calls for it.'),('Source integrity','Preserve diacritics, intentional Tatweel, invisible controls, names and prices exactly as supplied.'),('Context-led design','Choose hierarchy, spacing and available typefaces for the content and audience. A fixed font recipe cannot replace that choice.'),('Evidence-based review','Separate static diagnostics, observed browser rendering and editorial judgment. Unchecked results remain unchecked.')],idea='Room for the text and clarity for the reader',ideatext='Every heading, paragraph and link serves the content. Do not add decoration to fill space or change Unicode order to repair display.',skills='Four independent skills',roles=['Set the language, medium, purpose and editing scope.','Websites, interfaces, direction and mixed scripts.','Documents, reports and slides with explicit verification limits.','Read-only review without modifying the original.'],install='Start with the tool you use',installtext='Choose your host bundle or a standalone skill. Each platform has five packages with file checksums.',cta='Get started',source='View the source',status='Verification limits',limit='These are assisted workflows, not typography certification. Native host installation and invocation are not checked. Persian copy needs native-speaker review.',pending='Release pending',available='Release packages',guide='Installation guide',steps='Install for your platform',downloads='Downloads and verification',verify='Compare SHA-256 with the published checksum file. With your five selected ZIPs in one directory, run the GNU command below and confirm that all five are reported OK. For a single ZIP, compare its hash with MANIFEST.json; on macOS use shasum -a 256 and compare the matching entry.',invoke='Use and update',prompt='Use kumihan-fa-review to review this page without changing source text, names or numbers. Separate static findings from rendering you actually observed.',update='Back up customizations and verify the new version before reinstalling. Attaching a file to chat does not establish skill installation.',back='Back to the product',free='Free and open source',notes={
'chatgpt':['Check that your account and client offer a plugin or Skills installation interface. Availability differs between ChatGPT and Codex.','For Codex, extract an individual skill folder into your project’s .agents/skills/, then request the skill by name. Consult your client’s documentation for plugin installation.','In ChatGPT, use the actual import interface if available. Otherwise read SKILL.md as manual guidance; that is not plugin installation.'],
'claude':['For Claude Code, extract the full plugin into its own directory.','Start a local session with the command below. For Claude chat, use an individual skill ZIP through the Skills interface where available.','Local loading does not establish official marketplace listing. Discovery and invocation on a real account remain not checked.'],
'gemini':['Use Gemini CLI with Extensions support. Extract the archive and locate gemini-extension.json at the folder root.','Install the local folder with the command below and review the permission prompt.','Individual skill archives are separate. Gemini Apps import is manual and unverified; a CLI extension is not a chat-app import package.']}),
'ja':dict(title='文字が整うと意味が伝わる',lead='ペルシア語のWebサイト・文書・プレゼンテーションを制作するための、オープンソースのスキル集です。内容と目的から設計し、原文を守り、静的検査と実際の表示を分けて確認します。',skip='本文へ移動',nav='メインナビゲーション',language='言語',intro='文字組は意味から考える',introtext='文章の方向は、読みやすさの一部です。ペルシア語と欧文が混在する場面を捉え、文字の逆転や、枠に合わせた名前・数値の書き換えを避けます。',features='読みやすさを支える4つの観点',principles=[('文章の方向','言語・段落方向・右揃えを区別し、URLや製品コードは文脈に応じて分離します。'),('原文の保全','母音記号、意図的な伸ばし、不可視文字、姓名、価格を元の文字列のまま保持します。'),('目的に合う設計','内容と読者に合わせて情報の順序・余白・利用可能な書体を選びます。固定の書体を押し付けません。'),('根拠のあるレビュー','静的検査・ブラウザでの実表示・編集上の判断を分け、未確認を合格にしません。')],idea='文字のための余白を読む人のための明快さを',ideatext='見出し・段落・リンクには、それぞれ役割があります。空間を埋めるための装飾や、表示のためのUnicode順序の変更は行いません。',skills='作業に合わせて選ぶ4つのスキル',roles=['言語・媒体・目的・変更範囲を定める。','Webサイト・UI・文章方向・多言語混植を扱う。','文書・レポート・スライドと検証の限界を扱う。','原本を変更しない、読み取り専用のレビュー。'],install='いつものAIツールからはじめよう',installtext='ホスト別の一式、または独立したスキルを選べます。各ホスト5パッケージと、ファイル照合用のハッシュを用意しています。',cta='導入方法を見る',source='ソースコードを見る',status='検証範囲について',limit='制作を支援する指針であり、文字組の品質認証ではありません。各ホストでのインストール・呼び出しは未確認です。ペルシア語のコピーは母語話者による校閲が必要です。',pending='Release公開準備中',available='Release配布物',guide='導入ガイド',steps='ホストに合わせて導入する',downloads='ダウンロードと照合',verify='公開されたチェックサムとSHA-256を照合します。選んだ5 ZIPを同じフォルダに置き、次のGNUコマンドで5件すべてのOKを確認します。単体ZIPやmacOSではshasum -a 256の結果をMANIFEST.jsonの該当項目と照合します。',invoke='使い方と更新',prompt='kumihan-fa-reviewを使い、原文・名前・数値を変更せずにこのページをレビューしてください。静的な指摘と、実際に確認した表示を分けてください。',update='カスタマイズを保存し、新版を照合してから再インストールします。チャットへの添付だけでは、スキルのインストールを確認したことにはなりません。',back='製品ページに戻る',free='無料のオープンソース',notes={
'chatgpt':['アカウントとクライアントにPluginまたはSkillsの導入画面があるか確認します。ChatGPTとCodexでは利用条件が異なります。','Codexでは独立スキルのフォルダをプロジェクトの.agents/skills/に展開し、名前を指定して使用を依頼します。Plugin一式の導入は利用中のクライアントの公式手順に従います。','ChatGPTでは実際のインポート画面を使います。画面がなければSKILL.mdを手動の指針として読みます。これはPluginのインストールとは区別します。'],
'claude':['Claude CodeではPlugin一式を独立したフォルダに展開します。','次のコマンドでローカルセッションを開始します。Claude chatでは、利用可能なSkills画面から独立スキルZIPを取り込みます。','ローカルでの読み込みと公式マーケットへの掲載は別です。実アカウントでの検出・呼び出しは未確認です。'],
'gemini':['Extensionsに対応するGemini CLIを使います。展開先のルートにgemini-extension.jsonがあることを確認します。','次のコマンドでローカルフォルダを導入し、権限の確認画面を読みます。','独立スキルZIPは別の配布形式です。Gemini Appsへの取り込みは手動・未検証です。CLI Extensionをチャット用パッケージとして扱いません。']})}

def path(lang,host=None):
    suffix='' if lang=='fa' else '.'+lang
    return ('docs/install-kumihan-fa-'+host if host else 'kumihan-fa')+suffix+'.html'
def link(url,label,attrs=''):
    return f'<a href="{e(url,quote=True)}" {attrs}>{e(label)}</a>'
def brand():return '<span dir="ltr">KUMIHAN｜</span><bdi lang="fa" dir="rtl">تراز</bdi>'
def files(host):
    if host=='chatgpt':return ['kumihan-fa-GPT-Codex-plugin-v0.1.0.zip']+[r+'-v0.1.0.zip' for r in ROLES]
    if host=='claude':return ['kumihan-fa-Claude-Code-plugin-v0.1.0.zip']+[r+'-Claude-skill-v0.1.0.zip' for r in ROLES]
    return ['kumihan-fa-Gemini-CLI-extension-v0.1.0.zip']+[r+'-Gemini-Apps-skill-v0.1.0.zip' for r in ROLES]
def published():
    return (ROOT/'_data/fa-release-published').exists()
# Landing copy follows the KUMIHAN index (kumihan.html) with Persian-specific
# content kept (RTL direction, mixed scripts, ZWNJ, Persian Kaf and Yeh); see
# assets/fa-site-copy.json. Install-guide steps above stay product-specific.
import json
from importlib.util import module_from_spec, spec_from_file_location
def _load(name,file):
    spec=spec_from_file_location(name,Path(__file__).with_name(file));mod=module_from_spec(spec);spec.loader.exec_module(mod);return mod
SITE=_load('kumihan_product_site','product_site.py')
FRAME=_load('kumihan_install_frame','install_frame.py')
SITE_COPY=json.loads((ROOT/'assets/fa-site-copy.json').read_text(encoding='utf-8'))
LOGO='assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png'
LABELS=[('fa','فارسی'),('en','English'),('ja','日本語')]
SYMBOLS=('ت','↗','¶','◎')
# kumihan-fa-web: semantic direction first; the canonical index CSS uses physical
# edges, so they are mirrored for dir="rtl". No letter-spacing on Arabic (it
# breaks cursive joining); fallback stacks only make Arabic glyphs available.
OVERRIDES=r"""
    html[lang="fa"] { --display: "Vazirmatn", "Noto Naskh Arabic", Tahoma, sans-serif; --sans: "Vazirmatn", "Noto Naskh Arabic", Tahoma, sans-serif; --font-jp: "Vazirmatn", "Noto Naskh Arabic", Tahoma, sans-serif; }
    html[lang="fa"] body { font-family: "Vazirmatn", "Noto Naskh Arabic", "Noto Sans Arabic", "Geeza Pro", "Segoe UI", Tahoma, system-ui, sans-serif; line-height: 1.9; }
    html[lang="fa"] :is(h1, h2, h3, p, .eyebrow, .brand, .footer-mark, .skill-desc, .button, .feature-index, .section-number) { letter-spacing: 0; text-transform: none; }
    html[lang="fa"] .hero h1 { font-size: clamp(40px,4.8vw,68px); line-height: 1.55; }
    html[lang="fa"] :is(.intro-text h2, .section-heading h2, .idea-band h2, .install-intro h2, .cta-layout h2) { line-height: 1.7; }
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
      html[lang="fa"] .hero h1 { font-size: clamp(32px,8.6vw,44px); line-height: 1.6; }
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
      html[lang="fa"] .feature-grid { grid-template-columns: minmax(0,1fr); }
      html[lang="fa"] .feature, html[lang="fa"] .feature:not(:first-child), html[lang="fa"] .feature:nth-child(3) { padding: 22px 0; min-height: 0; border-right: 0; border-left: 0; border-bottom: 1px solid var(--line); }
      html[lang="fa"] .feature:last-child { border-bottom: 0; }
    }
"""
def head_links(lang,host=None):
    name=path(lang,host)
    alternates=''.join(f'<link rel="alternate" hreflang="{l}" href="{PUBLIC+path(l,host)}">' for l in COPY)
    return f'<link rel="canonical" href="{PUBLIC+name}">{alternates}<link rel="alternate" hreflang="x-default" href="{PUBLIC+path("fa",host)}">\n<link rel="icon" href="{BASE}favicon.ico">'
def landing(lang):
    c=dict(SITE_COPY[lang]);c['skills']=[[r,d] for r,(_,d) in zip(ROLES,c['skills'])]
    head=(f"<title>{e(c['title'])}</title>\n<meta name=\"description\" content=\"{e(c['description'],quote=True)}\">\n"
          f'<meta property="og:type" content="website"><meta property="og:title" content="{e(c["title"],quote=True)}"><meta property="og:url" content="{PUBLIC+path(lang)}"><meta property="og:image" content="{PUBLIC+LOGO}">\n'
          +head_links(lang)+f'\n<link rel="stylesheet" href="{BASE}assets/kumihan-fa.css">')
    return SITE.landing(dict(
        lang=lang,dir='rtl' if lang=='fa' else 'ltr',head=head,brand=brand(),home_label='KUMIHAN｜تراز',
        languages=[(l,label,BASE+path(l),l==lang) for l,label in LABELS],
        logo=BASE+LOGO,repo=REPO,release=REPO+'/releases/tag/kumihan-fa-v0.1.0',license=REPO+'/blob/main/LICENSE',
        skills=[(r,REPO+'/tree/main/plugins/kumihan-fa/skills/'+r,SYMBOLS[i]) for i,r in enumerate(ROLES)],
        hosts=[('Claude / Claude Code' if h=='claude' else t,BASE+path(lang,h)) for h,t in HOSTS.items()],
        gateway=(BASE+GATEWAY[lang],c['gateway_label']),family=(c['family'][0],BASE+c['family'][1])),c)
def guide(lang,host):
    c=COPY[lang];s=SITE_COPY[lang];g=dict(s['guide'])
    title=f"{c['guide']} · {HOSTS[host]}"
    head=(f"<title>KUMIHAN｜تراز — {e(title)}</title>\n<meta name=\"description\" content=\"{e(g['lead'],quote=True)}\">\n"+head_links(lang,host))
    if lang=='fa':
        head += ('<style>html[lang="fa"] { --sans:"Vazirmatn","Noto Naskh Arabic",Tahoma,sans-serif;'
          ' --display:"Vazirmatn","Noto Naskh Arabic",Tahoma,sans-serif;'
          ' --font-jp:"Vazirmatn","Noto Naskh Arabic",Tahoma,sans-serif; }'
          'html[lang="fa"] body { font-family:"Vazirmatn","Noto Naskh Arabic",Tahoma,sans-serif;line-height:1.85; }'
          'html[lang="fa"] :is(h1,h2,h3,p,li,.nav-item,.button){letter-spacing:normal;}</style>')
    b=f'<section id="steps"><h2>01 / {e(c["steps"])}</h2><ol>'+''.join('<li>'+e(x)+'</li>' for x in c['notes'][host])+'</ol>'
    if host=='claude':b+='<pre><code>claude --plugin-dir /absolute/path/kumihan-fa</code></pre>'
    if host=='gemini':b+='<pre><code>gemini extensions install /absolute/path/kumihan-fa</code></pre>'
    docs={'chatgpt':[('https://developers.openai.com/codex/skills/','Codex Skills'),('https://developers.openai.com/codex/plugins/','Codex Plugins')],'claude':[('https://code.claude.com/docs/en/plugins','Claude Code plugins'),('https://support.claude.com/en/articles/12512180-using-skills-in-claude','Claude Skills')],'gemini':[('https://geminicli.com/docs/extensions/','Gemini CLI Extensions'),('https://geminicli.com/docs/cli/skills/','Gemini CLI Skills')]}[host]
    b+='<p>'+' · '.join(link(u,t) for u,t in docs)+'</p></section>'
    b+=f'<section id="download"><h2>02 / {e(c["downloads"])}</h2><p>{e(c["available"] if published() else c["pending"])}</p><ul class="download-list">'
    for f in files(host):
        b+='<li>'+(link(RELEASE+f,f) if published() else e(f))+'</li>'
    b+=f'</ul><p>{e(c["verify"])}</p><pre><code>sha256sum --ignore-missing -c SHA256SUMS.txt</code></pre><p>'+(link(RELEASE+'SHA256SUMS.txt','SHA256SUMS.txt') if published() else 'SHA256SUMS.txt')+' · '+link(BASE+'plugins/kumihan-fa/downloads/MANIFEST.json','MANIFEST.json')+'</p></section>'
    b+=f'<section id="use"><h2>03 / {e(c["invoke"])}</h2><blockquote><p>{e(c["prompt"])}</p></blockquote><p>{e(c["update"])}</p><p class="note">{e(c["limit"])}</p></section>'
    g.update(skip=s['skip'],language=s['lang_label'],source_href=REPO+'/tree/main/plugins/kumihan-fa/INSTALL.md')
    return FRAME.render(FRAME.Frame(lang=lang,dir='rtl' if lang=='fa' else 'ltr',head=head,css=BASE+'assets/kumihan-install.css',asset_root=BASE,
        brand=brand(),home=BASE+path(lang),hosts=[(t,BASE+path(lang,h),h==host) for h,t in HOSTS.items()],
        languages=[(l,label,BASE+path(l,host),l==lang) for l,label in LABELS],number=f'0{list(HOSTS).index(host)+1}',
        title=e(title),description=e(g['lead']),toc=[('steps',c['steps']),('download',c['downloads']),('use',c['invoke'])],
        content=b,platform=HOSTS[host],ui=g,footer_sub=e(s['footer_sub'])+'<br>v0.1.0 · Apache-2.0 · Developed by L&amp;Co. LLC',
        footer_links=[('GitHub',REPO+'/tree/main/plugins/kumihan-fa',True),('Apache-2.0',REPO+'/blob/main/LICENSE',True)],
        gateway=(BASE+GATEWAY[lang],s['gateway_label'])))
@version_outputs
@seo_outputs
def outputs():
    out={path(l,h):guide(l,h) if h else landing(l) for l in COPY for h in (None,*HOSTS)}
    out['assets/kumihan-fa.css']=SITE.canonical_css('KUMIHAN｜تراز index: canonical KUMIHAN index CSS + Arabic RTL settings.',OVERRIDES)
    return out
def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args();out=outputs()
    changed=[n for n,s in out.items() if not (ROOT/n).exists() or (ROOT/n).read_text()!=s]
    if a.check:
        for n in changed:print('out of date: '+n)
        return int(bool(changed))
    for n in changed:(ROOT/n).write_text(out[n])
    print('Generated 12 Arabic product pages and kumihan-fa.css');return 0
if __name__=='__main__':raise SystemExit(main())
