# 安裝與驗收

這是未發布的預覽候選；來源在專用 feature branch，請固定審查過的 commit。
日本語版的根目錄 plugin.json 與安裝指南不適用於字衡。不要把 monorepo 根目錄當成字衡套件。

## Codex：獨立 Skill

在 原始碼或配布資料夾的 `downloads/skills/` 選擇一個 ZIP。驗證 SHA256SUMS.txt 後展開，
把完整的 `kumihan-ziheng*` 資料夾放到目標專案的 `.agents/skills/` 下。
例如 `.agents/skills/kumihan-ziheng-review/SKILL.md`；保留其 references、rules、profiles、schemas、scripts 與 sources。
只需一個 Skill 就能完成該角色工作，無須其他兄弟 Skill 或日本語安裝。
在新對話中明示 Skill 名稱並用原創小樣本驗收；不同主機的重新載入方式可能不同。
不要覆寫同名既有資料夾，先移到備份位置。

## Codex／ChatGPT：整包插件

原始碼或配布資料夾的 `downloads/plugins/` 的 ZIP 展開後，`kumihan-ziheng/` 本身才是套件根目錄。
其中有 portable `plugin.json`、相容 `.codex-plugin/plugin.json` 和四個 `skills/`。
將這個目錄交給目前主機支援的本地插件匯入／測試流程。
ChatGPT／Codex 的目錄來源與私有安裝能力依環境而異：沒有相應入口時，不要把 ZIP 上傳成普通附件當成已安裝插件。
此變更不建立 marketplace 登錄或遠端插件，也不修改使用者的主機設定。
實際安裝、探索、onboarding 和呼叫尚未測試，請在可用主機驗收並記錄版本。

官方參考：[Skills](https://learn.chatgpt.com/docs/build-skills)、[Plugin package](https://developers.openai.com/plugins/build/plugins)。
上述結構已做本地展開與路徑檢查；官方文件閱讀不等於主機驗收。

## 其他主機

Claude／Gemini 的字衡原生 manifest 與配布未提供；這些主機的專屬驗收為 not-checked，
不能拿既有日本語配布宣稱字衡已支援。通用 Markdown 資料可閱讀，但不代表已註冊為原生 Skill。

## 先做的小樣本

確認 `zh-Hant-TW` 和 `zh-Hant-HK` 能分開選；原稿「陳𠮷、臺／台、ＨＫ＄１２３、é」保持原樣。
香港未指定引號體例時應先確認；URL、程式碼和英文引文不應被改寫。
唯讀檢視前後比較目標 digest，保留 needs-review／not-checked。
