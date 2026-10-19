# Instalacja / Installation — v0.1.0
PL: Wybierz ZIP zawierający v0.1.0, sprawdź MANIFEST.json i SHA256SUMS.txt i rozpakuj pakiet dla swojego narzędzia. Sam ZIP w rozmowie nie oznacza instalacji.
EN: Verify checksums and unpack a host-specific package or an independently distributed skill. Plugin display name is KUMIHAN｜Szyk; machine ID kumihan-szyk.
Claude Code: unpack the Claude-Code-plugin ZIP; validate using claude plugin validate /path/to/kumihan-szyk. Use supported Claude plugin loader. Standalone Claude skills can be imported if supported by your account.
Gemini CLI: unpack Gemini-CLI-extension ZIP to a folder containing gemini-extension.json at the root; run gemini extensions install /path/to/folder then gemini extensions list. Gemini app import requires host support.
GPT/Codex: unzip the GPT-Codex plugin; individual Codex skills may be placed at .agents/skills/. ChatGPT skill/plugin import depends on client availability.
Update: install the newly verified package; GitHub updates do not update installed copies automatically. Native host integration and marketplace listing remain unverified until tested.
