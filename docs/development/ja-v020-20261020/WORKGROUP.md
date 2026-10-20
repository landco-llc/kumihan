# KUMIHAN 日本語版 v0.2.0 更新 Work群

- Workgroup ID: `KUMI-JA-V020-RESEARCH-WG-20261020-01`
- Owner依頼: 「今回のリサーチ・分析などを基に、KUMIHAN日本語版をv0.2.0としてアップデート。」（2026-10-20 JST）
- 状態: `READY_FOR_CODEX_IMPLEMENTATION`。この指示書の配置は製品実装・テスト成功・公開を意味しない。
- Repository: `landco-llc/kumihan`
- 観測main: `8b647cc752d7a9bc3db48356fa0ab7b221bb66d6`
- 観測tree: `b07f043a431eb6f76b55c8155d1ca4fb08f45793`
- 指示配置branch: `control/ja-v020-research-20261020`
- 指示配置path: `docs/development/ja-v020-20261020/WORKGROUP.md`
- 実装branch案: `feat/ja-v020-research-20261020`。同名が存在すれば実体を確認し、無断で上書きしない。
- 実行環境: Codex Cloud または Codexアプリの当該repo。管制チャットから自動起動しない。Remote Desktop経由のローカルCodex CLI起動は行わない。

## Goal / Architecture / Stack

**Goal:** 2026-10-20の日本語研究を、原稿保全と既存互換性を維持した日本語版v0.2.0の4スキル・参考資料・検証素材・配布候補へ反映する。

**Architecture:** 共通正本は `skills/kumihan/`。残る3スキルへ既存builderで同期する。研究の条件・限界を伴う判断支援を拡充し、検出器や組版エンジンが存在するかのような説明を追加しない。新しい文脈・証拠情報は参考資料または独立したexperimental sidecarとして保持する。

**Stack:** 既存Markdown / JSON / Pythonテスト・配布builder / HTML・CSSの検証素材。新しい本番サービスや有料API依存は追加しない。

**Spec:** 今回の研究設計 `KUMIHAN_JA_Update_Spec_20261020.md` draft 1.1、研究本文、30ケース。実行上の採否・境界は本書を優先する。研究ファイルの「未採用・未実装」は作成時点の記録として改変しない。本依頼による採用決定は別の実装記録に残す。

## 1. 採用する範囲と除外範囲

### 採用

1. 文字の役割、読者の課題、表現意図、prose / display / hybridの領域別評価。
2. 静的な文字列一致と、実字形・可視性・操作・意味判断の証拠の分離。
3. Web・文書レシピの過度な断定の修正。サイズ・比率は条件付きの比較開始値。
4. 日本語の文字・書体史、話し言葉と書き言葉、文章構成、改行、実フォント・字面・視距離に関する参照知識。
5. UPD-01〜10の説明・知識・fixture・検証運用への反映。ただし物理会場実験など未実施項目は未実施とする。
6. 日本語4スキル、ChatGPT/Codex・Claude・Geminiの既存配布物、日本語版サイト・導入説明・更新履歴の整合。

### 今回は実施しない

- 他20言語の一斉バージョンアップ、翻訳・デザインの横断改変。
- Universal MCPのPHP、Composer、言語自動判定、ツールI/O、本番配備。PR #101 / #116 / #118は別作業系統として保持する。
- 別管制で設計・予定扱いの共通資料生成機能。日本語固有の新規PPTX/PDFレンダラー等を先行実装しない。テストfixtureの生成とは区別する。
- 現行report schemaの破壊的変更、新しい必須profile / rule ID / statusの追加。
- 「AIらしさ」「美しさ」「意味改行の正解」の自動点数化、読者実験の捏造。
- mainへの直接push・merge、tag作成、Release公開、Pages本番反映、Marketplace提出、既存プラグインの無断差替え。まずDraft PRと配布候補まで進め、既存の最終Owner Gateへ戻す。

## 2. 不変条件

