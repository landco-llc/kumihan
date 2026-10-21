# KUMIHAN｜Μέτρο — installation

Οδηγίες ελληνικής τυπογραφίας με διατήρηση του αρχικού κειμένου και σαφή όρια ελέγχου. | Greek typography guidance with original-text preservation and explicit verification limits.

Unpack the desired **v0.1.0** archive and retain its single product/skill directory intact. Source and archives are Private candidates; no marketplace publication or native host test is implied. No credentials, server settings or network access are required.

- GPT/Codex plugin: use the product directory containing `plugin.json`, `.codex-plugin/plugin.json` and `skills/` with the host's supported local plugin workflow. For one standalone skill, install the directory containing `SKILL.md` through that host's skill installer.
- Claude Code plugin: use the directory containing `.claude-plugin/plugin.json` through the supported local plugin workflow, for example `claude --plugin-dir /absolute/path/to/kumihan-metro`. Standalone Skills are installed as intact skill directories in the supported user/project skills location.
- Gemini CLI extension: use the product directory containing `gemini-extension.json` and `GEMINI.md` with `gemini extensions install /absolute/path/to/kumihan-metro`. For a standalone skill use the current host's supported skills-install command and keep its bundled files. Consumer Gemini Apps invocation is not certified.

Verify the selected archive against its `manifest.json`/`SHA256SUMS`, inspect the exact installed name and official icon in [README](README.md), and test a small source-preservation request before using production content. Host commands and feature availability can vary by version; native invocation remains not checked.

From the installed skill directory, run `python runtime/check_source.py SOURCE --locale el --medium review`; Python 3.10+ with its standard library is sufficient. `--candidate CANDIDATE` compares a supplied derivative without modifying either file. Add `--format html --medium web` for bounded static HTML source diagnostics. Do not treat that output as a browser or Office rendering pass.
