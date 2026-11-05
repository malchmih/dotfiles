---
name: checkup
description: Assess this machine's software and setup across relevant managers; give prioritized, evidence-based advice without making changes.
disable-model-invocation: true
---

# Checkup

Use only when the user explicitly invokes this skill. Assess the current
machine's software and setup across relevant managers; this is advice, not
remediation, a complete inventory, or a claim that the machine is healthy.

## Establish relevant context

Read root [agent instructions](../../../AGENTS.md) and [glossary](../../../GLOSSARY.md).
Use only relevant context from [Recovery and shared preferences](../../../README.md),
[shell and Local configuration](../../../docs/shell.md), and
[maintenance and toolchains](../../../docs/maintenance.md). Inspect
[`mise.toml`](../../../mise.toml) for declared resources instead of treating docs
as a complete machine inventory.
If inspecting OpenCode preferences, also read
[OpenCode agent instructions](../../../opencode/AGENTS.md).

Identify platform, architecture, WSL status, and the user's goal using bounded
evidence; keep unknowns explicit. Ask about intended use or ownership only when
it can change advice; discover other safe environmental facts yourself. Read the
[inspection rules](references/inspection.md) and only the applicable platform note:

- [macOS](references/macos.md)
- [Ubuntu/Debian and WSL](references/linux-wsl.md)

Elsewhere, use verified generic checks only and state the coverage limit. Do not
assume the agent shell represents a fresh interactive shell.

## Inspect and follow evidence

Use bounded, read-only local package/app-manager metadata, command resolution,
targeted configuration data, and relevant startup/service or maintenance metadata.
Check owners across managers; follow concrete leads rather than inventorying
everything. Read shell startup files statically—never source private Local hooks
or launch a login/interactive shell as a probe.

Only bounded, low-risk evidence collection is pre-approved. Get consent for
broader, network, or consequential diagnostics; elevated, sensitive, or
workload-impacting operations require separate, specific approval. A refusal is
a coverage limit; continue only with evidence already authorized. Consent is for
evidence only and never authorizes remediation.

Minimize local/private reads. Exclude credentials, personal content, histories,
and private project contents; sanitize external queries and output. A copy's age,
duplicate installation, lack of repo references, or absence from PATH alone does
not establish it is safe to remove.

## Advise and stop

Separate verified problems from optional improvements, core candidates, and
uncertain **Cleanup** candidates. Give concise, prioritized advice grounded in
evidence; distinguish facts from inference and include confidence, trade-offs,
and material coverage limits. Use official sources for current support/freshness
claims only with appropriate consent. A clean result means no problem was
evidenced within the stated scope—not that the whole machine is healthy.

Report in chat by default. Write a file only if requested, after agreeing on its
path and privacy; keep it outside repository documentation, preferably outside
the checkout. Provide exact remediation commands only when asked, clearly marked
as proposed and not executed. Checkup never changes the machine or repository;
do not create issues, commits, or inventories. Stop after reporting.
