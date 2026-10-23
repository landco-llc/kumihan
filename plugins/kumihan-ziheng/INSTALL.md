# 安裝與驗收

這是獨立套件；GitHub 原始碼可用，ChatGPT 公開插件商店尚未發布。請固定使用經檢查的 commit 或 ZIP checksum。
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

Claude Code 與 Gemini CLI 的字衡專屬套件，以及各自四個個別技能 ZIP，已提供下載。請使用對應的繁體中文／English／日本語導入指南：

- [Claude 導入指南](https://github.com/landco-llc/kumihan/blob/main/plugins/kumihan-ziheng/docs/installation-claude.zh-hant.md) / [English](https://github.com/landco-llc/kumihan/blob/main/plugins/kumihan-ziheng/docs/installation-claude.en.md) / [日本語](https://github.com/landco-llc/kumihan/blob/main/plugins/kumihan-ziheng/docs/installation-claude.ja.md)
- [Gemini 導入指南](https://github.com/landco-llc/kumihan/blob/main/plugins/kumihan-ziheng/docs/installation-gemini.zh-hant.md) / [English](https://github.com/landco-llc/kumihan/blob/main/plugins/kumihan-ziheng/docs/installation-gemini.en.md) / [日本語](https://github.com/landco-llc/kumihan/blob/main/plugins/kumihan-ziheng/docs/installation-gemini.ja.md)
- [Claude ZIP 與 SHA-256](https://github.com/landco-llc/kumihan/blob/main/plugins/kumihan-ziheng/downloads%20Claude/README.md)、[Gemini ZIP 與 SHA-256](https://github.com/landco-llc/kumihan/blob/main/plugins/kumihan-ziheng/downloads%20Gemini/README.md)

Claude Code 的 Marketplace 可從本 mono-repo 的 .claude-plugin/marketplace.json 安裝獨立字衡套件。
Gemini CLI 無法將 monorepo 根目錄視作字衡延伸；請解壓 Gemini CLI 專用 ZIP 並以**本機資料夾**安裝。
以上只確認套件檔案、路徑與靜態檢測；各主機實際載入、呼叫及描畫仍屬 not-checked，不可視為已全面支援。

## 先做的小樣本

確認 `zh-Hant-TW` 和 `zh-Hant-HK` 能分開選；原稿「陳𠮷、臺／台、ＨＫ＄１２３、é」保持原樣。
香港未指定引號體例時應先確認；URL、程式碼和英文引文不應被改寫。
唯讀檢視前後比較目標 digest，保留 needs-review／not-checked。

## v0.2.2 migration

Use the active MANIFEST.json in downloads, downloads Claude or downloads Gemini to select exactly one full bundle or the four Skills for the same host/version. Verify SHA256SUMS.txt before replacing the backed-up installation folder. Do not combine references/scripts from different versions. Native host discovery/invocation still needs acceptance testing. Historical v0.1.0 and v0.2.0 paths remain usable; their original manifests and checksums are retained under history/<version>/.

先備份舊版，按相同 host 取得並校驗 v0.2.2 套件；整包替換、重載、以固定原稿小樣本確認。直排小樣本應包含標點、引號、數字／拉丁字母片段及原有 Unicode 序列。版本升級不會自動更新既有安裝；正式公開版本與下載連結以[網站](https://landco-llc.github.io/kumihan/kumihan-zh-han.html)的已驗證版本為準。
