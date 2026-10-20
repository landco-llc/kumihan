# Public sources for the multilingual composition design

Research bibliography; not a runtime certification. Only public source fields are included here. Private Drive identities, internal references, unpublished assets and figures are intentionally excluded.

| ID | Source | URL | Class | Limited relevance |
|---|---|---|---|---|
| S01 | Unicode UAX #9 — Bidirectional Algorithm | https://www.unicode.org/reports/tr9/tr9-51.html | standard | 論理順と視覚順、段落方向、双方向処理。参照版17.0.0 / revision 51。 |
| S02 | Unicode UAX #14 — Line Breaking Algorithm | https://www.unicode.org/reports/tr14/ | standard | 行分割機会と実際の行位置の分離。固定実装版は開発時に記録。 |
| S03 | Unicode UAX #29 — Text Segmentation | https://www.unicode.org/reports/tr29/ | standard | 書記素・単語・文境界とtailoring。字形クラスタと同一ではない。 |
| S04 | Unicode UAX #24 — Script Property | https://www.unicode.org/reports/tr24/tr24-39.html | standard | Script / Script_Extensions、Common / Inherited、文字体系と言語の分離。参照版17.0.0 / revision 39。 |
| S05 | W3C Language tags in HTML and XML | https://www.w3.org/International/articles/language-tags/ | guidance | BCP 47による言語・文字体系・地域等の識別。 |
| S06 | W3C Inline markup and bidirectional text in HTML | https://www.w3.org/International/articles/inline-bidi-markup/ | guidance | 部分方向の分離とHTMLの方向マークアップ。 |
| S07 | HarfBuzz — Clusters | https://harfbuzz.github.io/clusters.html | implementation-doc | 入力文字と出力glyphの対応、結合・再配置・クラスタ。 |
| S08 | OpenType — BASE table | https://learn.microsoft.com/en-us/typography/opentype/spec/base | standard | 複数scriptのbaseline情報。利用・実効結果はホスト依存。 |
| S09 | ICU — Boundary Analysis | https://unicode-org.github.io/icu/userguide/boundaryanalysis/ | implementation-doc | 境界処理と辞書等の言語資源。 |
| S10 | CSS Text Module Level 4 | https://www.w3.org/TR/css-text-4/ | draft-standard | text-autospace、要素境界をまたぐshaping等。仕様と対応ブラウザを区別。 |
| S11 | CSS Writing Modes Level 3 | https://www.w3.org/TR/css-writing-modes-3/ | standard | writing-mode、text-orientation、directionを分離。 |
| S12 | Requirements for Japanese Text Layout | https://www.w3.org/TR/jlreq/ | layout-requirements | 禁則、和文組版、縦横、ルビ等。WG Noteであり認証ではない。 |
| S13 | Requirements for Chinese Text Layout | https://www.w3.org/TR/clreq/ | layout-requirements | 中国語約物・行配置・縦横等。版と地域差に注意。 |
| S14 | WCAG 2.2 Understanding — Text Spacing | https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html | accessibility-guidance | 行高1.5、段落2、字間0.12、語間0.16の上書き耐性。初期値ではなく適用例外あり。 |
| S15 | WCAG 2.2 Understanding — Language of Parts | https://www.w3.org/WAI/WCAG22/Understanding/language-of-parts.html | accessibility-guidance | 異言語部分の識別と固有名等の例外。 |
| S16 | WCAG 2.2 Understanding — Reflow | https://www.w3.org/WAI/WCAG22/Understanding/reflow.html | accessibility-guidance | リフロー。適用対象・二次元配置例外を分ける。 |
| S17 | Unicode Core 17 — Chapter 7 Europe-I | https://www.unicode.org/versions/Unicode17.0.0/core-spec/chapter-7/ | standard-background | Latin/Greek/Cyrillicの関係、言語別アクセントやcase。 |
| S18 | Unicode Core 17 — Chapter 9 Middle East-I | https://www.unicode.org/versions/Unicode17.0.0/core-spec/chapter-9/ | standard-background | Hebrew/Arabicの文字構造、結合記号・接合。 |
| S19 | Unicode Core 17 — Chapter 12 South and Central Asia-I | https://www.unicode.org/versions/Unicode17.0.0/core-spec/chapter-12/ | standard-background | Devanagari/Bengali等の構造と文字順・字形。 |
| S20 | Unicode Core 17 — Chapter 16 Southeast Asia-I | https://www.unicode.org/versions/Unicode17.0.0/core-spec/chapter-16/ | standard-background | Thai/Khmer等の文字体系。地理から方向を決めない。 |
| S21 | Unicode Core 17 — Chapter 18 East Asia | https://www.unicode.org/versions/Unicode17.0.0/core-spec/chapter-18/ | standard-background | Han/Kana/Hangul/Bopomofo等。 |
| S22 | Google Design / Ek Type — Anek | https://design.google/library/anek-multiscript | creator-case | Latin-firstにしない10文字体系の並行設計。script固有の上下領域と共有造形。 |
| S23 | Re-Levant — Bezalel Academy | https://re-levant.co.il/projects/bezalel-academy/?lang=en | creator-case | 2020年の三言語Abrahamを用いるブランド設計。 |
| S24 | Bezalel — Graduate Exhibition 2024 | https://www.bezalel.ac.il/events/658251 | brand-case | ヘブライ語・アラビア語・英語の催事タイトルと実用情報。 |
| S25 | Anagata — Google Sans KH | https://anagata.design/projects/google-sans-kh | creator-case | looped/loopless、text/displayの分離。小サイズ用のcounter等。 |
| S26 | Anagata — MiSans Khmer | https://anagata.design/projects/misans-khmer | creator-case | Khmerのloopを残しLatinとの造形調和。 |
| S27 | Anagata — PlerngKob | https://anagata.design/projects/plerngkob | creator-case | Khmer/Latinロゴの角度と積層の整合。 |
| S28 | Anagata — Grab Community KH | https://anagata.design/projects/grab-community-kh | creator-case | ブランド固有のKhmer表示書体。 |
| S29 | IBM Design Language — Type scale | https://www.ibm.com/design/language/typography/type-scale/ | brand-policy | IBM Plex内の言語別95%補正と共通line-height。 |
| S30 | GOV.UK — Type scale | https://design-system.service.gov.uk/styles/type-scale/ | design-system | 現行v6系の19px本文、48/36/24等の役割、狭幅の変化。 |
| S31 | Carbon — Typography type sets | https://www.carbondesignsystem.com/building-blocks/foundations/typography/type-sets | design-system | productive14pxとexpressive16px、compact/longの行高差。 |
| S32 | Carbon — Typography style strategies | https://www.carbondesignsystem.com/building-blocks/foundations/typography/style-strategies | design-system | タスク集中と表現的体験の用途差。 |
| S33 | Adobe — Introducing Source Han Sans | https://blog.adobe.com/en/publish/2014/07/15/introducing-source-han-sans-an-open-source-pan-cjk-typeface | creator-case | Pan-CJK書体の共同制作と多文字体系。歴史資料。 |
| S34 | Adobe Fonts — Source Han Sans Pan-CJK Japanese | https://fonts.adobe.com/fonts/source-han-sans-cjk-japanese | font-documentation | 日本語デフォルト字形と他言語字形。名前だけで実使用字形は保証しない。 |
| S35 | Google — Noto CJK language and region | https://developers.googleblog.com/noto-a-cjk-font-that-is-complete-beautiful-and-right-for-your-language-and-region/ | creator-case | 地域の字形を保ちながらファミリーを調和。 |
| S36 | Unicode UTS #39 Security Mechanisms | https://unicode.org/reports/tr39/ | standard | 識別子等のconfusableリスク。本文の多文字体系を一律禁止する根拠にはしない。 |
| S37 | Morisawa — Multilingual typesetting | https://www.morisawa.co.jp/fonts/multilingual/typesetting/ | foundry-guidance | 多言語組版と書体の役割。 |
| S38 | Unicode 17 core specification | https://www.unicode.org/versions/Unicode17.0.0/core-spec/ | standard | 版付きCore本文の参照起点。 |
| S39 | GOV.UK — Updated type scale | https://design-system.service.gov.uk/get-started/new-type-scale/ | design-system | 旧版の狭幅値を現行値として流用しない。 |

Spec reference IDs S01-S39 map to the corresponding rows. For time-sensitive standard versions, pin the precise document and test the implementation separately.
