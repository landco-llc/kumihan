# स्थापना | Installation

Download the host-specific v0.1.0 ZIP and verify SHA256SUMS.txt. Extract one enclosing kumihan-hi directory; no dependencies or server are required. Standalone Skill ZIPs contain one Skill directory with its own references/icon/license.

## ChatGPT / Codex
Use the host's supported plugin import/local-plugin UI when available. ChatGPT plugin and Skill UI availability depends on account and host version. A ZIP attached to a chat is reference material, not plugin installation. For Codex standalone Skills, extract the chosen directory into ~/.agents/skills/ and start a new session; verify the skill is listed. Do not overwrite an existing installation without checking the version.

## Claude Code / Claude Skills
Extract the Claude plugin, run `claude plugin validate /absolute/path/kumihan-hi`, then `claude --plugin-dir /absolute/path/kumihan-hi`. For standalone Skills, copy the skill directory to ~/.claude/skills/ (or the project .claude/skills/) and verify discovery. Claude chat custom Skill support depends on the plan/UI; uploading a ZIP in chat does not install a Claude Code plugin.

## Gemini CLI / Gemini Skills
Extract the extension and run `gemini extensions install /absolute/path/kumihan-hi`, then `gemini extensions list`. Confirm the extension and all four Skills are discovered by the installed CLI version. Standalone Skills use the CLI's supported `gemini skills install /absolute/path/skill-directory` flow; check `gemini skills --help` for your version. Gemini app file attachment is contextual reference, not CLI extension installation.

## Update and remove
Verify a new release checksum, replace the selected local version using the host's normal flow, restart and inspect discovery. Use the host uninstall command/UI for plugins/extensions; remove only the installed Skill directory for manual Skill installation. Keep project documents separately.

Try: “मूल पाठ बदले बिना क्षि क्षी त्रि ज्ञ श्र स्त्री की समीक्षा करें।” Ask for the rule ID, evidence kind and NOT_CHECKED list. Native host installation has not been performed in this build environment; schemas and archive contents are tested separately.

## हिंदी में संक्षिप्त स्थापना

अपने होस्ट का v0.1.0 ZIP डाउनलोड करें और SHA256SUMS.txt से मिलाएँ। प्लगइन में चारों Skills हैं; स्वतंत्र Skill ZIP भी अपने सभी नियम, संदर्भ और आइकन के साथ काम करता है। Codex में Skill फ़ोल्डर को ~/.agents/skills/ और Claude में ~/.claude/skills/ में रखें। Claude Code प्लगइन को validate करके --plugin-dir से चलाएँ। Gemini CLI एक्सटेंशन के लिए निकाले गए kumihan-hi फ़ोल्डर का पथ दें। ChatGPT और अन्य चैट ऐप में उपलब्ध समर्थित आयात UI जाँचें; केवल ZIP संलग्न करने से प्लगइन स्थापित नहीं होता। अपडेट से पहले अपने बदलाव सुरक्षित रखें और नए चेकसम जाँचें। वास्तविक होस्ट स्थापना इस वातावरण में नहीं की गई है।
