# PR #120 shared-path coexistence handoff

WG10 result: the fixed Japanese and Ziheng changes coexist in a disposable synthetic tree after explicit composition of their shared records. The complete unmodified root suite passed 123 tests, with no skips; the Ziheng suite passed 26 tests. This is local compatibility validation, not an independent audit, a PR #120 change, or hosted CI evidence for either real PR. The actual PR #122 source and its baseline were not changed by this validation.

| Input | Fixed identity |
| --- | --- |
| Common main/base | `8b647cc752d7a9bc3db48356fa0ab7b221bb66d6` |
| PR #120 read-only HEAD | `ce2fd8d23e4afb0816b5870625e02af3aa7a96b8` |
| PR #120 tree | `0a654d87b38d036b2f7401e1de507696af8b1ba8` |
| PR #122 implementation commit | `6be142c57300de933caaae94a59436aa1f319a0b` |
| PR #122 implementation tree | `a819dc438089509c4ad5a4f399540059aab84b36` |
| Executable snapshot tree before JA composition | `186909ee9a7005ab51be19e3f4810e074798624f` |
| Final disposable synthetic tree | `d94fcc4b05436ce4ebe1a0bd5aeda45d955d6b56` |

The snapshot was taken from the working tree before the implementation commit. Every recorded file matches the implementation commit by SHA256, and all executable paths changed in that commit were included. The snapshot excludes unrelated untracked reports; it therefore has a different tree identity. See [snapshot](evidence/ja120-pr122-snapshot.json), [commit mapping](evidence/ja120-commit-mapping.json), and [composition/commands](evidence/ja120-coexistence.json). These are separate identities, not invented PR HEADs.

The required child route was GPT-6.1 Sol / high / Standard. The launch selected GPT-6.1 Sol / high; speed selection and serving-model attestation were unavailable. This bounded producer validation does not claim formal independent assurance.

## Shared records and conflict resolution

| Shared path | Coexistence result / handoff |
| --- | --- |
| `README.md` | Three-way merge was clean. Keep the JA source row/status from #120 and the ZH-HANT source row from #122. Regeneration preserves JA published v0.1.8 and Ziheng unpublished state. |
| `assets/edition-versions.json` | Three-way merge was clean. Merge records by edition: JA source 0.2.0 / published 0.1.8; ZH-HANT source 0.2.0 / published null / unpublished. Full records equal their respective fixed inputs; other records are unchanged. |
| `tools/build_version_site.py` | Three-way merge was clean. Preserve the JA exact transition admission before byte reads (including removed JA old archives), plus the Ziheng exact transition path in `preservation_allowed`. |
| `tools/check_seo_preservation.py` | Three-way merge was clean. Preserve the JA protected-file admission and additive Ziheng transition admission; neither helper replaces the other or the ordinary overlay check. |
| `docs/version-automation/preservation.json` | The only textual conflict was the README `after` hash. Rebuild the overlay from combined generated outputs. Keep the original `before` hashes and original SEO snapshot. All 330 PR #122 overlay records remain; only the README after-value changes in this synthetic composition. |
| `tests/test_version_naming.py` | Three-way merge was clean. Keep #120's dynamic JA source-version assertions, #122's exact validated Ziheng retained-manifest classification, current v0.2.0 expectations and old v0.1.0 checks, and the standalone tools import path. |

Reproduction used fixed Git archives and a three-way file merge under a disposable directory. The full JA implementation and ZIPs existed only there. No Git worktree was registered, no JA ref was changed, and no JA implementation or ZIP was copied into PR #122. Commands to regenerate the combined display were `python3 tools/build_version_site.py`, `python3 tools/build_gateways.py`, and `python3 tools/build_version_site.py --preservation`. The immutable SEO snapshot and frozen Ziheng transition preimages remained byte-identical.

A first assembly attempt used Git rename detection and left 15 superseded Japanese ZIP paths in the disposable tree. Its test run failed and is retained as [construction-error evidence](evidence/ja120-construction-error-first-run.log). Assembly was corrected by applying all 15 deletions from the fixed PR #120 diff with `--no-renames`; no real branch changed.

## Disposable baseline adaptation

The correctly composed tree first ran the complete suite with the original PR #122 scoped baseline: 123 tests, 7 subtest failures and 15 errors, all within `test_other_edition_facts_are_unchanged`. The inherited JA source record, six manifest/checksum files, and 15 renamed archives correctly differ from the pre-JA baseline. This run was not counted as passing; [original-baseline log](evidence/ja120-root-before-baseline-adaptation.log).

Only the disposable copy of `evidence/shared-integration-baseline.json` was then adapted: its JA edition record and 21 JA distribution entries were replaced with exact fixed PR #120 values, including the 15 v0.2.0 archive paths. Ziheng baseline facts and the other 234 protected entries were retained. No test was edited, removed, skipped or omitted. The actual PR #122 baseline remained byte-identical. Exact before/after hashes and fixed JA input digests are in [baseline adaptation](evidence/ja120-baseline-adaptation.json).

A future integration must establish its own accepted inherited-main baseline under its Work authority; this disposable adaptation does not rewrite historical evidence or approve either candidate's merge.

## Complete synthetic validation

| Command / evidence | Result |
| --- | --- |
| `python3 -m unittest discover -s tests -v` — [log](evidence/ja120-command-00.log) | 123 passed; 0 skipped |
| `python3 -m unittest discover -s tests/ziheng -v` — [log](evidence/ja120-command-01.log) | 26 passed; 0 skipped |
| `python3 tools/build_ziheng.py --check` — [log](evidence/ja120-command-02.log) | Exit 0; 165 outputs current |
| `python3 tools/build_ziheng_hosts.py --check` — [log](evidence/ja120-command-03.log) | Exit 0; 32 outputs current |
| `python3 tools/build_ziheng_site.py --check` — [log](evidence/ja120-command-04.log) | Exit 0; 13 outputs current |
| `python3 tools/build_dist.py --check` — [log](evidence/ja120-command-05.log) | Exit 0; JA source 0.2.0, 168 outputs current |
| `python3 tools/check_ja_type_011_cases.py` — [log](evidence/ja120-command-06.log) | Exit 0; 11 internal fixtures; rendering not asserted |
| `python3 tools/build_seo.py --check` — [log](evidence/ja120-command-07.log) | Exit 0; 274 page contracts, 272 sitemap URLs |
| `python3 tools/check_seo_preservation.py` — [log](evidence/ja120-command-08.log) | Exit 0; preservation passed |
| `python3 tools/build_version_site.py --check` — [log](evidence/ja120-command-09.log) | Exit 0 |
| `python3 tools/build_version_site.py --preservation --check` — [log](evidence/ja120-command-10.log) | Exit 0 |
| `python3 tools/build_gateways.py --check` — [log](evidence/ja120-command-11.log) | Exit 0; 22 gateways |
| `git diff --check` — [log](evidence/ja120-command-12.log) | Exit 0 |

[Semantic validation](evidence/ja120-semantic-validation.json) additionally records exact edition equality, combined README rows, both transition admissions, retained overlay records, and unchanged immutable preimages.

CI EVIDENCE NOT PRESENT

The line above applies to the disposable synthetic tree; no hosted run was submitted for it. Actual PR #122 CI is recorded separately in the main Work results. Future main integration and final CI must use then-current refs and generated hashes. No delivery to PR #120, push, approval, merge, Ready transition or production publication was performed by this child.
