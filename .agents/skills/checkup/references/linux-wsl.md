# Ubuntu/Debian and WSL checks

- Read `/etc/os-release` as data and identify kernel/architecture with bounded
  metadata. Recovery targets Ubuntu/Debian desktop or WSL Linux; other
  distributions are outside the declared setup, not automatically broken.
- Prefer local `dpkg`/APT package records and manual/automatic marks to distinguish
  selected software from dependencies. Cached APT indexes may be stale; refreshing
  them needs network consent. Linuxbrew coexistence is intentional, so verify
  executable paths and ownership before calling it a conflict.
- For WSL, inspect only the Linux distribution and relevant visible interop
  settings. Windows-host inventory is outside scope: do not invoke PowerShell,
  `cmd.exe`, `wsl.exe`, or Windows programs to inspect it. State this coverage limit.
- Inspect only relevant user-service, autostart, or container metadata. Elevated
  inspection needs specific approval; do not control services, start an engine,
  or enumerate private workloads.
- See the [maintenance guide](../../../../docs/maintenance.md#daily-maintenance)
  for APT update implications. Do not terminate or restart WSL to validate a fix.
