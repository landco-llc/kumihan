# KUMIHAN Universal — OpenAI公式プラグイン公開管制・引き継ぎ

- **文書種別:** 新規管制チャット／Codex Cloud・Codex App向け引き継ぎ・実行指示
- **作成日:** 2026-10-20（JST）
- **対象:** KUMIHAN Universal v0.1.0 / L&Co. LLC / OpenAI Platform 公開審査
- **管制状態:** `PUBLICATION_PRE_SUBMISSION_HOLD`（登録済み、未審査提出、未公開）
- **正本リポジトリ:** https://github.com/landco-llc/kumihan
- **実装Draft PR:** https://github.com/landco-llc/kumihan/pull/101 （`feat/universal-mcp-php-runtime`、観測時 HEAD `d3dff4eff590980e115d002b93bca4d51b20169f`、未マージ）
- **公式管理画面:** https://platform.openai.com/plugins
- **MCP接続先:** `https://mcp-kmhn.landco.co.jp/mcp`
- **元監査資料:** `KUMIHAN_Universal_OpenAI_Plugin_Guidelines_Gap_Audit_20261020.md`（この文書の論点を詳細に整理）

> **最優先の結論**
> 法人認証、プラグインZIP登録、MCP接続、ドメイン認証、4件のSkillパッケージ検査は完了している。最初からやり直さない。**残っている明示的なPlatformのブロッカーは利用規約URLの不足とレビュー情報の未完了**。これに加え、ホスト型MCPに未対応のプライバシー文面、未確認のMCPツール注釈、再現性ある品質証跡を整えてから審査提出する。

---

## 1. この管制チャットが扱う作業と扱わない作業

### 対象（IN SCOPE）

1. OpenAI公式Plugin Guidelines、MCPレビュー、Submission Requirementsへの適合。
2. 公式公開用の利用規約、プライバシーポリシー、サポート導線、説明文、公開メタデータの整備。
3. 4件のMCPツールの宣言・Annotations・エラー動作・読み取り専用性の検証と必要な限定修正案。
4. 審査用の正常系5件＋異常系3件、動画、Starter Prompts、Release Notes、審査情報の作成。
5. OpenAI Platform再スキャン、Findingsの読戻し、申請準備、Owner最終承認を受けた後の提出管制。
6. GitHub・Drive正本への記録更新。既存ZIP・Skill・MCP機能を保全する。

### 対象外（OUT OF SCOPE）

- **自動言語判定の実装修正と本番適用**：別の管制チャットの専管。ここでは不具合・依存関係・受入結果を追跡するのみ。実装を重複して行わない。
- 新言語追加、翻訳研究の拡張、文字組エンジンの全面改築、有料化、UI新設。
- 過去の法人認証・ドメインチャレンジの再実施。既に完了済み。
- 無承認の `main` マージ、本番MCP改変、審査提出、公開。

### 作業方式

- 調査・文書・静的サイト修正・MCPソース修正は**Codex Cloud / Codex App優先**。本管制チャットで実行仕様をMDとして作成・配置し、実行場所・ブランチ・読むべき正本・完了条件を記した起動文を返す。
- W00〜W06の**Work群を一連のGoalとして自律連続処理**する。ただし必要なOwner承認ゲートでは停止する。単発Workで毎回Ownerに確認しない。
- 本番ロリポップの変更は明示的な範囲指定・バックアップ・最小パッチ・ロールバック確認・Owner許可後だけ。
- 既存の無関係なサイト、MCPの非公開ディレクトリ、機密設定に手を触れない。

---

## 2. 引き継ぐ確定事実（重複作業禁止）

