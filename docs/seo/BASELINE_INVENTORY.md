# KUMIHAN SEO baseline inventory — 2026-10-19

**Status: READ-ONLY INVENTORY / SEO IMPLEMENTATION PENDING.** Baseline main commit: `fce40015abaa1f5f309cf9e977f55e41537c13aa`. URLs are candidate outputs; build/runtime existence and canonical correctness require W00/W05 validation.

## Root-level public HTML candidates

| Page category | Count | Paths | Source |
| --- | ---: | --- | --- |
| Language gateways | 18 | `index.html` + `top-*.html` | `tools/build_gateways.py`, `assets/gateway-copy.json` |
| Japanese KUMIHAN three languages | 3 | `kumihan.html`, `en.html`, `zh-tw.html` | Frontmatter + `_layouts/landing.html` |
| Individual language product landing pages | 48 | 16 editions × 3 translations | `tools/product_site.py` and edition-specific site builders/templates |
| Total root-level HTML candidates | **69** | | |
| Docs HTML candidates | **150** | `docs/**/*.html` | Installation guide builders, Jekyll or templates; each must be checked for canonical/indexability |

### Gateway language codes (18)

`ar`, `bn`, `de`, `en`, `es`, `fr`, `hi`, `id`, `it`, `ja`, `ko-KR`, `pl`, `pt`, `ru`, `th-TH`, `vi`, `zh-Hans-CN`, `zh-Hant-TW`.

### Language edition / product pages (16 groups)

| Edition key | Page filenames |
| --- | --- |
| Arabic | `kumihan-ar.html`, `kumihan-ar.en.html`, `kumihan-ar.ja.html` |
| Bengali | `kumihan-bn.html`, `kumihan-bn.en.html`, `kumihan-bn.ja.html` |
| German | `kumihan-de.html`, `kumihan-de.en.html`, `kumihan-de.ja.html` |
| Spanish | `kumihan-es.html`, `kumihan-es.en.html`, `kumihan-es.ja.html` |
| French | `kumihan-fr.html`, `kumihan-fr.en.html`, `kumihan-fr.ja.html` |
| Hindi | `kumihan-hi.html`, `kumihan-hi.en.html`, `kumihan-hi.ja.html` |
| Indonesian | `kumihan-id.html`, `kumihan-id.en.html`, `kumihan-id.ja.html` |
| Italian | `kumihan-it.html`, `kumihan-it.en.html`, `kumihan-it.ja.html` |
| Korean | `kumihan-ko.html`, `kumihan-ko.en.html`, `kumihan-ko.ja.html` |
| Polish | `kumihan-pl.html`, `kumihan-pl.en.html`, `kumihan-pl.ja.html` |
| Portuguese | `kumihan-pt.html`, `kumihan-pt.en.html`, `kumihan-pt.ja.html` |
| Russian | `kumihan-ru.html`, `kumihan-ru.en.html`, `kumihan-ru.ja.html` |
| Thai | `kumihan-th.html`, `kumihan-th-en.html`, `kumihan-th-ja.html` |
| Vietnamese | `kumihan-vi.html`, `kumihan-vi.en.html`, `kumihan-vi.ja.html` |
| Simplified Chinese | `kumihan-zh-cn.html`, `kumihan-zh-cn.en.html`, `kumihan-zh-cn.ja.html` |
| Traditional Chinese | `kumihan-zh-han.html`, `kumihan-zh-han.en.html`, `kumihan-zh-han.ja.html` |

## Sample existing metadata findings

- `index.html`, `top-en.html`: `title`, description, canonical, hreflang present; complete OG/Twitter/JSON-LD blocks not found in inspected heads
- `kumihan-fr.html`: existing Open Graph fields and canonical/hreflang; no JSON-LD seen in inspected head
- `_layouts/landing.html`: title/description/canonical/OGP/hreflang present but JSON-LD block not found
- Root `robots.txt`, `sitemap.xml`, `_config.yml`: not present when read
- GitHub Pages published output might differ from source (Jekyll or cache); verify after deployment

## W00 required updates

1. Enumerate each actual source-builder→generated-file pair for all 69 candidates and 150 docs.
2. Test whether each candidate is indexable; explicit canonical and duplicate alias rules.
3. Record source HEAD, commit SHA, generator command and `--check` operation for each group.
4. Update counts for newer main changes before coding.
5. Record exclusions and whether any docs lack canonical or are redirect/duplicate.
6. Keep inventory up to date when new editions or translated pages are added.

A file present in git does **not** automatically imply an indexable page; treat counts above as discovery inventory, not published SEO coverage.
