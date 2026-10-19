## 13 提案ルールカタログ

以下の40ルールは初版の開発へ渡す提案である。実装済みの機能一覧でも、試験に合格した項目の一覧でもない。判定対象の言語・媒体・役割・編集方針を先に特定し、原稿の保護範囲を確定してから適用する。

`error` は対象と根拠が確定した不適合、`warn` は文脈・指定・実測の確認が必要な状態、`proposal` は任意の改善案、`preserve` は保持を表す。`error` であっても無断の一括修正を許可する意味ではない。レビュー時は指摘のみとし、変更は編集可能な範囲に限定して差分を残す。判断がつかない場合は `warn` または `preserve` に下げる。

根拠欄のLは言語・編集資料、Uはデジタル資料、TはUnicode資料、Vは制作・書体資料、Oは本調査の限定実測を指す。「本報告の提案」は規範そのものではなく、調査を踏まえたKUMIHANの設計判断である。

### 13.1 綴りと語法 — R01〜R08

| ID | 判定・対象 | 処理 | 根拠 |
| --- | --- | --- | --- |
| R01 | 通常のイタリア語におけるéとèの取り違え | error・辞書と文脈の確定後に修正案。外国語へ一括適用不可 | [L02] |
| R02 | 大文字化で失われたアクセント、動詞Èの代用表記 | error・表示原稿の修正案。大文字アクセントを保持 | [L02][L14] |
| R03 | 通常文のqual’èと標準綴りqual è | error・通常文は修正案。引用・表記解説は変更不可 | [L01] |
| R04 | pocoの短縮とpòの混同 | error・po’を提案。Poなどの固有名は変更不可 | [L03] |
| R05 | e/è、da/dà、si/sì、te/tèなどの意味・品詞 | warn・文脈を確認。文字列一致だけの修正不可 | [L02][L03] |
| R06 | sé stessoとse stessoの選択 | proposal・指定方針への統一案。無条件のerror判定不可 | [L02][L14] |
| R07 | da、fa、sta、vaと命令形・短縮形 | warn・語法を確認。アポストロフィやアクセントの自動追加不可 | [L03] |
| R08 | ed/ad/odと定着表現・後続音 | proposal・文体として確認。同母音だけを条件に変更不可 | [L05][L06] |

### 13.2 引用・大文字・原稿保護 — R09〜R16

| ID | 判定・対象 | 処理 | 根拠 |
| --- | --- | --- | --- |
| R09 | 引用符の外側・内側と編集方式 | preserve・一貫した既存方式を保持。指定時だけ統一案 | [L12][L13] |
| R10 | 引用内の空白と句読点の帰属 | warn・引用範囲と方針を確認。句点の一括移動不可 | [L07][L13][L15] |
| R11 | ハイフン、挿入句、範囲、負号の役割 | warn・用途と編集方式を確認。外見だけで置換不可 | [L13][L14] |
| R12 | 見出しの大文字、略語、正式名称 | proposal・通常見出しの案を提示。ロゴ・正式表記は保持 | [L10][L12][U01] |
| R13 | 月・曜日・祝祭名とカレンダー等の省略形 | warn・文頭・固有名・媒体を確認。小文字化や句点追加を強制しない | [L10][L11] |
| R14 | 原著引用、商品名、人名、外国語の綴り | preserve・原文を保持。変更は明示された編集範囲だけ | [L01][L07]を踏まえた本報告の提案 |
| R15 | URL、コード、ID、検索キー、保存用の値 | preserve・元文字列を保持。表示用記号変換の対象外 | 本報告の提案 |
| R16 | 正規化、署名・ハッシュ対象、結合文字の分割 | preserve・元バイト列を保持。必要な表示変換は別処理とし差分を記録 | [T01][T02]を踏まえた本報告の提案 |

### 13.3 改行・段落・文字表示 — R17〜R24

| ID | 判定・対象 | 処理 | 根拠 |
| --- | --- | --- | --- |
| R17 | アポストロフィ直後の改行 | preserve・合法な折返しを保持。母音復元による修正不可 | [L04] |
| R18 | 音節分割と複合語の境界 | warn・辞書と別解を確認。単一の正規表現による確定不可 | [L08][L09] |
| R19 | ページと外国語文章部分の言語指定 | warn・言語を確認して修正案。固有名・定着語の機械的なタグ追加不可 | [U07][U08][U09] |
| R20 | 自動分綴の言語資源と実際の動作 | warn・対象環境で確認。CSS指定だけで適用済みと判定不可 | [U10] |
| R21 | 本文の単語折返しと長いURLの局所対策 | warn・溢れのある領域を調整。本文全体のbreak-all化は不可 | [U10]を踏まえた本報告の提案 |
| R22 | 見出しの意味の切れ目、孤立行、見出しと次段落 | proposal・描画を見て配置案。語句削除や強制改行の一括挿入不可 | [L08][U11]を踏まえた本報告の提案 |
| R23 | 揃え方、行長、行高、段落間隔 | proposal・媒体と書体に応じて調整。推奨値を必須規範にしない | [U04]を踏まえた本報告の提案 |
| R24 | 実字形、太字・斜体、大文字アクセント、fallback | warn・実際の表示で確認。書体名や文字集合だけで合格判定不可 | [U04][U12][V11][V13] |

### 13.4 地域書式・書体・視覚表現 — R25〜R32

