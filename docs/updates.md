# 更新ガイド / Update guide

[トップに戻る](../README.md) ・ [English](#english)

<br>

**公開中の最新版は [v0.1.5 preview](https://github.com/landco-llc/kumihan/releases/tag/v0.1.5-preview)（2026年10月18日公開）です。**

KUMIHANを新しい版に更新する方法です。導入した方法によって、更新のしかたが異なります。

GitHub上でKUMIHANが新しくなっても、**お手元のコピーは自動では更新されません。** 以下の手順で更新してください。

<br>

## 導入方法ごとの更新のしかた

| 導入した方法 | 更新のしかた |
| --- | --- |
| Claude Code（GitHubから導入） | [コマンドで更新](#claude-code) |
| Codex（マーケットプレイスから導入） | [コマンドで更新](#codex) |
| Gemini CLI | [Geminiのガイド](installation.gemini.ja.md) を参照 |
| スキル管理ツール（skills CLI）で導入 | [コマンドで更新](#skills-cli) |
| ZIPをアップロード・展開して導入 | 新しいZIPをダウンロードして、入れ替える |

<br>

## Claude Code

```sh
claude plugin marketplace update kumihan-marketplace
claude plugin update kumihan@kumihan-marketplace
```

更新したあとは、Claude Codeを再起動してください。

自動更新は初期設定ではオフになっています。

<br>

## Codex

GitHubからKUMIHANを導入・更新できます。

**はじめて登録するとき**

```sh
codex plugin marketplace add landco-llc/kumihan --ref main
```

登録したら、Pluginsの画面で **KUMIHAN Git Preview** を選び、**KUMIHAN Private Install Preview** をインストールします。

**更新するとき**

```sh
codex plugin marketplace upgrade kumihan-git
```

更新したあとは、新しい会話で使ってください。

詳しくは [OpenAIのプラグイン案内](https://developers.openai.com/plugins/build/plugins) をご覧ください。

<br>

## skills CLI

[skills CLI](https://github.com/vercel-labs/skills) は、さまざまなAIツールにスキルを導入できる外部ツールです。Node.js（npm）とGitが必要です。

**導入するとき**（Codexに4つのスキルを導入する例）

```sh
npx skills add landco-llc/kumihan --agent codex --skill kumihan --skill kumihan-web --skill kumihan-documents --skill kumihan-review
```

**更新するとき**

```sh
npx skills update kumihan kumihan-web kumihan-documents kumihan-review
```

実行すると導入先が表示されるので、確認してから進めてください。

<br>

## 更新するときのご注意

- ご自身でスキルの中身を編集している場合は、更新すると上書きされることがあります。先に保存しておいてください。
- ZIPを手動でコピーして導入したスキルは、skills CLIでは更新できない場合があります。その場合は、新しいZIPで入れ替えてください。

<br>

---

<a id="english"></a>

## English

**Current release: [v0.1.5 preview](https://github.com/landco-llc/kumihan/releases/tag/v0.1.5-preview) (October 18, 2026).**

KUMIHAN does not update itself. When a new version is published on GitHub, update your copy using the method that matches how you installed it.

| Installed with | How to update |
| --- | --- |
| Claude Code (from GitHub) | `claude plugin marketplace update kumihan-marketplace`, then `claude plugin update kumihan@kumihan-marketplace` |
| Codex (marketplace) | `codex plugin marketplace upgrade kumihan-git` |
| Gemini CLI | See the [Gemini guide](installation.gemini.md) |
| skills CLI | `npx skills update kumihan kumihan-web kumihan-documents kumihan-review` |
| ZIP upload or extracted folder | Download the new ZIP and replace the old one |

**Codex: first-time setup**

```sh
codex plugin marketplace add landco-llc/kumihan --ref main
```

Then open Plugins, choose **KUMIHAN Git Preview**, and install **KUMIHAN Private Install Preview**.

**skills CLI: first-time setup** (example for Codex)

```sh
npx skills add landco-llc/kumihan --agent codex --skill kumihan --skill kumihan-web --skill kumihan-documents --skill kumihan-review
```

[skills CLI](https://github.com/vercel-labs/skills) is a third-party tool that requires Node.js (npm) and Git.

**Before updating**

- If you have edited the skill files yourself, save your changes first. Updates may overwrite them.
- Restart the tool or open a new conversation after updating.
- Claude Code auto-update for third-party marketplaces is off by default.
