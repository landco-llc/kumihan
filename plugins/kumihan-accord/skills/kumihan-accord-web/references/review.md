# Review protocol / Protocolo de revisión
- Audit is read-only, with rule_id, affected excerpt, offset, evidence type, limitation and proposal separately.
- Static helper only checks candidate punctuation and guillemet spacing; it never writes the input.
- Other typography rules require renderer, human editor or host evidence.
- An untested case remains not-checked; do not convert candidate to correctness PASS.
- Correct fr-CA zero spacing before ! ? ; must not be called an error.

- OQLF fine nonbreaking spacing before ! ? ; is also an accepted form. An empty finding list is not proof unless the relevant rule was evaluated.
- Report accepted, nonconforming, outside-supported-scope and review conditions distinctly. Keep normalization proposals separate from validation.
- Record syntax/time exclusions and source-bound range units. Keep rule identity consistent between audit and proposal.
- Read [regional capability boundaries](regional-capabilities.md); additional profiles are reference-only and do not imply a numeric formatter or DOM editor.
