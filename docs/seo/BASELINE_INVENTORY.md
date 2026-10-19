# SEO baseline inventory — 2026-10-19 (JST)

W00 Fresh Read基点: 最新取得 `origin/main` = `ba1c50fdf2de8f920257d417e6213cd9ea0a2443`。作業ブランチ `feature/seo-foundation-20261019` は `2ea293f5db838e85817c934625d9b9cf0ab30ac4` で最新mainを安全にmerge済み。仕様書の旧基点 `fce40015abaa1f5f309cf9e977f55e41537c13aa` 以後のMizani追加を含む。

## 公開候補と正本

root HTML **72** = gateway 18 + 日本語製品3 + その他17製品×3。docs HTML **159**。合計 **231**。最終indexability・canonical・生成一致の実測は [VALIDATION_LOG.md](VALIDATION_LOG.md) を参照。棚卸しは検索エンジン登録済みを意味しない。

各行は実在する公開候補1ファイル。出力URLは `https://landco-llc.github.io/kumihan/` + path（`index.html`のみ `/kumihan/` に正規化）。Jekyll行はテンプレート処理後の同名HTMLが公開物。生成器のコピー正本は各 `assets/*-site-copy.json`、共有JA/ENコピーは `tools/base_copy.py`。Arabic/Thai/Vietnamese/字律/字衡は固有生成経路を保持する。