- 日本語の既存39 rule ID、6 media profile、7 status（passed / failed / needs-review / not-checked / unsupported / waived / not-applicable）を維持する。
- `skills/kumihan/rules/catalog.json` と `skills/kumihan/schemas/` の既存ファイルは原則byte不変。今回の補足を新規規則へ膨らませない。どうしても変更が必要なら理由と最小差分を別に報告し、既存契約を勝手に変更しない。
- 正しいschemaパスは `skills/kumihan/schemas/report.schema.json`。repo直下の `schemas/report.schema.json` ではない。現行reportは `additionalProperties: false`。role等を未知のトップレベルfieldとして混入させない。製品版0.2.0とschema IDの0.1.0は別物。
- 4スキルは `kumihan` / `kumihan-web` / `kumihan-documents` / `kumihan-review`。共有物は `skills/kumihan/` のみ編集し、`SKILL.md` と `inventory.json` の例外を守る。
- 保護された名称・日時・価格・数値・単位・句読点・異体字・結合文字を正規化／補完しない。口語を文語へ変更する許可を推測しない。
- 装飾意図の宣言は例外承認ではない。表示の一部が造形でも、必須情報の完全性・可視性・到達性は別に確認する。
- `passed` は対象と環境に限定する。CSS.supports、DOM内存在、PDF抽出一致、schema-validを実描画やネイティブ利用の合格へ昇格させない。
- 規範、ガイド、実験結果、メーカー説明、観察、推論、提案を分ける。フォント分類・UD表記・サイズ表だけで可読性を保証しない。
- 表示名は `KUMIHAN`。版表示は `v0.2.0`、日本語のcanonical manifestは `0.2.0`。版名を@呼出名へ加えない。発行者は既存方針の `L&Co. LLC`。既存アイコンとライセンスを維持する。
- 旧Release/tag/資産は不変。`published_version`を未公開の0.2.0へ偽装しない。Source版と公開版の差を表示できる既存仕組みを使う。
- Web/Office/物理会場の未対応は該当検証だけに限定する。追加の形式的read-only入場条件や全作業停止ループを新設しない。

## 3. 原本・スナップショット

研究本文と詳細データはOwnerの研究Drive正本および実行用ZIPに保持する。この公開指示書には認証情報・署名付きURL・私的なDriveの共有リンクを複製しない。同梱 `RESEARCH_CASES.md` は30ケースの実装用要約であり、実行結果ではない。

| 原本ファイル | SHA-256 |
| --- | --- |
| KUMIHAN_JA_Research_Report_20261020.md | 95a88d0d08350dce70310e1642cfc31c393ff0cd390600b138972d0299a05dd4 |
| KUMIHAN_JA_Update_Spec_20261020.md | 6107c893c6265690bfadf7f4f835bfe43911f0e903d734a974885af3796a51ad |
| KUMIHAN_JA_Validation_Cases_20261020.json | 630ac9bee505cbbf73e476a6b696a67f38d922667ca51e0578c19a33e6d7dced |
| KUMIHAN_JA_Sources_20261020.json | af7a81c636a86fc579090728bcf15700104cca1d7e1ea39a6a0cd07ca6f36e83 |

実行用ZIPを使う場合は上記hashを確認する。原本を読めない環境でも、本書とケース要約から確定した改訂・検証素材作成は進める。未取得の史実・実験数値は創作せず、追加の出典整備だけを限定保留とする。元の研究PDFを再生成する作業は含めない。

## 4. Work群 — W00からW09へ自律継続

各Workで対象、変更、検証、限界を記録する。変更前に対応する失敗テストを作り、失敗を確認してから最小修正し、再実行する。文書変更では具体的な矛盾・禁止表現・リンク整合と対照例を検証する。Workごとに不要なOwner再承認を求めず、独立して進められる項目を継続する。

### W00 — Fresh Readと差分保護（UPD-01）

- [ ] repo、branch、worktreeの変更、最新main、既存指示、各対象配下のAGENTS等を再確認。観測時はrepo直下AGENTS.mdは存在しなかったため、存在するふりをしない。
- [ ] `docs/development.md`、`docs/versioning.md`、`docs/version-automation/README.md`、4入口、catalog、profiles、schemas、実行対象tests、builderを読む。
- [ ] 観測mainから進んでいれば対象pathの差分だけ照合し、独立した他案件を巻き戻さず安全な最新baseを選ぶ。自分以外の未commit変更を消さない。
- [ ] baselineに39 ID、6 profile、schema/file hash、他言語manifest版、既存ZIP資産のpath/hash、最新公開JA版、既存失敗を保存。
- [ ] control文書を取り込んだ実装branchを用意し、他の開いたPRへ無断pushしない。

