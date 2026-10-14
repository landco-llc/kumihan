# KUMIHAN ダウンロード：ChatGPT・Codex

[導入ガイド（日本語）](../docs/installation.ja.md) ・ [Installation guide (English)](../docs/installation.md) ・ [トップに戻る / Back to top](../README.md)

<br>

プレビュー版 **v0.1.4 preview** です。導入の手順は、上の導入ガイドをご覧ください。

Preview version **v0.1.4 preview**. See the installation guide above for setup steps.

<br>

## プラグイン / Plugin

4つのスキルをまとめたパッケージです。

All four skills in one package.

- [kumihan-GPT-Codex-plugin-0.1.4-preview.zip](plugins/kumihan-GPT-Codex-plugin-0.1.4-preview.zip)

<br>

## スキル / Skills

1つずつ追加して使います。

Add them one at a time.

- [kumihan](skills/kumihan-GPT-Codex-skill-0.1.4-preview.zip) — 最初の入口 / starting point
- [kumihan-web](skills/kumihan-web-GPT-Codex-skill-0.1.4-preview.zip) — Webページ / web pages
- [kumihan-documents](skills/kumihan-documents-GPT-Codex-skill-0.1.4-preview.zip) — 報告書・スライド / reports and slides
- [kumihan-review](skills/kumihan-review-GPT-Codex-skill-0.1.4-preview.zip) — レビュー / review

<br>

## ファイルの確認（任意） / Verify downloads (optional)

ダウンロードしたファイルが壊れていないかを確認できます。このページと同じフォルダー構成（`plugins/` と `skills/`）でファイルを置き、macOSのターミナルで次を実行してください。すべての行に `OK` と表示されれば問題ありません。

To check your downloads, keep the same folder layout as this page and run the following in the macOS Terminal. Every line should show `OK`.

```sh
cd "downloads GPT-Codex"
shasum -a 256 -c SHA256SUMS.txt
```

[SHA256SUMS.txt](SHA256SUMS.txt) ・ [MANIFEST.json](MANIFEST.json)
