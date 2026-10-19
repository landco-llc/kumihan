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

## 2026-10-19 integration notice — English first and new social preview generator

This runbook now includes the reconciled English-first baseline. Before using it for publication, read [RECONCILIATION_20261019_EN_TOP_NEW_LANGS.md](RECONCILIATION_20261019_EN_TOP_NEW_LANGS.md). The latest main has English `index.html`, Japanese `top-ja.html`, a `noindex` `top-en.html` alias, 22 gateway languages, and `site_share.py` as the shared localized OGP/Twitter generator with a 1200×630 preview image. All future language editions need to register their localized share description/locale and any Jekyll share data as appropriate, without duplicate OG/Twitter meta or a second share-copy registry. These changes are integrated into Draft PR #93. Use the latest exact-HEAD Hosted CI and validation log; the original 20/20 check is historical.

## 2026-10-19 v2 additions — future language and new packages

**PR #100はmainへマージ済み。** 新たな言語/ページを作成する前に最新mainと [SEO W09–W15再レビュー](REVIEW_REFRESH_20261019_MAIN_73D2B01.md) を確認する。旧SEOブランチ由来の配布ZIP・skills/・plugin manifest・README・CHANGELOGへの巻戻しを禁止。

- [ ] 今回の実装対象は現在のmainに存在するindexableページ。言語またはURLを推測して追加しない
- [ ] トップの英語 `index.html` にroot canonical、`top-ja.html` に自己canonical、転送 `top-en.html` はnoindex/Sitemap除外
- [ ] `tools/site_share.py` の locale/ABOUT と `_includes/share.html` のJekyllデータを各言語で照合
- [ ] 将来のJekyll言語を追加した際に `_data/site_share.json` の未登録がJAフォールバックで隠れないよう監査FAILにする
- [ ] OGP/Twitterは現行 `assets/kumihan-share.png` の1200×630、ローカライズ済み説明文を維持。SEOだけで上書きしない
- [ ] ビルドに使う生成器が転送aliasを通常ページとしてSEO強制しないこと（説明文なしを正常と認めるのは明示aliasのみ）
- [ ] ソースHTMLだけでなくJekyll最終公開HTMLでOGP、canonical、hreflang、JSON-LD、Sitemapを確認

## W09–W15 current generator contract

1. Register authoritative page copy in the existing product/gateway source. `site_share.ABOUT` reads `assets/gateway-copy.json`; add LOCALES and the language resolver mapping. Run `python tools/web_fonts.py` to refresh `_data/site_share.json` (all supported languages and required BCP47 aliases).
2. Wrap every HTML generator output with `seo_outputs`; Node uses the shared Python CLI. New Jekyll layouts need `templates/seo-<layout>-head.html` and a generated include followed by `share.html lang=seo_share_lang title=seo_share_title description=seo_share_description canonical=seo_canonical`. Do not leave old canonical/hreflang/social tags in the layout.
3. Jekyll copy/locale dictionary absence or drift fails `build_jekyll_seo.py`; no implicit Japanese share text for unknown locales. Effective default Japanese language is passed explicitly for legacy frontmatter without lang.
4. Run `build_seo.py --check`, `web_fonts.py --check`, `check_seo_preservation.py`, SEO regressions and Hosted Jekyll3.10 actual-output audit. Confirm one canonical, one shared social set, no duplicate alternates, English root and all URL fields aligned. `guides/` and comma-delimited robots=none negatives remain covered.
5. Preservation baseline is pinned to current-main a08fd66. A future intentional product/body/package change needs its own reviewed baseline refresh; never weaken hashes just to pass an SEO patch. Do not build distribution ZIPs in the SEO checkout.
