# 日本語 v0.2.0 — 30ケースの実装用対照表

研究原本: `KUMIHAN_JA_Validation_Cases_20261020.json`。
SHA-256: `630ac9bee505cbbf73e476a6b696a67f38d922667ca51e0578c19a33e6d7dced`。

**全ケースは研究時点でnot-run。以下は期待条件であって、観測結果ではない。**
原本JSONと詳述版は実行用ZIPの `research/` に同梱。本表はrepoだけでも対照fixtureを設計できる要約である。規則の現行条件はcatalogを参照する。`passed` は列挙した観察を実施して満たしたscopeだけに用いる。

## 共通原稿

文字列をNFC/NFKC等で正規化しない。Aの末尾はU+304B（か）とU+3099（結合濁点）であり、合成済み「が」ではない。fixture出力で追加するlayout上の折り返しは、原稿文字列とは分けて保持する。

| キー | 原稿 |
| --- | --- |
| A | 髙﨑さま／料金１,２００円／が |
| B | 日本語：骨／繁體中文：骨 |
| C | 2026年度・特別会員向けオンライン講座の受講登録を取り消す |
| D | いつものAIツールからはじめよう |
| E | 文字の庭／2026年11月3日／文字の広場（架空会場） |
| F | 処理済み 48件 |
| G | この書体なら全員の読解力が20%向上します。 |
| H | 申込条件を確認してください。〔改行〕Please read the application requirements. |
| I | 本文は読み手の設定によって表示が変わります。 |
| J | 日本語の報告書本文と注記 |
| K | 縦書きの短い頁が下へ続く記事 |
| L | 登録内容を確認する |
| M | 文字と余白の時間 |
| N | 文字と余白の時間／道具の使い方を本文で説明します。 |
| O | 会場で共有する手順と注意事項 |
| P | 手順3の前に電源を切ってください。 |
| Q | 出口 EXIT |
| R | 項目A 120件／条件：対象は申請済みの記録です。 |
| S | 報告本文と集計表 |
| T | 静的な本文のみを持つ記事領域です。 |
| U | 明日、こっちは17時で閉めます。 |

Hの〔改行〕は説明記号であり原稿へ入れない。実fixtureではU+000A一文字とする。会場名・件数・効果数値は合成テスト用であり、実在・実績を主張しない。

## 条件と期待するscope別結果

略号はmethodのみ: S=`static`、R=`rendered`、A=`assisted`、M=`manual`。結果は現行7 statusをそのまま使う。対照の不適切な報告や出力を実データの結果と混ぜない。

