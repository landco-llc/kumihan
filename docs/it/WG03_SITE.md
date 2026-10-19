# WG03 — サイト3＋導入9＋言語ゲートウェイ（W07–W09）

Parent: [GOAL_EQUILIBRIO_V010.md](GOAL_EQUILIBRIO_V010.md)。WG02(15 ZIP)の完了証拠がない限り制作着手禁止。

## W07 完成Skillsの適用とcanonical design
- 実装された plugins/kumihan-equilibrio/skills/kumihan-equilibrio-web/SKILL.md と日本語版の skills/kumihan-web/SKILL.md、必要なrules/sources/referencesを実読してからDesign Contractを起草。docs/it/DESIGN_APPLICATION_RECEIPT.mdにSkill ID、rule IDs、読んだpath/commit、制作目的、読者、媒体、例外理由を記録。
- canonical構造: kumihan.html / _layouts/landing.html / tools/product_site.py の hero, intro-strip, features, idea-band, skills-section, install-section, status-section, cta-section。見出し・情報階層、余白、背景、色、CTA/カードサイズを統一し、Italian版固有の文章量へ最小限のCSSで対応。
- 生成CSSはcanonical_cssで継承（assets/equilibrio-site.css）。AI風の新規グラデーション・過剰なカードの積み重ね、イタリア語専用の固定デザイン観の輸入を避ける。アクセント文字、長い語、引用符、文字拡大、スマホ折返しを幅/構造で解決し、元文を削除しない。
- 3 pages: kumihan-it.html (lang=it)、kumihan-it.en.html (lang=en)、kumihan-it.ja.html (lang=ja)。canonical/hreflang it/en/ja/x-default、OG、favicon、viewport、公式icon、language switch、corporate footerは既存原本に準拠。
- イタリア語タイトル/コピーは文脈に自然で、ブランド理念に忠実な文章。見出し候補は「Il design in italiano, più naturale」。イタリア語の文体と母語校閲実施有無を記録する。

## W08 日英共通copy + 9 install
- tools/base_copy.pyで EDITIONS に it: (KUMIHAN｜Equilibrio, Equilibrio, イタリア語, Italian, 0.1.0)、COPY_FILES に it: equilibrio を追加。今mainの他言語追記を消さず、tools/base_copy.py --checkで JA/EN 共通項目を検証。イタリア語固有 feature 01、feature 03、版数と導入状況だけ独自値を持つ。
- 日本語 title: KUMIHAN｜Equilibrio — イタリア語のデザインをもっと自然に。英語 title: KUMIHAN｜Equilibrio — Natural Italian typography, made with AI。日英本文とセクションは共有辞書へ収束。例外は何が固有要件なのかをledgerへ明記。
- 3 host × 3 languages＝9 files:
  - docs/install-equilibrio-chatgpt.html / .en.html / .ja.html
  - docs/install-equilibrio-claude.html / .en.html / .ja.html
  - docs/install-equilibrio-gemini.html / .en.html / .ja.html
- 導入ページ構造は docs/install-chatgpt.html / _layouts/installation.html、tools/install_frame.py、assets/kumihan-install.css、assets/kumihan-install.js に合わせる。新規host-specificコマンドは公式根拠なしに発明しない。製品ディレクトリ、実ZIP名、正しい相対path、用途別の導入条件を説明する。
- 導入ページはパンくず、host切替、言語切替、h1、setup TOC、ダウンロード、インストール、更新、制限/注意、footerを持つ。リンク先はW05の現物と対応させ、release公開状態に一致する文言へW11で更新。
- 全サイトで人間向けplugin名は **KUMIHAN｜Equilibrio** だけ。ZIPファイル名にはversionを付ける。

## W09 Gateway + Browser
- tools/build_gateways.pyの元データ assets/gateway-copy.json にIT/Equilibrioを追加してgateway群を再生成。必要なら tools/web_fonts.py のlatin対象にitを追加。他言語のカードや翻訳に不用意に触れない。将来言語追加を想定したカードサイズの統一を維持する。
- generatorは tools/build_equilibrio_site.py 等で再現可能にし、--checkでは無変更/失敗検出。Site/guideの共通CSSやリンクを参照できるようにする。
- 12ページ、幅320/375/768/1280px、通常と200%の文字拡大、字間/行間オーバーライド、キーボードfocus、lang/alt/ARIA、言語切替、ダウンロードリンク、長語、アクセント、数値、fallback font、横はみ出し、読み順を確認。
- CSSのtext-wrap:balanceが意味的改行を保証する、と主張しない。hyphens:autoは利用辞書の確認をするまでは静的設定にとどめる。ブラウザ環境未実施はnot-checked。200% CSS simulationはnative zoomと混同しない。
- docs/it/DESIGN_APPLICATION_RECEIPT.mdにKUMIHAN適用事実、画像/画面キャプチャ、CSSの意図的差分、未確認環境を記録。日英/日本語本体および既存独立言語のレイアウト回帰を軽く試験。

Done gate: スキル先行のデザイン経路が証明され、3LP+9guide+IT gateway、日英copy・リンク・基本QAが一致。WG04へ。
