# KUMIHAN｜Equilibrio v0.1.0 — /goal 実装・公開マスター指示

Status: OWNER_APPROVED / IMPLEMENTATION_NOT_STARTED
Date: 2026-10-19 JST
Repo: https://github.com/landco-llc/kumihan
Execution: Codex Cloud / Codex App の /goal。一回の起動で W00–W11 を自律継続。Remote Desktop Commander経由のローカルCodex CLI起動は不要。
Product: KUMIHAN｜Equilibrio (Italian edition)
Owner-approved scope: 4 Skills・3ホスト対応の独立製品実装、ZIP配布、日英伊サイト、導入ページ、軽量CI、main統合、GitHub公開Release、GitHub Pages確認。外部プラグインマーケットへの投稿、他言語製品の変更、認証・権限変更は含まない。

## 0. Fresh Read — まず正本を実読

1. リポジトリ main の最新SHA、既存PR・branch・CI・Release、AGENTS.mdや配下規則を確認。別言語Workが進行中なので衝突を回避する。既存PR #76 は日英共通コピーに関する変更が含まれていた。開始時点で最新状態を再確認すること。
2. 日本語基準: kumihan.html / _layouts/landing.html、英語 en.html、docs/install-chatgpt.html / _layouts/installation.html、assets/kumihan-install.css と .js。
3. 共通サイト構造: tools/product_site.py、tools/install_frame.py、tools/base_copy.py、tools/build_gateways.py、tools/web_fonts.py。ドイツ語版の実行例: docs/de/GOAL_SATZBILD_V010.md、tools/build_satzbild.py、tools/build_satzbild_site.py、.github/workflows/{satzbild,publish-satzbild}.yml。参考にするが盲目的にドイツ語の規則は流用しない。
4. イタリア語研究の再利用可能なスナップショット: docs/it/ITALIAN_RESEARCH_20261019_JA.md。元の調査正本はGoogle Drive KUMIHAN/RESEARCH/IT: https://drive.google.com/drive/folders/1EMib8ugMHyfNG2e38Mo7vuAX79a3iiGk （Markdown: https://drive.google.com/file/d/1p-q1oEXzibI7TXdRjtHgEdBtaPqJkPmL/view）。調査の40規則/48評価ケースは候補であり実装済み機能/試験成功を意味しない。
5. 先に同名製品・同じタグ・関連PR・既存ファイルの有無を探し、二重実装を避ける。先行成果がある場合は破壊せず継続・照合する。

## 1. Identity / scope — 固定事項

- 表示名: **KUMIHAN｜Equilibrio**。全角縦棒 U+FF5C。人間に表示するplugin名へホスト名、版数、Italy edition等の接尾辞を付けない。
- technical slug: kumihan-equilibrio（ASCII）。nameとdisplayNameのAPI要件を区別。version: 0.1.0。GitHubタグ: kumihan-it-v0.1.0。全てのZIPファイル名に v0.1.0 を入れる。既存他言語tagを動かさない。
- developer/author: **L&Co. LLC**。個人名を新規manifest、README、ZIP内作成者、コピーへ含めない。
- pluginと各Skillの description/short/long は **イタリア語＋英語**の2言語で意味対応。Webページは IT・EN・JA の3言語に分ける。Skills名/技術IDはASCII、公開表示名は全プラグインで厳密に正式名のみ。
- product path: plugins/kumihan-equilibrio/。Skills: kumihan-equilibrio、kumihan-equilibrio-web、kumihan-equilibrio-documents、kumihan-equilibrio-review。それぞれ単独ZIPとして参照が閉じる。媒体別制作とread-only reviewの4スキル構成を守る。
- 3 host groups: ChatGPT/Codex agent plugin + 4 standalone skills、Claude/Claude Code plugin + 4 standalone skills、Gemini/Gemini CLI extension + 4 standalone skills = 合計15 ZIP。host-native UI / marketplaceでの成功は検証した場合のみ主張。
- 既存の公式logo: assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png を使い、manifestの相対pathと各ZIP実体を検査。新規ロゴ生成は禁止。オープンソース、無料、Apache-2.0、第三者権利を継承する。

