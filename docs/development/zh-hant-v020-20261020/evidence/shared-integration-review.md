# PR #122 shared integration — one lightweight technical review

Date: 2026-10-20 JST. Review context: same-task Child under the producer Runtime Parent; nonformal technical review/self-validation. This is not an independent audit, independent PASS, merge-readiness decision, or release authorization.

## Fixed identity and authority

- Repository: `landco-llc/kumihan`; PR #122; branch `feat/zh-hant-v020-research-20261020`.
- Reviewed source HEAD: `6be142c57300de933caaae94a59436aa1f319a0b`; TREE: `a819dc438089509c4ad5a4f399540059aab84b36`.
- Integration start: `773289a1dc7d04627a7cd3b539eb640f65c40fa8`; main/base: `8b647cc752d7a9bc3db48356fa0ab7b221bb66d6`.
- Requirements: Owner-bounded `KUMI-ZIHENG-V020-SHARED-INTEGRATION-20261020-R1`, WG11; scope and boundaries recorded in `SHARED_INTEGRATION_PLAN.md`. Private instruction was read; its link and full text are excluded.
- Fresh Read: global AGENTS, applicable DG control/routing/proportionality guidance, current Work, integration plan and exact diff. No repository or nested AGENTS was found. Agentic Change Audit skill and its relevant normative references informed identity/evidence discipline; the exact Work limits this result to one lightweight review.
- Required route supplied by Parent: `gpt-6.1-sol` / `high`, requested/default Standard. Parent owns accepted launch evidence; provider serving metadata and speed readback are not independently observable here.

At live readback PR #122 remained OPEN/Draft at the integration-start commit; this review therefore covers the fixed local source commit before normal push. Remote main matched the stated base. Final local HEAD/TREE remained unchanged, with no tracked working-tree drift. Other workers were adding untracked validation/handoff evidence; those additions are outside this immutable source review.

## Scope and observed checks

Reviewed the entire 58-path integration delta, concentrating on the six shared paths, localized generator/version-label dependencies, preservation/transition records, retention admission and six new negative/boundary regression methods. The original 220-path candidate and its four prior corrective findings were not re-audited. Existing correction history remains intact.

Observed read-only checks in the repository:

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_ziheng_v020_shared_integration.py' -v`: exit 0; six methods succeeded. These exercise exact historical-manifest retention, unrelated/unregistered history rejection through the original assertion, corrupt/deleted legacy ZIP rejection, unknown transition path and altered preimage/baseline/snapshot/after rejection, other-edition preservation, and source/download/publication distinction.
- Direct immutable `git show` comparisons and SHA-256 checks: exit 0. All 255 protected baseline files match both START and reviewed HEAD byte-for-byte, including retained/current ZIPs, other-language distributions, original SEO snapshot and inactive release contract. Edition JSON differs only in `zh-hant.source_version` becoming `0.2.0`.
- Immutable HTML comparison: all 34 generated HTML files retain every `href`/`src` sequence; all 22 gateways differ only inside the ZH-HANT card. The 12 Ziheng pages distinguish source v0.2.0 from retained v0.1.0 downloads and preserve unpublished status.
- Immutable overlay/transition comparison: no existing overlay row removed; existing before hashes retained. All transition preimages and the frozen baseline remain unchanged; 12 generated-body after-values changed and every transition after-hash matches the reviewed output.
- `git diff --check START HEAD`: exit 2, solely for three trailing spaces in raw captured failure logs (`shared-regression-red.log:4`, `shared-root-before.log:14,82`). These preserve test-run evidence and have no program effect. This is a formatting limitation, not a material correction request. A clean working-tree `git diff --check` is a different check.

Implementation and separate validator logs report root118 and Ziheng26 successful tests plus generator/distribution/SEO/preservation checks. I read their command records and test summaries; I did not rerun those complete suites or recast precommit working-tree evidence as final hosted CI. Parent retains responsibility for final evidence attribution and PR #120 coexistence reconciliation.

## Findings and limits

No blocking or non-blocking findings.

The retention change calls the existing exact validated Ziheng manifest exception; it does not exclude arbitrary history. Both transition hooks are additive and retain existing shared behavior. Generated labels preserve old URLs while identifying v0.1.0 downloads, and no publication fact is advanced by the source bump.

No additional reviewer or repeat review was used. No correction, repository write, commit, push, approval, Ready transition, merge, publication, or PR #120 change was performed by this reviewer. No AL2/AL3, host-proof, Office/AT/native-language/real-UA200%/glyph acceptance was demanded or inferred. Browser, ZIP CRC/public URL checks and synthetic coexistence are separate validator evidence, not reproduced here.

CI EVIDENCE NOT PRESENT

This statement concerns hosted CI for the reviewed pre-push source commit. Old-head CI and local successful checks do not substitute for final-head hosted evidence.

Technical review result: no actionable defect identified within the bounded integration delta. Next permitted action: Parent/publisher completes the already-authorized Draft PR evidence update and normal push, then reads final-head CI and returns the fixed candidate to the Owner Gate. Main merge, Ready, tags, Release, production Pages, Marketplace and MCP adoption remain unauthorized. This source review applies only to the exact identities and scope above; later documentation-only publication requires Parent attribution, while any material source change ends its applicability.
