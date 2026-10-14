# KUMIHAN

Open-source skills for Japanese typography and high-quality AI-generated websites and documents. Designed to eliminate generic AI aesthetics.

> **Status / 開発状況:** v0.1 is under development. No release or installed-host compatibility is verified yet.  
> **v0.1は開発中です。** 正式リリースおよび実行環境での動作確認は未完了です。

## 日本語での紹介

**KUMIHAN** は、AIを使って日本語のWebサイト、文書、プレゼンテーション資料を制作する際に、日本語の文字組み・情報設計・可読性・デザイン品質の向上を支援するオープンソースプロジェクトです。

日本語組版に関する技術資料や実務上の知見を参考に、改行・禁則・約物・和欧混植・書体・余白などを媒体に応じて扱います。同時に、内容や目的に関係なく同じレイアウトを繰り返すような画一的なAIデザインを避け、**伝える内容に適した構成**を重視します。

### v0.1で計画しているSkills

| Skill | 役割 |
| --- | --- |
| `kumihan` | 目的・媒体・制作条件に応じて必要な指針を選択 |
| `kumihan-web` | Webサイト・記事・UIの日本語組版とレイアウトを支援 |
| `kumihan-documents` | 報告書・プレゼン資料の文字組みと情報構造を支援 |
| `kumihan-review` | 既存の制作物を原則として変更せずにレビュー |

原稿・数値・商品名などの保護や、実際に確認できた範囲を正確に報告することも重視します。現在検討している38件のルールは**制作・レビューの指針**であり、38件の自動検出機能を実装済みという意味ではありません。

KUMIHANは独立して設計・実装しており、Hallmarkのコード・文章・素材は取り込んでいません。

詳しい日本語利用ガイドは[開発中のドキュメントPR #5](https://github.com/landco-llc/kumihan/pull/5)で準備しています。正式な導入手順と対応環境はv0.1の検証後に案内します。

## License / ライセンス

[Apache License 2.0](LICENSE)
