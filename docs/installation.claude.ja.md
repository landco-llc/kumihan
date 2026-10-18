# Claudeへの導入

[English](installation.claude.md) ・ [トップに戻る](../README.md)

<br>

KUMIHANをClaude CodeやClaudeチャットで使うための手順です。

> **プレビュー版（v0.1.5 preview）について**  
> ご自身の環境で導入を試していただくための版です。各ツールでの動作はまだ十分に確認できていないため、うまく動かない場合があります。

<br>

## 1. 導入方法を選ぶ

| 使いたい場所 | おすすめの方法 |
| --- | --- |
| Claude Code | [A. GitHubから導入する](#a-claude-codegithubから導入する)（更新もかんたん） |
| Claude Code（ZIPで導入したい場合） | [B. ZIPから導入する](#b-claude-codezipから導入する) |
| Claudeチャット（claude.ai・アプリ） | [C. スキルをアップロードする](#c-claudeチャットスキルをアップロードする) |

Claude CodeとClaudeチャットは、導入方法が異なります。

<br>

## A. Claude Code：GitHubから導入する

1. ターミナルで、KUMIHANの配布元を登録します。

   ```sh
   claude plugin marketplace add "https://github.com/landco-llc/kumihan.git#main"
   ```

2. Claude Codeの会話の中で、次を入力します。

   ```text
   /plugin install kumihan@kumihan-marketplace
   ```

3. 内容を確認し、使う範囲（自分だけ・このプロジェクトだけ など）を選んでインストールします。

導入できると、次のコマンドが使えるようになります。

- `/kumihan:kumihan`
- `/kumihan:kumihan-web`
- `/kumihan:kumihan-documents`
- `/kumihan:kumihan-review`

更新の方法は [更新ガイド](updates.md#claude-code) をご覧ください。

<br>

## B. Claude Code：ZIPから導入する

1. [Claude Code用プラグインのZIP](../downloads%20Claude/plugins/kumihan-Claude-Code-plugin-0.1.5-preview.zip) をダウンロードします。
2. ZIPを展開すると、`kumihan` フォルダーができます。
3. そのフォルダーを指定して、Claude Codeを起動します。

   ```sh
   claude --plugin-dir "/absolute/path/kumihan"
   ```

**ご注意**

- フォルダーの中身は、そのまま使ってください。ファイルを削ったり、別のファイルを混ぜたりしないでください。
- この方法では自動で更新されません。新しい版が出たら、ZIPを入れ替えてください。

<br>

## C. Claudeチャット：スキルをアップロードする

claude.aiやClaudeアプリで使う方法です。

1. 使いたいスキルのZIPをダウンロードします。
   - [kumihan](../downloads%20Claude/skills/kumihan-Claude-skill-0.1.5-preview.zip) — 最初の入口
   - [kumihan-web](../downloads%20Claude/skills/kumihan-web-Claude-skill-0.1.5-preview.zip) — Webページ
   - [kumihan-documents](../downloads%20Claude/skills/kumihan-documents-Claude-skill-0.1.5-preview.zip) — 報告書・スライド
   - [kumihan-review](../downloads%20Claude/skills/kumihan-review-Claude-skill-0.1.5-preview.zip) — レビュー
2. Claudeの **Customize → Skills** を開き、追加ボタンから **Upload a skill** を選びます。
3. ZIPを1つずつアップロードし、スキルを有効にします。

**ご注意**

- Claude Code用プラグインのZIPは、ここでは使えません。スキルのZIPを使ってください。
- ZIPのファイル名は変えずにアップロードしてください。
- スキルを使うには、設定で「コード実行」が有効になっている必要があります。詳しくは [Claudeの公式案内](https://support.claude.com/en/articles/12512180-use-skills-in-claude) をご覧ください。
- 組織のアカウントでは、管理者の設定によって使えない場合があります。
- アップロードしたスキルは自動では更新されません。新しい版が出たら、もう一度アップロードしてください。

<br>

## 2. 使ってみる

最初は、ファイルを変更しない依頼で試すのがおすすめです。

> 日本語のWebページをつくる予定です。気をつけるポイントを教えてください。ファイルは変更しないでください。

<br>

## ファイルが正しいか確認する（任意）

ダウンロードしたファイルが壊れていないかを確認したい場合は、[SHA256SUMS.txt](../downloads%20Claude/SHA256SUMS.txt) を使います。

ダウンロードページと同じフォルダー構成（`plugins/` と `skills/`）でファイルを置き、ターミナルで次のコマンドを実行します。`shasum` がない環境では、Windows PowerShellの `Get-FileHash` などでSHA-256を照合してください。

```sh
cd "downloads Claude"
shasum -a 256 -c SHA256SUMS.txt
```

すべての行に `OK` と表示されれば問題ありません。

<br>

---

ほかのツール：[ChatGPT・Codex](installation.ja.md) ・ [Gemini](installation.gemini.ja.md)

画面や提供条件は変わることがあります。最新の情報は各サービスの公式案内をご確認ください（本ページの確認日：2026年10月14日）。
