# Deliberate maintenance

Run these commands **from this checkout**, as your ordinary account, after
reading their scopes. Installation (`setup-core`, `setup-toolchains`), applying
configuration (`install`), and maintenance are different actions. Nothing here
runs on shell startup. The former mixed-scope `up` alias is retired: `up` now
prints guidance and returns failure without updating anything. Start a fresh
shell to replace the old alias; inspect local overrides if it still behaves
differently. The scripts work from Bash/Zsh without OMZ aliases/plugins.

## User tools: whole selected inventories

```sh
./update-tools --help
./update-tools refresh        # Homebrew itself + definitions/taps, NOT packages
brew outdated --formula      # review candidates; inspection is manager-native
uv tool list                 # if installed
pipx list                    # if installed
./update-tools upgrade       # deliberate broad upgrade, not a preview
```

**`upgrade` covers ALL installed Homebrew formulae, uv tool environments, and
pipx applications owned by the invoked managers**, including optional and work
packages, dependencies, and managers—not just names in this repository's core
inventory. Inspect `type -a brew uv pipx` and manager inventories first. Invoking
the scripts is consent to that scope; there is no second custom confirmation.
Use native targeted commands instead when a broad update is inappropriate.
Homebrew's pins and each manager's constraints/exclusions still apply; this is
not a promise every installed item changes version.

- `refresh` runs `brew update`: it refreshes package definitions/taps **and
  updates Homebrew itself**. It does not upgrade installed packages. uv/pipx
  have no equivalent required global metadata-refresh step here; their upgrade
  commands query their configured package indexes directly.
- `upgrade` runs `brew upgrade --formula`, `uv tool upgrade --all`, and
  `pipx upgrade-all`, in that order. Homebrew auto-refresh and install cleanup
  are disabled to keep the explicit refresh/upgrade distinction. Refresh first;
  stale definitions otherwise mean stale upgrade candidates. No extra cleanup,
  pruning, forced linking, uninstall, or migration is requested.
- Homebrew upgrades its formula-owned managers (including optional mise/uv and
  pipx if Homebrew owns it), and packaged fzf/autosuggestions/highlighting. It
  does not inherently update the applications inside uv/pipx environments;
  those receive their own commands afterward. A pipx installed by another
  owner still updates its apps here, but **pipx itself stays with that owner**.
  Do not use `mise self-update` or `uv self update` for Homebrew-owned managers.
- Existing pipx applications stay with pipx. uv updates only its own tool
  environments; no application is installed in the other manager or given a
  competing executable link. Existing ownership conflicts are not repaired.
  Inspect `type -a <command>`, `uv tool list`, and `pipx list` before adding tools.
- Missing managers on PATH print `SKIP` and do not block the others. An invoked
  manager failure prints `FAILED`, leaves partial progress in place, and the
  other independent managers are still attempted. Any failure gives nonzero
  exit status. All missing is a successful no-op with visible skips, **not**
  evidence that an intended recovery is complete. Fix PATH or deliberately
  install the optional layer before retrying. Nothing installs a missing manager.

This is not a transaction or a custom dependency orchestrator. External package
installers/build hooks still run their own code; review sources and policies.
The user-tool command never invokes sudo or APT/Apple OS maintenance. Homebrew
formula upgrades can also update Homebrew-owned Node/Python/etc. if you installed
them; the command does not claim exclusive runtime ownership outside the chosen
mise/uv workflow. Configured taps and package indexes remain user-owned.

### OMZ and runtimes are distinct owners

Oh My Zsh retains `zstyle ':omz:update' mode auto` and its native cadence. For
an immediate manual update, run **`omz update` in interactive Zsh**, with the
desired `ZSH` checkout loaded. It updates OMZ, bundled plugins, and awesomepanda,
not external Homebrew-packaged plugins. Missing OMZ does not block the scripts;
core recovery can install it later. The helper deliberately does not launch an
interactive shell (which could trigger local code and the automatic updater).

Upgrading mise/uv binaries is **not** selecting new runtime versions:

- Rerun `./setup-toolchains` only to deliberately reselect newest-stable personal
  Node/Temurin JDK pins. It runs from home, preserves older installations and
  unrelated global entries, and does not rewrite project declarations. Review
  home config/hooks first. It can install missing mise/uv, unlike maintenance.
- Project pins/lockfiles and dependencies remain project decisions. For a
  reviewed project, use `mise install` for declared versions; inspect `mise
  outdated` and the scope of `mise upgrade` before deliberately changing them.
  Do not run a blanket runtime upgrade from arbitrary checkouts or add `--bump`
  as routine cleanup. NVM/SDKMAN are not reactivated or updated here; their
  existing data is not deleted.
- uv-managed Python is separate from uv tools and bootstrap/system Python.
  Inspect `uv python list --only-installed` and `uv python upgrade --help` before
  an explicit `uv python upgrade` (managed Python patch updates, not a blanket
  project or major-version change). No Python runtime upgrade, `uv lock
  --upgrade`, project sync, or legacy runtime deletion is requested by these
  helpers. Tool upgrades may update their own environment dependencies.

