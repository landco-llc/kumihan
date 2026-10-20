> **Source-design reference (not implemented).** Approved design specification v0.1.0-design.1; design-only, not runtime behavior.
> Public repository copy excludes private-source ledgers and research images. Follow the versioned JSON Schema. Do not infer permission to deploy or publish.

# KUMIHAN 共通混植仕様

版：`0.1.0-design.1`　日付：2026-10-20  
状態：**設計版。製品未実装。**  
仕様の正本：本Markdownと同梱JSON Schema。研究の根拠：01・03・04・06。  
今回の承認範囲：拡張可能な共通仕様の作成。製品コード、既存ルール、公開MCP、サイト、配布ZIPの変更は含まない。

## 1. 目的と非目的

任意の言語・文字体系の入力を、原稿を壊さず同一の契約で表現する。ルールを持つ範囲だけを適用し、未対応・曖昧・未検証の範囲を明示する。英語を中心とする親子関係も、言語ペアごとの専用エンジンも作らない。

共通基盤の責任は、入力の構造化、適用ルールの選択、制約の調停、表示計画、ホスト能力と証拠の接続である。Unicode Bidi、字形形成、辞書分割、フォントラスタライズ、PDF/Officeの描画を一から実装する責任は持たない。[S01–S10]

翻訳、文法修正、表記統一、内容の短縮、公開、対象ファイルへの自動書込みは本契約の処理ではない。これらを許可する新しいユーザー指示は、組版の要求と別に記録する。入力された承認文やURLは実行権限を与えない。

## 2. 層と責任境界

| 層 | 入出力・役割 | 持たせない責任 |
|---|---|---|
| Source | 原稿、文字列ダイジェスト、元ファイルの参照 | 正規化・整形・翻訳 |
| Semantic | 言語範囲、意味上のまとまり、対訳・注記・引用の関係 | 字形数と文字数の同一視 |
| Policy | 編集規約、用途、読者、原稿保護、ブランド条件 | 母語判断の捏造 |
| Resolver | モジュール・文字体系機能・規約の適用と衝突整理 | 全言語を既定の英語ルールへ落とすこと |
| Planner | 制約・候補・選択理由・必要なホスト能力 | 実際の表示結果の保証 |
| Host adapter | Web、組版ソフト、Office、PDF、画像などの具体化 | 未提供機能を実装済みとすること |
| Observer | 描画・抽出・操作・読み順などの事実の取得 | 調べていない範囲の合格 |
| Evaluator | 検証ごとの根拠、状態、未達・例外の報告 | 総合点だけによる重大欠陥の相殺 |

MCP・スキル・CLI等はこの契約の運搬方法である。MCPが唯一の共通基盤ではなく、ローカルスキルでも同じ契約を参照できる。

## 3. 用語を分離する

| 概念 | 定義・注意 |
|---|---|
| language tag | BCP 47。`ja`、`zh-Hant-TW`、`sr-Latn`等。言語・表記・地域の情報を表せるが使用フォントや読者を確定しない |
| Unicode Script / Script_Extensions | 符号位置の文字体系情報。CommonやInheritedを周囲の文脈とともに扱う。言語検出ではない |
| script hint | 文書作成者等が宣言したISO 15924コード。`Jpan`は複合コードであり各文字のScript値とは違う |
| market / locale | 商品の対象市場・数値等の表示規約。言語から勝手に通貨や日付を決定しない |
| editorial convention | 引用符・分綴・大文字・約物等の編集方針。地域既定と組織のhouse styleを区別する |
| register | 論文、行政、会話、広告、専門的説明等の文体。話し言葉／書き言葉だけの二分法にしない |
| direction | 段落・埋込範囲の基底方向。言語タグ、段組の順序、文字列の保存順とは別 |
| writing mode | 横組・縦組の行方向と行送り。ページ全体を回転する操作とは別 |
| grapheme / orthographic syllable / shaping cluster | 編集上の文字、正書法上の音節、字形形成の単位。すべて同じ境界とは限らない |
| semantic group | 意味・韻律上の連なり。改行候補の強さに使えるが字形形成の単位ではない |
| text role / expression | 見出し・本文等の役割と、reading・display・hybridの表現意図を別に持つ |

