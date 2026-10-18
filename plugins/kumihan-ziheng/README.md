# KUMIHAN｜字衡

繁體中文的文字組版指引，分別處理臺灣 `zh-Hant-TW` 與香港 `zh-Hant-HK`。
這是尚未正式發布的獨立預覽候選。版本以 [plugin.json](plugin.json) 為準；
與日本語 KUMIHAN 分開安裝、管理版本及配布，不需要先裝日本語版。

## 開始使用

1. 按 [安裝說明](INSTALL.md) 選擇整包或單一 Skill。
2. 告訴 AI 地區、媒體、工作模式，以及不可改動的原稿。範例：
   「以 zh-Hant-HK 唯讀檢視這份簡報。保留專名、價格與標點，先確認編輯體例；未實測的項目請明說。」
3. 製作前先確定讀者與資訊重點，完成後分開檢視文字保存和實際版面。

| Skill | 用途 |
| --- | --- |
| kumihan-ziheng | 工作入口、地區與媒體選擇 |
| kumihan-ziheng-web | 文章、行銷頁與介面 |
| kumihan-ziheng-documents | 文件、報告與簡報 |
| kumihan-ziheng-review | 唯讀檢視，不修改原檔 |

每個 Skill 都帶自己的規則、profiles、schemas、來源和參考檔，可單獨使用。
見 [臺港差異](skills/kumihan-ziheng/references/regions.md)、[檢視方式](skills/kumihan-ziheng/references/review.md) 和 [更新說明](UPDATES.md)。
不做繁簡轉換、原稿正規化、強制換字或固定字型推薦。

## 能力與限制

15 條獨立撰寫的字衡規則，加上從既有正本生成的 16 條共通政策。
5 條字衡規則有狹窄的靜態工具範圍，詳見各規則 verification.notes；
其餘 10 條是 guidance-only。implemented 不表示整條排版規則可自動判定。
ASCII 標點和引號只回報 needs-review 候選。精確 bytes 比對不保證擷取完整或視覺正確。

套件沒有 renderer。實際行端、地區字形、200% 放大、直排、注音／ruby、Word、PowerPoint、PDF 匯出及原生主機安裝／呼叫尚未驗收。
香港的機構別引號體例需確認；不套用臺灣教育部體例作為香港的預設。
22 件原創 fixture 是本次靜態測試資料；未取得較早研究集的 52 候選／28 案例原本，不宣稱已全部移植或驗證。

[測試摘要](TEST_REPORT.md) 與 [輕量審查](LIGHT_REVIEW.md) 說明實測及未測範圍。
Apache-2.0，見 [LICENSE](LICENSE)；出處與素材限制見 [notices](THIRD_PARTY_NOTICES.md)。

## 日本語

KUMIHAN｜字衡は台湾／香港の繁體中文向けの独立プラグインです。既存の日本語版のID・版・配布物を変更せず、共通ポリシーを生成時に再利用します。ネイティブホストや実描画は未検証です。

## English

KUMIHAN｜字衡 is an independent Traditional Chinese guidance plugin with explicit Taiwan and Hong Kong contexts. It preserves source text, reuses canonical shared policies at build time, and keeps Japanese package identity and distributions unchanged. Static candidates are separate from rendered evidence. Native host acceptance and document rendering remain unverified. This candidate is unpublished.
