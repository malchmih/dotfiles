# macOS checks

Apply the inspection rules to every probe. These are investigation targets, not
a mandatory command sequence or an exemption from consent.

## Baseline evidence

- Identify OS and architecture using trusted system metadata (`sw_vers`,
  `uname -m`). Note Apple Silicon versus Intel and any evidence of translated
  executables when investigating mixed installations; do not assume every second
  prefix is erroneous.
- Resolve selected commands and inspect competing PATH entries without sourcing
  shell files. Compare actual executable/link targets and owner with
  `docs/core-tools.md`. Apple's system copies are intentional and OS-owned, not
  duplicate installations to delete.
- Discover active Homebrew prefixes from existing paths and metadata. Inspect
  installed formulae/casks and requested-versus-dependency relationships using
  verified local-listing commands. Distinguish system, Homebrew, specialist,
  upstream, and managed-app ownership. A GUI application's presence alone does
  not identify its updater or justify moving it to Homebrew.
- Inspect the repo's configured deployment links, startup ordering, local
  overrides, and integration paths. Compare static intent with the agent's
  current PATH and state any fresh-shell verification gap.
- Check software-related login items, user LaunchAgents, and relevant service
  metadata for stale targets or competing software. Limit collection to useful
  fields; sensitive arguments or managed/system areas require the appropriate
  escalation. Do not load/unload jobs or change login items.
- Discover optional app/tool managers actually present, including runtime,
  Python-app, editor/plugin, and container tooling. Inventory metadata before
  invoking managers that might initialize or update themselves. For containers,
  distinguish CLI, engine/VM, and selected context without starting a daemon or
  enumerating private workloads by default.

## Follow evidence, not generic warnings

Check support/deprecation against official sources with approved research;
avoid embedding time-sensitive OS/Homebrew support tables here. Installed data
and stale package definitions cannot establish current release status.

For cleanup, investigate broken deployment links, orphaned software startup
entries, superseded app/CLI copies, and selected software caches. Confirm owners,
dependencies, and user-data preservation needs. Treat enterprise-managed tools,
Apple system binaries, and retained runtime data as intentional unless contrary
evidence exists. No uninstall, cleanup, update, or service-control commands run.
