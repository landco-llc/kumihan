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
