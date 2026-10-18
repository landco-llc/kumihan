# Korean Web recipe

1. Read the public preservation policy, selected profile and rules before work. Capture supplied copy bytes and declare ko-KR.
2. Distinguish eojeol (space-delimited groups), syllable blocks and grapheme clusters; do not split decomposed Jamo. Do not normalize source Unicode.
3. Compare `word-break: normal` and `keep-all` at actual widths and font metrics. Provide emergency overflow-wrap for long tokens where appropriate. Avoid forced br, nowrap, clipping and global shrink. Do not assume one CSS setting proves good Korean layout.
4. Check 320/375/768/1440px and 200% text enlargement, mixed Latin/digits, punctuation and isolated last lines in a renderer. Record native vs simulated zoom. Static helpers are guidance only.
5. Match CTA and completion copy to actual action/state. Preserve EC facts and brand tone. `3개` is not an unconditional violation; particles, dependent nouns and auxiliary verbs need context.
6. Return evidence and limitations; no implicit content changes. Review meaningful alt text and focus behavior.
