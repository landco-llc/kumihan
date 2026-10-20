# JA v0.2.0 Native Host Acceptance — manual / delegated smoke

State: planned; NOT EXECUTED. This is the evidence protocol for actual candidate v0.2.0.  
Workgroup: KUMI-JA-V020-QA-20261020-01. PR #120 remains Draft. No public submission.

## Host matrix

| Target environment | Source package | Expected route | Execution owner |
| --- | --- | --- | --- |
| ChatGPT app / Codex app supported installation pathway | downloads GPT-Codex/plugins/kumihan-GPT-Codex-plugin-0.2.0.zip and four skills | kumihan / kumihan-web / kumihan-documents / kumihan-review | Test host operator with authorized private test workspace |
| Claude / Claude Code supported pathway | downloads Claude/plugins/kumihan-Claude-Code-plugin-0.2.0.zip and four skills | Same four JavaScript-independent Japanese skill names | Test host operator |
| Gemini / Gemini CLI supported pathway | downloads Gemini/extensions/kumihan-Gemini-CLI-extension-0.2.0.zip and four skills | Same four Japanese skill purposes | Test host operator |

For every host: read its current installation guidance and actual package manifest first. A host-app skill and a CLI extension are not assumed to have the same install method. If a package cannot be installed in that host, record an explicit supported-path mismatch or ACCESS_NEEDED rather than guessing.

**The connected KUMIHAN Universal MCP currently reports Japanese module 0.1.8, guidance_only. It does not count as v0.2.0 candidate acceptance, and must not be silently updated by this QA.**

## Preparation

1. Record actual host, client build/version, machine or sandbox, account/workspace class (omit user identity), package basename, SHA-256 and ZIP members. Compare to PR #120 release-manifest.json.
2. Install in a private test area only if the operator has authority. Do NOT submit to the public directory, create a marketplace listing, publish a Release, or change active customer integrations.
3. Observe native discovery UI/CLI enumeration. If skill names are unavailable or absent, record the actual error and do not infer successful routing from reading source files.
4. For each test preserve original instruction, selected skill, output and actual observed behavior.

## Four deterministic prompts (run with each supported host)

### H-01 Entry and briefing — kumihan

Input: 「社内向け日本語のWeb案内をつくる前に、閲覧者の目的・必須情報・文章として読む領域と造形コピーを、区別した短い制作ブリーフを提示して。原稿はまだ変更しない。」

Expected evidence:
- The entry skill is actually called/discovered, not merely cited from a README.
- Explains intended audience/readingTask/roles and protected fields; no silent creative rewrite or claims of visual acceptance.
- Shows unknown intent or unavailable font as unknown; routes later build to appropriate medium.

### H-02 Japanese Web — kumihan-web

Input: 「320pxと1024pxで使う案内UIの組版案を示し、次の原稿をコードポイントも含め変えないで。『髙﨑さま／料金１,２００円／が』『2026年度・特別会員向けオンライン講座の受講登録を取り消す』『2026年11月3日／文字の広場（架空会場）』。ボタンは操作可能で、文字や日付が隠れないこと。日本語の単語や係り受けが不自然に分割されないか確認して。実描画していなければnot-checkedと記録。」

Expected evidence:
- Actual Japanese Web skill selected; output file/source captured.
- Exact Unicode codepoints for provided original (special character and decomposed combining mark retained), no fabricated date/price.
- Actual rendered state and line breaks assessed separately from source equality. Unrendered cannot become passed.
- The layout must explicitly address the PV-006 observed 「オ／ンライン」 split rather than promoting a generic CSS wrap to beautiful composition.

### H-03 Document/slides — kumihan-documents

Input: 「日本語の報告書とスライドの組版方針を提示。表が複数ページにまたがる場合の継続見出し、注記、図形に隠れる文字、見出しと本文の階層、投影距離不明時の未確認状態を扱って。PDF抽出一致は表示品質の保証としない。実ファイルを作った場合はページ・全スライドを確認して。」

Expected evidence:
- Actual skill invocation and format choice. If no output file generated, classify advice-only.
- Generated PDF/PPTX must be rendered and inspected independently (not counted by text-only response).
- Projection/Office-native not guaranteed from an HTML-PDF preview.

### H-04 Read-only review — kumihan-review

Input: 「次の原稿と実表示の問題候補をレビューだけして。原稿:『2026年度・特別会員向けオンライン講座の受講登録を取り消す』。画像で『オ／ンライン』と改行され、別の箇所では文言が図形に隠れているとする。原因候補・必要な実測・修正案を示すが、成果物そのものは編集しない。推測と確認済みを分けて。」

Expected evidence:
- Review does NOT mutate input artifact or change the protected source.
- Differentiates semantic judgment, actual observed clipping and missing evidence.
- No invented “verified all slides” or aggregate numerical beauty score.

## Expected reporting table (per host, per entry)

| Field | Required |
| --- | --- |
| host / app version / test environment | Actual product/version; otherwise unknown |
| bundle path + sha256 | Exact PR candidate ZIP identity |
| installation/discovery/invocation | Concrete step and result, separate fields |
| input path/codepoint digest | Exact source text and stable identifier |
| raw observed response | Captured file/log/screenshot |
| behavioral outcome | Pass / fail / not-checked / unsupported only within named scope |
| native-versus-emulated | NATIVE, SOURCE_READ_ONLY, or SIMULATED; never conflate |
| missing permission or host | ACCESS_NEEDED and precise recommended human action |

Each host has four required skill invocations: total **12 host-skill observations** if all three host pathways permit installation. **This is a test target, not a statement that 12 tests ran.**

## Human Gate checklist

If Codex Cloud cannot install in ChatGPT/Claude/Gemini native UI, create an operator packet with exact ZIPs and run prompts. The user/authorized host operator may perform the install and provide evidence for assessment. Never ask a user to paste a password or secret. If no evidence returns, keep that host NOT-CHECKED and exclude it from claims of verified native support.

All host acceptance remains separate from KUMIHAN Universal MCP production integration and from public Marketplace publication.
