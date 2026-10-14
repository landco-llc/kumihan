# KUMIHAN：Claude向け配布 / Claude downloads

プレビュー **0.1.0-preview.1**。Claude Code用プラグインとClaudeチャット用の単独Skillを分けています。実機動作は未検証です。

[導入方法（日本語）](../docs/installation.claude.ja.md) · [Installation (English)](../docs/installation.claude.md)

## Claude Codeプラグイン / Plugin

[プラグインZIP](plugins/kumihan-Claude-Code-plugin-0.1.0-preview.1.zip)

## Claudeチャットの単独Skills

- [kumihan](skills/kumihan-Claude-skill-0.1.0-preview.1.zip)
- [kumihan-web](skills/kumihan-web-Claude-skill-0.1.0-preview.1.zip)
- [kumihan-documents](skills/kumihan-documents-Claude-skill-0.1.0-preview.1.zip)
- [kumihan-review](skills/kumihan-review-Claude-skill-0.1.0-preview.1.zip)

[SHA256SUMS.txt](SHA256SUMS.txt) · [MANIFEST.json](MANIFEST.json)

```sh
cd "downloads Claude"
shasum -a 256 -c SHA256SUMS.txt
```

Keep the subfolder layout when checking hashes. The four standalone ZIPs preserve existing skill ZIP bytes. The Code plugin ZIP is a separate package; do not upload it as a standalone chat skill. Host installation and operation remain unverified.
