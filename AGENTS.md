## Agent skills

### Issue tracker

Issues and specs live in this repo's GitHub Issues. See `docs/agents/issue-tracker.md`.

### Triage labels

Use the default five triage labels. See `docs/agents/triage-labels.md`.

### Domain docs

Use a single-context layout. See `docs/agents/domain.md`.

## Documentation policy

Keep user docs short, task-focused, and limited to current behavior and critical
information. Do not put reports, migration history, temporary findings, or
historical behavior in documentation. Keep agent instructions separate from user
guides; retain other internal docs only for clear lasting value. Historical
context belongs in GitHub Issues or Git history, not a replacement appendix.

## Testing

Prefer temporary smoke checks and disposable validation environments; remove temporary test code and artifacts afterward. Add persistent tests only when their ongoing value is obvious; this repository does not need a standing test suite by default.
