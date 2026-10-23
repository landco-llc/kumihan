# 更新與開發

字衡的版本只由本目錄 `plugin.json` 管理，不跟隨日本語版版本。
以相同主機格式取得新套件、驗證 checksum，備份舊的字衡資料夾，再替換完整目錄。
不混合不同版本的 rules／references。重啟或重新載入後再次做小樣本驗收。

從 repo 根目錄執行（Python 3.9+ 標準函式庫）：

```sh
python3 tools/build_ziheng.py
python3 tools/build_ziheng.py --check
python3 tools/build_dist.py --check
```

字衡 build 只改 `plugins/kumihan-ziheng/skills/`、`downloads/`、相容 `.codex-plugin/` 與由 GitHub 正本官方 KUMIHAN logo 生成的 `assets/`。
不會呼叫日本語 builder 或重新包裝日本語 ZIP。修改版號可用：

```sh
python3 tools/build_ziheng.py --set-version 0.2.2
```

此命令只修改字衡正本 manifest，再產生字衡輸出。建置或更改版本都不是發布。
不執行 merge、tag、Release、marketplace 提交或部署。

`entrypoints/` 是四個 SKILL.md 的正本；`references/`、`schemas/`、`locales/`、`rules/`、`runtime/` 是字衡正本。
共通 CONTENT／DESIGN／EVIDENCE 只讀取 `skills/kumihan/rules/` 的既有正本；
產生的副本和 inventory 不可獨立編輯。其來源 digest 存在各 Skill 的 sources/common-provenance.json。
locale resolver 是新增的工具層，不改既有日本語 schema、title_ja、固定 ID 或 profiles。

測試：

```sh
python3 -m unittest discover -s tests/ziheng -v
```

測試用 JSON Schema 驗證需要 `jsonschema`；產品與 builder 本身不需要此套件。
生成的 ZIP 固定成員順序、時間與權限；同一 Python/zlib 環境會檢查重建一致，
不承諾跨壓縮函式庫版本 byte 完全相同。依 downloads/SHA256SUMS.txt 驗證候選產物。

顯示名稱固定為 **KUMIHAN｜字衡**（無版號）；ZIP 檔名含版本。官方 logo 由 repository 根目錄的 assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png 原本產生，未經重新繪製。

## Claude／Gemini 的独立配布

先執行一般字衡 builder（只驗證不修改也可），再重建專用 Host ZIP：

```sh
python3 tools/build_ziheng.py --check
python3 tools/build_ziheng_hosts.py
python3 tools/build_ziheng_hosts.py --check
```

Claude 的 `.claude-plugin/plugin.json` 與 Gemini 的 `gemini-extension.json` 由字衡 Host builder 產生；原本的日本語 KUMIHAN 配布不會改變。生成的 `downloads Claude/`、`downloads Gemini/` 各含五個 ZIP、完整 manifest 及 SHA-256。

## v0.2.0 歷史更新

新增地域／語體／角色／原稿權限的v2契約、證據sidecar、32個研究案例定義與16個作品決策卡。4個Skill保留獨立資料，靜態候選不代表描畫或母語驗收。原本v1介面與31個產品ID不變。

v0.2.0 的 GitHub Release 已公開。原 v0.1.0 ZIP 與 URL 保留，history/0.1.0 留存原 manifest 與 checksum；原生主機及 Marketplace 的驗收狀態另行記錄。

`retained-distributions.json`只允許列明path與digest的歷史bytes。`--check`不寫入，會拒絕舊版損壞；未知stale不會因保留舊版而獲豁免。

## v0.2.2 直排更新

依臺灣與香港的直排研究，補充閱讀／展示／混合表現、標點與引號位置、連續破折號及刪節號、數字與拉丁字母片段、注音與標示符號、字型縱向資訊、橫直排切換及閱讀順序的判斷。字距與標點壓縮依編輯體例、文字角色及實際環境選擇，不預設整頁負字距或自動改寫原稿。

新增 30 個直排案例；與原有 v0.2.0 案例分開管理。靜態契約、實際描畫、操作、原生文件應用程式及當地校閱分開記錄；未執行的驗證不因打包或規則選擇而變成通過。

更新時先備份原安裝，取得相同 host 的完整 v0.2.2 套件，核對該配布的 MANIFEST 與 SHA256SUMS，整個目錄替換，不混搭版本。重載後以固定原稿小樣本確認。現有使用者不會自動更新；v0.1.0 與 v0.2.0 ZIP 和 URL 保留，其原 manifest 與 checksum 存在各下載目錄的 history/<version>/。

原始碼建置、正式 Release 與主機 Marketplace 發布分別確認；目前正式下載請以[網站顯示的已驗證版本](https://landco-llc.github.io/kumihan/kumihan-zh-han.html)為準。
