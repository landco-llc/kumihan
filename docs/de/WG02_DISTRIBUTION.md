# WG02 — Satzbild 3ホスト配布とZIP検証（W04–W06）

Part of [GOAL_SATZBILD_V010.md](GOAL_SATZBILD_V010.md)
Prerequisite: WG01 の4 Skillsとmanifests実体、少量のコアテストPASS。**サイト制作に移る前に本WGを完了**する。

## W04 — Host adaptersと表示名/アイコンを固定

- 推奨パターンは既存 plugins/kumihan-grafia/ と tools/build_grafia.py。現行版の仕様・ディレクトリに合わせて最小変更でドイツ語版を作る。
- ChatGPT/Codex用 portable agent plugin / .codex-plugin、Claude Code plugin（.claude-plugin/）、Gemini CLI extension（gemini-extension.json/GEMINI.md）を作る。
- 各ホストの manifest を公式仕様と既存受入テストの両方で検証する。schema上ASCII必須の name と利用者向け displayName を区別。
- 利用者が見る plugin表示名は全ホスト **KUMIHAN｜Satzbild** だけ。バージョンや「German edition」「Claude」「Gemini」の接尾辞禁止。ファイル名と technical IDs は別。
- 全 host の description/short/long と4 Skillsのfrontmatter descriptionは ドイツ語 | 英語（意味を揃える）。著作/開発者名は L&Co. LLC。
- 既存公式PNGを正しい相対参照へコピー。root plugin、skills、supported logo/composerIcon、Claude iconなど実装に必要な配置を満たす。プラグイン／skillごとの実Host表示はnative起動を実施した場合だけ verified。

## W05 — 再現性のある15 ZIP

- products/pluginsの書込対象は新規 plugins/kumihan-satzbild/**。builder は tools/build_satzbild.py 推奨（現行命名規則に合わせて調整可）。
- 3ホスト群 × （pluginまたはextension1 + standalone skill4）= **15 ZIP**。ZIP名すべてに **-v0.1.0.zip** を含める。
- 例: kumihan-satzbild-GPT-Codex-plugin-v0.1.0.zip / kumihan-satzbild-Claude-Code-plugin-v0.1.0.zip / kumihan-satzbild-Gemini-CLI-extension-v0.1.0.zip。
- 例: kumihan-satzbild-web-GPT-Codex-skill-v0.1.0.zip / kumihan-satzbild-documents-Claude-skill-v0.1.0.zip / kumihan-satzbild-review-Gemini-Apps-skill-v0.1.0.zip。完全なスキル4個 × 3ホストの名称は builder で一意に規定。
- 各アーカイブには必要な manifests、4 Skillsの場合は各々の独立SKILL.md＋ローカルreferences、schemas、locale、rules、sources、test/readme、公式iconを閉包させる。ローカル絶対パス、他言語参照やSymlinkの不足を許さない。
- ZIP内部の version 0.1.0 / displayName / locale が一致。文字コードはUTF-8を維持。ファイル名順序・timestamp・permissions を安定化し、入力同一ならbyte-identical。外部依存実行やネットワーク取得をbuilderの必須要件にしない。
- plugins/kumihan-satzbild/downloads/** にZIP15・MANIFEST.json・SHA256SUMS.txtを記録。host、source path、SHA-256、サイズ、公開tag、公式ロゴdigest、native host/marketplace statusを正直に持たせる。
- buildコマンドと **--check** の非書込モードを用意する。checkは差分があればexit nonzero、mtimeを変えず、ZIP CRC、メンバー名、file size、SHA、参照閉包、重複ファイルを調べる。
- README / INSTALL / UPDATES / THIRD_PARTY_NOTICESで各ホストの具体的な導入手順を文書化する。ChatGPTプラグイン登録、Claude Code plugin、Gemini CLI extension、チャット製品のスキル導入は製品ごとに機能/条件が違うため、未対応のinstallコマンドを断定しない。プラグインストア掲載は別。

## W06 — 配布動作のfocused testと品質レシート

- tests/satzbild/ へ十分なfocused tests（目安20個程度）を用意。JSON schema、説明文のDE/EN、plugin displayName、author、icon実体、4 standalone Skills、15 ZIP、manifest、digest、内容の保護、--checkの非破壊性、パス逸脱や不正ZIP、localeと数字/引用符の例外を試験。
- Claude CLI / Gemini CLI / agent plugins validatorを実行できる場合は実行。環境未提供ならnot-checkedにし、manifestの静的検証PASSと区別。
- 既存日本語KUMIHAN、字衡、既存個別言語の主要テスト（範囲とコマンドをledger記録）を実行。既存の別言語配布物・manifest digestが変わっていないことを確認。
- 受入表: ①Skill4 ②各Host package5×3 ③icon実体 ④DE/EN metadata ⑤インストール先に応じたPATH ⑥ZIP digest ⑦研究44候補/48ケースの実装・未検証状態 ⑧原稿保護 ⑨既存回帰。
- docs/de/EXECUTION_LEDGER.mdへ各条件のPASS/FAIL/NOT-CHECKEDとコマンド、artifact SHA、作成時刻（timezone付）を書き込む。
- PR段階でCIは lightweight focused tests + package check + main相当の後方互換確認。OS全種類の手動installは要求しない。

## WG02終端の決定

4スキルと3ホストmanifest、15 ZIP＋一覧・照合結果があり、基本テストが成功していれば次のWG03へ進む。**ここで初めてサイト制作開始を許可**。品質上のblockerが残るなら修正し、無関係なデザイン作業で隠さない。

配布アーカイブを先に完成させ、後からWebコピーに埋め込むリンクはその実在する名前を用いる。マーケットプレイスの申請や登録成功を捏造しない。
