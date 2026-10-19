# KUMIHAN ダウンロード：Claude

[導入ガイド（日本語）](../docs/installation.claude.ja.md) ・ [Installation guide (English)](../docs/installation.claude.md) ・ [トップに戻る / Back to top](../README.md)

<br>

現行パッケージ **v0.1.8** です。導入の手順は、上の導入ガイドをご覧ください。

Current package **v0.1.8**. See the installation guide above for setup steps.

<br>

## Claude Code用プラグイン / Plugin for Claude Code

4つのスキルをまとめたパッケージです。Claude Codeで使います。

All four skills in one package, for Claude Code.

- [kumihan-Claude-Code-plugin-0.1.8.zip](plugins/kumihan-Claude-Code-plugin-0.1.8.zip)

<br>

## Claudeチャット用スキル / Skills for Claude chat

claude.aiやClaudeアプリに、1つずつアップロードして使います。

Upload one at a time to claude.ai or the Claude apps.

- [kumihan](skills/kumihan-Claude-skill-0.1.8.zip) — 最初の入口 / starting point
- [kumihan-web](skills/kumihan-web-Claude-skill-0.1.8.zip) — Webページ / web pages
- [kumihan-documents](skills/kumihan-documents-Claude-skill-0.1.8.zip) — 報告書・スライド / reports and slides
- [kumihan-review](skills/kumihan-review-Claude-skill-0.1.8.zip) — レビュー / review

<br>

## ファイルの確認（任意） / Verify downloads (optional)

ダウンロードしたファイルが壊れていないかを確認できます。このページと同じフォルダー構成（`plugins/` と `skills/`）でファイルを置き、ターミナルで次を実行してください。`shasum` がない環境では、Windows PowerShellの `Get-FileHash` 等でSHA-256を確認してください。すべての行に `OK` と表示されれば問題ありません。

To check your downloads, keep the same folder layout as this page and run the following in a terminal. If `shasum` is unavailable, use an equivalent SHA-256 command such as Windows PowerShell `Get-FileHash`. Every line should show `OK`.

```sh
cd "downloads Claude"
shasum -a 256 -c SHA256SUMS.txt
```

[SHA256SUMS.txt](SHA256SUMS.txt) ・ [MANIFEST.json](MANIFEST.json)
