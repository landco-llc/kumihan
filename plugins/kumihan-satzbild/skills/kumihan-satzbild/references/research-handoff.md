# KUMIHAN｜Satzbild — 研究用44ルールと48ケース（実装入力）

Extracted on 2026-10-19 JST from Owner-prepared KUMIHAN_DE_Research_Report_20261019_JA.md.

**Research-only. These are proposed guidance and test cases, not 44 implemented detectors or 48 passed tests.** Refer to the master /goal instruction and verify each adopted rule with sources and actual output. Content is an original research summary. Do not copy protected images, external article text, or paid standards into packages.

## 重要な作業区分

- KUMIHAN全言語の共通原則：原稿保護、目的に基づく情報設計、媒体別の品質検証、未検証/例外の明示。
- DE固有：ドイツ語正書法、de-DE/de-AT/de-CH、引用符、ß/ẞ/SS、複合語、分綴、数値、du/Sieなど。
- 44個のうち実際に静的判定可能な少数だけchecker実装、残りはガイダンスや人間判断と明示。
- 元報告の出典ID [Nxx] はこのファイル末尾で公開資料に対応。組織方針をDACH全域に一律適用しない。

## 13 開発用ルール候補44件

### 地域と前提

| ID | ルール候補と根拠 | 検証 | 重大度案 |
|---|---|---|---|
| DE-CTX-001 | 言語地域を明示する。未設定原稿を自動でDE表記へ変えない [N01][N27] | S L | E |
| DE-CTX-002 | 媒体とハウススタイルを地域とは別に解決する [N20][N22] | S L | E |
| DE-CTX-003 | 通貨 タイムゾーン 値型を独立設定にする [N30][W05] | S D | E |
| DE-CTX-004 | 名前 ブランド語彙 価格 原稿の文字列を保護する [P02] | D L | E |

### 文字組

| ID | ルール候補と根拠 | 検証 | 重大度案 |
|---|---|---|---|
| DE-TYPE-001 | ウムラウト ß ẞ 約物を最終書体で確認する [N05][T01] | S R | E |
| DE-TYPE-002 | ẞとSS双方の許容を守り 一律の逆変換をしない [N04] | D L | E |
| DE-TYPE-003 | 引用符の開閉 入れ子 方向と採用セットを確認する [N17][N18][N38] | S R L | W |
| DE-TYPE-004 | スラッシュ アポストロフィを文脈で分類する [N16][N19] | S L | W |
| DE-TYPE-005 | ダッシュ ハイフン マイナス 省略点を区別する [N14][N15] | S R L | W |
| DE-TYPE-006 | 複合語を空白で壊さず必須 任意ハイフンを区別する [N09] | L D | W |
| DE-TYPE-007 | 分綴は言語と語構造に応じて実表示を確認する [N10][N11][N12][N13] | S R L | E |
| DE-TYPE-008 | soft hyphenや非改行の範囲を保護語と用途に限定する [T03][P02] | D R | W |
| DE-TYPE-009 | 字間 行高を本文と見出しで分け 欠けを検査する [P01] | S R | W |
| DE-TYPE-010 | 合字の形態上の境界は専門組版の確認項目とする [N37][W06] | R L | A |
| DE-TYPE-011 | ラグ組 両端揃え 分綴 語間を一緒に判断する [T03] | R L | W |
| DE-TYPE-012 | 見出しの修飾関係と意味のまとまりを保つ [N07][P01] | R L | W |

### 数値と日時

| ID | ルール候補と根拠 | 検証 | 重大度案 |
|---|---|---|---|
| DE-NUM-001 | 採用するIntlとCLDRの版及び出力を記録する [N24][N25][W05] | S D | E |
| DE-NUM-002 | 値と単位 短い金額ペアの分離を確認する [N23] | R D | W |
| DE-NUM-003 | 日付 時刻 地域月名とタイムゾーンを分ける [N22][N26] | S D | E |
| DE-NUM-004 | 数値の入力解析と表示変換を分け識別子を保持する [W05][P02] | S D | E |

### コピー

