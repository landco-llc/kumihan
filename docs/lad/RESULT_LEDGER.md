# KUMIHAN｜Лад v0.1.0 — /goal W00–W08 実行記録

## Completed on candidate branch

- W00 — Fresh Read: KUMIHAN main, Japanese canonical layout, reusable installer, RU research source.
- W01 — 48 contextual rules, authoritative/exception labels and no unsafe universal edits.
- W02 — Four standalone Skills: entry/web/documents/review; Russian/English descriptions; official icons.
- W03 — ChatGPT/Codex, Claude Code and Gemini CLI plugin manifests. Display name exactly `KUMIHAN｜Лад`.
- W04 — Deterministic 15 ZIP generation (4 Skills + 1 plugin × 3 hosts), SHA256SUMS.txt, manifest. GitHub Actions build step succeeds before site compilation.
- W05 — RU/EN/JA product pages and nine install guides, canonical Japanese CSS and install frame, conditional Cyrillic font fallback, Russian label fix. Added `ru` to six-language homepage generator and generated six gateway pages.
- W06 — Candidate-integrity CI, RU unit/package/build CI and canonical site parity. Successful CI example: https://github.com/landco-llc/kumihan/actions/runs/39162911613 . The earlier PR gateway failure was due to stale index pages; now handled in `tools/build_gateways.py` source and its generated outputs.

## Publication gate W07

- Merge this PR only after latest source and cross-language CI pass.
- On main push, the workflow should create public GitHub Release `kumihan-ru-v0.1.0` with **15 ZIPs + MANIFEST + SHA256SUMS**, immutably.
- Verify real tag, uploaded assets, main branch, and GitHub Pages URLs. Do not claim publication before that readback.

## Honest unverified boundaries W08

- Native installation/invocation inside Claude, Gemini, ChatGPT has not been demonstrated by repository CI.
- Mother-tongue Russian copy editing and real-browser/Office/PDF rendering are separate acceptance tasks.
- No third-party marketplace approval implied. OSS security audit is intentionally lightweight.

Source research: https://drive.google.com/drive/folders/12l8XF3yMYHpfP80aAkmhUVO4LYFxXYQP

## 2026-10-19 release conflict resolution

The multi-language gateway is shared by many concurrently publishing editions. To preserve unrelated Bengali/Indonesian cards, the Russian product release is **decoupled from global gateway regeneration**. Localized RU/EN/JA landing pages link to the language gateway as navigation. A separately coordinated gateway registration remains a follow-up, not a blocker for releasing the independently addressable Russian product. This supersedes the earlier W05 claim of shipping gateway cards in the same commit.

## W07 verified public release — 2026-10-19

- **PR #72 MERGED:** https://github.com/landco-llc/kumihan/pull/72
  - Merge SHA: `c7ba2dbe236c421f70222a976f042522aecdc75d`
- **Release PUBLISHED:** https://github.com/landco-llc/kumihan/releases/tag/kumihan-ru-v0.1.0
  - `tag=kumihan-ru-v0.1.0`, non-draft, non-prerelease; published `2026-10-19T04:08:49Z`.
  - Immutable published tag target: `106b0306e2b28ff2e858342d9a0a77acdecbbe42`.
  - GitHub API returned **17 assets**: 15 v0.1.0 ZIPs (4 Skills + one host plugin for each of ChatGPT/Codex, Claude, Gemini), `MANIFEST.json`, `SHA256SUMS.txt`.
  - The GitHub release API returned each artifact's size and SHA-256 digest; release assets exist. Native host import remains a different test.
- **CI SUCCESS:** https://github.com/landco-llc/kumihan/actions/runs/39197988836
  - Source/unit: **6/6 PASS**.
  - Reproducible distributable build: **15 ZIPs**.
  - Canonical landing / installation site: **13 generated and 13 verified**.
  - Site tests: **2/2 PASS**.
  - Main output-cleanliness gate: PASS.
  - GitHub Release creation step: PASS.
- **GitHub Pages DEPLOY SUCCESS:** https://github.com/landco-llc/kumihan/actions/runs/39197988301
  - Pages built from tagged-release-era main at `106b0306e2b28ff2e858342d9a0a77acdecbbe42`.
  - Published source routes: `kumihan-ru.html`, `kumihan-ru.en.html`, `kumihan-ru.ja.html`, and nine `docs/install-lad-{host}{suffix}.html` guides.
  - **Limitation:** an external live HTTP fetch was not available from the verification environment. The Actions deployment result is not asserted to prove real-browser visual inspection, 320px/200% readability, or native host invocation.
- **Global gateway card:** deliberately not modified in the release integration because the shared gateway was under simultaneous changes from other language editions. This affects discovery from the KUMIHAN language index only; the product URLs and their RU/EN/JA language switches are published.
- **Third-party catalog:** GitHub marketplace configuration includes the Claude source entry but there is no claim of approval by external marketplaces.
- **Quality scope:** bounded OSS tests; Russian native-editor review and live display/host smoke tests remain separately `not-checked`.

This verified outcome supersedes the publication gate statements above that were written while the release was still pending.