| ID | 判定・対象 | 処理 | 根拠 |
| --- | --- | --- | --- |
| R25 | it-IT、it-CH、EU・スイス機関別の表示方式 | warn・localeと編集規程を分ける。Intlと機関書式を混同しない | [L14][L15][U05][U06][O01] |
| R26 | 数値・通貨・負号・桁数・丸め・4桁の区切り | preserve・元値と精度を保持。型と用途が確定した表示層だけ整形 | [U05][U06][O01]を踏まえた本報告の提案 |
| R27 | 数値と単位・通貨・割合、保護スペース | proposal・選択方式に沿って短いまとまりを保護。全段落のnowrap化不可 | [L14][L15][U05][U23] |
| R28 | 日付・時刻・先頭ゼロ・地域・タイムゾーン | warn・指定条件に沿う表示案。保存値・年・日時の意味は変更不可 | [L11][L14][L15][U05][U06] |
| R29 | 等幅数字、序数字形などのOpenType機能 | proposal・書体対応と実表示を確認して採用。CSS指定だけの適用宣言不可 | [U12] |
| R30 | 書体のWeb利用、埋込み、再配布、試用条件 | warn・採用用途と同梱文書を確認。権利範囲不明のまま配布物へ追加不可 | [V12][V14] |
| R31 | 文字のコントラストと画像化された本文・操作名 | warn・基準の適用範囲と例外を確認して改善。見た目だけで適合宣言不可 | [U16][U17] |
| R32 | 装飾、配色、書体の国籍、コピーの修辞 | proposal・目的と情報階層から代替案。好みだけのerror判定や全面禁止不可 | 本報告の提案 |

### 13.5 コピー・操作・アクセシビリティ — R33〜R40

| ID | 判定・対象 | 処理 | 根拠 |
| --- | --- | --- | --- |
| R33 | tu/Lei/voiと文脈・読者・ブランド文体 | proposal・役割を読んで整合案。引用や複数読者への呼びかけは保持 | [U02][U24] |
| R34 | 包摂的な言い換えと既存の著者表現 | preserve・指定表現を保持。任意の言い換え案のみ、無断追加・削除不可 | [U01][U25]を踏まえた本報告の提案 |
| R35 | CTAの操作内容と可視ラベル・アクセシブルネーム | warn・操作を確認してラベル案。可視ラベルを含む名前を確認 | [U03][U18] |
| R36 | 入力条件、エラー特定・修正案、成功と失敗の文言 | warn・観測された状態に合わせて修正案。原因や成功を推測で断言不可 | [U03][U19][U20][U21] |
| R37 | 文字200%拡大時の内容・機能の保持 | warn・文字拡大を独立確認。欠落時は修正案、未実施はnot-checked | [U13] |
| R38 | 320 CSS px相当幅のリフロー | warn・適用例外も含め確認。不要な二方向スクロールや欠落を調整 | [U14] |
| R39 | 行高・段落後・字間・単語間の同時上書き | warn・上書き耐性を確認。試験値を初期デザインへ強制しない | [U15] |
| R40 | 操作対象の大きさと間隔・例外 | warn・最小条件への適合を確認。全ボタン一律24pxへの変更不可 | [U22] |

## 14 評価用フィクスチャ

48件すべてが開発用の評価案であり、本報告書で評価器やKUMIHANの合格を確認したものではない。F01〜F24は言語判断と原稿保護、F25〜F48は表示・データ・操作の評価に重点を置く。同じ文字列でも、綴りの判断と描画・コピー操作の確認は別の評価である。

入力文は本報告の自作例と、確認条件を示す短い記号列である。期待結果に記した判定語はルール案の処理を指す。評価の実施結果は別に `pass`、`fail`、`needs-review`、`not-checked` で記録する。以下の全フィクスチャの実施状態は `not-checked` とする。

F32〜F35の一部には、第06章の限定実測[O01]を参考値として使用する。環境はNode.js v24.19.0、ICU 78.3、CLDR 48.0。数値は既定のIntl.NumberFormat、通貨はEURまたはCHF、割合は最大小数1桁の指定による。この既存観測と、提案したフィクスチャを後工程で実行した結果を混同しない。別環境の文字列差だけでは不合格とせず、使用版・option・値・通貨・符号を確認する。

表中の `NBSP` はU+00A0の明示表記であり、文字列中に英字NBSPを挿入する指示ではない。`U+0027` と `U+2019` も役割を区別するために記載する。

### 14.1 綴り・意味・原稿保護 — F01〜F12

| ID | 入力・条件 | 期待結果 |
| --- | --- | --- |
| F01 | 通常の質問文 `Qual’è il formato?` | errorとして `Qual è il formato?` を提案。修正は編集可能な原稿だけ。R03 |
| F02 | 表記解説 `Nel manoscritto compare «qual’è».` | 引用内の綴りをpreserve。F01と同じ部分一致でも書き換えない。R03・R14 |
| F03 | 通常文 `Un pò di spazio` | pocoの短縮と判断してpo’を提案。アクセント記号の装飾調整として処理しない。R04 |
| F04 | 河川名 `Il Po attraversa la pianura.` | Poをpreserve。短縮形po’へ変更しない。R04・R14 |
| F05 | 通常語 `perchè`、`caffé` | 語を確定したうえでperché、caffèを提案。鋭・重アクセントを区別。R01 |
| F06 | 通常文 `E' disponibile.` と大見出し `PERCHÉ` | 前者にÈの修正案。後者のアクセントを保持し、大文字だから削除しない。R02 |
| F07 | `Il tè e caldo.` と `Tè e caffè.` | 前者のみ文脈からèを検討。後者の接続詞eを保持。一括置換しない。R05 |
| F08 | `Pensa a sé stesso.` / `Pensa a se stesso.` | どちらも即errorにしない。必要なら選択した編集方針へのproposal。R06 |
| F09 | 条件文 `Se stessi meglio, verrei.` | 接続詞Seをpreserve。強勢代名詞séへ誤変換しない。R05・R06 |
| F10 | フランス語引用中の `café` | 外国語の綴りとしてpreserve。イタリア語caffèへ修正しない。R01・R14 |
| F11 | 固有名 `São Tomé`、`München` と外国語文章部分 | アクセント・ウムラウト・語形を保持。イタリア語の文字集合へ置換しない。R14 |
| F12 | `Fa caldo.` と `Fa’ attenzione.` | 叙述と命令の文脈を区別。全てのfaへアポストロフィやアクセントを付けない。R07 |

