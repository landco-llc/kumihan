# WG04 — 軽量QA / main統合 / 公開 / 証跡（W10–W11）

Part of [GOAL_SATZBILD_V010.md](GOAL_SATZBILD_V010.md)
Prerequisite: WG01 core complete → WG02 15 ZIP verified → WG03 12 pages+gateway verified。未完のまま公開してはいけない。

## W10 — branch統合と軽量レビュー

- docs/de/EXECUTION_LEDGER.md と docs/de/DESIGN_APPLICATION_RECEIPT.md を最終更新する。実行したcommand・環境・結果・false positive例外・未検証範囲・source SHAを残す。
- 固定リリース候補で必要最小限のCI: Python versionと依存固定、ドイツ語rules/fixtures・4Skill closure、host manifestsの説明文/表示名/icon、15 ZIP builder --check / SHA verification、site generator --check、JA/EN共通copy整合、HTMLリンク、Jekyll生成、既存言語テスト、browser QA。
- CIが通るまで明確な不具合を修正。未検証の48研究ケースすべてを自動PASSに変換しない。デザインのAIっぽさを点数で宣言しない。
- 1回の独立軽量レビュー（Childまたは独立視点）で中核の新規変更に誤った外部参照、配布ZIP破損、既存言語汚染、虚偽公開リンクがないか確認。実施できなければ not-checked と理由。
- 他言語ファイル・既存プラグイン/ ZIP /リリースと比較し、許可した共通コピー・ゲートウェイへの最小変更以外に変更がないか確認。古いmaster listを上書きしない。並列PR変更は rebase/merge を正しく調停。
- feat/satzbild-v0.1.0 上の成果を PR にまとめる（既に同ブランチにPRがあるなら更新）。title例: feat(de): KUMIHAN｜Satzbild v0.1.0 — 4 skills, 15 ZIPs and DE/EN/JA site。
- GitHub/branch rulesが許可する場合、必要CI greenと軽量review後に main merge。ユーザーは本プロダクトのGitHub公開を承認済み。repoが実際に別途human required reviewを要求する場合は勝手に迂回しない。
- 最終main merge SHA を固定し、あとでtagやartifactの指すcommitを勝手にすげ替えない。

## W11 — 公開tag/Release/Pages

- tagは **kumihan-de-v0.1.0**。同名tag/Releaseの存在を確認し、別SHAに既存releaseがあるなら破壊的な上書きではなく衝突解決の事実を報告する。
- 公開対象17点：plugin/extension3 + skills12＝15ZIP、MANIFEST.json、SHA256SUMS.txt。ダウンロード、サイズ、SHA256が plugins/kumihan-satzbild/downloads/ に保管した固定候補と一致。
- .github/workflows/satzbild.yml（CI）、必要に応じて .github/workflows/publish-satzbild.yml（GitHub Actionsでの公開）を用意。既存publish-grafia/publish-hi方式を参考に、main SHA固定／tag一致／assets照合／追加後の公開確認を実装。release uploadを現在の環境から直接できない場合は GitHub Actions が最小権限で公開可能な経路。権限エラーはHOLDとして記録。
- 自動実装したworkflowの実Run URL、該当SHA、結果が揃うまで publish PASS としない。Releaseは draft=false、公開URLを実際にreadback。
- Pages上の3 landing:
  https://landco-llc.github.io/kumihan/kumihan-de.html
  https://landco-llc.github.io/kumihan/kumihan-de.en.html
  https://landco-llc.github.io/kumihan/kumihan-de.ja.html
- Pages上の9 guides は /docs/install-satzbild-{chatgpt,claude,gemini}[.en|.ja].html。12ページ・ホームのDEカード・言語切替の実HTTP到達を確認。
- Release assetsのリンクはGitHub tag / downloadsに統一。release公開済みのコピーとインストール案内が正確に一致することを確認。未公開段階のpreview/nonexistent linkのまま完了しない。
- ZIPハッシュとmanifest結果を公表。manifestの native-host-invocation と provider-store-listing は直接検証していない場合 not-checked/not-listed とする。GitHub Release公開をClaude/Geminiの公式Marketplace承認やChatGPT私用plugin登録に読み替えない。
- 最終result path: docs/de/RELEASE_RESULT_V010.md（W00-W11 ledger要約、SHA、PR URL、CI、tag、Release、Pages URLs、assets17、QA、not-checked、残件）。既存ファイルの不可避変更とその理由を明記。

## 完了判定

- **PUBLISHED_VERIFIED**：main merge、tag fixed、公開Release/readback assets17一致、Pages12・DE gatewayリンク確認、配布/実装の主要CIが成功。
- **IMPLEMENTED_NOT_PUBLISHED**：製品・ZIP・Webは実装済みだが、Release/Pages/CIの一部が未達。blockerとresume stepを明示。
- **PARTIAL / HOLD**：テスト失敗、別言語破壊リスク、GitHub権限/外部hostの不可逆条件など。完了と偽装せず、できた範囲でcommitを残し再開可能にする。

人間への成果報告はW11後に1回。情報が不足するたびに新規ZIP/MD添付や承認を要求しない。Owner承認範囲内の通常のGitHub公開は自律で進める。

**署名・有料security review・多段独立監査は要求しない**。代わりに配布整合・原稿保護・読みやすさ・虚偽の公開記述防止を軽量に確かめる。
