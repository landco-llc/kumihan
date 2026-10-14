# KUMIHAN

[日本語](README.ja.md)

**Japanese typography for thoughtful AI-assisted design.**  
**日本語の文字組みから、AIのデザインをもっと自然に。**

KUMIHAN is an open-source project building reusable skills for creating and reviewing Japanese websites, articles, documents, and presentations with AI.

We focus on readable Japanese typography, clear information hierarchy, and layouts that fit the content rather than relying on generic templates.

## What KUMIHAN aims to help with

- **Japanese typography** — Line breaks, punctuation, spacing, and Japanese–Latin text.
- **Thoughtful layouts** — Readable, well-organized pages and presentations tailored to their purpose.
- **Content integrity** — Keeping original wording, names, and figures intact.
- **Design review** — Checking readability, visual structure, and layout issues.

## Four independent skill folders

| Skill | Intended use |
| --- | --- |
| [kumihan](skills/kumihan/SKILL.md) | Select guidance for the content and medium. |
| [kumihan-web](skills/kumihan-web/SKILL.md) | Support Japanese web pages, articles, and interfaces. |
| [kumihan-documents](skills/kumihan-documents/SKILL.md) | Support documents, reports, and presentations. |
| [kumihan-review](skills/kumihan-review/SKILL.md) | Review existing work without changing the original. |

## Availability

**v0.1 is in development; no release or published bundle is established here.** Four complete folders are checked in under `skills/`. Each includes 38 guidance rules, six profiles, cited standards, local references, schemas, inventory and license. Any one folder can be copied independently; consumers need neither Python nor development dependencies, sibling folders or a use-time network lookup.

These are guidance workflows, not 38 automatic detectors. They help select `study`, `build`, read-only `audit`, or explicitly authorized `refine` work using available host tools. Host discovery and invocation have not been tested. Rendering, native Office compatibility and automatic approval resolution are not verified or provided by these static checks. Independent review is pending.

[Installation](docs/installation.md) gives proposed source-folder instructions. [Coverage](docs/coverage.md) and [compatibility](docs/compatibility.md) separate current checks, unsupported features and future work. [Development](docs/development.md), [provenance](docs/provenance.md), [contributing](CONTRIBUTING.md), [security](SECURITY.md) and [third-party notices](THIRD_PARTY_NOTICES.md) explain the evidence and boundaries.

## License

[Apache License 2.0](LICENSE)
