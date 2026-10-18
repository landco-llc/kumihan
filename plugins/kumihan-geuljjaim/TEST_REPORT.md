# Validation scope

The Korean product has 36 catalog candidates (13 P0) and six media profiles. Four static detectors recognize narrow Korean candidate patterns; exact-byte comparison separately verifies supplied extractions. Warnings require context and never modify input.

`python -m unittest discover -s tests/geuljjaim -v` exercises positive, negative and protected-role exceptions; NFC/NFD/Jamo/emoji/whitespace preservation; 40 fixture byte replays; fifteen ZIP CRC, safe paths, unique members, inventory and checksum integrity; deterministic build output. `python tools/build_geuljjaim.py --check` compares canonical sources with generated files without writing.

Forty research scenarios remain in `references/fixture-ledger.json`. Their byte identity checks are separate from the **not-checked** semantic, visual and editorial acceptance outcomes. Passing byte replay does not validate meaning, line breaking or Korean grammar.

The site uses the entry/Web skills through explicit source reading. `tools/check_geuljjaim_site.py` checks actual Jekyll output in Chromium at 320/375/768/1440px and CSS root-font-size 200% simulation, links, focus, language metadata and clipboard. CSS simulation is not native text zoom. Native Korean editing, other browsers/OS, vertical text, Office/PDF and native plugin host invocation remain not-checked.

Host formats: Claude Code 2.1.302 `plugin validate` and Gemini CLI 0.64.0 `extensions validate` pass on the respective independently extracted bundles. All fifteen archives extract into 24 self-contained Skill instances; isolated Python static-helper smoke passes. These are native manifest/structure checks, not authenticated model invocation or UI upload tests.