See [toolchain ownership and trust](toolchains.md) and
[interactive shell updates](interactive-shell.md#updates-and-history).

## Native packages and OS: a separate privileged decision

```sh
./update-system --help
./update-system refresh
# Review candidates and save work before the separate upgrade invocation.
```

### Ubuntu/Debian desktop and WSL

`refresh` runs **`sudo apt-get update`**, refreshing configured repository indexes,
not installed software. `upgrade` runs **`sudo apt-get upgrade --no-remove`**:

```sh
apt list --upgradable                  # inspection after refresh
apt-get --simulate upgrade --no-remove # native preview; no sudo required
./update-system upgrade               # review APT's normal confirmation
```

This is the **whole native package inventory**, including APT-owned Zsh/Git/Vim,
bootstrap Python, libraries, services, and optional native applications. Those
remain in privileged distribution maintenance even though some are conceptually
user tools. Homebrew formulae remain in `update-tools`; neither manager upgrades
the other's packages. `upgrade` does not implicitly refresh indexes, pass `-y`,
remove packages, invoke `full-upgrade`/`dist-upgrade`, change distribution releases,
run autoremove, or request a reboot. Held/dependency-transition packages can stay
back for separate administrator review. Native package scripts can restart
services and configured system policy may have additional effects; the helper
is not a sandbox or a way to disable existing unattended-upgrade policies.

Use the ordinary account with sudo permission. Missing sudo/APT, unsupported
distributions, authentication errors, repository/network errors, or locks fail
visibly; the script stops that native action, does not remove locks, and does
not try another package manager. Resolve the cause before retrying. A reboot
requirement (for example `/var/run/reboot-required`) needs a separate decision.

**Inside WSL**, these commands maintain only the Linux distribution's native
packages. They do not update Windows, the WSL host/kernel, Microsoft Store apps,
or firmware. Windows Update and an intentional host-side `wsl --update` are
separate Windows workflows; no `wsl --shutdown` or reboot is invoked here.
Linux desktop kernel/service/reboot behavior cannot be assumed for WSL.

### macOS

`refresh` runs **`softwareupdate --list`** without sudo to scan/list Apple updates.
It does not refresh Homebrew or install anything. After reviewing the exact
version and label, request **one** update explicitly:

```sh
./update-system upgrade 'EXACT LABEL COPIED FROM THE LIST'
```

This runs `sudo softwareupdate --install "$label"`, never `--all`, `--restart`,
or `--fetch-full-installer`. Select maintenance updates for the current macOS
major release, **not** a new major-release offer; the helper cannot infer your
release policy from Apple's changing labels. Major upgrades are a separate
manual System Settings workflow. Apple-owned system tools/Command Line Tools
follow Apple's available updates, not Homebrew's formula inventory. Some updates
need volume-owner authentication, MDM approval, a GUI, or a later restart;
sudo alone is not guaranteed sufficient on Apple Silicon. Use System Settings
when required. No password is collected or passed through stdin by this script,
and no reboot is requested; installation may remain incomplete pending one.

### Optional native/GUI applications

Homebrew **casks** and Mac App Store apps are intentionally outside both helpers:
they are not formulae or Apple OS updates, and their installers may need admin
approval or GUI interaction. Inspect owners and run these separately if wanted:

```sh
brew outdated --cask
brew upgrade --cask           # all eligible installed casks; may ask for sudo
mas outdated                 # optional macOS-only manager, signed-in App Store
mas upgrade                  # all eligible App Store apps; may need approval
```

Normal Homebrew cask rules skip some auto-updating/`:latest` casks; inspect
`brew outdated --cask --greedy` if needed, rather than silently overriding their
policy. Do not run brew itself with sudo. Neither casks nor `mas` are Linux
requirements. Linux Snap/Flatpak/vendor self-updaters also retain their own
native ownership/policies and are not invoked here. No unrelated software is
removed, migrated, or forcibly taken over by maintenance.

## Recovery, troubleshooting, and future scheduling

- Update this checkout deliberately with Git after reviewing changes; new shell
  sessions see symlinked configuration immediately. Neither helper pulls the
  dotfiles repo, changes Dotbot's pinned submodule, applies links, or changes the
  login shell. See [core recovery](core-tools.md) and the README's Dotbot section.
- `./setup-core --check` diagnoses the selected core owners/PATH after recovery;
  it is not an updater. On errors inspect manager-native output, `type -a`,
  `brew doctor`, available disk space, repository/index access, configured pins,
  and environment ownership. Do not fix failures by indiscriminate sudo, deleting
  runtimes/locks, or reinstalling apps under another manager.
- Optional scheduling is **future work only**. If later wanted, choose manager
  scopes, notifications/logs, network/session PATH, credentials, failure policy,
  and a safe maintenance window before designing a cron/launchd/systemd job.
  Privileged native maintenance and interactive authentication need separate
  policy. No jobs, timers, services, or scheduling subsystem are added or enabled
  here. This does not disable the retained component-native OMZ automatic updater
  or existing OS/application update policies.

## Verification boundaries

Use `bash -n update-tools` and `bash -n update-system`, ShellCheck if available, both `--help`
commands, and a fresh-shell `up` refusal. Disposable PATH command probes can
check dispatch, scopes, skips, and error statuses without performing upgrades.
They do not establish real package compatibility or a Linux pass. No persistent
test suite/fixtures or CI are part of this workflow. Actual implementation
observations are recorded in #14; [#15](https://github.com/malchmih/dotfiles/issues/15)
collects the real Linux/WSL integration follow-up. Do not run broad upgrades just
to demonstrate a helper.