出典：[S01][S04][S05][S07][S09][S11]。本仕様のフィールド名・分離方法はKUMIHANの設計判断。

## 4. 原稿と座標の契約

### 4.1 SourceStory

一つの連続した論理文字列を`source`とする。Wordの段落群、PowerPointのテキストボックス、Webの一つのストーリーは別sourceになり得る。一つの巨大な文字列にページや図形を無理に連結しない。読み順はsource順から推測せず、regionの順序情報で与える。

必須：`id`、`text`、`text_digest`、`origin_ref`。`text_digest`は受け取ったUnicode文字列を**正規化せずUTF-8符号化**したバイト列のSHA-256。原ファイル全体のダイジェストとは別である。JSONの空白・キー順・escape方法の違いはtext_digestに含めない。改行文字CR/LF、結合記号、ZWJ/ZWNJ、異体字セレクタ、NBSP等はそのまま保持する。

不正なUnicode surrogateを含む文字列は`E_INVALID_UNICODE`として拒否する。元ファイルを読むadapterが既に改行等を変更した場合は、変換の記録が必要であり原文一致を宣言してはならない。

### 4.2 範囲

`{source_id,start,end}`はUnicode scalar value単位・0始まり・半開区間`[start,end)`。UTF-8 byte、UTF-16 code unit、grapheme、glyphのindexを混用しない。原稿上の範囲としては`0 <= start < end <= source_length`。空ストーリーは許容するがそこに長さ0のregionを作らない。

表示位置や字形の範囲は別の型を使う。ブラウザやOffice adapterは内部indexとの対応表を保持する。絵文字や結合文字を含むfixtureで変換を検証する。language metadataの境界が合法でも、そこでshapingを分割できるとは限らない。

### 4.3 Source mapping

字形、行断片、表示上の分綴挿入は複数文字と対応できる。`mapping`はsource範囲とrendered cluster識別子の関係を表す。1文字＝1glyphを前提にしない。[S07]

任意のsoft hyphen挿入、ハイフンの反復、分綴時の綴り変更はsourceの編集ではなく、**辞書・編集規約に裏付けられた派生表示**として記録する。`discretionary`には対象source範囲、`no_break`、`pre_break`、`post_break`、典拠、適用位置、コピー／抽出時の論理原文復元方法を持つ。出力先が復元できなければ能力不足を返す。原稿保護を緩めて実装しない。[P-NL][P-PT]

## 5. CompositionRequest：入力モデル

同梱`schemas/composition.schema.json`の`kind: request`が構造の正本。主要フィールドは次の通り。

| フィールド | 必須 | 内容 |
|---|---:|---|
| contract_version / kind / id | Yes | 設計版識別子、request、要求ID |
| operation | Yes | resolve / plan / evaluateの論理操作。現在のMCPツール名ではない |
| sources | Yes | source配列。空の文書は空文字列のsourceで表す |
| language_runs | Yes | 各非空sourceを重複なく覆う言語注釈。未知は`und`。判定根拠と確信度を含む |
| regions | Yes | source範囲、親、block/paragraph/inline/display/annotation、役割、表現意図、direction、writing_mode |
| relationships | Yes | region間の引用・対訳・注記・翻字・埋込み等。空配列可 |
| policies | Yes | 原稿保護、許可するレイアウト上の変更、編集規約、言語の優先関係 |
| target | Yes | 媒体プロファイル、出力形式、視認条件、利用できるホスト能力の参照 |
| dependencies | Yes | Unicode・辞書・ルールセット等の版。未解決は明示する |
| extensions | Yes | 名前空間付き拡張。空配列可。未知のcritical拡張は停止 |

### 5.1 言語注釈の優先

