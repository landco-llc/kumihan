# KUMIHAN｜លំនឹង — Installation / ការដំឡើង

Use the `kumihan-km-v0.1.0` public GitHub Release to download versioned ZIPs and compare `SHA256SUMS.txt` before importing. ZIP filenames contain `v0.1.0`; the visible name remains **KUMIHAN｜លំនឹង**.

**Claude Code plugin:** extract `kumihan-lumnung-claude-code-plugin-v0.1.0.zip` preserving the `kumihan-lumnung` folder, run `claude plugin validate /absolute/path/kumihan-lumnung`, then `claude --plugin-dir /absolute/path/kumihan-lumnung` where supported. Independent skills can go under `.claude/skills/<skill-name>`.

**Gemini CLI extension:** extract `kumihan-lumnung-gemini-cli-extension-v0.1.0.zip`, then run `gemini extensions install /absolute/path/kumihan-lumnung` where supported. Independent skills can go under `.gemini/skills/<skill-name>`.

**Codex:** install the individual skills under `.agents/skills/<skill-name>`. **ChatGPT** import/skill availability varies by account; ZIP upload is not automatic marketplace registration.

Review prompt: “Use kumihan-lumnung-review to review this Khmer design and text without changing the original source. Include rule IDs and evidence status.”

Offline check: `python runtime/checks.py source.txt --locale km-KH --candidate rendered.txt`.

Automatic source conversion, unapproved Khmer spelling changes and universal browser pass claims are out of scope.
