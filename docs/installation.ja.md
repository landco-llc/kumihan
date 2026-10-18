# ChatGPT・Codexへの導入

[English](installation.md) ・ [トップに戻る](../README.md)

<br>

KUMIHANをChatGPTやCodexで使うための手順です。

> **プレビュー版（v0.1.7 preview）について**
> ご自身の環境で導入を試していただくための版です。各ツールでの動作はまだ十分に確認できていないため、うまく動かない場合があります。

<br>

## 1. 導入方法を選ぶ

| 使いたい場所 | おすすめの方法 |
| --- | --- |
| ChatGPT（スキルのアップロードができる場合） | [A. スキルを1つずつ追加する](#a-chatgptにスキルを追加する) |
| ChatGPT（自分専用のプラグインとして登録したい場合） | [B. プラグインとしてまとめて登録する](#b-chatgptにプラグインとして登録する) |
| Codex（パソコン上で使う場合） | [C. フォルダーをコピーする](#c-codexにフォルダーをコピーする) |

**スキル**は機能1つ分、**プラグイン**は4つのスキルをまとめたパッケージです。

<br>

## 2. ファイルをダウンロードする

ファイルは [ダウンロードページ](../downloads%20GPT-Codex/) にあります。

**プラグイン（4つのスキルをまとめたもの）**

- [kumihan-GPT-Codex-plugin-0.1.7-preview.zip](../downloads%20GPT-Codex/plugins/kumihan-GPT-Codex-plugin-0.1.7-preview.zip)

**スキル（1つずつ）**

- [kumihan](../downloads%20GPT-Codex/skills/kumihan-GPT-Codex-skill-0.1.7-preview.zip) — 最初の入口
- [kumihan-web](../downloads%20GPT-Codex/skills/kumihan-web-GPT-Codex-skill-0.1.7-preview.zip) — Webページ
- [kumihan-documents](../downloads%20GPT-Codex/skills/kumihan-documents-GPT-Codex-skill-0.1.7-preview.zip) — 報告書・スライド
- [kumihan-review](../downloads%20GPT-Codex/skills/kumihan-review-GPT-Codex-skill-0.1.7-preview.zip) — レビュー

GitHubでファイルを開いたら、右上のダウンロードボタンから保存してください。

<br>

## A. ChatGPTにスキルを追加する

ChatGPTの画面に「Skills」とアップロードの項目がある場合に使える方法です。

1. スキルのZIPファイルを1つ選んでアップロードします。
2. 表示された内容を確認して、追加します。
3. 必要なスキルの数だけ、同じ手順をくり返します。

**ご注意**

- プラグインのZIPは、この方法では使えません。スキルのZIPを使ってください。
- チャットにファイルを添付するだけでは、スキルとして追加されません。
- 画面に項目が見当たらない場合は、お使いのプランやアプリでまだ提供されていない可能性があります。[OpenAIの公式案内](https://learn.chatgpt.com/docs/build-skills) をご確認ください。

<br>

## B. ChatGPTにプラグインとして登録する

4つのスキルをまとめて、自分専用のプラグインとして登録する方法です。

1. ChatGPTで新しい会話を開き、`@plugin-creator` を選びます。
2. プラグインのZIPファイルを添付します。
3. 次のように依頼します。

   > このパッケージを自分用のプライベートプラグインとして登録してください。公開ディレクトリには提出しないでください。

4. 登録できたら、Pluginsの「Personal」や「Created by me」に **KUMIHAN v0.1.6** が表示されます。
5. 必要に応じてインストールし、新しい会話で有効にします。

**ご注意**

- 登録先がチームのワークスペースになる場合があります。自分専用にしたい場合は、登録前に保存先を確認してください。
- この機能は、プランやワークスペースの設定によって使えない場合があります。詳しくは [Build plugins](https://learn.chatgpt.com/docs/build-plugins) と [Plugins](https://learn.chatgpt.com/docs/plugins) をご覧ください。
- この方法で登録したプラグインは、あなたのアカウントだけで使えます。公開ディレクトリには掲載されません。

<br>

## C. Codexにフォルダーをコピーする

スキルのZIPを展開すると、`kumihan` などのフォルダーができます。このフォルダーを、Codexが読み込む場所にコピーします。

| 使う範囲 | コピー先 |
| --- | --- |
| 特定のプロジェクトだけで使う | プロジェクト内の `.agents/skills/` |
| すべてのプロジェクトで使う | ホームフォルダーの `~/.agents/skills/` |

たとえば、プロジェクトに `kumihan` を追加する場合は次のとおりです。

```sh
mkdir -p /path/to/your-project/.agents/skills
cp -R kumihan /path/to/your-project/.agents/skills/
```

**ご注意**

- フォルダーは中身ごと、まるごとコピーしてください。一部のファイルだけでは正しく動きません。
- 同じ名前のフォルダーがすでにある場合は、上書きする前に中身を確認してください。

GitHubから直接導入したい場合や、Codexのマーケットプレイスを使いたい場合は、[更新ガイド](updates.md) をご覧ください。

<br>

## 3. 使ってみる

導入できたら、新しい会話を開いてスキルを呼び出します。

| ツール | 呼び出し方 |
| --- | --- |
| ChatGPT | `@` から選ぶ |
| Codex | `$` または `/skills` から選ぶ |

最初は、ファイルを変更しない依頼で試すのがおすすめです。

> 日本語の報告書をつくる予定です。気をつけるポイントを教えてください。ファイルは変更しないでください。

<br>

## ファイルが正しいか確認する（任意）

ダウンロードしたファイルが壊れていないかを確認したい場合は、[SHA256SUMS.txt](../downloads%20GPT-Codex/SHA256SUMS.txt) を使います。

ダウンロードページと同じフォルダー構成（`plugins/` と `skills/`）でファイルを置き、ターミナルで次のコマンドを実行します。`shasum` がない環境では、Windows PowerShellの `Get-FileHash` などでSHA-256を照合してください。

```sh
cd "downloads GPT-Codex"
shasum -a 256 -c SHA256SUMS.txt
```

すべての行に `OK` と表示されれば問題ありません。

<br>

---

ほかのツール：[Claude](installation.claude.ja.md) ・ [Gemini](installation.gemini.ja.md)

画面や提供条件は変わることがあります。最新の情報は各サービスの公式案内をご確認ください（本ページの確認日：2026年10月14日）。
