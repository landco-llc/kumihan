# NEXT_GATE — fixed source candidate, integration still blocked

1. Coordinate the six shared paths already owned by Japanese PR #120. Review/apply the exact Ziheng-only source-version/README/preservation/test transition in `shared-integration.patch` against the then-current main. This patch was validated in isolated staging; it is not active on this branch. Rebase/reconcile normally, do not force-push another writer. Preserve all other edition facts. The patch also updates gateway Ziheng badges; no other translations or distributions are changed. Re-run complete tests and build/SEO/preservation checks against the actual integrated HEAD. Until then this candidate is **not merge-ready**.
2. Owner decides whether the fixed source candidate may merge after the integration blocker and checks are resolved. No main merge is authorized by this report.
3. Formal Release requires a separate naming/asset-contract decision. `release-assets-proposal.json` proposes unique flat15 names; source ZIP paths stay intact. The currently unconfigured contract is not activated. No tag/Release exists from this work.
4. Production Pages, Marketplace/registration ZIP adoption and native-host acceptance are separate gates. Existing downloads stay available; this source update is not an automatic installed-user update.
5. MCP integration belongs to its separate lane. Use MCP_HANDOFF.md; no live registry/server is changed here.

Remaining observations are scoped: real UA200%, regional font/glyph/IVS support, selected vertical/ruby operations, clipboard/navigation, native Office/PDF and AT, physical projection/signage, TW/HK native-language proofreading. These are not fabricated as32 passes, nor automatically made universal release blockers for unused features.

No routine approval request is pending; authorized independent work has been carried through to this concrete Draft candidate. Owner Gate remains closed for publication and production actions.

The one review is recorded in evidence/final-review.md. Its four P2 findings were corrected by the author and checked with regression tests; this is not a second independent review or permission to bypass the shared integration hold. The transition preimages are frozen in source-transition-baseline.json and pinned by the unactivated helper digest.
