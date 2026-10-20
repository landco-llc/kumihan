# KUMIHAN v0.2.0 — GitHub Release Notes (JA)

**Release scope: Japanese typography guidance and source packages / 日本語版文字組ガイダンス・配布ソースの更新**

Developer / 開発元: L&Co. LLC. The plugin's display name remains **KUMIHAN**; only ZIP filenames include the version.

## 日本語

今回のv0.2.0では、日本語の文字史・書体・文章表現・Web／文書／スライドの組版に関する調査結果を、KUMIHANの4スキルに反映しました。文章として読む文字、情報探索、操作ラベル、造形コピーを役割ごとに扱い、原稿・字形・実表示・意味判断を別々に評価します。

主な更新：文字の役割と意図・読む課題の整理、必須情報の可視性、禁則と自然な改行の区別、書体・サイズ・行長の条件付きレシピ、検証証拠と未確認状態の記録。既存39規則・6媒体profile・7状態・レポートschemaの互換性を維持し、他20言語版は更新しません。

**受入の範囲と制限：** 105件の単体テスト、29件のSEOテスト、対象ブラウザーでの画像確認、15 ZIPのサイズ・CRC・SHA-256と再現性が検証記録にあります。研究用30ケースは15部分実施／15未実行で全ケースの実環境合格ではありません。ChatGPT/Codex、Claude、Geminiにおけるネイティブインストール・4スキル呼び出し（12件）、Microsoft Office、実ユーザーの文字拡大、物理投影・可読性実験は未検証です。

**既知の問題：** 特定のLibreOfficeDev 26.8 alphaと元のNoto Sans CJK JP環境で、PPTX→PDF変換時に日本語と英数字の境界へ余分な空白が抽出され、字間が変わって見える条件があります。代替フォント条件での改善は確認されていますが、元環境の問題は未解決です。すべてのPDF変換の完全一致や自動文字組品質は保証しません。

このReleaseはGitHub上のソース・ZIP配布です。Marketplaceへの申請やホスト動作認証、Universal MCP本番更新の完了を意味しません。

## English

KUMIHAN v0.2.0 updates the four Japanese-language skills with research-informed typography guidance. It distinguishes continuous reading, information scanning, UI operation and display/artistic lettering; records purpose, region and reader task; and separates source-text preservation from rendered appearance, glyph identity and semantic review. Web, report, slide and short-copy recipes remain conditional on actual typefaces, dimensions and environments.

The 39 Japanese rule IDs, six media profiles, seven report statuses and existing report schema are preserved. Other 20 language editions are unchanged. Recorded validation includes 105 unit tests, 29 SEO tests and 15 deterministic ZIP archives with integrity checks. Of the 30 research scenarios, 15 were partially exercised and 15 were not run. No full-case certification is claimed.

**Known limitations:** Native ChatGPT/Codex, Claude and Gemini installation/invocation (0/12), native Microsoft Office, native user text zoom, physical projection and reader-performance testing remain unverified. Historical LibreOfficeDev 26.8 alpha PDF export using the original Noto Sans CJK JP environment may alter extracted spacing between Japanese and numeric/Latin runs. An alternate font environment does not resolve this historical finding. This release does not claim automatically verified layout quality or universal PDF copy/paste fidelity.

GitHub source and ZIP distribution only; no Marketplace submission or native-host certification is implied. Universal MCP server deployment is separately tracked and must not be described as live until verified.

## Distribution SHA-256 contract (15 flat ZIP assets)

The release worker must verify these names and digests from the **exact tagged Git tree** before changing Draft to Published. Values below are audited v0.2.0 candidate digests and are not proof of Release upload.

| Asset name | Bytes | SHA-256 |
|---|---:|---|
| `kumihan-Claude-Code-plugin-0.2.0.zip` | 509143 | `78eb29f367d9c0014709825a6f45f496e75930db77fc4b2198590092a2edeba1` |
| `kumihan-Claude-skill-0.2.0.zip` | 124375 | `44d87e11078c48de44eea2d18aacdef74ba67620bab6b23adbe4592b031c76ca` |
| `kumihan-documents-Claude-skill-0.2.0.zip` | 124694 | `d09b422f8f149fffd51c1e79f3ef3050ec7d5604f99fdaf9e9dcbe0d78a68242` |
| `kumihan-review-Claude-skill-0.2.0.zip` | 124674 | `d292651bb180d688b5328857607ca34f6f05f31b005f76634b9cb95f301a5d69` |
| `kumihan-web-Claude-skill-0.2.0.zip` | 124727 | `858c6eea185817a4ac228087ea88efd06d8d9428a6fe2ad0f19e0954b792e3c6` |
| `kumihan-GPT-Codex-plugin-0.2.0.zip` | 1309156 | `1f8b2aaa943cd619dd9b3ffa918fc144f3c76d08c097472a2e9c372bcc1564f2` |
| `kumihan-GPT-Codex-skill-0.2.0.zip` | 124375 | `44d87e11078c48de44eea2d18aacdef74ba67620bab6b23adbe4592b031c76ca` |
| `kumihan-documents-GPT-Codex-skill-0.2.0.zip` | 124694 | `d09b422f8f149fffd51c1e79f3ef3050ec7d5604f99fdaf9e9dcbe0d78a68242` |
| `kumihan-review-GPT-Codex-skill-0.2.0.zip` | 124674 | `d292651bb180d688b5328857607ca34f6f05f31b005f76634b9cb95f301a5d69` |
| `kumihan-web-GPT-Codex-skill-0.2.0.zip` | 124727 | `858c6eea185817a4ac228087ea88efd06d8d9428a6fe2ad0f19e0954b792e3c6` |
| `kumihan-Gemini-CLI-extension-0.2.0.zip` | 506683 | `db68ec074cc45fecb48b1748f2048ab4f9a3ea73fcdbc362aafd353cd037cd3a` |
| `kumihan-Gemini-Apps-skill-0.2.0.zip` | 123799 | `067236ccd6b23ce97e50651a4bf4ee29cac8fa22de4b1240cf4df37845a58de8` |
| `kumihan-documents-Gemini-Apps-skill-0.2.0.zip` | 123398 | `a0997a0f216fcecfefc0520f557240ae03c09d2f298c883e65d984e24969fc0d` |
| `kumihan-review-Gemini-Apps-skill-0.2.0.zip` | 123594 | `f36b62bdbdc76330dc6e8a72602fee1b7937c82eed99a07b3decfd3492526231` |
| `kumihan-web-Gemini-Apps-skill-0.2.0.zip` | 123863 | `3a07dd00511cfaf1b6c9ca15ea6fc83007a4db52862404c209167583bfe943cc` |

Licensing: Apache License 2.0. Historical v0.1.8 and older assets remain available and unchanged. For audit provenance, use the immutable final Git tag source commit and `docs/development/ja-v020-20261020/qa/w09/RESULT.md`; do not publish an unfrozen candidate SHA as a release source.
