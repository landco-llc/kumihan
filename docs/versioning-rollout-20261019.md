# KUMIHAN 版名無接尾辞化 — 実装・検証記録（2026-10-19）

**Owner指示：** 「v0.1.8-previewではなく、v0.1.8とpreview表記を無くそう。これは全言語版で統一する。」
**対応範囲：** バージョン命名と整合するmanifest・配布ZIP・公式サイト／導入ガイド・チェックサム・CI受入テスト。**機能追加や別言語のバージョン番号同期ではない。**

## 採用した恒久規約

- ユーザー向け表示 `vMAJOR.MINOR.PATCH`、現行の正本 `plugin.json` は `MAJOR.MINOR.PATCH`。
- 日本語タグは `v0.1.8`。言語版は既存の言語slugを保って `kumihan-<slug>-v0.1.0` 等を使用。
- ZIPはプラットフォーム別・言語別の既存命名パターンを維持しつつ、`-preview` を除外する。ユーザー向けプラグイン表示名へバージョンを付けない。
- **21個の現行製品**の独立版数は維持し、共通テストで現行manifestの無接尾辞形式を検証。
- 過去に公開した`*-preview` Releaseとタグは移動・削除・上書きしない。旧い検証記録は当時の名称をそのまま参照してよい。
- suffixがなくてもネイティブHost互換・実描画や印刷保証にはならない。未実証事項は今後も明示する。
- SEO PR#93、MCP PR#101等の並行PRは今回の変更に含めない。

## 実装結果

| 項目 | 変更 |
|---|---|
| 日本語 KUMIHAN | 正本4つのmanifest `0.1.8-preview → 0.1.8`、配布15 ZIPと3 MANIFEST・SHA256SUMSを再生成。README、更新履歴・ガイド、サイトの版表示／Releaseリンクを修正 |
| KUMIHAN｜字衡 | `0.1.0-preview → 0.1.0`。正本・言語別3 LP・9導入ページ・6原文ガイド・3系統の15 ZIPと全チェックサムを一致させた |
| その他言語版 | 既存`0.1.0`、`0.1.1` 等を維持。実装・配布ZIP・既存Releaseを変更しない |
| 横断規約 | `docs/versioning.md`に採用規約を明文化。現在の21製品を検査する`tests/test_version_naming.py`を追加 |
| 更新コマンド | 日本語と字衡のbuilderが、新たな接尾辞付きバージョン指定を拒否するよう改訂 |

## 検証済み（変更ブランチの実測）

- 日本語 `python3 -m unittest discover -s tests -q`：**65件PASS**。
- 字衡 `python3 -m unittest discover -s tests/ziheng -q`：**26件PASS**。
- `tools/build_dist.py --check`：**148件の生成物一致**。
- `tools/build_ziheng.py --check`：**110件の生成物一致**。
- `tools/build_ziheng_hosts.py --check`：**18件の生成物一致**。
- `tools/build_ziheng_site.py --check`：**4件一致**。
- 日本語15 ZIP + 字衡15 ZIP、計**30 ZIP**：サイズ、SHA256、ZIP整合・配布MANIFESTを確認。
- 字衡Web/導入ページ内の69件のraw ZIP参照：ローカル対応パスで**欠落0**。新しいClaude/GeminiフルパッケージSHA256を6サイト・6原文ガイドに反映。
- 現行21製品のcanonical manifestはsuffixなし。履歴として残した古い証跡ファイルと過去Releaseタグは変更していない。
- 未実施／未主張：日本語・字衡の全ネイティブHost実呼出、全サイト実ブラウザ多環境、Office/印刷実物、言語別現行Releaseの一斉再公開。

## 公開とバージョンの境界

日本語の`v0.1.8-preview`は既存公開済みの不変履歴で、改名・削除しない。現行コードに準拠した新しい日本語`v0.1.8`のタグ／Releaseは、対象PRのCI確認とコミット固定後に**別の新規公開記録**として扱う。Zihengの名称統一は現行ソース・配布ZIP名の更新であり、それだけでは未公開の独立Marketplace登録／GitHub Releaseの初回公開を意味しない。

## 正本

- GitHub: https://github.com/landco-llc/kumihan
- 決定記録: KUMIHAN Drive `00_CONTROL/KUMIHAN_01_DECISION_LOG`
- 規約: `docs/versioning.md`
- 既存日本語 Release（履歴）: https://github.com/landco-llc/kumihan/releases/tag/v0.1.8-preview

検証記録は実際に実行したコマンドと結果の範囲を超えて合格を主張しない。