**成果:** `baseline.json`、対象path表、実際のbase SHA、既存失敗の記録。W00だけで完了扱いにしない。

### W01 — 文脈・証拠と情報領域（UPD-02/03/05）

**編集:** 4入口、`skills/kumihan/references/review-protocol.md`。**追加案:** 同references内 `typography-context.md`。

- [ ] briefへrole、readingTask、intentのdeclared/inferred/unknown、expressionMode、regionを導入。既存の短いbriefで足りる案件に長大な必須契約を追加しない。
- [ ] 必須情報をsource fieldと提示regionへ対応。exact-repeat / authorized-derived / decorative-echoを区別する。隠れたDOM、読者が使えないQR、発表者notesを自動的な代替としない。
- [ ] static / rendered / assisted / manualと観察scopeを既存reportの`scope`、`reason`、`evidence_refs`、`limitations`へ対応させる。必要な追加情報は独立sidecarで参照し、製品reportに未知fieldを追加しない。
- [ ] 独立sidecarを具体化するなら `references/experimental/` にdraft表示で置く。subject、context、typographyObservations、representationMap、evidence、findingsDraft、executionStatusを扱い、既存schemaを拡張したと説明しない。
- [ ] PV-001/002/010〜013/017/020/028/029の証拠誤昇格・適用条件を負例として固定する。

**受入:** 原稿一致と不可視の失敗が併存できる。unknown / 未実施を合格や非該当で埋めない。現行schema契約不変。

### W02 — Webレシピ（UPD-04/06/08）

**編集:** `skills/kumihan/references/web-recipes.md`、関連入口・リンク。**検証素材案:** `tests/fixtures/ja_v020/web/`。

- [ ] 「未対応CSSは無視されるから安全」を除き、構文対応・実font・実表示・fallbackを分離する。
- [ ] lang指定と実際の地域字形を分離。Pan-CJK名だけでja / zh-Hantの実字形を合格にしない。
- [ ] display基本例は通常字間とする。paltは実fontでの比較を伴う任意variant。本文への一括適用を避けるが、本文のpalt使用だけで自動失敗にしない。正のletter-spacingを「詰め」と説明しない。
- [ ] tabular-nums、禁則、spacing-trimを宣言だけで有効としない。過去のブラウザー実験を再実行したように書かない。
- [ ] reflowは実scroll軸、拡大は実施方式、spacingは言語runと適用特性を記録。日本語全体の除外やCSS模擬をnative text zoomと呼ぶ扱いを排除する。
- [ ] 16px、18px、30〜40字、0.875em等は用途付き開始値。固定の最小値・美的合格点にしない。

**受入:** 長いUIラベルの全文・操作を保持する対照fixture、通常/狭幅/実施できた拡大・上書きの実表示証拠。未実施方式を明記。

### W03 — 文書・スライドと改行（UPD-04/06/07）

**編集:** `skills/kumihan/references/document-recipes.md`、`docs/ja-type-011-prosodic-wrap.md`、4入口の古い011要約。

- [ ] Office東アジアフォント未設定を「最も多い原因」と断定しない。投影でゴシックが常に優れるという断定を実書体・字面・距離の比較へ置換する。
- [ ] 通常表示と意図的改行の必要性を先に確認する。「話すように」「文節で」「幅を広げる」を機械的な強制順序にしない。禁則002、不可分003、意味004、全行構成011を別に評価する。
- [ ] 本文字数・行送り・サイズを媒体条件付きの例とする。文長や漢字率を守るための原稿分割を行わない。
- [ ] 表全体・全行の無条件keepをやめ、短い行と1ページを超える行を区別。継続見出し、末尾セル、注記を保持する。
- [ ] 投影で18pt/24ptの指定だけを可読性の証明にしない。最小役割、投影寸法、最遠席が不明なら該当範囲をnot-checkedとする。
- [ ] PDF抽出一致と全頁描画・重なり・クリップ・読み順を分離する。PDF previewとnative Officeは別の結果にする。

**受入:** 修正前の誤断定を再導入する負例テスト、長い表と遮蔽の対照fixture。共通の資料生成機能は実装していないこと。

### W04 — 日本語知識を再利用可能にする（UPD-06/07/09）

