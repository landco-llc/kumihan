# Web 製作與檢查

先確認 [地區與原稿](workflow.md)，再選 [文章](../profiles/web-editorial.json)、[行銷](../profiles/web-marketing.json) 或 [介面](../profiles/web-ui.json)。保留標題、價格、說明、錯誤訊息及可操作內容。

- 在對應區塊標記實際內容語言；已明示臺港時可用 `lang="zh-Hant-TW"` 或 `lang="zh-Hant-HK"`，未定地域可保留 `zh-Hant`。英語片段另標示，不從文字猜地域。lang不是編輯體例或文字轉換指令。
- 以瀏覽器正常換行為起點，實際比較行寬、字級、行距、字型與 fallback。看到 DOM 的「，」不等於行首禁則失敗；需要實際行端證據。禁則嚴格度依出版需求記錄。
- 依實際捲動方向檢查重排：縱向捲動用320 CSS px寬、橫向捲動用256 CSS px高；實際 200% 文字放大、使用者間距調整分開測試，記錄瀏覽器／字型與頁面狀態。CSS 模擬放大不能充當實際瀏覽器 zoom 測試。
- 長網址可局部試用 `overflow-wrap: anywhere`，但要確認複製、連結目標與原稿一致。不要對全站套用 `word-break: break-all`、`nowrap`、裁切或縮字來藏住問題。
- 標點寬度調整、字距、字型特性和 ruby 依支援程度選用，逐一看實際效果。未實測的新 CSS 功能保留 fallback；不提供強迫所有作品相同外觀的固定模板。
- 不以標點轉碼、插入空白或 ZWSP/ZWJ 來達成視覺修補。必要且原本存在的不可見字元保留。

本套件沒有瀏覽器或行端偵測器。橫排／直排標點方向、複雜注音和行間注需實際 renderer。沒有工具時回報 `not-checked`，不要從原始碼推論描畫已通過。

直排工作先依 [直排布局](vertical-layout.md) 決定元素方向與run，再依 [字型證據](vertical-fonts.md) 確認實例。網站可採直排題字與橫排資訊的 [混合構成](vertical-expression.md)；實際測切換、焦點、選取和CTA。
