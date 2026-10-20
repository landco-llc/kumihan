# KUMIHAN JA v0.2.0 implementation result

Workgroup: KUMI-JA-V020-RESEARCH-WG-20261020-01. State: source candidate / Draft review; no publication acceptance.

## Fixed inputs and preservation

Base main: `8b647cc752d7a9bc3db48356fa0ab7b221bb66d6`; fixed instructions: `b3262f6bfedafb576b38c7d70f8ca1bd83a2672e`. Fresh fetch matched the observed main. Initial work branch was clean; existing work branch retained. Implementation branch: `feat/ja-v020-research-20261020`. Control delta consists only of WORKGROUP and RESEARCH_CASES; both match the attachment exactly. All packet file byte counts/SHA-256 verified (baseline.json).

## Work and scope

- W00: recorded866 baseline protected hashes, current main, input manifest and baseline91 tests passing. No root AGENTS.md found.
- W01: all4 entries route to region/role/readingTask/attributed intent and evidence guidance; required-information mapping and independent experimental sidecar draft. Existing report fields unchanged.
- W02: corrected CSS safety, language/glyph, ordinary display spacing, optional palt, tabular digits, scroll-axis, enlargement and language-run override claims. Historical Chromium141 recipe observations remain historical.
- W03: corrected font/projection certainty, ordinary wrapping first, oversized tables, extraction versus preview/native; retained old evidence history. No common document-generation feature added.
- W04: reusable writing/type history, conditional task comparisons and supplied97-source claim ledger with URLs/dates/classification/limits. Sources were read from supplied research, not independently re-fetched. No optimal-size or performance claims introduced.
- W05: all30 planned cases materialized as synthetic JSON contract fixtures with exact original source, expected scopes and negative decisions; planned execution fields remain unexecuted. Actual observations are separate in case-results.json.11 partially-run /19 not-run; no full30-case real-environment pass claimed. Real Chromium154 screenshots at1024/320, spacing override, actual button click and2-page Chromium PDF/PyMuPDF preview recorded. Parent inspected narrow Web and both PDF page images. PV-006 meaning remains needs-review; clipping negatives remain failed artifacts.
- W06:4 JA manifests0.2.0, shared references/inventories synchronized;15 archives CRC/size/hash/path verified and second rebuild byte-identical. Published Release metadata remains0.1.8. Other-language archives/manifests,39-rule catalog,6 profiles and schemas unchanged (evidence/preserved.json).
- W07: existing generators updated source/publication panels, README and authored Japanese/English installation notes. `kumihan.html` remains its Jekyll entry. Generated fragment screenshot is not a deployed full-site check. MCP_HANDOFF.md explicitly leaves Universal production separate.
- W08: independent read-only agent review plus parent review;4 concrete findings corrected. Regression results below. No claims of native invocation, physical or all-browser acceptance.
- W09: implementation candidate and evidence prepared for Draft PR/Issue119; NEXT_GATE.md preserves Owner publication gate.

## Verification and failures

Baseline:91 tests passed. New contract tests first failed (2 failures/2 errors), then passed after guidance/fixture changes. First full regression had5 failures: stale JA source facts, hardcoded active archive version and old-source preservation checks. Initial rendering via file URL was blocked by browser policy; own synthetic HTML was rendered with set_content instead. No target code or external document instruction executed.

Immutable SEO snapshot remains unchanged. Separate source-transition.json records exact before/after hashes only for explicitly bounded JA source paths. Old0.1.8 working-tree ZIP removals are admitted; missing active files and changed digests fail. Existing version-display overlay remains generated. This is a reviewed source transition, not a change to immutable Release assets. Mutation regression tests retain rejection of unrelated changes.

Final checks:

| Command | Result |
| --- | --- |
| python -m unittest discover -s tests -v |96 passed |
| python tools/check_ja_type_011_cases.py |11 specification fixtures internally consistent; not rendered success |
| python tools/build_dist.py --check |0.2.0,168 generated files current |
| python tools/build_seo.py --check |272 URLs,274 page source contracts pass |
| python tools/check_seo_preservation.py |pass; immutable snapshot retained |
| git diff --check |pass |
| second python tools/build_dist.py |byte-identical15 ZIPs and host manifests/checksums |

