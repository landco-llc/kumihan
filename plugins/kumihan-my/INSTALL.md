# KUMIHAN｜ဟန်ချက်

မြန်မာစာ မူရင်းကို မပြောင်းဘဲ စာစီပုံ၊ ခေါင်းစဉ်၊ ဝဘ်နှင့် စာရွက်စာတမ်းများအတွက် အကြံပြုချက်များ ပေးသည်။ | Source-preserving Burmese typography guidance for headings, web, interfaces and documents.

လိုအပ်သော Skill တစ်ခုချင်းစီကို သီးခြား ထည့်သွင်းနိုင်သည်။ မူရင်းစာကို သိမ်းထားပါ။
Each of the four Skills installs independently; retain the source unchanged.

GPT/Codex: install the plugin through a supported plugin interface, or copy the desired folder from skills/ into the host skill directory. The Codex manifest is .codex-plugin/plugin.json.

Claude Code: install the local plugin using /plugin install with the supported local/marketplace workflow; .claude-plugin/plugin.json supplies all four Skills. Standalone Skills go into the configured Claude skills directory.

Gemini CLI: run gemini extensions install PATH for the extracted extension and approve only its local context as appropriate; gemini-extension.json loads GEMINI.md. Alternatively install the individual SKILL.md folder using the host-supported Skills workflow.

Use a versioned host archive when supplied. ZIP extraction does not itself prove native host invocation. No server, credentials or font installation is required. Host commands and availability vary by client version; verify the supported workflow in that client.

The bundled bounded helper runs with Python 3: python runtime/check_source.py SOURCE --locale my-MM --medium review. Add --candidate FILE for exact-byte comparison; it never writes either input.

Checksum files: `SHA256SUMS-gpt-codex`, `SHA256SUMS-claude`, and `SHA256SUMS-gemini`; choose the file for your host.
