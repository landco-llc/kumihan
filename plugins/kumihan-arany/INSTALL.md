# Installation — KUMIHAN｜Arány

Select the versioned host archive. Extract into a new directory and retain its single product/Skill root. Do not overwrite an existing installation without a backup.

GPT/Codex: install the provider root containing `.codex-plugin/plugin.json` through the host's local plugin workflow, or install one portable Skill root containing `SKILL.md` in its supported local Skills directory. Host-specific distribution UI availability is not claimed.
Claude Code: use the extracted provider root as a local plugin directory (`claude --plugin-dir /absolute/path/kumihan-arany`), or place one Skill directory under the host's supported Skills directory. Gemini CLI: link the extracted extension root (`gemini extensions link /absolute/path/kumihan-arany`); `GEMINI.md` routes to bundled Skills. Portable Skill ZIPs contain one complete Skill; configure the host to load that SKILL.md, rather than linking it as a full extension.

Each provider archive contains all four Skills; each portable archive contains exactly one independent Skill, runtime, rules, icon and references. Do not assume host UI icon rendering from physical inclusion. Check downloads/SHA256SUMS and manifest.json before use. Native host invocation is not-checked.

Local static smoke: `python runtime/check_source.py SOURCE --locale hu --medium review`. Python 3.10+ standard library only. The checker reads but never writes source. Review output is JSON, not an edited manuscript.
