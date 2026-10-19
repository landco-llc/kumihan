# 新しい言語・ページを追加する場合のSEO手順

**状態: 実装完了前の運用チェックリスト。SEO基盤v1.0完成時に実コマンドと生成元を追記すること。**

## A. 作業開始前

- [ ] 最新main/実装ブランチをFresh Read
- [ ] 既存言語版/新しい言語版/新しい製品版のいずれかに分類
- [ ] 正本となる生成元・言語コピー・テンプレートを特定
- [ ] 翻訳元と翻訳先のURLの実在を確認（架空のURLを登録しない）
- [ ] 対象ページが公開・indexableであることを確認
- [ ] 他PRのSNSシェア/OGP/SEO変更との重複を確認

## B. SEO属性を作る

- [ ] `<html lang>`（RTL言語は必要に応じ`dir`）
- [ ] 既存コンテンツを正しく反映したtitleとdescription
- [ ] 自己参照のcanonical（ホームの`/index.html`別名だけ既定値に正規化）
- [ ] 同一コンテンツ群のhreflang（自己・相互、必要時x-default）
- [ ] og:type / og:title / og:description / og:url / og:locale / og:image
- [ ] twitter:card / twitter:title / twitter:description / twitter:image
- [ ] 正しい`WebPage.inLanguage`/`WebPage.url`を持つJSON-LD
- [ ] 既存ロゴ・画像の配信URL、画像寸法、ALT表記を確認
- [ ] メタタグはビルド前後とも1つ。生成済みHTMLへの手編集のみで終わらせない

## C. 既存生成機構へ追加

トップ言語ゲートウェイ:
- [ ] `tools/build_gateways.py` のGATEWAYSと必要に応じPRODUCTSを更新
- [ ] `assets/gateway-copy.json` の対応言語を更新
- [ ] トップ言語ページが全既存トップページのhreflang集合に入ることを確認

製品言語LP:
- [ ] 翻訳本文に合う各言語固有の生成元を特定
- [ ] `tools/product_site.py` または個別`build_*_site.py` / テンプレートに新言語を追加
- [ ] 既存製品の他言語LPとのみhreflang関係を追加
- [ ] 必要時にJekyllレイアウトも更新
- [ ] 導入ページにもcanonicalとindexable判定を付ける

独立したその他ページ:
- [ ] 公開・非公開・noindex・duplicate URLの意図を明記
- [ ] robots/alias/redirectをSEO登録と混同しない
- [ ] 公開するなら共通SEO helperからhead情報を生成

## D. 生成・テスト

- [ ] 最新の各ビルダーでHTMLを再生成。再生成した生成物をcommit
- [ ] SEO共通ビルダーで`sitemap.xml`を再生成
- [ ] 非書込`--check`を実施
- [ ] canonicalとsitemapが一致・重複なし
- [ ] hreflangの全相互参照が存在
- [ ] JSON-LDのJSON解析とURL整合がPASS
- [ ] OGP画像がHTTPS配信され、寸法メタが正しい
- [ ] 文字組/320px/Unicode/RTLの必要な表示確認
- [ ] 既存の言語版と配布ZIP/README/ダウンロードリンクに意図しない変更なし
- [ ] CIがPASS
- [ ] PRと`docs/seo/VALIDATION_LOG.md`にHEAD SHA、テスト結果、未確認を記録

## E. 公開後（Owner対応）

- [ ] SEO仕様反映済みのGitHub Pages公開URLを確認
- [ ] Search Consoleで所有権確認（未設定ならOwner）
- [ ] Search Consoleに`https://landco-llc.github.io/kumihan/sitemap.xml`を送信または再送信
- [ ] Search ConsoleのURL検査で主要新ページの取得・indexabilityを確認
- [ ] インデックス登録・検索表示・AI引用を保証しないことを記録

## このチェックリストのアップデート

具体的な生成/検証コマンドはW06で実コードに合わせて確定させる。ページ追加ごとに新設チェックが必要になった場合、既存手順と`DECISIONS.md`を同時更新。
