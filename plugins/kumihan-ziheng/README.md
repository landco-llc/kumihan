# KUMIHAN｜字衡

繁體中文的文字組版指引，分別處理臺灣 `zh-Hant-TW` 與香港 `zh-Hant-HK`。
這是獨立技能套件；GitHub 原始碼已提供，ChatGPT 公開插件商店尚未發布。版本以 [plugin.json](plugin.json) 為準；
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

字衡的地區規則與從既有正本生成的共通政策分開管理。
部分規則有狹窄的靜態工具範圍，詳見各規則 verification.notes；
其他判斷需依實際作品提出指引。implemented 不表示整條排版規則可自動判定。
ASCII 標點和引號只回報 needs-review 候選。精確 bytes 比對不保證擷取完整或視覺正確。

套件沒有 renderer。實際行端、地區字形、200% 放大、直排、注音／ruby、Word、PowerPoint、PDF 匯出及原生主機安裝／呼叫尚未驗收。
香港的機構別引號體例需確認；不套用臺灣教育部體例作為香港的預設。
原有靜態 fixture、v0.2.0 的 32 個研究案例與 v0.2.2 的 30 個直排案例各自保留身分。案例定義、規則選擇與實際驗收結果分開記錄。

[驗證範圍](VERIFICATION.md) 說明實測及未測範圍。
Apache-2.0，見 [LICENSE](LICENSE)；出處與素材限制見 [notices](THIRD_PARTY_NOTICES.md)。

## 日本語

KUMIHAN｜字衡は台湾／香港の繁體中文向けの独立プラグインです。既存の日本語版のID・版・配布物を変更せず、共通ポリシーを生成時に再利用します。ネイティブホストや実描画は未検証です。

## English

KUMIHAN｜字衡 is an independent Traditional Chinese guidance plugin with explicit Taiwan and Hong Kong contexts. It preserves source text, reuses canonical shared policies at build time, and keeps Japanese package identity and distributions unchanged. Static candidates are separate from rendered evidence. Native host acceptance and document rendering remain unverified. The GitHub source and ZIP distributions are available; the ChatGPT public plugin has not been released.

## Claude / Gemini 配布と導入 / Claude and Gemini

Claude Code、Claude chat、Gemini CLI 及 Gemini 應用程式已有字衡專用套件，均沿用同一套臺灣與香港規則。正式主機驗收仍需在使用者環境中進行。

ZiHeng bundles for Claude Code / Claude chat and Gemini CLI / Gemini app are available; native invocation is **not yet verified**. Separate skill ZIPs and SHA-256 values are provided for each host.

| Host | 繁體中文 | English | 日本語 |
| --- | --- | --- | --- |
| Claude | [指南](https://github.com/landco-llc/kumihan/blob/main/plugins/kumihan-ziheng/docs/installation-claude.zh-hant.md) | [Guide](https://github.com/landco-llc/kumihan/blob/main/plugins/kumihan-ziheng/docs/installation-claude.en.md) | [ガイド](https://github.com/landco-llc/kumihan/blob/main/plugins/kumihan-ziheng/docs/installation-claude.ja.md) |
| Gemini | [指南](https://github.com/landco-llc/kumihan/blob/main/plugins/kumihan-ziheng/docs/installation-gemini.zh-hant.md) | [Guide](https://github.com/landco-llc/kumihan/blob/main/plugins/kumihan-ziheng/docs/installation-gemini.en.md) | [ガイド](https://github.com/landco-llc/kumihan/blob/main/plugins/kumihan-ziheng/docs/installation-gemini.ja.md) |

Downloads: [Claude](https://github.com/landco-llc/kumihan/blob/main/plugins/kumihan-ziheng/downloads%20Claude/README.md) · [Gemini](https://github.com/landco-llc/kumihan/blob/main/plugins/kumihan-ziheng/downloads%20Gemini/README.md). These hosts remain independent from the Japanese KUMIHAN product.

## Display name / 顯示名稱

**KUMIHAN｜字衡** is the version-free display name used for `@` mentions. Versions stay in ZIP filenames (for example `kumihan-ziheng-0.1.0.zip`) and package metadata.

**KUMIHAN｜字衡** 為不含版號的顯示名稱，避免影響 `@` 提及操作。版本寫在 ZIP 檔名（例如 `kumihan-ziheng-0.1.0.zip`）與套件資訊中。

## v0.2.2 直排更新 / Vertical typography

四個獨立技能依文字角色選擇閱讀、展示或混合表現，分別檢視直排與橫排的標點、引號、行端、字距、欄距及閱讀順序。先確認臺灣／香港的編輯體例、原稿權限、實際字型與輸出環境；不把整段旋轉、負字距或字型品牌當作直排品質的證據。

數字、拉丁字母、網址、注音及標示符號依內容與用途處理。固定原稿維持原字元、Unicode 序列與數值；字型替代、縱向字形、實際行端及讀取順序須在目標環境分開驗證。30 個直排案例提供可重複的檢視輸入，不等同於 30 件描畫或母語校閱通過。

The four independent Skills now include purpose-led vertical typography guidance, mixed-script run handling, contextual spacing and explicit font/rendering evidence. Reading copy, display copy and hybrid compositions keep separate purposes. Existing text and Unicode sequences remain protected. The new 30 vertical case definitions do not claim browser, native Office, accessibility or native-language acceptance.

原始碼版本以本目錄 `plugin.json` 為準；正式公開版及已驗證下載以[字衡網站](https://landco-llc.github.io/kumihan/kumihan-zh-han.html)與 [Release 紀錄](https://github.com/landco-llc/kumihan/releases?q=kumihan-ziheng)為準。v0.1.0、v0.2.0 的舊 ZIP 與 URL 保留；網站發布、GitHub Release 與各主機的 Marketplace 登錄是不同狀態。
