# W02 — MCP契約・注釈 検証仕様

状態: 静的確認済み、パッチ未作成、本番変更未承認。

| Tool | 読み書き・通信の静的根拠 | 注釈候補 |
|---|---|---|
| kumihan_list_languages | Registryのローカルカタログ参照 | readOnlyHint=true / destructiveHint=false / openWorldHint=false |
| kumihan_detect_language | 入力とローカルRegistryによる候補判定 | 同左 |
| kumihan_get_guidance | ローカルルール先頭1〜25件返却。媒体別絞込みではない | 同左 |
| kumihan_review_text | 原稿不変、候補返却、checked=[]、not_checked明示 | 同左 |

これは注釈の設計根拠であり本番tools/listの観測ではない。全4 addToolには現ソース上明示annotationsがない。外部ユーザー資源の変更はないが内部FileSessionStore/Lockの書込みはある。SDKの保存対象と外部ネットワークを依存ソースまで調べて最終値を決定する。

## 最小パッチ手順

1. PHP 8.5とComposerで依存解決し、mcp/sdk 0.9.xのaddTool annotations引数およびToolAnnotations実クラスを確認。推測したAPIで書かない。composer.lockは現コミットにない。解決版とaudit結果を記録する。
2. testsで実HTTP tools/listから4ツールの3注釈を検証。未登録locale/medium、30,000 bytes本文境界、64KiB HTTP境界、不正UTF-8のプロトコル応答・機密非露出を検証。
3. public/index.phpの4宣言だけを変更してPHP lint、既存smoke、HTTP smoke、Composer auditを実行。LanguageRouter.phpの変更は禁止。
4. セッションの保存項目・TTL・GC、ログ、WAF、呼出制限を運用担当と確認。未知値をコードから本番設定として推認しない。

## 限定展開と復旧（実行前Owner Gate）

対象はサーバーprivate runtimeの注釈宣言の最小差分のみ。現在ファイルの安全なバックアップとSHA、差替えファイルのSHA、SDK互換、private/public配置を確認してからOwnerに提示。既存router修正を丸ごと含むアーカイブは配布禁止。適用後initialize/tools/list/4 tool呼出しとPlatform Scan Toolsの注釈読戻しを記録。失敗時は当該ファイルをバックアップから復旧し再測定。承認commit・対象・期限・実行者を記録するまで実行しない。

このCloud環境にはPHP/Composerがなく、パッチを検証できていない。4注釈最終値、SDK例外、セッション実保存、HTTP境界、Platform scanはNOT_CHECKED。次はPHP 8.5が利用できるCodex環境で上記を連続実行。
