# START_HERE — KUMIHAN 日本語版 v0.2.0 W09限定修正

- 承認: Owner「推奨を承認」（2026-10-20 JST）= W09限定修正の実行許可。merge/公開は未承認。
- Repository: `landco-llc/kumihan`
- 管理: https://github.com/landco-llc/kumihan/issues/121
- 親: https://github.com/landco-llc/kumihan/issues/119
- 対象: https://github.com/landco-llc/kumihan/pull/123
- 指示branch: `control/ja-v020-w09-20261020`
- 観測PR #123 HEAD: `384f073ba122abde42f5836b15650c055928e724`
- 起動環境: Codex CloudまたはCodexアプリ。ローカルCodex CLI / Remote Desktopで代行しない。

## 実行前に読む

1. `docs/development/ja-v020-20261020/qa/w09/WORKGROUP.md`
2. `docs/development/ja-v020-20261020/qa/w09/ACCEPTANCE.json`
3. `docs/development/ja-v020-20261020/qa/RESULT.md`
4. `docs/development/ja-v020-20261020/qa/evidence/documents-result.md`
5. `docs/development/ja-v020-20261020/qa/evidence/web-result.md`
6. `docs/development/ja-v020-20261020/qa/evidence/independent-review.md`
7. `tools/qa_documents_v020.py` / `tools/qa_web_acceptance.py`
8. 旧PR #123レビューとIssue #121最新コメント（QA-V03、V04、V05）。

## 起動

- W09-00 Fresh Readで現在のPR #123 HEAD/TREE、main、並行PR #101/#116/#118、clean worktreeを検証。異なれば上書きせず新しい事実を固定する。
- `control/ja-v020-w09-20261020` の本指示を含む状態から `fix/ja-v020-w09-20261020` を作業branchとして用意する。存在済みbranchは保全する。
- W09-01〜03は独立に自律継続してよい。W09-04〜06で回帰・独立レビュー・結果報告を統合する。無用なWork単位ごとの承認質問は不要。
- **必ず実原稿を一字も変えず**、新しいPDF全ページ・Web20状態・PPTX8枚を再描画・目視し、残るP1を失敗/未確認と分ける。
- 新しい証拠は `qa/w09/evidence/`、最終結果は `qa/w09/RESULT.md`。旧QAと失敗対照を上書き・「passed」へ書換えしない。
- Final implementation HEADでCI/15 ZIPと他20言語を再確認。新しいDraft stacked PRをbase `qa/ja-v020-acceptance-20261020` に提出し、Issue #121 / #119へ一括報告。
- 最後はOwner Gate停止。main merge/tag/Release/Pages/Marketplace/Universal MCP本番変更なし。

## 報告様式

`VERIFIED | PARTIALLY_VERIFIED | FAILED | NOT_CHECKED` を対象・方法・環境別に記載。
最終HEAD/TREE、Draft PR、新旧の行分割画像、PDF全ページ、Web各状態、PPTX全8枚、実際のLOコピー/抽出・字間の別結果、最新CI URL、全15 ZIP digest、不変ファイル数、P0/P1、native host未確認と次Owner Gateを提示する。

本書の作成は、実装・QA実行・修正完了の証拠ではない。
