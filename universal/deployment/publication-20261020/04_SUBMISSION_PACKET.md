# W04 — 申請説明・デモ原稿（ドラフト）

製品: KUMIHAN Universal / kumihan-universal / v0.1.0 / L&Co. LLC / Productivity。Platform識別は引き継ぎ値で独立読戻し待ち。

EN: Reference typography guidance for 21 language modules, with conservative text review that preserves your source. Specify a language or locale to retrieve source-backed advice for web pages, documents and presentations. Preview modules remain unverified in target rendering environments. This service does not automatically certify layout or editorial quality.

JA: 21言語モジュールの文字組参照ガイダンスと、原稿を保持する保守的なテキストレビューを提供します。言語やlocaleを指定してWeb・文書・プレゼンテーション向けの助言を参照できます。各モジュールはプレビュー段階で、対象環境でのレンダリング検証や自動品質認定は行いません。

## Starter prompts（3件）

1. 日本語（ja）のWeb向け文字組ガイダンスを表示してください。
2. 繁体字中国語（zh-Hant）の次の原稿を変更せずにレビューし、未検証の項目を示してください：文字，排版。
3. アラビア語（ar）の文書用ガイダンスと、実際のレンダリングで確認が必要な点を教えてください。

## Release notes候補

初回プレビュー。4 MCPツールを通じて言語一覧、保守的な言語候補、参照ガイダンス、原稿不変レビューを提供。21モジュールはpreview_unverified。自動ルール実行・視覚検査は提供しない。既知の自動判定問題は別管制で対応中で、解消証拠受領までは公開不可。固定ルール総数を宣伝しない。

## 90秒デモ脚本

0〜15秒: 製品名・版・プレビュー制約を表示。15〜30秒: list_languagesで21モジュールとpreview_unverifiedを表示。30〜50秒: ja / webのguidanceを呼び出し、候補ルールと出典を説明。50〜75秒: zh-Hant明示の原稿レビューでsource_unchanged、checked=[]、not_checkedを表示。75〜90秒: arの参照ガイダンスと実レンダリング未検証、個人情報は公開Issuesに書かない旨を説明。

最終版実機で録画し、レビュアーがログイン障害なく視聴できるURL・録画日時・commit/配備版を記録する。現時点で録画未実施、動画URLなし。静止画や脚本を動画完了と扱わない。

Annotation justificationは02を参照し、デプロイ後のtools/listと一致させる。無料・公開地域・サポート窓口はOwnerの設定確認待ち。説明文の入力と保存はまだ行っていない。
