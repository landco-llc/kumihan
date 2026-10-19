#!/usr/bin/env node
// Generated with product-specific KUMIHAN｜Nhịp Chữ skills after standalone Skills were completed.
// No external dependencies. --check is non-writing; otherwise regenerate all twelve HTML files.
import {readFileSync,writeFileSync} from "node:fs";
// KUMIHAN index (language gateway) for each page language.
const GATEWAY={vi:"top-vi.html",en:"index.html",ja:"top-ja.html"};
// Typefaces per page language: same links as tools/web_fonts.py (tests/test_web_fonts.py checks them).
const GOOGLE_FONTS={"vi": "<link rel=\"preconnect\" href=\"https://fonts.googleapis.com\"><link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin><link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&amp;family=Noto+Serif:wght@100..900&amp;display=swap\"><link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/css2?family=Noto+Sans+JP&amp;family=Noto+Sans+KR&amp;family=Noto+Sans+SC&amp;family=Noto+Sans+TC&amp;family=Noto+Sans+Thai&amp;family=Noto+Naskh+Arabic&amp;family=Noto+Sans+Devanagari&amp;family=Noto+Sans+Bengali&amp;family=Noto+Sans+Khmer&amp;family=Vazirmatn&amp;text=-%D8%A7%D8%A8%D8%A9%D8%AA%D8%AF%D8%B1%D8%B2%D8%B3%D8%B6%D8%B9%D9%81%D9%84%D9%86%D9%8A%DB%8C%E0%A4%82%E0%A4%85%E0%A4%95%E0%A4%97%E0%A4%A4%E0%A4%A6%E0%A4%B0%E0%A4%B7%E0%A4%B8%E0%A4%B9%E0%A4%BF%E0%A5%80%E0%A5%8D%E0%A6%82%E0%A6%85%E0%A6%95%E0%A6%9C%E0%A6%AC%E0%A6%B0%E0%A6%B2%E0%A6%B7%E0%A6%B8%E0%A6%BE%E0%A7%8D%E0%B8%81%E0%B8%94%E0%B8%97%E0%B8%A2%E0%B8%A3%E0%B8%A5%E0%B8%A9%E0%B8%AD%E0%B8%B1%E0%B8%B8%E0%B9%84%E1%9E%80%E1%9E%81%E1%9E%84%E1%9E%93%E1%9E%97%E1%9E%98%E1%9E%9A%E1%9E%9B%E1%9E%9F%E1%9E%B6%E1%9E%B9%E1%9F%82%E1%9F%86%E1%9F%92%E3%81%82%E4%B8%AD%E4%BD%93%E5%8F%B0%E5%AD%97%E5%BE%8B%E6%96%87%E6%97%A5%E6%9C%AC%E6%B1%89%E6%B8%AF%E6%BC%A2%E7%81%A3%E7%AE%80%E7%B9%81%E8%87%BA%E8%A1%A1%E8%AA%9E%E9%A6%99%E9%AB%94%EA%B5%AD%EA%B8%80%EC%96%B4%EC%9E%84%EC%A7%9C%ED%95%9C&amp;display=swap\">", "en": "<link rel=\"preconnect\" href=\"https://fonts.googleapis.com\"><link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin><link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/css2?family=Inter:wght@100..900&amp;family=Source+Serif+4:wght@200..900&amp;display=swap\"><link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/css2?family=Noto+Sans+JP&amp;family=Noto+Sans+KR&amp;family=Noto+Sans+SC&amp;family=Noto+Sans+TC&amp;family=Noto+Sans+Thai&amp;family=Noto+Naskh+Arabic&amp;family=Noto+Sans+Devanagari&amp;family=Noto+Sans+Bengali&amp;family=Noto+Sans+Khmer&amp;family=Vazirmatn&amp;text=-%D8%A7%D8%A8%D8%A9%D8%AA%D8%AF%D8%B1%D8%B2%D8%B3%D8%B6%D8%B9%D9%81%D9%84%D9%86%D9%8A%DB%8C%E0%A4%82%E0%A4%85%E0%A4%95%E0%A4%97%E0%A4%A4%E0%A4%A6%E0%A4%B0%E0%A4%B7%E0%A4%B8%E0%A4%B9%E0%A4%BF%E0%A5%80%E0%A5%8D%E0%A6%82%E0%A6%85%E0%A6%95%E0%A6%9C%E0%A6%AC%E0%A6%B0%E0%A6%B2%E0%A6%B7%E0%A6%B8%E0%A6%BE%E0%A7%8D%E0%B8%81%E0%B8%94%E0%B8%97%E0%B8%A2%E0%B8%A3%E0%B8%A5%E0%B8%A9%E0%B8%AD%E0%B8%B1%E0%B8%B8%E0%B9%84%E1%9E%80%E1%9E%81%E1%9E%84%E1%9E%93%E1%9E%97%E1%9E%98%E1%9E%9A%E1%9E%9B%E1%9E%9F%E1%9E%B6%E1%9E%B9%E1%9F%82%E1%9F%86%E1%9F%92%E3%81%82%E4%B8%AD%E4%BD%93%E5%8F%B0%E5%AD%97%E5%BE%8B%E6%96%87%E6%97%A5%E6%9C%AC%E6%B1%89%E6%B8%AF%E6%BC%A2%E7%81%A3%E7%AE%80%E7%B9%81%E8%87%BA%E8%A1%A1%E8%AA%9E%E9%A6%99%E9%AB%94%EA%B5%AD%EA%B8%80%EC%96%B4%EC%9E%84%EC%A7%9C%ED%95%9C&amp;display=swap\">", "ja": "<link rel=\"preconnect\" href=\"https://fonts.googleapis.com\"><link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin><link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@100..900&amp;family=Noto+Serif+JP:wght@200..900&amp;display=swap\"><link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/css2?family=Noto+Sans+KR&amp;family=Noto+Sans+SC&amp;family=Noto+Sans+TC&amp;family=Noto+Sans+Thai&amp;family=Noto+Naskh+Arabic&amp;family=Noto+Sans+Devanagari&amp;family=Noto+Sans+Bengali&amp;family=Noto+Sans+Khmer&amp;family=Vazirmatn&amp;text=-%D8%A7%D8%A8%D8%A9%D8%AA%D8%AF%D8%B1%D8%B2%D8%B3%D8%B6%D8%B9%D9%81%D9%84%D9%86%D9%8A%DB%8C%E0%A4%82%E0%A4%85%E0%A4%95%E0%A4%97%E0%A4%A4%E0%A4%A6%E0%A4%B0%E0%A4%B7%E0%A4%B8%E0%A4%B9%E0%A4%BF%E0%A5%80%E0%A5%8D%E0%A6%82%E0%A6%85%E0%A6%95%E0%A6%9C%E0%A6%AC%E0%A6%B0%E0%A6%B2%E0%A6%B7%E0%A6%B8%E0%A6%BE%E0%A7%8D%E0%B8%81%E0%B8%94%E0%B8%97%E0%B8%A2%E0%B8%A3%E0%B8%A5%E0%B8%A9%E0%B8%AD%E0%B8%B1%E0%B8%B8%E0%B9%84%E1%9E%80%E1%9E%81%E1%9E%84%E1%9E%93%E1%9E%97%E1%9E%98%E1%9E%9A%E1%9E%9B%E1%9E%9F%E1%9E%B6%E1%9E%B9%E1%9F%82%E1%9F%86%E1%9F%92%E3%81%82%E4%B8%AD%E4%BD%93%E5%8F%B0%E5%AD%97%E5%BE%8B%E6%96%87%E6%97%A5%E6%9C%AC%E6%B1%89%E6%B8%AF%E6%BC%A2%E7%81%A3%E7%AE%80%E7%B9%81%E8%87%BA%E8%A1%A1%E8%AA%9E%E9%A6%99%E9%AB%94%EA%B5%AD%EA%B8%80%EC%96%B4%EC%9E%84%EC%A7%9C%ED%95%9C&amp;display=swap\">"};
const ASSETS=JSON.parse(readFileSync(new URL("../_data/kumihan_assets.json", import.meta.url),"utf8"));
const fonts=(lang,root)=>`${GOOGLE_FONTS[lang]}<link rel="stylesheet" href="${root}${ASSETS.fonts_css}">`;
import {resolve} from "node:path";
const META={"id":"kumihan-nhip-chu","display":"KUMIHAN｜Nhịp Chữ","version":"0.1.0","repo":"https://github.com/landco-llc/kumihan","base":"https://landco-llc.github.io/kumihan/","release":"https://github.com/landco-llc/kumihan/releases/tag/kumihan-vi-v0.1.0","download":"https://github.com/landco-llc/kumihan/releases/download/kumihan-vi-v0.1.0/","logo":"KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png"};
// The footer every KUMIHAN page shares (tools/site_footer.py, written by tools/web_fonts.py).
const FOOTERS=JSON.parse(readFileSync(new URL("../_data/site_footer.json", import.meta.url),"utf8"));
const footer=(lang,root)=>FOOTERS[lang].replaceAll("@ROOT@",root);
// Link-preview tags every KUMIHAN page shares: the same as apply() in tools/site_share.py
// (data written by tools/web_fonts.py; tests/test_site_share.py checks the pages).
const SHARE=JSON.parse(readFileSync(new URL("../_data/site_share.json", import.meta.url),"utf8"));
const SHARE_IMAGE=META.base+"assets/kumihan-share.png";
const unescapeHtml=s=>s.replace(/&(#x[0-9a-f]+|#\d+|amp|lt|gt|quot|apos);/gi,(m,c)=>c[0]==="#"
 ?String.fromCodePoint(c[1].toLowerCase()==="x"?parseInt(c.slice(2),16):Number(c.slice(1)))
 :{amp:"&",lt:"<",gt:">",quot:'"',apos:"'"}[c.toLowerCase()]);
const escapeHtml=s=>s.replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;").replaceAll('"',"&quot;").replaceAll("'","&#x27;");
function share(html){
 const lang=html.match(/<html\b[^>]*\slang="([^"]+)"/)[1],{about,separator,locale}=SHARE[lang];
 const title=escapeHtml(unescapeHtml(html.match(/<title>([\s\S]*?)<\/title>/)[1].trim()));
 const meta=html.match(/<meta\b(?=[^>]*\sname="description")[^>]*\scontent="([^"]*)"/),page=meta?unescapeHtml(meta[1]):"";
 const desc=escapeHtml(page.includes(about)?page:(about+separator+page).trim());
 const url=escapeHtml(unescapeHtml(html.match(/<link\b(?=[^>]*\srel="canonical")[^>]*\shref="([^"]*)"/)[1]));
 const tags=['<meta property="og:type" content="website">','<meta property="og:site_name" content="KUMIHAN">',
  `<meta property="og:title" content="${title}">`,`<meta property="og:description" content="${desc}">`,
  `<meta property="og:url" content="${url}">`,`<meta property="og:locale" content="${locale}">`,
  `<meta property="og:image" content="${SHARE_IMAGE}">`,'<meta property="og:image:width" content="1200">',
  '<meta property="og:image:height" content="630">','<meta property="og:image:alt" content="KUMIHAN">',
  '<meta name="twitter:card" content="summary_large_image">',`<meta name="twitter:title" content="${title}">`,
  `<meta name="twitter:description" content="${desc}">`,`<meta name="twitter:image" content="${SHARE_IMAGE}">`];
 html=html.replace(/[ \t]*<meta\b(?:\s+[\w:-]+="[^"]*")*\s*\/?>\n?/g,t=>/\s(?:property="og:|name="twitter:)/.test(t)?"":t);
 return html.replace("</head>",tags.join("\n")+"\n</head>");
}
const DATA=JSON.parse(readFileSync(new URL("../assets/nhip-chu-site-copy.json", import.meta.url),"utf8"));
function e(s){return String(s).replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;").replaceAll('"',"&quot;").replaceAll("'","&#39;")}
function pageName(lang){return "kumihan-vi"+(lang==="vi"?"":"."+lang)+".html";}
function guideName(host,lang){return "install-nhip-chu-"+host+(lang==="vi"?"":"."+lang)+".html";}
function hostZip(host){return META.id+"-"+({chatgpt:"chatgpt-codex-plugin",claude:"claude-code-plugin",gemini:"gemini-cli-extension"})[host]+"-v"+META.version+".zip";}
function skillZip(host,suffix){return META.id+suffix+"-"+host+"-skill-v"+META.version+".zip";}
function hostLabel(host){return {chatgpt:"ChatGPT / Codex",claude:"Claude / Claude Code",gemini:"Gemini"}[host];}
function altLinks(guide,host){return ["vi","en","ja"].map(lang=>'<link rel="alternate" hreflang="'+lang+'" href="'+e(META.base+(guide?"docs/"+guideName(host,lang):pageName(lang)))+'">').join("\n");}
function renderLanding(lang){
 const c=DATA[lang],file=pageName(lang),ls={vi:"VI",en:"EN",ja:"日本語"};
 const links=["vi","en","ja"].map(l=>`<a href="${pageName(l)}" lang="${l}" hreflang="${l}"${l===lang?' aria-current="page"':""}>${ls[l]}</a>`).join("");
 const feature=c.features.map(f=>`<article class="feature"><span class="feature-index">${e(f[0])}</span><div class="feature-motif" aria-hidden="true">${e(f[1])}</div><h3>${e(f[2])}</h3><p>${e(f[3])}</p></article>`).join("\n");
 const skills=["","-web","-documents","-review"].map((s,i)=>`<article class="skill-card"><div class="card-top"><span class="skill-type">0${i+1} / ${["ENTRY","WEB","DOCUMENTS","REVIEW"][i]}</span><span class="skill-symbol" aria-hidden="true">${["◎","↗","¶","◌"][i]}</span></div><h3 class="skill-name">${e(c.skills[i][0])}</h3><p class="skill-desc">${e(c.skills[i][1])}</p><a class="skill-end" href="${META.repo}/blob/main/plugins/${META.id}/skills/${META.id}${s}/SKILL.md">${e(c.view)} ↗</a></article>`).join("\n");
 const hosts=["chatgpt","claude","gemini"].map((h,i)=>`<a class="platform-row" href="docs/${guideName(h,lang)}"><span class="platform-index">0${i+1}</span><div class="platform-info"><div class="platform-name"><bdi dir="ltr">${e(hostLabel(h))}</bdi></div><div class="platform-note">${e(c.installNotes[i])}</div></div><span class="platform-arrow" aria-hidden="true">↗</span></a>`).join("");
 return `<!doctype html>
<html lang="${lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#f5f3ee">
<meta name="description" content="${e(c.description)}">
<title>${e(c.title)}</title>
<link rel="canonical" href="${META.base+file}">
${altLinks(false)}
<link rel="alternate" hreflang="x-default" href="${META.base}kumihan-vi.html">
<link rel="icon" type="image/png" href="assets/favicon-32x32.png">
<link rel="stylesheet" href="assets/nhip-chu-site.css">
${fonts(lang,"")}
</head>
<body id="top">
<a class="skip-link" href="#main">${e(c.skip)}</a>
<header class="site-header"><div class="shell header-content">
<a class="brand" href="#top" aria-label="${e(META.display)}"><span>KUMIHAN<span class="brand-sub">｜Nhịp Chữ</span></span></a>
<nav class="header-nav" aria-label="${e(c.navLabel)}"><a href="#concept">${e(c.nav[0])}</a><a href="#features">${e(c.nav[1])}</a><a href="#skills">${e(c.nav[2])}</a><a href="#install">${e(c.nav[3])}</a></nav>
<div class="header-controls"><nav class="language-switch" aria-label="${e(c.language)}">${links}</nav></div>
</div></header>
<main id="main" tabindex="-1">
<section class="hero" aria-labelledby="hero-title"><div class="shell hero-layout">
<div class="hero-copy"><p class="eyebrow"><span class="line" aria-hidden="true"></span> ${e(c.eyebrow)}</p>
<h1 id="hero-title">${c.h1.slice(0,-1).map(e).join("<br>")}<br><span class="accent">${e(c.h1.at(-1))}</span></h1>
<p class="hero-desc">${e(c.lead)}</p>
<div class="hero-cta"><a class="button button-primary" href="#install">${e(c.cta[0])}<span class="arrow" aria-hidden="true">↗</span></a><a class="button" href="#concept">${e(c.cta[1])}<span class="arrow" aria-hidden="true">↘</span></a></div>
<div class="hero-foot"><span>${e(c.heroFoot[0])}</span><span class="rule" aria-hidden="true"></span><span>${e(c.heroFoot[1])}</span><span class="rule" aria-hidden="true"></span><span>${e(c.heroFoot[2])}</span></div></div>
<div class="hero-stage" aria-label="KUMIHAN"><div class="logo-card"><img src="assets/${META.logo}" width="1254" height="1254" alt="KUMIHAN official logo" fetchpriority="high"></div><span class="stage-label">WORDS · SPACE · PURPOSE</span></div>
</div></section>
<section class="intro-strip" id="concept" aria-labelledby="concept-title"><div class="shell intro-layout"><span class="section-number">01 / THE IDEA</span><div class="intro-text"><h2 id="concept-title">${e(c.concept[0])}<br><em>${e(c.concept[1])}</em></h2><p>${e(c.conceptBody)}</p></div></div></section>
<section class="features" id="features" aria-labelledby="features-title"><div class="shell">
<div class="section-heading"><div><span class="section-number">02 / PRINCIPLES</span><h2 id="features-title">${e(c.featuresH2)}</h2></div><p>${e(c.featuresDeck)}</p></div>
<div class="feature-grid">${feature}</div>
</div></section>
<section class="idea-band" aria-labelledby="idea-title"><div class="shell idea-layout"><div><p class="eyebrow"><span class="line" aria-hidden="true"></span> ${e(c.ideaEyebrow)}</p><h2 id="idea-title">${e(c.idea[0])}<br><strong>${e(c.idea[1])}</strong></h2><p>${e(c.ideaBody)}</p></div><div class="idea-art" aria-hidden="true"><span></span><span></span><span></span><span></span><span></span><small>FORM FOLLOWS MEANING</small></div></div></section>
<section class="skills-section" id="skills" aria-labelledby="skills-title"><div class="shell"><div class="section-heading"><div><span class="section-number">03 / SKILLS</span><h2 id="skills-title">${e(c.skillsH2[0])}<br>${e(c.skillsH2[1])}</h2></div><p>${e(c.skillsDeck)}</p></div><div class="skills-grid">${skills}</div></div></section>
<section class="install-section" id="install" aria-labelledby="install-title"><div class="shell install-layout"><div class="install-intro"><div class="section-number" dir="ltr">04 / GET STARTED</div><h2 id="install-title">${e(c.installH2[0])}<br>${e(c.installH2[1])}</h2><p>${e(c.installBody)}</p></div><div><div class="install-links">${hosts}</div><div class="install-extra"><a href="${META.release}" target="_blank" rel="noopener noreferrer">${e(c.allZips)}</a></div></div></div></section>
<section class="status-section" aria-labelledby="status-title"><div class="shell status-box"><div><div class="status-title" id="status-title" dir="ltr">${e(c.statusTitle)}</div><p>${e(c.statusBody)}</p></div><div class="status-meta"><a href="${META.release}" target="_blank" rel="noopener noreferrer">${e(c.statusLink)}</a><br><span dir="ltr">OPEN SOURCE · APACHE 2.0</span></div></div></section>
<section class="cta-section" aria-labelledby="final-title"><div class="shell cta-layout"><div><span class="section-number">05 / OPEN SOURCE</span><h2 id="final-title">${e(c.finalH2[0])}<br>${e(c.finalH2[1])}</h2><p>${e(c.finalBody)}</p></div><a class="button button-primary" href="${META.repo}">${e(c.finalCta)}<span class="arrow" aria-hidden="true">↗</span></a></div></section>
</main>
${footer(lang,"")}
</body></html>
`;
}
function renderGuide(host,lang){
 const c=DATA[lang],g=c.guide,label=hostLabel(host),file=guideName(host,lang);
 const labelHead=(lang==="vi"?"Cài đặt cho ":lang==="ja"?"導入方法：":"Install for ")+label;
 const langs=["vi","en","ja"].map(l=>`<a href="${guideName(host,l)}" lang="${l}" hreflang="${l}"${l===lang?' aria-current="page"':""}>${{vi:"Tiếng Việt",en:"EN",ja:"日本語"}[l]}</a>`).join("");
 const nav=["chatgpt","claude","gemini"].map((h,i)=>`<a href="${guideName(h,lang)}"${h===host?' aria-current="page"':""}>${"0"+(i+1)} / ${e(hostLabel(h))}<span class="arrow" aria-hidden="true">↗</span></a>`).join("");
 const zips=["","-web","-documents","-review"].map(s=>`<li><a href="${META.download+skillZip(host,s)}">${e(skillZip(host,s))}</a></li>`).join("");
 const cmd=host==="claude"?`claude --plugin-dir /absolute/path/${META.id}\nclaude plugin validate /absolute/path/${META.id}`:host==="gemini"?`gemini extensions install /absolute/path/${META.id}\ngemini extensions list`:"";
 const step=host==="claude"?
  (lang==="vi"?"Giải nén tệp ZIP vào thư mục trống, giữ nguyên thư mục sản phẩm; dùng Claude Code để nạp plugin. Có thể dùng marketplace của kho mã nguồn khi công cụ hỗ trợ.":lang==="ja"?"ZIPを展開し製品フォルダを保持したままClaude Codeで読み込みます。対応する環境ではリポジトリのマーケットプレイスから導入できます。":"Unzip into an empty directory, keep the product folder and load it from Claude Code. The repository marketplace is an alternative where supported."):
  host==="gemini"?
  (lang==="vi"?"Giải nén để gemini-extension.json nằm trong thư mục plugin và cài bằng Gemini CLI. Chưa xác minh việc nhập trong ứng dụng chat Gemini.":lang==="ja"?"gemini-extension.jsonが製品フォルダに入るよう展開してGemini CLIで導入します。Geminiチャットアプリへの導入は未検証です。":"Unzip so gemini-extension.json is in the product folder, then install with Gemini CLI. Gemini chat app importing is not verified."):
  (lang==="vi"?"Dùng trình cài plugin được hỗ trợ trên ChatGPT/Codex hoặc chọn một kỹ năng riêng khi có giao diện Skills. Đính kèm tệp ZIP không phải cài đặt.":lang==="ja"?"ChatGPT/Codexで対応しているプラグイン導入機能を使うか、Skills対応画面で単独スキルを選びます。ZIP添付はインストールではありません。":"Use a supported ChatGPT/Codex plugin importer or a standalone Skill through an available Skills interface. A ZIP attachment is not an install.");
 return `<!doctype html>
<html lang="${lang}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#f5f3ee">
<title>${e(labelHead)} | ${e(META.display)}</title><meta name="description" content="${e(g.lead)}">
<link rel="canonical" href="${META.base}docs/${file}">${altLinks(true,host)}
<link rel="alternate" hreflang="x-default" href="${META.base}docs/${guideName(host,"vi")}">
<link rel="icon" href="../assets/favicon-32x32.png" type="image/png"><link rel="stylesheet" href="../assets/kumihan-install.css">
<style>html[lang="vi"] body{font-family:"Be Vietnam Pro","Noto Sans",system-ui,Arial,sans-serif}html[lang="vi"] :is(h1,h2,h3){letter-spacing:-.02em;line-height:1.45}html[lang="vi"] .guide-pane{line-height:1.95} .hero .language-switch{flex-wrap:wrap} .guide-pane section{scroll-margin-top:28px} .guide-pane li{overflow-wrap:anywhere}</style>
${fonts(lang,"../")}
</head><body>
<a class="skip skip-link" href="#main">${e(c.skip)}</a>
<header class="site-header"><div class="shell header-inner"><a class="brand" href="../${pageName(lang)}">KUMIHAN<span class="brand-sub">｜Nhịp Chữ</span></a>
<nav class="header-nav" aria-label="${e(g.nav)}"><a href="${guideName("chatgpt",lang)}"${host==="chatgpt"?' aria-current="page"':""}>ChatGPT / Codex</a><a href="${guideName("claude",lang)}"${host==="claude"?' aria-current="page"':""}>Claude</a><a href="${guideName("gemini",lang)}"${host==="gemini"?' aria-current="page"':""}>Gemini</a></nav></div></header>
<section class="hero" aria-labelledby="page-title"><div class="shell"><nav class="breadcrumb" aria-label="${e(g.crumb)}"><a href="../${GATEWAY[lang]}">${e(c.family)}</a><span aria-hidden="true">/</span><a href="../${pageName(lang)}">${e(META.display)}</a><span aria-hidden="true">/</span>${e(g.crumb)}</nav>
<div class="hero-grid"><div><p class="eyebrow">INSTALL GUIDE / ${host==="chatgpt"?"01":host==="claude"?"02":"03"} OF 03</p><h1 id="page-title">${e(labelHead)}</h1><p class="hero-desc">${e(g.lead)}</p><nav class="language-switch" aria-label="${e(c.language)}">${langs}</nav></div>
<div class="hero-logo"><img src="../assets/${META.logo}" width="1254" height="1254" alt="KUMIHAN official logo"></div></div></div></section>
<nav class="platform-nav" aria-label="${e(g.nav)}"><div class="shell platform-inner">${nav}</div></nav>
<div class="shell content-layout" id="main"><aside class="toc" aria-label="${e(g.toc)}"><details class="toc-details" open><summary>${e(g.toc)}</summary><h2 class="toc-title">${e(g.toc)}</h2>
<ol><li><a href="#format">${e(g.formats)}</a></li><li><a href="#download">${e(g.download)}</a></li><li><a href="#steps">${e(g.install)}</a></li><li><a href="#test">${e(g.test)}</a></li><li><a href="#updates">${e(g.updates)}</a></li><li><a href="#limits">${e(g.limits)}</a></li></ol></details>
<div class="toc-note"><strong>${e(g.note)}</strong><a class="source-link" href="${META.repo}/blob/main/plugins/${META.id}/INSTALL.md">${e(g.source)} ↗</a></div></aside>
<article class="guide" aria-labelledby="guide-title"><div class="guide-head"><span>INSTALLATION / ${host.toUpperCase()}</span><span class="step-label">v${META.version}</span></div>
<div class="guide-pane"><h2 id="guide-title">${e(g.crumb)}</h2>
<section id="format"><h2>${e(g.formats)}</h2><p>${e(g.formatDesc)}</p><ul><li>${e(g.plugin)}: <code>${e(hostZip(host))}</code></li><li>${e(g.skill)}: <code>${e(skillZip(host,""))}</code></li></ul></section>
<section id="download"><h2>${e(g.download)}</h2><p>${e(g.downloadDesc)}</p><p><a href="${META.download+hostZip(host)}">${e(hostZip(host))}</a></p><p><a href="${META.download}SHA256SUMS.txt">SHA256SUMS.txt</a> · <a href="${META.download}MANIFEST.json">MANIFEST.json</a></p><h3>4 Skills</h3><ul class="download-list">${zips}</ul></section>
<section id="steps"><h2>${e(g.install)}</h2><p>${e(step)}</p>${cmd?`<h3>${e(g.cmd)}</h3><pre><code>${e(cmd)}</code></pre>`:""}${host==="claude"?`<pre><code>/plugin marketplace add landco-llc/kumihan\n/plugin install ${META.id}@kumihan-marketplace</code></pre>`:""}</section>
<section id="test"><h2>${e(g.test)}</h2><p>${e(g.testing)}</p><blockquote><p>${e(g.prompt)}</p></blockquote><pre><code>python runtime/checks.py input.txt --locale vi-VN</code></pre></section>
<section id="updates"><h2>${e(g.updates)}</h2><p>${e(g.updateDesc)}</p></section>
<section id="limits"><h2>${e(g.limits)}</h2><p>${e(g.limitDesc)}</p></section>
</div></article></div>
${footer(lang,"../")}
</body></html>\n`;
}
const out={};
for(const lang of ["vi","en","ja"]){
 out[pageName(lang)]=share(renderLanding(lang));
 for(const host of ["chatgpt","claude","gemini"])out["docs/"+guideName(host,lang)]=share(renderGuide(host,lang));
}
const base=resolve(new URL("..",import.meta.url).pathname);
let invalid=[];
for(const [p,content] of Object.entries(out)){
 const filepath=resolve(base,p);
 if(process.argv.includes("--check")){
  if(readFileSync(filepath,"utf8")!==content)invalid.push(p);
 }else writeFileSync(filepath,content,"utf8");
}
if(invalid.length){console.error("Out of date:",invalid);process.exit(1);}
console.log("KUMIHAN Nhịp Chữ pages:",Object.keys(out).length, process.argv.includes("--check")?"verified":"written");