### 14.2 編集方式・改行・文字データ — F13〜F24

| ID | 入力・条件 | 期待結果 |
| --- | --- | --- |
| F13 | `ad esempio`、`ad eccezione di` | 定着表現をpreserve。母音が違うことだけを理由にdを削除しない。R08 |
| F14 | `Case e edifici` と原著引用中の `od` | 同母音でedを強制せず、原著のodを保持。文体提案は引用外に限定。R08・R14 |
| F15 | caporali方式を指定した `«Una forma “aperta”»` | 指定階層として保持。内部に別の引用符があるだけで混在エラーにしない。R09 |
| F16 | 英式を指定した `“Una forma ‘aperta’”` | F15と異なる正当な指定として保持。caporaliへ強制しない。R09 |
| F17 | 通常引用 `«Torna domani!».` と忠実な原著転記 | 句読点の帰属・原著再現・編集方針を確認。全句点の内外移動はしない。R10・R14 |
| F18 | 文中の `19 maggio`、祝祭名 `Primo Maggio` | 月名と固有の祝祭名を区別。全てのMaggioを小文字化しない。R13 |
| F19 | 正式名の `ONU`、編集指定の `Onu`、ポスターの全大文字 | 各役割と指定を保持。Title Caseや一つの大文字方式を強制しない。R12・R32 |
| F20 | カレンダーの `gen` と本文の略記 `gen.` | 媒体差として確認。一律の句点追加・削除をしない。R13 |
| F21 | 本文がアポストロフィの後で折り返す `dell’` → 次行 | 合法な改行としてpreserve。母音を復元しない。見出しの見栄えは別途proposal。R17 |
| F22 | 元語superatticoを `su-pe-rat-ti-co` / `su-per-at-ti-co` と分綴 | 音節境界の別解を受容。分綴用の記号を元語の恒久的なハイフンと混同しない。R11・R18 |
| F23 | URL、商品ID、JavaScriptやSQLの直線引用符を含む原稿 | 保護範囲の元文字列が不変。スマート引用符・翻訳・全角化を適用しない。R15 |
| F24 | NFCのcaffèと、NFDの `caffe\u0300`。原本は署名対象 | 元バイト列と署名を保持。表示上の正規化は別処理とし、切詰めで結合文字を分断しない。R16 |

### 14.3 言語指定・描画・地域データ — F25〜F36

| ID | 入力・条件 | 期待結果 |
| --- | --- | --- |
| F25 | イタリア語ページ内に英語の一段落。言語値候補は `it`、`it-IT`、`it_CH` | ページと文章部分の言語を確認。HTMLでは適切なBCP 47表記を使い、固有名を全て別言語指定しない。読み上げ成功は未確認。R19 |
| F26 | `à è é ì ò ù À È É Ì Ò Ù` を通常・太字・斜体で表示。Webフォントの読込失敗条件も用意 | 実字形、上端、欠字、fallbackの可読性を各条件で確認。指定した書体名だけでpassにしない。R24 |
| F27 | 表の数字、`1º`、`1°`、`20 °C` にOpenType機能を指定 | 字形機能の実在と意味を確認。序数・度・温度を一括変換せず、空白文字で桁揃えしない。R29 |
| F28 | 試用フォントの配布候補と、ライセンス文書が同梱された別の候補 | Web・埋込み・再配布の各条件を確認。無料取得やOSS製品であることから同梱可と推定しない。R30 |
| F29 | `internazionalizzazione` をイタリア語辞書が使える環境／使えない環境で配置 | 分綴または適切な再配置を確認。辞書未確認ならnot-checkedを保持し、任意の文字切断を既定にしない。R18・R20 |
| F30 | 狭幅の本文と長いURL。折返し後にコピーする | URLだけに必要な溢れ対策を適用。コピー値は元と同じ。本文全体をbreak-allにしない。R15・R21 |
| F31 | `text-wrap:balance` の見出し、ページ末の見出し、短い最終行、75chの本文 | 実際の意味の切れ目・段落の連結を確認。75chを75文字と断定せず、収めるために語句を削らない。R22・R23 |
| F32 | 型付き数値1234.56と12345.67を[O01]と同条件のit-ITで表示 | 参考値は `1234,56` と `12.345,67`。4桁区切りを強制せず、元値を保持。別環境では版・optionを確認。R25・R26 |
| F33 | 同じ数値をIntlのit-CHとスイス連邦官房方式で表示 | [O01]の参考値は `1234.56`、`12'345.67`。連邦官房の一般数値12345.67は別方式の `12`＋NBSP＋`345,67` とし、プロファイルを区別。R25 |
| F34 | 12345.67のEUR/CHF表示と、0・負数・端数の追加条件 | [O01]の参考値は `12.345,67`＋NBSP＋`€`、`CHF`＋NBSP＋`12'345.67`。追加条件は後工程で実行し、通貨・符号・精度を保持。R26 |
| F35 | 0.125を割合表示。Intl方式と機関別の空白方針を選択 | [O01]の参考値はit-ITで `12,5%`、it-CHで `12.5%`。機関方式の空白との差だけでerrorにしない。値や割合の倍率を変えない。R25・R27 |
| F36 | 用途不明の `1.234`、年の `2026`、数字を含む商品ID | 元文字列をpreserve。数値・年・IDを確定せずに解析、桁区切り、ローカライズしない。R15・R26 |

### 14.4 操作・拡大・確認状態 — F37〜F48

