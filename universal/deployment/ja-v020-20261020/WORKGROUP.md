# Universal MCP — Japanese module v0.2.0 integration / production rollout

**Owner authority:** 2026-10-20 JST explicitly requested "KUMIHAN Universal MCPにも反映". This authorizes the **existing connected Universal MCP's Japanese module** to consume released source v0.2.0, including a minimal backward-compatible way to return its Japanese typography research guidance, and a guarded production update on the already deployed host IF actual private access, checksum preconditions and rollback are verified. It does NOT authorize OpenAI/Claude/Gemini Marketplace submission, unrelated LanguageRouter fixes, Composer upgrades or a general runtime replacement.

- Workgroup ID: `KUMI-UNIVERSAL-JA-V020-20261020-01`
- Tracker: [Issue #127](https://github.com/landco-llc/kumihan/issues/127). Dependency: verified Japanese GitHub release [Issue #126](https://github.com/landco-llc/kumihan/issues/126).
- Control branch: `control/universal-ja-v020-20261020` off Universal Draft PR [#101](https://github.com/landco-llc/kumihan/pull/101) head `5d32ea64618e33a171705363c223fe43060c31e1`.
- Source candidate for JA: [PR #125](https://github.com/landco-llc/kumihan/pull/125) head `1f205124cee538235f4cee384ca67f414c5e0e26`, not a publication tag. After Issue #126 finishes, **use the verified immutable `v0.2.0` tag**, not a movable branch. JA source plugin.json version `0.2.0`.
- Existing MCP endpoint: `https://mcp-kmhn.landco.co.jp/mcp`. Current connected MCP returns 21 modules; Japanese module version `0.1.8`, JA Universal normalized rule candidates `78` (source Japanese canonical catalog `39` IDs); Japanese module hash `ec67c409db050ae3fe371c795fabe614d99b406d563bf3e270ce160e22332b93`.
- Live 21-module digest snapshot and pinned source-reference inventory: [MODULE_CONTRACT.json](MODULE_CONTRACT.json). This snapshot must be re-read against actual live before deployment. Any unexpected drift requires reconciliation rather than resetting other languages.
- Source Universal branches [#101](https://github.com/landco-llc/kumihan/pull/101), [#118](https://github.com/landco-llc/kumihan/pull/118) (Composer lock), [#116](https://github.com/landco-llc/kumihan/pull/116) (Marketplace publication control), Traditional Chinese [#122](https://github.com/landco-llc/kumihan/pull/122) remain distinct. Do not merge/rebase those into main as a side effect of JA.
- Execution: Codex Cloud/App for repository, diff, tests and package. Hosting deployment requires **authorized account-specific remote access**; perform from approved host/runtime only and never assume Cloud holds SSH secrets. Do not use Remote Desktop merely to run local Codex CLI.

## Product behavior and key v0.2.0 gap

Current `universal/tools/build_registry.py` generates a 21-module registry by ingesting module `plugin.json`, entry `SKILL.md`, and `rules/*.json` only. It does NOT ingest `skills/kumihan/references`. `UniversalTools.php::getGuidance` currently returns a 4500-byte `entry_guidance` fragment and a limited rule list, not referenced v0.2.0 `typography-context.md`, `typography-recipes-by-task.md`, `japanese-writing-and-type.md`, Web/document recipes or evidence guidance. The JA v0.2.0 SKILL entry itself is longer than 4500 bytes. **Changing registry version alone is not sufficient**: the new role/intent/evidence/conditional-layout guidance would remain inaccessible or truncated.

The MCP remains read-only guidance-only. **No text-editing tool, automatic rule pass, browser renderer, presentation generator or arbitrary source-file server is approved** by this task. Keep the existing four tool names and input signatures:
- `kumihan_list_languages`
- `kumihan_detect_language`
- `kumihan_get_guidance`
- `kumihan_review_text`

A backward-compatible OPTIONAL `reference_guidance` field to `getGuidance`, populated from an explicit build-time allowlist for Japanese 0.2.0, is preferred. The response MAY include `source_path`, SHA-256, relevant text/summary, `truncated` or `not_checked` marker. It MUST NOT let a client choose an arbitrary path or cause runtime filesystem reads/URL fetches, and must not flood responses with the approximately 78 KB research claim ledger.

## W00 — Fresh Read and dependency admission

- [ ] Read [Release Issue #126](https://github.com/landco-llc/kumihan/issues/126), verify Release `v0.2.0` is **public, non-Draft**, tag points to the reviewed actual merged main commit, and all 15 source ZIPs match hashes. If not yet verified, complete independent read-only source/schema design but HOLD live source-switch and distribution claims.
- [ ] Fetch current PR #101 head, source `universal/languages.json`, `universal/tools/build_registry.py`, `universal/server/src/Registry.php`, `UniversalTools.php`, `LanguageRouter.php`, `universal/server/tests/smoke.php`, `universal/tests`, deployment target current facts, and #116/#118/#122 heads. Pin all actual SHAs to source log; preserve unrelated changes.
- [ ] Invoke currently connected MCP: list_languages, get_guidance JA, review_text JA source-preserving, detect_language Japanese/ambiguous Chinese. Compare JA v0.1.8/78 and 20 other module digests to `MODULE_CONTRACT.json`. A known router false-positive for Chinese punctuation is independent work; do NOT silently include LanguageRouter changes or claim repaired by this JA update.
- [ ] Confirm actual live registry and PHP source identities using an authorized private read-only host check where available. No private paths/account/usernames/passwords written to GitHub.

## W01 — Release-source import and scoped build

- [ ] On a **new integration branch based on fresh PR #101** (do not rewrite PR #101/#116/#118), import only the released JA `plugin.json`, four Japanese SKILL entries and shared JA references/rules/profile/schema that are necessary to regenerate the exact new Japanese module. No import of entire main, 236 QA artifacts, all 20 other plugins or unrelated HTML.
- [ ] Pin each JA source file to tag `v0.2.0` with exact SHA-256 and provenance. Verify 39 canonical Japanese rule IDs and existing schema/status untouched.
- [ ] The 20 other modules' exact current live IDs, versions, source digests, normalized rule counts and guidance MUST remain identical to `MODULE_CONTRACT.json` (prefer preserving the production registry old entries verbatim in the final delta if the PR #101 builder source would otherwise drift).
- [ ] Run base registry generation and unit tests on the release-source snapshot. A generated local `registry.json` is not a deployed registry. Show a clear old→new JA module diff and 20 exact unchanged module hashes before proceeding.

## W02 — Make actual v0.2.0 guidance accessible via existing tool

- [ ] Implement a **bounded build-time allowlist** of Japanese v0.2.0 references:
  - `skills/kumihan/references/typography-context.md` — role, readingTask, intent attribution, expressionMode, required-info/evidence contract.
  - `skills/kumihan/references/typography-recipes-by-task.md` — comparison starts, medium task, limits.
  - `skills/kumihan/references/japanese-writing-and-type.md` — historical/type/linguistic background and caution.
  - `skills/kumihan/references/web-recipes.md` (when web/display).
  - `skills/kumihan/references/document-recipes.md` (when document/presentation/print).
  - `skills/kumihan/references/review-protocol.md` (bounded context if review/audit).
  - `skills/kumihan/references/research-claims.json` — metadata only (large claim ledger, DO NOT embed or expose 78 KB in every call).
- [ ] Return selected source-backed context through optional `reference_guidance` field **without changing existing `getGuidance` argument schema/old fields**. Cap returned text budget, mark truncation and preserve UTF-8 boundaries. Do not overwrite or edit original file contents. Per-medium selection must not imply a file was rendered, externally verified or all research was reread.
- [ ] For JA full entry: avoid raw-byte substring cutting in the middle of UTF-8/markdown; use safe bounded full entry or explicit source-backed excerpts with `truncated`. The original `entry_guidance` field must remain backwards-compatible.
- [ ] Registry module digest SHOULD include SHA-256 provenance of the actually delivered JA refs (otherwise the advertised module digest cannot detect changes to served guidance), while keeping all 20 non-JA module hash algorithms/results byte-identical.
- [ ] The additional field is static data, not instructions supplied by clients; its content is source/documentation to be interpreted with the user's request, not a new authority, waiver or automatic audit.
- [ ] Retain original `rules_total`, advisory`candidate_requires_context` semantics, preview status and read-only `reviewText` checked=[] / not_checked scopes; no 'rendered PASSED' promotion.

## W03 — Static, PHP 8.5 and protocol validation

- [ ] Add unit tests: direct JSON registry build 21 languages, JA version=0.2.0 from pinned source, JA digest changed, 20 other module IDs/versions/digests unchanged and no permissions/unknown report schema changes.
- [ ] PHP 8.5 lint, Composer/SDK smoke with **pinned compatible lock from #118 where applicable**. If lock integration is separate/unavailable, do not accidentally upgrade Composer packages or clobber the existing installed vendor tree just for JA module update.
- [ ] Protocol tests for `list_languages`, `detect_language`, `get_guidance` in `ja/web`, `ja/document`, `ja/presentation`, `ja/display-copy` and one non-JA module, `review_text` with `髙﨑さま／料金１,２００円／が` unchanged.
- [ ] Confirm JA `reference_guidance` actually contains role/intent/required-info and relevant task recipe text; 20 other modules' response shape/versions remain accepted.
- [ ] Failure tests for missing reference, invalid Unicode, unsafe path, oversized data, unknown module/mode, stale registry and ambiguous Chinese punctuation; preserve known language-router regression status, do not claim this W fixes it.
- [ ] Verify exact HTTP session/Origin/current SDK transport behavior before making a server-side source change; no new public endpoint or write privileges.

## W04 — Proposed public-source PR and deploy packet

- [ ] Create dedicated Draft stacked PR against PR #101 for minimal changes to registry builder and existing PHP guidance (plus test files/docs). Explicitly account for #118 Composer lock and #116 Marketplace publication control without merging unrelated work.
- [ ] Record per-file changed SHA/hashes, JA before/after module version/digest, 20-module comparison, SHA of PHP file and generated registry, test/CI and L&Co. LLC ownership.
- [ ] Package **private** deployment candidates for existing Lolipop PHP 8.5 MCP with only allowed files. Never commit runtime/config.php, credentials, SSH targets/home paths, private session payloads, or raw request logs. Public source may document relative file roles only.
- [ ] If exact live PHP source differs from pinned expected, test a compatibility patch against *that observed version*; do not replace the entire private runtime from old PR #101.

## W05 — Private hosting preflight and reversible rollout

Private deployment on already connected `https://mcp-kmhn.landco.co.jp/mcp` is within the owner's scoped request, **only if**:
1. Authorized connection to the actual Lolipop host is available; no credential paste/upload to chat or GitHub.
2. Private runtime directory is verified outside *all* exposed Web roots. Source PHP, current registry and session config are readable and hash-pinned. Current exact 21 modules / JA 0.1.8 / nonJA digests match the preflight baseline.
3. Protected server tree, PHP 8.5 extensions, SDK and session write compatibility are verified without changing configuration; no wildcard public exposure.
4. Old registry/PHP files are backed up with byte hash and actual rollback path/test, separately protected from the new files.
5. Package diff includes only Japanese module data and essential optional PHP guide reader. There is no blanket deployment of #101/#116/#118/#122, and no modifications to private config or session store.

**Change sequence (backwards-compatible):** stage candidate data; lint/smoke in a private staging copy; atomically switch the compatible PHP reference reader first while old registry remains valid; then atomically switch the registry. Run immediate live probes. If regressions arise, reverse the sequence: restore previous registry first, then prior PHP, re-probe JA 0.1.8 and 20 others. Do not flip a public bootstrap/symlink or restart unrelated services without proof. If filesystem/permission/SCP capability cannot support an atomic rollback, stop at `ACCESS_NEEDED` instead of unsafe partial deployment.

## W06 — Real connected MCP readback (mandatory for "reflected")

After actual rollout, call the existing connected Universal plugin:
- [ ] `kumihan_list_languages`: still 21; JA version **0.2.0**, JA digest matches staged released module, other 20 entries/version/digests bitwise same before vs after.
- [ ] `kumihan_get_guidance(language=ja, medium=web/document/presentation/display-copy)`: `module_version=0.2.0`, source-backed `reference_guidance` really contains v0.2.0 context/conditional recipes and clear not-checked limits. Verify no broken character from entry truncation.
- [ ] `kumihan_review_text` on protected Unicode and a deliberately awkward headline: source unchanged, no automatic PASS for unrendered checks, 0.2.0 module_version, proper advisory status.
- [ ] `kumihan_detect_language` for Japanese Kana, explicit `ja` and `zh-Hant`, and known mixed/ambiguous Chinese punctuation. Preserve the router's pre-existing status rather than claiming it fixed.
- [ ] Validate 3 independent non-JA guides (e.g. `zh-Hant`, `ar`, `fr`) remain same digest and guidance; actual Streamable HTTP handshake/session if credentials/client available.
- [ ] Re-read actual remote PHP/registry hashes and private log boundaries, no raw request texts. Store only sanitized evidence in GitHub.

**Do not use output from a local php test to claim live v0.2.0.** The direct connected plugin must return the new module and usable reference material, or state `DEPLOYED_UNVERIFIED` / `NOT_DEPLOYED` with the exact blocker.

## W07 — Completion, rollback evidence and owner report

Write `universal/deployment/ja-v020-20261020/RESULT.md` on source branch with exact repo/PR/tag SHA/TREE, module-before/after SHA, all 20 unchanged SHA records, PHP/SDK tests, live connected plugin results and rollback route; state every unverified host behavior.

Report once in [#127](https://github.com/landco-llc/kumihan/issues/127) and source [#119](https://github.com/landco-llc/kumihan/issues/119), linking GitHub Release [#126](https://github.com/landco-llc/kumihan/issues/126), source Draft PR, deployment result. Keep Marketplace/public listing separate; no new adapter version or native host certification.

No additional Owner approval loop for the explicitly scoped Japanese update when all conditions hold. If account-specific SSH access/rollback/private path is unavailable, report `ACCESS_NEEDED` with a single exact operator-run deployment packet and stop only the live-write operation. Source/tests/PR may finish independently. All 20 other modules and customer use must be preserved.

**The creation of this document does not prove registry was updated, deployed, or a 0.2.0 result was observed.**