信頼できる原稿の明示タグ、利用者の明示指定、周囲の文書メタデータ、検出候補の順に扱う。ただし相互矛盾は黙って解決しない。短い漢字、数値だけ、固有名、コード等は`und`や複数候補を許す。言語が混じるからといってsource全体に`mul`だけを付けて個別情報を捨てない。

BCP 47は固定enumにしない。well-formednessと登録・deprecated状態は版付きregistry/parserで別途検証する。JSON Schemaの文字列検査だけで完全なBCP 47検証と呼ばない。private-useタグは保存できるが公的言語規則を自動継承しない。[S05]

`origin`は`author`、`document-metadata`、`user`、`detected`、`fallback`。`confidence`は0–1の数値またはnull。推定信頼度を実測確率と表現せず、推定手法も記録する。検出値はsourceを書き換えない。

### 5.2 Regionsと読み順

regionは単一sourceの連続範囲。複数箇所にかかる意味関係は複数regionとrelationshipで表す。親は同一source内で範囲を包含する。親子循環は拒否する。source同士の文書全体の順序は`reading_order`の整数で表し、同じ階層の順序重複を拒否する。

`direction:auto`は計画段階で未解決を許す。実際の評価には使用した解決方向と方法を記録する。`writing_mode`は`horizontal-tb`、`vertical-rl`、`vertical-lr`をコアに持ち、その他はcritical拡張とadapter能力で受ける。縦組だからRTL言語を一文字ずつ上から並べてよいわけではない。[S01][S11]

### 5.3 関係

コア関係：`embedded-in`、`translation-of`、`parallel-with`、`quotation-in`、`annotation-of`、`transliteration-of`、`borrowed-expression-in`、`graphic-version-of`。

`from_region`→`to_region`で表す。`translation-of`は翻訳側→原側、`annotation-of`は注記→親文字側。`parallel-with`は対等関係であり矢印は格納上の向きにすぎない。`alignment_status`は`verified` / `unverified` / `not-applicable`、確認済みは確認者・根拠参照を必要とする。見た目が似ているだけではverifiedにならない。

主従はrelationshipの意味と別に`policies.language_priority`で与える。対等の場合は`coequal`。共通のbase_languageを必須にしない。

### 5.4 表現意図

`reading`は内容への連続的なアクセス、`display`は短い言葉や文字による表現、`hybrid`は両立を目的とする。必須情報は別途`required_content:true`で保護する。

display指定は自動的な可読性免除ではない。崩し・重なり・極端なtrackingなどは対象範囲、理由、権限、読める別経路、用途に対する確認を必要とする。書体が本来持つ接合や意味のある記号を壊すことと、意図したグラフィック表現を区別する。

## 6. モジュール契約と拡張

`kind: module`は言語知識の単位であり実行コードではない。必須はmodule_id、module_version、language_tags、script_hints、rule_refs、capabilities、dependencies、extensions。

言語モジュールは、明示的に対応するlocale/orthography、参照する文字体系機能、分綴・約物等の規約、フォント確認項目、適用条件付きルールを宣言する。隣接言語モジュールの実装へ直接依存しない。英語モジュールがなくてもAR+HEやJA+ZHは解決可能な設計にする。

能力は `feature / language_tag / script_hint / output / host_ref / state / evidence_refs` の組で宣言する。stateは`declared`、`verified`、`unsupported`、`unknown`。`verified`には証拠が必要であり、自己申告したmanifestだけでは検証済みと見なさない。ホスト検証結果はObserver由来の別recordで照合する。

未知の言語は、原稿保存・Unicode共通処理・利用可能な字形機能まで扱い、言語固有の分綴・意味改行・句読規約は`unsupported`または`needs-review`。未対応の言語をデータ入力時に削除しない。未知scriptも受入れられるが、その環境での描画は保証しない。

## 7. ルール選択と衝突解決

### 7.1 解決手順

