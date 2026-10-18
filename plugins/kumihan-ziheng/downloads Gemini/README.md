# KUMIHAN｜字衡 for Gemini / Gemini 版本

v0.1.0-preview (preview). 臺灣 / 香港繁體中文文字組版 — Traditional Chinese typography and read-only review.

Gemini CLI: extract the extension ZIP into a new folder, then run `gemini extensions install /absolute/path/to/folder`. Direct install from this monorepo's root selects **Japanese KUMIHAN**, not ZiHeng.

Gemini app: use an individual skill ZIP if the Skills import feature is available.

## Full bundle / 整包

- [kumihan-ziheng-Gemini-CLI-extension-0.1.0-preview.zip](extensions/kumihan-ziheng-Gemini-CLI-extension-0.1.0-preview.zip)

## Four independent skills / 四個獨立技能

- [kumihan-ziheng](skills/kumihan-ziheng-Gemini-Apps-skill-0.1.0-preview.zip)
- [kumihan-ziheng-web](skills/kumihan-ziheng-web-Gemini-Apps-skill-0.1.0-preview.zip)
- [kumihan-ziheng-documents](skills/kumihan-ziheng-documents-Gemini-Apps-skill-0.1.0-preview.zip)
- [kumihan-ziheng-review](skills/kumihan-ziheng-review-Gemini-Apps-skill-0.1.0-preview.zip)

## SHA-256 verification / 校驗

`shasum -a 256 -c SHA256SUMS.txt` (or equivalent) from this download folder.

No automatic rendering, regional glyph, Office/PDF, or native-host compatibility guarantee. No public marketplace listing is implied.
