# 新しい言語・ページを追加する手順

作業者が正本更新・生成・CIを担当し、独立レビュアーが翻訳群・indexability・コピー保護を確認する。Ownerは公開判断とSearch Console操作を担当する。mainへ自動mergeしない。

## 1. 正本を決める

- [ ] 最新main・対象ブランチ・関連PRをFresh Readし、[棚卸し](BASELINE_INVENTORY.md) で同種ページの生成元を探す。
- [ ] gateway、製品LP、導入ガイド、独立ページのどれかを決め、実際の本文言語・翻訳関係を明記する。
- [ ] 公開URLとindexable/noindex/外部canonicalの意図を決める。不存在の翻訳URLを推測しない。
- [ ] 既存コピー正本へtitle/description/本文を登録する。`assets/seo-config.json` にページごとの翻訳レジストリを作らない。

## 2. 生成経路へ登録する

Gatewayは `tools/build_gateways.py` の `GATEWAYS` と `assets/gateway-copy.json` を更新し、必要なら `PRODUCTS` へ製品を登録する。全gateway間のhreflang集合はその登録を再利用する。

製品・導入ガイドは既存の `tools/build_*_site.py` / `tools/product_site.py` / `tools/install_frame.py` を使う。Vietnameseは `tools/build_nhip_chu_site.mjs` の共通SEOアダプタ経路を使う。独立版テンプレートはテンプレートと生成先の両方を棚卸しに記録する。新しい生成器を作る場合は `tools/build_seo.py` の実行対象へ加え、非書込 `--check` を実装する。

Jekyllは適切な `_layouts/` とページfrontmatter・既存コピーを更新する。レイアウトのSEO include生成も全体ビルダーで再生成する。Bangla等のソースHTMLは本文・既存コピーを正本に保ち、共通SEOアダプタを使う。

- [ ] 同一製品の実在翻訳だけをhreflangへ登録し、自己・相互リンクを維持する。
- [ ] `<html lang>`、必要な `dir="rtl"`、表示言語と一致するOG localeを確認する。
- [ ] 自己canonical、OG URL、JSON-LD WebPage URLを一致させる。
- [ ] gatewayと製品、導入ガイドを互いの翻訳として登録しない。
- [ ] 画像変更時は共有設定と実画像を更新し、寸法・MIME・HTTPS取得を実測する。
- [ ] root/docsへ新HTMLを置けば探索対象になる。SEO未整備のまま除外設定を足してCIを回避しない。非公開fixtureは `tests/seo/fixtures/test-fixture-new-language` 配下へ置く。

## 3. 生成し、漏れとドリフトを検証する

リポジトリrootで実行する。

```sh
python tools/build_seo.py
python tools/build_seo.py --check
python tools/build_sitemap.py --check
python tools/check_seo.py
python -m unittest discover -s tests/seo -v
```

- [ ] 生成済みHTML・SEO include・`sitemap.xml`を同じPRに含める。
- [ ] 2回目の生成で追加差分がなく、`--check`実行前後にファイル変更がない。
- [ ] 新ページがSitemapへ1回だけ追加される（indexableの場合）。ホームの `index.html` とルートを二重登録しない。
- [ ] 不完全な新言語fixtureが監査で失敗し、共通SEO適用後はメタ・Sitemap監査を通るテストを維持する。
- [ ] Jekyllビルド後の `_site` を `python tools/check_seo.py --site-dir _site` と `python tools/build_sitemap.py --check --site-dir _site` で検証する。
- [ ] 変更言語のUnicode・RTL・表示幅・既存リンクを実画面で確認し、未実測ならそのまま記録する。
- [ ] `git diff origin/main -- plugins skills '*.zip'` 等で配布物・versionに意図しない変更がない。
- [ ] [棚卸し](BASELINE_INVENTORY.md)、必要なら [設計判断](DECISIONS.md)、[検証ログ](VALIDATION_LOG.md) を更新する。
- [ ] `.github/workflows/seo-foundation.yml` と既存関連CIがPASSし、独立レビュー結果・対象SHA・未実施をDraft PRへ記録する。

## 4. 公開後のOwner操作

- [ ] 承認・merge後、GitHub Pages公開HTML・画像・Sitemapを取得してブランチの検証結果と区別する。
- [ ] Search Console所有権を確認し、`https://landco-llc.github.io/kumihan/sitemap.xml` を送信／再送信する。
- [ ] URL検査で主要新ページの取得・indexabilityを確認する。検索登録・順位やAI引用を保証しない。
- [ ] SNS取得検査を行う場合はキャッシュ・ログイン制約を記録する。

### Other public directories

New HTML directories (for example `guides/`) are discovered recursively by `tools/seo_inventory.py`; Jekyll frontmatter pages there use the same include generator. Source/package directories are explicitly excluded in that scanner. A new publishing convention must update the scanner policy and `_config.yml` together. `tests/seo/test_audit.py` proves missing SEO in a new directory fails before a complete page passes and enters Sitemap.