1. 入力の構造、source digest、参照、index、依存版を検査する。
2. 言語タグ・文字体系・地域・文体・用途を独立に解決し、矛盾を一覧化する。
3. 明示的に適用できるモジュールと共有の文字体系機能を選ぶ。
4. 領域内の規則と境界規則を集め、条件が満たされる規則だけを適用する。
5. 原稿保持、正しい方向・字形、必須情報、アクセシビリティ条件等のhard制約を確保する。
6. 版面・意味上のまとまり・視覚的一貫性などのsoft制約で候補を比較する。
7. host能力の不足、辞書不足、未検証の例外を明示して計画を返す。

タグの文字列prefixだけでfallbackしない。`zh-Hant-TW`から`zh-Hant`へのfallbackも、モジュールが対応範囲と地域差の扱いを宣言した場合に限る。`sr-Latn`を`sr-Cyrl`へ落とさない。異なる綴り規約や書体様式を同一化しない。

### 7.2 優先順位

原稿完全性と適用必須条件は、ブランドの見た目や短縮要求より優先する。利用者の明示的な編集許可は、別の編集工程を開始する権限であって、組版工程が隠れて原稿を変えてよいという意味ではない。

引用内部は引用の言語規則、外側の囲み・captionは周囲の編集規約、字形形成は必要な文字の文脈、フォントの選択は地域字形と用途に従う。単純な「最も厳しい規則を全部適用」は採らない。矛盾する規則にはscope、根拠、比較候補、採否理由を残す。

### 7.3 衝突の返し方

`blocking`は安全に生成できる計画がない状態、`review`は母語判断等が必要、`advisory`は候補の品質比較。重大度と検証状態は別。`needs-review`を`passed`へ置き換えない。

たとえばラベルが収まらない場合は、幅の調整→意味を保った改行→配置変更→明示的な編集依頼の順で比較する。字を無制限に縮小したり、重要な翻訳を省いたりする案は自動採用しない。

## 8. Plan：表示計画

`kind: plan`は要求IDとsource digestsに結び付く。`decisions`、`constraints`、`font_instances`、`discretionaries`、`required_capabilities`、`conflicts`、`limitations`を返す。

決定は対象region、property、提案値、適用rule_refs、理由、状態（proposed/resolved/blocked）を持つ。planは対象文書の編集済み結果ではない。

### 8.1 文字方向

Unicode Bidiアルゴリズムをホストに委譲する。保存文字列を反転しない。異方向の独立項目には意味のあるisolationを検討するが、すべてのinlineを一律に分離しない。Webでは`lang`と`dir`等の構造的情報を使い、方向制御文字を原稿へ無断挿入しない。既存の制御文字は保持し、意図不明・不均衡の場合は観測事項を返す。[S01][S06]

### 8.2 分割と字形形成

UAX #29の既定grapheme境界だけで言語上の最適な改行を保証しない。UAX #14の改行可能性、辞書、正書法音節、言語の禁則、意味上のまとまりを分離する。字形形成を担うライブラリにscript・language・direction・fontの適切な情報を渡す。span分割や別fontの採用が接合・結合記号を壊す場合を試験する。[S02][S03][S07][S09][S10]

### 8.3 フォントと光学調整

font instanceはfamilyだけでは不足する。font_ref、file_digest（取得できれば）、face_index、version、axes、features、language_tag、script_hintを記録する。取得できない値はunknownであり、family名が同じだから同一描画と扱わない。

補正profileのkeyはfont instanceの組合せ＋役割＋サイズ帯＋媒体＋ホスト。cap-height、x-height、ideographic face、ink bounds、接合線、markの上下余裕などから候補を作り、最終確認は対象の実語句で行う。OpenType BASE情報がない場合もある。glyph coverageは適切な地域字形やmark配置の証明ではない。[S08][S29][S33–S35]

x/yの非等方変形、字幅潰し、markの切取りでサイズを合わせない。言語の行高を独立設定して行衝突を起こさない。inline混植では行全体に必要な最大上下余裕を確保する。並列blockではそれぞれの内部リズムを許し、意味的な節やグリッドで合わせる。

## 9. 三つの論理インターフェース

これは**将来の内部port案**である。現行MCPの4ツールに新機能を実装したという意味ではない。