| 論点 | 状態 | 根拠・留意点 |
|---|---|---|
| Developer Identity | **L&Co. LLC 法人認証済み** | Ownerが「申請済みで許可済み」と明言。再申請不要 |
| Platform登録 | **KUMIHAN Universal / `kumihan-universal` / v0.1.0 Draft** | OpenAI Platformの接続中画面で確認済み |
| Developer / Category | **L&Co. LLC / Productivity** | Platform表示 |
| 公開状態 | **Not published** | Platform表示 |
| MCP設定 | **Configured / No authentication** | Platform表示 |
| ドメイン所有確認 | **Domain verified** | OpenAI Platform画面で認証済みと確認 |
| ドメインチャレンジ | **配置済み、HTTP 200、43 bytes一致** | ロリポップ公開フォルダ配下 `/.well-known/openai-apps-challenge` に配置、HTTPS検証成功。既存MCP実装・`.htaccess`は未変更 |
| MCPエンドポイント | **HTTPS実接続成功** | `https://mcp-kmhn.landco.co.jp/mcp`。21言語と4ツールの動作記録あり |
| MCPツール | **4件** | `kumihan_list_languages`, `kumihan_detect_language`, `kumihan_get_guidance`, `kumihan_review_text` |
| ZIP / Skills | **登録済み・4 SkillともChecks passed** | `kumihan-start`, `kumihan-web`, `kumihan-documents`, `kumihan-review`。これはパッケージ検査であり編集品質の証明ではない |
| 対応言語 | **21モジュール** | MCPの実呼出しで確認 |
| ルール総数 | **現ライブ応答の合計749** | 過去報告729と20差。合計の説明が整うまで公開コピーで固定件数を宣伝しない |
| モジュール検証状態 | **全件`preview_unverified`** | 登録＝現地言語品質検証完了ではない |
| 言語判定 | **既知バグあり** | `kumihan_detect_language("文字，排版。")` が現ライブで `ja` / `kana` を返す。別管制の修正待ち |
| 外部公開 | **審査未提出・ディレクトリ未公開** | 本文書時点。Platform管理画面の最新情報をFresh Readすること |

### 実際にPlatformに表示されたFindings

1. `Terms of service URL is required.`
2. `Incomplete review information`
3. MCP欄は確認時 `Scanning your MCP server`。スキャン**最終判定は未取得**。追加のblocking / warningsは後日必ず再読込する。

### 特に避けるべき巻き戻し

- GitHubの `universal/deployment/OPENAI_PUBLIC_PLUGIN_SUBMISSION_20261020.md` には**「ZIP未アップロード」「法人確認未証明」「ドメイン未認証」「Skill 1件」等の古い記述**がある。Platformの現在状態が優先。次のWorkで文書を更新する。
- 以前作成した `KUMIHAN_Universal_ChatGPT_Public_Submission_v0.1.0_DRAFT_r02.zip` は1 Skillベースの旧構成で、現在Platform上の**4 Skill構成と一致しない可能性**がある。**旧ZIPをそのまま再アップロードしない**。現登録リリースのアーカイブとSHA・Skill一覧を比較してから新バージョンを作る。
- 本番MCPを停止してドメイン認証をやり直す必要はない。OpenAI認証ファイルやドメイン設定も不要に変更しない。

---

## 3. 優先度A：審査提出前の不足・ブロッカー

| ID | 区分 | 現状 | 受入条件 | 主担当 |
|---|---|---|---|---|
| **A01** | **明示的Blocking / Terms** | PlatformにTerms URLがない | 法人承認済み利用規約をHTTPS公開、URLが200で取得可能、申請ZIP/Platformに一致、Finding解消 | Owner最終承認＋Codex |
| **A02** | **プライバシー整合性** | `privacy.html` は静的Skill中心の記載。「入力をL&Co. LLCに送らない」「MCP導入前に改定」は稼働サービスと矛盾 | 実際のデータ流通、運用者、ロリポップ上の保存・ログ、保持/削除、委託先、連絡先を事実ベースで英日正本に明記。全翻訳と文脈整合 | Owner事実確認・承認＋Codex |
| **A03** | **MCP Annotations** | PR #101の4 `addTool` に明示的な`readOnlyHint` / `openWorldHint` / `destructiveHint`がない | 各ツールの真の挙動を確認し3種の値と根拠を付与、限定デプロイ・Platform再スキャンで取得値を検証 | Codex / MCP担当 |
| **A04** | **Review情報** | `Incomplete review information` | 審査画面の必須欄を埋め、blocking 0。製品説明、テスト、注釈根拠、提供国、ポリシー等の実装との一致 | PMO＋Owner |
| **A05** | **デモ録画** | 公開で確認できるURL未記録 | 現行版で再現する代表例・ツール/Skill操作・制約を録画し、レビュアーが視聴可能なURLを設定 | Owner / 制作 |
| **A06** | **審査テスト** | 正常系5＋異常系3はドラフト段階。合否証跡は未確認 | 各ケース：プロンプト、条件、期待ツール、期待結果、観測結果、PASS/FAIL、再現手順を記録 | Codex / QA |
| **A07** | **既知ルーティング不具合** | 繁体中国語の句読点をKanaとして誤認。PR #101側の修正と現行ライブに差異 | 別管制からの本番修正・回帰PASS・ロールバック/証跡を受領。受領前に「自動判定修正済み」と言わない | **別管制** |
| **A08** | **公開品質の定義** | `review_text` はルール候補と`not_checked`を返し、実際のレンダリング判定・自動検証は行わない | スコープを「21言語の文字組参照ガイダンスと原稿を保持する保守的レビュー」に正確に限定。媒体/言語別の基本機能を検証し、完成済み自動監査と誇張しない | PMO / QA / Owner |

