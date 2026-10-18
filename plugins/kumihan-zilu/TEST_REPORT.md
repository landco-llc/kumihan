# KUMIHAN｜字律 — v0.1.0 verification

简体中文排版指导与只读审查。 / Simplified Chinese typography guidance and read-only review.

This candidate provides workflow instructions and bounded static checks, not an automatic typography engine. Catalog `implemented` means a workflow or limited static capability. 20 advisory-only entries require target-environment or editorial evidence; vertical layout and ruby are deferred. See `rules/zh-hans-cn.json` for per-rule scope, source sections, exceptions and change authority.

The original 44 synthetic research cases are retained as test fixtures. `tests/zilu/acceptance-results.json` distinguishes **3 full cases passed, 41 not-run**, and **44 narrower source-preservation subchecks passed**. A byte comparison passing does not pass a layout, typography, business-action or Office export scenario.

Local checks: eight unittest methods including all 44 preservation subchecks, deterministic 15 ZIP generation, safe ZIP paths/modes, internal per-skill inventory hashes, no private Drive URLs, source references, twelve-page language and local links. Other-language regression: Japanese 5 tests + 11 spec fixtures; ZiHeng 23 tests; Korean 9 tests; Thai 16 tests; all five existing product/host builders remained current.

Host manifest validators: Claude Code 2.1.302 and Gemini CLI 0.64.0 passed. This establishes manifest validation only. No authenticated model invocation, ChatGPT/Codex import, UI branding, official marketplace listing, native Office/PDF export or full accessibility conformance is claimed. Claude/Gemini use the ASCII technical name; their tested schemas do not provide the portable OpenAI displayName field.

Local Chromium 154.0.8037.57: 144 layout conditions and 30 local links passed after fixing 16 text-resize overflow failures in long English headings and CLI paths. All 12 extracted standalone skill packages executed their bundled helper in isolation, preserving CRLF and Unicode source hashes. CI results are attached to the candidate PR. Local browser scope: actual new static pages, Chromium, 320/375/768/1440 CSS px, computed 200% text-size simulation, user spacing overrides, horizontal geometry and keyboard skip navigation. Computed text resizing is not native browser zoom. Full GB line-box compliance, resolved regional glyphs, screen reader and dynamic forms remain not-checked.

Design contract: use the existing warm paper/ink/red brand and unchanged logo; a reading-led hierarchy with a specimen, rule explanations, skill rows and host guides. No font binary, universal font palette or fixed typography template is distributed. The website CSS values are this site's layout choices, not global Chinese typography rules.

Reproduce:

```sh
python -m unittest discover -s tests/zilu -v
python tools/build_zilu.py --check
python tools/build_zilu_site.py --check
# Serve repository as /kumihan/ on localhost:8765, then:
python tools/check_zilu_site.py --output /tmp/zilu-browser
```

Publication: release candidate; final publication approval pending. GitHub source, Release, Pages, local install and marketplace listing are separate facts.
