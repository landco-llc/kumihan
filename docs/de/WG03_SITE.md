# WG03 — Satzbild サイト・3言語と9導入ガイド（W07–W09）

Part of [GOAL_SATZBILD_V010.md](GOAL_SATZBILD_V010.md)
Prerequisite: WG02 complete。4 Skills、3 Host plugin/extension、15 ZIP、manifest digest の現物が検証されるまで **Web制作開始は禁止**。

## W07 — 完成したSatzbild Web Skillを適用してサイト設計

サイト制作の前に、完成した plugins/kumihan-satzbild/skills/kumihan-satzbild-web/SKILL.md と原本日本語の skills/kumihan-web/SKILL.md を実ファイルから読んで採用ルールを確認する。合わせて design contract（目的、読者、情報順序、書体選択、余白、視線、採用しない定型、例外理由）を docs/de/DESIGN_APPLICATION_RECEIPT.md に記録する。

- 正本は **kumihan.html** と **_layouts/landing.html**。ページの構造は hero、intro-strip、features、idea-band、skills-section、install-section、status-section、cta-section の8要素を tools/product_site.py に沿って再利用。
- CSSは _layouts/landing.html 由来を tools/product_site.py の canonical_css で導出、追加オーバーライドはドイツ語長語、字形、レスポンシブ、配列差だけ。不要なAI風グラデーション・独立カード群・カラースキームの持ち込みを避ける。
- 追加する主ページ：kumihan-de.html / kumihan-de.en.html / kumihan-de.ja.html（同じ構成/同じ主旨）。ドイツ語 lang=de、英語 en、日本語 ja。
- 上記3ページ間に正確な canonical、hreflang de / en / ja、x-default、OG/Twitterメタ（既存流儀）、公式favicon、モバイルviewport、footer L&Co. LLCの公式corporateサイト別タブリンクを設定。
- German body: 不必要に長い複合語をletter spacingやbreak-allで切らない。高さ固定のUIでは多行許容、ソースの長語と引用符は保護、必要に応じて狭幅のlayout-first対応。
- 既存日本語版の主デザインを標準とする。ドイツ語圏風の装飾として勝手にBauhaus/Swiss gridを押し付けない。使用書体はKUMIHAN固定セットを定めず利用可能/許諾済みの環境から選ぶ。

### 3言語のタイトル／コピー方針

**日本語・英語の理念と共通見出しは tools/base_copy.py の JA/EN辞書を正本として使うこと**。実行時点で最新版を読み、EDITIONSとCOPY_FILESへ de を追加し、ドイツ語版 assets/satzbild-site-copy.json の ja/en 共通キーを共有辞書から生成する。対象言語と製品名のみ置換。以下は源に合うべき指標であり、手作業の異文を正本にしてはいけない。

- 日本語<title>: KUMIHAN｜Satzbild — ドイツ語のデザインをもっと自然に
- English<title>: KUMIHAN｜Satzbild — Natural German typography, made with AI
- Deutsch<title>候補: KUMIHAN｜Satzbild — Deutsche Typografie, natürlich gestaltet
- 日本語リード: AIとつくるドイツ語のWebサイト、記事、報告書、プレゼンテーション。読みやすさも、伝わりやすさも、内容を大切にすることも。KUMIHAN｜Satzbildは、ドイツ語のための制作・レビュースキル集です。
- English lead: KUMIHAN｜Satzbild is a set of open-source AI skills for creating and reviewing German websites, articles, reports, and presentations—with care for readability, layout, and the integrity of your original content.
- Deutsch lead候補: KUMIHAN｜Satzbild ist eine Sammlung quelloffener KI-Skills für die Gestaltung und Prüfung deutschsprachiger Websites, Artikel, Berichte und Präsentationen. Sie achtet auf Lesbarkeit, passende Typografie und den unveränderten Originaltext.
- ドイツ語だけに特有の feature 01、文体・地域、導入・version statusは別キーで管理。DE/AT/CHの地域差は説明しても実証していない適合宣言はしない。
- DE copyは読みやすい標準ドイツ語を基本とする。Native reviewがない場合は not-checked を記録。スペリングや口調で2024正書法とハウススタイルを混同しない。