| ID | 入力・条件 | 期待結果 |
| --- | --- | --- |
| F37 | 狭いカードに数値＋NBSP＋単位。通貨を含む長い説明文も配置 | 指定した短いまとまりを分断せず、周囲の文は折り返す。段落全体のnowrapによる横溢れを作らない。R27 |
| F38 | 保存用ISO日時と表示日付。it-IT/it-CH、時刻の機関方式、タイムゾーンを指定 | 保存値を保持し、明示した地域・option・タイムゾーンで表示。日付ずれや区切り記号を意味確認なしに修正しない。R28 |
| F39 | ラベル・エラー・固定高領域を含めて文字を200%に拡大 | 内容・機能の欠落、重なり、クリップを確認。リフローや間隔試験とは別に記録。未実施はnot-checked。R37 |
| F40 | 縦スクロール主体の内容を320 CSS px相当幅で表示 | 情報・機能を保持し、不要な二方向スクロールを生まない。二次元配置を要する部分の例外は分けて確認。R38 |
| F41 | 文字サイズに対して行高を1.5倍、段落後の間隔を2倍とし、字間0.12em、単語間0.16emを同時に上書き | 欠落・隠蔽・操作不能がないことを確認。これらを初期デザインの必須値として固定しない。R39 |
| F42 | 可視CTAが `Scarica KUMIHAN`、アクセシブルネームが別の操作名 | 操作実体と名称の不一致を確認して修正案。可視ラベルを名前に含める。単なる短文化を優先しない。R35 |
| F43 | 入力後に消えるplaceholderだけに条件を置いた欄と、エラー表示 | 持続するラベル・条件説明を提案。エラー対象と修正手段を文字で示し、色だけで伝えない。R36 |
| F44 | 原因不明の送信失敗、保存処理中、保存完了の三状態 | 未確認の通信原因や成功を断言しない。実際に確認できた状態と文言を対応させる。R36 |
| F45 | 個人向けtu、正式応対のLei、複数読者向けvoiを使った原稿 | 役割とブランド方針を確認。混在検出だけで一つの人称へ置換しない。必要な変更はproposal。R33 |
| F46 | 著者が指定したschwa・アスタリスク・男女併記と、中立な言い換え案 | 指定表現をpreserve。代案は差分で提示。読み上げ不能・対応済みを一律に断言しない。R34 |
| F47 | 低コントラスト候補、画像化された説明文、小さな操作対象 | コントラスト、文字画像の必要性、対象サイズと間隔・例外を別々に確認。画像だけで一括passにしない。R31・R40 |
| F48 | スクリーンリーダーを使わず、HTMLと画面だけを確認したレビュー | 読み上げはnot-checkedと明示。ブラウザ・OS・支援技術・音声設定を伴う実行記録ができるまで成功を主張しない。R19・R35の証跡確認 |

### 評価記録へ残す項目

各フィクスチャについて、入力、保護範囲、適用ルール、期待する性質、実際の出力、変更差分、結果状態、確認者を残す。描画を伴うものはフォント・太字や斜体・fallback・ブラウザ・OS・viewport・ズーム・言語辞書を記録する。数値ではランタイム・ICU・CLDR・formatterのoptionと元値、読み上げでは支援技術と音声設定を加える。

一つのフィクスチャに複数の確認条件がある場合は、条件ごとに結果を分ける。綴りの正しさ、原文の保持、見た目の収まり、操作の理解、読み上げは互いに代替できない。部分的な確認結果をフィクスチャ全体のpassへ広げない。

## 15 初版開発の順序と完了条件

### 名称と配布構造は実装開始時に確定する

初版候補をv0.1.0とする場合、イタリア語版の名称、識別子、配布先、説明文の言語、対応を宣言する媒体を先に確定する。本報告では名称を決定していない。既存リポジトリのコードや配布形式を読んだ実装計画ではないため、下記は作業群の提案として扱う。

処理の順序は、**言語の確認 → 媒体の選択 → localeと編集方針の設定 → コピーの調整 → QA**とする。イタリア語の規則をすべて読み込んで全文へ一括適用する構成を避け、文章の役割と変更できる範囲を各工程で引き継ぐ。

### W00〜W06の作業群

| 作業群 | まとめて扱う内容 | 次へ渡す成果物 |
| --- | --- | --- |
| W00 現状照合と範囲確定 | 現在のリポジトリ、既存言語版、共通規則、命名・配布方法を確認 | 対象版、差分、対応範囲、変更する場所 |
| W01 言語と媒体の入口 | it・it-IT・it-CHの識別、媒体、文章の役割、編集方針、原稿保護を設計 | 設定表と適用順序、未指定時の挙動 |
| W02 表記規則と反例 | アクセント、引用、アポストロフィ、分綴、数値の規則と保護対象を実装 | 根拠付き規則、正例・反例、変更差分 |
| W03 コピーと評価 | 操作文、文体の切替、包摂表現、画一的表現を避ける確認を整備 | 媒体別の作例、提案理由、意味確認の項目 |
| W04 媒体と検証素材 | Web・文書・スライド等の対応範囲に合わせて出力方針とfixtureを用意 | 描画条件、フォント、長文・狭幅・数値の検証素材 |
| W05 実測と修正 | 宣言対象の環境で描画・操作・拡大を確認し、誤検出を修正 | 実行環境付き結果、残課題、未確認の範囲 |
| W06 配布と説明の整合 | 確定した名称・版・説明・アイコン・導入文書・同梱物を照合 | v0.1.0候補パッケージと対応範囲を示す完了報告 |

実装先の仮構造は「入口」「媒体別の説明」「規則と出典」「作例とfixture」「検証結果」「配布メタデータ」に分けて考えられる。具体的なディレクトリ名や既存スキルの識別子はW00で確認し、現在の構造に合わせる。今回の調査用フォルダをそのまま配布構造として採用する意味ではない。

### 完了は設定・挙動・証拠で判定する

