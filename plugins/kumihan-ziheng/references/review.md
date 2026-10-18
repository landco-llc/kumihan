# 唯讀檢視與證據

審閱時不編輯、轉存、轉換、上傳或執行受審作品的程式碼、巨集或外部連結。修正需要另一項明示請求。報告可在回覆中提供；不要覆寫原檔。

1. 記錄目標、digest（有能力時）、locale、媒體、地區編輯體例及實際檢查範圍。沒有原稿或 renderer 時先列限制。
2. 先檢查原稿，再看實際排版、理解與操作。保護姓名、價格、全半形、變體選擇符、組合字元與 emoji 序列。
3. 若主機有 Python，可選用本 Skill 的 [純函式 helper](../scripts/checks.py)。`check_preservation(source_bytes, returned_bytes)` 僅比對呼叫者提供的精確擷取 bytes。`review_text(text, locale, role, quote_style=None)` 僅檢查已分段文字：role 為 prose/name/url/code/english-quote/protected。不得把原始 HTML、混合語言整頁或文件直接當成 prose。
4. helper 不寫檔、不連網、不渲染、不修正。ASCII 標點與特定引號只能形成 `needs-review` 候選，不是語法錯誤或描畫失敗；無候選也不是整體 PASS。香港省略 quote_style 時不預設臺灣體例。
5. 依 [報告 schema](../schemas/report.schema.json) 記錄每個 ID、status、method、位置／scope、reason、evidence_refs。用 [來源](../sources/public-sources.json) 區分專案政策、教育指引與規格。規則的 implemented 僅指 notes 中列出的狹窄工具範圍。

| status | 意義 |
| --- | --- |
| passed | 已檢查，且有對應證據 |
| failed | 實測不符合所選規則 |
| needs-review | 有候選或編輯選擇待判斷 |
| not-checked | 尚未執行 |
| unsupported | 目前環境不能檢查 |
| not-applicable | 不適用於本範圍 |
| waived | 具現行、指定目標的明示例外批准 |

method 分為 static、rendered、assisted、manual。沒有實際描畫就不填 rendered PASS；沒有精確原稿／擷取就不宣稱字元保全 PASS。不能免除默默改寫原稿的問題。

結束時在有能力的環境重算目標 digest，記錄前後值。不一致就報告，不要偷偷還原。審閱自己的測試摘要不等於獨立原生主機驗收。
