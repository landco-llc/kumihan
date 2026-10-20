# Work群 結果台帳 / 2026-10-20 JST

共通Git証拠: main [8b647cc](https://github.com/landco-llc/kumihan/commit/8b647cc752d7a9bc3db48356fa0ab7b221bb66d6)、[Draft PR #101](https://github.com/landco-llc/kumihan/pull/101) HEAD d3dff4e。管制文書はcontrol/openai-publication-20261020ブランチ、差分の基点はPR #101。commit/新PR URLは配置完了後のGit履歴・PRとDrive保存版を参照。

| Work | 成果 / 実測 | 未確認・ブロッカー | 次アクション |
|---|---|---|---|
| W00 | Git・サイト・MCP読戻しPASS、terms404・privacy不整合FAIL | Platform最新ドラフトとZIP実体未取得 | 00のアクセス可能Appで読戻し |
| W01 | 英日法務ドラフトとHTML改修仕様を作成 | 保持/ログ/委託先/私的窓口未確定、HTML差分未作成、法務承認なし | 01の事実確認、全翻訳とサイト差分、Owner公開承認 |
| W02 | 4ツール静的動作・注釈候補・限定展開/復旧仕様 | PHP/Composerなし、SDK実検証とパッチ未作成、本番変更承認なし | 02をPHP8.5環境で実装・テストし、差分をOwner提示 |
| W03 | 21/21取得、正常5+異常3は限定条件PASS。自動判定FAIL。Python28/29 | 別管制修正、レンダリング、エラー境界、Skill実ホスト操作 | 03と生ログを用いて未確認補完 |
| W04 | 英日説明、3 Starter prompts、release notes、90秒動画脚本 | 実録画/動画URLなし、最終版未確定 | 04を最終版に合わせて録画 |
| W05 | NO-GO判定・読戻し手順を作成 | Platformアクセス、現ZIP SHA、最新Findings、blocking 0証拠、提出承認なし | 05条件を満たしてOwnerへ提出判断提示 |
| W06 | NOT_STARTED、審査/公開記録枠を作成 | W05未通過、OpenAI審査とPublish承認なし | 提出承認→審査→別途公開承認 |

サイト証拠: [home](https://landco-llc.github.io/kumihan/) / [privacy](https://landco-llc.github.io/kumihan/privacy.html) / [terms404](https://landco-llc.github.io/kumihan/terms.html)。MCP証拠: [endpoint](https://mcp-kmhn.landco.co.jp/mcp)、evidence/live-mcp.json。Platform: [portal](https://platform.openai.com/plugins)、今回NOT_CHECKED_ACCESS。

法人確認・ドメイン検証・ZIP登録・4 Skillパッケージ検査は再実行していない。法務公開・本番変更・Submit・Publishも未実行。現在はレビュー用管制成果物の配置まででありW00〜W06全完了ではない。

## PR116同期 — KUMI-PR116-SYNC-CI-20261020-01 / 2026-10-20 JST

今回のユーザー依頼は既存PR116ブランチの同期とCI再検証のみを許可する。上段の公開申請W00〜W06は歴史的台帳であり、今回実行していない。`/goal`の開始機能は提供されていないため、通常の継続実行と進捗台帳を使用。

- WG00/W00–W01: Fresh Read完了。正確な同期前SHA・CIは00の追加欄。元15パス・元JSON・元差分を作業用領域に固定。
- WG01/W02–W03: upstreamをnon-FF merge、競合なし。元15パスと完全一致。LanguageRouter.php / smoke.php / test_deployment_target.pyはupstreamと同一blob。target.json全体は元と同値、G3・public_bootstrap_installed=true・public_release_authorized=false・production_fix_deployed=falseを保持。
- WG02/W04–W05: 00と本台帳へ追記のみ。evidenceの3ファイルとtarget.jsonは変更なし。Python 29/29 PASS。生成前のregistry --checkはOutdated registry artifactでFAIL（生成物はgit管理外）。既存workflow同様、使い捨て出力へbuild→--checkで21 modules PASS。ソースやregistryはcommitしない。CloudにPHP/ComposerがないためローカルPHPはNOT_CHECKED、Hosted PHP8.5を照合する。
- WG03/W06: 新HEADのHosted CI待ち。candidate-integrityはpull_request base main限定であり本PRのfeature baseではトリガー対象外（SKIPPEDをPASSに数えない）。
- WG03/W07: 限定独立レビューはCI照合後。
- WG04/W08: 結果追記・PRコメントへ継続。OWNER_GATE=HOLD。

Ruling: 指定外ソース/テスト/ZIP作成禁止を優先し、追加テスト・実装修正は行わず既存テストで検証する。公開申請用の旧作業開始指示は今回の権限外。履歴値の置換はしない。

### W06〜W08 返却票（初回検証済みsnapshot、最終HEADのCIはPR116結果コメントを正本とする）

PR116_SYNC_RESULT: SYNCED_CI_VERIFIED_OWNER_GATE（下記snapshot）
REPO: landco-llc/kumihan
PR101_UPSTREAM_SHA: 5d32ea64618e33a171705363c223fe43060c31e1
PR116_ORIGINAL_SHA: 4bd43f4047d4d77d3dd448eda05e82be9ea9a146
PR116_CURRENT_SHA: f6e8e0e564bc88f35c944d6f2d8ff8750ceb1fc4（この返却票追記前のCI検証対象）
PR116_TREE_SHA: f152eb10f46b15834cc4d31959c4707bf5bd330d（同snapshot）
PR116_DIFF_PATHS: 15、同期前と同一集合、allowlist外0
DOC_EVIDENCE_PRESERVED: PASS（target.jsonと既存evidence3ファイルは元HEADと同一blob）
PYTHON_TESTS: ローカル29/29 PASS、Hostedの既存unittestステップSUCCESS
PHP85_SMOKE: Hosted setup/lint/routing/review SUCCESS
MCP_SDK_HTTP: Composer install/validate/audit、initialize/tools/list/tools/call、模擬Lolipop HTTP SUCCESS
OTHER_REQUIRED_CI: registry build/check、shell/helper lint、限定public preflight失敗回帰、staging生成/非公開領域展開/アップロード SUCCESS。Candidate integrityはbase mainのみのPRトリガーで本PRは対象外・未実行。
CI_RUN_URLS: https://github.com/landco-llc/kumihan/actions/runs/39352285990
LIVE_PHP_UPDATED: NO
PLATFORM_SUBMITTED: NO
MAIN_OR_RELEASE_CHANGED: NO
OWNER_GATE: HOLD
BLOCKERS: 同期/Hostedステップ結果に未達なし。生ログ配信先403、PHP/Composer実バージョン・解決SDKパッチ版・tar内包SHAの生ログ読戻しはNOT_CHECKED。稼働MCP再試験/本番反映、Platform/法務/他クライアント/実レンダリングは未検証・未承認。
NEXT_START: 最終結果コメントのHEADとCIを照合してOwner判断。後続の統合・本番修正・法務公開・Platform処理は別途明示承認まで開始しない。

- Graph: `4bd43f4 + 5d32ea6 → 6551325` (non-FF merge) `→ f6e8e0e → この返却票だけを追記したcommit`。最後のcommit自身のSHA/TREEを本文へ自己参照で埋め込むことはできないため、最終SHA/TREE・最終CI IDは追記後にPR116コメントで固定する。上記snapshotを最終HEADの証拠に流用しない。
- CI fingerprint: run=39352285990 / attempt=1 / event=pull_request / suite=106638862352 / job=118398995799、2026-10-20T01:14:07Z〜01:14:26Z。APIのrun head/baseは上記snapshot/upstreamと一致。workflow `.github/workflows/universal-mcp-php.yml` SHA256=`35c5673e67ca08d56cf157dd40838803c776bf20617670cde49c96f0fc21d9c7`。全step conclusion=success、skipなし。
- 初回staging artifact ID=12233009596 / bytes=796923 / API digest=`sha256:1d07bded912f64f2eb96ff4ca85a85cfb0941d5ec585fc70f127469817c07bab`。これはGitHub artifactのdigestであり内包tarのSHAと同一視しない。Hosted展開smoke成功を確認、Cloudでartifact内容の独立再展開は未実施。配布/登録ZIPは作成・再登録していない。
- CI生ログは`gh run view --log`で配信先Forbidden。APIの実際のstep結果と当該workflow、http_smoke.pyを照合。Composerは`mcp/sdk ^0.9.0`、PHP設定8.5、Composer v2。composer.lockとregistry.jsonは当該Git treeに存在せずCIで生成するので、完全固定依存版とは主張しない。TLS stepは情報提供で失敗を吸収するため、step SUCCESSからTLS PASSを推認しない（本実行のTLS結果NOT_CHECKED）。
- W07独立read-onlyレビュー: PASS、P0/P1なし。元15パス/祖先/実装blob/G3/729・749/旧ja観測/過去ログ/機密非導入/両PR Draft OPENを照合。初回snapshotとCIを別reviewerが確認。本返却票は親agentが追加照合し、最終HEADはPRコメントで確認する。
- 今回の最小変更は00とWORK_RESULTSへの追記のみ。target.jsonのbaseline_main/baseline_pr101、21/729、21/749、FAIL_ja_kanaとproduction_fix_deployed=falseを変更しない。旧PHP CIのko誤判定は最新候補のrouting smoke成功と分離。live ja/kanaの再試験はNOT_CHECKED。terms404/privacy不整合は歴史観測、公開・提出NO-GOを継続。
- Driveへのprivate保存・readbackは未実施。許可された既存WORK_RESULTSとPR116コメントを返却先とする。設定/権限変更、main/PR101書込、tag/Release、本番操作、法務公開、Platform Scan/Submit/Publishは本Workで実行していない。
