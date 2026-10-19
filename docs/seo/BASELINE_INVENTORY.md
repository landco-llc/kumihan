# SEO inventory — reconciled 2026-10-19 JST

Main baseline: `05c60fd5d519a3a6d38feb616f60fddd373b635f` (PR #100/#102/#103/#104 merged; #101 Draft/unmerged).
Original integration: `fa9451a`, Jekyll review fixes: `d395e14`; current privacy/footer main05c60fd safely integrated. Historical 231-page inventory is superseded; recover it from Git history if needed.

Actual source audit: **274 HTML files, 273 indexable canonical URLs**. 22 gateways + 63 product landings + 186 guides + 2 privacy policies = 273; the additional `top-en.html` is an explicit noindex/meta-refresh alias. No external canonical exclusions. Jekyll supplies 21 of these contracts; source simulation is not evidence of actual rendering.
English `index.html` canonical is the project root; Japanese top is `top-ja.html`. 22 gateway language alternates + x-default; product translation groups remain separate. All URL paths and indexability are in [machine inventory](evidence/20261019-current-inventory.json).

257 main static/layout body suffixes, 21 Jekyll frontmatter/body sources and 2609 distribution/skill/manifest/readme files are SHA256 protected by [baseline snapshot](evidence/20261019-main-preservation.json), checked by `python tools/check_seo_preservation.py`.

| Public file | Language | Indexable | Source → output |
| --- | --- | --- | --- |
| `docs/install-accord-chatgpt.en.html` | en | yes | `tools/build_accord_site.py` |
| `docs/install-accord-chatgpt.html` | fr | yes | `tools/build_accord_site.py` |
| `docs/install-accord-chatgpt.ja.html` | ja | yes | `tools/build_accord_site.py` |
| `docs/install-accord-claude.en.html` | en | yes | `tools/build_accord_site.py` |
| `docs/install-accord-claude.html` | fr | yes | `tools/build_accord_site.py` |
| `docs/install-accord-claude.ja.html` | ja | yes | `tools/build_accord_site.py` |
| `docs/install-accord-gemini.en.html` | en | yes | `tools/build_accord_site.py` |
| `docs/install-accord-gemini.html` | fr | yes | `tools/build_accord_site.py` |
| `docs/install-accord-gemini.ja.html` | ja | yes | `tools/build_accord_site.py` |
| `docs/install-chatgpt.html` | ja | yes | `Jekyll frontmatter + _layouts + tools/build_jekyll_seo.py + _includes/share.html` |
| `docs/install-chatgpt.zh-tw.html` | zh-Hant-TW | yes | `Jekyll frontmatter + _layouts + tools/build_jekyll_seo.py + _includes/share.html` |
| `docs/install-claude.html` | ja | yes | `Jekyll frontmatter + _layouts + tools/build_jekyll_seo.py + _includes/share.html` |
| `docs/install-claude.zh-tw.html` | zh-Hant-TW | yes | `Jekyll frontmatter + _layouts + tools/build_jekyll_seo.py + _includes/share.html` |
| `docs/install-compasso-chatgpt.en.html` | en | yes | `tools/build_compasso_site.py` |
| `docs/install-compasso-chatgpt.html` | pt | yes | `tools/build_compasso_site.py` |
| `docs/install-compasso-chatgpt.ja.html` | ja | yes | `tools/build_compasso_site.py` |
| `docs/install-compasso-claude.en.html` | en | yes | `tools/build_compasso_site.py` |
| `docs/install-compasso-claude.html` | pt | yes | `tools/build_compasso_site.py` |
| `docs/install-compasso-claude.ja.html` | ja | yes | `tools/build_compasso_site.py` |
| `docs/install-compasso-gemini.en.html` | en | yes | `tools/build_compasso_site.py` |
| `docs/install-compasso-gemini.html` | pt | yes | `tools/build_compasso_site.py` |
| `docs/install-compasso-gemini.ja.html` | ja | yes | `tools/build_compasso_site.py` |
| `docs/install-equilibrio-chatgpt.en.html` | en | yes | `tools/build_equilibrio_site.py` |
| `docs/install-equilibrio-chatgpt.html` | it | yes | `tools/build_equilibrio_site.py` |
| `docs/install-equilibrio-chatgpt.ja.html` | ja | yes | `tools/build_equilibrio_site.py` |
| `docs/install-equilibrio-claude.en.html` | en | yes | `tools/build_equilibrio_site.py` |
| `docs/install-equilibrio-claude.html` | it | yes | `tools/build_equilibrio_site.py` |
| `docs/install-equilibrio-claude.ja.html` | ja | yes | `tools/build_equilibrio_site.py` |
| `docs/install-equilibrio-gemini.en.html` | en | yes | `tools/build_equilibrio_site.py` |
| `docs/install-equilibrio-gemini.html` | it | yes | `tools/build_equilibrio_site.py` |
| `docs/install-equilibrio-gemini.ja.html` | ja | yes | `tools/build_equilibrio_site.py` |
| `docs/install-gemini.html` | ja | yes | `Jekyll frontmatter + _layouts + tools/build_jekyll_seo.py + _includes/share.html` |
| `docs/install-gemini.zh-tw.html` | zh-Hant-TW | yes | `Jekyll frontmatter + _layouts + tools/build_jekyll_seo.py + _includes/share.html` |
| `docs/install-grafia-chatgpt.en.html` | en | yes | `tools/build_grafia_site.py` |
| `docs/install-grafia-chatgpt.html` | es | yes | `tools/build_grafia_site.py` |
| `docs/install-grafia-chatgpt.ja.html` | ja | yes | `tools/build_grafia_site.py` |
| `docs/install-grafia-claude.en.html` | en | yes | `tools/build_grafia_site.py` |
| `docs/install-grafia-claude.html` | es | yes | `tools/build_grafia_site.py` |
| `docs/install-grafia-claude.ja.html` | ja | yes | `tools/build_grafia_site.py` |
| `docs/install-grafia-gemini.en.html` | en | yes | `tools/build_grafia_site.py` |
| `docs/install-grafia-gemini.html` | es | yes | `tools/build_grafia_site.py` |
| `docs/install-grafia-gemini.ja.html` | ja | yes | `tools/build_grafia_site.py` |
| `docs/install-hlela-chatgpt.en.html` | en | yes | `tools/build_hlela_site.py` |
| `docs/install-hlela-chatgpt.html` | zu | yes | `tools/build_hlela_site.py` |
| `docs/install-hlela-chatgpt.ja.html` | ja | yes | `tools/build_hlela_site.py` |
| `docs/install-hlela-claude.en.html` | en | yes | `tools/build_hlela_site.py` |
| `docs/install-hlela-claude.html` | zu | yes | `tools/build_hlela_site.py` |
| `docs/install-hlela-claude.ja.html` | ja | yes | `tools/build_hlela_site.py` |
| `docs/install-hlela-gemini.en.html` | en | yes | `tools/build_hlela_site.py` |
| `docs/install-hlela-gemini.html` | zu | yes | `tools/build_hlela_site.py` |
| `docs/install-hlela-gemini.ja.html` | ja | yes | `tools/build_hlela_site.py` |
| `docs/install-ko-chatgpt.en.html` | en | yes | `Jekyll frontmatter + _layouts + tools/build_jekyll_seo.py + _includes/share.html` |
| `docs/install-ko-chatgpt.html` | ko-KR | yes | `Jekyll frontmatter + _layouts + tools/build_jekyll_seo.py + _includes/share.html` |
| `docs/install-ko-chatgpt.ja.html` | ja | yes | `Jekyll frontmatter + _layouts + tools/build_jekyll_seo.py + _includes/share.html` |
| `docs/install-ko-claude.en.html` | en | yes | `Jekyll frontmatter + _layouts + tools/build_jekyll_seo.py + _includes/share.html` |
| `docs/install-ko-claude.html` | ko-KR | yes | `Jekyll frontmatter + _layouts + tools/build_jekyll_seo.py + _includes/share.html` |
| `docs/install-ko-claude.ja.html` | ja | yes | `Jekyll frontmatter + _layouts + tools/build_jekyll_seo.py + _includes/share.html` |
| `docs/install-ko-gemini.en.html` | en | yes | `Jekyll frontmatter + _layouts + tools/build_jekyll_seo.py + _includes/share.html` |
| `docs/install-ko-gemini.html` | ko-KR | yes | `Jekyll frontmatter + _layouts + tools/build_jekyll_seo.py + _includes/share.html` |
| `docs/install-ko-gemini.ja.html` | ja | yes | `Jekyll frontmatter + _layouts + tools/build_jekyll_seo.py + _includes/share.html` |
| `docs/install-kumihan-ar-chatgpt.en.html` | en | yes | `tools/build_ar_site.py` |
| `docs/install-kumihan-ar-chatgpt.html` | ar | yes | `tools/build_ar_site.py` |
| `docs/install-kumihan-ar-chatgpt.ja.html` | ja | yes | `tools/build_ar_site.py` |
| `docs/install-kumihan-ar-claude.en.html` | en | yes | `tools/build_ar_site.py` |
| `docs/install-kumihan-ar-claude.html` | ar | yes | `tools/build_ar_site.py` |
| `docs/install-kumihan-ar-claude.ja.html` | ja | yes | `tools/build_ar_site.py` |
| `docs/install-kumihan-ar-gemini.en.html` | en | yes | `tools/build_ar_site.py` |
| `docs/install-kumihan-ar-gemini.html` | ar | yes | `tools/build_ar_site.py` |
| `docs/install-kumihan-ar-gemini.ja.html` | ja | yes | `tools/build_ar_site.py` |
| `docs/install-kumihan-bn-chatgpt.en.html` | en | yes | `tools/build_bn_site.py` |
| `docs/install-kumihan-bn-chatgpt.html` | bn | yes | `tools/build_bn_site.py` |
| `docs/install-kumihan-bn-chatgpt.ja.html` | ja | yes | `tools/build_bn_site.py` |
| `docs/install-kumihan-bn-claude.en.html` | en | yes | `tools/build_bn_site.py` |
| `docs/install-kumihan-bn-claude.html` | bn | yes | `tools/build_bn_site.py` |
| `docs/install-kumihan-bn-claude.ja.html` | ja | yes | `tools/build_bn_site.py` |
| `docs/install-kumihan-bn-gemini.en.html` | en | yes | `tools/build_bn_site.py` |
| `docs/install-kumihan-bn-gemini.html` | bn | yes | `tools/build_bn_site.py` |
| `docs/install-kumihan-bn-gemini.ja.html` | ja | yes | `tools/build_bn_site.py` |
| `docs/install-kumihan-fa-chatgpt.en.html` | en | yes | `tools/build_fa_site.py` |
| `docs/install-kumihan-fa-chatgpt.html` | fa | yes | `tools/build_fa_site.py` |
| `docs/install-kumihan-fa-chatgpt.ja.html` | ja | yes | `tools/build_fa_site.py` |
| `docs/install-kumihan-fa-claude.en.html` | en | yes | `tools/build_fa_site.py` |
| `docs/install-kumihan-fa-claude.html` | fa | yes | `tools/build_fa_site.py` |
| `docs/install-kumihan-fa-claude.ja.html` | ja | yes | `tools/build_fa_site.py` |
| `docs/install-kumihan-fa-gemini.en.html` | en | yes | `tools/build_fa_site.py` |
| `docs/install-kumihan-fa-gemini.html` | fa | yes | `tools/build_fa_site.py` |
| `docs/install-kumihan-fa-gemini.ja.html` | ja | yes | `tools/build_fa_site.py` |
| `docs/install-kumihan-hi-chatgpt.en.html` | en | yes | `tools/build_hi_site.py` |
| `docs/install-kumihan-hi-chatgpt.html` | hi | yes | `tools/build_hi_site.py` |
| `docs/install-kumihan-hi-chatgpt.ja.html` | ja | yes | `tools/build_hi_site.py` |
| `docs/install-kumihan-hi-claude.en.html` | en | yes | `tools/build_hi_site.py` |
| `docs/install-kumihan-hi-claude.html` | hi | yes | `tools/build_hi_site.py` |
| `docs/install-kumihan-hi-claude.ja.html` | ja | yes | `tools/build_hi_site.py` |
| `docs/install-kumihan-hi-gemini.en.html` | en | yes | `tools/build_hi_site.py` |
| `docs/install-kumihan-hi-gemini.html` | hi | yes | `tools/build_hi_site.py` |
| `docs/install-kumihan-hi-gemini.ja.html` | ja | yes | `tools/build_hi_site.py` |
| `docs/install-kumihan-th-chatgpt.en.html` | en | yes | `tools/build_th_site.py + tools/build_th_*_index.py` |
| `docs/install-kumihan-th-chatgpt.html` | th | yes | `tools/build_th_site.py + tools/build_th_*_index.py` |
| `docs/install-kumihan-th-chatgpt.ja.html` | ja | yes | `tools/build_th_site.py + tools/build_th_*_index.py` |
| `docs/install-kumihan-th-claude.en.html` | en | yes | `tools/build_th_site.py + tools/build_th_*_index.py` |
| `docs/install-kumihan-th-claude.html` | th | yes | `tools/build_th_site.py + tools/build_th_*_index.py` |
| `docs/install-kumihan-th-claude.ja.html` | ja | yes | `tools/build_th_site.py + tools/build_th_*_index.py` |
| `docs/install-kumihan-th-gemini.en.html` | en | yes | `tools/build_th_site.py + tools/build_th_*_index.py` |
| `docs/install-kumihan-th-gemini.html` | th | yes | `tools/build_th_site.py + tools/build_th_*_index.py` |
| `docs/install-kumihan-th-gemini.ja.html` | ja | yes | `tools/build_th_site.py + tools/build_th_*_index.py` |
| `docs/install-lad-chatgpt.en.html` | en | yes | `tools/build_lad_site.py` |
| `docs/install-lad-chatgpt.html` | ru | yes | `tools/build_lad_site.py` |
| `docs/install-lad-chatgpt.ja.html` | ja | yes | `tools/build_lad_site.py` |
| `docs/install-lad-claude.en.html` | en | yes | `tools/build_lad_site.py` |
| `docs/install-lad-claude.html` | ru | yes | `tools/build_lad_site.py` |
| `docs/install-lad-claude.ja.html` | ja | yes | `tools/build_lad_site.py` |
| `docs/install-lad-gemini.en.html` | en | yes | `tools/build_lad_site.py` |
| `docs/install-lad-gemini.html` | ru | yes | `tools/build_lad_site.py` |
| `docs/install-lad-gemini.ja.html` | ja | yes | `tools/build_lad_site.py` |
| `docs/install-laras-chatgpt.en.html` | en | yes | `tools/build_laras_site.py` |
| `docs/install-laras-chatgpt.html` | id | yes | `tools/build_laras_site.py` |
| `docs/install-laras-chatgpt.ja.html` | ja | yes | `tools/build_laras_site.py` |
| `docs/install-laras-claude.en.html` | en | yes | `tools/build_laras_site.py` |
| `docs/install-laras-claude.html` | id | yes | `tools/build_laras_site.py` |
| `docs/install-laras-claude.ja.html` | ja | yes | `tools/build_laras_site.py` |
| `docs/install-laras-gemini.en.html` | en | yes | `tools/build_laras_site.py` |
| `docs/install-laras-gemini.html` | id | yes | `tools/build_laras_site.py` |
| `docs/install-laras-gemini.ja.html` | ja | yes | `tools/build_laras_site.py` |
| `docs/install-lumnung-chatgpt.en.html` | en | yes | `tools/build_lumnung_site.py` |
| `docs/install-lumnung-chatgpt.html` | km | yes | `tools/build_lumnung_site.py` |
| `docs/install-lumnung-chatgpt.ja.html` | ja | yes | `tools/build_lumnung_site.py` |
| `docs/install-lumnung-claude.en.html` | en | yes | `tools/build_lumnung_site.py` |
| `docs/install-lumnung-claude.html` | km | yes | `tools/build_lumnung_site.py` |
| `docs/install-lumnung-claude.ja.html` | ja | yes | `tools/build_lumnung_site.py` |
| `docs/install-lumnung-gemini.en.html` | en | yes | `tools/build_lumnung_site.py` |
| `docs/install-lumnung-gemini.html` | km | yes | `tools/build_lumnung_site.py` |
| `docs/install-lumnung-gemini.ja.html` | ja | yes | `tools/build_lumnung_site.py` |
| `docs/install-mizani-chatgpt.en.html` | en | yes | `tools/build_mizani_site.py` |
| `docs/install-mizani-chatgpt.html` | sw | yes | `tools/build_mizani_site.py` |
| `docs/install-mizani-chatgpt.ja.html` | ja | yes | `tools/build_mizani_site.py` |
| `docs/install-mizani-claude.en.html` | en | yes | `tools/build_mizani_site.py` |
| `docs/install-mizani-claude.html` | sw | yes | `tools/build_mizani_site.py` |
| `docs/install-mizani-claude.ja.html` | ja | yes | `tools/build_mizani_site.py` |
| `docs/install-mizani-gemini.en.html` | en | yes | `tools/build_mizani_site.py` |
| `docs/install-mizani-gemini.html` | sw | yes | `tools/build_mizani_site.py` |
| `docs/install-mizani-gemini.ja.html` | ja | yes | `tools/build_mizani_site.py` |
| `docs/install-nhip-chu-chatgpt.en.html` | en | yes | `tools/build_nhip_chu_site.mjs + tools/seo_metadata.py` |
| `docs/install-nhip-chu-chatgpt.html` | vi | yes | `tools/build_nhip_chu_site.mjs + tools/seo_metadata.py` |
| `docs/install-nhip-chu-chatgpt.ja.html` | ja | yes | `tools/build_nhip_chu_site.mjs + tools/seo_metadata.py` |
| `docs/install-nhip-chu-claude.en.html` | en | yes | `tools/build_nhip_chu_site.mjs + tools/seo_metadata.py` |
| `docs/install-nhip-chu-claude.html` | vi | yes | `tools/build_nhip_chu_site.mjs + tools/seo_metadata.py` |
| `docs/install-nhip-chu-claude.ja.html` | ja | yes | `tools/build_nhip_chu_site.mjs + tools/seo_metadata.py` |
| `docs/install-nhip-chu-gemini.en.html` | en | yes | `tools/build_nhip_chu_site.mjs + tools/seo_metadata.py` |
| `docs/install-nhip-chu-gemini.html` | vi | yes | `tools/build_nhip_chu_site.mjs + tools/seo_metadata.py` |
| `docs/install-nhip-chu-gemini.ja.html` | ja | yes | `tools/build_nhip_chu_site.mjs + tools/seo_metadata.py` |
| `docs/install-satzbild-chatgpt.en.html` | en | yes | `tools/build_satzbild_site.py` |
| `docs/install-satzbild-chatgpt.html` | de | yes | `tools/build_satzbild_site.py` |
| `docs/install-satzbild-chatgpt.ja.html` | ja | yes | `tools/build_satzbild_site.py` |
| `docs/install-satzbild-claude.en.html` | en | yes | `tools/build_satzbild_site.py` |
| `docs/install-satzbild-claude.html` | de | yes | `tools/build_satzbild_site.py` |
| `docs/install-satzbild-claude.ja.html` | ja | yes | `tools/build_satzbild_site.py` |
| `docs/install-satzbild-gemini.en.html` | en | yes | `tools/build_satzbild_site.py` |
| `docs/install-satzbild-gemini.html` | de | yes | `tools/build_satzbild_site.py` |
| `docs/install-satzbild-gemini.ja.html` | ja | yes | `tools/build_satzbild_site.py` |
| `docs/install-szyk-chatgpt.en.html` | en | yes | `tools/build_szyk_site.py` |
| `docs/install-szyk-chatgpt.html` | pl | yes | `tools/build_szyk_site.py` |
| `docs/install-szyk-chatgpt.ja.html` | ja | yes | `tools/build_szyk_site.py` |
| `docs/install-szyk-claude.en.html` | en | yes | `tools/build_szyk_site.py` |
| `docs/install-szyk-claude.html` | pl | yes | `tools/build_szyk_site.py` |
| `docs/install-szyk-claude.ja.html` | ja | yes | `tools/build_szyk_site.py` |
| `docs/install-szyk-gemini.en.html` | en | yes | `tools/build_szyk_site.py` |
| `docs/install-szyk-gemini.html` | pl | yes | `tools/build_szyk_site.py` |
| `docs/install-szyk-gemini.ja.html` | ja | yes | `tools/build_szyk_site.py` |
| `docs/install-ziheng-claude.en.html` | en | yes | `tools/build_ziheng_site.py` |
| `docs/install-ziheng-claude.html` | zh-Hant-TW | yes | `tools/build_ziheng_site.py` |
| `docs/install-ziheng-claude.ja.html` | ja | yes | `tools/build_ziheng_site.py` |
| `docs/install-ziheng-gemini.en.html` | en | yes | `tools/build_ziheng_site.py` |
| `docs/install-ziheng-gemini.html` | zh-Hant-TW | yes | `tools/build_ziheng_site.py` |
| `docs/install-ziheng-gemini.ja.html` | ja | yes | `tools/build_ziheng_site.py` |
| `docs/install-ziheng.en.html` | en | yes | `tools/build_ziheng_site.py` |
| `docs/install-ziheng.html` | zh-Hant-TW | yes | `tools/build_ziheng_site.py` |
| `docs/install-ziheng.ja.html` | ja | yes | `tools/build_ziheng_site.py` |
| `docs/install-zilu-chatgpt.en.html` | en | yes | `tools/build_zilu_site.py` |
| `docs/install-zilu-chatgpt.html` | zh-Hans-CN | yes | `tools/build_zilu_site.py` |
| `docs/install-zilu-chatgpt.ja.html` | ja | yes | `tools/build_zilu_site.py` |
| `docs/install-zilu-claude.en.html` | en | yes | `tools/build_zilu_site.py` |
| `docs/install-zilu-claude.html` | zh-Hans-CN | yes | `tools/build_zilu_site.py` |
| `docs/install-zilu-claude.ja.html` | ja | yes | `tools/build_zilu_site.py` |
| `docs/install-zilu-gemini.en.html` | en | yes | `tools/build_zilu_site.py` |
| `docs/install-zilu-gemini.html` | zh-Hans-CN | yes | `tools/build_zilu_site.py` |
| `docs/install-zilu-gemini.ja.html` | ja | yes | `tools/build_zilu_site.py` |
| `en.html` | en | yes | `Jekyll frontmatter + _layouts + tools/build_jekyll_seo.py + _includes/share.html` |
| `index.html` | en | yes | `tools/build_gateways.py + assets/gateway-copy.json` |
| `kumihan-ar.en.html` | en | yes | `tools/build_ar_site.py` |
| `kumihan-ar.html` | ar | yes | `tools/build_ar_site.py` |
| `kumihan-ar.ja.html` | ja | yes | `tools/build_ar_site.py` |
| `kumihan-bn.en.html` | en | yes | `tools/build_bn_site.py` |
| `kumihan-bn.html` | bn | yes | `tools/build_bn_site.py` |
| `kumihan-bn.ja.html` | ja | yes | `tools/build_bn_site.py` |
| `kumihan-de.en.html` | en | yes | `tools/build_satzbild_site.py` |
| `kumihan-de.html` | de | yes | `tools/build_satzbild_site.py` |
| `kumihan-de.ja.html` | ja | yes | `tools/build_satzbild_site.py` |
| `kumihan-es.en.html` | en | yes | `tools/build_grafia_site.py` |
| `kumihan-es.html` | es | yes | `tools/build_grafia_site.py` |
| `kumihan-es.ja.html` | ja | yes | `tools/build_grafia_site.py` |
| `kumihan-fa.en.html` | en | yes | `tools/build_fa_site.py` |
| `kumihan-fa.html` | fa | yes | `tools/build_fa_site.py` |
| `kumihan-fa.ja.html` | ja | yes | `tools/build_fa_site.py` |
| `kumihan-fr.en.html` | en | yes | `tools/build_accord_site.py` |
| `kumihan-fr.html` | fr | yes | `tools/build_accord_site.py` |
| `kumihan-fr.ja.html` | ja | yes | `tools/build_accord_site.py` |
| `kumihan-hi.en.html` | en | yes | `tools/build_hi_site.py` |
| `kumihan-hi.html` | hi | yes | `tools/build_hi_site.py` |
| `kumihan-hi.ja.html` | ja | yes | `tools/build_hi_site.py` |
| `kumihan-id.en.html` | en | yes | `tools/build_laras_site.py` |
| `kumihan-id.html` | id | yes | `tools/build_laras_site.py` |
| `kumihan-id.ja.html` | ja | yes | `tools/build_laras_site.py` |
| `kumihan-it.en.html` | en | yes | `tools/build_equilibrio_site.py` |
| `kumihan-it.html` | it | yes | `tools/build_equilibrio_site.py` |
| `kumihan-it.ja.html` | ja | yes | `tools/build_equilibrio_site.py` |
| `kumihan-km.en.html` | en | yes | `tools/build_lumnung_site.py` |
| `kumihan-km.html` | km | yes | `tools/build_lumnung_site.py` |
| `kumihan-km.ja.html` | ja | yes | `tools/build_lumnung_site.py` |
| `kumihan-ko.en.html` | en | yes | `Jekyll frontmatter + _layouts + tools/build_jekyll_seo.py + _includes/share.html` |
| `kumihan-ko.html` | ko-KR | yes | `Jekyll frontmatter + _layouts + tools/build_jekyll_seo.py + _includes/share.html` |
| `kumihan-ko.ja.html` | ja | yes | `Jekyll frontmatter + _layouts + tools/build_jekyll_seo.py + _includes/share.html` |
| `kumihan-pl.en.html` | en | yes | `tools/build_szyk_site.py` |
| `kumihan-pl.html` | pl | yes | `tools/build_szyk_site.py` |
| `kumihan-pl.ja.html` | ja | yes | `tools/build_szyk_site.py` |
| `kumihan-pt.en.html` | en | yes | `tools/build_compasso_site.py` |
| `kumihan-pt.html` | pt | yes | `tools/build_compasso_site.py` |
| `kumihan-pt.ja.html` | ja | yes | `tools/build_compasso_site.py` |
| `kumihan-ru.en.html` | en | yes | `tools/build_lad_site.py` |
| `kumihan-ru.html` | ru | yes | `tools/build_lad_site.py` |
| `kumihan-ru.ja.html` | ja | yes | `tools/build_lad_site.py` |
| `kumihan-sw.en.html` | en | yes | `tools/build_mizani_site.py` |
| `kumihan-sw.html` | sw | yes | `tools/build_mizani_site.py` |
| `kumihan-sw.ja.html` | ja | yes | `tools/build_mizani_site.py` |
| `kumihan-th-en.html` | en | yes | `tools/build_th_site.py + tools/build_th_*_index.py` |
| `kumihan-th-ja.html` | ja | yes | `tools/build_th_site.py + tools/build_th_*_index.py` |
| `kumihan-th.html` | th | yes | `tools/build_th_site.py + tools/build_th_*_index.py` |
| `kumihan-vi.en.html` | en | yes | `tools/build_nhip_chu_site.mjs + tools/seo_metadata.py` |
| `kumihan-vi.html` | vi | yes | `tools/build_nhip_chu_site.mjs + tools/seo_metadata.py` |
| `kumihan-vi.ja.html` | ja | yes | `tools/build_nhip_chu_site.mjs + tools/seo_metadata.py` |
| `kumihan-zh-cn.en.html` | en | yes | `tools/build_zilu_site.py` |
| `kumihan-zh-cn.html` | zh-Hans-CN | yes | `tools/build_zilu_site.py` |
| `kumihan-zh-cn.ja.html` | ja | yes | `tools/build_zilu_site.py` |
| `kumihan-zh-han.en.html` | en | yes | `tools/build_ziheng_site.py` |
| `kumihan-zh-han.html` | zh-Hant-TW | yes | `tools/build_ziheng_site.py` |
| `kumihan-zh-han.ja.html` | ja | yes | `tools/build_ziheng_site.py` |
| `kumihan-zu.en.html` | en | yes | `tools/build_hlela_site.py` |
| `kumihan-zu.html` | zu | yes | `tools/build_hlela_site.py` |
| `kumihan-zu.ja.html` | ja | yes | `tools/build_hlela_site.py` |
| `kumihan.html` | ja | yes | `Jekyll frontmatter + _layouts + tools/build_jekyll_seo.py + _includes/share.html` |
| `privacy-ja.html` | ja | yes | `tools/build_privacy.py + assets/privacy-copy.json` |
| `privacy.html` | en | yes | `tools/build_privacy.py + assets/privacy-copy.json` |
| `top-ar.html` | ar | yes | `tools/build_gateways.py + assets/gateway-copy.json` |
| `top-bn.html` | bn | yes | `tools/build_gateways.py + assets/gateway-copy.json` |
| `top-de.html` | de | yes | `tools/build_gateways.py + assets/gateway-copy.json` |
| `top-en.html` | en | no: redirect | `tools/build_gateways.py + assets/gateway-copy.json` |
| `top-es.html` | es | yes | `tools/build_gateways.py + assets/gateway-copy.json` |
| `top-fa.html` | fa | yes | `tools/build_gateways.py + assets/gateway-copy.json` |
| `top-fr.html` | fr | yes | `tools/build_gateways.py + assets/gateway-copy.json` |
| `top-hi.html` | hi | yes | `tools/build_gateways.py + assets/gateway-copy.json` |
| `top-id.html` | id | yes | `tools/build_gateways.py + assets/gateway-copy.json` |
| `top-it.html` | it | yes | `tools/build_gateways.py + assets/gateway-copy.json` |
| `top-ja.html` | ja | yes | `tools/build_gateways.py + assets/gateway-copy.json` |
| `top-km.html` | km | yes | `tools/build_gateways.py + assets/gateway-copy.json` |
| `top-ko.html` | ko-KR | yes | `tools/build_gateways.py + assets/gateway-copy.json` |
| `top-pl.html` | pl | yes | `tools/build_gateways.py + assets/gateway-copy.json` |
| `top-pt.html` | pt | yes | `tools/build_gateways.py + assets/gateway-copy.json` |
| `top-ru.html` | ru | yes | `tools/build_gateways.py + assets/gateway-copy.json` |
| `top-sw.html` | sw | yes | `tools/build_gateways.py + assets/gateway-copy.json` |
| `top-th.html` | th-TH | yes | `tools/build_gateways.py + assets/gateway-copy.json` |
| `top-vi.html` | vi | yes | `tools/build_gateways.py + assets/gateway-copy.json` |
| `top-zh-cn.html` | zh-Hans-CN | yes | `tools/build_gateways.py + assets/gateway-copy.json` |
| `top-zh-han.html` | zh-Hant-TW | yes | `tools/build_gateways.py + assets/gateway-copy.json` |
| `top-zu.html` | zu | yes | `tools/build_gateways.py + assets/gateway-copy.json` |
| `zh-tw.html` | zh-Hant-TW | yes | `Jekyll frontmatter + _layouts + tools/build_jekyll_seo.py + _includes/share.html` |
