# KUMIHAN プレビューの導入

[English](installation.md) · [プロジェクト](../README.md)

この配布物は **0.1.0-preview.1** です。個人が自分の環境で導入を試すためのプレビューであり、監査済み安定版 v0.1、実行環境での動作保証、公開 Plugin Directory 掲載を示しません。ここでの「プライベート」は導入先の公開範囲を指します。GitHub 上のファイルは公開されます。

`downloads GPT-Codex/` は ChatGPT・Codex 向けの配布フォルダーです。ZIP名の `GPT-Codex-plugin` は4つの Skill をまとめたプラグイン、`GPT-Codex-skill` は単独 Skill を示します。名前は形式上の導入先を示し、実機動作の検証済み表示ではありません。

## ファイルを選ぶ

| 導入先・用途 | ファイル／フォルダー |
| --- | --- |
| ChatGPT の単独 Skills アップロードが利用できる環境 | 以下の単独 Skill ZIP を1つずつ選択 |
| 自分のアカウントへのプライベートプラグイン登録 | [プラグイン ZIP](../downloads%20GPT-Codex/plugins/kumihan-GPT-Codex-plugin-0.1.0-preview.1.zip) |
| ローカル Codex／Claude Code | [完全な skills フォルダー](../skills/)から必要なものをコピー |

単独 ZIP: [kumihan](../downloads%20GPT-Codex/skills/kumihan-GPT-Codex-skill-0.1.0-preview.1.zip)、[kumihan-web](../downloads%20GPT-Codex/skills/kumihan-web-GPT-Codex-skill-0.1.0-preview.1.zip)、[kumihan-documents](../downloads%20GPT-Codex/skills/kumihan-documents-GPT-Codex-skill-0.1.0-preview.1.zip)、[kumihan-review](../downloads%20GPT-Codex/skills/kumihan-review-GPT-Codex-skill-0.1.0-preview.1.zip)。各 ZIP は1つの Skill フォルダーを含みます。プラグイン ZIP は4つ全部とマニフェスト、元のロゴ、ライセンスを含みます。GitHub で各ファイルを開き、Raw／ダウンロード操作で ZIP 本体を保存してください。

[SHA256SUMS.txt](../downloads%20GPT-Codex/SHA256SUMS.txt) と [全メンバーの検証マニフェスト](../downloads%20GPT-Codex/MANIFEST.json)も同じ版から保存します。macOS では、配布フォルダーの構造を保持し、ZIPを `plugins/` と `skills/` に置いて確認できます。単独で保存した場合も対応する下位フォルダーに配置してください。

```sh
cd "downloads GPT-Codex"
shasum -a 256 -c SHA256SUMS.txt
```

全行が OK であることを確認してください。ハッシュは一致確認であり、ホスト互換性や安全性の認証ではありません。

## ChatGPT の単独 Skills