| Output path | Category | Source → output |
| --- | --- | --- |
| `docs/install-accord-chatgpt.en.html` | Generated guide | `tools/build_accord_site.py + tools/install_frame.py` |
| `docs/install-accord-chatgpt.html` | Generated guide | `tools/build_accord_site.py + tools/install_frame.py` |
| `docs/install-accord-chatgpt.ja.html` | Generated guide | `tools/build_accord_site.py + tools/install_frame.py` |
| `docs/install-accord-claude.en.html` | Generated guide | `tools/build_accord_site.py + tools/install_frame.py` |
| `docs/install-accord-claude.html` | Generated guide | `tools/build_accord_site.py + tools/install_frame.py` |
| `docs/install-accord-claude.ja.html` | Generated guide | `tools/build_accord_site.py + tools/install_frame.py` |
| `docs/install-accord-gemini.en.html` | Generated guide | `tools/build_accord_site.py + tools/install_frame.py` |
| `docs/install-accord-gemini.html` | Generated guide | `tools/build_accord_site.py + tools/install_frame.py` |
| `docs/install-accord-gemini.ja.html` | Generated guide | `tools/build_accord_site.py + tools/install_frame.py` |
| `docs/install-chatgpt.html` | Jekyll guide | `docs/install-chatgpt.html frontmatter/Markdown includes → _layouts/installation.html` |
| `docs/install-chatgpt.zh-tw.html` | Jekyll guide | `docs/install-chatgpt.zh-tw.html frontmatter/Markdown includes → _layouts/installation.html` |
| `docs/install-claude.html` | Jekyll guide | `docs/install-claude.html frontmatter/Markdown includes → _layouts/installation.html` |
| `docs/install-claude.zh-tw.html` | Jekyll guide | `docs/install-claude.zh-tw.html frontmatter/Markdown includes → _layouts/installation.html` |
| `docs/install-compasso-chatgpt.en.html` | Generated guide | `tools/build_compasso_site.py + tools/install_frame.py` |
| `docs/install-compasso-chatgpt.html` | Generated guide | `tools/build_compasso_site.py + tools/install_frame.py` |
| `docs/install-compasso-chatgpt.ja.html` | Generated guide | `tools/build_compasso_site.py + tools/install_frame.py` |
| `docs/install-compasso-claude.en.html` | Generated guide | `tools/build_compasso_site.py + tools/install_frame.py` |
| `docs/install-compasso-claude.html` | Generated guide | `tools/build_compasso_site.py + tools/install_frame.py` |
| `docs/install-compasso-claude.ja.html` | Generated guide | `tools/build_compasso_site.py + tools/install_frame.py` |
| `docs/install-compasso-gemini.en.html` | Generated guide | `tools/build_compasso_site.py + tools/install_frame.py` |
| `docs/install-compasso-gemini.html` | Generated guide | `tools/build_compasso_site.py + tools/install_frame.py` |
| `docs/install-compasso-gemini.ja.html` | Generated guide | `tools/build_compasso_site.py + tools/install_frame.py` |
| `docs/install-equilibrio-chatgpt.en.html` | Generated guide | `tools/build_equilibrio_site.py + tools/install_frame.py` |
| `docs/install-equilibrio-chatgpt.html` | Generated guide | `tools/build_equilibrio_site.py + tools/install_frame.py` |
| `docs/install-equilibrio-chatgpt.ja.html` | Generated guide | `tools/build_equilibrio_site.py + tools/install_frame.py` |
| `docs/install-equilibrio-claude.en.html` | Generated guide | `tools/build_equilibrio_site.py + tools/install_frame.py` |
| `docs/install-equilibrio-claude.html` | Generated guide | `tools/build_equilibrio_site.py + tools/install_frame.py` |
| `docs/install-equilibrio-claude.ja.html` | Generated guide | `tools/build_equilibrio_site.py + tools/install_frame.py` |
| `docs/install-equilibrio-gemini.en.html` | Generated guide | `tools/build_equilibrio_site.py + tools/install_frame.py` |
| `docs/install-equilibrio-gemini.html` | Generated guide | `tools/build_equilibrio_site.py + tools/install_frame.py` |
| `docs/install-equilibrio-gemini.ja.html` | Generated guide | `tools/build_equilibrio_site.py + tools/install_frame.py` |
| `docs/install-gemini.html` | Jekyll guide | `docs/install-gemini.html frontmatter/Markdown includes → _layouts/installation.html` |
| `docs/install-gemini.zh-tw.html` | Jekyll guide | `docs/install-gemini.zh-tw.html frontmatter/Markdown includes → _layouts/installation.html` |
| `docs/install-grafia-chatgpt.en.html` | Generated guide | `tools/build_grafia_site.py + tools/install_frame.py` |
| `docs/install-grafia-chatgpt.html` | Generated guide | `tools/build_grafia_site.py + tools/install_frame.py` |
| `docs/install-grafia-chatgpt.ja.html` | Generated guide | `tools/build_grafia_site.py + tools/install_frame.py` |
| `docs/install-grafia-claude.en.html` | Generated guide | `tools/build_grafia_site.py + tools/install_frame.py` |
| `docs/install-grafia-claude.html` | Generated guide | `tools/build_grafia_site.py + tools/install_frame.py` |
| `docs/install-grafia-claude.ja.html` | Generated guide | `tools/build_grafia_site.py + tools/install_frame.py` |
| `docs/install-grafia-gemini.en.html` | Generated guide | `tools/build_grafia_site.py + tools/install_frame.py` |
| `docs/install-grafia-gemini.html` | Generated guide | `tools/build_grafia_site.py + tools/install_frame.py` |
| `docs/install-grafia-gemini.ja.html` | Generated guide | `tools/build_grafia_site.py + tools/install_frame.py` |
| `docs/install-ko-chatgpt.en.html` | Jekyll Korean | `docs/install-ko-chatgpt.en.html frontmatter/body → _layouts/geuljjaim.html` |
| `docs/install-ko-chatgpt.html` | Jekyll Korean | `docs/install-ko-chatgpt.html frontmatter/body → _layouts/geuljjaim.html` |
| `docs/install-ko-chatgpt.ja.html` | Jekyll Korean | `docs/install-ko-chatgpt.ja.html frontmatter/body → _layouts/geuljjaim.html` |
| `docs/install-ko-claude.en.html` | Jekyll Korean | `docs/install-ko-claude.en.html frontmatter/body → _layouts/geuljjaim.html` |
| `docs/install-ko-claude.html` | Jekyll Korean | `docs/install-ko-claude.html frontmatter/body → _layouts/geuljjaim.html` |
| `docs/install-ko-claude.ja.html` | Jekyll Korean | `docs/install-ko-claude.ja.html frontmatter/body → _layouts/geuljjaim.html` |
| `docs/install-ko-gemini.en.html` | Jekyll Korean | `docs/install-ko-gemini.en.html frontmatter/body → _layouts/geuljjaim.html` |
| `docs/install-ko-gemini.html` | Jekyll Korean | `docs/install-ko-gemini.html frontmatter/body → _layouts/geuljjaim.html` |
| `docs/install-ko-gemini.ja.html` | Jekyll Korean | `docs/install-ko-gemini.ja.html frontmatter/body → _layouts/geuljjaim.html` |
| `docs/install-kumihan-ar-chatgpt.en.html` | Generated guide | `tools/build_ar_site.py + tools/install_frame.py` |
| `docs/install-kumihan-ar-chatgpt.html` | Generated guide | `tools/build_ar_site.py + tools/install_frame.py` |
| `docs/install-kumihan-ar-chatgpt.ja.html` | Generated guide | `tools/build_ar_site.py + tools/install_frame.py` |
| `docs/install-kumihan-ar-claude.en.html` | Generated guide | `tools/build_ar_site.py + tools/install_frame.py` |
| `docs/install-kumihan-ar-claude.html` | Generated guide | `tools/build_ar_site.py + tools/install_frame.py` |
| `docs/install-kumihan-ar-claude.ja.html` | Generated guide | `tools/build_ar_site.py + tools/install_frame.py` |
| `docs/install-kumihan-ar-gemini.en.html` | Generated guide | `tools/build_ar_site.py + tools/install_frame.py` |
| `docs/install-kumihan-ar-gemini.html` | Generated guide | `tools/build_ar_site.py + tools/install_frame.py` |
| `docs/install-kumihan-ar-gemini.ja.html` | Generated guide | `tools/build_ar_site.py + tools/install_frame.py` |
| `docs/install-kumihan-bn-chatgpt.en.html` | Authored Bangla | `docs/install-kumihan-bn-chatgpt.en.html (authored body/head copy; shared build_seo adapter)` |
| `docs/install-kumihan-bn-chatgpt.html` | Authored Bangla | `docs/install-kumihan-bn-chatgpt.html (authored body/head copy; shared build_seo adapter)` |
| `docs/install-kumihan-bn-chatgpt.ja.html` | Authored Bangla | `docs/install-kumihan-bn-chatgpt.ja.html (authored body/head copy; shared build_seo adapter)` |
| `docs/install-kumihan-bn-claude.en.html` | Authored Bangla | `docs/install-kumihan-bn-claude.en.html (authored body/head copy; shared build_seo adapter)` |
| `docs/install-kumihan-bn-claude.html` | Authored Bangla | `docs/install-kumihan-bn-claude.html (authored body/head copy; shared build_seo adapter)` |
| `docs/install-kumihan-bn-claude.ja.html` | Authored Bangla | `docs/install-kumihan-bn-claude.ja.html (authored body/head copy; shared build_seo adapter)` |
| `docs/install-kumihan-bn-gemini.en.html` | Authored Bangla | `docs/install-kumihan-bn-gemini.en.html (authored body/head copy; shared build_seo adapter)` |
| `docs/install-kumihan-bn-gemini.html` | Authored Bangla | `docs/install-kumihan-bn-gemini.html (authored body/head copy; shared build_seo adapter)` |
| `docs/install-kumihan-bn-gemini.ja.html` | Authored Bangla | `docs/install-kumihan-bn-gemini.ja.html (authored body/head copy; shared build_seo adapter)` |
| `docs/install-kumihan-hi-chatgpt.en.html` | Generated guide | `tools/build_hi_site.py + tools/install_frame.py` |
| `docs/install-kumihan-hi-chatgpt.html` | Generated guide | `tools/build_hi_site.py + tools/install_frame.py` |
| `docs/install-kumihan-hi-chatgpt.ja.html` | Generated guide | `tools/build_hi_site.py + tools/install_frame.py` |
| `docs/install-kumihan-hi-claude.en.html` | Generated guide | `tools/build_hi_site.py + tools/install_frame.py` |
| `docs/install-kumihan-hi-claude.html` | Generated guide | `tools/build_hi_site.py + tools/install_frame.py` |
| `docs/install-kumihan-hi-claude.ja.html` | Generated guide | `tools/build_hi_site.py + tools/install_frame.py` |
| `docs/install-kumihan-hi-gemini.en.html` | Generated guide | `tools/build_hi_site.py + tools/install_frame.py` |
| `docs/install-kumihan-hi-gemini.html` | Generated guide | `tools/build_hi_site.py + tools/install_frame.py` |
| `docs/install-kumihan-hi-gemini.ja.html` | Generated guide | `tools/build_hi_site.py + tools/install_frame.py` |
| `docs/install-kumihan-th-chatgpt.en.html` | Generated guide | `tools/build_th_site.py + tools/install_frame.py` |
| `docs/install-kumihan-th-chatgpt.html` | Generated guide | `tools/build_th_site.py + tools/install_frame.py` |
| `docs/install-kumihan-th-chatgpt.ja.html` | Generated guide | `tools/build_th_site.py + tools/install_frame.py` |
| `docs/install-kumihan-th-claude.en.html` | Generated guide | `tools/build_th_site.py + tools/install_frame.py` |
| `docs/install-kumihan-th-claude.html` | Generated guide | `tools/build_th_site.py + tools/install_frame.py` |
| `docs/install-kumihan-th-claude.ja.html` | Generated guide | `tools/build_th_site.py + tools/install_frame.py` |
| `docs/install-kumihan-th-gemini.en.html` | Generated guide | `tools/build_th_site.py + tools/install_frame.py` |
| `docs/install-kumihan-th-gemini.html` | Generated guide | `tools/build_th_site.py + tools/install_frame.py` |
| `docs/install-kumihan-th-gemini.ja.html` | Generated guide | `tools/build_th_site.py + tools/install_frame.py` |
| `docs/install-lad-chatgpt.en.html` | Generated guide | `tools/build_lad_site.py + tools/install_frame.py` |
| `docs/install-lad-chatgpt.html` | Generated guide | `tools/build_lad_site.py + tools/install_frame.py` |
| `docs/install-lad-chatgpt.ja.html` | Generated guide | `tools/build_lad_site.py + tools/install_frame.py` |
| `docs/install-lad-claude.en.html` | Generated guide | `tools/build_lad_site.py + tools/install_frame.py` |
| `docs/install-lad-claude.html` | Generated guide | `tools/build_lad_site.py + tools/install_frame.py` |
| `docs/install-lad-claude.ja.html` | Generated guide | `tools/build_lad_site.py + tools/install_frame.py` |
| `docs/install-lad-gemini.en.html` | Generated guide | `tools/build_lad_site.py + tools/install_frame.py` |
| `docs/install-lad-gemini.html` | Generated guide | `tools/build_lad_site.py + tools/install_frame.py` |
| `docs/install-lad-gemini.ja.html` | Generated guide | `tools/build_lad_site.py + tools/install_frame.py` |
| `docs/install-laras-chatgpt.en.html` | Generated guide | `tools/build_laras_site.py + tools/install_frame.py` |
| `docs/install-laras-chatgpt.html` | Generated guide | `tools/build_laras_site.py + tools/install_frame.py` |
| `docs/install-laras-chatgpt.ja.html` | Generated guide | `tools/build_laras_site.py + tools/install_frame.py` |
| `docs/install-laras-claude.en.html` | Generated guide | `tools/build_laras_site.py + tools/install_frame.py` |
| `docs/install-laras-claude.html` | Generated guide | `tools/build_laras_site.py + tools/install_frame.py` |
| `docs/install-laras-claude.ja.html` | Generated guide | `tools/build_laras_site.py + tools/install_frame.py` |
| `docs/install-laras-gemini.en.html` | Generated guide | `tools/build_laras_site.py + tools/install_frame.py` |
| `docs/install-laras-gemini.html` | Generated guide | `tools/build_laras_site.py + tools/install_frame.py` |
| `docs/install-laras-gemini.ja.html` | Generated guide | `tools/build_laras_site.py + tools/install_frame.py` |
| `docs/install-mizani-chatgpt.en.html` | Generated guide | `tools/build_mizani_site.py + tools/install_frame.py` |
| `docs/install-mizani-chatgpt.html` | Generated guide | `tools/build_mizani_site.py + tools/install_frame.py` |
| `docs/install-mizani-chatgpt.ja.html` | Generated guide | `tools/build_mizani_site.py + tools/install_frame.py` |
| `docs/install-mizani-claude.en.html` | Generated guide | `tools/build_mizani_site.py + tools/install_frame.py` |
| `docs/install-mizani-claude.html` | Generated guide | `tools/build_mizani_site.py + tools/install_frame.py` |
| `docs/install-mizani-claude.ja.html` | Generated guide | `tools/build_mizani_site.py + tools/install_frame.py` |
| `docs/install-mizani-gemini.en.html` | Generated guide | `tools/build_mizani_site.py + tools/install_frame.py` |
| `docs/install-mizani-gemini.html` | Generated guide | `tools/build_mizani_site.py + tools/install_frame.py` |
| `docs/install-mizani-gemini.ja.html` | Generated guide | `tools/build_mizani_site.py + tools/install_frame.py` |
| `docs/install-nhip-chu-chatgpt.en.html` | Generated guide | `tools/build_nhip_chu_site.mjs + assets/nhip-chu-site-copy.json + tools/install_frame.py` |
| `docs/install-nhip-chu-chatgpt.html` | Generated guide | `tools/build_nhip_chu_site.mjs + assets/nhip-chu-site-copy.json + tools/install_frame.py` |
| `docs/install-nhip-chu-chatgpt.ja.html` | Generated guide | `tools/build_nhip_chu_site.mjs + assets/nhip-chu-site-copy.json + tools/install_frame.py` |
| `docs/install-nhip-chu-claude.en.html` | Generated guide | `tools/build_nhip_chu_site.mjs + assets/nhip-chu-site-copy.json + tools/install_frame.py` |
| `docs/install-nhip-chu-claude.html` | Generated guide | `tools/build_nhip_chu_site.mjs + assets/nhip-chu-site-copy.json + tools/install_frame.py` |
| `docs/install-nhip-chu-claude.ja.html` | Generated guide | `tools/build_nhip_chu_site.mjs + assets/nhip-chu-site-copy.json + tools/install_frame.py` |
| `docs/install-nhip-chu-gemini.en.html` | Generated guide | `tools/build_nhip_chu_site.mjs + assets/nhip-chu-site-copy.json + tools/install_frame.py` |
| `docs/install-nhip-chu-gemini.html` | Generated guide | `tools/build_nhip_chu_site.mjs + assets/nhip-chu-site-copy.json + tools/install_frame.py` |
| `docs/install-nhip-chu-gemini.ja.html` | Generated guide | `tools/build_nhip_chu_site.mjs + assets/nhip-chu-site-copy.json + tools/install_frame.py` |
| `docs/install-satzbild-chatgpt.en.html` | Generated guide | `tools/build_satzbild_site.py + tools/install_frame.py` |
| `docs/install-satzbild-chatgpt.html` | Generated guide | `tools/build_satzbild_site.py + tools/install_frame.py` |
| `docs/install-satzbild-chatgpt.ja.html` | Generated guide | `tools/build_satzbild_site.py + tools/install_frame.py` |
| `docs/install-satzbild-claude.en.html` | Generated guide | `tools/build_satzbild_site.py + tools/install_frame.py` |
| `docs/install-satzbild-claude.html` | Generated guide | `tools/build_satzbild_site.py + tools/install_frame.py` |
| `docs/install-satzbild-claude.ja.html` | Generated guide | `tools/build_satzbild_site.py + tools/install_frame.py` |
| `docs/install-satzbild-gemini.en.html` | Generated guide | `tools/build_satzbild_site.py + tools/install_frame.py` |
| `docs/install-satzbild-gemini.html` | Generated guide | `tools/build_satzbild_site.py + tools/install_frame.py` |
| `docs/install-satzbild-gemini.ja.html` | Generated guide | `tools/build_satzbild_site.py + tools/install_frame.py` |
| `docs/install-szyk-chatgpt.en.html` | Generated guide | `tools/build_szyk_site.py + tools/install_frame.py` |
| `docs/install-szyk-chatgpt.html` | Generated guide | `tools/build_szyk_site.py + tools/install_frame.py` |
| `docs/install-szyk-chatgpt.ja.html` | Generated guide | `tools/build_szyk_site.py + tools/install_frame.py` |
| `docs/install-szyk-claude.en.html` | Generated guide | `tools/build_szyk_site.py + tools/install_frame.py` |
| `docs/install-szyk-claude.html` | Generated guide | `tools/build_szyk_site.py + tools/install_frame.py` |
| `docs/install-szyk-claude.ja.html` | Generated guide | `tools/build_szyk_site.py + tools/install_frame.py` |
| `docs/install-szyk-gemini.en.html` | Generated guide | `tools/build_szyk_site.py + tools/install_frame.py` |
| `docs/install-szyk-gemini.html` | Generated guide | `tools/build_szyk_site.py + tools/install_frame.py` |
| `docs/install-szyk-gemini.ja.html` | Generated guide | `tools/build_szyk_site.py + tools/install_frame.py` |
| `docs/install-ziheng-claude.en.html` | Generated guide | `tools/build_ziheng_site.py + tools/install_frame.py` |
| `docs/install-ziheng-claude.html` | Generated guide | `tools/build_ziheng_site.py + tools/install_frame.py` |
| `docs/install-ziheng-claude.ja.html` | Generated guide | `tools/build_ziheng_site.py + tools/install_frame.py` |
| `docs/install-ziheng-gemini.en.html` | Generated guide | `tools/build_ziheng_site.py + tools/install_frame.py` |
| `docs/install-ziheng-gemini.html` | Generated guide | `tools/build_ziheng_site.py + tools/install_frame.py` |
| `docs/install-ziheng-gemini.ja.html` | Generated guide | `tools/build_ziheng_site.py + tools/install_frame.py` |
| `docs/install-ziheng.en.html` | Generated guide | `tools/build_ziheng_site.py + tools/install_frame.py` |
| `docs/install-ziheng.html` | Generated guide | `tools/build_ziheng_site.py + tools/install_frame.py` |
| `docs/install-ziheng.ja.html` | Generated guide | `tools/build_ziheng_site.py + tools/install_frame.py` |
| `docs/install-zilu-chatgpt.en.html` | Generated guide | `tools/build_zilu_site.py + templates/zilu-*-landing.html + tools/install_frame.py` |
| `docs/install-zilu-chatgpt.html` | Generated guide | `tools/build_zilu_site.py + templates/zilu-*-landing.html + tools/install_frame.py` |
| `docs/install-zilu-chatgpt.ja.html` | Generated guide | `tools/build_zilu_site.py + templates/zilu-*-landing.html + tools/install_frame.py` |
| `docs/install-zilu-claude.en.html` | Generated guide | `tools/build_zilu_site.py + templates/zilu-*-landing.html + tools/install_frame.py` |
| `docs/install-zilu-claude.html` | Generated guide | `tools/build_zilu_site.py + templates/zilu-*-landing.html + tools/install_frame.py` |
| `docs/install-zilu-claude.ja.html` | Generated guide | `tools/build_zilu_site.py + templates/zilu-*-landing.html + tools/install_frame.py` |
| `docs/install-zilu-gemini.en.html` | Generated guide | `tools/build_zilu_site.py + templates/zilu-*-landing.html + tools/install_frame.py` |
| `docs/install-zilu-gemini.html` | Generated guide | `tools/build_zilu_site.py + templates/zilu-*-landing.html + tools/install_frame.py` |
| `docs/install-zilu-gemini.ja.html` | Generated guide | `tools/build_zilu_site.py + templates/zilu-*-landing.html + tools/install_frame.py` |
| `en.html` | Jekyll landing | `en.html frontmatter/body → _layouts/landing.html` |
| `index.html` | Gateway | `tools/build_gateways.py + assets/gateway-copy.json` |
| `kumihan-ar.en.html` | Generated landing | `tools/build_ar_site.py` |
| `kumihan-ar.html` | Generated landing | `tools/build_ar_site.py` |
| `kumihan-ar.ja.html` | Generated landing | `tools/build_ar_site.py` |
| `kumihan-bn.en.html` | Authored Bangla | `kumihan-bn.en.html (authored body/head copy; shared build_seo adapter)` |
| `kumihan-bn.html` | Authored Bangla | `kumihan-bn.html (authored body/head copy; shared build_seo adapter)` |
| `kumihan-bn.ja.html` | Authored Bangla | `kumihan-bn.ja.html (authored body/head copy; shared build_seo adapter)` |
| `kumihan-de.en.html` | Generated landing | `tools/build_satzbild_site.py` |
| `kumihan-de.html` | Generated landing | `tools/build_satzbild_site.py` |
| `kumihan-de.ja.html` | Generated landing | `tools/build_satzbild_site.py` |
| `kumihan-es.en.html` | Generated landing | `tools/build_grafia_site.py` |
| `kumihan-es.html` | Generated landing | `tools/build_grafia_site.py` |
| `kumihan-es.ja.html` | Generated landing | `tools/build_grafia_site.py` |
| `kumihan-fr.en.html` | Generated landing | `tools/build_accord_site.py` |
| `kumihan-fr.html` | Generated landing | `tools/build_accord_site.py` |
| `kumihan-fr.ja.html` | Generated landing | `tools/build_accord_site.py` |
| `kumihan-hi.en.html` | Generated landing | `tools/build_hi_site.py` |
| `kumihan-hi.html` | Generated landing | `tools/build_hi_site.py` |
| `kumihan-hi.ja.html` | Generated landing | `tools/build_hi_site.py` |
| `kumihan-id.en.html` | Generated landing | `tools/build_laras_site.py` |
| `kumihan-id.html` | Generated landing | `tools/build_laras_site.py` |
| `kumihan-id.ja.html` | Generated landing | `tools/build_laras_site.py` |
| `kumihan-it.en.html` | Generated landing | `tools/build_equilibrio_site.py` |
| `kumihan-it.html` | Generated landing | `tools/build_equilibrio_site.py` |
| `kumihan-it.ja.html` | Generated landing | `tools/build_equilibrio_site.py` |
| `kumihan-ko.en.html` | Jekyll Korean | `kumihan-ko.en.html frontmatter/body → _layouts/geuljjaim-index.html` |
| `kumihan-ko.html` | Jekyll Korean | `kumihan-ko.html frontmatter/body → _layouts/geuljjaim-index.html` |
| `kumihan-ko.ja.html` | Jekyll Korean | `kumihan-ko.ja.html frontmatter/body → _layouts/geuljjaim-index.html` |
| `kumihan-pl.en.html` | Generated landing | `tools/build_szyk_site.py` |
| `kumihan-pl.html` | Generated landing | `tools/build_szyk_site.py` |
| `kumihan-pl.ja.html` | Generated landing | `tools/build_szyk_site.py` |
| `kumihan-pt.en.html` | Generated landing | `tools/build_compasso_site.py` |
| `kumihan-pt.html` | Generated landing | `tools/build_compasso_site.py` |
| `kumihan-pt.ja.html` | Generated landing | `tools/build_compasso_site.py` |
| `kumihan-ru.en.html` | Generated landing | `tools/build_lad_site.py` |
| `kumihan-ru.html` | Generated landing | `tools/build_lad_site.py` |
| `kumihan-ru.ja.html` | Generated landing | `tools/build_lad_site.py` |
| `kumihan-sw.en.html` | Generated landing | `tools/build_mizani_site.py` |
| `kumihan-sw.html` | Generated landing | `tools/build_mizani_site.py` |
| `kumihan-sw.ja.html` | Generated landing | `tools/build_mizani_site.py` |
| `kumihan-th-en.html` | Generated landing | `tools/build_th_site.py` |
| `kumihan-th-ja.html` | Generated landing | `tools/build_th_site.py` |
| `kumihan-th.html` | Generated landing | `tools/build_th_site.py` |
| `kumihan-vi.en.html` | Generated landing | `tools/build_nhip_chu_site.mjs + assets/nhip-chu-site-copy.json` |
| `kumihan-vi.html` | Generated landing | `tools/build_nhip_chu_site.mjs + assets/nhip-chu-site-copy.json` |
| `kumihan-vi.ja.html` | Generated landing | `tools/build_nhip_chu_site.mjs + assets/nhip-chu-site-copy.json` |
| `kumihan-zh-cn.en.html` | Generated landing | `tools/build_zilu_site.py + templates/zilu-*-landing.html` |
| `kumihan-zh-cn.html` | Generated landing | `tools/build_zilu_site.py + templates/zilu-*-landing.html` |
| `kumihan-zh-cn.ja.html` | Generated landing | `tools/build_zilu_site.py + templates/zilu-*-landing.html` |
| `kumihan-zh-han.en.html` | Generated landing | `tools/build_ziheng_site.py` |
| `kumihan-zh-han.html` | Generated landing | `tools/build_ziheng_site.py` |
| `kumihan-zh-han.ja.html` | Generated landing | `tools/build_ziheng_site.py` |
| `kumihan.html` | Jekyll landing | `kumihan.html frontmatter/body → _layouts/landing.html` |
| `top-ar.html` | Gateway | `tools/build_gateways.py + assets/gateway-copy.json` |
| `top-bn.html` | Gateway | `tools/build_gateways.py + assets/gateway-copy.json` |
| `top-de.html` | Gateway | `tools/build_gateways.py + assets/gateway-copy.json` |
| `top-en.html` | Gateway | `tools/build_gateways.py + assets/gateway-copy.json` |
| `top-es.html` | Gateway | `tools/build_gateways.py + assets/gateway-copy.json` |
| `top-fr.html` | Gateway | `tools/build_gateways.py + assets/gateway-copy.json` |
| `top-hi.html` | Gateway | `tools/build_gateways.py + assets/gateway-copy.json` |
| `top-id.html` | Gateway | `tools/build_gateways.py + assets/gateway-copy.json` |
| `top-it.html` | Gateway | `tools/build_gateways.py + assets/gateway-copy.json` |
| `top-ko.html` | Gateway | `tools/build_gateways.py + assets/gateway-copy.json` |
| `top-pl.html` | Gateway | `tools/build_gateways.py + assets/gateway-copy.json` |
| `top-pt.html` | Gateway | `tools/build_gateways.py + assets/gateway-copy.json` |
| `top-ru.html` | Gateway | `tools/build_gateways.py + assets/gateway-copy.json` |
| `top-th.html` | Gateway | `tools/build_gateways.py + assets/gateway-copy.json` |
| `top-vi.html` | Gateway | `tools/build_gateways.py + assets/gateway-copy.json` |
| `top-zh-cn.html` | Gateway | `tools/build_gateways.py + assets/gateway-copy.json` |
| `top-zh-han.html` | Gateway | `tools/build_gateways.py + assets/gateway-copy.json` |
| `zh-tw.html` | Jekyll landing | `zh-tw.html frontmatter/body → _layouts/landing.html` |