## 2. イタリア語機能の境界

- it-ITを基準として it-CH を別localeで表現。一般localeとEU/スイス機関固有のhouse-styleを独立した設定にする。通貨・数値・日付の再解釈はしない。
- source_fidelity / medium / content_role / house_style / locale / editorial voice / evidence を混ぜず、typesetting_only・proofread・rewriteを明確に分ける。原稿の無断変更なし。reviewはread-only。
- 必須の保護・反例: è/é/È、perché/caffè、e/è・da/dà・si/sì、qual è、po’とPo、原著引用、固有名、外国語、URL・JSON・JS・識別子、NFC/NFD元バイト、文字結合、数値・通貨・日時の元値。
- 文字組の例外: Accademia della Cruscaはアポストロフィ直後の改行を認める。無条件に禁則・errorとしてはならない。見出しでの改善は任意のデザイン提案。引用符は caporali方式・英式二重引用符・原著忠実引用の複数編集方針を許容。
- CSSの hyphens:auto や text-wrap:balance があるだけで「辞書分綴が働く」「意味に沿って改行できた」と判定しない。描画結果と仕様の静的チェックを分離。
- イタリア語を単一の書体・色・デザインで縛らない。AI的な画一テンプレートや理由のないカード/グラデーション/強調を抑える一方で、伝達目的のある大胆な造形は認める。
- 40の研究規則と48の評価案を source_refs / severity / context / scope / expected / status で紐付ける。全40個を完全な自動判定器として実装する必要はない。未測定は not-checked、判断困難は needs-review。実際の測定結果を偽装しない。

## 3. 正本コピー / サイト契約

- 主ページ: kumihan-it.html（lang=it / 基本locale it-IT）、kumihan-it.en.html（lang=en）、kumihan-it.ja.html（lang=ja）。
- 導入ページ計9: docs/install-equilibrio-{chatgpt,claude,gemini}[.en|.ja].html。プレフィックスは install-equilibrio- とする。
- サイト制作は「製品完成 → 15 ZIP実体/manifest/チェック → 完成した kumihan-equilibrio-web と日本語版 KUMIHAN指針を実読・適用 → 3主ページ・9導入ページ」を厳守。適用した規則とデザイン上の判断を docs/it/DESIGN_APPLICATION_RECEIPT.md に残す。
- ページ構造・CSSは日本語版 _layouts/landing.html と tools/product_site.py 由来の8 sectionsを再利用。導入ガイドは _layouts/installation.html / tools/install_frame.py と既存CSS/JSから生成。別物のAIテンプレートへ差し替えない。
- **英語と日本語のコンセプト・理念・タイトル・主要コピーは tools/base_copy.py のJA/EN辞書を正本にする。** 言語名/製品名だけ置換し、イタリア語固有のfeature 01、原稿保護、地域差、導入事実だけ個別説明。主ページh1は日本語「イタリア語の／デザインを／もっと自然に」、英語「Natural Italian typography,／made with AI」を基準にする。
- 日本語<title>: KUMIHAN｜Equilibrio — イタリア語のデザインをもっと自然に
- 英語<title>: KUMIHAN｜Equilibrio — Natural Italian typography, made with AI
- イタリア語コピー案（母語話者確認未済）: 「Il design in italiano, più naturale」および「Ogni parola al suo posto」。正式採用は文脈・ブランド理念と照合し、校閲の実施有無を記録。日本語・英語コピーをイタリア語へ強引に逐語訳しない。
- リンクは実在するrelease filenamesに一致。言語切替、canonical、hreflang、OG、alt、フッターL&Co. LLCのcorporate外部リンク（新規タブ・rel）、導入ページ間導線を検証。
- index/言語選択ゲートウェイへITカードを追加。tools/build_gateways.py / assets/gateway-copy.jsonを正本として再生成する。既存カードサイズ・将来追加前提を保つ。他言語の生成出力を無差別上書きしない。

