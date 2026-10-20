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
