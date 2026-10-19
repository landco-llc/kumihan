# KUMIHAN v0.1.8-preview — GitHub Release result

**Status:** PUBLISHED, VERIFIED (GitHub Release).
**Owner decision:** 2026-10-19, “承認。進めて” — accept PR #102 and publish the reviewed v0.1.8 preview candidate.
**Published at:** `2026-10-19T10:27:49Z` (2026-10-19 19:27:49 JST).
**Release:** https://github.com/landco-llc/kumihan/releases/tag/v0.1.8-preview
**Release ID:** `417160813`
**Git tag:** `v0.1.8-preview`, annotated tag object `c2eb0890d5a8420a6005c2ba53e4b684724bdf38`
**Immutable source commit:** `b7a8c83f2a8fa2cb5b7cdca4d38a728b4226eb92` (merge PR #102)
**Release state:** `draft=false`, `prerelease=true` (not a stable/GA claim).

## Scope and approval

1. PR #100 had already been merged, introducing six optional use-case adapters, conservative Japanese/English route selection with manual override, and Standard/Strict design-review guidance. The six media profiles, 39 rule IDs, frozen public schemas and independent language modules remain unchanged.
2. [PR #102](https://github.com/landco-llc/kumihan/pull/102) was reviewed as a **documentation-only** change, passed its three hosted CI checks and was merged. Merge commit `b7a8c83f2a8fa2cb5b7cdca4d38a728b4226eb92`.
3. The release tag was created non-forcefully **after** verifying no existing `v0.1.8-preview` ref. Annotated tag-peel was verified against the exact PR #102 merge commit. Older release tags and assets were not moved.
4. A draft prerelease was created, 15 ZIPs were attached, and its uploaded asset list was checked **before** publication. Only after matching 15/15 manifest sizes/digests and tag target was `draft=false` applied.
5. The GitHub API was reread after publication, and all 15 ZIPs were independently downloaded from the public Release using GitHub CLI.

## Verified release artifacts

- **15/15** assets present, state `uploaded`, unique filenames, and matching size and `sha256:` digests to the three source `MANIFEST.json` files.
- **15/15 public asset downloads** rehashed and matched the fixed source ZIPs exactly. Combined downloaded size: **3,045,346 bytes**.
- Public GitHub Release page returned HTTP **200**.
- Each platform includes one plugin/extension ZIP and four standalone Skill ZIPs: ChatGPT/Codex 5, Claude 5, Gemini 5.
- All three source MANIFEST archives contained five entries and corresponded to source SHA-256 plus `SHA256SUMS.txt`. Each ZIP's internal file list, member sizes and member digests were checked.
- Source acceptance before tag: `python3 -m unittest discover -s tests -q` — **59 tests PASS**; `python3 tools/build_dist.py --check` — **148 generated files up to date**; JA-TYPE-011 — **11 source fixtures consistent** (not a rendered test).
- Synthetic rendered QA remains published as bounded evidence at `docs/design-quality/RENDERED_FIXTURE_QA_20261019.md`; full source/visual QA packet is in the project Drive `30_EXECUTION/KUMIHAN_DESIGN_QUALITY_RENDERED_QA_20261019`.

## Boundaries and unresolved items

- No native ChatGPT/Claude/Gemini invocation was conducted in this publication step.
- Browser text-only zoom, native Microsoft PowerPoint/Keynote, physical print/CMYK, AI-authorship detection and cross-language design quality are **not verified**.
- This prerelease does **not** claim automatic visual-quality scoring, self-directed image creation, permission to edit source in audit mode, or production-wide design certification.
- PR #93 (SEO) and PR #101 (multilingual MCP), and the independent locale-plugin distribution releases, are outside this release. No merge/retag for those projects is implied.
- README, CHANGELOG, updates guide and this receipt were updated **after the immutable release tag** in a separate documentation-only PR. The immutable release ZIP files were not changed to reflect post-publication copy.
- Drive decision log records the Owner approval, publication and verification facts separately from prior draft-stage notes.

## Links

- Release: https://github.com/landco-llc/kumihan/releases/tag/v0.1.8-preview
- PR #100: https://github.com/landco-llc/kumihan/pull/100
- PR #102: https://github.com/landco-llc/kumihan/pull/102
- Bounded QA report: https://github.com/landco-llc/kumihan/blob/b7a8c83f2a8fa2cb5b7cdca4d38a728b4226eb92/docs/design-quality/RENDERED_FIXTURE_QA_20261019.md
