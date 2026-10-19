# KUMIHAN｜Equilibrio

Skill di IA open source per la tipografia italiana / Open-source Italian typography skills.
Version: 0.1.0. Author: L&Co. LLC. Apache-2.0. Free and open source.

Four independent skills: kumihan-equilibrio, kumihan-equilibrio-web, kumihan-equilibrio-documents, kumihan-equilibrio-review. Explicit it-IT/it-CH, original preservation and evidence-based review. In a plugin archive see skills/kumihan-equilibrio/references/coverage.md; in a standalone skill see references/coverage.md for limits. Research summaries are original; external fonts, private PDFs and protected article text are not bundled. Official KUMIHAN logo is supplied by the repository owner; external rights remain with their owners.

## Installation / Installazione
Verify SHA256SUMS.txt before extracting the matching versioned archive. All three host families provide a package and four standalone skills (15 ZIPs). Native host import/invocation and icon display are not-checked; provider marketplace listing is not verified.

ChatGPT/Codex: use the portable plugin only in a client supporting agent plugins. For Codex local skills copy the extracted skill directory to .agents/skills/<skill-name>/ or the supported user skill directory. This is distinct from ChatGPT private plugin registration. Availability and UI depend on the account/client; no universal install command is promised.

Claude Code: extract the Claude-Code-plugin archive; run `claude plugin validate /absolute/path/kumihan-equilibrio`, then `claude --plugin-dir /absolute/path/kumihan-equilibrio` where supported. Standalone Claude skills go in .claude/skills/<skill-name>/; chat attachment support depends on the product/account. No marketplace approval is implied.

Gemini CLI: extract the extension archive into a directory with gemini-extension.json at its root, then use `gemini extensions install /absolute/path/to/folder` and `gemini extensions list` on a supporting CLI. Gemini Apps skill/file support is account dependent and differs from extensions. Standalone skills contain their own references; attach/select only through supported client features.

Test with: “Usa kumihan-equilibrio-review; conserva nomi, valori e testo originale.” Confirm the assistant reports source preservation and unchecked rendering. The offline helper `python skills/kumihan-equilibrio/runtime/checks.py original.txt --locale it-CH --candidate candidate.txt` from the extracted plugin root (for a standalone skill, use `python runtime/checks.py` from its own root) only prints JSON; it does not validate host import.

## Updates / Aggiornamenti
Keep originals, compare version and SHA-256, replace only the matching product folder, and recheck your local paths and client support. No silent content migration or destructive cleanup. Public release target: kumihan-it-v0.1.0; source website kumihan-it.html. GitHub release availability is separate from marketplace status.