## 公開探索から除外するもの

- `_layouts/*.html`、`_includes/` はJekyll入力であり独立URLではない。
- `templates/zilu-*-landing.html` は生成元。コピーやSEOを更新後、字律ビルダーでrootへ生成する。
- `tests/`（`tests/seo/fixtures/test-fixture-new-language` を含む）は非公開fixture。公開root/docs探索へ混ぜない。
- `plugins/`、`skills/`、`downloads*`、配布ZIP・manifest・versionは配布実体。サイトLPではなく本作業で保護する。
- `docs/**/*.md` はこのHTML基盤の探索対象外（導入本文はJekyllのHTMLからincludeされる）。Markdown文書に自動でLP用SEOを付与しない。
- `noindex`、外部canonical、redirect/aliasはサイトマップに登録しない。欠落canonicalや衝突を暗黙除外で隠さず検証エラーにする。

## 競合作業のFresh Read

- SNS仕様ブランチ `feature/sns-share-spec-20261019` をfetchし、`4147a9a9e7bf6a497a0df9b7c299a513a68869e8` の `docs/specs/KUMIHAN_SNS_SHARE_IMPLEMENTATION_SPEC_20261019.md` を実読。SNS側は公開canonical/OGPを消費し、SEO側を正本とする。SNS UIや投稿APIは本PRで追加しない。
- [PR #92](https://github.com/landco-llc/kumihan/pull/92) open、head `1c931aaa47e6af9d6a9b6f7c7b2d1123a4e1bd4b`。gateway CSS版付きURL/menu scroll変更が `tools/build_gateways.py` と18生成HTMLで重なる。main取込み時に生成器の両変更を保持し再生成する。CSS修正をSEO目的で先取りしない。
- [PR #91](https://github.com/landco-llc/kumihan/pull/91) Mizani mergedが最新main基点に含まれる。[PR #87](https://github.com/landco-llc/kumihan/pull/87) MCP RFC openは配布設計側で本SEO実装と独立。
- PR状態はW00読取時点。最終PR作成時の差分・CIとmain追従確認は検証ログに追記する。

## 保護確認

比較基準は作業ブランチ開始時の古いmainではなく上記最新 `origin/main`。`git diff origin/main -- plugins skills '*.zip'` および配布先manifest/versionを確認し、サイトの生成元・HTML以外への意図しない変更を排除する。配布を再生成する `tools/build_dist.py` / `scripts/build_bn_release.py` / `tools/build_*` のpackage builderはSEO生成コマンドから呼ばない。確認結果は検証ログを正本とする。

Legacy ZiHeng guide source→output: `templates/ziheng/docs/install-ziheng*.html` → `tools/build_ziheng_site.py` → matching `docs/` path (9 pages). New public directories are recursively discovered; see ADR-SEO-012.
