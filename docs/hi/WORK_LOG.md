# 実装台帳 — KUMIHAN｜अक्षर-संगति v0.1.0

## W00 Fresh Read
- 2026-10-19 JST: origin/main 0492307 をfetchし、新規branchを作成。作業ツリーはclean。AGENTS.mdなし。
- GOAL.md、研究PDF抽出、研究全文Markdown、Requirements（Drive HIフォルダ）を読了。研究の観測を製品PASSへ転記しない。
- 既存compasso/accord/arのmanifest、builder、共通product_site/install_frame、base_copyとlanding、日本語master・gatewayを基準にする。
- 実行方式はOwner指定の連続自律実行。設計はGOALを正本とし、4独立Skills→3ホスト→15 ZIP→12ページ→検証→PR/merge/release/Pagesの順。
- 研究原資料は私有Driveのまま保持し、公開製品には必要なルール・出典・fixtureのみを実装。第三者画像は再配布しない。

## 実装計画と確認観点
W01: 24ルール・24fixtures・read-only比較（NFC同値でもbyte差を検出）。
W02: 全Skillsへルール・source index・locale・runtime・公式iconを同梱。
W03: ASCII IDと正確な表示名、Hindi→Englishのdescription、ホスト別導入。
W04: 安全な相対path・安定timestamp・15ZIP・size/hash・再現性を検証。
W05: 新Hindi web/reviewと既存日本語KUMIHAN guidance適用、共通JA/EN copy、Hindi固有例。
W06–07: 狭幅・拡大・spacing・fallback・リンク・byte保持・既存回帰、実測とNOT_CHECKEDを分離。
W08–10: focused CI後PR/merge、固有tag、全assetと12公開pageのHTTP確認。

## W01–W03
24 rules/24 QAをRequirementsから対応付け。55件source index、6 profiles、hi-IN locale、byte比較を実装。4 standalone Skillsは参照・runtime・iconを自己完結同梱。portable/Codex/Claude/Gemini manifestsを作成。Claude/Geminiの未対応displayName/icon keyは追加せずSkill/contextに正式名を表示。実ホスト導入はNOT_CHECKED。

## W04 配布物完成
15 ZIPを生成し、2回のbuildの全byte一致、SHA256/size、相対path・非symlink・全icon・全4独立Skillの自己完結をテスト。focused tests 4件PASS。ここまでサイト制作なし。各ホストUI実導入はNOT_CHECKED。

## W05 サイト制作
配布物QA完了後にHindi web/reviewおよび既存日本語KUMIHAN web/reviewを読んで適用。SITE_AUTHORING.md/COPY_MATRIX.jsonにbriefとルール適用を記録。共通product_site/install_frameから3 LP＋9導入ページを生成。JA/EN generic copyはbase_copyと一致。gateway共通カードへHindiを追加し既存CSS/会社footer挙動を維持。Noto Sans Devanagari 2.007/OFLを自サイト配信。

## W06 実測と修正
Chromium 154.0.8037.57で12ページ×3幅×4条件（通常/文字200%/4種spacing同時override/webfont失敗）=144観測。初回は文字200%のSkill IDとcodeに9件overflowを観測し、ASCII識別子とpre codeだけ局所折返しを修正。再検証中。
Q01–19はfixtureの原稿とDOMのUTF-8 round-tripが19/19一致。描画見本を確認し、母音記号・結合・上下空間に明白な欠けなし（AI補助による限定視認、母語校正ではない）。Intl.SegmenterはZWNJの境界を含む実測値を記録、普遍解扱いなし。PDF抽出は19文字列中17がそのまま一致し、2件は不一致。PDFの見た目だけで原文再利用を保証しない、Markdown/編集可能原稿を正本とする。Office/実機/IME/支援技術/母語校正はNOT_CHECKED。QA全体24件PASSとは表明しない。

## W07 自動テスト
Hindi focused 7件PASS、既存root 11件PASS、compasso 8件/accord 26件/arabic 20件/grafia 13件PASS。build_dist --check（128生成物）、JA-TYPE-011 11fixture、base_copy/gateway/site生成一致を確認。既存gatewayリンクtestへ新言語hi→indexの期待値と新12ページを追加（初回KeyErrorの原因）。focused Hindi GitHub Actionsを追加。

## W08 軽量レビュー
requesting-code-review skillに従い独立read-only reviewerへ新規製品とGOALの照合を依頼。15 ZIP/manifest/自己完結/byte比較/12ページ/共通copyを確認し重大ブロッカーなし。ネイティブホスト導入と公開可用性は別途確認対象。

### W06/W07 最終確認
修正後Chromium 144/144のgeometry観測でoverflow 0。これはfont-sizeの実測2倍でありブラウザUI zoomそのものはNOT_CHECKED。通常描画の320/1280 screenshotとfixture screenshotを保存し限定視認。ソースhashは読取前後一致。ja/en gateway×3幅の6観測で全10カード同一寸法・overflowなし・もっと見る展開・会社URL target=_blankを確認。最終focused suiteは8件PASS（文字破損変換の拒否を追加）。root11/compasso8/accord26/arabic20/grafia13と合わせ86件PASS。再現可能なbrowser_qa.py/fixture_qa.pyを保存。browser-results.json、qa-results.json、gateway-results.jsonを根拠とする。

### W08 CI差分の解消
初回CIはルートTHIRD_PARTY_NOTICESの追記が既存日本語ZIPの内容へ影響したため失敗。追記を取り消し、新規fontのOFL/READMEへ通知を集約し既存128生成物の一致を復旧。さらに作業中mainにPR #68（77595b1、日本語heroの3行化）が入り、PRのmerge試験でcopy parity不一致が発生。origin/mainを再fetch/mergeし、共通copyからHindi日本語LPを再生成。主言語本文を変更せず、影響する日本語LPの12条件を再計測。
Gateway Hindi glyph/title/brandにも局所font-faceとnormal trackingを適用し、共通Latin trackingがIndicへ入らないようにした。ja/en×3幅の6条件でフォント読込後もカード同寸法・normal tracking・overflowなしを再確認。

## W09 マージ・タグ・公開
PR #71をmain 5b7057366621ace37fd36185450bfe0d7282846cへマージ。直前のmain dd81733（ベトナム語版）との生成HTML/test mapping競合を両言語保持で解消。統合後root11/focused8およびfocused CIを確認。両言語を含む11カードをja/en×3幅で再測定し同寸法・normal Hindi tracking・overflowなし。
タグkumihan-hi-v0.1.0は上記main SHAを指す。gh release createのasset uploadはCloudのuploads.github.com接続先制限で拒否され公開前に失敗したため、既存publish-ar方式と同様のGitHub Actions公開経路を追加。タグ/期待SHA固定、17assetのsize/digest検証後のみpublic化、既存public/添付済release上書き禁止。
Claude Code 2.1.302 / Gemini CLI 0.64.0の実CLI manifest validatorsがPASS（host-validation.json）。実ホストのモデル呼出し・accountへの導入とは別。
