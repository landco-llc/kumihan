# Experimental composition core — 0.1.0-design.1

Internal, offline, read-only candidate. Implements the bounded W00–W08 static portions of [GOAL](../development/composition-20261020/GOAL.md). No public MCP tool, adapter registration, deployment or distribution change. Existing 21 language packages remain independent preview guidance.

Python 3.12+ and existing `requirements-dev.txt` (`jsonschema==4.26.0`) provide development JSON Schema Draft2020-12 validation. Schema bytes/ID remain exactly approved. PHP Resolver.php is an isolated PHP 8.5 **exact-locale prototype for prevalidated records**, not a full PHP contract validator. Full PHP Schema support requires a separate dependency/integration gate with #118.

From the repository root:

```sh
python3 -m unittest discover -s universal/tests -v
PYTHONPATH=universal/composition python3 -m unittest discover -s universal/composition/tests -v
python3 universal/tools/build_registry.py --output /tmp/kmc-registry.json
python3 universal/tools/build_registry.py --output /tmp/kmc-registry.json --check
python3 universal/composition/cli.py validate request.json
python3 universal/composition/cli.py resolve request.json --registry /tmp/kmc-registry.json > plan.json
python3 universal/composition/cli.py evaluate request.json --registry /tmp/kmc-registry.json --plan plan.json --source-id s0 --target exact-story.txt > review.json
php universal/composition/tests/php_resolver_smoke.php /tmp/kmc-registry.json
```

Fixture requests are constructed in tests/fixtures.py and tests/test_acceptance.py. They are synthetic, not approved translations or native-language editorial corpus. CLI `validate` checks structure for all six kinds plus source/range/reference semantics for requests. Structural acceptance of an audit/observation/module does NOT authenticate its passed/verified/waiver claims. Error JSON contains named code/location and no source text. Exit 0 means the stated static command succeeded; exit 2 is a bounded-input error.

`resolve(request, legacy_registry, candidates=[]) -> Plan` returns schema-valid metadata and hard constraints, with missing modules/hosts and conflicting language annotations recorded. `candidates` is a local in-process argument: each item has exactly run_id, language_tag, origin. It records extra annotations for an existing exact run, never changes coverage. It is not a transport envelope or a new public API. Author → user → document metadata → detected → fallback precedence; same-priority contradictory tags become und. No script-based selection, prefix fallback or English pivot. Registry locale declarations alone permit exact case-insensitive selection; e.g. zh-Hant-TW is accepted only if explicitly present. All declared capabilities remain declared; this phase has no verified capability promotion path. Script analysis, language detection, IANA registry/deprecated lookup and all language-specific rule execution remain outside this prototype.

Plan IDs bind complete canonical request, complete registry, dependency identities, candidates and engine version through the noncritical `kumihan:composition-binding` extension. This namespace is output-only. Other noncritical extensions are preserved, never executed; all critical extensions stop. Reuse requires regenerating the deterministic plan and comparing every field. Hard preservation/direction/boundary/required-content constraints precede cosmetic preferences. Composition metadata is proposed or resolved by explicit provenance; resolved metadata does not mean layout has passed. This phase proposes no font size, optical ratio or discretionary line break; absolute versus relative units and font metrics remain unavailable.

`evaluate(request, plan, registry, observations=[], target=None, source_id=None) -> (Audit, Observation[])` inspects **one** selected logical UTF-8 SourceStory. Multiple stories require source_id and separate audit calls. `target`, if supplied, must be exactly that story's UTF-8 file; HTML markup, PDF or Office extraction is not implemented. Files are opened only for bounded reads and pre/post bytes compared. Without target it checks the supplied logical source only. The result's artifact_ref is that source's ID, never a claim of whole-document verification. Scope/reference/digest checks on supplied observations do not authenticate facts; caller observations never promote rendering, native/editorial, verified alignment or approval results. Waivers remain an external mandatory approval gate and cannot be granted here.

Every passed static check refers to a generated source-bound Observation. Render, shaping, font geometry, wrapping, native editor, visibility, screen reader, visual display exceptions and optical correction stay not-checked. Unknown modules are unsupported; ambiguity is needs-review. Bidi controls, CRLF, NBSP, marks, ZWJ/ZWNJ and variation selectors are preserved. Scalar zero-based half-open offsets are distinct from legacy byte offsets; byte_range_to_scalar rejects non-boundary byte positions. Metadata boundaries do not prove safe shaping boundaries.

Legacy adapter: contract.legacy_snapshot/restore_legacy use a **separate local envelope**, deep-copy the original report unchanged, map status/not_checked only and refuse unauthenticated checked claims. They do not append any key to old reports or merge root JA 39-rule and Universal JA 78-rule scopes. There is no invented conversion of guidance into passed checks.

Limits: 1 MiB combined UTF-8 source, 128 stories, 4096 items per request array, 128 ancestor levels; CLI files at most 16 MiB (registry includes existing guidance). Limit errors request source-based splitting and never return partial success. Ref strings are opaque identifiers; no URLs, fonts, code, telemetry or network calls are executed. No supplied document text is logged. Audit digest is not asserted to anonymize tiny secrets.

For the exact verified scope and pending host/publication gates see RESULT.md, TEST_REPORT.md, NEXT_GATE.md and EVIDENCE_MANIFEST.json. P01–P40 is a registration matrix, not forty passes.

Region selections preserve the original full source-run range when intersecting a region; they do not represent clipped, applicable style spans. Any future applying host adapter must intersect explicitly and verify shaping-safe boundaries. `validate_audit_binding` requires the current registry, revalidates the request and deterministic plan, and accepts passed static facts only when the complete observation equals freshly recomputed internal source/plan evidence; supplied fact names or host strings alone cannot authenticate a pass.
