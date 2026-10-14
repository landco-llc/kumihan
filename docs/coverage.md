# Coverage and evidence limits

Every standalone folder contains the same 38 independently authored guidance rules and six profiles. Counts describe guidance, not automatic detectors or successful production reviews.

| Family | IDs | Rules |
| --- | --- | ---: |
| Content | CONTENT-001 through CONTENT-005 | 5 |
| Japanese typography | JA-TYPE-001 through JA-TYPE-010 | 10 |
| Web | WEB-001 through WEB-008 | 8 |
| Documents | DOC-001 through DOC-004 | 4 |
| Design | DESIGN-001 through DESIGN-006 | 6 |
| Evidence | EVIDENCE-001 through EVIDENCE-005 | 5 |

The six profiles are `web-editorial`, `web-marketing`, `web-ui`, `report-document`, `presentation` and `display-copy`. Profile selection does not erase applicable rules outside that selection. See the [canonical rules](../rules/), [profiles](../profiles/) and [source registry](../sources/public-sources.json).

All 38 rule verification records declare `guidance-only`. Their methods distinguish static, rendered, assisted and manual review intent. The 57 declared case IDs are metadata, not integrated rule fixtures. The existing 19 offline verifier tests exercise structural integrity and negative controls, not 57 rule-specific production scenarios.

The [standalone checker](../scripts/check_standalone.py) inspects the fixed candidate's source snapshots, inventories, digests, safe paths, local resource closure, schema structure and bounded admitted syntax. The [public-boundary checker](../scripts/check_public_boundary.py) heuristically scans all tracked paths and UTF-8 text with no fixture exemptions. They do not execute targets, authenticate approvals, exhaustively detect disclosures, prove asset rights, evaluate native Office output or render typography.

Producer CI succeeded at exact commit `59630799fbf0a29089cdda4118734dae07078d2b`: [run 38525367349](https://github.com/landco-llc/kumihan/actions/runs/38525367349/job/115724354225) and [run 38525397671](https://github.com/landco-llc/kumihan/actions/runs/38525397671/job/115724454744). Run/job status was checked on 2026-10-14. That earlier producer reported 17 passing tests; status metadata alone does not show the test transcript. The current README-compatible checker revision is `f706a629208b101818975bdc794e7897b56773cd`, with 19 offline verifier tests. Its [run 38541607181](https://github.com/landco-llc/kumihan/actions/runs/38541607181) and [run 38541652680](https://github.com/landco-llc/kumihan/actions/runs/38541652680) also report success at that exact commit, checked on 2026-10-14. This is producer verification, not independent review. See [development](development.md) for reproducible local commands and [provenance](provenance.md) for exact source identities.

The seven report statuses remain distinct: `passed`, `failed`, `needs-review`, `not-checked`, `unsupported`, `waived`, `not-applicable`. A waiver is never a pass; schema validity is not permission. Future work requires actual host discovery/invocation, synthetic rendered web/report/presentation evidence, applicable native-app checks and independent review. Those results are pending and must not be inferred from static checks.
