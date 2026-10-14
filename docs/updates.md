# Gitからの導入と更新 / Git installation and updates

[日本語の導入ガイド](installation.ja.md) · [English installation guide](installation.md)

このGit配布は既存の4つの `skills/` フォルダーを共有します。README、96スキルファイル、公開ZIPは変更していません。実機での導入・更新・呼び出しは未検証です。下記は利用者が自分の環境で実行する手順例であり、ここでは実行していません。

## 単独Skill / Standalone skills

[skills CLIの公式案内](https://github.com/vercel-labs/skills)を確認し、利用するCLI版と導入先を確認してください。CLIは外部ツールです。Node/npmとGitを利用できる環境から、対象Skillを明示して導入する例:

```sh
npx skills add landco-llc/kumihan --agent codex --skill kumihan --skill kumihan-web --skill kumihan-documents --skill kumihan-review
```

個人用の `--global` や確認省略オプションを指定していません。画面に表示される導入先と対象を確認してください。対応版のCLIで、導入済みの4つだけを明示して更新する例:

```sh
npx skills update kumihan kumihan-web kumihan-documents kumihan-review
```

更新対象のスコープと差分を確認し、導入済みコピーに独自編集がある場合は退避・競合解決を先に行ってください。Gitへのpushだけでコピーが常時更新される方式ではありません。手動コピーで導入したフォルダーがCLI管理対象になるとは限りません。

These optional commands use the third-party skills CLI to select four skills and explicitly refresh installed copies. Confirm its version, destination and scope; preserve local edits. Neither command was run here. A Git push alone is not an installed-copy refresh.

## CodexのGit marketplace / Codex Git marketplace

[OpenAIのプラグイン配布案内](https://developers.openai.com/plugins/build/plugins)を確認してください。このリポジトリの `.agents/plugins/marketplace.json` は `kumihan-git` というカタログで、同じリポジトリのルートプラグインをGit sourceとして参照します。ルート `plugin.json` と互換マニフェストは既存の `skills/` を利用し、複製したペイロードはありません。

対応CodexのCLIでカタログを登録・更新する例:

```sh
codex plugin marketplace add landco-llc/kumihan --ref main
codex plugin marketplace upgrade kumihan-git
```

登録後は対応するPlugins画面で **KUMIHAN Git Preview** を選び、**KUMIHAN Private Install Preview** の内容と導入先を確認して利用します。カタログ登録、プラグイン導入、更新後の新しい会話での検出は別々に確認してください。CLI・画面・キャッシュ更新の対応はホストに依存し、このパッケージでの受け入れは未検証です。

The catalog references this repository's root plugin on `main`, sharing the four existing skill folders. Registration and refresh are explicit host operations; installed cache behavior is untested. Plugin identity remains `kumihan-private-install-preview`, version `0.1.0-preview.1`, matching the existing ZIP. This does not modify an existing personal or workspace plugin automatically.

## 更新の範囲 / Update boundaries

| 経路 / Route | 更新の扱い / Behavior |
| --- | --- |
| Git → 単独Skill | CLI等による明示的な取得・更新。Installed copies need an explicit refresh. |
| Git → marketplaceプラグイン | ホストによるカタログ・キャッシュ更新。Refresh depends on the host. |
| Git → 公開ZIP | 現在のZIPは固定スナップショット。No automatic rebuild is provided. |
| ChatGPTの個人ZIPアップロード | アップロード時のスナップショット。No Git auto-sync is provided. |
| ChatGPTワークスペース同期 | 管理者の別設定・権限・対応状況による。Separate admin-managed configuration, not established here. |

公開ZIP、SHA256SUMS、マニフェストは[配布フォルダー](../downloads%20GPT-Codex/)の既存版を保持しています。将来Gitプラグインの内容を変えるときは、両マニフェストのversionを同時に更新し、別途許可された配布更新として差分・ハッシュを確認してください。同じ版のZIPを黙って再生成しません。追従する `main` と固定コミットの選択は利用者の更新方針に依存します。

No background updater, runtime fetch of instructions, hook, MCP server, credentials, project configuration, Actions workflow or ZIP rebuild is added. These guidance skills require no network lookup at use time. Static format checks do not prove host discovery, invocation, rendering or stable-release acceptance.