## 4. 自律継続する Work 群

同一/goal中にW00〜W11を必要な範囲で連続実行。単一Work終端を製品完成と誤認しない。Ownerに毎WGで新規MD・ZIP添付を求めず、repoとledgerを引き継ぐ。

- **WG01 / W00–W03** 研究ハンドオフ、製品基盤、4 skills、原稿保護、core fixtures: WG01_PRODUCT.md
- **WG02 / W04–W06** ChatGPT/Codex・Claude・Geminiの静的adapter、15 ZIPの再現ビルドとlight tests: WG02_DISTRIBUTION.md
- **WG03 / W07–W09** スキル適用ログを先行させた伊英日サイト3 + 導入9 + IT言語カードと表示チェック: WG03_SITE.md
- **WG04 / W10–W11** light review、CI/main統合、公開tag/Release17assets/Pages、結果読戻し: WG04_RELEASE.md

状態は docs/it/EXECUTION_LEDGER.md に必ず累積記録する。未着手/進行/失敗/保留/成功の違いを残す。

## 5. Release Acceptance / 禁止事項

1. **4 Skillsが独立**し、各相対参照閉包・IT/EN説明、例示、rules/sources/fixtures/locale、公式アイコンを収録。対応範囲と動作保証を混同しない。
2. host manifestは配布先の既存・現在の仕様に対して静的検査。表示名、version、L&Co. LLC、logo path、説明の2言語、technical slugの一致。
3. **15 ZIP + MANIFEST.json + SHA256SUMS.txt** を決定論的にビルド、--check非書込、CRC、パス、メンバー一覧、digest照合。ZIP名は全て v0.1.0。
4. イタリア語特有の保護反例と代表的な正例テスト、既存日本語・他言語の回帰。40規則の登録/48候補の評価状態は実装済み・PASSと同一視しない。
5. 3 LP + 9導入ページはcanonical構造・CSSを継承し、h1/タイトル/日英共通copy/link/lang/canonical/hreflang/alt/ariaを確認。Italian見出し・アクセントglyphと引用符の表示を実際に見る。
6. ブラウザが使える環境で320/375/768/1280 CSS px、文字拡大200%、文字間隔上書き、横はみ出し、フォーカスとキーボード、fallback表示を確認。未実行環境はnot-checked。CSS simulation≠native zoomと明記する。
7. レビューは軽量でよい。関連テスト/CI PASS、重要ブロッカー0、他言語の既存distribution/ZIP汚染0、並行PRとの衝突解消を重視。有料のセキュリティ監査・多段Owner Gateを要求しない。
8. Merge SHA・固定tag・公開GitHub Release(draft=false)に**15 ZIP + MANIFEST + SHA256SUMS=17** assets、配布digest/readback、Pagesの12URLのHTTPとリンク実体を確認して初めて **PUBLISHED_VERIFIED**。GitHub公開はClaude/Gemini/ChatGPTの公式ストア掲載やnativeインストール成功とは異なる。

## 6. Owner承認と停止条件

この依頼でOwnerはGitHubへのv0.1.0公開まで承認済み。標準的なPR/CI/main merge/tag/Release/Pagesは毎回確認せず連続実行してよい。ただしGitHub保護規則、外部権限/シークレット、重要な並行変更の破壊には勝手な回避・強制push・権限変更をしない。進められない工程だけHOLDし、他の完了可能部分、原因と次の起動点をledgerへ残す。

既存releaseが同じtagに別SHAで存在する場合は破壊せず照合してHOLD。本文未完成・ZIP未公開なのに公開済みと書かない。関連外のコードや言語サイトを変更しない。release後もnative providerの表示と動作が未確認なら明記する。

終端の報告は commit SHA / PR / checks / merge / tag / Release URL / 15 ZIP digest+manifest / Pages12件+gateway / focused regression 数と環境 / NOT-CHECKED / 他言語への影響 / 欠落項目と再開点。HumanからZIP/MDを再度受領する運用には戻さない。
