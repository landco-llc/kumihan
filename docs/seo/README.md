# KUMIHAN SEO運用正本

技術SEOの共通生成・横断検証を管理する。検索登録・順位・SNSキャッシュ更新を保証するものではない。実行結果と未確認事項は [VALIDATION_LOG.md](VALIDATION_LOG.md) を参照。

| 責務 | 正本 |
| --- | --- |
| 実装要件 | [SEO仕様書](../specs/KUMIHAN_SEO_FOUNDATION_IMPLEMENTATION_20261019.md) |
| ページタイトル・説明・本文・言語 | 既存 `assets/gateway-copy.json`、各 `assets/*-site-copy.json`、frontmatter、独立テンプレート／HTML |
| URL・メタ・JSON-LD共通契約 | `tools/seo_metadata.py` |
| 共有定数のみ | `assets/seo-config.json`（site URL、publisher、OG画像。ページ翻訳の二重登録禁止） |
| 全サイト生成・生成器検証 | `tools/build_seo.py` |
| Sitemap | `tools/build_sitemap.py` → `sitemap.xml` |
| 横断監査 | `tools/check_seo.py` |
| PR検証 | `.github/workflows/seo-foundation.yml` |
| 個々の生成元→出力・除外理由 | [BASELINE_INVENTORY.md](BASELINE_INVENTORY.md) |
| 新言語／ページ追加 | [ADD_LANGUAGE_OR_PAGE.md](ADD_LANGUAGE_OR_PAGE.md) |
| 設計判断・例外 | [DECISIONS.md](DECISIONS.md) |

## 再生成と検証

リポジトリrootで実行する。Python 3とNode.jsが必要。これらはサイト生成器であり配布ZIPの再ビルドではない。

```sh
python tools/build_seo.py
python tools/build_seo.py --check
python tools/build_sitemap.py --check
python tools/check_seo.py
python -m unittest discover -s tests/seo -v
```

`--check` は書き込まず、生成ドリフトを失敗として報告する。初回生成後に再生成して差分が増えないことも確認する。単独の言語生成器を使う場合は棚卸しの該当 `tools/build_*_site.py --check`、Vietnameseは `node tools/build_nhip_chu_site.mjs --check` を実行する。

Jekyllのfrontmatter本文を完成HTMLと混同しない。ソース監査は生成済みSEO契約を照合し、GitHub Pages相当のJekyllビルド後には実HTMLも検証する。CIのビルドコマンド・依存設定を正本とし、ローカルで生成した出力パスを渡す。

```sh
python tools/check_seo.py --site-dir _site
python tools/build_sitemap.py --check --site-dir _site
```

## 公開規則

canonicalは絶対HTTPS・言語別自己参照。ホームだけ `index.html` を `/kumihan/` に正規化する。hreflangは実在する翻訳群の自己参照・相互参照を維持し、gatewayと製品、製品と導入ガイドを混ぜない。rootとdocsの新HTMLは自動探索され、不完全なSEOをCIが検出する。

Sitemapはindexableなcanonical URLのみを決定的な順序で出力する。架空のlastmod、priority、changefreqは付けない。公開URLは [sitemap.xml](https://landco-llc.github.io/kumihan/sitemap.xml)。HTMLのhreflangを正本とし、Sitemapへ重複登録しない。

OG画像は既存の公式ロゴ（1254×1254 PNG）を使用し、Twitterは正方形に合う `summary`。画像・ブランドを変更する場合は実体の寸法とMIMEを再検証する。JSON-LDのOrganizationは公開情報 `L&Co. LLC` / `https://landco.co.jp/` のみ。架空のレビュー・価格・販売実績は追加しない。

## Owner対応と境界

本PRはDraft PRまで。mainへの直接push/mergeは禁止。公開後のSearch Console所有権確認・Sitemap送信・URL検査はOwnerが行う。未公開ブランチのHTMLを公開サイトに反映済みと記録しない。

GitHub Pagesプロジェクトサイトの `/kumihan/robots.txt` はホスト直下の `/robots.txt` を代替しないため追加しない。GA4/GTM・Consent Mode・追跡Cookie・AI学習クローラー方針・スキル／プラグイン／配布ZIP／versionは対象外。

更新時はコード・生成物・棚卸し・手順を同じPRで変更し、検証日（JST）、対象SHA、コマンド、結果、未確認を検証ログへ追記する。HumanによるMD/ZIP再添付は不要。次の担当はGitHub上の仕様書と本ディレクトリをFresh Readして継続する。

Discovery extends automatically beyond root/docs into new public directories. See the explicit source/package exclusions in `tools/seo_inventory.py` and ADR-SEO-012; adding a public page with incomplete metadata fails the audit. The current inventory remains 231 pages.
