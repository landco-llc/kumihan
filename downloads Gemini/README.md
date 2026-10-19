# KUMIHAN ダウンロード：Gemini

[導入ガイド（日本語）](../docs/installation.gemini.ja.md) ・ [Installation guide (English)](../docs/installation.gemini.md) ・ [トップに戻る / Back to top](../README.md)

<br>

プレビュー版 **v0.1.8 preview** です。導入の手順は、上の導入ガイドをご覧ください。

Preview version **v0.1.8 preview**. See the installation guide above for setup steps.

<br>

## Gemini CLI用拡張機能 / Extension for Gemini CLI

4つのスキルをまとめたパッケージです。

All four skills in one package.

- [kumihan-Gemini-CLI-extension-0.1.8-preview.zip](extensions/kumihan-Gemini-CLI-extension-0.1.8-preview.zip)

<br>

## Geminiアプリ用スキル / Skills for the Gemini app

1つずつアップロードして使います。

Upload them one at a time.

- [kumihan](skills/kumihan-Gemini-Apps-skill-0.1.8-preview.zip) — 最初の入口 / starting point
- [kumihan-web](skills/kumihan-web-Gemini-Apps-skill-0.1.8-preview.zip) — Webページ / web pages
- [kumihan-documents](skills/kumihan-documents-Gemini-Apps-skill-0.1.8-preview.zip) — 報告書・スライド / reports and slides
- [kumihan-review](skills/kumihan-review-Gemini-Apps-skill-0.1.8-preview.zip) — レビュー / review

<br>

## ファイルの確認（任意） / Verify downloads (optional)

ダウンロードしたファイルが壊れていないかを確認できます。このページと同じフォルダー構成（`extensions/` と `skills/`）でファイルを置き、ターミナルで次を実行してください。`shasum` がない環境では、Windows PowerShellの `Get-FileHash` 等でSHA-256を確認してください。すべての行に `OK` と表示されれば問題ありません。

To check your downloads, keep the same folder layout as this page and run the following in a terminal. If `shasum` is unavailable, use an equivalent SHA-256 command such as Windows PowerShell `Get-FileHash`. Every line should show `OK`.

```sh
cd "downloads Gemini"
shasum -a 256 -c SHA256SUMS.txt
```

[SHA256SUMS.txt](SHA256SUMS.txt) ・ [MANIFEST.json](MANIFEST.json)
