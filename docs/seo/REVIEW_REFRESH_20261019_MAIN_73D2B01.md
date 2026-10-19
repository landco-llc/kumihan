# Current final Owner Gate — latest main05c60fd / 2026-10-19 JST

W09–W15 implementation is integrated with current main `05c60fd5d519a3a6d38feb616f60fddd373b635f` (including newly merged PR #103 privacy policy/footer). Current audit is **274 HTML / 273 canonical URLs**, not the earlier272/271. 22 gateways +63 LP +186 guides +2 privacy policies, plus1 excluded alias. Privacy translation group is en/ja/x-default, separate from gateways/products. No body or policy text rewritten by SEO.

Latest-main protection PASS: **257 body suffixes** (253 static +4 layouts),21 original Jekyll sources,2609 protected distribution/skill/manifest files. Root tests62/62 and SEO26/26 PASS. Shared language previews and 1200×630 image retained. Current inventory: [BASELINE_INVENTORY.md](BASELINE_INVENTORY.md).

**Authoritative final SHA / Hosted CI / independent review / Owner Gate state:** [final PR #93 gate record](https://github.com/landco-llc/kumihan/pull/93#issuecomment-6265452330). This stable GitHub record is updated after exact-head CI, avoiding another evidence-only commit that would invalidate its own SHA. Earlier snapshots below remain historical evidence for their explicitly named commits.

Draft remains unmerged, auto-merge disabled. Owner alone may approve merging; then deployed HTML/image/current273-URL Sitemap must be verified before Search Console. SEO does not publish or send sitemap.

---

# W09–W15 review resolution — 2026-10-19 JST

**This resolution supersedes the historical read-only status below. Draft PR #93 remains unmerged; integrated HEAD 6c4ecbf Hosted CI23/23 PASS; final evidence-only HEAD checks are recorded on PR #93.**
Latest refreshed main: `a08fd66fcb58d70dd448dfcb51745c0c91d03d4f` (#100/#102/#104 merged; #101 Draft/unmerged).

| Finding | Resolution and real evidence |
| --- | --- |
| P0-01 alias exception | `seo_metadata.enrich_html` exact top-en allowlist requires noindex + expected refresh. Descriptionless normal page and invalid alias negative tests. Sitemap excludes alias. |
| P0-02 OGP authority | Calls `site_share.tags/description/locale`; language copy and 1200×630 PNG/large card preserved. Mixed-quote duplicates and repeated hooks tested. Jekyll passes same canonical/title/description/effective lang to actual share.html. |
| P0-03 root URLs | index canonical/OG/WebPage/en/x-default = `/kumihan/`; Japanese top-ja self; audited root once and alias excluded. |
| P0-04 new languages | 22 gateways, 63 LP, 186 guides; source audit272/Sitemap271 PASS. All new builders covered. Local Chromium320 nine routes HTTP200, JS errors0, width320, fa RTL; font requests blocked during smoke. Body255 + Jekyll21 byte protection PASS. |
| P0-05 current main artifacts | 2609 paths SHA256 protected; skills/plugins/ZIP/version/README/CHANGELOG match refreshed a08fd66. #104 upstream release announcement preserved. No release changes by SEO. |
| P1-06 Jekyll share locale | All supported locale data generated from gateway authority; unknown/missing/stale data fails CI. Existing legacy default-ja explicitly passed to share.html, rather than silent unknown-locale fallback. |
| P1-07 duplicates/CI | Independent review found duplicate landing hreflang; Hosted actual audit found nil language handoff. Both fixed at d395e14, two regressions FAIL→PASS, SEO24/root59 PASS. Push actual Jekyll3.10/audit success [39238730392](https://github.com/landco-llc/kumihan/actions/runs/39238730392). After upstream merge, 6c4ecbf Hosted CI23/23 PASS, including push and PR actual Jekyll3.10/audit. |

**Integrated code CI23/23 PASS; all original five P0 issues resolved. Independent P1 finding fixed and actual Jekyll verified.** No blocker is being waived. Independent report/fix record: [INDEPENDENT_REVIEW.md](INDEPENDENT_REVIEW.md). CI evidence and limitations: [VALIDATION_LOG.md](VALIDATION_LOG.md). No production/Google indexing claim. Main merge remains Owner Gate.

---

## Historical mandatory review (before implementation)

# SEO PR #93 / 未実行W09–W15 — 最新main再レビュー（2026-10-19 JST）

**状態:** READ-ONLY REVIEW COMPLETE / RECONCILIATION NOT RUN / MERGE HOLD  
**GitHub接続から実読したmain:** `73d2b01d2f604608360beabe364f59af72b8b66c`  
**SEO PR #93に既存のコード変更が残るbranch:** `feature/seo-foundation-20261019`  
**レビュー開始時のSEO branch HEAD:** `861bd3346ecd218cf45bf0b2c4cbbbfab6b3823f`  
**Source of task:** `docs/seo/RECONCILIATION_20261019_EN_TOP_NEW_LANGS.md`（修正版を必ず読む）  
**評価対象:** SEOコードと現行公開候補のGitHubリポジトリ状態、関連PR、既存レビュー・CI証跡。ライブGoogle検索登録の確認ではない。

## 1. 判定

- **マージ禁止を維持。** PR #93はDraft、未マージ、GitHub上で `mergeable=false`。
- 前回W09–W15は**未実行**。今回行ったのは再Fresh Read・レビュー・管制正本更新のみ。既存SEOコード統合、Sitemap再生成、最新main向けJekyll実ビルド、再CI・独立実装レビューは未実施。
- PR #93の旧CI 20/20 PASSは `0cfadad` 以前の旧ベースに対するもの。文書-only HEADのCIが成功しても、現行mainとの統合証拠にはならない。
- 最新mainは前回の `db14de2` から `73d2b01` へ進み、**PR #100がマージ済み**。PR #101はMCPのDraft未マージ、PR #102はRendered QA資料のDraft未マージ（SEO実装対象外）。
- #100は配布物/Plugin Manifest等を `v0.1.8-preview` 候補へ更新している。これは現行mainの**保護対象**。SEO用旧ブランチの状態に戻してはならない。公開Release完了を意味しない。

## 2. 現行ページ棚卸し（観測値）

GitHub mainのrecursive git treeで確認したHTMLファイル候補:

| 対象 | 数量 | 確認事項 |
| --- | ---: | --- |
| 公開言語ゲートウェイ | 22 | 英語index、日本語top-jaを含む |
| 製品LP | 63 | 日本語KUMIHAN 3 + 多言語製品 20×3 |
| docsのHTML | 186 | 個別生成元 / Jekyll / authored mixed |
| 旧トップの転送alias | 1 | `top-en.html` は `noindex` |
| HTMLファイルの合計 | **272** | root 86 + docs 186 |
| indexable URL予想 | **271** | 旧alias1件除外を仮定。実SEO監査前の見込み値 |

重要: 271はコード/サイト上で正式検証されたSitemap件数ではない。追加のnoindex/異常canonicalや発行条件で実数は変化し得る。直近の旧231 URLは現在の公開候補を網羅していない。

### URLの正本方針

- 英語標準トップ: `https://landco-llc.github.io/kumihan/`（実体 `index.html`）
- 日本語トップ: `https://landco-llc.github.io/kumihan/top-ja.html`
- 旧 `top-en.html`: noindex/meta refresh → 英語トップ。Sitemap掲載禁止
- トップ系hreflang: 22言語＋適切な `x-default`（英語ルート）。相互参照であること
- 製品LP群やinstall guideは**トップの翻訳群へ混入させない**

## 3. 指摘・修正要求

### P0-01 / 旧aliasにSEOエンリッチャーが失敗する可能性

Mainの `top-en.html` はnoindex転送用の極小HTMLで、一般ページ用 `meta[name=description]` がない。旧 `tools/seo_metadata.py::enrich_html` はtitle/description/langが必須で、欠落するとValueErrorを投げる。main側 `tools/build_gateways.py::outputs` はaliasも出力する。単純rebaseした場合、ビルダー全体が止まる危険。

**修正:** alias判定を共有契約に追加し、明示的noindex/転送ページは一般SEOメタ付加対象から除外。SiteMapは非index扱いを検証。未知のdescription欠落を自動でalias認定しない。正常HTMLのdescription欠落は従来どおりFAIL。aliasを回帰テスト固定。

### P0-02 / PR #99共有カード上書きと二重OGP

Current mainの `tools/site_share.py` と `_includes/share.html` は、言語別OGPコピー（meta descriptionより詳しい合成説明文）と `assets/kumihan-share.png` (1200×630)を管理。旧SEO `render_metadata()` は別説明文・旧正方形マスター(1254×1254)/twitter summaryを設定。単純採用は既存プレビュー後退になる。

**修正:** SEO headの唯一性を保ちながら責務を分離。SEO = canonical/hreflang/JSON-LD、site_share = OGP/Twitterの表現と画像。meta title/descriptionは既存正本。ハンドオフ引数/呼出順序を明示し、`og:url` がcanonicalと一致。ハードコードしたJekyll `page.url` に依存せず正規URLを渡す。最終HTMLでOGP/Twitterが各1組、タイトル・説明・画像の言語別適合をテスト。

### P0-03 / 英語ホームの正規化とhreflang

現行mainの `index.html` は自己canonicalを `.../index.html` としており、英語トップのx-default/OGPも旧の表記を残している。SEO側は `.../kumihan/` を正本とする予定。混在のままではURL・構造化データが不一致。

**修正:** 英語ルートのcanonical / og:url / WebPage.url / sitemap loc / hreflang en + x-defaultを**同一のroot URL**へ統一。日本語トップ `top-ja.html` は独立自己canonical。転送aliasのcanonicalもrootへ更新する場合はnoindex意図を保持。これをテスト。

### P0-04 / 新規言語版と新公開ページ

現行mainにはsw/zu/km/fa（スワヒリ語、ズールー語、クメール語、ペルシア語）のトップがあり、zu/km/faの3言語LP・導入ガイドも追加済み。旧SEOグループは旧GATEWAYSから生成している。

**修正:** mainの実データを唯一の基準として全登録・生成元にSEOを適用。FAはRTL/ZWNJ、KMは結合文字、ZU/SWは原文表記をbyte-for-byte保護。新規ディレクトリ/公開HTMLが追加されるとSEO検証がFAILまたは正しくSitemapへ入ること。推測の言語ページを作らない。

### P0-05 / #100マージと既存リリース候補の保護

前回の指示書は「PR #100 Draft未マージ」と記載しており現状と異なる。#100は最新mainに入っており、パッケージ、Plugin Manifest、README/CHANGELOG等を含む75ファイルを更新。

**修正:** rebase/mergeの比較基準をFresh Readした最新mainへ変更。PR #100を**含んだ**skill/plugin/distributionを保護し、SEO実装による差分0を検証。BuildDistのversion変更、再パッケージ、配布ZIP変更は実行禁止。元々変わったものを旧baseとの差分だけで「SEO改変」と誤認しない。PR #101/102は未マージの独立並行作業として管理。

### P1-06 / Jekyll共有コピーの言語フォールバック

現行 `_data/site_share.json` は既存Jekyll対象言語の一部のみを列挙。新言語のJekyllページが増えると `_includes/share.html` がJAフォールバックになり、表示言語とOGP説明文が不一致になり得る。

**修正:** Jekyll対象言語とshare辞書をビルド時に照合。未登録の言語に無条件でJAを適用しない。既存`assets/gateway-copy.json`をコピー正本にして必要な辞書を生成、または有効な明示的対応表をテスト。言語未登録時はfail-closedか監査FAILで可視化。新言語追加手順に追記。

### P1-07 / 二重メタ・生成順と旧CIの扱い

- Python/Node/Jekyllの2度実行でOG/JSON-LDが増殖しないこと
- 旧SEOの `description == og:description` テストを現行site_share仕様へ置換
- Jekyll3.10で実際の出力を監査。ソースHTMLと生成済みHTMLの混同は不可
- 負例: duplicate canonical/OGタグ、alias noindex、root/index混在、未知言語、Unicode/RTL、非公開ディレクトリ
- 最終branch HEADに結びついたHosted CI、独立コードレビューと差分監査が必要
- その時点までPR #93の旧20/20をマージ判定に流用しない

## 4. 優先実装順

1. **W09**: 最新mainを読み込み、最新packageを保護しつつ既存SEO branchへ安全に統合。競合解決台帳
2. **W10**: 英語index・日本語top-ja・旧top-en aliasを正規化し、aliasの生成スキップとSitemap除外
3. **W11**: 22ゲートウェイ+新言語製品/導入ページの生成元を更新
4. **W12**: site_shareをOGP/Twitterの唯一正本としてSEO/Jekyll/Nodeを整合
5. **W13**: Sitemap再生成（271は目安）/実Jekyllビルド/CI/既存生成器チェック/本文とパッケージ保護テスト
6. **W14**: `docs/seo/BASELINE_INVENTORY.md`、`DECISIONS.md`、`ADD_LANGUAGE_OR_PAGE.md`、`VALIDATION_LOG.md`を実結果で更新
7. **W15**: 新HEADのHosted CIを待たずに結果が揃ったことにせず、独立コードレビューでP0 blocker 0を確認し、既存Draft PR #93をOwner Gateへ返す

**Owner Gate:** このレビューは実装・CI・マージ許可ではない。技術実装後もmainへ自動mergeしない。本番URL・Sitemap・Google Search Consoleの確認は公開後。

## 5. 参照ソース

- GitHub main: https://github.com/landco-llc/kumihan/tree/main
- SEO PR: https://github.com/landco-llc/kumihan/pull/93
- Share PR: https://github.com/landco-llc/kumihan/pull/99
- Design/Skills merged PR: https://github.com/landco-llc/kumihan/pull/100
- MCP Draft PR: https://github.com/landco-llc/kumihan/pull/101
- QA Draft PR: https://github.com/landco-llc/kumihan/pull/102

## 6. レビューの限界

- GitHub API経由のソース/PR/履歴/CIメタ確認を実施。最新mainを統合した実コードのテストは**未実行**
- 公開Webの直接取得はこのレビュー時のWebアクセス制限で確認できず。GitHub上でのファイル存在は本番稼働の証明ではない
- 271 URLは現行ファイルの棚卸しからの推定値であり、実行済Sitemap監査結果ではない
