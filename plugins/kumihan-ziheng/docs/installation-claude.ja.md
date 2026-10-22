# KUMIHAN｜字衡 — Claude / 導入ガイド

完全版パッケージと4つの独立スキルは、同じ字衡のルールを使います。検証済みの現行公開ZIP、SHA-256、版数はホスト別のWebガイドで確認してください。日本語版KUMIHANのmonorepoルートは別製品です。

## 現在の公開版とダウンロードの照合

[導入ガイド](https://landco-llc.github.io/kumihan/docs/install-ziheng-claude.ja.html)

Claude CodeではKUMIHAN marketplaceから独立した字衡プラグインを導入するか、完全版ZIPを展開したローカルフォルダーを使用します。Claudeアプリにスキルのインポート機能がある場合は、個別Skill ZIPを使用します。

```sh
claude plugin marketplace add "https://github.com/landco-llc/kumihan.git#main"
```

```text
/plugin install kumihan-ziheng@kumihan-marketplace
```

```sh
claude --plugin-dir "/absolute/path/kumihan-ziheng"
```

## Skills

- `kumihan-ziheng`
- `kumihan-ziheng-web`
- `kumihan-ziheng-documents`
- `kumihan-ziheng-review`

既存フォルダーをバックアップし、ZIPを照合してから同じホスト・版数の完全なパッケージに置き換え、再読み込みします。異なる版のreferences、rules、scriptsを混在させないでください。

ソース配布のactive MANIFEST.jsonとSHA256SUMS.txtは、Webサイトの公開版より新しい版を示す場合があります。v0.1.0とv0.2.0の旧ZIPは保持し、当時のmanifestとchecksumをhistory/<version>/に保管しています。

- [MANIFEST.json](../downloads%20Claude/MANIFEST.json)
- [SHA256SUMS.txt](../downloads%20Claude/SHA256SUMS.txt)

ホストでの検出、導入、呼び出し、描画は実環境での受入確認が必要です。zh-Hant-TWとzh-Hant-HKの固定原稿を使い、縦書きの約物、混植、読む順序、Unicode配列の保持を個別に確認してください。
