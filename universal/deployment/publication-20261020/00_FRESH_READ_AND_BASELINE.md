# W00 — Fresh Read / 2026-10-20 JST

## 実測と証拠

| 対象 | 結果 | 証拠 / 限界 |
|---|---|---|
| main | PASS: 8b647cc752d7a9bc3db48356fa0ab7b221bb66d6 | https://github.com/landco-llc/kumihan/commit/8b647cc752d7a9bc3db48356fa0ab7b221bb66d6 / git fetchで確認 |
| PR #101 | PASS: open / Draft / unmerged / d3dff4e | https://github.com/landco-llc/kumihan/pull/101 / GitHub connectorとfetch一致 |
| deployment | PASS: 現行ソース読戻し | https://github.com/landco-llc/kumihan/tree/d3dff4eff590980e115d002b93bca4d51b20169f/universal/deployment |
| サイト | PASS: HTTPS 200 | https://landco-llc.github.io/kumihan/ |
| privacy | HTTP PASS / 内容不整合FAIL | https://landco-llc.github.io/kumihan/privacy.html / static Skillのみ、MCP導入前改定の記述が残る |
| terms | FAIL: HTTP 404 | https://landco-llc.github.io/kumihan/terms.html |
| 公開MCP | 接続ツール実呼出しPASS: 21モジュール / 749ルール | https://mcp-kmhn.landco.co.jp/mcp / 全件preview_unverified。直接HTTPはCloud proxy 403、接続済みMCP connector経由で観測 |
| 自動判定 | FAIL: 文字，排版。→ja / kana | 同MCP detect_language。ソース修正は既存PRにあるが本番適用を推認しない |
| Platform | NOT_CHECKED_ACCESS | https://platform.openai.com/plugins / proxy CONNECT 403、対応するドラフト読取API・ブラウザーtoolなし |

## 引き継ぎ済み事項（再実行しない）

法人認証済み、Domain verified、ZIP登録済み、4 Skill Checks passedは制御文書から継承。今回のPlatform独立再確認ではない。現行登録4 Skill名: kumihan-start / kumihan-web / kumihan-documents / kumihan-review。旧1 Skill ZIPは再利用しない。

過去の明示的Findingsは `Terms of service URL is required.` / `Incomplete review information`。現在の件数とMCP scan最終判定は未確認。Blocking 0とは記録しない。

PR本文と旧申請MDにはNOT DEPLOYED、ZIP未登録等の古い記述。target.jsonのchatgpt_connection.rules=729は過去観測として保持し、新観測749は追記で区別。mainにはprivacyがあるがPR #101の起点にはないため、法務差分は必ずmainの最新HTMLから作る。

## 次アクション

PlatformにアクセスできるCodex Appで現ドラフトの識別子・Findings・MCP annotations・登録ZIPの実体を読戻し。再認証・再登録は不要。W00全体はPARTIAL、公開判定NO-GO。