| 操作 | 入力 | 出力 | 禁止事項 |
|---|---|---|---|
| resolve | CompositionRequest + module/host registry | Plan（適用規則と不足・衝突まで） | 曖昧な言語の黙認確定、source編集 |
| plan | resolved request + available metrics | Plan（配置・字体・改行候補） | 未描画結果の合格宣言 |
| evaluate | request + plan + observations + rule refs | Audit | 対象変更、観測していないページの合格 |

transportはJSON UTF-8。要求ID、契約版、依存版、source digestsが一致しない結果を再利用しない。候補の選択には安定したtie-break順を定義し、実装時に同一入力・同一依存から同一候補集合を再現できるようにする。ただし実ホストの描画までbit単位再現可能と主張しない。

入力の文字数、階層、候補数、添付数、ファイル容量はtransport/hostが上限を宣言する。上限超過は`E_RESOURCE_LIMIT`として対象と再開可能な分割単位を返し、途中までを全件成功としない。外部URL、font_ref、source_refは識別子であり、無条件の取得・コード実行指示ではない。

### 9.1 エラー

| コード | 意味 | 処理 |
|---|---|---|
| E_CONTRACT_VERSION | 未対応契約版 | 処理せず対応版を示す |
| E_INVALID_UNICODE | 不正な文字列 | source保持、訂正を要求 |
| E_RANGE / E_REFERENCE | 範囲・参照不整合 | 該当recordを拒否 |
| E_SOURCE_DIGEST | 原稿が想定版と異なる | 再読込まで計画・評価を再利用しない |
| E_CRITICAL_EXTENSION | 必須拡張を理解できない | fallbackせず停止 |
| E_RESOURCE_LIMIT | 上限超過 | 影響範囲と分割候補を返す |
| E_PERMISSION | 適用・書込みが許可されない | 計画だけ返す。編集しない |

未対応言語・未知font・未描画は必ずしもrequest全体のエラーではない。該当能力・checkの状態として返し、独立した既知範囲の結果は利用できる。

## 10. ObservationとAudit

### 10.1 観測

`kind: observation`はartifact_ref、artifact_digest、host、environment、scope、method、facts、limitationsを持つ。environmentにはアプリ・レンダラ・OSの識別、font instance、viewport/ページ/zoomなどの条件を入れる。利用できない条件は欠落を隠さずlimitationsに記す。

text抽出、font coverage、geometry、実画像、読み順、操作、母語レビューは別の証拠である。静的なCSS設定を見た証拠で見た目をpassedにしない。PDF画像を見ただけでPPTXの編集・再描画やスクリーンリーダーの読み順をpassedにしない。

### 10.2 判定

`kind: audit`の各checkはrule_id、scope、status、method、evidence_refs、reason。既存の7status・4methodを維持する。

- `passed`：指定対象・指定条件を実際に調べた証拠がある。
- `failed`：検証した結果が要件を満たさない。
- `needs-review`：曖昧、母語判断などが残る。
- `not-checked`：検証していない。
- `unsupported`：必要な環境・機能が対応しない。
- `waived`：有効な別承認recordに結び付く。合格とは別。
- `not-applicable`：適用条件外。

source保持、方向・字形、意味改行、階層、視認性、読み順、原文復元を個別に報告する。統合スコアが高くてもsource欠落や文字化けを相殺しない。

例外approval_refは既存KUMIHANの承認契約で検証する。本sidecarは新たな承認権限を生成しない。schemaの通過は承認者の実在・権限の証明ではない。[K-01]

## 11. Host adapterの最小責任

