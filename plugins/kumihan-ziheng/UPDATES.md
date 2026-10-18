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
python3 tools/build_ziheng.py --set-version 0.1.1-preview
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
