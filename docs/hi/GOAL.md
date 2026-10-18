# /goal — KUMIHAN｜अक्षर-संगति v0.1.0

Status: **APPROVED FOR END-TO-END IMPLEMENTATION AND PUBLIC RELEASE** (Owner decision: 2026-10-19 JST).
Repository: https://github.com/landco-llc/kumihan
Canonical source: Git repository; research evidence: https://drive.google.com/drive/folders/121unZNhXt4qIq0AQo1WXiS6BjHmmMpTj
Work environment: Codex Cloud or Codex App, at repository root, branch freshly based on main.
Execution method: **/goal**, contiguous autonomous W00–W10. Do not stop after drafting an implementation plan. Execute, validate, merge and publish where host permissions permit. No routine per-Work human attachment or confirmation.
Scope: ONLY this repository and the Hindi product. No changes to another repository or project-specific governance controls.
Language for technical reporting: Japanese.

## 0. Non-negotiable Owner decisions

1. Public name is **KUMIHAN｜अक्षर-संगति**, with exactly this orthography and the full-width vertical separator (U+FF5C). Do not silently shorten, translate or replace the visible plugin name.
2. Version **v0.1.0**. Distinct product release tag: **kumihan-hi-v0.1.0** (avoid collisions with global KUMIHAN tags). Every distribution ZIP filename must contain **v0.1.0**.
3. Internal machine-readable IDs are ASCII kebab-case, preferring **kumihan-hi** and **kumihan-hi-web / kumihan-hi-documents / kumihan-hi-review**. Provider manifest internal ID may be ASCII but every supported user-facing display name must be the exact public name, without platform suffix or a duplicate brand.
4. **Descriptions for every Skill and plugin manifest must be bilingual Hindi + English only** (Hindi first, English second). No Japanese/French/Portuguese residue in those description fields. Website and installation pages additionally need their separately requested Japanese edition.
5. Deliver independently installable four Skills (entry / web / documents / review), the ChatGPT/Codex plugin, a Claude Code plugin and Claude Skills, a Gemini CLI extension and Gemini Skills. Provider support / UI availability must be honestly scoped; ZIP attachment alone is not plugin installation.
6. Use the existing official KUMIHAN logo and ensure every plugin and every standalone Skill package includes a valid icon file and all referenced relative paths resolve.
7. Public site paths:
   - Hindi: **kumihan-hi.html**
   - English: **kumihan-hi.en.html**
   - Japanese: **kumihan-hi.ja.html**
   - Installation: **docs/install-kumihan-hi-{chatgpt,claude,gemini}.html** and corresponding **.en.html / .ja.html** for all three hosts; nine installation pages total.
8. Site composition and CSS are based on the current Japanese KUMIHAN page, https://landco-llc.github.io/kumihan/kumihan.html, and the existing canonical layout in _layouts/landing.html. Installation guides follow the equivalent Japanese guide design and the shared install-frame. **Complete Skills/plugins BEFORE producing the site**; use KUMIHAN｜अक्षर-संगति and relevant existing KUMIHAN skills to author and review the website, with actual evidence.
9. The basic KUMIHAN concept, philosophy, navigation hierarchy and generic Japanese/English title/copy must agree with the Japanese master. Translate or substitute only language-specific functions, scripts, copy examples, locale advice and product identity; do not rewrite generic Japanese/English marketing copy for variety.
10. Apache-2.0, developer name **L&Co. LLC**, public worldwide, price free. GitHub source/Release/Pages publication is the target. Do **not** independently submit anything to third-party public plugin directories or claim provider approval.
11. Quality assurance is lightweight and focused because this is a low-risk OSS typography Skill. Do not impose unrelated security / audit work, but do not publish broken ZIPs, inaccurate manifests, incorrect URLs or text-damaging transformations.
12. Respect the project scope: project GPT supplies these instructions; Codex executes. Do not involve another project's DG/governance coordinator for this product work.

## 1. Evidence and mandatory Fresh Read

