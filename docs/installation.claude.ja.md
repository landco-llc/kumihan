# Claude向け導入と更新

[English](installation.claude.md) · [GPT・Codexの導入](installation.ja.md) · [Claude配布ファイル](../downloads%20Claude/)

**0.1.0-preview.1** の配布プレビューです。Claude CodeとClaudeチャットは別の導入経路です。実際のインストール・アップロード・検出・呼び出し・更新は未検証です。開発者名は **L&Co.LLC**。96スキルファイルとGPT-Codex配布物は変更していません。

## Claude Code：Git marketplace

[公式インストール案内](https://code.claude.com/docs/en/discover-plugins)に従い、対応版で内容と利用範囲を確認して導入してください。Gitからカタログを登録する例:

```sh
claude plugin marketplace add "https://github.com/landco-llc/kumihan.git#main"
```

Claude Codeの会話内で詳細画面を開く例:

```text
/plugin install kumihan@kumihan-marketplace
```

内容とユーザー／プロジェクト／ローカル等のスコープを選びます。導入後は `/kumihan:kumihan`、`/kumihan:kumihan-web`、`/kumihan:kumihan-documents`、`/kumihan:kumihan-review` 等が表示されるか、ローカル参照を解決できるかを確認してください。ここでは上記操作を実行していません。

明示的にカタログと導入済みプラグインを更新する例:

```sh
claude plugin marketplace update kumihan-marketplace
claude plugin update kumihan@kumihan-marketplace
```

[公式更新案内](https://code.claude.com/docs/en/plugins/host-marketplace)のとおり、versionが同じままのGit変更を新しいプラグイン版として受け取るとは限りません。今後の内容変更では `.claude-plugin/plugin.json` のversionを更新します。versionはmarketplace側に重複記載しません。第三者marketplaceの自動更新は初期OFFです。この配布で自動更新を有効化・設定しません。実際の適用・再読み込みはホストの表示に従って確認してください。

## Claude Code：手動ZIP

[Claude Code用プラグインZIP](../downloads%20Claude/plugins/kumihan-Claude-Code-plugin-0.1.0-preview.1.zip)を検証・展開すると `kumihan/` が得られます。ローカル読み込みを試す例:

```sh
claude --plugin-dir "/absolute/path/kumihan"
```

これは展開済みフォルダーの読み込み例であり、marketplace登録やClaudeチャットへのSkillアップロードではありません。`.claude-plugin/plugin.json` と全 `skills/`、ライセンス・通知を保持してください。機密ファイルを混ぜず、既存フォルダーを上書きしないでください。

## Claudeチャット：単独Skill ZIP

[公式Skills案内](https://support.claude.com/en/articles/12512180-use-skills-in-claude)はFreeを含む各プランと、コード実行機能が必要であることを説明しています。組織の権限や提供状況も確認してください。設定操作は利用者側の選択であり、ここでは変更していません。

`Customize > Skills` の追加操作から `Upload a skill` を選び、[単独Skill ZIP](../downloads%20Claude/skills/)を1つずつ追加します。プラグインZIPをこの画面にアップロードしないでください。単独ZIPはSkill名のトップフォルダーと `SKILL.md`、全24ファイルを含みます。ファイル名・大小文字を変更せず、追加後に有効化と利用を確認してください。Git pushやClaude Codeの更新は、手動アップロードしたSkillを自動更新しません。

## ファイルの確認と限界

[SHA256SUMS.txt](../downloads%20Claude/SHA256SUMS.txt) と [MANIFEST.json](../downloads%20Claude/MANIFEST.json)を同じ版から取得し、ZIPを `plugins/` と `skills/` に配置します。配布フォルダーの親からmacOSで確認する例:

```sh
cd "downloads Claude"
shasum -a 256 -c SHA256SUMS.txt
```

全行がOKであることを確認してください。ハッシュ一致は導入成功や安全性の認証ではありません。Skillsは指針であり自動検出器ではなく、描画・Officeネイティブ互換性も未検証です。Claudeの公式validator・実機による確認は未実施です。静的な名前・構造・参照確認だけで、ホスト受け入れを保証しません。
