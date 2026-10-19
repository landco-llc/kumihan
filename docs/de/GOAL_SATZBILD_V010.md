# KUMIHAN｜Satzbild v0.1.0 — /goal 実装・公開マスター指示

Status: OWNER_APPROVED / EXECUTION_NOT_STARTED
Date: 2026-10-19 JST
Repository: https://github.com/landco-llc/kumihan
Execution branch: feat/satzbild-v0.1.0
Owner scope: 独立ドイツ語版の実装・既存デザインを踏襲したWeb・品質確認・main統合・GitHub Release・GitHub Pages公開まで承認済み。商用ストアへの申請や権限変更は対象外。
Execution: Codex Cloud / Codex App の /goal。Codex CLIのローカル起動は不要。

## 0. 最初に実読する正本

1. 最新 main を fresh read。AGENTS.md 等の指示、Git状況、既存PR、CI、公開状態を確認する。既存の別言語Workを上書きしない。
2. 日本語の主ページ: kumihan.html（Jekyll frontmatter）と _layouts/landing.html、英語 en.html。導入ページ: docs/install-chatgpt.html と _layouts/installation.html、assets/kumihan-install.css / .js。
3. 複数言語版の実装パターン: plugins/kumihan-grafia、plugins/kumihan-compasso、tools/build_grafia.py、tools/build_grafia_site.py、tools/product_site.py、tools/install_frame.py、tools/base_copy.py、tools/build_gateways.py、各CIと公開workflow。コピー元の固定パス・構造は現HEADで再確認。
4. 正式研究の入力は同じフォルダの RESEARCH_RULES_V010.md に抜粋。研究正本はOwnerのGoogle Drive KUMIHAN / RESEARCH / DE。参照しないまま原典を読んだと主張しない。
5. 既存共通ポリシー、4スキル分割・原稿保護・非定型デザイン・ライトレビューを維持する。

## 1. 製品・公開識別子 — FIXED

- 公開表示名は **KUMIHAN｜Satzbild** のみ。縦棒は全角 U+FF5C。「KUMIHAN｜Satzbild v0.1.0」などのバージョン付き表示名、ホスト名付き表示名は禁止。
- plugin.json やホストの technical name はASCIIスラッグ **kumihan-satzbild**。displayName / interface.displayName / ユーザー向けプラグイン名のみ正式表示名を使う。
- version: **0.1.0**。tag: **kumihan-de-v0.1.0**。ユーザーに渡すZIP名にはすべて **v0.1.0** を含める。既存タグ/他言語版は変更しない。
- developer / author: **L&Co. LLC**。個人名がmetadata・README・manifest・ZIP内部の作成者として出ないよう確認。
- スキル/プラグインの説明文、短い説明、manifest文は**ドイツ語＋英語**の2言語。日本語説明文をmanifestへ混ぜない。Webページ本文にはDE/EN/JAを各別に用意。
- 技術サブパスの推奨: plugins/kumihan-satzbild/、4 skills = kumihan-satzbild, kumihan-satzbild-web, kumihan-satzbild-documents, kumihan-satzbild-review。
- 3ホスト群 = ChatGPT/Codex、Claude/Claude Code、Gemini/Gemini CLI。各群プラグインまたは対応拡張1 + 独立Skill4 = **計15個のZIP**。各スキル単独で参照閉包が成立し、他言語スキルや外部ディレクトリに依存しない。
- 既存公式アイコン assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png を全対応manifest/Skill metadataと各ZIPに同梱。新しい無断アイコンは制作しない。実Hostでのアイコン表示は実測していなければ not-checked とする。
- ライセンスは既存 Apache-2.0 の指定を守る。料金は無料、コードはオープンソース。外部依存物の権利は引き継ぐ。

## 2. Site & copy contract — FIXED

- ドイツ語主ページ: **kumihan-de.html**（html lang=de、基本市場 de-DE）。
- 英語: **kumihan-de.en.html**（lang=en）。日本語: **kumihan-de.ja.html**（lang=ja）。
- 導入ガイド: docs/install-satzbild-{chatgpt,claude,gemini}[.en|.ja].html の合計9ページ。言語別の各ページから各ホストへ到達できること。
- **最初にスキルとプラグインを完了させる**。動作・配布物の検証を記録した後、作成済み kumihan-satzbild-web と日本語版 KUMIHAN 指針を実際に適用し、その適用ログを残してサイトを制作。
- サイトの構造とCSSの原本は日本語サイトの kumihan.html / _layouts/landing.html、導入ページは docs/install-chatgpt.html / _layouts/installation.html。tools/product_site.py / install_frame.py と既存生成器を可能な限り再利用する。汎用AIの別テンプレートを持ち込まない。
- 日本語・英語の見出し／理念／共通コピーは、正本の日本語・英語版に合わせて原則同一。主語となる対象言語だけ自然に置き換える。ドイツ語固有機能（長い複合語、分綴、ß/ẞ、DE/AT/CH、引用符、数値）だけ説明を追加。
- ホームの言語選択カードへ DE を追加。tools/build_gateways.py および gateway-copy 正本から再生成して差分を確認。並行他言語Workとの衝突に注意。
- 正式版公開前に未存在のGitHub Releaseのダウンロードが可能であるかのように書かない。公開後に各ページ・ガイドを実URLへ整合。