初版の完了報告には、少なくとも次を含める。

- **範囲が一致すること。** 説明文、入口の判定、出力例、配布物で対応言語と媒体が食い違わない。it-CHを見つけてもit-ITの数値へ黙って置換しない。
- **原稿を守ること。** 引用、固有名、コード、数値、既存の編集方式を保護する反例を通す。自動変更と任意の提案が分かれ、差分を確認できる。
- **実測を説明できること。** ブラウザやOfficeで確認した結果には環境と条件を付ける。描画、コピー、拡大、読み上げを一括して合格にしない。
- **未確認を残せること。** 母語話者の校閲、辞書、フォント機能、支援技術などを未確認のまま対応保証へ変えない。確認していない媒体を説明文へ追加しない。
- **配布物が説明と一致すること。** 確定した名称とバージョン、導入案内、アイコン、出典参照、同梱ファイルを照合し、受け手が使い始められる形で揃える。

検証は言語の破壊、誤検出、描画の欠落、操作の不明確さに集中する。選択したfixtureで問題がなかったことを、すべてのイタリア語文書や全環境への適合へ広げない。未確認の項目は残課題として示し、初版の説明を実際に確かめた範囲へ合わせる。

現段階での次の作業は、名称と対応範囲を決め、W00で既存のKUMIHANへ接続することである。言語規則、デザイン事例、検証ケースを個別の資料に分散させず、採用した規則から出典と反例へ辿れる状態を保つ。

## 16 調査範囲と残る確認

### 今回の根拠が示すこと

本報告は、正書法・編集規定・デジタル仕様・実作品を照合して、イタリア語版KUMIHANの設計要件へ整理したものである。参照資料の発行主体と実例の制作者を明示し、資料の記述、公開図版の観察、KUMIHANへの提案を分けた。調査日はいずれも2026年10月19日日本時間、UTCでは2026年10月18日である。

現代の主要制作事例10件に、Saloneの歴史資料と2026年のキャンペーン、Corrainiの出版物、現行の商業サイト、書体の公式資料を加えた。これは市場を統計的に代表する無作為調査ではない。文化・出版・家具・デザイン分野の制作者と発行主体を中心にした、開発判断のための事例調査である。

| 確認の種類 | 実施した範囲 | この段階では言えないこと |
| --- | --- | --- |
| 資料の本文確認 | Crusca、Treccani、大学・機関の規定、公式仕様 | あらゆる出版社や地域が同じ規定に従うこと |
| 図版・PDFの視認 | 作品紹介の画像、明記したPDFページ、公式アーカイブ | Web全画面、全端末、全言語での動作保証 |
| サイト文言の確認 | 公開ページから取得できた見出し・CTA・価格等 | 実際の折返し、ホバー、決済、フォーム送信の検証 |
| 数値表示の限定実測 | Node・ICU・CLDRの記録した環境でのIntl出力 | Safari・Chrome・Firefox等の同一出力 |
| 開発設計 | 40規則案、48フィクスチャ、作業群と完了条件 | KUMIHANへの実装完了、48件のテスト合格 |

### 初版の制作時に追加する確認

イタリア語母語話者によるコピーの自然さと意味の確認、対象ブラウザでの分綴・フォント読込み・文字拡大・画面幅変更・読み上げの確認を残す。文書はMicrosoft Word等の対象アプリで、見出し・表・ページ送りを確認する。PDFは描画確認だけでアクセシブルな構造を保証せず、タグ、読む順番、文書と言語の設定を別に調べる。

実フォントを使った字形・OpenType機能の評価、再配布用フォントの選定、現在のKUMIHANリポジトリとの統合も実装段階の作業となる。今回作成した自作コピーとコードは説明用の提案であり、公開前の品質確認が完了した製品資産ではない。

### 図版の扱い

本文中の図版は構成・字形・情報階層を論じるために、出典と制作者を併記して掲載する。掲載作品の模倣用テンプレートや再配布可能な素材集としては扱わない。図版の分析から導く規則案と、図版自体の利用条件は別である。

## 17 参照資料

本文の角括弧IDからこの一覧を参照できる。リンク先は発行主体・制作者・ブランドの一次資料を原則とした。Webのページ更新と作品制作年は異なる。技術仕様のLiving StandardやEditor's Draftは、取得時の記述を参照し、実装対応を保証する資料としては扱わない。

### L 言語と編集規定 15件

**[L01] Accademia della Crusca — L’esatta grafia di qual è**

