# 更新履歴 / Changelog

[トップに戻る](README.md) ・ [更新ガイド](docs/updates.md)

<br>

## 0.1.0-preview.4

### 主な変更

- **レビューの記録を確実に**：レビュー前後のハッシュ値を、報告書に必ず書くようにしました。対象のファイルを変更していないことを、報告書だけで確かめられます。
- **PDF用の設定を補足**：本文全体で文字単位の折り返しを有効にしないよう、報告書・スライド用のパターン集に注意書きを加えました。

### 旧版との比較テスト

同じ原稿を使い、最初のプレビュー版（0.1.0-preview.1）と、今回の内容の版を比べました。対象は5つの場面です。

| 場面 | 手数（ターン） | 費用 | 時間 |
| --- | --- | --- | --- |
| LP（ランディングページ） | 10 → 5 | 0.42 → 0.17ドル | 84 → 38秒 |
| 読みもの記事 | 9 → 5 | 0.25 → 0.16ドル | 58 → 29秒 |
| A4報告書 | 10 → 7 | 0.27 → 0.19ドル | 52 → 39秒 |
| スライド | 20 → 6 | 0.40 → 0.18ドル | 103 → 42秒 |
| レビュー | 21 → 14 | 0.56 → 0.40ドル | 133 → 71秒 |
| **合計** | **70 → 37** | **1.90 → 1.10ドル** | **430 → 219秒** |

- 両方の版とも、原稿の文言・数字・表の値・発表者ノートはすべて保たれました。また、320px幅での横はみ出しはありませんでした。
- レビューの場面では、わざと仕込んだ問題7件（価格の誤り、根拠のない実績表示、全体への字詰め指定など）を、両方の版とも7件すべて見つけました。
- 新しい版は、パターン集の設定（文節での改行、見出しの行長をそろえる指定など）を使っていました。
- 各場面1回ずつの結果です。参考値としてご覧ください。

<br>

## 0.1.0-preview.3

### 主な変更

- **より軽く、より速く**：スキルの説明文を約半分の長さに整理しました。
- **組版の実装パターン集を追加**：Webページ用と、報告書・スライド用の2つです。本文・見出し・ボタンなど、文字の役割ごとに推奨設定をまとめました。
- **Webパターン集の対応ブラウザを最新化**：各設定の対応ブラウザを、最新の情報にもとづいて更新しました。
- **導入ガイドを読みやすく**：README、導入ガイド、更新ガイドを、手順に沿って読める構成に書き直しました。

短期間だけ公開していた 0.1.0-preview.2 の変更も、この版に含まれています。

### 更新のしかた

| 導入した方法 | 更新のしかた |
| --- | --- |
| Claude Code（GitHubから導入） | `claude plugin marketplace update kumihan-marketplace` のあと `claude plugin update kumihan@kumihan-marketplace` |
| Codex（マーケットプレイスから導入） | `codex plugin marketplace upgrade kumihan-git` |
| Gemini CLI（拡張機能） | `gemini extensions update kumihan` |
| ZIPをアップロード・展開して導入 | 新しいZIPをダウンロードして入れ替え |

詳しくは [更新ガイド](docs/updates.md) をご覧ください。

<br>

## 0.1.0-preview.1

最初のプレビュー版です。

<br>

---

## English

### 0.1.0-preview.4

- Reviews now always record the target's hash before and after, so the report alone shows the file was not changed.
- The document recipes now warn against character-level wrapping on the whole body in HTML-to-PDF output.
- Comparison test against 0.1.0-preview.1, using the same inputs in five scenarios (landing page, article, A4 report, slides, review): total turns 70 → 37, cost $1.90 → $1.10, time 430 → 219 seconds. Both versions kept all supplied text, numbers, table values and speaker notes intact, and both found all seven planted issues in the review test. Each scenario was run once, so treat these numbers as indicative.

### 0.1.0-preview.3

- **Lighter and faster** — skill instructions are about half as long.
- **Typography recipes** — two new references, one for web pages and one for reports and slides. They give recommended settings for each text role, such as body, headings and buttons.
- **Up-to-date browser support** — the web recipes now list browser support based on current information.
- **Clearer guides** — the README, installation guides and update guide were rewritten to follow step by step.

This release also includes the changes from 0.1.0-preview.2, which was available only briefly.

To update, see the table above or the [update guide](docs/updates.md).

### 0.1.0-preview.1

First preview.