| Case / 優先 / 原稿 | fixtureの条件 | 条件を観察した場合の期待結果 | 避ける誤判定 |
| --- | --- | --- | --- |
| PV-001 / P0 / A | 対応extractorによる原稿一致だけを確認し、font/字形は未観察 | CONTENT-001 S passed（文字列scope）; WEB-007 R not-checked（字形scope） | static一致を実表示全体のpassedへ昇格 |
| PV-002 / P0 / A | 無断NFKC等で全角数字・分解表記が変化した負例 | CONTENT-001 S failed; CONTENT-004 S failed。処理と保護範囲のコードポイント差を示す | 正規化後一致を保全の証拠にする |
| PV-003 / P0 / B | family名と言語指定のみ。地域字形参照・実画像なし | JA-TYPE-001 R not-checked; WEB-007 R not-checked | CJK名や豆腐なしだけで適切な地域字形と断定 |
| PV-004 / P1 / B | ja/zh-Hant-TWのrun、許諾された字形参照、実font、実画像を照合 | JA-TYPE-001 R passed; WEB-007 R passed。ただし観察したrun・正常読込条件だけ | 「骨」に必ず同じ地域差があると仮定、全fallbackへ一般化 |
| PV-005 / P0 / C | 幅320 CSS px相当の実状態で全文nowrapとclipが末尾・操作を失わせる | WEB-005 R failed; WEB-004 R failed; JA-TYPE-003 R failed | 一行を守ることを優先して情報・操作喪失を無視 |
| PV-006 / P0 / C | PV-005と同じfont・viewport。複数行にして全文・操作を保持 | WEB-005 R passed; JA-TYPE-004 A passed（実改行の意味を別確認） | 二行ボタンを形式だけで失敗にする |
| PV-007 / P1 / D | 実font・幅で自然に一行。固定二行の意図なし | JA-TYPE-011 A passed。通常表示の妥当性と意図的改行不要を確認 | 文節境界があるだけでbrを入れる |
| PV-008 / P0 / D | 文節解析のみ。幅・font・行マップ・画像なし | JA-TYPE-004 A needs-review; JA-TYPE-011 A not-checked | 文節解析を見出し品質の自動正解とする |
| PV-009 / P1 / D | 行マップ「いつものAIツールか／ら／はじめよう」。禁則文字なしを確認 | JA-TYPE-002 R passed; JA-TYPE-004 A needs-review; JA-TYPE-011 A needs-review | 不自然な意味改行をすべて禁則違反とする |
| PV-010 / P0 / E | 造形領域だけ編集可。断裁した装飾とは別に題名・日時・会場を同一面へ完全表示 | CONTENT-001 S passed（保護field一致）; DESIGN-003 A passed（実際に情報へ到達）; JA-TYPE-009 M not-applicableは造形領域への本文行長小確認のみ | 装飾の断裁だけで全体失敗、または同文があるだけで全条件合格 |
| PV-011 / P0 / E | DOM文字列は一致。日時・会場がclipされ、利用可能な代替経路なし | CONTENT-001 S passed; WEB-004 R failed; DESIGN-003 A failed | HTML内存在を可視性の証拠にする |
| PV-012 / P0 / E | 正本11月3日に対し一箇所だけ11月4日。別箇所は正しい | CONTENT-001 S failed（全保護fieldの整合） | 正しい再提示が一つあるため不一致を許容 |
| PV-013 / P0 / E | 題名とQRだけの掲示。外部詳細ページの利用条件・通信・端末未確定 | DESIGN-003 A needs-review; EVIDENCE-001 S passedは未実施を正しく報告したscopeだけ | URLがあるだけで読者の到達を合格にする |
| PV-014 / P1 / F | value48px、label14px、page title24px等。値を主役にしlabelとの関連が読める | DESIGN-005 R passedは役割・実表示の整合を確認した場合。数値比率自体は最適値ではない | valueがheadingより大きいだけで階層逆転エラー |
| PV-015 / P2 / G | 根拠はメーカー説明または限定的選好調査だけ。全員・読解力・20%の裏付けなし | CONTENT-002 A failed（主張と供給資料の不一致） | 好みを速度・正確さ・理解の全性能へ読み替え |
| PV-016 / P1 / H | 和文段落と英語runに、適用条件に沿った利用者spacing上書きを実施 | WEB-003 R passedは変更後の内容・機能を確認した範囲だけ | 日本語ページなので英語run・段落余白も一括除外 |
| PV-017 / P0 / I | 初期letter-spacing:0.12emだけ。変更試験は未実施なのに合格とした負例報告 | WEB-003 R not-checked; EVIDENCE-001 S failed（不実な報告との照合） | WCAGが作者に初期0.12emを義務付けたと説明 |
| PV-018 / P0 / J | PDFのみ、HTMLなし。全頁実表示・抽出は未実施 | WEB-003 M not-applicable（同一Web上書き試験）; DOC-004 R not-checked | Web試験N/AをPDF品質合格に変える |
| PV-019 / P1 / K | writing-modeはvertical-rlでも、頁は下へ積まれ実scroll軸は縦 | WEB-001 R passedは縦scrollに対応する幅条件で再配置・操作を確認後 | 縦書きだから高さ256pxだけを自動選択 |
| PV-020 / P0 / L | DevTools等のCSS模擬だけ。native text zoom200%確認済みとした負例報告 | WEB-002 R not-checked（利用者の実拡大機構）; EVIDENCE-001 S failed（方式の誤称） | CSS模擬をnativeへ昇格。逆にnative text zoomだけが許容方式とも断定しない |
| PV-021 / P0 / M | CSS.supportsのみ。実font、OpenType支持、表示比較なし | JA-TYPE-006 R not-checked; WEB-007 R not-checked | 構文受理をfont機能の支持・効果と混同 |
| PV-022 / P1 / N | 実在・利用可能なfontで機能支持を確認。display任意variantを比較しbodyへcascadeさせない | JA-TYPE-005 R passed; JA-TYPE-006 R passed。当該font・役割・条件のみ | displayの全本文適用、または本文paltの文脈なし自動失敗 |
| PV-023 / P0 / O | 主要本文24ptとslide寸法だけ。投影面・最遠席・環境未定 | DOC-003 R not-checked（実会場scope） | 24pt以上だから会場で必ず読めると保証 |
| PV-024 / P1 / P | 投影寸法・最遠席を定め、必須注意書きが読めない負例。全文はspeaker notesだけで聴衆への経路なし | DOC-003 R failedは所定条件で読めないと確認した場合 | 発表者notes内の文字を聴衆への情報到達とみなす |
| PV-025 / P1 / Q | 合成projectは参照M19の10m和文40mm目安を採用。ボディ40mmだが「木」の実高32mm | JA-TYPE-009 R failedは採用した測定量・目安との不一致。法的最低基準違反とは呼ばない | 仮想ボディと実字面高を同一の量として比較 |
| PV-026 / P1 / Q | 同じ採用条件で「木」実高40mm以上、「E」30mm以上を測定。10mは仮定、現場は未観察 | JA-TYPE-009 R passedは実字面寸法の照合のみ; DESIGN-005 R not-checked（現場の読者課題） | 寸法表から全員・全現場の利用性能を保証 |
| PV-027 / P1 / R | 1ページ有効高を超える行へkeepを強制し、注記・末尾セルをclipさせる負例 | DOC-002 R failed（実表示した表・注の内容と対応） | 分割しなかったことだけで文書品質合格 |
| PV-028 / P0 / S | 全頁PDF previewは確認。native Officeを実行できない環境であると確認済み | DOC-004 R passedはPDF preview scope; DOC-004 R unsupportedはnative scope。単なる未着手ならnot-checked | 別rendererのpreviewをnative Office確認済みと呼ぶ |
| PV-029 / P0 / T | 対象regionにlink/input/button/動的操作なし。browser UIは対象外 | WEB-008 M not-applicableは当該regionの操作状態だけ | error/loading/disabled画面を捏造・要求する |
| PV-030 / P2 / U | 発話日・店舗・引用保持の要否が未確定。対照に日時等が明確な長文を用意 | CONTENT-001 S passedはレビューが原稿を変えず保全した場合のみ。文脈不足の助言は別記 | 日時・店舗を推測補完、または短文だけを分かりやすいと判定 |

## 実行記録の最低項目

ケースごとにcaseId、実fixtureのpathとdigest、対象region、保護原稿、profile、fontとrenderer、viewport/物理条件、実施方式、expected、observedResult、evidenceRefs、制約を記録する。未実行はobservedResult=nullを保ち、実行済みのような画像やlogを作らない。

Sは入力/抽出器/比較範囲、Rは実際の表示/環境/状態、Aは読んだ対象と判断理由、Mは適用条件の確認理由を伴う。原稿コードポイント検査だけを見た目の試験と数えない。負例が期待どおりfailedを返した場合、テストは成功でも対象artifactの問題はfailedのままである。