See evidence/ for initial/final logs, rendering JSON/images, PDF, Unicode negative, preservation, reproducibility and independent review. Exact implementation revision is recorded in revision.json after candidate commit; it identifies the tested implementation before this reporting-only record. The PR head includes the final reporting commit.

## Candidate archives

These are unpublished source candidates. Old public assets are immutable.

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `downloads Claude/plugins/kumihan-Claude-Code-plugin-0.2.0.zip` | 509143 | `78eb29f367d9c0014709825a6f45f496e75930db77fc4b2198590092a2edeba1` |
| `downloads Claude/skills/kumihan-Claude-skill-0.2.0.zip` | 124375 | `44d87e11078c48de44eea2d18aacdef74ba67620bab6b23adbe4592b031c76ca` |
| `downloads Claude/skills/kumihan-documents-Claude-skill-0.2.0.zip` | 124694 | `d09b422f8f149fffd51c1e79f3ef3050ec7d5604f99fdaf9e9dcbe0d78a68242` |
| `downloads Claude/skills/kumihan-review-Claude-skill-0.2.0.zip` | 124674 | `d292651bb180d688b5328857607ca34f6f05f31b005f76634b9cb95f301a5d69` |
| `downloads Claude/skills/kumihan-web-Claude-skill-0.2.0.zip` | 124727 | `858c6eea185817a4ac228087ea88efd06d8d9428a6fe2ad0f19e0954b792e3c6` |
| `downloads GPT-Codex/plugins/kumihan-GPT-Codex-plugin-0.2.0.zip` | 1309156 | `1f8b2aaa943cd619dd9b3ffa918fc144f3c76d08c097472a2e9c372bcc1564f2` |
| `downloads GPT-Codex/skills/kumihan-GPT-Codex-skill-0.2.0.zip` | 124375 | `44d87e11078c48de44eea2d18aacdef74ba67620bab6b23adbe4592b031c76ca` |
| `downloads GPT-Codex/skills/kumihan-documents-GPT-Codex-skill-0.2.0.zip` | 124694 | `d09b422f8f149fffd51c1e79f3ef3050ec7d5604f99fdaf9e9dcbe0d78a68242` |
| `downloads GPT-Codex/skills/kumihan-review-GPT-Codex-skill-0.2.0.zip` | 124674 | `d292651bb180d688b5328857607ca34f6f05f31b005f76634b9cb95f301a5d69` |
| `downloads GPT-Codex/skills/kumihan-web-GPT-Codex-skill-0.2.0.zip` | 124727 | `858c6eea185817a4ac228087ea88efd06d8d9428a6fe2ad0f19e0954b792e3c6` |
| `downloads Gemini/extensions/kumihan-Gemini-CLI-extension-0.2.0.zip` | 506683 | `db68ec074cc45fecb48b1748f2048ab4f9a3ea73fcdbc362aafd353cd037cd3a` |
| `downloads Gemini/skills/kumihan-Gemini-Apps-skill-0.2.0.zip` | 123799 | `067236ccd6b23ce97e50651a4bf4ee29cac8fa22de4b1240cf4df37845a58de8` |
| `downloads Gemini/skills/kumihan-documents-Gemini-Apps-skill-0.2.0.zip` | 123398 | `a0997a0f216fcecfefc0520f557240ae03c09d2f298c883e65d984e24969fc0d` |
| `downloads Gemini/skills/kumihan-review-Gemini-Apps-skill-0.2.0.zip` | 123594 | `f36b62bdbdc76330dc6e8a72602fee1b7937c82eed99a07b3decfd3492526231` |
| `downloads Gemini/skills/kumihan-web-Gemini-Apps-skill-0.2.0.zip` | 123863 | `3a07dd00511cfaf1b6c9ca15ea6fc83007a4db52862404c209167583bfe943cc` |

## Limits and next gate

No native AI-host/Office invocation, user-native text zoom, regional glyph/OpenType certification, real projection/sign environment, reader experiment, Marketplace submission or production deployment.19 planned scenarios remain not-run; fixture contracts do not turn them into observed outcomes. The supplied research originals retain their research-time not-run/unadopted wording. Optional draft sidecar is not a production schema extension. No unresolved observed source blocker is concealed, but this evidence does not authorize shipping acceptance.

Owner reviews candidate content, new preservation transition, CI and archives before merge/publication. See NEXT_GATE.md and MCP_HANDOFF.md. No main push/merge, tag, Release publication, Pages production update or Marketplace submission performed.
