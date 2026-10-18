# KUMIHAN｜字衡 — Claude / 字衡の導入

**v0.1.0-preview** — Claude Codeプラグイン1本と、Claudeチャット向けの独立スキルZIP4本を配布します。

> 本パッケージは組版の指針であり、自動レンダラーではありません。各ホストでの実インストールと呼び出しは未検証です。台湾・香港の代表例で実機確認してください。

## 導入手順

**1.** Claude Code：GitHubからKUMIHANマーケットプレイスを登録します。日本語版は変更しません。

```sh
claude plugin marketplace add "https://github.com/landco-llc/kumihan.git#main"
```

**2.** Claude Code内で、区別された字衡のプラグイン名を指定して導入します。

```text
/plugin install kumihan-ziheng@kumihan-marketplace
```

**3.** 代わりに専用ZIPを解凍し、そのフォルダを指定してローカル起動できます。

```sh
claude --plugin-dir "/absolute/path/kumihan-ziheng"
```

**4.** Claudeチャット：Skillsのアップロードが利用できる場合に限り、個別スキルZIPを1本ずつ追加します。Claude Code用の一括ZIPとは異なります。

## ダウンロードと検証

- [フルパッケージを入手 (kumihan-ziheng-Claude-Code-plugin-0.1.0-preview.zip)](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Claude/plugins/kumihan-ziheng-Claude-Code-plugin-0.1.0-preview.zip)
- フルパッケージのSHA-256: `a4d7e1d49c1a84545cc8fe8d207f3ea706032a18b80518c162ec27f3a1566c3b`

### 独立スキル4本

- [kumihan-ziheng](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Claude/skills/kumihan-ziheng-Claude-skill-0.1.0-preview.zip)
- [kumihan-ziheng-web](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Claude/skills/kumihan-ziheng-web-Claude-skill-0.1.0-preview.zip)
- [kumihan-ziheng-documents](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Claude/skills/kumihan-ziheng-documents-Claude-skill-0.1.0-preview.zip)
- [kumihan-ziheng-review](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Claude/skills/kumihan-ziheng-review-Claude-skill-0.1.0-preview.zip)

台湾はzh-Hant-TW、香港はzh-Hant-HKを明示的に選択し、原稿の文字を変更しないでください。

`shasum -a 256 -c SHA256SUMS.txt`

- [ソースを見る](https://github.com/landco-llc/kumihan/tree/main/plugins/kumihan-ziheng)

- [SHA256SUMS.txt](https://github.com/landco-llc/kumihan/tree/main/plugins/kumihan-ziheng/downloads%20Claude/SHA256SUMS.txt)