## W08 — 各AIホストの3言語導入ページ9本

- docs/install-satzbild-chatgpt.html / .en.html / .ja.html
- docs/install-satzbild-claude.html / .en.html / .ja.html
- docs/install-satzbild-gemini.html / .en.html / .ja.html

上記3ホスト×3言語、合計9本。既存 **docs/install-chatgpt.html** と **_layouts/installation.html** の情報構造を守り、共有 **tools/install_frame.py** と **assets/kumihan-install.css / .js** を使う。独自に異なるUIや導入構造を作らない。

- 各guideの上部にブランド、該当ホストリンク、de/en/ja切替、breadcrumb、ヒーロー、手順TOC、ダウンロード/導入方法、更新方法、必要なら注意事項を置く。
- 実在する4 skills + 3ホストpackagingから導入対象、ZIPの実ファイル名、解凍先と相対PATH、技術的name、サンプル起動文を組む。存在しないコマンドやホストAPIを記載しない。
- すべてのリンクは作成済みZIPかGitHub Release assetsを参照。発行後に実URLへ修正し、「publish予定」と「公開済み」を混ぜない。
- 各ページのtitle/descriptionとユーザー向けのプラグイン名は KUMIHAN｜Satzbild に統一し、lang/hreflang/alt/aria-label を適切に設定。
- 既存の日本語ページ構成、背景色、ヘッダー、CTA、余白、ボタン、文字階層は保持。ユーザークライアント固有のinstall UIを捏造しない。

## W09 — ゲートウェイとWebの実表示確認

- tools/build_gateways.py で DE/Satzbildカードを追加。必要な assets/gateway-copy.json の ja,en,ko,th,zh などの共有言語別カード説明・導線も既存生成フローに従って加える。カードの増加後もサイズを均等に保ち、将来の追加に対応。
- 古いindex.htmlを手作業で1か所だけ更新してはいけない。生成元を修正して生成→--check、関連ゲートウェイの回帰を確認。
- サイトジェネレータの例: tools/build_satzbild_site.py + assets/satzbild-site-copy.json + assets/satzbild-site.css。標準レイアウトは tools/product_site.py、導入ガイドは tools/install_frame.py。新規ファイルを手編集・生成チェック不能にする構成を避ける。
- CSS生成はcanonical CSSとの内容一致と意図的差分を表示。日本語/英語本文の共有キーは tools/base_copy.py --check で照合。書き換え差分はDE固有キーのみ。
- 以下12ページで実ブラウザ検証：320/375/768/1280 CSS px、実ズーム200%や同等の文字拡大、文字間隔オーバーライド、キーボードfocus、言語切替、戻るリンク、導入リンク、表示中版数、公式ロゴ、長複合語・見出しの折返し。
- 横幅超過・ラベル隠し・文字切れ・クリック不可能なCTA・意図しない強制単語切断は禁止。上端だけclipする/小さなフォントへ縮める応急措置も合格扱いしない。
- 既存日本語版、言語トップ、少なくとも一つの既存独立言語版を回帰検査。他言語の独立CSSを巻き込むGlobal変更は避ける。
- docs/de/DESIGN_APPLICATION_RECEIPT.md に使用した Skill ID/実ファイルpath/Rule IDs、起点のcanonical source、実行前Design Contract、描画環境、screenshots、所見と例外を記録。実際のSkillが適用できなかった場合は事実を残す。

WG03 Done gate: 完成した製品に基づく3 LP + 9 install guides + DE language card と、コピー共通性・responsive・必要な根拠が揃う。公開前の「公開済み」表示はしない。WG04へ進む。