At W00 read the latest:
- main HEAD, AGENTS.md if present, repo instructions, current release/build conventions and layout;
- canonical Japanese page / _layouts/landing.html / assets and tools/product_site.py / tools/install_frame.py;
- analogous product: plugins/kumihan-compasso, plugins/kumihan-accord and plugins/kumihan-ar; their build/test scripts, host manifest formats and page builders. Reuse functionality, not translated Portuguese/French or unrelated marketing copy;
- current main homepage index.html, language cards/navigation, top-en.html if English landing is the active gateway, and footer link behavior;
- KUMIHAN Hindi research PDF, full Markdown and v0.1.0 Requirements Markdown in the Google Drive HI folder above. The Requirements file contains **24 rules (HI-T01…HI-T14, HI-C01…HI-C06, HI-D01…HI-D04)** and **24 QA cases (Q01…Q24)**. It is the typography contract. Do not replace with a generic Devnagari article or a novel rule set.

Known repository state observed before task creation (re-verify, do not lock to this SHA): main had product-site reusable builders and no Hindi product paths; do not overwrite intervening changes. Paths and dependency versions must follow fresh main.

Relevant primary specifications (check their current version if implementation needs a change):
- Unicode UAX #29, #14, #15 and Devanagari script implementation notes.
- W3C CSS Text 3 and WCAG 2.2 text spacing/reflow.
- Unicode CLDR Hindi locale formatting.
- OpenAI portable plugin manifest: https://developers.openai.com/plugins/build/plugins
- Gemini CLI extension reference: https://geminicli.com/docs/extensions/reference/
- Claude Code plugin manual / existing working Claude product in this repository.

## 2. Product contract

### 2.1 Text integrity, language and design

- Hindi language is not equivalent to Devanagari script or India market. Default hi-IN/Deva but do not treat Marathi, Nepali and Sanskrit as Hindi. Do not auto-create Hinglish.
- Preserve original logical code-point sequence, ZWJ/ZWNJ, nukta, matras, nasal marks, danda, visarga, words, identifiers, quotations, numbers, URLs and proper nouns. Keep NFC normalization only in derived comparisons/search, never silently mutate source. A bare change of Unicode normalization can change source bytes.
- For clipping, spans, highlights or animation, do not naively split UTF-16 or single code points. Use appropriate grapheme and orthographic-syllable precautions. Rendering or editing engine evidence remains operation-specific: do not advertise Intl.Segmenter as a universal solution for deletion, cursor movement or shaping.
- Do not force break-all/anywhere across Hindi paragraphs. Keep source intact, localize emergency URL breaks. CSS baseline: normal tracking, normal word-break, adequate line-height and padding for above/below signs; adjust visually where needed.
- When mixing Latin and Devanagari, preserve original brand spellings and compare font optical weight / digit glyph forms. Latin-numbered IDs, OTP, phone numbers and version identifiers are not locale quantities; never reformat or translate them.
- No automatic punctuation conversion, forced Devanagari digits, gender assumptions, dictionary substitutions or UI-copy rewriting. Default content policy = preserve. Separate study/build/audit/refine from preserve/propose/rewrite, so a build request does not grant carte blanche for supplied copy edits.
- Make contextual and editorial design judgments. Reduce generic formulaic AI-style repetition, meaning-free gradients, generic card grids and ornamental type without context; never impose religious motifs or a stereotypical India palette because of script. This is design guidance, not an AI-detector guarantee.
- Show actual observations separately from static validation, editorial proposals, native-speaker review and NOT_CHECKED.

### 2.2 Four standalone Skills

Proposed canonical directories:
- plugins/kumihan-hi/skills/kumihan-hi/SKILL.md
- plugins/kumihan-hi/skills/kumihan-hi-web/SKILL.md
- plugins/kumihan-hi/skills/kumihan-hi-documents/SKILL.md
- plugins/kumihan-hi/skills/kumihan-hi-review/SKILL.md

