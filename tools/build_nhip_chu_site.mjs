#!/usr/bin/env node
// Generated with product-specific KUMIHAN｜Nhịp Chữ skills after standalone Skills were completed.
// No external dependencies. --check is non-writing; otherwise regenerate all twelve HTML files.
import {readFileSync,writeFileSync} from "node:fs";
import {resolve} from "node:path";
const META={"id":"kumihan-nhip-chu","display":"KUMIHAN｜Nhịp Chữ","version":"0.1.0","repo":"https://github.com/landco-llc/kumihan","base":"https://landco-llc.github.io/kumihan/","release":"https://github.com/landco-llc/kumihan/releases/tag/kumihan-vi-v0.1.0","download":"https://github.com/landco-llc/kumihan/releases/download/kumihan-vi-v0.1.0/","logo":"KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png"};
const DATA=JSON.parse(readFileSync(new URL("../assets/nhip-chu-site-copy.json", import.meta.url),"utf8"));
function e(s){return String(s).replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;").replaceAll('"',"&quot;").replaceAll("'","&#39;")}
function pageName(lang){return "kumihan-vi"+(lang==="vi"?"":"."+lang)+".html";}
function guideName(host,lang){return "install-nhip-chu-"+host+(lang==="vi"?"":"."+lang)+".html";}
function hostZip(host){return META.id+"-"+({chatgpt:"chatgpt-codex-plugin",claude:"claude-code-plugin",gemini:"gemini-cli-extension"})[host]+"-v"+META.version+".zip";}
function skillZip(host,suffix){return META.id+suffix+"-"+host+"-skill-v"+META.version+".zip";}
function hostLabel(host){return {chatgpt:"ChatGPT / Codex",claude:"Claude / Claude Code",gemini:"Gemini"}[host];}
function altLinks(guide,host){return ["vi","en","ja"].map(lang=>'<link rel="alternate" hreflang="'+lang+'" href="'+e(META.base+(guide?"docs/"+guideName(host,lang):pageName(lang)))+'">').join("\n");}
function renderLanding(lang){
 const c=DATA[lang],file=pageName(lang), rel=lang==="vi"?"vi_VN":lang==="ja"?"ja_JP":"en_US",ls={vi:"VI",en:"EN",ja:"日本語"};
 const links=["vi","en","ja"].map(l=>`<a href="${pageName(l)}" lang="${l}" hreflang="${l}"${l===lang?' aria-current="page"':""}>${ls[l]}</a>`).join("");
 const feature=c.features.map(f=>`<article class="feature"><span class="feature-index">${e(f[0])}</span><div class="feature-motif" aria-hidden="true">${e(f[1])}</div><h3>${e(f[2])}</h3><p>${e(f[3])}</p></article>`).join("\n");
 const skills=["","-web","-documents","-review"].map((s,i)=>`<article class="skill-card"><div class="card-top"><span class="skill-type">0${i+1} / ${["ENTRY","WEB","DOCUMENTS","REVIEW"][i]}</span><span class="skill-symbol" aria-hidden="true">${["◎","↗","¶","◌"][i]}</span></div><h3 class="skill-name">${e(c.skills[i][0])}</h3><p class="skill-desc">${e(c.skills[i][1])}</p><a class="skill-end" href="${META.repo}/blob/main/plugins/${META.id}/skills/${META.id}${s}/SKILL.md">${e(c.view)} ↗</a></article>`).join("\n");
 const hosts=["chatgpt","claude","gemini"].map((h,i)=>`<a class="platform-row" href="docs/${guideName(h,lang)}"><span class="platform-index">0${i+1}</span><span class="platform-info"><strong class="platform-name">${e(hostLabel(h))}</strong><span class="platform-note">${e(c.installNotes[i])}</span></span><span class="platform-arrow" aria-hidden="true">↗</span></a>`).join("");
 return `<!doctype html>
<html lang="${lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#f5f3ee">
<meta name="description" content="${e(c.description)}">
<title>${e(c.title)}</title>
<meta property="og:type" content="website"><meta property="og:locale" content="${rel}">
<meta property="og:title" content="${e(c.title)}"><meta property="og:description" content="${e(c.description)}">
<meta property="og:url" content="${META.base+file}"><meta property="og:image" content="${META.base}assets/${META.logo}">
<link rel="canonical" href="${META.base+file}">
${altLinks(false)}
<link rel="alternate" hreflang="x-default" href="${META.base}kumihan-vi.html">
<link rel="icon" type="image/png" href="assets/favicon-32x32.png">
<link rel="stylesheet" href="assets/nhip-chu-site.css">
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
<h1 id="hero-title">${e(c.h1[0])}<br><span class="accent">${e(c.h1[1])}</span></h1>
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
<section class="idea-band" aria-labelledby="idea-title"><div class="shell idea-layout"><div class="idea-art" aria-hidden="true"><span>Ă&nbsp;Â&nbsp;Ê</span><strong>Đ Ệ Ễ</strong><span>Ơ&nbsp;Ư&nbsp;Ắ</span></div><div><p class="eyebrow">${e(c.ideaEyebrow)}</p><h2 id="idea-title">${e(c.idea[0])}<br>${e(c.idea[1])}</h2><p>${e(c.ideaBody)}</p></div></div></section>
<section class="skills-section" id="skills" aria-labelledby="skills-title"><div class="shell"><div class="section-heading"><div><span class="section-number">03 / SKILLS</span><h2 id="skills-title">${e(c.skillsH2[0])}<br>${e(c.skillsH2[1])}</h2></div><p>${e(c.skillsDeck)}</p></div><div class="skills-grid">${skills}</div></div></section>
<section class="install-section" id="install" aria-labelledby="install-title"><div class="shell install-layout"><div class="install-intro"><span class="section-number">04 / GET STARTED</span><h2 id="install-title">${e(c.installH2[0])}<br>${e(c.installH2[1])}</h2><p>${e(c.installBody)}</p><a class="install-extra" href="${META.release}">${e(c.allZips)}</a></div><div class="install-links">${hosts}</div></div></section>
<section class="status-section" aria-label="${e(c.statusTitle)}"><div class="shell status-box"><span class="status-title">${e(c.statusTitle)}</span><p>${e(c.statusBody)}</p><div class="status-meta"><a href="${META.release}">${e(c.statusLink)}</a></div></div></section>
<section class="cta-section" aria-labelledby="final-title"><div class="shell cta-layout"><div><span class="section-number">05 / OPEN SOURCE</span><h2 id="final-title">${e(c.finalH2[0])}<br>${e(c.finalH2[1])}</h2><p>${e(c.finalBody)}</p></div><a class="button button-primary" href="${META.repo}">${e(c.finalCta)}<span class="arrow" aria-hidden="true">↗</span></a></div></section>
</main>
<footer class="footer"><div class="shell footer-layout"><div class="footer-mark"><strong>${e(META.display)}</strong><p class="footer-sub">${e(c.footerSub)}</p></div><nav class="footer-links" aria-label="Footer"><a href="index.html">${e(c.family)}</a><a href="${META.repo}">GitHub</a><a href="https://landco.co.jp/" target="_blank" rel="noopener noreferrer">L&amp;Co. LLC ↗</a><a href="#top">${e(c.backTop)} ↑</a></nav></div></footer>
</body></html>
`;
}
function renderGuide(host,lang){
 const c=DATA[lang],g=c.guide,label=hostLabel(host),file=guideName(host,lang),loc=lang==="vi"?"vi_VN":lang==="ja"?"ja_JP":"en_US";
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
<meta property="og:type" content="website"><meta property="og:locale" content="${loc}"><meta property="og:title" content="${e(labelHead)}"><meta property="og:image" content="${META.base}assets/${META.logo}">
<link rel="icon" href="../assets/favicon-32x32.png" type="image/png"><link rel="stylesheet" href="../assets/kumihan-install.css">
<style>html[lang="vi"] body{font-family:"Be Vietnam Pro","Noto Sans",system-ui,Arial,sans-serif}html[lang="vi"] :is(h1,h2,h3){letter-spacing:-.02em;line-height:1.45}html[lang="vi"] .guide-pane{line-height:1.95} .hero .language-switch{flex-wrap:wrap} .guide-pane section{scroll-margin-top:28px} .guide-pane li{overflow-wrap:anywhere}</style>
</head><body>
<a class="skip skip-link" href="#main">${e(c.skip)}</a>
<header class="site-header"><div class="shell header-inner"><a class="brand" href="../${pageName(lang)}">KUMIHAN<span class="brand-sub">｜Nhịp Chữ</span></a>
<nav class="header-nav" aria-label="${e(g.nav)}"><a href="${guideName("chatgpt",lang)}"${host==="chatgpt"?' aria-current="page"':""}>ChatGPT / Codex</a><a href="${guideName("claude",lang)}"${host==="claude"?' aria-current="page"':""}>Claude</a><a href="${guideName("gemini",lang)}"${host==="gemini"?' aria-current="page"':""}>Gemini</a></nav></div></header>
<section class="hero" aria-labelledby="page-title"><div class="shell"><nav class="breadcrumb" aria-label="${e(g.crumb)}"><a href="../index.html">${e(c.family)}</a><span aria-hidden="true">/</span><a href="../${pageName(lang)}">${e(META.display)}</a><span aria-hidden="true">/</span>${e(g.crumb)}</nav>
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
<footer class="footer"><div class="shell footer-inner"><a href="../${pageName(lang)}">${e(META.display)}</a><a href="https://landco.co.jp/" target="_blank" rel="noopener noreferrer">L&amp;Co. LLC ↗</a><a href="${META.repo}">GitHub</a></div></footer>
</body></html>\n`;
}
const out={};
for(const lang of ["vi","en","ja"]){
 out[pageName(lang)]=renderLanding(lang);
 for(const host of ["chatgpt","claude","gemini"])out["docs/"+guideName(host,lang)]=renderGuide(host,lang);
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