> 注：A01/A04は**Platform画面に実際に表示されたblocking**。A02/A03/A05〜A08は公式提出要件・コード観測・品質リスクに基づく公開前是正。すべてが既にPlatformのblocking欄へ表示されていると誤解しないこと。

### A02：サイト改定の運用条件

- 既存の `privacy.html` は英語・日本語を正本として、多言語版を**1つのHTML**内にまとめる設計。言語選択・アンカー・アコーディオンの構造を維持し、サイトデザインは既存KUMIHANに合わせる。
- ポリシーを実態のない宣言にしない。**PHPセッション保存、レンタルサーバーのアクセスログ、入力本文の取扱い・削除、送受信先**を調査してから文面を確定する。
- `LICENSE`（Apache-2.0）は**ソフトウェア利用許諾**であって、MCPホスティングサービスの利用規約の代用にはならない。
- 申請用利用規約は `terms.html` 等で英日2言語を最低限カバー。Termsの内容・責任制限等はOwnerが確認し、必要なら法務専門家レビュー。

### A03：注釈の候補（最終値は実挙動に依存）

現在の4ツールはユーザーの外部ファイルやアカウントを変更しない設計なので、候補は`readOnlyHint: true`、`openWorldHint: false`、`destructiveHint: false`。**無検証で全件に貼り付けない**。`FileSessionStore`がサーバー内部で書き込む点、ホストログ、外部ネットワークアクセス有無、MCP仕様のannotations意味論を照合する。Tool descriptionsや申請文言による説明はサーバーの実Annotationsの代替にはならない。

---

## 4. 優先度B：公開運用・品質の必要対策

| ID | 論点 | 対応 |
|---|---|---|
| B01 | 匿名MCPの濫用・負荷 | レート制限、WAF、最大入力、負荷上限、停止・復旧を設計。無料でも無制限運用はしない |
| B02 | データ保持・ログ | LiteSpeed/ロリポップアクセスログ、PHPセッションのTTL・削除、本文・IP等の保持とアクセス権を事実確認。保持ゼロを断言しない |
| B03 | エラー処理 | 未登録locale、`invalid-utf8`、入力長超過、Unsupported medium、WAF・MCP例外を試験。機密パスやトークンを返さない |
| B04 | ガイダンスの関連性 | `getGuidance`が現在rules配列の先頭最大25件を返すため、媒体・modeとの関連性を計測。必要最小限の改善のみ |
| B05 | 応答メタデータ | `entry_skill_path`、SHA、`source_file`等の利用者価値と開示リスクを整理 |
| B06 | 依存関係 | Composerの固定、パッケージ脆弱性調査、保守アップデートとリリース証跡 |
| B07 | 非公開サポート | GitHub Issuesは公開。個人情報・秘密情報を含む問い合わせの法人窓口を明記 |
| B08 | 正本同期 | PR #101の公開申請文書とPlatform現況を一致。版本・ZIPのダイジェストと検証限界を記録 |
| B09 | リリース後の更新 | Tool schema/annotationsの変更は再審査可能性を考慮。無審査の自動配信を前提としない |
| B10 | 多言語品質 | RTL（ar/fa）、複雑スクリプト（th/km/bn/hi）、中日判定、Latin系地域差、混在言語、原稿保全の回帰を計画 |

**明示的に不要:** 現在はCustom UI、UIスクリーンショット、OAuth、課金導線、不要な外部APIの導入は求めない。MCPだけのプラグインとして審査できるようにする。

---

## 5. Work群（自律進行とOwner Gate）