**追加案:** references内 `japanese-writing-and-type.md`、`typography-recipes-by-task.md`、`research-claims.json`。必要な章だけ遅延参照しSKILL.mdを肥大化させない。

- [ ] 漢字・かなの成立、活字/写植/デジタル、文字列/字体/字形/font、OpenType・実font・fallbackの違いを、選定と原稿保全へ結び付ける。出典未確認の字源説明をロゴの「事実」にしない。
- [ ] 会話/告知/説明/ブランドコピーの違いを、文脈・目的・読者・編集可能性で説明。口語/文語とprose/displayは別軸。書き換え例には合成原稿を使い、実原稿の編集権限を拡張しない。
- [ ] copy-as-prose / display / hybridと情報探索・数値比較・操作等をつなぐ。見出しを必ず本文や大きなvalueより大きくする規則を作らない。
- [ ] サイズ・比率はauthoring値、resolved font、rendered字面、physical寸法、読者課題を分ける。報告書のWeb18px・UI16px・A4本文11.5pt/送り18pt・投影24ptは仮の比較開始案としてのみ扱う。
- [ ] claim-source台帳はsource ID/URL/版または日付/主張分類/適用対象/限界を持つ。研究の非有意を効果ゼロと呼ばず、選好と速度・正確さ・理解を混同しない。メーカーの主張を独立実験に数えない。

**受入:** 各知識が「どの判断に使うか」と「何を保証しないか」を持つ。出典不明の新しい数値断定ゼロ。

### W05 — 30ケースを実際のfixtureへ具体化（UPD-10）

**入力:** 同梱 `RESEARCH_CASES.md` と、アクセスできる場合は原本JSON。**追加案:** `tests/test_ja_v020_research.py`、`tests/fixtures/ja_v020/`、実装記録内 `case-results.json`。

- [ ] PV-001〜030を欠番なく登録し、元のexpectedと実際のobservedResultを別fieldにする。研究のgood/badは製品statusではない。
- [ ] 原稿は正確なコードポイント列を維持する。fixtureは合成・検証用であると明示する。
- [ ] contract回帰は30ケースのID/rule/scope/method/期待条件と禁止判定を検証する。これは30個の実環境試験成功ではない。
- [ ] 実描画で検証可能なWeb、文書preview、遮蔽、長い行・表、大小関係を実行し、実物の画像・環境・寸法を保存する。比較する良例/負例で原稿・条件を勝手に変えない。
- [ ] 意味・意図のassisted評価はテストの文字列マッチだけで代替しない。実行者が何を見て判断したかを短く記録する。
- [ ] ネイティブAIホスト、native Office、物理投影、サイン現場は実行できたものだけ結果を出す。環境非対応を確認した場合はunsupported、未着手はnot-checked。全体へ波及させない。

**受入:** 30件すべてに実行範囲・未実施理由が存在し、証拠なしのpassedがない。必須のP0修正が未完なら出荷候補完成としない。

### W06 — v0.2.0の配布候補と同期

**編集:** `plugin.json`、`.codex-plugin/plugin.json`、`.claude-plugin/plugin.json`、`gemini-extension.json`の日本語版versionと、対象の説明・更新履歴。

