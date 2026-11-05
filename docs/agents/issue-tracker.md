# Issue tracker: GitHub

Issues and specs live in this repository's GitHub Issues. Use `gh` from the
checkout; it resolves the repository from its remote. Read a ticket with
`gh issue view <number> --comments`; include labels when triaging. A skill asking
to fetch a ticket uses that command, and “publish to the issue tracker” means
create a GitHub issue. See [triage labels](triage-labels.md) for this repository's
label mapping.

## Triage contract

**PRs as a request surface: no.** `/triage` reads this setting. GitHub shares
issue and PR numbers, so resolve an ambiguous `#<n>` with `gh pr view <n>` and
then `gh issue view <n>`.

## `/wayfinder` contract

- A map is one issue labelled `wayfinder:map`, with Notes, Decisions-so-far, and
  Fog (`gh issue create --label wayfinder:map`). Link children as native GitHub
  sub-issues through the sub-issues API; if unavailable, use a map task list and
  a `Part of #<map>` line.
  Child type labels are `wayfinder:research`, `wayfinder:prototype`,
  `wayfinder:grilling`, or `wayfinder:task`.
- Use UI-visible native issue dependencies for blockers:
  `gh api --method POST repos/<owner>/<repo>/issues/<child>/dependencies/blocked_by -F issue_id=<blocker-id>`.
  Get the blocker ID with `gh api repos/<owner>/<repo>/issues/<n> --jq .id`;
  it is the numeric database ID, not the issue number or node ID. If dependencies
  are unavailable, use a `Blocked by: #<n>, #<n>` line listing every blocker.
  A child is blocked when `issue_dependencies_summary.blocked_by > 0` or any
  fallback-listed blocker is open. The frontier is the first map-ordered open
  child with no open blocker and no assignee.
- Claim with `gh issue edit <n> --add-assignee @me`; this is the session's first
  write. Resolve with `gh issue comment <n> --body "<answer>"`, then
  `gh issue close <n>`, then append a gist/context link to the map's
  Decisions-so-far.
