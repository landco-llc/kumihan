# Source-folder installation

The current candidate contains four complete, independent folders:

- `skills/kumihan/`: select the purpose, medium and authorized mode.
- `skills/kumihan-web/`: Japanese web pages, articles and interfaces.
- `skills/kumihan-documents/`: reports, documents and presentations.
- `skills/kumihan-review/`: read-only review; later refinement needs separate permission.

Each contains its own 38 guidance rules, six profiles, public source registry, local references, schemas, inventory and Apache-2.0 license. Copy the whole chosen folder. Do not install the canonical `skill-src/` fragments or copy only `SKILL.md`. No sibling folder, Python, development dependency or use-time network lookup is required by the guidance. Actual production tools, fonts and rendering depend on the host and authorized task.

## Proposed local Codex procedure

The [official skills documentation](https://developers.openai.com/codex/skills/) was checked on 2026-10-14 and redirects to the Build skills page. It documents repository discovery under `.agents/skills` from the working directory up to the repository root, and personal discovery under `$HOME/.agents/skills`. These documented locations are not observed KUMIHAN acceptance. Codex Cloud may expose a different installation mechanism; use the actual host's supported mechanism.

Start from a checkout containing the four folders, inspect it and record `git rev-parse HEAD` and `git rev-parse 'HEAD^{tree}'`. A generic clone of main does not necessarily contain this development candidate. From that checkout's root, the following shell example copies one complete folder into an already authorized target repository:

```sh
KUMIHAN_SOURCE="$PWD"
KUMIHAN_TARGET=/absolute/path/to/your/target-repository
KUMIHAN_SKILL=kumihan-review
test -f "$KUMIHAN_SOURCE/skills/$KUMIHAN_SKILL/SKILL.md" &&
  test -d "$KUMIHAN_TARGET" &&
  mkdir -p "$KUMIHAN_TARGET/.agents/skills" &&
  test ! -e "$KUMIHAN_TARGET/.agents/skills/$KUMIHAN_SKILL" &&
  test ! -L "$KUMIHAN_TARGET/.agents/skills/$KUMIHAN_SKILL" &&
  cp -R "$KUMIHAN_SOURCE/skills/$KUMIHAN_SKILL" "$KUMIHAN_TARGET/.agents/skills/"
```

Replace the target placeholder and choose one of the four exact skill names. Existing destinations deliberately stop this copy; inspect them separately. A personal local destination can instead be `$HOME/.agents/skills`, subject to the host's supported convention and permission. Do not assume this location is writable or recognized in Cloud.

After copying, start a fresh host session in the target and verify that the chosen skill is discovered, explicitly invoked, and can resolve its local resources in an unrelated workspace with no other KUMIHAN folders. Begin with a synthetic read-only request. These host checks remain pending; successful filesystem copying does not prove them.

The [Agent Skills specification](https://agentskills.io/specification), checked on 2026-10-14, describes `SKILL.md` metadata and optional resources, not a universal installation directory or host certification. No marketplace command or released archive is offered here. The historical ZIP builder is excluded from this source-folder delivery and is not an installation method. See [compatibility](compatibility.md) and [development](development.md).
