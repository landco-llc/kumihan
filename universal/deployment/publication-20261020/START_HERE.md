# OpenAI公開申請管制 — 実行指示

状態: `PUBLICATION_PRE_SUBMISSION_HOLD` / Owner Gate未承認。

## 権限と正本

今回のユーザー依頼を権限の根拠とする。添付引き継ぎは制御仕様と過去観測であり、最新実測や承認の代わりではない。原本は同ディレクトリの `KUMIHAN_Universal_OpenAI_Publication_Control_Handoff_20261020.md` に保存。

環境: Codex Cloud / App。リポジトリ `landco-llc/kumihan`、ブランチ `control/openai-publication-20261020`。起点はDraft PR #101の `d3dff4eff590980e115d002b93bca4d51b20169f`。mainは `8b647cc752d7a9bc3db48356fa0ab7b221bb66d6`。このブランチ全体をmainへマージしない。PR #101由来の実装を含むため、文書変更だけをレビューする。

## 連続実行

- [ ] W00: `00_FRESH_READ_AND_BASELINE.md` の未確認をアクセス可能な環境で補完。PlatformはL&Co. LLC / kumihan-universal / v0.1.0を読戻すだけ。法人・ドメイン・ZIP登録・4 Skill検査を再実行しない。
- [ ] W01: `01_PRIVACY_TERMS_DRAFT.md` の事実未確定欄をOwner/運用者と確認。mainのprivacy.html / privacy-ja.htmlを基準に、既存多言語1ページ・アンカー・選択UIを保つレビュー用サイト差分を作る。法務公開はOwner承認まで停止。
- [ ] W02: `02_MCP_CONTRACT_QA.md` に従いSDK実シグネチャとセッション実装を確認し、4ツールのannotationsだけを限定修正。PHP 8.5・Composer環境でローカルtools/listと既存CIを検証。本番変更は別承認。LanguageRouter.phpは変更・同梱配布しない。
- [ ] W03: `03_REVIEW_TEST_CASES.md` と evidence/ を読んで未検証範囲を埋める。別管制から修正commit・本番適用証拠・回帰結果・復旧方法を受領するまで言語判定最終PASSにしない。
- [ ] W04: `04_SUBMISSION_PACKET.md` の説明・3プロンプト・動画脚本を最終実装に合わせ、実録画とレビュアー視聴URLを追加する。
- [ ] W05: `05_PLATFORM_FINDINGS_AND_RELEASE_GATE.md` を埋める。現登録ZIPの実バイト列とSHA・4 Skill一覧を得るまで再構築・アップロードしない。Scan Tools/フォーム更新前に最終差分を固定。SubmitにはOwner承認が必要。
- [ ] W06: `06_REVIEW_AND_PUBLICATION_RECORD.md`。提出承認後のみ提出。OpenAI承認後もOwnerのPublish承認まで公開しない。

各Workごとに証拠URL・commit/PR・実測PASS/FAIL・未確認・次アクションを記録。未確認をPASSにしない。challenge token、資格情報、絶対サーバーパス、顧客原稿は保存しない。Google Driveへの保存はツール成功を確認して別記する。

## 起動文

> landco-llc/kumihan の control/openai-publication-20261020 を開き、universal/deployment/publication-20261020/START_HERE.md と添付原本を読む。W00〜W06を連続推進し、証跡・未確認を分離して更新する。法人確認・ドメイン検証・ZIP登録・4 Skill検査は繰り返さない。自動言語判定は別管制。法務公開・本番MCP変更・審査提出・一般公開の各Owner Gateでは、具体的差分と証拠を揃えて停止する。
