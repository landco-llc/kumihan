# WG04 — CI / Release / Pages 公開（W10–W11）

Parent: [GOAL_EQUILIBRIO_V010.md](GOAL_EQUILIBRIO_V010.md)。WG01→WG02→WG03の完了が前提。公開はOwnerが本チャットで承認済み。

## W10 Lightweight review, merge
- 必要最小限の機能回帰/構文/配布SHA/サイト生成--check/固定copy/HTMLリンク/Jekyll/ブラウザを実行。GitHub Actionsに .github/workflows/equilibrio.yml 等のfocused CIを追加。既存共通CIを壊さない。
- 既存他言語製品とそのZIPを変更しない。許される共通差分は tools/base_copy.py, tools/build_gateways.py, assets/gateway-copy.json, fontsの該当言語追加, generatorに必要な範囲だけ。並行PR #76などの最新状態をfresh readし、コンフリクトを正しく解消。
- 文字/数値/引用/コードを壊す誤修正、15 ZIPの参照閉包不備、ユーザー向け名称不一致、言語切替失敗、公開リンク偽装を重要blockerとして修正。それ以外の厳格なセキュリティ監査/多段独立承認は不要。
- docs/it/EXECUTION_LEDGER.md と DESIGN_APPLICATION_RECEIPT.mdに作業実施・環境・Status・tests・未確認事項を記載。研究48件すべて自動PASSと書かない。
- feat/equilibrio-v0.1.0 の実装PRを作る。同名PR/branchがある場合は上書きせず継続・照合。CI greenになったらrepository rulesを守ってmainへmerge。要求されるhuman reviewがあるなら強行しない。

## W11 Tag / public release / GitHub Pages
- public tag: kumihan-it-v0.1.0。既存同名Tag/Releaseの有無を確認し、immutableのまま扱う。別SHAへの強制付け替えは禁止。
- 17 release assets: 15 ZIP + MANIFEST.json + SHA256SUMS.txt。GitHub Actions publish workflowを使う場合は GitHub token最小権限、tag==固定main SHAを検証し、まずdraftでasset完全一致を確認、問題なければdraft=falseに変更。runログとサイズ/hash readbackを残す。
- Site: https://landco-llc.github.io/kumihan/kumihan-it.html / .en.html / .ja.html。Guide: https://landco-llc.github.io/kumihan/docs/install-equilibrio-{chatgpt,claude,gemini}[.en|.ja].html 計9件。実HTTP 200とcontent一致、canonical/hreflang、内部導線、gateway ITカードとそのクリック、公式icon/CSS取得を公開環境で確認。
- RELEASE_NOTESにはItaly v0.1.0、対応範囲、IT/EN descriptions、無料オープンソース、研究候補40/48の非完全自動対応、native providerの未確認事項を明記。ChatGPT/Claude/Geminiの公式ストア登録は行わない。
- docs/it/RELEASE_RESULT_V010.md を作り、main SHA、PR、CI、tag、公開Release（draft=false）、assets17 SHA/サイズ、公開Pages12、gateway、原稿保護/重点tests・未確認事項・他言語差分を列記。公開済みを主張するのはreadback証拠が揃った場合のみ。

## 最終status
- PUBLISHED_VERIFIED: merged main + immutable tag + public Release/17 assets hashes readback + Pages12/gateway HTTP確認＋重要CI green。
- IMPLEMENTED_NOT_PUBLISHED: 製品・ZIP・Web実装済みで権限/CI/公開条件のみ不達。
- PARTIAL/HOLD: 技術的障害、重要テスト失敗、別言語破壊リスク、公開権限不足など。作業済みの現物と再開起動点をledgerへ残す。
