# KUMIHAN [クミハン]

**日本語の文字組みから、AIのデザインをもっと自然に。**  
**Japanese typography for thoughtful AI-assisted design.**

<br>

## KUMIHANとは

KUMIHANは、AIが日本語のWebサイト・記事・報告書・プレゼンテーション資料をつくるときや見直すときに使う、オープンソースのスキル集です。

日本語の改行や禁則、句読点・括弧の扱い、和文と欧文の混ざり方、文字と余白のバランスを大切にしています。

決まりきったテンプレートに当てはめるのではなく、**内容と目的にふさわしい、読みやすく伝わりやすいデザイン**を目指します。

<br>

## できること

| | |
| --- | --- |
| **読みやすい文字組み** | 改行位置、字間・行間、書体の選び方を、日本語に合わせて整えます。 |
| **内容に合ったデザイン** | 伝えたい情報の順番や重要度から、構成とレイアウトを考えます。 |
| **原稿を大切に** | 名前、価格、数値、元の文章を勝手に書き換えません。 |
| **制作後の見直し** | ファイルを変更せずにレビューし、気になる点を一覧で返します。 |

<br>

## 4つのスキル

| スキル | 使う場面 |
| --- | --- |
| `kumihan` | 最初の入口。何をつくるか（Web・報告書・スライドなど）と、作業の範囲を整理します。 |
| `kumihan-web` | Webページ、記事、LP、アプリ画面の制作・調整。 |
| `kumihan-documents` | 報告書やプレゼンテーション資料の制作・調整。 |
| `kumihan-review` | できあがったものを、変更せずにレビューします。 |

<br>

## 導入方法

お使いのAIツールに合わせてガイドを選んでください。

| 利用するツール | 日本語 | English |
| --- | --- | --- |
| Claude（Claude Code / Claudeチャット） | [導入ガイド](docs/installation.claude.ja.md) | [Guide](docs/installation.claude.md) |
| ChatGPT / Codex | [導入ガイド](docs/installation.ja.md) | [Guide](docs/installation.md) |
| Gemini（Gemini CLI / Geminiアプリ） | [導入ガイド](docs/installation.gemini.ja.md) | [Guide](docs/installation.gemini.md) |

更新の方法は [更新ガイド](docs/updates.md)、変更内容は [更新履歴](CHANGELOG.md)、全言語で共通の版名は [バージョン表記規約](docs/versioning.md) にまとめています。

<br>

## 用途に合わせたデザイン支援（v0.1.8）

文字組だけでなく、目的に応じた情報階層、文字と図像の関係、ブランドの一貫性、AIにありがちな定型レイアウトの見直しを支援します。**自動選択を標準・手動指定で上書き可能・重要な曖昧さだけ質問**の用途別アダプターを追加しました。媒体プロファイルは従来の6種類のまま。通常のデザインレビューはStandard、Strictはユーザーの明示指定が必要です。

この機能は画像生成エンジンや自動デザイン品質判定器ではありません。ユーザーの原稿と権限を保護し、観察した結果と未検査を区別します。詳細は[用途ルーティング](skills/kumihan/references/use-case-selection.md)と[レビュー方式](skills/kumihan/references/design-review-modes.md)をご参照ください。

<br>

## 開発状況

現在も段階的に改善を続けています。

**最新の公開版はv0.1.8（2026年10月19日公開）です。** [GitHub Release・15 ZIPをダウンロード](https://github.com/landco-llc/kumihan/releases/tag/v0.1.8)。用途別アダプターとStandard／Strictデザインレビューのガイドを追加しました。各AIホストでのネイティブ動作や実画像・Officeでの検証範囲には制限があります。

<br>

---

## About KUMIHAN

KUMIHAN is an open-source set of skills that helps AI create and review Japanese websites, articles, reports and presentations.

It focuses on natural line breaks, punctuation and spacing, mixed Japanese and Latin text, and a good balance of type and white space. Rather than relying on repetitive templates, it encourages layouts that suit the content and its purpose.

### What it helps with

- **Better Japanese typography** — line breaks, spacing and type choices suited to Japanese text.
- **Purposeful design** — structure and layout based on what needs to be communicated.
- **Content integrity** — names, prices, numbers and original wording stay as supplied.
- **Practical review** — read-only reviews that list issues without changing your files.

### Installation

- Claude: [Guide](docs/installation.claude.md)
- ChatGPT / Codex: [Guide](docs/installation.md)
- Gemini: [Guide](docs/installation.gemini.md)
- Updates: [Update guide](docs/updates.md) · [Changelog](CHANGELOG.md) · [Version policy](docs/versioning.md)

### Status

KUMIHAN continues to be improved, with scope-limited verification. **The latest published release is v0.1.8 (October 19, 2026).** [Download the published release and its 15 ZIP archives](https://github.com/landco-llc/kumihan/releases/tag/v0.1.8). This version adds conservative use-case routing and Standard/Strict design-review guidance. Native AI-host behavior and real rendering across tools remain only partially verified.

<br>

## License / ライセンス

[Apache License 2.0](LICENSE)

Developed by L&Co. LLC.

## Korean edition / 한국어판

[KUMIHAN｜글짜임 v0.1.0](https://landco-llc.github.io/kumihan/kumihan-ko.html) is an independently packaged Korean guidance product. [Source and four standalone Skills](plugins/kumihan-geuljjaim/README.md) · [Korean release](https://github.com/landco-llc/kumihan/releases/tag/kumihan-ko-v0.1.0). Japanese KUMIHAN and 字衡 are not prerequisites.

## French edition / Édition française

**[KUMIHAN｜Accord v0.1.1](kumihan-fr.html)** — French typography using selected editorial conventions with source preservation and read-only review. [Source and install packages](plugins/kumihan-accord/README.md) · [GitHub Release](https://github.com/landco-llc/kumihan/releases/tag/kumihan-fr-v0.1.1). Skill and plugin descriptions: Español / English.


## Russian edition / Русская версия

**[KUMIHAN｜Лад v0.1.0](kumihan-ru.html)** — natural Russian/Cyrillic typography with source protection and content-led design. [Four Skills and source](plugins/kumihan-lad/README.md) · [GitHub Release](https://github.com/landco-llc/kumihan/releases/tag/kumihan-ru-v0.1.0).
