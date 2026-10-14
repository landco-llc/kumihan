# KUMIHAN：GPT・Codex 向けダウンロード

プレビュー版 **0.1.0-preview.1**。ZIP名の `plugin` は4つの Skill をまとめたプラグイン、`skill` は単独 Skill を示します。形式上の導入先を示す名前であり、実機動作は未検証です。

[導入方法（日本語）](../docs/installation.ja.md) · [Installation (English)](../docs/installation.md)

## プラグイン / Plugin

[プラグイン ZIP](plugins/kumihan-GPT-Codex-plugin-0.1.0-preview.1.zip)

## スキル / Skills

- [kumihan](skills/kumihan-GPT-Codex-skill-0.1.0-preview.1.zip)
- [kumihan-web](skills/kumihan-web-GPT-Codex-skill-0.1.0-preview.1.zip)
- [kumihan-documents](skills/kumihan-documents-GPT-Codex-skill-0.1.0-preview.1.zip)
- [kumihan-review](skills/kumihan-review-GPT-Codex-skill-0.1.0-preview.1.zip)

## チェックサム / Checksums

[SHA256SUMS.txt](SHA256SUMS.txt) · [MANIFEST.json](MANIFEST.json)

ZIPは `plugins/` と `skills/` の配置を保持してください。配布フォルダーの親ディレクトリから、macOSで確認する場合:

```sh
cd "downloads GPT-Codex"
shasum -a 256 -c SHA256SUMS.txt
```

The plugin ZIP contains all four skills; each standalone ZIP contains one complete skill folder. Keep the subfolder layout when checking SHA256SUMS. Host installation and operation remain unverified; this preview does not establish a stable release.
