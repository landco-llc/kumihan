# KUMIHAN｜نضيد v0.1.0 — verification scope

تنضيد عربي يحفظ الأصل ويميّز الدليل عن الإرشاد. | Arabic typography that preserves source and distinguishes evidence from guidance.

The product offers four self-contained skills and five archives per host family. Generated package inventories and SHA-256 files describe actual bytes. Native ChatGPT/Codex, Claude and Gemini discovery/import/invocation have **not been checked**. Gemini Apps skill import is manual/unverified. No provider directory listing is claimed. Arabic editorial copy needs native-speaker review.

## Site production

The landing follows the eight sections of `_layouts/landing.html`: hero, intro-strip, features, idea-band, skills-section, install-section, status-section and cta-section. Each section retains its information role, paper/ink/red palette, spacing hierarchy and the official wordmark. Installation guides share the same branding and direct language/host navigation. Existing products are preserved.

`assets/kumihan-install.css` was absent from main at `a0f54332bd666a16eda33ce4816e9cd1ee7d2bde`. Its actual source was recovered unchanged from repository history commit `6783d130554b535905ef67cfec975f868b9f7874`, where it had been used for existing installation guides. This is recovery of a real file, not reconstruction. `assets/kumihan-ar.css` uses the main landing's inline styles with localized reflow/direction adaptations. Both stylesheets are linked by all twelve pages.

The initial generator draft preceded the final Arabic skill read. The final production/refinement pass read `plugins/kumihan-ar/skills/kumihan-ar/SKILL.md`, `kumihan-ar-web/SKILL.md`, their source/evidence contract and web playbook. Arabic pages use semantic RTL, host shaping, local LTR isolation, normal Arabic tracking and logical order. No text reversal, glyph splitting or Tatweel injection is used. General `ar` copy does not prescribe regional digit/calendar conversion.

Japanese production read the existing `skills/kumihan/SKILL.md`, `skills/kumihan-web/SKILL.md`, design contract and web recipes from the main baseline. JA-TYPE-011 comparison found ordinary desktop wrapping split 意味 in the hero; local balanced wrapping improved it without modifying source or forcing phrase spans. Strict line breaking remains active. English uses the common design contract, normal word spacing, local long-word fallback, semantic headings and measured reflow. No English-specific skill is claimed. These are **file reads and applied guidance**, not native plugin activation.

The purpose is to help Arabic-content creators understand source preservation and select an actual host package. The eight-section brand structure introduces the problem, explains four concrete priorities, then compares four task skills before host acquisition. Body type uses available system fonts; headings carry hierarchy, captions carry scope, and technical identifiers wrap locally. No font files, external design images or commercial assets are distributed.

## Observed checks

- Python unittest: Arabic runtime/source, standalone extraction, byte inventories, deterministic distribution and twelve-page link/locale contracts.
- Existing Japanese/core, ZiHeng, Korean, Thai, ZiLu and French tests were run separately without failures.
- Chromium: twelve pages × 320/375/768/1280 CSS pixels × ordinary/200% CSS text-size simulation. Document horizontal reflow and image loading checked; direct language switching preserves host; keyboard first focus reaches the skip link.
- Screenshots reviewed for Arabic mobile and Japanese desktop; normal Japanese and balanced heading alternatives compared. The published Japanese baseline was fetched with certificate-verified HTTP and rendered locally for structural/visual comparison.
- One independent lightweight source/package/site review found no critical blocker. Its host-partial checksum usability finding was corrected: selected archives use GNU `--ignore-missing`, with explicit verification of all selected files; single-file/macOS checks compare the matching digest.

A source diagnostic is not a rendering proof. CSS text enlargement is not native browser text zoom. Safari/Firefox, screen readers, native clipboard/export, Office, provider installation and native Arabic editorial review remain **not-checked**. The runtime's external CSS, scripts and shadow DOM limitations are documented in its bundled web playbook. Public Release/Pages status must be established by live HTTP and release metadata, separately from these checks.