Each Skill MUST contain bilingual Hindi/English YAML front-matter description, visible identity, user-intent routing, bounded duties, and **self-contained references, locale information, rule catalog and source index** so standalone ZIP is functional without reading sibling Skills or fetching resources at runtime. Shared source can be generated/copied deterministically during build.

Roles:
- Entry: record script, language, market, medium, reader, intent and content modification authority, route to the appropriate Skill.
- Web: semantic markup, HTML lang=hi, font selection, responsive lines/wrapping, Indic shaping, mixed scripts, 320px, 200% zoom, fallback and realistic rendering checks.
- Documents: Word/Office/PDF/slide originals and extraction, correct glyphs and line-boxes, accessible editable masters, font embedding and copy/paste verification where environments permit.
- Review: read-only report with finding position, rule ID, evidence type, severity, remediation suggestion and explicit NOT_CHECKED limitations.

Profiles: ui, editorial, marketing, report, slides, display. Rules may be advisory or conditioned; do not force an identical design across genres.

### 2.3 Rules and QA

Implement an inspectable JSON catalog with all **24 IDs**, each with application condition, class (normative/implementation guidance/editorial choice), source refs, exception, recommended action, QA links, and implementation-vs-evidence status.

T-series: HI-T01…14 (logical order, joining/segmentation, normalization, ZWJ/ZWNJ, nukta/nasal marks, symbol distinctions, break rules, tracking, Indic shaping, line box, font files/digits/fallback, mixed script/display, language/accessible text, PDF text extraction).

C-series: HI-C01…06 (copy preservation/editorial authority, respectful plain UI language, grammatical agreement without gender guesses, labels/tokens/proper names, media-dependent punctuation/code-switching, locale digits/currency/date/IDs).

D-series: HI-D01…04 (language/script distinction, meaning-driven visual hierarchy, traceable visual design choices, claim/evidence transparency).

Fixtures Q01–Q24 must reproduce and check Hindi research cases, including:
- matras and conjuncts (क्षि, क्षी, त्रि, ज्ञ, श्र, स्त्री), RA forms, आधा/halant and logical order;
- NFC source variants क़ and क़; ZWJ U+200D and ZWNJ U+200C remain intact;
- nukta, visarga vs colon, nasal marks and Hindi spelling variants;
- danda and punctuation, compound/hyphenation, data like ₹1,23,456.78 and native digit samples;
- mixed Latin/Devanagari, 320 CSS pixels, 200% text zoom, CSS text spacing overrides, fallback font, Web→PDF copy/extraction, IME/editing/screen reading when possible.
Tests distinguish what is static executable in CI versus browser/manual/native-speaker tasks. No manufactured PASS.

Use Python 3.12 stdlib for standalone offline checks when suitable; do not pretend it understands all Hindi grammar. Include test assertions that source text is not changed.

### 2.4 Plugin/extension and distribution

Product root: plugins/kumihan-hi/.
- Root plugin.json: portable OpenAI Agent Plugins schema with extensions.com.openai.interface.displayName **KUMIHAN｜अक्षर-संगति**, supported logo paths and bilingual descriptions.
- Keep .codex-plugin/plugin.json if needed for existing Codex compatibility; same exact visible displayName, correct skills path and icon.
- .claude-plugin/plugin.json: legitimate Claude Code plugin descriptor; exact visible name wherever the host supports displayName, Hindi + English descriptions.
- gemini-extension.json + GEMINI.md: valid Gemini CLI extension; internal ASCII ID, public name exact when displayName supported, bilingual descriptions.
- Four Skills and skill-relative bundled assets; icon checked inside actual ZIPs.
- README, INSTALL, RELEASE_NOTES, UPDATES, supported scope, third-party notices and LICENSE; Hindi+English information where meaningful and no false host-install promises.

Create a deterministic packaging builder (e.g., tools/build_hi.py). Distribute **15** v0.1.0 ZIPs = 4 standalone Skills + 1 plugin/extension for each of ChatGPT/Codex, Claude, Gemini. Reuse current release filename conventions; examples:
- kumihan-hi-GPT-Codex-plugin-v0.1.0.zip
- kumihan-hi-Claude-Code-plugin-v0.1.0.zip
- kumihan-hi-Gemini-CLI-extension-v0.1.0.zip
- kumihan-hi-review-Claude-skill-v0.1.0.zip

