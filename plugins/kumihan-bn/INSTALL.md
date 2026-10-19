# Install KUMIHAN｜অক্ষরসজ্জা v0.1.0

## Claude Code plugin
Extract `kumihan-bn-Claude-Code-plugin-v0.1.0.zip` into a folder, then use the installation mechanism supported by your Claude Code version to register the directory containing `.claude-plugin/plugin.json`. The plugin includes all four skills. Do not claim Claude.ai or marketplace compatibility without host verification.

## Gemini CLI extension
Extract `kumihan-bn-Gemini-CLI-extension-v0.1.0.zip`. Use the local extension installation method supported by your Gemini CLI version (for example `gemini extensions install <extracted-folder>` when offered) with `gemini-extension.json` and `GEMINI.md`. Gemini Apps may support individual imported Skills where available; a Gemini CLI extension is not an Apps plugin.

## Standalone skills
Extract one of the four `kumihan-bn-*-skill-v0.1.0.zip` archives and register its folder using the host's supported Skills directory/install workflow. `SKILL.md` must sit at the root of each standalone skill and all referenced resources must be present. Review the host's current installation guide; installation is never achieved by merely pasting a ZIP as a chat attachment.

## Safest first run
Ask for a read-only review of: `কি কো কৌ ক্ষ জ্ঞ শ্র স্ত্র র‍্য ক্‌ষ অ্যা ৎ ড়`. Preserve exact Unicode sequences. Ask it to record the locale, original versus candidate hashes, risk suggestions and NOT_CHECKED for browser shaping and native-language proofreading.

## Update
Download the next release's complete package; review notes; install into a new folder or replace as permitted by the host. Do not silently rewrite a user's existing files or language profile.

## Evidence and limitations
The offline Python checker checks only byte preservation and a few static flags. It does not validate actual glyph shaping, paragraph line endings, browser/UI behavior, translation, editing quality, host installation or native speaker judgement. Those need separate evidence. See `references/workflow.md`.