[公式解説](https://accademiadellacrusca.it/it/consulenza/lesatta-grafia-di-qual-%C3%A8/6)。標準綴りとアポストロフィの判定。

**[L02] Accademia della Crusca — Vademecum sull’accento: quando indicarlo e dove pronunciarlo**

[公式解説](https://accademiadellacrusca.it/it/consulenza/vademecum-sullaccento-quando-indicarlo-e-dove-pronunciarlo/34)。アクセントの種類、単音節語、sé stessoの扱い。

**[L03] Accademia della Crusca — Guida all’uso di accenti e apostrofi nell’italiano**

[公式解説](https://accademiadellacrusca.it/it/consulenza/uso-di-gli-per-a-loro/100)。po’などの確認。URL末尾の文言と取得本文の題名が異なるため、本文題名を採用した。

**[L04] Accademia della Crusca — Apostrofo in fin di rigo**

[公式解説](https://accademiadellacrusca.it/it/consulenza/apostrofo-in-fin-di-rigo/5)。アポストロフィ直後の改行を許容する説明。

**[L05] Treccani — d eufonicaに関する文法相談**

[2024年2月28日の回答](https://www.treccani.it/magazine/lingua_italiana/domande_e_risposte/grammatica/grammatica_1990.html)。同母音の目安と例外。

**[L06] Treccani — D [eufonica]**

[La grammatica italiana](https://www.treccani.it/enciclopedia/d-eufonica_(La-grammatica-italiana)/)。ad・ed・odの扱い。

**[L07] Treccani — 引用符と句点の位置に関する相談**

[2020年12月9日の回答](https://www.treccani.it/magazine/lingua_italiana/domande_e_risposte/varie/varie_82.html)。文末記号と原著引用の関係。

**[L08] Treccani — Sillabe, divisione in [prontuario]**

[Enciclopedia dell’Italiano](https://www.treccani.it/enciclopedia/divisione-in-prontuario-sillabe_(Enciclopedia-dell%27Italiano)/)。音節分割の詳説。

**[L09] Treccani — Sillabe, divisione in**

[La grammatica italiana](https://www.treccani.it/enciclopedia/divisione-in-sillabe_(La-grammatica-italiana)/)。分綴規則と複合語の別解。

**[L10] Treccani — Maiuscole, uso delle**

[La grammatica italiana](https://www.treccani.it/enciclopedia/uso-delle-maiuscole_(La-grammatica-italiana)/)。一般語、固有名、敬称等の大文字。

**[L11] Treccani — Giorni e mesi, nomi dei [prontuario]**

[Enciclopedia dell’Italiano](https://www.treccani.it/enciclopedia/giorni-e-mesi-nomi-dei-prontuario_(Enciclopedia-dell%27Italiano)/)。月と曜日の表記。

**[L12] Università di Bologna, CISUI — Norme redazionali**

[公式編集規定](https://centri.unibo.it/cisui/it/pubblicazioni/norme-redazionali/)。caporaliを外側に置く方式等。同機関の出版物に適用。

**[L13] Università di Bologna, Francesco Spampinato — 論文の編集・書式指示**

[教員の公式掲載資料](https://www.unibo.it/sitoweb/francesco.spampinato/contenuti-utili/1e6c5d5c)。英式二重引用符を外側に置く方式。L12との差を確認。

**[L14] Cancelleria federale svizzera — Istruzioni per la redazione dei testi ufficiali in italiano**

[官房の公式PDF](https://www.bk.admin.ch/dam/it/sd-web/gSEkvTH4mFka/istruzioni_dellacancelleriafederaleperlaredazionedeitestiufficia.pdf)。2023年版、取得文書に2025年12月15日の状態表示。引用、数値、通貨、時刻等。スイス連邦の公文書向け。

**[L15] Consiglio dell’Unione europea — Norme redazionali**

[2025年7月1日版PDF](https://www.consilium.europa.eu/media/dkogzdyg/joint_handbook_it_01-july-2025_clean_def_final.pdf)。EU文書の引用・数字・空白等。取得して本文を確認した版を採用。

### U デジタル・コピー・アクセシビリティ 25件

**[U01] Designers Italia — Linguaggio**

[.italia公式](https://designers.italia.it/design-system/fondamenti/linguaggio/)。行政向けの平易な言葉、表記と可読性。

**[U02] Designers Italia — Tono di voce**

[.italia公式](https://designers.italia.it/design-system/fondamenti/tono-di-voce/)。利用者との関係、tuと文脈に応じた声の調整。

**[U03] Designers Italia — Microtesti**

[.italia公式](https://designers.italia.it/design-system/fondamenti/microtesti/)。ボタン、入力補助、エラー等の操作文。

**[U04] Designers Italia — Tipografia**

[.italia公式](https://designers.italia.it/design-system/fondamenti/tipografia/)。Titillium Web、Lora、Roboto Monoと可読性。参照時点のTitillium Proは実験段階の説明。

**[U05] Unicode CLDR 49 — Locale Data Summary for Italian**

[公式チャート](https://unicode.org/cldr/charts/49/summary/it.html)。itとit-CHの地域差を含む表示データ。実測環境O01のCLDR 48.0とは版が異なる。

**[U06] Ecma TC39 — ECMA-402 Internationalization API Specification**

[公開仕様](https://tc39.es/ecma402/)。Intlのオプションと実装・データ依存の扱い。取得時のLiving Draftの見出し年を、確定した将来版の発行年と解釈しない。

**[U07] WHATWG — HTML Living Standard, lang / xml:lang**

[言語属性の仕様](https://html.spec.whatwg.org/multipage/dom.html#the-lang-and-xml:lang-attributes)。ページと部分の言語宣言。

**[U08] W3C WAI — Understanding 3.1.1 Language of Page**

[WCAG 2.2解説](https://www.w3.org/WAI/WCAG22/Understanding/language-of-page.html)。ページ言語の識別。

**[U09] W3C WAI — Understanding 3.1.2 Language of Parts**

[WCAG 2.2解説](https://www.w3.org/WAI/WCAG22/Understanding/language-of-parts.html)。部分言語と固有名等の例外。

**[U10] W3C CSS WG — CSS Text Module Level 3**

[公開仕様](https://drafts.csswg.org/css-text-3/)。分綴、改行、空白、overflow-wrap等。

**[U11] W3C CSS WG — CSS Text Module Level 4**

[公開仕様](https://www.w3.org/TR/css-text-4/)。text-wrapのbalance・pretty等。対応状況は実機確認の対象。

**[U12] W3C CSS WG — CSS Fonts Module Level 4**

[公開仕様](https://www.w3.org/TR/css-fonts-4/)。数字・序数などのフォント機能と表示。

**[U13] W3C WAI — Understanding 1.4.4 Resize Text**

[WCAG 2.2解説](https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html)。テキストを200%まで拡大する確認。

**[U14] W3C WAI — Understanding 1.4.10 Reflow**

[WCAG 2.2解説](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html)。縦方向の内容で幅320 CSS px相当のリフロー等。二次元配置が必要な内容には例外がある。

**[U15] W3C WAI — Understanding 1.4.12 Text Spacing**

[WCAG 2.2解説](https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html)。行・段落・文字・語の間隔を利用者が変更した際の保持。本文デザインの一律指定値ではない。

**[U16] W3C WAI — Understanding 1.4.3 Contrast (Minimum)**

[WCAG 2.2解説](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)。通常文字4.5:1、大きな文字3:1等の区別と例外。

**[U17] W3C WAI — Understanding 1.4.5 Images of Text**

[WCAG 2.2解説](https://www.w3.org/WAI/WCAG22/Understanding/images-of-text.html)。文字画像と、ロゴ等の例外。

**[U18] W3C WAI — Understanding 2.5.3 Label in Name**

[WCAG 2.2解説](https://www.w3.org/WAI/WCAG22/Understanding/label-in-name.html)。視認ラベルとアクセシブルな名前の対応。

**[U19] W3C WAI — Understanding 3.3.1 Error Identification**

[WCAG 2.2解説](https://www.w3.org/WAI/WCAG22/Understanding/error-identification.html)。エラー箇所と内容を文字で識別。

**[U20] W3C WAI — Understanding 3.3.3 Error Suggestion**

[WCAG 2.2解説](https://www.w3.org/WAI/WCAG22/Understanding/error-suggestion.html)。判明している修正方法の提示。

**[U21] W3C WAI — Understanding 3.3.2 Labels or Instructions**

[WCAG 2.2解説](https://www.w3.org/WAI/WCAG22/Understanding/labels-or-instructions.html)。入力に必要なラベルと指示。

**[U22] W3C WAI — Understanding 2.5.8 Target Size (Minimum)**

[WCAG 2.2解説](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)。24×24 CSS px、間隔やインライン等の例外を含む。文字サイズとは別の評価。

**[U23] Alessi — イタリア語公式サイト**

[公式ページ](https://alessi.com/it)。取得できた価格・商品・操作の文言を観察。ログインや購入操作はしていない。

**[U24] Moleskine — イタリア向けイタリア語サイト**

[公式ページ](https://www.moleskine.com/it-it/)。取得できたキャンペーンとCTAの人称を観察。

**[U25] Cancelleria federale svizzera — Guida al linguaggio inclusivo di genere**

[公式案内ページ](https://www.bk.admin.ch/it/guida-al-linguaggio-inclusivo-di-genere)。機関ごとに言語方針があることの確認。案内ページの確認に限定し、リンク先全文の読了を意味しない。

### V 制作事例と書体 17件

**[V01] studio FM milano — Archive and the City**

[公式作品紹介](https://studiofmmilano.com/works/archive-the-city/)。2025年。展示壁・図解の公開画像を視認。図解の制作協力と書体のクレジットは公式説明を参照。

**[V02] studio FM milano — BOLD! Declinazioni tipografiche Campari: Munari, Depero e oltre**

[公式作品紹介](https://studiofmmilano.com/works/bold-declinazioni-tipografiche-campari-munari-depero-e-oltre/)。2024年。公開ポスターモックと関連画像を構成観察に使用。モック内の日付を正確な会期や設置証拠には使用しない。

**[V03] studio FM milano — Cassina Identity System**

[公式作品紹介](https://studiofmmilano.com/works/cassina-timeline/)。2014年。新旧ロゴ比較の視認と制作者の説明。

**[V04] Leftloft — The City of Lights / Euroluce 2023**

[公式作品紹介](https://leftloft.com/case-study/the-city-of-lights/)。2023年。主題画像と会場案内の写真。Giò Pastoriの紙の構成とDinamo Whyte Inktrapの使用は公式説明に基づく。

**[V05] Leftloft — Artefiera Bologna 2025**

[公式作品紹介](https://leftloft.com/case-study/artefiera-bologna-2025/)。2025年。ロゴとタイポグラフィの継続、会場・配布物・案内写真を確認。

**[V06] TassinariVetta — Casabella: 2024–2025 special / covers series**

[公式作品紹介](https://www.tassinarivetta.it/progetto/casabella-covers-series/)。2024〜2025年のシリーズ。953・954号の公開表紙を視認。制作説明の本文も確認した。[公式アーカイブ](https://www.tassinarivetta.it/archive/?category=publishing)にも当該シリーズの掲載を確認。

**[V07] Triennale Milano — PIET / LINE / NOSE is the studio òbelo tribute to Saul Steinberg**

[公式記事](https://triennale.org/en/magazine/piet-line-nose)。2022年2月3日公開。studio òbeloによる三冊のプロトタイプの公開画像を視認。画像クレジットは© studio òbelo。

**[V08] Leonardo Sonnoli — Artdust / Artissima 2015**

[制作者の公式掲載](https://www.sonnoli.com/)。2015年9月7日記事。Leonardo SonnoliとIrene Bacchiによるポスター群。静止画像を視認し、アニメーションの再生評価は実施していない。

**[V09] Pirelli HangarBicocca — Nan Goldin 展覧会イタリア語ガイド**

[公式PDF](https://web-assets-hangarbicocca.pirelli.com/wp-content/uploads/2023/12/Nan-Goldin-Guida-alla-mostra.pdf)。奥付2025年10月、グラフィックはStudio Sonnoli。先頭3ページを視認。URLの2023/12を制作年と解釈しない。

**[V10] Pirelli HangarBicocca — Museo per tutti アクセシブルガイド集**

[公式PDF](https://web-assets-hangarbicocca.pirelli.com/wp-content/uploads/2025/09/GUIDE-ACCESSIBILI-TUTTE-def_web.pdf)。奥付2025年9月、Studio Sonnoli。導入ページを視認。公開目的と組版の観察であり、全ページの認証・適合判定ではない。

**[V11] CAST — Fabbrica**

[書体の公式ページ](https://www.c-a-s-t.com/typefaces/fabbrica/)。Michele Patanè、2019〜2022年。書体構成と対応言語、tabular numbers、case sensitive forms等の公開見本を確認。フォントファイルを用いた試験は未実施。

**[V12] CAST — Licence Options**

[公式ライセンス案内](https://www.c-a-s-t.com/licences/)。Desktop・Web・Server・App等の用途別方式を確認。採用時は対象製品の契約本文を照合する。

**[V13] Collletttivo — Apfel Grotezk Family**

[書体の公式ページ](https://www.collletttivo.it/typefaces/apfel-grotezk)。Luigi Gorlero、2019年公開、2023年10月6日更新、表示版2.000。公開文字一覧と5スタイルの説明を確認。

**[V14] Collletttivo — Licensing**

[公式ライセンス案内](https://www.collletttivo.it/licensing)。OFLと同梱LICENSE.txtの存在を確認。無料配布と契約条件を分ける。

**[V15] Triennale Milano — 公式サイト**

[公式ページ](https://triennale.org/)。公開ナビゲーションの情報分類と言語入口を静的確認。全画面の描画・操作は未確認。

**[V16] MAXXI — 公式サイト**

[公式ページ](https://www.maxxi.art/)。公開テキスト、ナビゲーション、取得可能な画像代替情報を静的確認。代替テキストの適否や全画面の動作を断定しない。

**[V17] studio òbelo — 公式サイト**

[公式ページ](https://www.obelo.it/)。静的抽出では本文取得が限定的だった。これはサイトの可読性やSEOに問題があることの証拠ではない。

### P 歴史・出版・商業サイトの補助資料 9件

**[P01] Salone del Mobile.Milano — Manifesti**

[公式アーカイブ](https://www.salonemilano.it/it/manifesti)。1961年以降の歴史的ポスターへの入口。

**[P02] Salone del Mobile.Milano — A Matter of Salone, 2026年の広告キャンペーン**

[公式記事](https://www.salonemilano.it/it/articoli/a-matter-of-salone-campagna-comunicazione-2026)。2025年12月19日公開、Motel409によるコンセプト。公開された主題画像を視認。

**[P03] Salone del Mobile.Milano — 1994年のポスター**

[公式PDF](https://www.salonemilano.it/sites/default/files/2021-07-22/1994.pdf)。公式アーカイブの年次から特定。色・文字の大小・配置を視認。画像だけから制作者や書体を特定しない。

**[P04] Corraini — Inventario 07**

[公式刊行物ページ](https://corraini.com/products/inventario-07)。2013年、編集Beppe Finessi、グラフィックDesignwork、伊英。公開見開き画像を視認。

**[P05] Falcinelli & Co. — Chi siamo**

[スタジオ公式](https://falcinelliand.co/chi-siamo/)。出版物の設計とスタジオの説明を本文確認。サイト全体の視覚・操作評価ではない。

**[P06] Cassina — イタリア語公式トップページ**

[公式ページ](https://www.cassina.com/it/it.html)。取得時点の大文字見出し、英語のコレクション名、CTA等のテキストを確認。

**[P07] Riccardo Falcinelli — Fare i libri / minimum fax**

[出版社の書籍ページ](https://www.minimumfax.com/shop/product/fare-i-libri-1472)と[公開試し読みPDF](https://www.minimumfax.com/web/content/book/3959/preview_file/fare-i-libri-1472.pdf)。2011年。読者・出版社・シリーズの設計に関する本文を確認。公開範囲のみ参照。

**[P08] Cassina — Products and collections**

[イタリア語公式ページ](https://www.cassina.com/it/it/products-and-collections.html)。探索・相談・ダウンロード・登録等の操作名をテキスト確認。

**[P09] Salone del Mobile.Milano — 1961年のポスター**

[公式PDF](https://www.salonemilano.it/sites/default/files/2021-07-21/Manifesto_1961_0.pdf)。図像、配色、イベント情報の配置を視認。

### T 文字データの補助仕様 2件

**[T01] Unicode — Unicode Standard Annex #15: Unicode Normalization Forms**

[公式仕様](https://www.unicode.org/reports/tr15/)。正規化の形式と等価性。署名済みデータ等の書換え許可を与える仕様ではない。

**[T02] Unicode — Unicode Standard Annex #29: Unicode Text Segmentation**

[公式仕様](https://www.unicode.org/reports/tr29/)。書記素クラスタ等の境界。コードポイント数と見かけの文字数を区別する。

### O 本調査の限定実測 1件

**[O01] Intl.NumberFormat / Intl.DateTimeFormatの実行記録**

実行時刻2026年10月18日21:05 UTC。Node.js v24.19.0、ICU 78.3、CLDR 48.0。it-ITとit-CH、数値1234.56・12345.67、通貨EUR・CHF、割合0.125を使用した。一般数値は既定オプション、通貨はstyleとcurrency指定、割合はstyle:percentとmaximumFractionDigits:1を指定した。日付入力2026-10-19T12:00:00Z、dateStyle:long、timeZone:Europe/Rome。結果は第06章に掲載した。

再現用コードは以下のとおり。実行結果の一致には同じ環境とオプションを用いる。

```js
for (const locale of ['it-IT', 'it-CH']) {
  const currency = locale === 'it-IT' ? 'EUR' : 'CHF';
  const number = new Intl.NumberFormat(locale);
  const money = new Intl.NumberFormat(locale, {
    style: 'currency', currency
  });
  const percent = new Intl.NumberFormat(locale, {
    style: 'percent', maximumFractionDigits: 1
  });
  const date = new Intl.DateTimeFormat(locale, {
    dateStyle: 'long', timeZone: 'Europe/Rome'
  });
  console.log(locale, number.format(1234.56),
    number.format(12345.67), money.format(12345.67),
    percent.format(0.125),
    date.format(new Date('2026-10-19T12:00:00Z')));
}
```
