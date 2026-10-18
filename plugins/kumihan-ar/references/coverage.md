# Measured scope and reproducibility

The catalog derives 36 rule IDs and public citations from a research study; its 48 scenario proposals had no executable text and remain unrun as supplied. Product tests below define new explicit inputs and expected outcomes, rather than inheriting research success. The full suite is `python -m unittest discover -s tests/arabic` from the repository root.

| Rule | Implemented scope | Product test in tests/arabic/test_runtime.py |
| --- | --- | --- |
| AR-SRC-01 | Exact supplied bytes and metadata only | test_exact_bytes_metadata_and_protected_unicode; test_original_number_proposal_has_real_input |
| AR-SRC-02 | Source inequality retained even when derived NFC agrees | test_normalization_is_only_derived; test_nfkc_proposal_has_real_input |
| AR-LANG-02 | Explicit fa/ur exclusion and missing-language unknown | test_language_exclusions_and_locale_unknown; test_explicit_fa_does_not_get_arabic_tracking_checks |
| AR-BIDI-01 | Explicit root dir; inherited paragraph candidates | test_html_positive_negative_and_no_render_claim |
| AR-BIDI-02 | Mixed Arabic URL/email local-isolation candidate only | test_html_positive_negative_and_no_render_claim |
| AR-BIDI-05 | Presence of directional controls; intent needs review | test_control_tatweel_tracking_and_wrapping_are_candidates |
| AR-TYPE-01 | Inline letter-spacing candidate in explicitly Arabic elements | test_control_tatweel_tracking_and_wrapping_are_candidates |
| AR-TYPE-03 | Inline nowrap/break-all/hidden overflow candidate | test_control_tatweel_tracking_and_wrapping_are_candidates; test_intentional_nonjoining_label_is_not_failed |
| AR-TYPE-05 | Tatweel presence; never removed | test_control_tatweel_tracking_and_wrapping_are_candidates; test_exact_bytes_metadata_and_protected_unicode |
| AR-EVID-01 | Explicit static/rendered boundary in report | test_html_positive_negative_and_no_render_claim |

The remaining 26 catalog rules are guidance-only. Implemented-and-tested does not certify the full research rule or rendered behavior. Proposed scenarios F01 (digits changed), F02 (normalization changed), F04 (explicit non-Arabic language) and F05 (wrong root direction) informed the corresponding explicit product controls above; their original research execution statuses are unchanged.

Additional controls test input bounds and locale-dependent digits without conversion. Packaging tests verify fifteen exact filenames, full package inventories, digests, metadata order, five archives per host, deterministic output freshness, and actual runtime invocation after standalone extraction in temporary isolated directories. This is instruction-level and local Python execution evidence. Provider-native import, Arabic wording review, browser rendering, Office/PDF export, font fallback and copy interaction require separate measured evidence.