| ID | ルール候補と根拠 | 検証 | 重大度案 |
|---|---|---|---|
| DE-COPY-001 | du Sie 大文字化 話者の一貫性を確認する [N08][S01][S02][S03] | S L | W |
| DE-COPY-002 | 名詞と見出しの大文字を守り英語式Title Caseを強制しない [N06][N07] | S L | W |
| DE-COPY-003 | CTAとエラーを実際の処理及び確定状態に合わせる [S01][S10][S14] | L D R | E |
| DE-COPY-004 | 具体性のない主張や無根拠の効果を追加しない [S12][P02] | L D | E |
| DE-COPY-005 | ジェンダー表記の方針を保ち意味を変える自動変換をしない [N31][S16][S17] | L D | W |
| DE-COPY-006 | 地域語 英語 固有名とplain easyの目的を区別する [S06][S11][S19][A01][A02] | L D | W |

### Web

| ID | ルール候補と根拠 | 検証 | 重大度案 |
|---|---|---|---|
| DE-WEB-001 | 本文全体にbreak-allやanywhereを適用しない [T03] | S R | E |
| DE-WEB-002 | 長いラベルで幅と行数を調整し固定高を確認する [A05][A06] | R | E |
| DE-WEB-003 | langと必要な言語部分及び分綴リソースを確認する [A03][A08][T03] | S R | E |
| DE-WEB-004 | 狭幅 200%拡大 文字間隔上書きを別条件で確認する [A05][A06][W07] | R | E |
| DE-WEB-005 | 追加CSS機能は対象環境で検証し未対応を区別する [W02] | S R | W |
| DE-WEB-006 | エラー フォーカス状態と可視ラベル 名前を照合する [A04][P02] | S R L | E |
| DE-WEB-007 | フォント読み込み前後を確認しclipで欠落を隠さない [T01][A05] | S R | E |

### 資料

| ID | ルール候補と根拠 | 検証 | 重大度案 |
|---|---|---|---|
| DE-DOC-001 | 文書言語 分綴辞書と出力先の設定を確認する [P02][N10] | S R | W |
| DE-DOC-002 | 見出し孤立 表行 図版出典 分綴の連続を確認する [P02] | R L | W |
| DE-DOC-003 | スライドは情報を分割し縮小だけで解決しない [P02] | R L | W |
| DE-DOC-004 | PDFの選択 コピー 書体 編集性を別々に確認する [P02][T02] | D R | E |

### デザイン

| ID | ルール候補と根拠 | 検証 | 重大度案 |
|---|---|---|---|
| DE-DESIGN-001 | 制作前に読者 目的 情報構造とその理由を記録する [P01] | L | W |
| DE-DESIGN-002 | 表現書体 手書き 回転文字は役割から判断する [D06][D07][D09] | R L | A |
| DE-DESIGN-003 | ポスターの像とWeb本文 UIの機能を分ける [D02][D04][D08] | R L | W |
| DE-DESIGN-004 | 図版 発言 書体の出所と使用範囲を確認する [P02][F15][F20] | S L | E |

### 根拠と検証

| ID | ルール候補と根拠 | 検証 | 重大度案 |
|---|---|---|---|
| DE-EVID-001 | 規範 組織方針 観察 提案を分ける [P01][P02] | S L | E |
| DE-EVID-002 | 実行環境 フォント 辞書 仕様の版を記録する [P02] | S D | E |
| DE-EVID-003 | 未確認 例外 不合格を区別し修正後の範囲を再確認する [P02] | S D R | E |


## 14 検証ケース候補48件

以下は将来の検証に用いる入力と期待結果の案であり、今回は実行していない。Aは初版で代表ケースを確認する群、Bは媒体・機能の採用に応じて追加する群を示す。48件すべてを毎回の制作・更新に一律実行する運用は想定しない。

