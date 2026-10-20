# W01 — 法務・データ処理 起案（未承認・公開禁止）

目的: Ownerと運用担当が公開文面と実態を照合できる英日レビュー原稿。媒体はMarkdown、画面閲覧。既存サイトHTMLの変更・公開はまだ行っていない。

## 確認できた処理と未確認

ソース: universal/server/public/index.php / src/UniversalTools.php / src/LanguageRouter.php（PR #101 HEAD）。入力はHTTPS MCPリクエストとして受信し、サーバー内で言語候補・ガイダンスを生成。各ツールに外部API呼出しやユーザーファイルの変更は見当たらない。FileSessionStore / FileSessionLockを利用。HTTP body上限64KiB、router本文上限30,000 bytes。SDKセッションが実際に保存するフィールド、TTL、GCとバックアップの残存、ロリポップアクセス/エラーログの本文・IP・保持期間・権限は未確認。ゼロ保存・ゼロログとは宣言しない。

Owner確認が必要: ホスティング契約上の委託先と処理国、ログ設定/保持日数、セッション削除タイミング、バックアップ保持、管理権限、削除依頼の手順、私的問い合わせ先、濫用制限と停止責任者。

## Privacy 英日差替え候補

EN: KUMIHAN Universal is a hosted MCP service operated by L&Co. LLC (Japan). When your AI client calls a tool, it sends the selected text and tool parameters to our HTTPS MCP endpoint. The server uses these inputs to resolve language candidates and return reference guidance. The tools do not edit your original documents. Your AI provider processes your conversation under its own policies. Hosting and protocol operation may process technical information and session data; the exact fields, retention periods, deletion procedures and processors must be confirmed before this draft is published. Do not submit confidential material until you have reviewed the final service policy. Public GitHub issues are visible to others; use the confirmed corporate private support route for personal information.

JA: KUMIHAN Universalは、L&Co. LLC（日本）が運営するホスト型MCPサービスです。AIクライアントがツールを呼び出すと、対象のテキストとツール引数が当社のHTTPS MCP接続先へ送信されます。サーバーは言語候補の判定と参照ガイダンスの返却に使用し、原稿ファイルは編集しません。会話に関するAI提供者の処理には各社のポリシーが適用されます。ホスティングと通信処理では技術情報やセッション情報が処理される場合があります。保存項目、保持期間、削除手順、委託先は公開前に実態を確認して確定します。GitHub Issuesは公開されるため、個人情報の問い合わせには確認済みの法人窓口を使用してください。

上記の未確定文は公開用の完成文ではない。確認結果を具体的に記載後、英日正本と既存全翻訳を同期する。「L&Coへ送信しない」は静的Skill単体に限定し、ホスト型MCPとの適用範囲を分ける。

## 利用規約 英日レビュー候補

EN: L&Co. LLC provides KUMIHAN Universal as a free preview service for multilingual typography reference guidance and conservative, source-preserving text review. It does not certify rendered layout, font coverage, semantic quality or compliance. Language routing can be uncertain; specify the locale and confirm advice in your target application. You retain your rights in submitted text and must have authority to provide it. Do not use the endpoint to disrupt the service or process unlawfully obtained material. We may restrict requests or suspend the service for maintenance or abuse prevention. Open-source software remains governed by its applicable license. Service terms, liability provisions, applicable law, dispute venue, effective date and private support contact require Owner approval before publication.

JA: L&Co. LLCは、多言語の文字組参照ガイダンスと原稿を保持する保守的レビューのため、KUMIHAN Universalを無料のプレビューサービスとして提供します。レンダリング、フォント収録、意味内容、法令適合を保証するものではありません。言語判定には不確実性があるため、localeを明示し、対象アプリケーションで助言を確認してください。入力原稿の権利は利用者に帰属し、入力に必要な権限は利用者が確保します。サービスを妨害する利用や違法に取得した資料の処理には使用できません。保守・濫用防止のため、呼出しの制限や提供停止を行う場合があります。オープンソース部分には各ライセンスが適用されます。責任制限、準拠法、紛争管轄、発効日、非公開窓口はOwner承認後に確定します。

## サイト差分の実行仕様

mainのprivacy.htmlの1ページ多言語構造・全id・言語切替・既存CSSを保持。privacy-ja.html互換リンクを維持。英日を確定後に全翻訳更新。terms.htmlは英日で既存サイト共通デザインを使い、ナビ/フッターに導線を追加。未確定原稿をサイトrootに置かない。

検証: 差分から既存言語sectionとanchorが全て残ること、内部リンク、lang/dir、キーボード操作を確認。承認済みcommitだけ公開し、公開後HTTPS 200・文面一致・Platform URL一致を実測。戻しは当該サイトcommitのrevert。現状: DRAFT / 事実確認待ち / HTML差分未作成。
