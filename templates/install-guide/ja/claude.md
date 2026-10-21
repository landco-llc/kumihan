{{brand}}をClaude CodeやClaudeチャットで使うための手順です。

> **v{{version}}について**
> ご自身の環境で導入を試していただくための版です。各ツールでの動作はまだ十分に確認できていないため、うまく動かない場合があります。

## 1. 導入方法を選ぶ

| 使いたい場所 | おすすめの方法 |
| --- | --- |
{{#if marketplace}}
| Claude Code | [A. GitHubから導入する](#a)（更新もかんたん） |
{{/if}}
| Claude Code（ZIPで導入したい場合） | [{{L_zip}}. ZIPから導入する](#{{l_zip}}) |
| Claudeチャット（claude.ai・アプリ） | [{{L_chat}}. スキルをアップロードする](#{{l_chat}}) |

Claude CodeとClaudeチャットは、導入方法が異なります。

{{#if marketplace}}
## A. Claude Code：GitHubから導入する

1. ターミナルで、KUMIHANの配布元を登録します。

   ```sh
   claude plugin marketplace add "https://github.com/landco-llc/kumihan.git#main"
   ```

2. Claude Codeの会話の中で、次を入力します。

   ```text
   /plugin install {{plugin}}@kumihan-marketplace
   ```

3. 内容を確認し、使う範囲（自分だけ・このプロジェクトだけ など）を選んでインストールします。

導入できると、次のコマンドが使えるようになります。

{{claude_commands}}

{{/if}}
## {{L_zip}}. Claude Code：ZIPから導入する

1. [Claude Code用プラグインのZIP]({{plugin_url}}) をダウンロードします。
{{#if plugin_folder}}
2. ZIPを展開すると、`{{plugin_folder}}` フォルダーができます。
{{else}}
2. 空の `{{plugin}}` フォルダーを作り、その中に展開します。
{{/if}}
3. そのフォルダーを指定して、Claude Codeを起動します。

   ```sh
   claude --plugin-dir "/absolute/path/{{plugin_dir}}"
   ```

**ご注意**

- フォルダーの中身は、そのまま使ってください。ファイルを削ったり、別のファイルを混ぜたりしないでください。
- この方法では自動で更新されません。新しい版が出たら、ZIPを入れ替えてください。

## {{L_chat}}. Claudeチャット：スキルをアップロードする

claude.aiやClaudeアプリで使う方法です。

1. 使いたいスキルのZIPをダウンロードします。
{{skills_list_indented}}
2. Claudeの **Customize → Skills** を開き、追加ボタンから **Upload a skill** を選びます。
3. ZIPを1つずつアップロードし、スキルを有効にします。

**ご注意**

- Claude Code用プラグインのZIPは、ここでは使えません。スキルのZIPを使ってください。
- ZIPのファイル名は変えずにアップロードしてください。
- スキルを使うには、設定で「コード実行」が有効になっている必要があります。詳しくは [Claudeの公式案内](https://support.claude.com/en/articles/12512180-use-skills-in-claude) をご覧ください。
- 組織のアカウントでは、管理者の設定によって使えない場合があります。
- アップロードしたスキルは自動では更新されません。新しい版が出たら、もう一度アップロードしてください。

## 2. 使ってみる

最初は、ファイルを変更しない依頼で試すのがおすすめです。

> {{lang}}のWebページをつくる予定です。気をつけるポイントを教えてください。ファイルは変更しないでください。

## ファイルが正しいか確認する（任意）

ダウンロードしたファイルが壊れていないかを確認したい場合は、[SHA256SUMS.txt]({{sums}}) を使います。

ダウンロードしたZIPファイルと同じフォルダーに SHA256SUMS.txt を置き、ターミナルで次のコマンドを実行します。`shasum` がない環境では、Windows PowerShellの `Get-FileHash` などでSHA-256を照合してください。

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

ダウンロードしたファイルの行に `OK` と表示されれば問題ありません。

---

ほかのツール：[ChatGPT・Codex]({{page_chatgpt}}) ・ [Gemini]({{page_gemini}})

画面や提供条件は変わることがあります。最新の情報は各サービスの公式案内をご確認ください（本ページの確認日：2026年10月14日）。
