# KUMIHAN の Gemini での利用（プレビュー）

[English](installation.gemini.md) · [配布物・SHA256](../downloads%20Gemini/README.md)

開発者: L&Co.LLC。`0.1.0-preview.1` は配布形式のプレビューです。Gemini CLI / Apps への実インストール、受理、呼び出し、更新は未検証です。安定版・Google公式掲載・対応保証を意味しません。4スキルは日本語組版の指針で、自動検出ツールではありません。公式情報確認日: 2026-10-14。

## Gemini CLI: 4スキル入り extension

[公式 extension 手順](https://geminicli.com/docs/extensions/reference/)に従い、CLI と Git を用意した利用者が任意で実行します。

```sh
gemini extensions install https://github.com/landco-llc/kumihan --ref main
```

リポジトリ直下の `gemini-extension.json` と `skills/<name>/SKILL.md` が入口です。extension は既定で全体に有効になるため、インストール先・同意画面を確認してください。この配布に MCP サーバー、フック、秘密情報設定はありません。既に同名スキルを別経路で入れている場合は重複を確認します。

Gitへのpushだけで手元のコピーは更新されません。更新時は次を明示的に実行し、CLIを再起動します。将来の配布変更では extension のバージョンも更新する必要があります。

```sh
gemini extensions update kumihan
```

手動ZIPは [extension ZIP](../downloads%20Gemini/extensions/kumihan-Gemini-CLI-extension-0.1.0-preview.1.zip) を空の `kumihan` フォルダに展開します。直下に `gemini-extension.json` があることを確認し、そのフォルダをローカルソースとして指定します。

```sh
gemini extensions install "/absolute/path/kumihan"
```

この手動経路はGit追従ではありません。新しいZIPへ手動で置き換え、利用中のCLIのローカルソース更新手順を確認してください。ZIPを直接渡す操作はここでは案内しません。

## Gemini CLI: 単独スキルを選ぶ

extension を使う場合、この追加操作は不要です。[公式 Agent Skills 手順](https://geminicli.com/docs/cli/skills/)に基づき、対象プロジェクトで例を実行します。

```sh
gemini skills install https://github.com/landco-llc/kumihan --path skills/kumihan --scope workspace
```

必要なスキルだけ `--path` を `skills/kumihan-web`、`skills/kumihan-documents`、`skills/kumihan-review` に変えます。`workspace` はプロジェクト単位で、既定の `user` は個人全体です。更新は同じインストール操作を再実行します。[公式実装](https://github.com/google-gemini/gemini-cli/blob/main/packages/cli/src/utils/skillUtils.ts)では同名のインストール済みディレクトリを置き換えるため、ローカル編集がある場合は先に保存してください。`/skills reload` は検出一覧の読み直しで、Gitダウンロードではありません。独立した `gemini skills update` は案内しません。

公式実装のCLIファイル入力は ZIP を `.skill` 拡張子で扱います。このページの Apps 用 `.zip` はCLI用 `.skill` として検証していません。CLIには上記Git経路または展開済みスキルディレクトリを使い、拡張子だけの変更で互換性を想定しないでください。

## Gemini Apps: 個人アカウントのアップロード

[公式 Skills ヘルプ](https://support.google.com/gemini/answer/17094296?hl=ja)では、18歳以上の個人Googleアカウント、Keep Activity有効が条件で、段階的提供です。仕事・学校アカウントは現時点で対象外です。利用者自身の設定・提供状況を確認してください。Web / Mac / モバイルでの表示はアカウントや展開状況により異なります。

Webでは Customize（見つからなければ More）→ Skills → Upload から、[skills フォルダ](../downloads%20Gemini/skills/)の Apps 用 ZIP を1つずつ選び、内容確認後 Create を選びます。4つは選択式です。各ZIP直下に `SKILL.md` と同じスキルの23参考ファイルがあります。extension ZIPはこの画面用ではありません。

AppsはGit更新に追従しません。更新時は新しいZIPを手動アップロードし、既存スキルの差し替え・重複を確認します。本配布は全ファイルがテキストで、各ZIPの展開サイズは100MB未満です。Appsの実受理と適用は未検証です。

[ChatGPT / Codex](installation.ja.md) · [Claude](installation.claude.ja.md) · [更新案内](updates.md)
