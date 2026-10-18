# KUMIHAN｜字衡 — URL and locale routing (2026-10-18)

The publicly chosen product-directory stems are **`zh-han` for Traditional Chinese** and **`zh-ch` for a planned, separate Simplified Chinese product**. They are custom product route names, not BCP 47 language tags.

| Role | URL under `main` / GitHub Pages | HTML language | State |
| --- | --- | --- | --- |
| ZiHeng Traditional Chinese main | `/kumihan-zh-han.html` | `zh-Hant-TW` | implemented |
| ZiHeng English translation | `/kumihan-zh-han.en.html` | `en` | implemented |
| ZiHeng Japanese translation | `/kumihan-zh-han.ja.html` | `ja` | implemented |
| ZiHeng Traditional Chinese installation | `/docs/install-ziheng.html` | `zh-Hant-TW` | implemented |
| ZiHeng English installation | `/docs/install-ziheng.en.html` | `en` | implemented |
| ZiHeng Japanese installation | `/docs/install-ziheng.ja.html` | `ja` | implemented |
| Simplified Chinese proposed product | `/kumihan-zh-ch.html` | `zh-Hans-CN` (when decided) | **reserved only; not published** |

The Traditional Chinese language attribute reflects the default Taiwan editorial voice of the landing page, not the only locale covered by the plugin. In the product, users select `zh-Hant-TW` or `zh-Hant-HK` explicitly. A Hong Kong-only page can use `zh-Hant-HK` if authorized later.

The existing `/zh-tw.html` translates the Japanese-language KUMIHAN introduction into Traditional Chinese; it is **not** the ZiHeng product homepage. Link to ZiHeng from the Japanese KUMIHAN landing footer without changing the identity of `/zh-tw.html`.

Keep independent metadata, `hreflang`, canonical, language-switch links and relative paths in sync. Do not rewrite original Chinese quotations or the literal U+FF5C branding separator (`｜`) to enforce a font palette. No external fonts are downloaded.

The package is guidance: the static review helper does not render text or guarantee all native hosts. ZiHeng has four independent skills and a `0.1.0-preview` full-plugin archive. The ZIP filename carries the version; its display name is simply **KUMIHAN｜字衡**.
