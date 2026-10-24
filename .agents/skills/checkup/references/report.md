# Report contract

Report in chat. Lead with the most important outcome and prioritized next steps,
not a transcript of commands. A checkup is advice about observed evidence, never
a certification that the machine has no problems.

## Structure

1. **Scope and outcome:** platform, execution context, software/setup boundary,
   highest-impact findings, and important limits. Use sanitized identifiers.
2. **Problems:** verified configuration, ownership, compatibility, or software
   health issues, ordered by impact and urgency.
3. **Improvements:** optional ideas with a concrete benefit and costs. Separate
   core candidates from optional-tool/workflow suggestions. Label any proposed
   change to the core definition as policy reconsideration.
4. **Cleanup candidates:** distinguish established redundancy/breakage from
   suspected disuse; name preservation needs and required confirmation.
5. **Coverage and follow-up:** account for every baseline area as checked,
   inapplicable, unavailable, declined, or unresolved. Include relevant checks
   passed, blocked leads, metadata freshness limits, and any separately scoped
   inspection worth considering. Omit empty finding sections with a short note.

For each finding, supply:
- Category, affected software/configuration, and owner/scope (shared repo, local
  machine, native OS, specialist manager, or employer-managed).
- Evidence from a bounded local observation or repo reference; official URL and
  retrieval date for external facts. Distinguish facts from inference.
- Impact/priority and confidence, separately: an uncertain issue can have high
  potential impact. State what would confirm or refute it.
- Suggested action in prose, expected benefit, trade-offs/migration effort, and a
  safe verification step. For cleanup, include consumers/dependencies and data
  preservation/recovery cautions, or explicitly state they are not yet known.

Consolidate symptoms of one underlying issue. Use concise findings, not a raw
package dump. A valid outcome is no evidenced problem plus a precise coverage
statement; generating speculative recommendations is not a completion criterion.

## Output and action boundaries

Exact remediation commands are provided only on request. Verify syntax and
ownership first; show prerequisites, targets, risks, preservation/rollback needs,
and validation. Mark them **proposed, not executed**. For uncertain or destructive
actions, resolve missing facts or explain the required checks rather than invent
a ready-to-run command. Giving commands does not authorize executing them.

Diagnostic commands/evidence may appear when useful, with sensitive values
removed. Exclude credentials, employer identifiers, private package names,
personal content, and unnecessary absolute user paths. Keep requested private
details local to the agreed audience; never copy them into public research.

Save Markdown only when requested and after agreeing on path and privacy.
Prefer an approved destination outside the checkout for private machine reports;
do not assume a report is ignored by Git or change ignore rules automatically.
No automatic issue creation, repository edits, installs, fixes, or follow-on
implementation. Stop after reporting.