Do not hide an arbitrary suffix in the actual visible name; the host-specific details belong in distribution filenames. ZIP members must have no absolute paths, traversal or symlink entries. Include SHA256SUMS.txt and MANIFEST.json listing all 15 packages, sizes and hashes; reproducible archives with stable timestamps/file ordering. Packages must contain no accidental Portuguese/French/Spanish strings in descriptions.

### 2.5 Website and copy

**AFTER Skills/plugins and QA for distributions are complete**, build pages with Hindi KUMIHAN and existing KUMIHAN review/authoring guidance.

Deliver:
- 3 landings: kumihan-hi.html (hi), kumihan-hi.en.html (en), kumihan-hi.ja.html (ja).
- 9 platform-specific guides: docs/install-kumihan-hi-chatgpt.html, -claude.html, -gemini.html, and their .en.html/.ja.html suffixes.
- Source-backed editable copy data, builder, isolated Hindi CSS overrides and tests. Prefer tools/product_site.py + tools/install_frame.py; derive core CSS from _layouts/landing.html, not a new unrelated visual theme. Avoid copying existing Portuguese/Arabic page text or stale language labels as template content.
- Language switchers on each landing and guide page, hreflang hi/en/ja/x-default, canonical and OG metadata, correct anchors and relative paths for GitHub Pages /kumihan/ base.
- Correct Hindi web fonts/fallbacks (Devanagari plus Latin); mark HTML lang=hi, no RTL (Hindi is LTR). Font load/fallback and shaping tests. No invisible/clipped matras, no forced tracking or letter breaking. Treat long brand label responsively instead of squeezing or cutting it.
- Install-page distribution links point to real release assets and give host-specific correct instructions. Never tell users that uploading ZIP to a chat installs a plugin. Include valid icon in all archives.
- English and Japanese generic title/hero/concept/design philosophy must remain aligned with the current Japanese KUMIHAN master. Differences are permitted only for Hindi-specific script rules/features, genuine product identity and distribution instructions. Create a copy matrix showing generic keys vs Hindi-localized exceptions; regression-test this parity. Japanese/English titles should not introduce an unrelated brand promise.
- Keep the original philosophy: linguistic-specific typesetting plus information design and constraints against formulaic AI-looking design. It is not simply a text formatter.
- If multilingual index uses equal-card language grid, add Hindi/English link appropriately without changing other language cards' uniform size or navigation. Do not break current homepage/corporate footer links or target=_blank on external company URL.

Possible Hindi title/copy is a **draft**, not native-speaker-approved. Reconcile with master philosophy and keep original when supplied:
- Hindi hero proposal: "भाषा बदले तो / अक्षरों का विन्यास भी बदलता है"
- Generic JA and EN hero/copy are to be lifted in meaning and structure from current KUMIHAN Japanese canonical page, not improvised new marketing slogans.
- Avoid mechanically replacing every danda, number or Roman brand word for stylistic consistency.

### 2.6 Release / verification

Product tag **kumihan-hi-v0.1.0**. GitHub Release is public and carries all 15 ZIPs, SHA256SUMS.txt, MANIFEST.json and concise Hindi+English release notes. GitHub Pages must serve all 12 intended pages. Public source is main. Distribution link tests must check exact filenames and availability. Release need not be added to any public provider marketplace without explicit separate Owner approval.

Honor provider-supported release creation paths; if GitHub connector cannot write releases, use an authorized Codex Cloud/App environment with gh CLI or existing release workflow. Do not mark PUBLISHED until remote API + HTTP checks confirm it.

## 3. Contiguous Work groups (/goal)

Work groups are milestones, not per-step Human gates. No need to stop for regular Owner messages.

