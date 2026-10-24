---
name: checkup
description: Review this machine's software and setup, reporting problems, improvements, core candidates, and cleanup opportunities without applying changes.
disable-model-invocation: true
---

# Checkup

Assess the current machine's software and setup. Produce advice, not remediation.
This skill is explicitly invoked; it does not run a checkup merely because the
repo is opened. It is portable across personal and work machines, not a remote
or multi-machine scanner.

## 1. Establish context

Read the repo's `AGENTS.md`, `GLOSSARY.md`, and relevant domain decisions. Read
`docs/core-tools.md`, `docs/recovery.md`, `docs/local-configuration.md`,
`docs/maintenance.md`, and `docs/toolchains.md` for intended ownership and scope.
Consult other guides only for the features being inspected. Derive current
selections and deployment targets from the repo, rather than a cached inventory.

Read [inspection rules](references/inspection.md) before collecting host evidence.
Use low-risk inspection to identify OS/distribution, architecture, WSL status,
current shell/PATH, available package managers, and repo deployment locations.
Do not infer interactive-shell behavior solely from the agent's shell.

Load the applicable platform reference:
- macOS: [macOS checks](references/macos.md).
- Ubuntu/Debian, including WSL: [Linux and WSL checks](references/linux-wsl.md).
- Elsewhere: report the support limit; use only verified generic checks and
  propose a separately approved extension rather than guessing platform commands.

Context is established when platform, intended setup, and applicable check areas
are identified, with unknowns explicit. Ask about goals or usage only when the
answer changes a recommendation; discover environmental facts yourself.

## 2. Inspect baseline, then follow leads

Apply the three approval tiers in the inspection rules. Low-risk work is
pre-approved. Present medium-risk work as a bounded batch plan before running it;
include anticipated high-risk operations in that plan, but obtain separate,
operation-specific consent for each. Continue with available evidence when
approval is declined; mark the coverage gap.

Account for every baseline area below. Use installed metadata and focused checks
first, then investigate evidence-backed leads instead of scanning indiscriminately.

| Area | Questions to resolve |
| --- | --- |
| Shared/local configuration | Are intended links and targets correct? Are startup order, overrides, integrations, and PATH consistent with repo intent? |
| Installed software | Which managers own the selected and optional tools/apps? Are executables shadowed, broken, unsupported, or unnecessarily duplicated? |
| Software startup/services | Are relevant autostarts, agents, services, plugins, or container engines conflicting, stale, or left behind by removed software? |
| Maintenance | Are supported update owners clear? Is there verified deprecation or actionable outdated software, accounting for metadata age and distribution backports? |
| Improvements/core | Is there a concrete capability gap or simpler ownership/workflow? Does a candidate fit the core environment or belong in optional inventory? |
| Cleanup | Are there broken links, obsolete integrations, superseded installations, or software caches/data worth reviewing, with dependencies and retained data accounted for? |

Discover managers and applications beyond the curated optional inventory when
present; that inventory is neither a full machine manifest nor a requirement to
install everything listed. Read a repo check before executing it. Reuse
`./setup-core --check` only after verifying its current implementation and the
resolved tools satisfy the inspection rules; it is a narrow check, not proof of
overall correctness. Inspect deployment links directly instead of running the
installer as a diagnostic.

Keep this a software/setup review: general security posture, vulnerability or
malware scans, hardware health, performance benchmarking, and employer-policy
compliance are outside scope. Inspect service configuration for software conflicts,
not general workload profiling. Treat employer-managed controls as constraints;
recommend consulting the owner where appropriate, not bypassing them.

Baseline is complete when every area is checked, inapplicable, unavailable,
declined, or unresolved, with its evidence and limits recorded. Follow leads until
each is an evidenced finding, an explicitly uncertain candidate, or a named
follow-up blocked by access, consent, or unavailable information.

## 3. Evaluate recommendations

Separate confirmed problems, optional improvements, core candidates, and cleanup
candidates. Cite local evidence; use official sources for freshness/replacement
claims under the inspection rules. Compare benefits against migration effort,
maintenance, overlap, portability, and existing ownership. Leave healthy intentional
choices alone; novelty or a newer upstream version alone is not a recommendation.

Use **core environment** as defined in `GLOSSARY.md`. Prefer broadly useful,
portable, low-maintenance interactive CLI capabilities that fill a concrete gap.
Keep IDEs, runtimes, and desktop apps optional by default. A compelling proposal
to expand the core boundary must be labeled as a policy reconsideration, with
its rationale and costs, not treated as current repo intent.

For cleanup, distinguish confirmed broken/redundant items from uncertain disuse.
Age, absence from PATH, a second installation, or lack of repo references does
not prove abandonment. Identify owner, consumers/dependencies, retained data,
preservation needs, and what would establish safe removal. Do not inspect shell
history to infer usage by default. Ask a focused usage question if needed, or
retain the uncertainty in the report. Respect deliberately retained legacy
runtime managers/data and intentional compatibility stubs.

## 4. Report and stop

Use the [report contract](references/report.md). Report in chat by default;
create a file only on request after agreeing on its location and privacy. No
automatic issues, commits, inventory files, or edits to the repo/system.

Give recommendations in prose. Prepare exact remediation commands only when
requested, under the report contract; that request never authorizes execution.
End with prioritized advice and coverage limits, not an offer to apply changes.