| ID | 入力または状態 | 確認する結果 | 群 |
|---|---|---|---|
| DE-FX-01 | de-DEのStraßeとde-CHのStrasse | 地域の違いを扱い原稿を勝手に変えない | A |
| DE-FX-02 | de-CH本文のドイツ企業の固有名 | 地域置換から保護語を除く | A |
| DE-FX-03 | STRASSEとSTRAẞE | 双方の許容を認識しSSを逆変換しない | A |
| DE-FX-04 | MüllerとMuellerという別の名前 | 一括変換せず文字列を維持 | A |
| DE-FX-05 | NFCのäとa＋U+0308 | 表示とコピーを確認し保存方針を保つ | B |
| DE-FX-06 | ÄÖÜßẞと引用符を最終書体へ | 欠字と代替書体を明示 | A |
| DE-FX-07 | DEの„…“と入れ子‚…‘ | 選択した開閉と入れ子が一致 | A |
| DE-FX-08 | CHの«…»と‹…› | 内向きへ無断変換しない | A |
| DE-FX-09 | 承認されたDE編集用»…« | 正当な別セットを誤検出しない | A |
| DE-FX-10 | 引用符を含むコードとURL | 自然文の約物変換から除外 | A |
| DE-FX-11 | アポストロフィを含む商号 | 全体が固有名の例外を検討 | A |
| DE-FX-12 | 語省略の…とUI表示のellipsis | 文法上の省略と表示切詰めを区別 | B |
| DE-FX-13 | 語と語群に含まれるスラッシュ | 左右と文脈を確認し一括空白化しない | B |
| DE-FX-14 | KI-gestützte Gestaltung | 語の連結構造と略語を保持 | A |
| DE-FX-15 | 500 gと500-g-Beutel | 量の表示と複合語を区別 | A |
| DE-FX-16 | ch sch ckを含む分綴例 | 文字数だけで切らず辞書と規則へ照合 | A |
| DE-FX-17 | 接頭辞と複合語境界 | 許容される分綴を誤りにしない | B |
| DE-FX-18 | Stoffladenの合字 | 専門組版の境界と例外を確認 | B |
| DE-FX-19 | 単語にsoft hyphenを含む原稿 | 分綴 コピー 検索と元文字列を確認 | B |
| DE-FX-20 | Datenschutzeinstellungenのボタン | 狭幅でも全文と操作が保たれる | A |
| DE-FX-21 | Barrierefreiheitserklärungの見出し | 縮小だけで収めず意味のある表示 | A |
| DE-FX-22 | 本文にword-break:break-all | 単語の途中切断を確認し限定修正を提案 | A |
| DE-FX-23 | 長いメール URLと通常本文 | 識別子だけの折返しを適用 | A |
| DE-FX-24 | フォント不達と読み込み完了 | 改行 欠字 レイアウト変化を区別 | A |
| DE-FX-25 | 大文字ウムラウトとタイトな行高 | 上部の切れと行の重なりがない | A |
| DE-FX-26 | 長い本文を狭い列の両端揃え | 広すぎる語間と分綴の連続を観察 | B |
| DE-FX-27 | 価格と短い単位ペアを行末へ | 値や単位が不適切に分離しない | A |
| DE-FX-28 | 同じ値をDE AT CHで表示 | runtimeの期待値と組織方針を区別 | A |
| DE-FX-29 | de-ATの一般数値とEUR | 千位区切りと通貨位置の違いを保持 | A |
| DE-FX-30 | de-CH runtimeとZürich州の文書 | 別プロファイルとして整合 | B |
| DE-FX-31 | 1.000という入力と郵便番号 | 曖昧な数値を推定せず識別子を保持 | A |
| DE-FX-32 | 比率0.1と通貨小数精度 | 値を壊す倍率変更や丸めをしない | A |
| DE-FX-33 | 年末日時と別タイムゾーン | 表示変更で日付値を誤変更しない | B |
| DE-FX-34 | Jänner Marille Billette | 地域語をドイツの語へ自動統一しない | A |
| DE-FX-35 | 同一フローにduとSieが混在 | 話者 引用 法的補足を分けて候補検出 | A |
| DE-FX-36 | Du系ブランドと通常小文字du | ハウススタイルと規範を区別 | B |
| DE-FX-37 | 英語式Title Caseと独語見出し | 名詞と文頭の大文字を保つ | A |
| DE-FX-38 | 承認英語名と未承認の別言語文 | 固有名例外を残し混入を確認 | A |
| DE-FX-39 | 確認画面のCTAに購入確定語 | 実動作との不一致を指摘 | A |
| DE-FX-40 | 支払状態が不明 成功 失敗 | 不明状態を成功や未請求と断定しない | A |
| DE-FX-41 | ジェンダー方式の変更案 | 方針とリライト許可を確認 | A |
| DE-FX-42 | 普通の短文をLeichte Spracheと表示 | 未実施の適合 認証を宣言しない | A |
| DE-FX-43 | 320 CSS px相当の画面 | 例外以外の横往復と情報欠落を確認 | A |
| DE-FX-44 | 文字200%と間隔4値の上書き | 別条件として内容 機能の保持を検査 | A |
| DE-FX-45 | 独語可視ラベルと英語の名前 | アクセシブル名との対応を確認 | A |
| DE-FX-46 | 表行と見出しがページ末へ | 表見出し 図版出典 孤立を確認 | A |
| DE-FX-47 | 長いスライドをPDFへ変換 | 文字 単位 出典 書体 コピーを確認 | A |
| DE-FX-48 | ポスターと業務UIへ同一の装飾 | 目的に応じた差を確認し絶対採点しない | B |