まず [OpenAI の Build skills](https://learn.chatgpt.com/docs/build-skills) を確認してください。現在の公式文書は単独 Skills の利用先にデスクトップアプリ等を挙げていますが、すべてのプランや画面で ZIP アップロードが提供されるとは確認できません。

自分の画面に Skills とアップロード操作がある場合だけ、単独 Skill ZIP を選び、表示される内容を確認して個人用として追加します。4つは個別に追加してください。プラグイン ZIP、リポジトリ全体の ZIP、SKILL.md だけを単独 Skill ZIP の代わりに使わないでください。通常のチャット添付はインストールの確認にはなりません。操作がない場合は、その環境でこの手順を利用できるとは判断せず、公式案内を確認します。

## ChatGPT のプライベートプラグイン

[Build plugins](https://learn.chatgpt.com/docs/build-plugins) と [Plugins](https://learn.chatgpt.com/docs/plugins) を確認してください。利用にはワークスペースの権限、Plugin Creator の提供状況、プランやアプリの対応が関係します。

対応環境では、新しい会話で `@plugin-creator` を選び、上記のプラグイン ZIP を添付して「このパッケージを自分用のプライベートプラグインとして登録してください。公開ディレクトリには提出しないでください」と依頼します。保存先がワークスペースになる場合もあるため、登録前に自分の個人アカウントを対象にできるか確認し、個人用に限定したい場合は不明なまま進めないでください。ローカルファイルを扱える対応 Codex 環境で依頼する場合は、ZIP の絶対パスを渡します。

これは Plugin Creator のパッケージ保存手順に基づく案内です。現在の公開公式ページだけでは全利用者向けの ZIP インポート画面は確立できず、この ZIP の新規登録から利用までの一連のテストも未実施です。自分の環境で登録機能が利用できない場合は、個人用登録を完了したとは扱わないでください。

登録が成功したら、自分の Plugins の Personal／Created by me 等に表示されたパッケージ内容を確認し、インストール操作が必要なら実行して、新しい会話で有効にします。表示名は **KUMIHAN Private Install Preview** です。作者専用のプライベートリンクから全員が導入できる方式ではありません。公開 Plugin Directory への提出は別手続きです。この配布はその審査を通過したものではありません。ポータルでの適格性やアカウントごとの制限は、ここでは確認していません。

## ローカル Codex と Claude Code

単独 Skill ZIP を展開すると `kumihan` 等の完全なフォルダーになります。これは Codex が扱う `SKILL.md` フォルダー形式です。プラグイン ZIP にはルート `plugin.json`、`.codex-plugin/plugin.json` の互換マニフェスト、4つの `skills/` フォルダーが含まれ、互換マニフェストは `skills: "./skills"` を宣言しています。形式上は Codex のローカル marketplace 経路で導入を試せる構成ですが、現在のホストでの受け入れや動作は未検証です。単独フォルダーの配置は ZIP アップロードとは別の方法です。[Codex の公式ローカル配置](https://learn.chatgpt.com/docs/build-skills)では、プロジェクトの `.agents/skills/` と個人用の `~/.agents/skills/` 等を説明しています。[Claude Code の公式配置](https://code.claude.com/docs/en/skills)は `.claude/skills/` と `~/.claude/skills/` です。同じホストの既存フォルダーを上書きせず、必要な Skill フォルダーを丸ごとコピーします。

たとえば、このリポジトリのルートで、導入先プロジェクトに同名フォルダーがないことを確認したうえで、1つをコピーする場合:

```sh
mkdir -p /path/to/your-project/.agents/skills
cp -R skills/kumihan /path/to/your-project/.agents/skills/
```

Claude Code では導入先を `.claude/skills/` に変えます。個人用ディレクトリへの配置は、その利用者が全プロジェクトで使いたい場合の任意の選択です。ここでは個人インストールを実行していません。フォルダー内の rules、profiles、references、schemas、sources、inventory.json、LICENSE を省略しないでください。

[公式プラグインの接続・テスト案内](https://developers.openai.com/plugins/deploy/connect-chatgpt)はローカル marketplace からの導入も説明しています。プラグイン利用と単独フォルダー配置は別経路です。Gitからの単独Skill導入とCodex marketplaceの登録・更新例は[Git導入と更新](updates.md)を参照してください。これらのコマンドとホスト動作は未実行・未検証です。

## 導入後の確認と限界

新しい会話で選択した Skill が表示されるか確認し、ChatGPT では `@`、Codex では `$`／`/skills`、Claude Code では `/kumihan` 等のホストに応じた方法で呼び出します。最初は「日本語の報告書について study モードで指針を説明してください。ファイルは変更しないでください」など、変更を伴わない依頼で試してください。表示、呼び出し、ローカル参照解決、出力をそれぞれ確認します。

4フォルダー、合計96ファイルは [固定ソース](https://github.com/landco-llc/kumihan/tree/180fdb2439c1e6a8563f24b4b29c666394bfaf67/skills) と同じバイトです。38ルールと6プロファイルは制作・レビューの指針であり、自動検出器の数ではありません。静的検証は、ChatGPT Chat／Work、Codex、Claude Code での検出・呼び出し・動作、実際の描画、Office ネイティブ互換性を証明しません。利用結果は未検証です。利用時に Python や開発用依存関係は不要ですが、制作・描画に使えるツールと権限はホストに依存します。

公式ページの確認日: 2026-10-14。画面や提供条件が変わった場合は、最新の公式案内と自分の画面を優先してください。

Claude向けは[Claudeの導入と更新](installation.claude.ja.md)を参照してください。
