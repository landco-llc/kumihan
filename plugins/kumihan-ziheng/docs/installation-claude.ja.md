# KUMIHAN｜字衡 — Claude / 字衡の導入

**v0.1.0** — Claude Codeプラグイン1本と、Claudeチャット向けの独立スキルZIP4本を配布します。

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

- [フルパッケージを入手 (kumihan-ziheng-Claude-Code-plugin-0.1.0.zip)](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Claude/plugins/kumihan-ziheng-Claude-Code-plugin-0.1.0.zip)
- フルパッケージのSHA-256: `b37ee0c95c7575b773667f0256eadd3ecf983d7f1e9db26761614ee71c76fe0e`

### 独立スキル4本

- [kumihan-ziheng](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Claude/skills/kumihan-ziheng-Claude-skill-0.1.0.zip)
- [kumihan-ziheng-web](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Claude/skills/kumihan-ziheng-web-Claude-skill-0.1.0.zip)
- [kumihan-ziheng-documents](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Claude/skills/kumihan-ziheng-documents-Claude-skill-0.1.0.zip)
- [kumihan-ziheng-review](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Claude/skills/kumihan-ziheng-review-Claude-skill-0.1.0.zip)

台湾はzh-Hant-TW、香港はzh-Hant-HKを明示的に選択し、原稿の文字を変更しないでください。

`shasum -a 256 -c SHA256SUMS.txt`

- [ソースを見る](https://github.com/landco-llc/kumihan/tree/main/plugins/kumihan-ziheng)

- [SHA256SUMS.txt](https://github.com/landco-llc/kumihan/tree/main/plugins/kumihan-ziheng/downloads%20Claude/SHA256SUMS.txt)


Version candidate: v0.2.0. Back up the existing folder, verify the active host MANIFEST/SHA256, replace the complete folder and reload. Historical v0.1.0 URLs remain available. Native host acceptance and formal Release are not implied.

Current v0.2.0 full bundle SHA-256: `5da65c3d2085ec55e48309c01ee8a6a148ffecff13f490ec9747b24a0c51b06e`. The older checksum above applies only to its explicitly named v0.1.0 archive.