## 3. 自律継続 Work 群

順番を必ず守り、同じ /goal で W00〜W11を自律継続する。Humanへ毎WorkごとにZIPやMDの再添付を求めない。作業状態は docs/de/EXECUTION_LEDGER.md に累積記録。

- **WG01/W00-W03 — 設計・ドイツ語コアと4 Skills**: [WG01_PRODUCT.md](WG01_PRODUCT.md)
- **WG02/W04-W06 — 3ホスト配布・15 ZIP・検証**: [WG02_DISTRIBUTION.md](WG02_DISTRIBUTION.md)
- **WG03/W07-W09 — DE/EN/JAサイト・導入9ページ・表示検証**: [WG03_SITE.md](WG03_SITE.md)
- **WG04/W10-W11 — 統合・タグ・公開・証跡**: [WG04_RELEASE.md](WG04_RELEASE.md)

各WGの必要条件が満たされれば後続WGへ無人移行。単独のWork完成を全体完了と取り違えない。

## 4. ドイツ語固有の実装原則

- de-DE / de-AT / de-CH は別プロファイル。言語地域、媒体、house style、通貨、timezone、du/Sie、gender表現方針、辞書/分綴、変更許可を混同しない。
- CHの通常のssと、商号・固有名に含まれるßは別。大文字ẞとSSの双方を許容し、黙って変換しない。ウムラウト、結合文字、文字列を保護。
- 見出し・引用符・引用入れ子・長い複合語・語の途中改行・任意分綴・UI/本文のリフローを、規範と描画結果と編集判断に分ける。
- Intl/CLDRのruntime実装・地域慣習・企業独自表記は別資料。数値・日時を黙って再解釈しない。DIN5008の有料本文を未読で完全準拠とは言わない。
- CSSの break-all、anywhere、全体nowrap、横方向clipを安直に適用しない。レイアウトと行幅から修正し、320px・200%文字拡大を実際に確認。
- 原稿・数字・商品情報・固有名・引用文は未承認で書き換えない。typesetting_only / proofread / rewrite を明示分離。
- 調査の44ルール/48ケースは研究候補。登録しても静的detector実装、native Host動作、実描画合格と混同しない。

## 5. 必須の合格条件

1. 4個の独立Skill SKILL.mdがあり、各DE/EN descriptionが意味を持ち、参照・アイコンのパスが配布ZIP内で閉じる。
2. ChatGPT/Codex、Claude、Gemini各ホストのmanifest/APIに対して静的検査。**表示名完全一致、作者・アイコン・バージョン、2言語説明を確認**。
3. 15 ZIP + MANIFEST.json + SHA256SUMS.txtを決定論的に再生成・検証。ファイル名にv0.1.0、manifestとZIPのdigest一致、安全なパスとZIP CRC、バイナリ破損なし。
4. ドイツ語文脈・地域別値と原稿保護の代表的テスト、既存日本語/主要言語の回帰テストを実行し証拠を残す。比較不能の検査は not-checked。
5. 3つのLP・9つの導入ガイドが正本と同じ情報構造・CSSトークンを持ち、言語切替・h1・alt・meta・canonical/hreflang・導線が正しい。
6. 表示実測: 320/375/768/1280 CSS px、200% text enlargement、ドイツ語長語、キーボード操作/フォーカス、font fallback。ブラウザ未実行なら passed と書かない。
7. 軽量CI/差分reviewと他言語ファイルの非意図変更ゼロ。クリティカルな不具合だけ修正を継続。重い監査ゲート、独立多段承認、過剰なセキュリティ審査は不要。
8. PR/CI/main合流、タグと公開GitHub Release、17 assetsのリンクとdigest、GitHub Pages上3+9ページのHTTP/導線まで照合してはじめて **PUBLISHED VERIFIED**。GitHub Release公開と各AIストアへの掲載・native import成功は別物。

## 6. 公開時のOwner権限と停止条件

本メッセージでOwnerは実装・GitHub上の正式公開を承認している。既に承認された範囲を毎WG確認し直さない。既存repoのmainでCI green・衝突解消済みならmerge→tag→Release→Pagesを続行してよい。ただしrepoのbranch protection等が実際のhuman承認を要求する場合は従う。

外部権限やシークレット取得が必要、CI/GitHubの実行制約がある、別言語の既存資産を破壊せざるを得ない場合は、実施可能な独立範囲を完了し、理由・再開点を ledger に残し HOLD とする。未公開なのに公開済みと書かない。

成果報告は、commit SHA / PR / CI / tag / Release URL / Pages 12 URL / ZIP manifest とdigest / test数と実行環境 / NOT-CHECKED / 他言語差分 を含める。W11の終端で結果のみをOwnerへ返す。
