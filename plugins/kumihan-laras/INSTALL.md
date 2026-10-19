# Pemasangan / Installation — KUMIHAN｜Laras v0.1.0

Plugin name shown to users: **KUMIHAN｜Laras**. Technical slug: `kumihan-laras` (required by plugin tooling).

1. Download from [GitHub Release](https://github.com/landco-llc/kumihan/releases/tag/kumihan-id-v0.1.0) and verify `SHA256SUMS.txt`.
2. Claude Code: extract Claude plugin archive, then `claude --plugin-dir /absolute/path/kumihan-laras`. If supported, use `/plugin marketplace add landco-llc/kumihan` then `/plugin install kumihan-laras@kumihan-marketplace`.
3. Gemini CLI: extract extension archive and run `gemini extensions install /absolute/path/kumihan-laras`; inspect `gemini extensions list`.
4. Individual skills: extract each ZIP to a host-supported skills directory; for Codex project installs, `.agents/skills/` is typical. In-app ChatGPT/Gemini skill upload depends on your account and UI.
5. Optional static read-only review: `python runtime/checks.py original.txt --locale id-ID --candidate candidate.txt`.

Mengunggah ZIP ke chat bukan pemasangan otomatis. / Attaching a ZIP in chat is not automatic installation. Host and native-editor verification must be reported separately.
