# KUMIHAN SEO運用正本（開発中）

**Status: DESIGN/IMPLEMENTATION PENDING.** この文書は実装完了を証明しない。

- SEO実装指示正本: [SEO v1.0 指示書](../specs/KUMIHAN_SEO_FOUNDATION_IMPLEMENTATION_20261019.md)
- 正本となる構成: `assets/gateway-copy.json` / `tools/build_gateways.py` / `_layouts/landing.html` / `tools/product_site.py` / 各言語固有ビルダー
- 追加・変更手順: [ADD_LANGUAGE_OR_PAGE.md](ADD_LANGUAGE_OR_PAGE.md)
- 設計判断: [DECISIONS.md](DECISIONS.md)
- 検証実績: [VALIDATION_LOG.md](VALIDATION_LOG.md)
- ページ一覧: `BASELINE_INVENTORY.md`（W00で生成・更新）

## 不変ルール

1. ページのtitle/description/langなどの文言は**ページの既存コピー正本**を優先。SEOだけ別の翻訳正本を作らない。
2. canonicalは絶対HTTPSの公開URL。言語が違うページを英語など単一URLへcanonicalでまとめない。
3. hreflangは実際に存在する翻訳URL同士のみ、自己参照・相互参照をチェックする。
4. サイトマップはcanonicalで集計した公開ページのみ。架空の変更日・存在しないURLを記載しない。
5. 静的HTMLのheadにOGPとJSON-LDを出す。JavaScriptでクローラー用のタグを後付けしない。
6. 生成済みHTMLのみ編集禁止。生成元と生成物の一致テスト必須。
7. 新言語・ページを追加したPRでSEOの自動チェックを必須にする。
8. GA4、クローラー学習許諾、Cookie、AI検索ランキング対策はこのWorkに含めない。
9. P0未実装・未検証の項目を「導入済み」と記載しない。

## GitHub Pages注意事項

`https://landco-llc.github.io/kumihan/` はプロジェクトサイト。`/kumihan/robots.txt` はホストルートの `/robots.txt` と同じ扱いにはならない。所有権・ホストルート管理の可否を確認するまでrobots.txtを安易に追加しない。Search Consoleでの所有権確認・Sitemap送信は実装PRとは独立したOwner操作。

## Codexによる完成後に記録する項目

- SEO共通ライブラリ・設定正本とエントリポイント
- 生成・検証の実際のコマンド（Python/Node/Jekyll）
- 言語別・製品別の対象ページ一覧と除外理由
- Sitemap・Search Console関連の正本と取得URL
- CIワークフローとテスト結果
- 今後の言語・ページ追加の確認担当とGate

**更新ルール:** 実装と運用手順を同じPRで変更し、`VALIDATION_LOG.md`に証拠を残す。
