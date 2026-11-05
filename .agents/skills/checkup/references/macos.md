# macOS checks

- Establish OS version and architecture with bounded metadata. Recovery targets
  Apple Silicon; Intel is outside the declared setup, not proof the machine is
  broken.
- Distinguish Apple system commands from manager-owned copies. If multiple
  Homebrew prefixes or translated binaries matter, check executable/link targets
  and ownership; a second prefix is not automatically a conflict.
- Use local Homebrew formula/cask metadata, including requested-versus-dependency
  state when relevant. A GUI app's presence alone does not identify its owner or
  updater.
- Inspect only relevant login-item, LaunchAgent, or service metadata. Do not alter
  startup or service state; sensitive arguments and managed/system data need the
  appropriate consent.
- See the [maintenance guide](../../../../docs/maintenance.md#daily-maintenance)
  for Apple update implications. Do not invoke update or removal paths as probes.
