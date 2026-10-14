# Installation draft

No v0.1 release or verified consumer bundle is published by this documentation draft. Do not copy `skill-src` fragments as if they were complete standalone bundles. Build and verification require integrated product inputs; see [development](development.md).

After a verified bundle exists, inspect its inventory and extract it safely. The frozen builder interface produces a ZIP with top-level `kumihan/`, `kumihan-web/`, `kumihan-documents/` and `kumihan-review/` directories. Select one complete folder and retain all included references and profiles, license and inventory. It must work without the other three folders or a sibling repository. Do not overwrite an existing installed skill without inspecting it.

## Codex locations: documented, not observed installation

The [official Codex skills documentation](https://developers.openai.com/codex/skills/), checked on 2026-10-13, redirects to the current Build skills page. It documents local repository discovery under `.agents/skills` from the working directory up to the repository root, and user discovery under `$HOME/.agents/skills`.

For a repository-local installation, the intended resulting path is `.agents/skills/kumihan-review/SKILL.md` when choosing `kumihan-review`. For personal local discovery, it is `$HOME/.agents/skills/kumihan-review/SKILL.md`. Copy the complete `kumihan-review/` folder, not only its Markdown entry point. These are documented local locations; successful discovery, invocation and standalone use in Codex Cloud are pending/unverified. Follow the actual host's current supported mechanism rather than assuming Cloud exposes local user installation.

The [Agent Skills specification](https://agentskills.io/specification), checked on 2026-10-13, defines a directory with `SKILL.md`, YAML `name` and `description`, and optional resources. It does not define a universal install location or certify a host. Host documentation is evidence, not permission to install or execute tools. KUMIHAN does not provide marketplace installation commands in this milestone.

Consumers need neither Python nor `jsonschema`. The skill guidance has no use-time network requirement; optional browsing, production or rendering tools depend on the actual host, available assets and explicit permissions. No font files are bundled. Verify discovery and a read-only request before trusting the installation; record missing tools honestly in the report. See [compatibility](compatibility.md).
