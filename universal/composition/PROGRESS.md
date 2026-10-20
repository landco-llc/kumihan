# Execution ledger — plan: universal/development/composition-20261020/GOAL.md

Authority: user authorized W00–W08 and same Draft PR update. One continuous task; no scheduler. Reference design permission text is superseded only by this bounded authorization.

Pre-flight interfaces: W01 schema constrains W03 ranges, W04 module sidecar, W05 plan, W06 observations/audit. Exact schema is binding; no core keys added. W02 legacy byte ranges cannot enter W03 without explicit conversion. W04 preview declarations cannot become W06 verified evidence. W05 plan must bind full request, registry/dependency identity before W06 reuse.

Ruling: use universal/composition/ for implementation and durable ledger, rather than skill scratch scripts absent from this cloud package — preserves reproducible evidence in the authorized path; cost if wrong: relocate internal artifacts.
Ruling: Python jsonschema is the complete development validation path; PHP prototype only resolves an already validated sidecar/legacy registry, no PHP Schema conformance claim — avoids #118 Composer collision; cost: full native PHP contract validation remains an integration gate.

W00: complete — clean baseline, 21 modules, Python 29 + root21 green; PHP/Composer unavailable, upstream #101/#118 checks recorded separately.
W01: complete — exact approved schema, six record kinds accepted, unknown fields/version/status and malformed waiver rejected. Group A 6 tests GREEN.
W02: complete — read-only deep-copy legacy envelope/restore; never attaches fields to legacy record, rejects unverified checked claims. No public registration changes.

W03: complete — exact UTF-8 hashes; scalar ranges; byte-boundary adapter; source coverage, hierarchy and reference checks; invalid Unicode/digest/ranges/duplicates fail closed. Group B 16 tests GREEN.
W04: complete — exact declared locale only, no prefix/script/English fallback; trusted origin precedence with disagreements retained; equal-priority conflict stays und. Preview and declared capability states retained. PHP 8.5 Docker prototype RED (missing resolver) → GREEN, 14 cases. Host PHP absent, recovered with isolated read-only Docker; no dependency changes.
W05: complete (static candidate scope) — deterministic source/request/registry/dependency-bound plan, region expression/direction, relationships, hard constraints, scoped metadata conflict trace, font/host limitations. No shaping, optical sizing or broad language rule execution.
Ruling: evaluate one explicitly selected SourceStory per Audit, requiring source_id for multi-story requests — keeps exact artifact digest and evidence scopes unambiguous; cost: callers issue one audit per story. Corrected one test expecting an implicit multi-source target, without weakening target checks.
