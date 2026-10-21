# KUMIHAN｜Samspel

## Svenska

Välj paket för ditt värdprogram. Installera pluginen i Codex eller Claude Code, eller tillägget i Gemini CLI enligt värdens aktuella anvisningar. Fyra Skills finns i `skills/`; varje mapp är självständig. Installera hela Skill-mappen, inklusive dess resurser. Den officiella ikonen finns i `assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png`. Ingen serveranslutning behövs.

Starta med ingången och ange medium, sv-SE eller sv-FI och tillstånd för textändringar. För lokal bytekontroll: `python runtime/check_source.py original.txt --locale sv-SE --medium review`. Verktyget läser och rapporterar; det skriver inte om originalet. Värdinstallation och faktisk rendering är inte verifierade av bytekontrollen.

## English

Choose your host package. Install the plugin in Codex or Claude Code, or the extension in Gemini CLI, following the host’s current instructions. The four folders in `skills/` are independent Skills; install the whole selected folder with its resources. The official icon is `assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png`. No server connection is required.

Use entry to establish medium, sv-SE or sv-FI, and permission to alter text. For local byte checks run `python runtime/check_source.py original.txt --locale sv-SE --medium review`. This reads and reports without rewriting. Byte checks do not verify host installation or rendering.

Checksum files: `SHA256SUMS-gpt-codex`, `SHA256SUMS-claude`, and `SHA256SUMS-gemini`; choose the file for your host.
