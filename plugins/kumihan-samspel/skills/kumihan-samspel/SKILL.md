---
name: kumihan-samspel
description: "Välj medium och omfattning för svensk typografi. | Route Swedish typography work by medium and permission."
---

# KUMIHAN｜Samspel

Välj medium och omfattning för svensk typografi. / Route Swedish typography work by medium and permission.

## Svenska

Använd detta Skill för entry. Bevara originalets byte, namn, tal, citat, kod och Unicode-tecken. Ingen översättning, normalisering eller automatisk rättning. Ange sv, sv-SE eller sv-FI uttryckligen; latinbokstäver identifierar inte språket. Vid sv: be om region bara om den påverkar uppdraget. Föreslå textändringar separat och endast med tillstånd. Review är skrivskyddat.

Läs arbetsflödet och relevanta villkorade regler nedan. Skilj löptext, uttrycksfull reklam och UI. Svensk regional variation ska inte ersättas med danska eller norska regler. Kontrollera ÅÄÖ och avstavning i faktiskt typsnitt; ändra inte nattåg i grundtexten för en avstavning.

## English

Use for entry. Preserve exact original bytes, names, numbers, quotations, code and Unicode combining sequences. Never translate, normalize or autocorrect automatically. Require explicit sv, sv-SE or sv-FI; Latin script does not identify Swedish. For sv ask region only when it materially affects the task. Keep authorized text proposals separate; review is read-only.

Distinguish reading prose, expressive copy and UI. Apply Swedish regional guidance conditionally; never import Danish or Norwegian rules. Real rendering is required to verify ÅÄÖ clipping and hyphenation. Do not change stored nattåg to implement a line break.

Read [workflow](references/workflow.md), [rules](rules/catalog.json), [sources](sources.json), [trace](references/research-trace.json), [profiles](profiles/mediums.json), [locales](locales/supported.json), [fixtures](fixtures/acceptance.json), [schema](schemas/report.schema.json), [coverage](inventory.json), [rights](THIRD_PARTY_NOTICES.md) and [license](LICENSE). The [official icon](assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png) and every referenced resource are included in this Skill.

Run `python runtime/check_source.py SOURCE --locale sv-SE --medium entry` from this folder. `--candidate FILE` compares exact bytes without writing. Invalid locales receive no Swedish guidance. The tool is a bounded static diagnostic, not a renderer or grammar checker.

Return original SHA/integrity, locale and context, findings with rule/source IDs, separately authorized proposals, evidence and unrun checks. Native rendering, Office/PDF, host invocation and specialist language review remain `not_checked` until actually performed. Supplied research cases are not PASS evidence.