| Work | 処理 | 完了成果物 | 停止条件・ゲート |
|---|---|---|---|
| **W00: Fresh Read** | `main`/PR #101 HEAD、Platformドラフト、MCPライブ応答、法務ページ、既存4 Skillを読戻し。差分表作成 | `00_FRESH_READ_AND_BASELINE.md`、Evidence/未確認事項リスト | 現版を特定できなければ推測更新しない |
| **W01: Legal** | 実データ処理を確認、プライバシーポリシーMCP対応・利用規約・サポート説明を起案。既存HTML多言語構造維持 | `01_PRIVACY_TERMS_DRAFT.md`、レビュー可能なサイト差分、URL確認計画 | **Ownerが法務・データ処理の内容を承認するまで外部公開しない** |
| **W02: MCP Contract** | 4ツールのAnnotations/スキーマ/例外/セッションを検証し最小修正、CI・限定テスト。別管制の言語判定修正とは切り分け | `02_MCP_CONTRACT_QA.md`、差分、テスト、展開・復旧手順 | **本番パッチはOwnerの別承認後**。既知言語判定バグをこのWorkから修正しない |
| **W03: Functional QA** | 21言語の代表スモーク、レビューの実価値検証、正常系5＋異常系3の再現試験、別管制の言語判定修正を受入 | `03_REVIEW_TEST_CASES.md`、結果ログ・PASS/FAIL、未検証範囲 | 既知の誤判定がユーザーに誤案内する状態なら公開を止める |
| **W04: Submission Assets** | ローカライズ説明・版情報・Release notes・3件以内のStarter Prompts・動画脚本/録画・Annotation justificationを用意 | `04_SUBMISSION_PACKET.md`、デモ動画URL、審査向け説明 | 現行版で再現できない機能をデモしない |
| **W05: Platform Gate** | 現在登録済みのZIPを基準に修正版作成・検証、リリース整合確認、必要なら新バージョンをアップロード。MCP再スキャンとFindings読戻し | `05_PLATFORM_FINDINGS_AND_RELEASE_GATE.md`、ZIP SHA256、全必須項目、blocking 0の証拠 | **審査提出前にOwner承認**。無承認で`Submit for review`しない |
| **W06: Review / Launch** | OpenAIの審査提出後の質問・差戻し対応。承認後に公開範囲とリンクを検証 | `06_REVIEW_AND_PUBLICATION_RECORD.md`、審査結果、公開判断 | **OpenAI審査承認後も、Ownerが最終Publishを決定** |

### 並行処理の方針

- W01（法務）とW02（MCPアノテーション）は独立して着手可能。W03 QAの多くも先行できる。
- ただしW03の**言語判定最終PASS**は別管制の修正受領後に確定。
- W04のドラフト制作は並行できるが、最後の録画とW05は**最終版の実際の挙動**に揃える。
- B項目は公開リスクに直結するB01/B02/B03/B07を優先。他は実害と必要工数で判断する。監査のための過剰実装をしない。

### 必須Owner判断

1. **法務・プライバシー事実確認と公開文面**：個人情報とログ取扱い、利用規約、責任分界。
2. **MCPの本番変更許可**：固定対象・差分・バックアップ・ロールバックを提示した後。
3. **提出Go/No-Go**：blocking 0、5+3実測、4 Skill / 4ツール・21言語の保全、動画、既知バグの扱い。
4. **一般公開許可**：OpenAI審査の合格を確認した後。

---

## 6. 更新すべき正本

### GitHub

- `universal/deployment/OPENAI_PUBLIC_PLUGIN_SUBMISSION_20261020.md` — 現在の法人認証済み/ZIP登録済み/4 Skill/Domain verified/Findingsへ更新。
- `universal/deployment/target.json` — MCP公開/運用状態を実測証拠に基づき更新（credential、challenge token、絶対サーバーパスは入れない）。
- `universal/server/public/index.php` — 必要と確認されたTool Annotations/登録情報の限定ソース修正。展開は別ゲート。
- `privacy.html` — 英日正本＋多言語翻訳を含む1ページ構造でMCP実態反映。`privacy-ja.html`の互換導線を壊さない。
- 新規 `terms.html` 等 — 公式利用規約。サイト内の導線・SEO・アクセシビリティと同期。
- `universal/deployment/` — Work群の監査証跡・成果物・バージョン情報・スキャン結果を格納。
- 既存の `HANDOFF_LANGUAGE_ROUTER_OTHER_CONTROL_CHAT.md` — 自動言語判定は別管制で、ここでは結果参照のみ。

### Google Drive / KUMIHANプロジェクト

- 既設 `kumihan` プロジェクト正本フォルダ（https://drive.google.com/drive/folders/1GEf3aojPe9kpamsPsjl0B2eH3OwOINBP）へ、最新の運用決定／申請証跡／Owner判断結果を整理。具体的配置先は既存フォルダ構成をFresh Readして決定。
- **この引き継ぎMDの出力自体はGitHub/Driveへの保存を意味しない**。配置/更新は実行後に明示的に報告。

