<!-- Generated from authored installation Markdown; do not edit. -->
# Geminiへの導入

[English](installation.gemini.md) ・ [トップに戻る](../README.md)

<br>

KUMIHANをGemini CLIやGeminiアプリで使うための手順です。

> **v0.1.8について**
> ご自身の環境で導入を試していただくための版です。各ツールでの動作はまだ十分に確認できていないため、うまく動かない場合があります。

<br>

## 1. 導入方法を選ぶ

| 使いたい場所 | おすすめの方法 |
| --- | --- |
| Gemini CLI（4つまとめて） | [A. 拡張機能として導入する](#a-gemini-cli拡張機能として導入する) |
| Gemini CLI（必要なものだけ） | [B. スキルを選んで導入する](#b-gemini-cliスキルを選んで導入する) |
| Geminiアプリ（Web・Mac・スマートフォン） | [C. スキルをアップロードする](#c-geminiアプリスキルをアップロードする) |

<br>

## A. Gemini CLI：拡張機能として導入する

4つのスキルをまとめて導入する方法です。

```sh
gemini extensions install https://github.com/landco-llc/kumihan --ref main
```

確認画面が表示されたら、内容を確認して進めてください。拡張機能は、導入するとすべてのプロジェクトで有効になります。

**更新するとき**

```sh
gemini extensions update kumihan
```

更新したあとは、Gemini CLIを再起動してください。

**ZIPから導入する場合**

1. [拡張機能のZIP](https://github.com/landco-llc/kumihan/releases/download/v0.1.8/kumihan-Gemini-CLI-extension-0.1.8.zip) をダウンロードします。
2. 空の `kumihan` フォルダーを作り、その中に展開します。
3. フォルダーを指定して導入します。

   ```sh
   gemini extensions install "/absolute/path/kumihan"
   ```

ZIPから導入した場合は、自動では更新されません。新しい版が出たら、ZIPを入れ替えてください。

<br>

## B. Gemini CLI：スキルを選んで導入する

必要なスキルだけを、プロジェクト単位で導入する方法です。Aで導入した場合、この手順は不要です。

たとえば `kumihan` を導入する場合は、対象のプロジェクトで次を実行します。

```sh
gemini skills install https://github.com/landco-llc/kumihan --path skills/kumihan --scope workspace
```

ほかのスキルを導入するときは、`--path` を次のように変えてください。

- `skills/kumihan-web` — Webページ
- `skills/kumihan-documents` — 報告書・スライド
- `skills/kumihan-review` — レビュー

`--scope workspace` は「このプロジェクトだけ」で使う設定です。省略すると、すべてのプロジェクトで使えるようになります。

**更新するとき**

同じコマンドをもう一度実行します。導入済みのスキルは置き換えられるため、ご自身で編集した内容がある場合は先に保存してください。

<br>

## C. Geminiアプリ：スキルをアップロードする

1. 使いたいスキルのZIPをダウンロードします。
   - [kumihan](https://github.com/landco-llc/kumihan/releases/download/v0.1.8/kumihan-Gemini-Apps-skill-0.1.8.zip) — 最初の入口
   - [kumihan-web](https://github.com/landco-llc/kumihan/releases/download/v0.1.8/kumihan-web-Gemini-Apps-skill-0.1.8.zip) — Webページ
   - [kumihan-documents](https://github.com/landco-llc/kumihan/releases/download/v0.1.8/kumihan-documents-Gemini-Apps-skill-0.1.8.zip) — 報告書・スライド
   - [kumihan-review](https://github.com/landco-llc/kumihan/releases/download/v0.1.8/kumihan-review-Gemini-Apps-skill-0.1.8.zip) — レビュー
2. Geminiの **Customize**（見当たらない場合は **More**）→ **Skills** → **Upload** を開きます。
3. ZIPを1つずつ選び、内容を確認して **Create** を押します。

**ご注意**

- 利用できるのは、18歳以上の個人のGoogleアカウントです。仕事用・学校用のアカウントでは、現在は使えません。
- 「Keep Activity（アクティビティの保存）」をオンにしておく必要があります。
- 機能は順次提供されているため、まだ表示されない場合があります。詳しくは [Geminiの公式ヘルプ](https://support.google.com/gemini/answer/17094296?hl=ja) をご覧ください。
- 拡張機能のZIP（Gemini CLI用）は、ここでは使えません。
- アップロードしたスキルは自動では更新されません。新しい版が出たら、もう一度アップロードしてください。

<br>

## 2. 使ってみる

最初は、ファイルを変更しない依頼で試すのがおすすめです。

> 日本語のプレゼン資料をつくる予定です。気をつけるポイントを教えてください。ファイルは変更しないでください。

<br>

## ファイルが正しいか確認する（任意）

ダウンロードしたファイルが壊れていないかを確認したい場合は、[SHA256SUMS.txt](https://raw.githubusercontent.com/landco-llc/kumihan/d3d55a344ab5cfe942a640261f9a8760fceee2a2/downloads%20Gemini/SHA256SUMS.txt) を使います。

ダウンロードページと同じフォルダー構成（`extensions/` と `skills/`）でファイルを置き、ターミナルで次のコマンドを実行します。`shasum` がない環境では、Windows PowerShellの `Get-FileHash` などでSHA-256を照合してください。

```sh
cd "downloads Gemini"
shasum -a 256 -c SHA256SUMS.txt
```

すべての行に `OK` と表示されれば問題ありません。

<br>

---

ほかのツール：[ChatGPT・Codex](installation.ja.md) ・ [Claude](installation.claude.ja.md)

画面や提供条件は変わることがあります。最新の情報は各サービスの公式案内をご確認ください（本ページの確認日：2026年10月14日）。
