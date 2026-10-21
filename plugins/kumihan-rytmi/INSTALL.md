# KUMIHAN｜Rytmi

Tarkista jakelun SHA256SUMS-* ennen purkamista. Valitse isännällesi sopiva v0.1.0-paketti. Itsenäinen taito sisältää omat säännöt, lähteet, apuohjelman, lisenssin ja virallisen kuvakkeen; muita taitoja ei tarvita.

Verify distribution SHA256SUMS-* before extracting the matching v0.1.0 edition. Each standalone Skill includes its own rules, references, helper, license and official icon; no sibling installation is required.

GPT/Codex: pura taitohakemisto isännän määrittämään skills-hakemistoon tai käytä paikallisen lisäosan asennusta. Claude Code: `claude --plugin-dir /absolute/path/kumihan-rytmi`; itsenäiset taidot `.claude/skills/`-hakemistoon. Gemini CLI: `gemini extensions link /absolute/path/kumihan-rytmi`; itsenäinen taito isännän tukemaan skills-hakemistoon. Tarkista asennetun version ohje.

GPT/Codex: extract a Skill into the host-configured skills directory, or use its local plugin flow. Claude Code: `claude --plugin-dir /absolute/path/kumihan-rytmi`; standalone Skills go in `.claude/skills/`. Gemini CLI: `gemini extensions link /absolute/path/kumihan-rytmi`; standalone Skills use the host-supported skills directory. Check your installed CLI help for version-specific support. Native invocation is not_checked.

Suorita taidon hakemistossa / Run inside a Skill: `python runtime/check_source.py SOURCE --locale fi-FI --medium review`. `--candidate FILE` vertaa tavut kirjoittamatta / compares exact bytes without writing. Tallenna omat muutokset ennen päivitystä / preserve local edits before updates. Tarkista uusi versio ja tiiviste / verify the replacement version and hash.

Checksum files: `SHA256SUMS-gpt-codex`, `SHA256SUMS-claude`, and `SHA256SUMS-gemini`; choose the file for your host.