- **W00 Fresh Read / Snapshot** — read requirements and repo HEAD, determine copy baseline, identify source paths and actual supported provider specs; save a small implementation ledger. No unrelated policy edits.
- **W01 Rules & source-preserving core** — all 24 Hindi rules, profiles, source refs, content-policy modes and bounded checks.
- **W02 Skills** — four independent Skills, bilingual descriptions, embedded rules/references/assets and meaningful usage examples. Ensure they can be used before any site work begins.
- **W03 Host integrations** — valid ChatGPT/Codex, Claude Code/Skills, Gemini CLI/Skills manifests, identity, icon references, test direct installation when environments available.
- **W04 Deterministic packages** — 15 ZIPs, checksums, manifests, reproducibility, practical install instructions. Milestone: skills and bundles are complete.
- **W05 Hindi-driven site authoring** — invoke/explicitly apply newly completed Hindi Skill and existing KUMIHAN Skills to copy/HTML/CSS work. Build three landings and nine host/language guides from common Japanese structural baseline; add only necessary navigation links.
- **W06 Visual and editorial checks** — browser render at 320/768/1280 widths, 200% zoom, font fallback, script shaping, copy-preservation, generic copy parity, internal navigation, language metadata. Where unavailable log NOT_CHECKED.
- **W07 Automated tests** — all 24 tests mapped to actual executable/static/manual status; focused product tests; existing high-signal language and build regressions. Add focused GitHub Actions workflow. Keep OSS review lightweight.
- **W08 PR & corrections** — open coherent PR with release artifacts or a CI-produced reproducible build; fix blockers, run CI, include actual evidence and known limitations. Do not claim unsupported provider/native-speaker validation.
- **W09 Publish** — merge after focused checks pass, publish product v0.1.0 tag + GitHub Release with ZIPs, ensure GitHub Pages deploy, test all 12 public HTML pages and release asset links.
- **W10 Handover** — final concise Japanese report: main SHA, PR URL/merge, tag/release, 12 page URLs, 15 ZIPs, test numbers with evidence, remaining native/mobile/native-speaker NOT_CHECKED, any source files to update. Clearly label PUBLISHED or BLOCKED_WITH_REASON.

At each milestone record a short ledger in docs/hi/WORK_LOG.md, but continue immediately to the next milestone. A missing non-critical native host, screenshot tool or mother-tongue reviewer does not halt bounded packaging / site publication; record the gap. Only block release for incorrect/unsafe binaries, source corruption, broken essential links, failed focused tests or missing ability to actually publish.

## 4. Acceptance matrix

All required:
- [ ] Display name everywhere possible equals exactly **KUMIHAN｜अक्षर-संगति**.
- [ ] Skills/plugins descriptions Hindi and English only; no third-language debris.
- [ ] 4 complete standalone skills; 24 rules linked to sources; 24 QA cases with real statuses; original text byte preservation.
- [ ] 3 supported host packages + 12 skill packages = 15 valid v0.1.0 ZIPs; contained images/fonts licensing respected; archive icon references resolve.
- [ ] Manuals and HTML are UTF-8; all 3 landing and 9 installation pages generated and linked.
- [ ] Site structure/CSS consistent with Japanese KUMIHAN, JA/EN common-copy parity checked, Hebrew/Arabic RTL code not accidentally inherited; hi pages are LTR.
- [ ] At 320px, no clipping of matras or missing functionality; 200% text and non-default text spacing checked or openly declared NOT_CHECKED.
- [ ] New site uses KUMIHAN｜अक्षर-संगति rules after Skills build; record which rules were applied.
- [ ] Focused CI passing; no regressions in existing top card sizing/nav/corporate link or other language builds.
- [ ] Public GitHub tag + Release verified, assets available, Pages 200 responses and internal links verified. Avoid claiming public app-marketplace approval.
- [ ] Short Japanese result report with source of truth and honest limitations.

Do not substitute a mere plan, draft PR or incomplete artifacts for the requested finished public release. If implementation/publishing cannot be executed due to permissions or platform limitations, deliver the complete partial work, identify exact blocker and the single immediate next action without pretending the release is live.
