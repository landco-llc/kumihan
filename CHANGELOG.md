# 更新履歴 / Changelog

[トップに戻る](README.md) ・ [更新ガイド](docs/updates.md)

<br>

## 0.1.0-preview.3

### 主な変更

- **より軽く、より速く**：スキルの説明文を約半分の長さに整理しました。社内テストでは、同じWebページを作るときの手数（ターン数）と時間が半分ほどになりました。
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

### 0.1.0-preview.3

- **Lighter and faster** — skill instructions are about half as long. In our tests, building the same web page took about half the turns and time.
- **Typography recipes** — two new references, one for web pages and one for reports and slides. They give recommended settings for each text role, such as body, headings and buttons.
- **Up-to-date browser support** — the web recipes now list browser support based on current information.
- **Clearer guides** — the README, installation guides and update guide were rewritten to follow step by step.

This release also includes the changes from 0.1.0-preview.2, which was available only briefly.

To update, see the table above or the [update guide](docs/updates.md).

### 0.1.0-preview.1

First preview.
