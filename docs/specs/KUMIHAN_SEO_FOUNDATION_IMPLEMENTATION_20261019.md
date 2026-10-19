# KUMIHAN SEO基盤 v1.0 実装・継続運用指示書

- Doc ID: KUMIHAN-SEO-FOUNDATION-20261019
- 作成: 2026-10-19 (JST)
- Status: **APPROVED IMPLEMENTATION SPEC / EXECUTION NOT YET STARTED**
- Priority: A
- Repo: https://github.com/landco-llc/kumihan
- Work branch: \`feature/seo-foundation-20261019\`
- Site: https://landco-llc.github.io/kumihan/
- Baseline when this task was opened: \`main\` at \`fce40015abaa1f5f309cf9e977f55e41537c13aa\`. **必ず作業開始時に最新mainと関連ブランチをFresh Readし、適切に追従**
- Scope: technical SEO **only**. GA4/GTM/Consent Mode/追跡CookieおよびAIO特化施策は別Work
- Developer/executor: Codex Cloud/App; Parent＝管制とGate、専門Child＝実装・独立レビュー可
- Execution style: \`/goal\` で下記W00〜W08を自律継続。HumanによるMD/ZIPの再添付を前提にしない
- Delivery: 実装コード＋生成済み公開ファイル＋自動検証＋永続Runbook＋PR。mainには直接push/mergeしない

## 0. 目的

KUMIHANの多言語サイトを検索可能で一貫したサイトにし、**新しい言語やランディングページが追加されても同じSEO情報と検証を再利用**できる仕組みを実装する。単発の手作業でheadを書き換える運用は禁止。

SEOは検索結果への掲載・順位・AI検索引用を保証しない。公開前の正確なコンテンツと技術的な一貫性を優先。

## 1. GitHub実読で確認した現状と前提

2026-10-19 に最新mainを確認した結果:

- 静的GitHub Pages、既定ブランチ\`main\`
- トップ言語ゲートウェイは \`index.html\` と \`top-*.html\`（確認時18言語）。生成元 \`tools/build_gateways.py\`、コピー \`assets/gateway-copy.json\`、CSS \`assets/gateway.css\`
- 日本語版 \`kumihan.html\`、\`en.html\`、\`zh-tw.html\` はfrontmatter経由で \`_layouts/landing.html\` を使用するJekyllページ
- 各言語製品LPは \`kumihan-*.html\` 系。多くが \`tools/product_site.py\` および \`tools/build_*_site.py\` から生成される。Thai、Korean、Vietnamese、Simplified/Traditional Chinese、Bengali等には個別の生成元/テンプレートがある。**共通rendererを改修しただけで全ページ対応済みと主張しない**
- \`docs/\` 配下にも多数のインストールページ（HTML）。各ページのcanonical・indexabilityを検査したうえでサイトマップ対象を選別する
- \`index.html\`、\`top-en.html\` ではtitle/description/canonical/hreflangは存在、OGP/Twitterカード/JSON-LDは未確認（headに実装なし）
- \`kumihan-fr.html\` 等の各言語LPではOGPとcanonical/hreflangの実装例があるが、JSON-LD等は未整備
- \`robots.txt\`、\`sitemap.xml\`、\`_config.yml\` はリポジトリ直下で未検出（GitHub Pagesの公開結果を別途確認）
- GA4/GTM計測タグは現行の主なHTML/テンプレートで未確認
- 既存のSNSシェア機能仕様書は別ブランチ \`feature/sns-share-spec-20261019\` の \`docs/specs/KUMIHAN_SNS_SHARE_IMPLEMENTATION_SPEC_20261019.md\`。**canonicalとOGPの正本を本SEO側に寄せる設計**とし、並行作業があれば差分整合する

## 2. このWorkの範囲

### P0 — 必須

1. \`<title>\`、\`meta[name=description]\`、\`<html lang>\`、必要な\`dir\`
2. ページごとの \`rel=canonical\` 統一。必ず実在・公開される絶対HTTPS URL。トップ \`/kumihan/\` と \`/kumihan/index.html\` の重複はホームURL \`https://landco-llc.github.io/kumihan/\` に正規化する（既存ルートを壊さない）
3. 対応する多言語版の \`hreflang\`（自己参照・相互参照・必要な\`x-default\`）。トップ言語ゲートウェイ同士、製品/版の翻訳同士を区別。**製品紹介ページとトップページを誤って互いの翻訳として紐づけない**
4. OGP: \`og:type/title/description/url/locale/image\`、必要に応じて \`og:image:alt/width/height\`
5. X向け \`twitter:card/title/description/image\`（\`summary_large_image\` は画像比率に適する場合のみ）
6. JSON-LD: \`Organization\`、\`WebSite\`、\`WebPage\` を実際に該当するページへ。属性は公開情報に基づき、架空のレビュー・料金・販売実績を付与しない。必要な製品ページに限り正確な \`SoftwareSourceCode\` を検討する。Google向けSoftwareApplicationリッチリザルトのために架空の\`offers\`等を入れない
7. \`sitemap.xml\` の決定的・再生成可能な生成。canonical URLだけ、重複URLなし、\`noindex\`・外部canonical・URL不存在を除外。\`<lastmod>\` は信頼できる更新情報がある場合のみ付与し、ビルド時刻の偽装はしない。 \`priority\`、\`changefreq\` は不要
8. 既存テンプレート/ジェネレータへの組込み（生成HTMLだけの後付けや手動修正で終わらない）
9. 追加言語/ページの自動登録・ドリフト検出・CIチェック・運用ドキュメント

### P1 — このPRで対応しない

- Google Analytics 4 / Google Tag Manager / Consent Mode / 広告タグ
- Search Console所有権の本人確認や管理画面へのログイン、Sitemap送信（Humanまたは別権限作業）
- バックリンク獲得、コンテンツ増産、広告、ランキング改善保証
- \`llms.txt\` や根拠のないAIO専用のmeta keywordsの追加
- AIクローラーの学習許諾方針の変更
- スキル/プラグイン本体、Release、ZIP、バージョン番号の変更
- \`main\` への自動マージ

## 3. アーキテクチャ決定

### 3.1 正本と生成物の分離

「ページのコピーや言語構造を既存の生成元に置く」「SEOで共通化できる処理は1か所に実装」「XMLサイトマップは生成物」という3層。

推奨（ファイル名は既存repoに合わせて最小変更可）:

- \`tools/seo_metadata.py\` — URL正規化、メタ出力、JSON-LD生成、言語別alternateの共通処理
- \`tools/build_sitemap.py\` — canonical/公開対象に基づくサイトマップ生成と\`--check\`
- \`tools/check_seo.py\` — 生成結果を読み、meta/URL/hreflang/OGP/JSON-LD/Sitemapを横断検証
- \`assets/seo-config.json\` — サイトURL、publisher情報、OG画像パス等の**共有定数のみ**。ページタイトル/本文は既存コピー正本から取得し、重複した翻訳レジストリを作らない
- \`docs/seo/README.md\` — SEO設計と正本ファイルの対応表
- \`docs/seo/ADD_LANGUAGE_OR_PAGE.md\` — 新言語/ページ追加時の実行手順とチェックリスト
- \`docs/seo/DECISIONS.md\` — ADR形式の判断理由・例外
- \`docs/seo/VALIDATION_LOG.md\` — 検証日/commit/対象/実行コマンド/結果/未確認を記録
- \`.github/workflows/seo-foundation.yml\` — PR時の自動check

ページを新規追加する際、必要以上に\`seo-config.json\`へページごとの情報を二重登録させない。既存の \`GATEWAYS\`/\`PRODUCTS\` 登録、言語別コピー、生成済みcanonicalから得られる情報を再利用する。

### 3.2 GitHub Pages/Jekyllへの適用

- \`tools/build_gateways.py\` を修正し、すべての \`index.html\`/\`top-*.html\` のSEO headが再生成される
- \`_layouts/landing.html\` のJekyll変数を使い \`kumihan.html\`/\`en.html\`/\`zh-tw.html\` のSEO headを出力。**Jekyllの生テンプレートの値とビルド後HTMLを混同しない**
- \`tools/product_site.py\` を共通rendererとして利用する言語版はそこでSEO出力する。ただし固有HTMLを持つ言語版では個別の生成元へのフックを追加し、\`--check\`で再生成一致を保証
- Python製以外の生成元（例:\`tools/build_nhip_chu_site.mjs\`）も独自処理を放置せず、正本からSEOが反映されるアダプタ・共通メタデータ契約を作る。Python/Node間で同じJSON情報を消費して構わない
- 直接編集を要するテンプレート（例: 独立版テンプレート）は、編集対象と生成先のペアを明記
- HTMLソースに重複meta、同一属性の矛盾した値、重複canonicalを作らない
- JekyllのFront Matterページが\`--check\`で誤って失敗する場合、出力HTMLを前提とした別検証を設ける
- CIの\`--check\`は**非書込**で、コード変更なしの2度目の再生成で差分0となること

### 3.3 Sitemap登録規則

- Site base: \`https://landco-llc.github.io/kumihan/\`
- 対象候補: サイト公開対象のHTMLページ（リポジトリrootと言語版LP、インストールガイド等）。自動探索と公開対象/正規URLの検証を組み合わせる
- **サイトマップに含むのは存在するindexableなcanonical URLだけ**。自分自身へcanonicalが向くか、指定したホーム別名だけ例外許容する
- 既存ページのredirect/alias/重複/404/非公開へのリンクをサイトマップに掲載しない
- hreflangはまずHTML側の相互参照を正本にする。サイトマップにxhtml:linkを重複出力する場合はHTMLとの自動一致検証が必須。Googleは複数方式の併用を必要としていないため、初期版は\`loc\`をシンプルに保つことを推奨
- project siteのルートURLと \`index.html\` を二重登録しない
- \`sitemap.xml\` はコミットしてGitHub Pagesから公開。新ページ追加時は生成して差分をコミットする
- Search Consoleへの送信URL: \`https://landco-llc.github.io/kumihan/sitemap.xml\`。送信は所有権確認後

### 3.4 robots.txtの境界

\`https://landco-llc.github.io/kumihan/\` はGitHub Pagesのプロジェクトサイト。
\`/kumihan/robots.txt\` を置いても通常はホスト直下\`https://landco-llc.github.io/robots.txt\` の代わりにはならない。ユーザー所有のGitHub Pagesユーザーサイトまたは独自ドメインの設定可否を調べるまで、誤解を招くrobots.txtをプロジェクト直下へ置かない。

このWorkでは、クローラーをブロックしない方針の確認と制約の記録まで。AIクローラーの学習利用許可等の新規変更は別途Owner判断。

### 3.5 OGP画像

現存の \`assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png\` を利用するか、ブランドに沿った共有用横長画像を用意。既存画像が正方形なら**サイズ/比率を偽って1200×630とmeta表示しない**。横長画像を作る場合は公式ロゴの縦横比、余白を保ち、KUMIHANを用いて文字組・コントラストを確認。サイトとSNSで画像取得可能性、サイズ、MIMEをテストする。

## 4. 多言語SEOの非交渉ルール

- 言語はページの実際の本文に従って\`<html lang>\`を設定。日本語/英語/繁体中国語のページはそれぞれ独立したURL
- 中国語の地域表現（\`zh-Hant-TW\`、\`zh-Hans-CN\`）、韓国語、タイ語、アラビア語、ヒンディー語、ベンガル語、ベトナム語等のUnicode・方向性・語境界を保護
- 実際に翻訳が存在するペアだけhreflang相互参照。存在しない翻訳ページを推測して生成しない
- x-defaultは言語選択ゲートウェイに向けるなど、同一コンテンツ群の中で意味のある既定ページに設定
- \`hreflang\`のタグに入れるURLは絶対URLで統一し、全代替ページから互いにリンクしあうこと
- canonicalは**言語別に自己参照**（例: フランス語ページから英語をcanonicalにしない）
- 現在のトップ\`GATEWAYS\`（18言語）はトップ同士で同じ代替グループに属する
- 各製品版の3言語訳は製品版ごとに独立した代替グループにする
- \`og:locale\`は妥当なコードで、ページの表示言語と意味的に一致
- 各製品名や説明文を勝手に翻訳、改称、正規化しない
- 画面外のhiddenコンテンツをSEO目的で増やさない

## 5. JSON-LDの対象と注意

候補:
- サイト・トップの主要ページ: \`WebSite\`、必要に応じて \`Organization\` と \`WebPage\`
- 個別の版紹介ページ: \`WebPage\`、掲載されているオープンソース配布実体に該当する場合だけ \`SoftwareSourceCode\`（schema.orgの情報付けでありGoogleのリッチリザルトを保証しない）
- \`Organization\` の\`name = "L&Co. LLC"\`、URLは公式\`https://landco.co.jp/\`。正式ロゴが公開された安全なHTTPS URLにあること。団体名、URL、ロゴ等の事実以上を作らない
- \`@id\`は安定したURIにし、多言語版で不必要に別Organizationを作らない
- 各\`WebPage.url\`とcanonicalは一致。\`inLanguage\`は表示言語と一致
- SEOを理由に不要な\`aggregateRating\`、\`offers.price\`、\`FAQPage\`等を推測で追加しない
- JSON-LDは安全なJSONエスケープで静的HTMLへ埋め込む。読み込めるが意味が虚偽という状態を防ぐ

## 6. Codex Work群（Human再添付なし）

### W00 — Fresh Read / conflict check

最新main・branch・関連PR・サイト生成器と並行SNSシェア開発を読んで一覧化。source→generated HTML のマッピングを作成。対象をroot HTML・Jekyll・個別生成ランディング・docsに分類。既存リリースの配布ZIP・パッケージは改変禁止。HEADがベースから進んでいる場合は安全に再同期。

**成果:** \`docs/seo/BASELINE_INVENTORY.md\`（対象ページ一覧、生成元、追加/除外、未確認、基点SHA）。

### W01 — SEOデータ契約

URL/canonical、title/description、言語、hreflang、OGP、Twitter、JSON-LDの共通型と出力規則を実装。既存ページのコピー正本が優先。ゲートウェイ/製品/インストールガイドに対して同じ契約を適用。

**成果:** SEO共通ライブラリ・設定ファイル・小さなユニットテスト。

### W02 — ゲートウェイ全言語対応

\`tools/build_gateways.py\` と必要なコピー・共通ライブラリを改修し、index/top-* 全対象にSEO headを生成。共通OGP画像の実体・リンクも整備。canonicals/hreflangsはサイトのURL構造に統一。

**成果:** 生成元＋生成済みHTML＋check PASS。

### W03 — 言語版ランディング・Jekyll対応

\`_layouts/landing.html\`、\`tools/product_site.py\`、各独立生成元に必要な変更。言語ごとの固有title/descriptionを保持。frontmatterやJekyllのレイアウト処理を確認。ビルド後にもJSON-LD/OGP/canonicalが表示されること。

**成果:** 対象全ランディングへの反映・source→output対応表・固有生成器の検証。

### W04 — Sitemap自動生成

rootとindexableなdocs等のページを検出し、正規URLのみを\`sitemap.xml\`に出力。決定的な順序で再生成し、\`--check\`が書込みなしで差分を検出できる。重複・非公開・canonical不一致は検出し黙って無視しない。

**成果:** build tool＋sitemap.xml＋ユニットテスト。

### W05 — 自動監査とCI

PR CIで、
- Sitemapに存在しないURL・重複URL・非canonicalを検出
- 対象ページのtitle/description/canonicalが各1つ、OGP/JSON-LDが妥当
- lang/hreflangの自己リンク・相互リンクと存在性をチェック
- 新規ページがSEO対象から漏れたらFAILし、\`docs/seo/ADD_LANGUAGE_OR_PAGE.md\`へ誘導
- 既存ビルダーの\`--check\`を維持し、SEO追加による差分ループを防止
- JSON-LDをJSONとしてパースし、\`WebPage.url\`とcanonical一致をチェック
- 日本語/繁体中国語/アラビア語等、文字化けと方向性の基本検査
- 既存の言語版公開テストと衝突しないよう変更対象を限定。

**成果:** 専用CIワークフロー＋テスト＋既存check PASS証跡。

### W06 — 将来追加に強い記録

\`docs/seo/\`配下の4つの正本（README、ADD_LANGUAGE_OR_PAGE、DECISIONS、VALIDATION_LOG）を実際のコードに一致させて作成。新しい言語の登録手順、ページ作成、OG画像、indexable判定、コマンド、CI、確認責任を**実行可能なチェックリスト**にする。例題として\`test-fixture-new-language\`（公開しないfixture）を追加し、将来言語を追加したときSitemap/メタ/CIが自動検知するテストを通す。

**成果:** 運用ドキュメントと自動検出の証明。

### W07 — 独立レビュー・プレビュー実測

専門Childまたは独立レビューで静的メタとサイト構造を照合。可能ならGitHub Pages相当のJekyll生成、ブラウザ表示、Google Rich Results Test・Schema Markup Validator等を使って確認。**Google側のインデックス登録済みやSearch Console送信済みを主張しない**。SNSのメタデータ取得を検査する場合はキャッシュやログインの影響を明記。

**成果:** テスト結果・未達事項・リスクと例外。

### W08 — PRと引き継ぎ

- 専用ブランチからmain向けDraft PRを作成
- \`docs/seo/VALIDATION_LOG.md\`に最終HEADとテスト実行結果
- PRに変更ファイル一覧、対象ページ数、除外理由、テストPASS/FAIL/未実施、Search Console Owner操作、競合作業との差分を記載
- 未確認がある場合はfail-openで「完了」と主張しない
- Humanによる次WorkへのMD/ZIP添付は不要
- mergeや公開のOwner Gateで停止（明示承認がない限りmainへmergeしない）

## 7. 受入基準（Definition of Done）

- [ ] 各公開対象のmeta title/description/canonical/hreflang/OGP/JSON-LDが意味・URLとも整合
- [ ] トップ18言語と現行各製品言語LPを生成元からカバー、未対象ページは公開/非公開理由が記録済み
- [ ] \`sitemap.xml\`が公開対象を網羅し、重複canonical URLを含まない
- [ ] 既存/新規の言語版に対するhreflang自己参照と相互参照が正しい
- [ ] 新規言語/ページfixtureが追加された際にSEO漏れをCIが検出し、必要な変更でPASSになる
- [ ] 生成元と生成HTMLが\`--check\`で一致（再実行して不要な変更を作らない）
- [ ] JSON-LDは実在する組織・ソフトウェアの公開情報だけで構成
- [ ] OGP画像の公開URLとmeta上の寸法/種別が一致
- [ ] GA4/GTM/ユーザートラッキング、架空のスコアや評価は含まない
- [ ] ドキュメント4点とページ棚卸しが実装に同期され、運用コマンドを記載
- [ ] CI PASS と独立レビュー結果がPRで確認できる
- [ ] Search Console未接続/登録未実施・未確認事項を明記
- [ ] 配布ZIP・プラグイン・各言語製品のversionを変更していない
- [ ] PRだけ作成し、mainは未マージ

## 8. 主要参照資料

- Google 多言語hreflang: https://developers.google.com/search/docs/specialty/international/localized-versions
- Google 多言語サイト: https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites
- Google Sitemap: https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- Google canonical: https://developers.google.com/search/docs/crawling-indexing/canonicalization
- Google 組織構造化データ: https://developers.google.com/search/docs/appearance/structured-data/organization
- Google ソフトウェア構造化データ: https://developers.google.com/search/docs/appearance/structured-data/software-app
- Schema.org: https://schema.org/
- Open Graph: https://ogp.me/
- Google Search Console: https://search.google.com/search-console/about
- Jekyll Sitemap: https://github.com/jekyll/jekyll-sitemap

### 注意

仕様書上での「現状」は2026-10-19の観測。CodexのW00で必ず最新状態を優先する。本書の文面と実際のコードが矛盾すれば勝手にコードを推測修正せず、証跡を基に判断し、\`docs/seo/DECISIONS.md\`に理由を記録する。

## 9. Codex起動文

~~~
対象: GitHub landco-llc/kumihan
作業ブランチ: feature/seo-foundation-20261019
正本: docs/specs/KUMIHAN_SEO_FOUNDATION_IMPLEMENTATION_20261019.md

上記仕様書をFresh Readし、/goalでW00〜W08を一気通貫で実装してください。サイトのSEO共通生成・多言語canonical/hreflang・OGP・Twitterカード・JSON-LD・sitemap.xml・検証CI・新言語追加Runbookまで完成させること。生成済HTMLだけでなく各生成元を修正し、既存の言語別タイトル・コピー・文字組・配布スキル/プラグインを保護してください。HumanのMD/ZIP再添付なしで自律継続し、独立レビューとテストを実施してDraft PRを提出。GA4/分析タグ/学習クローラー設定変更は対象外。mainへの直接push/mergeは禁止。完了時はPR URL、変更範囲、PASS/未実施、Search ConsoleでHumanが行う操作を報告してください。
~~~
