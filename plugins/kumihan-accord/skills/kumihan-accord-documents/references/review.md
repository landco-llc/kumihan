# Review protocol / Protocolo de revisión
- Audit is read-only, with rule_id, affected excerpt, offset, evidence type, limitation and proposal separately.
- Static helper only checks candidate punctuation and guillemet spacing; it never writes the input.
- Other typography rules require renderer, human editor or host evidence.
- An untested case remains not-checked; do not convert candidate to correctness PASS.
- Correct fr-CA zero spacing before ! ? ; must not be called an error.