---

## 7. 公開申請Go / No-Go判定表

以下が全て真になるまで`Submit for review`を押さない。

- [ ] L&Co. LLCのドラフトが現行ZIP/Versionで識別され、4 Skillの`Checks passed`が維持されている。
- [ ] 4つのMCPツールがScan Toolsで正常取得・安全性注釈が正確である。
- [ ] `Domain verified`が維持されている。
- [ ] Terms of Serviceが公開HTTPS 200で、PlatformのURL必須Findingが解消している。
- [ ] Privacy Policyがホスト型MCPの実運用と一致し、Owner承認済み。
- [ ] 無認証公開MCPの濫用対策・保持ポリシー・サポート導線に運用責任者が同意している。
- [ ] 5件の正常系・3件の異常系で実測と再現手順が完成している。
- [ ] 審査員がアクセスできる現行版のデモ動画URLがある。
- [ ] 21言語の代表的な挙動が検証され、誤判定を放置したままの過大な品質保証がない。
- [ ] Starter prompts / Release notes / 全世界無料公開の設定・申請内容が現行の機能と一致する。
- [ ] 最終`Blocking Findings = 0`。未確認項目をPASSに置き換えていない。
- [ ] Ownerが提出を明示承認した。

公開（Publish）は**別ゲート**：OpenAI審査承認＋Owner公開承認後に実行する。

---

## 8. 新しい管制チャットへの起動文（そのまま貼り付け可）

> 添付の `KUMIHAN_Universal_OpenAI_Publication_Control_Handoff_20261020.md` を制御文書として読んで、OpenAI公式KUMIHAN Universal公開申請管制を再開する。最初にGitHub `landco-llc/kumihan` のmain、Draft PR #101、`universal/deployment/`、OpenAI Platform現行ドラフト、公開MCP・サイトをFresh Readし、既済・未完・ブロッカーを照合する。W00〜W06を一連のWork群としてCodex Cloud/App優先で自律推進し、必要な指示MDを正本に配置したら実行環境・ブランチ・指示場所・起動文を提示する。法人確認、ドメイン検証、ZIP登録、4件のSkill検査をやり直さない。自動言語判定修正は別管制に留保。法務公開・本番MCP変更・審査提出・一般公開は各Owner Gateを厳守する。各Workの結果は証拠URL、commit/PR、実測PASS/FAIL、未確認、次アクションをまとめて報告する。

---

## 9. 参照リンク

- OpenAI Guidelines（移転先として確認）: https://developers.openai.com/plugins/app-guidelines
- ユーザー指定の元URL: https://developers.openai.com/plugins/plugin-guidelines （確認時404）
- Submission: https://developers.openai.com/plugins/deploy/submission
- Submission errors: https://developers.openai.com/plugins/deploy/submission-errors
- MCP review requirements: https://developers.openai.com/plugins/deploy/app-review
- Security & Privacy: https://developers.openai.com/plugins/guides/security-privacy
- GitHub正本: https://github.com/landco-llc/kumihan
- Draft PR #101: https://github.com/landco-llc/kumihan/pull/101
- KUMIHANサイト: https://landco-llc.github.io/kumihan/
- 現プライバシーポリシー: https://landco-llc.github.io/kumihan/privacy.html
- 法人サイト: https://landco.co.jp/
- プラグイン管理: https://platform.openai.com/plugins

## 10. 観測限界・取り扱い

- この文書は**OpenAIによる審査結果ではなく、公開前の内部管制資料**。
- Platformの最新スキャン完了結果や審査情報フォームの全項目、実登録ZIPバイト列・ハッシュ、サーバーログの運用設定、他クライアントの全互換性はまだ独立に確認していない。
- 本番MCP `kumihan_list_languages` は21言語 / 749件を返したが、各モジュール`preview_unverified`。宣伝・監査で「言語別の文字組自動品質監査済み」と扱わない。
- チャレンジトークン・ホスティング契約アカウントの絶対パス・秘密設定・顧客入力全文は、このMDや公開Issue/PRへ複写しない。
- PR #101本文や一部ドキュメントは、現在の稼働MCPに関する古い状態を含む。**新しい管制チャットは現実のPlatform/ライブMCPと最新Gitを優先して差分記録すること**。
