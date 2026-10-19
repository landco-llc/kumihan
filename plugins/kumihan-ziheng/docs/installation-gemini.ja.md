# KUMIHAN｜字衡 — Gemini / 字衡の導入

**v0.1.0** — Gemini CLI拡張機能1本と、Geminiアプリ向けの独立スキルZIP4本を配布します。

> 本パッケージは組版の指針であり、自動レンダラーではありません。各ホストでの実インストールと呼び出しは未検証です。台湾・香港の代表例で実機確認してください。

## 導入手順

**1.** Gemini CLI専用の拡張機能ZIPをダウンロードし、新しい空フォルダに解凍します。

```sh
unzip kumihan-ziheng-Gemini-CLI-extension-0.1.0.zip -d /absolute/path/kumihan-ziheng
```

**2.** そのローカルフォルダをGemini CLIに指定してインストールし、再起動後にSkillsを確認します。

```sh
gemini extensions install "/absolute/path/kumihan-ziheng"
```

**3.** GitHubリポジトリのルートは日本語版KUMIHANの拡張機能です。ルートURLのインストールは字衡の導入ではありません。

```sh
gemini extensions list
```

**4.** Geminiアプリ：Skillsのアップロードに対応したアカウントでは、個別スキルZIPを追加して実際の動作を確認します。

## ダウンロードと検証

- [フルパッケージを入手 (kumihan-ziheng-Gemini-CLI-extension-0.1.0.zip)](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Gemini/extensions/kumihan-ziheng-Gemini-CLI-extension-0.1.0.zip)
- フルパッケージのSHA-256: `6f199799a7905d55636c28cf5598bd143cadc90b7aa2460aa4b7befb9df24e75`

### 独立スキル4本

- [kumihan-ziheng](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Gemini/skills/kumihan-ziheng-Gemini-Apps-skill-0.1.0.zip)
- [kumihan-ziheng-web](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Gemini/skills/kumihan-ziheng-web-Gemini-Apps-skill-0.1.0.zip)
- [kumihan-ziheng-documents](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Gemini/skills/kumihan-ziheng-documents-Gemini-Apps-skill-0.1.0.zip)
- [kumihan-ziheng-review](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Gemini/skills/kumihan-ziheng-review-Gemini-Apps-skill-0.1.0.zip)

台湾はzh-Hant-TW、香港はzh-Hant-HKを明示的に選択し、原稿の文字を変更しないでください。

`shasum -a 256 -c SHA256SUMS.txt`

- [ソースを見る](https://github.com/landco-llc/kumihan/tree/main/plugins/kumihan-ziheng)

- [SHA256SUMS.txt](https://github.com/landco-llc/kumihan/tree/main/plugins/kumihan-ziheng/downloads%20Gemini/SHA256SUMS.txt)