- [ ] 4 manifestsを選択的に0.2.0へ変更する。既存 `build_dist.py --set-version` はREADMEとdocs/*.mdを広く置換するため、そのまま使って歴史・公開済み表示を変えない。原則manifestの対象fieldと必要な現行説明だけを修正して通常buildを行う。
- [ ] `python tools/build_dist.py` で4 Skills共通データ・inventory・既存3ホスト計15 ZIP・manifest・checksumを再生成する。現行builderが削除する旧作業tree ZIPと、保持するimmutable Release資産を区別する。
- [ ] 未変更の他言語source ZIP・manifest・ライセンス、既存の公開Releaseを保持する。歴史的0.1.8の記録は変更しない。
- [ ] builderをもう一度実行しbyte再現性を照合。ZIP CRC、member path、版、inventory、size、SHA-256、アイコン、ライセンスを確認する。

**受入:** 日本語4 Skills/3ホストの候補が0.2.0で一致。旧schemaはそのまま。他言語差分ゼロ（共有表示の必須差分は明示）。

### W07 — サイト・導入・MCP引き継ぎ

- [ ] 既存 `kumihan.html`、日本語版を説明する英語ページ、導入ページの実入力・generatorをFresh Readし、変更点と候補/公開の状態を反映。サイトを変更する際は更新したKUMIHANでレビューする。
- [ ] `assets/edition-versions.json`のsource/published分離、`assets/edition-release-contracts.json`、既存version-automationを維持する。JA source=0.2.0でも公開は検証済みの版のままとする。
- [ ] generatorから作り直し、既存の他言語リンク・84件を含む復旧済みsource ZIPリンク・著作表示・未公開表示を壊さない。保護snapshotをテスト回避のために書き換えない。
- [ ] Universal側へ渡す `MCP_HANDOFF.md` を作成し、必要なJA入力差分・バージョン・39規則と集約規則数の違い・再生成/回帰確認事項を記載する。ライブMCPをv0.2.0と称さず、別管制で取り込むまで未反映とする。

**受入:** 未公開版を公開済みとする表示ゼロ。MCP本番変更ゼロ。サイト更新候補と将来の公開後同期手順が分離している。

### W08 — 全体回帰・独立した観点でのレビュー

最低限、対象baseで以下の存在・依存関係を確認して実行する。初回失敗と修正後結果は両方保持する。

```sh
python -m unittest discover -s tests -v
python tools/check_ja_type_011_cases.py
python tools/build_dist.py --check
python tools/build_seo.py --check
python tools/check_seo_preservation.py
git diff --check
```

`tools/sync_edition_versions.py`はネットワークで全Releaseを検証する。必要なら現行手順で同期し、その後 `tools/build_seo.py` と表示回帰を行う。API・資産取得失敗を無視して公開factを書き換えない。名前だけのPASSを作らない。

- [ ] レビューは原稿保全、schema互換、誤断定、証拠の誤昇格、配布整合、他言語非変更、公開状態の7点に絞る。
- [ ] 別レビュアーを利用できれば限定範囲で実行し、利用できなければself-reviewと正確に記録する。追加の厳格監査のために作業を無限停止しない。
- [ ] 既存失敗と今回導入した失敗を区別する。blockingを未解決のまま隠さず、必要なCIが未完ならその状態を維持する。

### W09 — Draft PR / Owner Gate / 再開情報

- [ ] 実装branchからmain向けDraft PRを作り、元の管制Issueへ結果を返す。既存の無関係PRはmerge・closeしない。
- [ ] 同記録dirへ `RESULT.md`、`baseline.json`、`case-results.json`、`release-manifest.json`、`MCP_HANDOFF.md`、`NEXT_GATE.md` を保存する。
- [ ] 最終報告に実際のHEAD/TREE、diff、実行コマンドと結果、30件の内訳、15 ZIPのsize/hash、他言語保持、残課題を記す。無関係な過去の緑CIを今回の証明に使わない。
- [ ] 次Gateは「候補の内容・CI・配布物をOwnerが確認してmerge/公開判断」。今回の依頼だけで既存の公開Gateを解除しない。公開後は新tag v0.2.0、資産照合、版情報の半自動patch、Pages読戻し、必要なMCP別管制連携を行う計画を残す。

## 5. 自律継続・停止条件

小さな不明点は保守的に扱い、根拠と判断を記録して次Workへ進む。具体的に停止するのは、他人の変更を消す必要、保護原稿変更、既存schema破壊、対象外サーバー変更、main/tag/公開等のOwner Gate越えが必要な箇所だけ。独立した安全なWorkは継続する。

Drive未接続、native未対応、無関係PRの失敗、root AGENTS不在を理由に全件未着手へ戻さない。発見した真のblockingと、製品の明示的限界を混同しない。

## 6. Review Focus

- 一致した文字列が図形の背面・clip外にあり、見えていないのにpassedになること。
- 正しい地域字形・OpenType効果をfont-family/CSS宣言だけから断定すること。
- 重要な大きな数値を「見出しより大きい」という理由だけで誤検出すること。
- バージョン更新がhistorical evidenceや他言語の版、公開済みmetadataを書き換えること。
- 共通資料生成・MCP本番改修を日本語版更新に紛れ込ませること。

各項目はW01/W02/W05/W06/W07の受入へ対応する。本書自体の配置時点では製品テストは未実行。
