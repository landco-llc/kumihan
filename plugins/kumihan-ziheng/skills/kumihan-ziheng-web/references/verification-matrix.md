# 驗證方法與32項的範圍

本版保留31個產品規則ID。研究提案P01–P32（A18/B10/C4）與F01–F32是不同集合；[案例契約](../fixtures/research-v020/cases.json)逐項記錄來源、條件、輸入、預期、例外、方法與限制。定義fixture不代表32項合格；候選結果在版本候選報告另記。

## 可執行契約

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
