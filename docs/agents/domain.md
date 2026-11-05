# Domain docs

This is a single-context repository. For domain or design work, read the root
`GLOSSARY.md` and relevant ADRs under `docs/adr/` when present.

If those docs are absent, continue without flagging it or proposing empty files.
`/domain-modeling` creates them only when a term or decision is actually
resolved, including through `/grill-with-docs` or
`/improve-codebase-architecture`.

Use the glossary's terms in issues, proposals, and tests; avoid synonyms it
explicitly rejects. If a needed term is missing, reconsider whether it is new or
note the genuine gap for `/domain-modeling`. Surface conflicts with an existing
ADR rather than silently overriding it.
