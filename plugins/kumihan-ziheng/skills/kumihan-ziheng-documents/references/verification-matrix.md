# 驗證方法與案例的範圍

v0.2.2 有34個產品規則ID（18個繁體中文規則與16個共通規則）；既有31個ID保持，新增ZH-HANT-016–018。先前研究提案P01–P32（A18/B10/C4）與F01–F32是不同集合；[案例契約](../fixtures/research-v020/cases.json)逐項記錄來源、條件、輸入、預期、例外、方法與限制。定義fixture不代表32項合格；候選結果在版本候選報告另記。


## v0.2.2 直排契約

[直排案例](../fixtures/research-v022/cases.json) 是 TW12／HK10／shared8，共30個獨立輸入；[採用對應](vertical-adoption.json) 把14個基礎、10個條件式和4個保留提案連到規則。這些件數不能和舊32例、規則34個或個別 shaping 條件合計為通過率。fixture 本身的 result 為 null，執行欄位保持 not-checked；實際觀察另外保存。

- `scripts/checks.py` 的 `validate_vertical_fixture`／`validate_vertical_suite` 檢查原稿hash、完整輸入契約與未執行模板；沒有渲染原稿。`inspect_vertical_runs(text, runs)` 只查已宣告範圍，`inspect_vertical_pair_breaks(text, break_offsets)` 只查呼叫者提供的斷點。零候選不等於列端或書記素全部合格。
- `scripts/context.py` 為016、017、018保留適用條件：直排字型證據；已選語意標記與地域體例；已有element_role／expression_mode的直排閱讀及操作。016與018可做地域中立部分，不能由此通過未定地域的glyph。未選功能或缺少條件時記入deferred；不是failed。
- [直排證據schema](../schemas/vertical-evidence-v022.schema.json) 與 `scripts/evidence.py` 的 `validate_vertical_evidence(record)` 是加列契約，不改寫v2既有方法enum。一筆紀錄連結一個artifact digest、完整fixture輸入digest、variant、scope、method與證據。JSON有效只是宣告結構合格，不能認證截圖、操作者或檔案的真實性。
- 方法明確區分 static、rendered、interaction、native-application、native-proofreading。最後兩者分別是原生應用操作與當地語文校閱，不能互相替代。舊v2的native-review值仍依舊契約使用，不把新方法硬塞入舊schema。
- glyph／font的passed必須有實檔識別、配發版、內部版、SHA及實際使用的fallback；描畫另要glyph觀察、畫面／測量和shaping路徑。只有`vert`標籤、CSS family或字型品牌不足。無法識別時可以記觀察與限制，但不得聲稱該glyph範圍passed。
- Web、Office、PDF分別記錄OS、應用與引擎版本、尺寸、放大方法、字級、字重、列長、列間、字距及功能。AT另外標識實際AT與版本。換方向測內容和狀態；reflow根據捲動方向選物理寬320或高256 CSS px，不從writing-mode猜測。

詳細判斷參見 [直排布局](vertical-layout.md)、[字型證據](vertical-fonts.md) 與 [用途比較](vertical-expression.md)。參考來源為ZV-*；本版沒有附帶字型白名單、組版引擎、Office renderer或母語校閱服務。

## 既有可執行契約

1. `scripts/context.py` 的 `resolve_review_context(raw)` 接收新增metadata，不修改v1 strict context。`select_review_rules(context, records, profile)` 回傳 candidate_rule_ids（profile/medium聯集）、applicable_rule_ids（條件已滿足，待檢查）、deferred_rules（缺項或未採功能及原因）、selection_only=true。適用不等於執行／passed，候選不進合否分母。未知地域僅使用明列的中立規則；臺灣不適用004，香港不適用003；未選引號、直排、ruby等需保留理由。
2. `scripts/checks.py` 的 `check_preservation(bytes, bytes)` 只比較提供的bytes與SHA，不保證抽取完整；segment wrapper只對caller已分類的TW/HK中文正文提出有限標點候選，其他role保護。位置為0起算Unicode code point，非UTF-16或grapheme。舊review_text介面不變；raw HTML不當正文解析。零候選不產生artifact passed。
3. `scripts/evidence.py` 與 [v2證據schema](../schemas/review-evidence-v2.schema.json) 要求artifact digest、方法、scope、七狀態、證據及限制。證據需綁定同一artifact。rendered passed需觀察環境與截圖／位置測量，interaction需實操作紀錄；CSS字串不足。實用font未知可觀察畫面，但不能宣稱地域glyph或IVS passed。validator只查宣告，不驗證檔案真實性、母語正確性或認證。

## 描畫、互動與編輯驗收

禁則水準與CSS line-break是不同資料；UAX14提供斷點機會，實行端要用實font、寬度和引擎觀察。二倍破折號、六點省略、數量／符號／單位各選定結合單位，不對全段nowrap。URL/code的視覺換行、href、複製、導航分開記錄，不能插入ZWSP使其折行。[ZR-T01/T03/T09/T16]

標點的code point、glyph位置、壓縮是不同層。臺灣常保留全寬、香港常有壓縮不是強制值。比較文中、行端、鄰接標點；palt/halt與CSS trim不可因名稱就假定可疊加。中歐混排的視覺空隙不可用原稿插空格代替；既有空格亦保留。[ZR-T04/T17]

直排分開writing-mode、orientation、combine、Latin旋轉與表單操作。ruby／注音只在採用時驗基底、聲調、行端、搜尋、複製及AT讀序；HTML語義或CSS存在不保證支援。IVS-like保全樣本不代表已查註冊collection或指定glyph。[ZR-T02/T05/T08/T10/T13/T14/T19]

Web範圍：縱向捲動寬320 CSS px，橫向捲動高256 CSS px；二維表格等例外按內容區域記錄。200%用實際受支援的UA放大機制並記錄方法，CSS zoom/device scale不冒充。spacing同時覆寫行高1.5、段後2em、字間.12em、詞間.16em，其他style不改，記錄語言/script例外。這些是使用者覆寫耐性，不是作者初值。[ZR-T20/T21/T22/T23]

對比通常4.5:1、大字3:1，包含CJK相當字級和適用例外，取實際相鄰顏色／互動狀態；字形判讀另看。沒有WCAG通用16px或18px最低線。Office原生顯示／編輯與PDF出圖、搜尋、抽取、連結、順序分開驗，不移用Web結果。[ZR-T20/T24/T25]

七狀態維持 passed / failed / needs-review / not-checked / unsupported / not-applicable / waived。未做是not-checked，環境缺能力為unsupported，免除需理由。題字風格、未採ruby或直排不自動升為阻擋。地域語體草稿需當地校閱；技術schema不能代替。

來源：[台帳](../sources/public-sources.json)。本版無組版引擎、Office生成器或MCP runtime。
