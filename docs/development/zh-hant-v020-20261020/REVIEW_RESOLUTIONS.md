# Single review correction record

Reviewed source HEAD3322d4840421cce4b53df64cd88d2f2e791ab3f8; no second review dispatched.

| Finding | Correction | Evidence |
|---|---|---|
| CI PyYAML dependency | Existing pinned requirements-dev.txt installed by Ziheng workflow; permissions remain contents:read. | Requirement file and corrected workflow; remote CI is reported separately. |
| Old hash not validated | Unactivated local transition helper validates independently frozen baseline file digest and exact main_before, snapshot_before and candidate after. The active preservation overlay is not used as its own preimage. | test_old_hash_and_candidate_hash_must_both_match; original reviewer probe; red/green review-fix logs. |
| Global history exception | Shared test patch now calls exact digest-validated is_retained_manifest; other-product and unregistered history remain in the prior assertion. | test_history_exemption_only_accepts_exact_retained_ziheng_manifests; staging112 suite. |
| Static bytes accepted as glyph | Known regional-glyph/ivs-glyph passed scopes require rendered method; font/glyph observations still required. Ordinary static-byte checks remain browser-independent. | test_glyph_scopes_cannot_pass_with_static_byte_evidence; source/standalone regeneration; new21 and Ziheng26 tests. |

Ruling carried from execution: pause overlapping shared paths under the instruction's #120 writer rule and supply a concrete unapplied patch. Cost: actual branch remains blocked by4 root checks and cannot merge until coordinated integration/retesting. No finding was silently declined. Remaining font/glyph/UA200%/Office/AT/native-review uncertainty stays explicit in case-results and NEXT_GATE.
