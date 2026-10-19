# KUMIHAN｜Mizani · Install / Usakinishaji

1. Download the matching **v0.1.0** archive from the [GitHub Release](https://github.com/landco-llc/kumihan/releases/tag/kumihan-sw-v0.1.0). Verify the SHA-256 list before unpacking.
2. **Claude Code:** extract `kumihan-mizani-claude-code-plugin-v0.1.0.zip`; inspect its `.claude-plugin/plugin.json`, then run `claude plugin validate /absolute/path/kumihan-mizani` and `claude --plugin-dir /absolute/path/kumihan-mizani` if supported. For a standalone skill, unpack into `.claude/skills/<skill-name>/`.
3. **Gemini CLI:** extract `kumihan-mizani-gemini-cli-extension-v0.1.0.zip`. The extension directory root contains `gemini-extension.json`; use `gemini extensions install /absolute/path/kumihan-mizani`. Standalone skills can be placed under `.gemini/skills/<skill-name>/`.
4. **Codex:** portable skill folders may be placed under `.agents/skills/<skill-name>/`. ChatGPT plugin and Gemini Apps import depend on client/account support and are not equivalent to Gemini CLI/Claude Code installation.
5. Try review mode first: `Use kumihan-mizani-review. Preserve the original Swahili text, including ng’ombe, and list layout observations without editing.`
6. Run optional offline read-only checks: `python runtime/checks.py original.txt --locale sw-TZ --candidate candidate.txt`.

Never assume a downloaded ZIP is registered with an AI provider's public marketplace. The name visible in the product is KUMIHAN｜Mizani; internal manifests use `kumihan-mizani` where required by host identifiers.