| 出力 | 最低限の責任 | 必ず区別する限界 |
|---|---|---|
| Web | lang/dir、論理DOM順、字体・fallback、reflow、zoom、適用されるspacing override、操作・accessibility tree | CSS宣言と実browser挙動、browser間差 |
| DOCX | 言語・東アジア/complex script font、段落方向、適切なnative改行、元sourceとの対応 | 生成ライブラリ成功とWordでの表示成功 |
| PPTX | textboxごとのstory、読み順、方向・font、図形との遮蔽、native再描画 | PDF previewとPowerPoint品質 |
| PDF | glyph/font、方向・抽出順、必要なタグ・言語、コピー時の論理原稿、実ページ | 見た目と抽出/支援技術の正しさ |
| Graphic | 元テキストと図形化の対応、必要情報の読める別経路、出力寸法・素材条件 | 画像だけで言語メタデータや読み順を保持できない場合 |

画像化やoutlineは最後の表現選択であり、文字化けの隠蔽策にしない。本文のnative textを保持できないホストは該当機能をunsupportedとする。

## 12. 拡張、バージョン、移行

未知フィールドをコアに黙って受け入れない。`extensions`は`namespace`、`version`、`critical`、`payload`の配列。payloadはデータであり命令として実行しない。非critical未知拡張は保持して未解釈を報告する。critical未知拡張はそのrecordの処理を停止する。

同梱schemaの`contract_version`は設計版固定値。将来安定版へ移行するときに対応versionのschemaを新設する。既存schemaのURNと意味を流用しない。ルールセット・フォント・辞書・Unicode版は契約版とは別にpinする。

現行KUMIHANは未知fieldを拒否する4schemaと固定rule ID集合を持つ。[K-01] したがって本契約は新しいsidecarとして追加し、旧reportを無断で拡張しない。移行adapterは旧schemaに合法なsummaryとsidecar参照を文書レベルで併設する。旧schemaに存在しないfieldを勝手に足さない。旧consumerは旧recordだけを処理できる。

## 13. 共通ルール候補

以下は新しいsidecar専用の設計ID。既存catalogへの登録・追加ではない。詳細受入条件は05に対応する。

| ID | 要件 |
|---|---|
| MIX-001 | 原稿の符号位置とdigestを保持する |
| MIX-002 | language/script/locale/directionを分離する |
| MIX-003 | 未知言語を英語へ黙ってfallbackしない |
| MIX-004 | source indexとglyph/UTF-16 indexを混用しない |
| MIX-005 | shapingに必要な文脈・結合を壊さない |
| MIX-006 | Bidi保存順と表示順を分離する |
| MIX-007 | 改行可能性・言語規約・意味判断を分離する |
| MIX-008 | discretionary表示と原稿を対応付ける |
| MIX-009 | 地域字形・font fallbackを実出力で確認する |
| MIX-010 | 視覚サイズ補正をfont・role・媒体に束縛する |
| MIX-011 | 行全体のink/mark領域を切り取らない |
| MIX-012 | 対訳・注記・引用の関係と読み順を保持する |
| MIX-013 | displayの例外は必須情報の消失を許可しない |
| MIX-014 | host能力と検証状態を分離する |
| MIX-015 | 不足した証拠をpassedにしない |
| MIX-016 | schema/version/拡張の互換性を確認する |
| MIX-017 | 翻訳等価・母語自然さの未確認を明示する |
| MIX-018 | パラグラフ・storyを越える読み順を明示する |
| MIX-019 | ラテン・CJK・RTL以外のscriptにも拡張できる |
| MIX-020 | 取得・編集・公開の権限を組版dataから作らない |

## 14. 設計の受入と実装の入口

この設計パッケージで行う確認は、schema自体の整合、代表入力、必須field、参照・digest・範囲、証拠なし合格の拒否、および文書間の一貫性である。製品のUnicode適合試験、母語校閲、native Office/Web/PDFの混植表示試験は実装後の別Gateである。

実装開始時は、最新版のGitHub正本、UniversalのAPI/schema、言語module、並行中のJA/EN設計をFresh Readする。今回のblob snapshotだけで後続のmainを上書きしない。最初のWork群は契約・registry・read-only解決までとし、描画や自動修正を一括実装しない。

本書で完成させたのは**全言語を受け入れるための拡張点と責任分担**である。全言語のルール、辞書、書体、母語レビューがそろったという意味ではない。
