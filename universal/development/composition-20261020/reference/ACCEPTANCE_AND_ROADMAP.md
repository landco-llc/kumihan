> **Source-design reference (not implemented).** Acceptance cases P01-P40; they are proposed and not product-tested.
> Public repository copy excludes private-source ledgers and research images. Follow the versioned JSON Schema. Do not infer permission to deploy or publish.

# 受入試験と段階導入計画

版：0.1.0-design.1 / 2026-10-20  
**この文書は将来の製品試験計画。下表の試験は実施していない。** 同梱schema・例示・参照validatorの設計検証だけが今回の実施対象である。

## 1. 二つのGateを分ける

### D：設計パッケージの整合

JSON Schemaのmeta-schema、代表12record、範囲・参照・digest・原稿保持の不変条件、証拠なしpassed、既存reportとの責任分離を確認する。同梱`validation/test_contract.py`はこの範囲の試験である。母語評価、Unicode全適合、製品描画テストではない。

### P：製品機能の受入

実装後に対象hostとfontを固定し、下記を実行する。合格を宣言する単位は `機能 × 言語/文字体系 × 媒体 × host/version × corpus`。全体を単一の「21言語対応」フラグで扱わない。

## 2. 必須の試験記録

sourceの元バイトまたは保持すべき論理文字列とdigest、BCP 47注釈の由来、規則・辞書・Unicodeの版、font instance、host/app/browser/OS、viewportまたはページ寸法・zoom、生成artifactとdigest、実際の画像・抽出・読み順、検証範囲、判定者、未検証事項を記録する。

文字列が壊れないという静的試験と、正しく読める表示になったという描画・母語試験は別である。

## 3. 製品受入ケース40件

| ID | 入力・条件 | 必須確認／期待結果 | 主な証拠 |
|---|---|---|---|
| P01 | JA+ZH-Hant、同じ漢字を含む商品説明 | 原字保持、言語注釈、地域字形をfont選択で区別 | text+render+母語 |
| P02 | ZH-Hans+ZH-Hant、引用と地名 | 簡繁自動変換なし、引用内部を保持 | text+render |
| P03 | KO+TH、短いボタンと本文 | 韓国語・タイ語を同じ単語分割器に押し込まない | boundary+render+母語 |
| P04 | HI+BN、結合字と上下mark | glyph clusterを途中分割しない、切取りなし | shaping+render |
| P05 | AR+HE、同一段落と並列block | RTL同士でも同じ接合処理にしない | bidi+render |
| P06 | FA+RU、引用符・型番・数字 | 保存順不変、局所方向が段落を乱さない | text+bidi+render |
| P07 | JA+AR+FR、3言語の説明 | 英語moduleなしで処理、段落ごとの方向 | resolver+render |
| P08 | ZH-Hant+KO+VI、展示解説 | 行数を強制一致させない、同等の重要度 | render+母語 |
| P09 | FR+DE、同じLatin文字体系 | 引用・分綴・約物のlanguage差を保持 | boundary+editorial |
| P10 | PL+ES、1字語・アクセント | 全大文字でも記号を脱落させない | text+render |
| P11 | PT+NL、分綴の派生表示 | no_break/pre/postとsource mapping、抽出復元 | dictionary+extract |
| P12 | ID+SW+ZU、長い語・接辞 | 見た目のために語へ空白を追加しない | text+母語+render |
| P13 | EL+RU、似た字形を含む語 | Latinへの置換なし、glyphとscriptの区別 | text+font |
| P14 | TH+KM、上下の記号と辞書分割 | 不要なASCII空白を入れずmarkを表示 | dictionary+render |
| P15 | HEのniqqud＋AR母音記号 | 基底文字とmarkのfont fallbackを検証 | shaping+render |
| P16 | VIの結合アクセント＋FA ZWNJ | NFC/NFKCや不可視文字除去をしない | source digest |
| P17 | 空白・数字・記号だけ | 言語を英語と断定しない | resolver |
| P18 | 1–2字のHan、固有名 | 候補・undを返し、黙ってlocaleを確定しない | resolver |
| P19 | private-useタグ・未知locale | 入力保持、未対応規則を明示 | schema+resolver |
| P20 | Adlam等の拡張script | LTR地理推定をせず、能力不足を明示 | resolver+host |
| P21 | Mongolian縦組 | vertical-lr等とadapter能力を分離 | host+render |
| P22 | 日本語縦組＋別scriptの長い語 | orientation/縦中横/回転を条件付きで検討 | render+母語 |
| P23 | 数式・絵文字ZWJ列・異体字セレクタ | scalar/UTF-16/glyph indexを混用しない | index mapping |
| P24 | sourceに既存Bidi制御文字 | 無断除去なし、異常は警告 | static+bidi |
| P25 | authorタグと検出候補の不一致 | 明示情報と矛盾を示し、根拠を記録 | resolver |
| P26 | 等価未確認の2言語見出し | translation verifiedにしない | relationship audit |
| P27 | ルビ・注音・IPA・翻字 | 親範囲、注記、読み順を保持 | render+accessibility |
| P28 | 本文と広告短句が同じページ | reading/displayの規則をregion単位に適用 | plan+render |
| P29 | 承認されたロゴの重なり | 指定範囲だけ例外、本文への波及なし | scope+approval+render |
| P30 | CTAや重要条件が図形に隠れる | displayを理由に許可せずfailed | full-page render |
| P31 | fallback font未ロード/ネット切断 | 欠字・高さ・改行の変化を検出 | font+render |
| P32 | 可変fontのaxes/版を変更 | 前の校正結果をそのまま再利用しない | font identity |
| P33 | Web 320 CSS px | 適用範囲のreflow、操作情報の欠落なし | browser+interaction |
| P34 | Web text 200% zoom | clipping/overlapなし、重要情報保持 | browser |
| P35 | 適用されるWCAG spacing override | 言語例外を踏まえ内容・機能を保持 | browser |
| P36 | PPTXの複数textbox/図形/ノート | 全slide表示、遮蔽、読み順、原稿・ノート保持 | native PowerPoint |
| P37 | DOCXの段落・脚注・表・caption | ページ跨ぎと方向、source対応を保持 | native Word |
| P38 | PDF抽出とコピー | 画面の見た目と論理原文の一致を別に評価 | PDF render+extract |
| P39 | グラフィック化・outline化 | 必須情報の読める別経路、source対応 | artifact+access |
| P40 | stale digest/未知critical拡張/上限超過 | 偽の完了を返さず対象範囲と再開条件を返す | contract+negative |

