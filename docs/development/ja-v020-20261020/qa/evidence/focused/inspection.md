# Focused diagnostics — exact bounded scopes

Authoring brief: compare actual scroll axis, optional OpenType display treatment and context-dependent copy. These are synthetic diagnostics, separate from the positive Web/report/deck artifacts. Inputs remain unchanged. Profiles web-editorial/web-marketing, default Standard review. Source: candidate kumihan and web/document/review entries, typography-context, typography-recipes-by-task, Japanese writing/type and recipes read during this QA.

Chromium 154.0.8037.57, 768 CSS px, local Noto Sans CJK JP. `tools/qa_ja_focused.py` reproduces HTML, screenshots and measurements. Both before-scroll.png and after-scroll.png were inspected by the parent agent (assisted visual judgment).

- PV-019 / WEB-001 rendered: vertical-rl paragraphs in vertically stacked pages have scrollHeight 813 > clientHeight 300, scrollWidth equals clientWidth 690; scrollTop changes to 350. Both images show the expected vertically scrollable window. Partial pages at window boundaries are scroll states, not absent source. This tests actual axis, not every narrow viewport.
- PV-021 / JA-TYPE-006: original condition deliberately has only syntax evidence and no real font. That original case remains not-checked for real effect. PV-022 is the separate executed resolved-font comparison; no blanket inference for all fonts.
- PV-022 / JA-TYPE-006 rendered + static font inspection: installed Noto Sans CJK JP regular TTC has GPOS `palt`; CDP reports NotoSansCJKjp-Regular for both samples. Normal display width 240px versus optional palt 235.359375px, visibly slightly tighter. No universal quality preference or reading-performance claim. JA-TYPE-005: body retains font-feature-settings normal; exact full protected string is separately present. No global palt cascade.
- PV-030 / CONTENT-001 static: exact quote `明日、こっちは17時で閉めます。` retained. The source does not establish an utterance date, store or permission to convert to standalone notice. These remain unknown. The longer contrast explicitly identifies itself as separate fictional QA text, not an inferred expansion of the quote. Contextual suitability is needs-review; no reader-comprehension experiment ran.

No native text zoom, native AI installation, native Office, physical sign/projection or reader study is established by these diagnostics.
