# Ubuntu/Debian and WSL checks

Apply the inspection rules to every probe. Use Linux guidance for both desktop
Linux and WSL; add the interop checks only when WSL is detected.

## Linux baseline evidence

- Read distribution identity from `/etc/os-release` as data, not shell code, and
  inspect kernel/architecture metadata. Confirm supported-distribution facts
  through approved official research when needed.
- Discover package owners. Use verified local metadata queries such as
  `dpkg-query`, `apt-mark showmanual`/`showauto`, and installed Homebrew listings.
  Optional Snap, Flatpak, runtime, and Python-app managers matter only if present.
  Distinguish explicitly selected packages from dependencies before recommending
  cleanup. Never use autoremove/cleanup execution as an inventory shortcut.
- Compare selected executable paths with `docs/core-tools.md`: native APT
  ownership of foundational tools is deliberate, while other selected CLI tools
  use Homebrew. Distribution versions/backports need not match upstream latest.
  APT and Linuxbrew coexistence is not itself a conflict.
- Inspect deployment links, startup/PATH ordering, shell integrations, and local
  overrides statically. Confirm manager activation and executable ownership
  without sourcing startup hooks or activating legacy runtime managers.
- Inspect relevant user-service and desktop-autostart metadata with bounded,
  verified queries. Inspect system-service configuration only when relevant and
  permitted; elevation is high-tier. Minimize command arguments/log content.
  No daemon reload, start/stop, enable/disable, or service repair.
- Inspect optional container/runtime setup through metadata first. Distinguish
  client from engine and existing sockets/contexts from a working service. Do
  not start engines or inspect private workload contents by default.

Cached upgrade listings reflect cached indexes, not necessarily current support
or available updates. Index refresh needs its own effects-aware approval; package,
manager, distribution upgrades, and reboots remain follow-up advice only.

## WSL interop boundary

Identify WSL from available Linux-side kernel/environment evidence; state
uncertainty if generation or host details cannot be established safely. Review
Linux-side WSL configuration and Windows PATH entries visible in the current
environment. Investigate whether Windows executables shadow intended Linux tools,
whether shell/launcher assumptions differ, and whether multiple container-engine
integrations compete. Observe configuration rather than changing mounts,
interop, PATH propagation, services, or distro settings.

The default audit covers Ubuntu and WSL interop, not the Windows host's installed
apps, registry, services, security posture, or all other distributions. Do not
launch PowerShell, `cmd.exe`, `wsl.exe`, or Windows programs as an implicit bridge
to host inventory. A justified Windows-host software inspection is a separately
scoped extension with a new plan and the same risk/consent rules; prefer official
documentation and report unsupported checks instead of improvising them. Never
terminate or restart WSL to verify a proposed fix.

## Cleanup cautions

Installed runtimes, project environments, caches, mounted
Windows directories, and container data can retain valuable state. Presence,
age, or inactive PATH entries alone establish no removal case. Prefer package
dependency metadata and activation references; ask about usage or report an
uncertain candidate without opening histories or private projects.