これらは代表的な問題クラスを覆う試験であり、全言語の全文章を網羅する保証ではない。特にP01–P16は英語以外の組合せを意図的に含める。

## 4. コーパスの作り方

最初は短句・長文・固有名・数字・引用・注記・重要情報を分ける。人工fixtureはUnicodeや原稿保持の失敗を再現しやすいが、広告コピーや言語としての自然さを証明しない。公開許諾のある実コーパスと母語レビューを後から追加し、出典・権利・翻訳確認状態を記録する。

単語の正誤を期待値にする場合は辞書の版か母語校閲者を必要とする。モデルが生成した期待値を同じモデルに採点させて「独立検証」と呼ばない。意味改行の正解が一意でないケースは、複数の許容候補と避ける境界を持つ。

## 5. 優先順位とWork群

| Work群 | 目的 | 完了条件 | 開始条件 |
|---|---|---|---|
| W00–W02 | 本設計と現行schema/registryの差分、契約と互換性 | 旧consumerを壊さず新sidecarを読める | 実装の別承認、最新版Fresh Read |
| W03–W05 | source保護・言語範囲・関係・能力解決 | 未知言語と矛盾を明示、negative tests成立 | 契約受入 |
| W06–W08 | read-only混植レビューと代表Web adapter | P01/P03/P05/P06/P07/P16/P23/P25/P33–35の選定範囲 | host/font/corpus固定 |
| W09–W11 | native文書adapter、抽出・読み順 | P36–P38を対象アプリで確認 | 文書共通基盤との調整 |
| W12以降 | 光学補正・辞書・縦組・特殊表現 | 各featureの証拠付き拡張 | 利用実績と優先顧客の確認 |

今回このWork群を実行したわけではない。Codex Cloud/Appへの起動指示も発行していない。

## 6. 90日・180日の計画案

**0–30日**：設計レビューと現行差分確認。コア契約、未知言語fallback、原稿保持、読み順、代表テストの最小実装。英語版開発は共通契約への接続口を作り、英語を既定親にしない。

**31–90日**：利用目的を絞ったWebの実証。多言語LP・商品説明・展示解説・社内資料から2–3種類を選び、通常のAI生成とKUMIHAN適用後を同じ原稿・font・環境で比較する。重大欠陥、修正時間、レビュー指摘、原稿差分、母語評価を測る。売上の仮定を置かず、導入先が再利用したかを確認する。

**91–180日**：native Office/PDF、縦組、拡張scriptを需要に応じて追加。書体・用途別の校正profileを蓄積し、未検証環境へ横流ししない。商用導入・制作支援等を検討する場合も、無料の共通知識と個別の検証・運用支援を混同しない。

固定日程の約束ではない。母語校閲・テストhost・fontの利用条件と担当が整うことを前提とする。

## 7. やらないこと

全言語ペアへの専用CSS、独自Unicodeエンジン、すべての書体への固定95%補正、国ごとの固定デザイン趣味、母語レビューなしの自然さ保証、未描画対象の自動合格、資料を読み込んだだけでの製品公開は行わない。
