# KUMIHAN｜Nhịp Chữ — Cài đặt / Installation

## Tiếng Việt

Tải gói v0.1.0 phù hợp với công cụ của bạn tại https://github.com/landco-llc/kumihan/releases/tag/kumihan-vi-v0.1.0. Có ba plugin cho ChatGPT/Codex, Claude Code và Gemini CLI; bốn kỹ năng độc lập cho từng nền tảng. Kiểm tra SHA256SUMS.txt trước khi cài. Tệp đính kèm trong đoạn chat không đồng nghĩa với cài đặt.

## English

Download v0.1.0 host-specific ZIPs from https://github.com/landco-llc/kumihan/releases/tag/kumihan-vi-v0.1.0; check SHA256SUMS.txt. Three host plugins and twelve standalone Skill ZIPs are supplied. Import methods depend on the host and account. Official marketplace approval is not implied.

### ChatGPT / Codex

Use `kumihan-nhip-chu-chatgpt-codex-plugin-v0.1.0.zip` in a supported plugin installer. Alternatively select one of four `*-chatgpt-skill-v0.1.0.zip` packages in a Skills-enabled interface. Do not assume attaching a ZIP installs a plugin.

### Claude Code / Claude

Unzip `kumihan-nhip-chu-claude-code-plugin-v0.1.0.zip` and keep `kumihan-nhip-chu` directory, then run:

```sh
claude --plugin-dir /absolute/path/kumihan-nhip-chu
claude plugin validate /absolute/path/kumihan-nhip-chu
```

Repository marketplace commands, where supported:

```text
/plugin marketplace add landco-llc/kumihan
/plugin install kumihan-nhip-chu@kumihan-marketplace
```

Individual Skills are available as `*-claude-skill-v0.1.0.zip`.

### Gemini CLI / Gemini

Unzip `kumihan-nhip-chu-gemini-cli-extension-v0.1.0.zip` so `gemini-extension.json` resides in the product directory. Then:

```sh
gemini extensions install /absolute/path/kumihan-nhip-chu
gemini extensions list
```

Or use individual `*-gemini-skill-v0.1.0.zip` in supported Gemini environments. The Gemini chat app importer is not verified. Do not install the monorepo root as this product.

### Check / Kiểm tra

```sh
python runtime/checks.py input.txt --locale vi-VN
python runtime/checks.py input.txt --candidate output.txt --css site.css
```

The checker never writes to source; it reports static review candidates. Real font rendering, native Vietnamese copy review and host activation require separate testing.
