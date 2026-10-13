# Coverage and evidence

The planned catalog has 38 guidance rules: content 5, Japanese typography 10, web 8, documents 4, design 6, evidence 5. Counts describe retained IDs, not automatic detectors. Six media profiles select relevant rules without deleting the remaining catalog.

Fifteen priority IDs are `CONTENT-001`, `CONTENT-002`, `CONTENT-004`, `JA-TYPE-002`, `JA-TYPE-004`, `JA-TYPE-005`, `JA-TYPE-006`, `JA-TYPE-008`, `JA-TYPE-009`, `WEB-001`, `WEB-004`, `WEB-005`, `DESIGN-001`, `DESIGN-002`, `EVIDENCE-001`. Positive, negative and exception cases are planned for each: at least 45 case records. Case integration is pending; case counts do not prove host execution. The other 23 IDs remain visible with explicit coverage.

Each rule declares method (`static`, `rendered`, `assisted`, `manual`) and coverage (`implemented`, `guidance-only`, `planned`, `unsupported`). Implemented coverage must refer to an actual detector or documented tested procedure, not a default inferred from a valid schema. Typography and design remain assisted, rendered or manual where no detector exists. Exact source-content comparison is machine-checked only when a supported fixture/extractor supplies exact text.

Reports use these distinct statuses:

| Status | Meaning |
| --- | --- |
| `passed` | Relevant observed evidence supports the bounded check with a named method. |
| `failed` | Evidence demonstrates a requirement failure in the stated scope. |
| `needs-review` | Judgment or evidence needs further review. |
| `not-checked` | The check was not performed. |
| `unsupported` | The available environment cannot perform the check. |
| `waived` | A bounded current approval permits an exception; it is not a pass. |
| `not-applicable` | A stated condition excludes this particular scope. |

Include artifact identity/digest, profile, ruleset version, scope, reason, evidence references, actual environment, limitations and content changes. A waiver must bind the exact artifact and scope, with authority and currency verified by the host; an opaque reference alone grants nothing. Do not publish private approval records.

Missing rendering is `not-checked` or `unsupported`, never a visual pass. Model judgment is assisted/manual. Schema validity does not establish evidence authenticity, semantic truth, copyright ownership or visual quality. Package integrity does not establish host compatibility.

Narrow viewport review is separate from text zoom, text-spacing changes, browser engines and native Office rendering. Reflow conditions depend on writing direction and applicable regions; do not turn one viewport dimension into universal conformance. Native output and font substitution require actual observation. See [compatibility](compatibility.md) and [architecture](architecture.md).