検証の結果はpassed、failed、needs-review、not-checked、unsupported、not-applicable等を区別する。支援技術の試験をしていない場合に、スクリーンショットだけを根拠として読み上げもpassedにしない。[P02]


## 一次資料と技術資料（原報告の参照索引）

### 正書法 地域差と文書規範

[N01] [IDS grammis・2024公式正書法「Einführung」](https://grammis.ids-mannheim.de/rechtschreibung/6392)。公式正書法の学校・行政への適用と企業等の参照、地域標準

[N02] [Rat・2024-07-03発表](https://www.rechtschreibrat.com/amtliche-deutsche-rechtschreibung-ueberarbeitetes-regelwerk-und-neufassung-woerterverzeichnis-fuer-schule-und-verwaltung-verbindlich/)。2024基準日、各国の移行期間、改訂事項

[N03] [öbv・ÖWB更新44版](https://www.oebv.at/produkte/oewb-1-4-9)。ATで2025-09-01から2年移行、ATの標準語彙

[N04] [IDS・§25](https://grammis.ids-mannheim.de/rechtschreibung/6180)。ß/ss、CH/LI、ẞ/SS

[N05] [IDS・文字集合](https://grammis.ids-mannheim.de/rechtschreibung/6144)。Umlaut、大文字ẞ、外来固有名の追加文字

[N06] [IDS・大文字小文字総説](https://grammis.ids-mannheim.de/rechtschreibung/6161)。名詞・名詞化・固有名等の大文字

[N07] [IDS・§53](https://grammis.ids-mannheim.de/rechtschreibung/6162)。見出しの第一語の大文字

[N08] [IDS・§65–66](https://grammis.ids-mannheim.de/rechtschreibung/6197)。Sie/Ihr、du/ihr、手紙の選択肢

[N09] [IDS・§40–45](https://grammis.ids-mannheim.de/rechtschreibung/6159)。複合語・必須/任意ハイフン・英語借用語

[N10] [IDS・§84](https://grammis.ids-mannheim.de/rechtschreibung/6214)。単独母音一字を分離しない、誤読分割を避ける

[N11] [IDS・§85](https://grammis.ids-mannheim.de/rechtschreibung/6215)。複合語と接頭辞境界の分綴

[N12] [IDS・§86–89](https://grammis.ids-mannheim.de/rechtschreibung/6216)。子音・ch/sch/ck等の分綴

[N13] [IDS・§90](https://grammis.ids-mannheim.de/rechtschreibung/6217)。複数の許容分綴があり得る

[N14] [IDS・§77](https://grammis.ids-mannheim.de/rechtschreibung/6209)。GedankenstrichとDivisの差

[N15] [IDS・§78](https://grammis.ids-mannheim.de/rechtschreibung/6210)。省略点と空白、句読点、引用の角括弧

[N16] [IDS・§83](https://grammis.ids-mannheim.de/rechtschreibung/6122)。スラッシュの空白・語群・省略条件

[N17] [Duden・Anführungszeichen](https://www.duden.de/sprachwissen/rechtschreibregeln/anfuehrungszeichen)。引用符の複数形状、入れ子、句読点。Duden編集解説

[N18] [Universität Zürich・綴りと句読法](https://www.kommunikation.uzh.ch/de/web/bestpractice/spelling.html)。UZHでの«»と内側‹›、複合語の扱い。組織限定の方針

[N19] [IDS・§80](https://grammis.ids-mannheim.de/rechtschreibung/6212)。アポストロフィの機能、全体が固有名になる属格s例外

[N20] [DIN Media・DIN5008:2020-03](https://www.dinmedia.de/de/norm/din-5008/318422674)。規格の公式スコープと状態。本文未読

[N21] [スイス連邦首相府・Schreibweisungen紹介](https://www.bk.admin.ch/de/schreibweisungen)。連邦文書への適用、公開PDFへのリンク。PDF条項は未確認

[N22] [Kanton Zürich・Umgang mit Sprache](https://www.zh.ch/de/webangebote-entwickeln-und-gestalten/inhalt/inhalte-gestalten/informationen-bereitstellen/umgang-mit-sprache.html)。同州の日時・非通貨/CHF/EUR・桁区切りなど。全国一律でない

[N23] [PTB・SIブロシュア独訳2025（更新2024）](https://www.ptb.de/cms/fileadmin/internet/presse_aktuelles/broschueren/intern_einheitensystem/PTB-Mitteilungen_2025_Heft_2.pdf)。数値/単位間の空白、角度例外、複合語、%と科学数字表示

[N24] [Unicode CLDR49・Numbers:Symbols](https://unicode.org/cldr/charts/49/by_type/numbers.symbols.html)。de/de-AT/de-CHの小数・桁区切り、AT通貨別区切り

[N25] [Unicode CLDR49・Number Formatting Patterns](https://unicode.org/cldr/charts/49/by_type/numbers.number_formatting_patterns.html)。通貨記号の前後、数値型の別パターン

[N26] [Unicode CLDR49・German Summary](https://www.unicode.org/cldr/charts/49/summary/de.html)。ドイツ語地域データ・月名Jännerなど

[N27] [Rat・2017地域差の決議](https://www.rechtschreibrat.com/DOX/rfdr_2017-11-10_Beschluss_laenderspezifischer_Variation.pdf)。各地域の標準語が対等である方針。現行個別綴りは2024版で確認

[N30] [Unicode CLDR・Number and currency patterns](https://cldr.unicode.org/translation/number-currency-formats/number-and-currency-patterns)。小数・通貨・割合・科学の別パターン、データ運用

[N31] [IDS・Sonderzeichen](https://grammis.ids-mannheim.de/rechtschreibung/6123)。語中ジェンダー記号と正書法の範囲

[N33] [Austrian Standards・ÖNORM A1080:2007-03-01](https://www.austrian-standards.at/de/shop/onorm-a-1080-2007-03-01~p1536064)。文書構成・教育目的のカタログ説明のみ。現行性結論は出さない

[N35] [IDS・§79](https://grammis.ids-mannheim.de/rechtschreibung/6211)。引用符と句読点の関係、作品名・言及・距離の機能

[N37] [Typografie.info・Ralf Herrmann「Wann setzt man im Deutschen Ligaturen und wann nicht?」（2014）](https://www.typografie.info/3/faq.htm/wann-setzt-man-im-deutschen-ligaturen-und-wann-nicht-r28/)。合字と形態素境界、接尾辞・省略形の例外。専門家自身の組版解説で、公式正書法ではない

[N38] [Typolexikon・Wolfgang Beinert「Anführungszeichen」（2023）](https://www.typolexikon.de/anfuehrungszeichen/)。DE/AT内向きとCH外向き、CH内空白なし、位置と書体上の形の区別。専門家の組版解説



Documentation origin: original research report is stored in the Owner's KUMIHAN / RESEARCH / DE Drive folder. This public excerpt includes only candidate rules, fixtures and reference index; it does not publish private PDFs or observation images.
