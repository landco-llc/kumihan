# KUMIHAN

[日本語の使い方](README.ja.md)

KUMIHAN is a planned v0.1 skills product for Japanese web and document production. It helps agents preserve source content, make deliberate typography and layout decisions, and report the evidence they actually obtained. v0.1 is not a published release. This documentation branch contains contracts and public drafts; integration, standalone bundles and host acceptance are pending.

## Planned skills

| Standalone skill | Purpose |
| --- | --- |
| `kumihan` | Establish purpose, medium, mode, permissions and protected content; select relevant resources. |
| `kumihan-web` | Guide editorial, marketing and UI production, Japanese typography and conditional reflow review. |
| `kumihan-documents` | Guide reports and presentations: hierarchy, pagination, notes, source data and render review. |
| `kumihan-review` | Review an existing target read-only and report findings. |

The catalog preserves **38 guidance rules**, not 38 automatic detectors. The six profiles are `web-editorial`, `web-marketing`, `web-ui`, `report-document`, `presentation` and `display-copy`. See [coverage](docs/coverage.md).

## Choose the effect before using a skill

| Mode | Intended effect |
| --- | --- |
| `study` | Explain applicable guidance and options; no target edits. |
| `build` | Create the requested artifact within explicit output and tool permissions. |
| `audit` | Inspect and report; no target edits. |
| `refine` | Edit only the explicitly authorized target and scope. An audit needs new explicit refine authorization before changes. |

State the audience, objective, medium, output target, allowed tools, editable scope and protected content. Preserve names, prices, values, units, punctuation, variation selectors and decomposed Unicode unless a specific change is authorized. A valid schema or a skill instruction does not grant permission. Record structure, typography roles, actual asset provenance, brand constraints, rejected defaults and exceptions before generation. Cards, gradients and symmetry are judged against purpose rather than universally prohibited.

For example: “Use kumihan-review in audit mode for this Japanese article. Preserve all source text. Review narrow-screen layout using the available renderer; report unavailable checks. Do not edit.” Invocation syntax depends on the host and remains unverified here.

## Installation and evidence

Once a verified bundle is available, copy **one complete standalone skill folder** to a host-supported skills location, retaining its `SKILL.md` and included references. Consumers need neither Python nor `jsonschema`, a sibling repository, nor a separate planning service. [Installation](docs/installation.md) explains local Codex locations and the pending Cloud discovery check. There is no KUMIHAN marketplace command or published download claimed here.

Use the host's actual production tools when available and authorized. Browser rendering, PDF/slide conversion and font access are optional capabilities of the host, not supplied by KUMIHAN. Without a renderer, report visual checks as `not-checked` or `unsupported`; never infer a typography pass from text alone. Reports distinguish `passed`, `failed`, `needs-review`, `not-checked`, `unsupported`, `waived` and `not-applicable`. A pass needs relevant evidence and a named method. A bounded waiver is distinct from a pass. Model judgment is assisted/manual, not deterministic verification.

Schema and package checks establish structural properties, not factual truth, visual beauty, legal originality or actual host behavior. There is no native Office, all-browser or other-provider certification. [Compatibility](docs/compatibility.md) remains pending/unverified until observed host records exist.

## Public project

KUMIHAN is independently authored under the existing [Apache-2.0 LICENSE](LICENSE). It imports no Hallmark source, prose, assets or dependency, and bundles no fonts. Public references inform guidance; they do not certify legal originality or grant rights to external material. See [provenance](docs/provenance.md) and [third-party notices](THIRD_PARTY_NOTICES.md).

[Contributing](CONTRIBUTING.md) · [Security](SECURITY.md) · [Development](docs/development.md) · [Architecture](docs/architecture.md) · [Release checklist](docs/release-checklist.md) · [Changelog](CHANGELOG.md)
