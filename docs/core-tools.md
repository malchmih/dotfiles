# Core tools and recovery inventory

`./setup-core` is the deliberate core installation action. It is **not** run by
shell startup or `./install`. Recovery restores a useful core environment, not
identical versions or the entire workstation. No task runner, container engine,
language toolchain, or GUI application is required. Shell enhancements are core
selections but remain optional at startup if not yet installed.

## Bootstrap prerequisites

Use a maintained macOS or Ubuntu/Debian desktop/WSL Linux release, an ordinary
user account with a writable home, and working HTTPS access to GitHub and package
repositories. Native Windows and Arch/Manjaro are not current targets. WSL means
running these commands **inside the Linux distribution**, preferably WSL 2, not
PowerShell or Git Bash. `install.ps1` is not a supported native-Windows recovery
workflow.

Before cloning this repository:

- **macOS:** install Apple's Command Line Tools (`xcode-select --install`, then
  finish the dialog) to obtain bootstrap Git. Bash and Zsh ship with macOS.
  Install [Homebrew](https://brew.sh/) after reviewing its instructions. Do not
  run ordinary `brew` or `./setup-core` with sudo.
- **Ubuntu/Debian:** have an administrator run `apt-get update` and
  `apt-get install git bash python3 ca-certificates build-essential procps curl file sudo`
  (normally via `sudo`). These bootstrap packages provide cloning, Dotbot's
  Python, HTTPS trust, and Homebrew's native build prerequisites. Then install
  [Homebrew on Linux](https://docs.brew.sh/Homebrew-on-Linux) as your ordinary user.
  The setup command needs sudo only if APT-owned core packages are missing or
  existing core packages need to be marked as manually installed.
- **Both:** put Homebrew on the current shell's PATH using the installer's
  printed `eval "$(.../bin/brew shellenv)"` command. The usual prefixes are
  `/opt/homebrew` (Apple Silicon), `/usr/local` (Intel Mac), and
  `/home/linuxbrew/.linuxbrew` (Linux). Install Python 3 for Dotbot if
  `python3 --version` fails (Homebrew `python` on macOS; APT `python3` on Linux).
  Python is an installer prerequisite, not a selected project runtime.

Homebrew is not installed automatically. Check its current
[installation requirements](https://docs.brew.sh/Installation) and
[support tiers](https://docs.brew.sh/Support-Tiers) before relying on it. As of
October 2026, Apple Silicon macOS 15+ is the normal supported Mac path; Intel
macOS is Tier 3. Linux Tier 1 requires supported Ubuntu, glibc >= 2.39, kernel
>= 3.2, and ARM64 or x86_64 with SSSE3. Debian is not promised Ubuntu's Tier 1
coverage; older glibc may cause Homebrew to install its own glibc/GCC. The default
Linux prefix maximizes bottle availability. WSL 1 and 32-bit ARM have reduced
support, and 32-bit x86 is unsupported. This helper does not repair unsupported
Homebrew installations or enable distribution repositories for you.

## Recovery sequence

```sh
git clone https://github.com/malchmih/dotfiles.git
cd dotfiles
brew update                 # deliberately refresh definitions, not package upgrades
./setup-core                # install missing core tools; clone Oh My Zsh if absent
./setup-core --check         # inspect ownership, PATH, and executable versions
./install --dry-run          # preview shared configuration (bootstrap can still fetch)
./install                   # apply shared symlinks, not packages
```

Bootstrap needs Git before setup can install the selected Git. Setup explicitly
lists all core packages even if they were once installed as dependencies. It
keeps installed selected packages, marks Homebrew core formulae as requested
and existing automatic APT core packages as manually installed (protecting both
from autoremove), installs only missing ones, and never runs a
broad upgrade or cleanup. APT refreshes indexes only when packages are missing;
`--no-upgrade --no-remove` protects already-installed packages from upgrades and
removals. Homebrew auto-refresh and installed-dependent checks are disabled for
this action; installing a missing formula may still install or upgrade a
dependency required by that formula. This is not a version lock or a package
transaction. Failures leave visible partial progress; fix the reported cause and
rerun. `--check` neither installs packages nor clones/updates Oh My Zsh.

Setup checks the selected manager's package record, not just whether some copy
of a command happens to exist. It then prints command paths and versions. If
another manager owns a competing executable, inspect `type -a git` (or the
reported command) and deliberately fix PATH/ownership; setup never uninstalls or
migrates that copy. Apple system binaries remain intact, but Homebrew's versions
should resolve first. No enhanced tool is aliased over `grep`, `find`, `cat`, or
other familiar commands: use `rg` and `http` explicitly.

After applying configuration, open a new terminal and repeat `./setup-core
--check`. On Linux, shared `.zshenv` recognizes the standard
`/home/linuxbrew/.linuxbrew` prefix when `bin/brew` is executable; its bin/sbin
follow `.local/bin` in every Zsh, including noninteractive shells. Before links
are applied, use the installer's shellenv instructions for the current shell.
For custom prefixes or noninteractive macOS access, preserve Homebrew PATH setup
outside the shared checkout: use `./scaffold-local`, then add its `bin` and `sbin`
directories to `path` in local `env.zsh`. For example, on Apple Silicon:

```zsh
path=("$HOME/.local/bin" /opt/homebrew/bin /opt/homebrew/sbin $path)
```

Use the actual prefix on other platforms. macOS login `path_helper` can reorder
PATH; shared `.zprofile` restores the usual Homebrew prefix after `.local/bin`
(`/opt/homebrew` first, otherwise `/usr/local`, only when `brew` exists there),
including noninteractive login shells. Custom prefixes need deliberate local
PATH handling; an override in local `interactive.zsh` can set final interactive
precedence. See the README's startup/PATH table. Check actual
fresh-shell resolution rather than assuming a successful setup process changed
its parent shell. The helper does not edit PATH files or authenticate GitHub;
use `gh auth login` separately when wanted, without committing credentials.

### Oh My Zsh and the account shell

Oh My Zsh uses an explicit supported exception to package management: clone its
[upstream repository](https://github.com/ohmyzsh/ohmyzsh#manual-installation)
into `${ZSH:-$HOME/.oh-my-zsh}`. Setup only clones; it does **not** invoke the
upstream installer, copy its `.zshrc` template, run Zsh, or call `chsh`. An
existing readable installation is kept without fetching or resetting it. An
incomplete existing path, including a broken symlink, is reported for manual
inspection, never deleted/replaced. If using a nondefault `ZSH`, export the same
value during setup and in local `env.zsh` before interactive startup.

Try `zsh -l` first. Only if you deliberately want Zsh as the account default,
inspect `command -v zsh` and `/etc/shells`, ensure the **chosen** executable is
listed there (administrator action if not), then run:

```sh
chsh -s "$(command -v zsh)"
```

Log out and back in afterward. Choosing macOS's `/bin/zsh` instead is legitimate
for the account shell, but it is Apple's separately updated copy. Managed
accounts, WSL launchers, and terminal profiles may override or disallow `chsh`;
configure those deliberately. Neither package setup nor Dotbot changes the
account shell.

## Selected sources and update owners

Current releases are preferred; nothing here pins package versions. Homebrew
owns the current standalone CLI releases. On Linux, APT is the deliberate
native-packaging exception for the shell, foundational Git, and fallback editor:
distribution integration, security/support lifecycle, and fewer foundational
Homebrew dependencies outweigh upstream freshness. Their versions follow the
supported distribution, not necessarily upstream's latest release.

| Core component / command | macOS source and update owner | Ubuntu/Debian source and update owner |
| --- | --- | --- |
| Zsh / `zsh` | Homebrew `zsh`; `brew upgrade zsh` | APT `zsh`; distribution package maintenance |
| Git / `git` | Homebrew `git`; `brew upgrade git` (Apple Git is bootstrap only) | APT `git`; distribution package maintenance |
| GitHub CLI / `gh` | Homebrew `gh`; `brew upgrade gh` | Homebrew `gh`; `brew upgrade gh` |
| ripgrep / `rg` | Homebrew `ripgrep`; `brew upgrade ripgrep` | Homebrew `ripgrep`; `brew upgrade ripgrep` |
| HTTPie / `http`, `https` | Homebrew `httpie`; `brew upgrade httpie` | Homebrew `httpie`; `brew upgrade httpie` |
| fzf / `fzf` and OMZ integration | Homebrew `fzf`; `brew upgrade fzf` | Same Homebrew formula/update owner |
| Inline autosuggestions | Homebrew `zsh-autosuggestions`; `brew upgrade zsh-autosuggestions` | Same Homebrew formula/update owner |
| Syntax highlighting | Homebrew `zsh-syntax-highlighting`; `brew upgrade zsh-syntax-highlighting` | Same Homebrew formula/update owner |
| Vim / `vim` | Homebrew `vim`; `brew upgrade vim` (Apple Vim remains available) | APT `vim`; distribution package maintenance |
| Oh My Zsh | Upstream Git checkout; `omz update` in interactive Zsh | Same upstream checkout/updater |
| Dotbot (configuration application only) | Committed submodule **1.24.0**; reviewed repository update | Same pinned submodule |

Refresh Homebrew definitions deliberately with `brew update` before targeted
`brew upgrade <formula...>`; setup is not an update command. Keep APT-owned tools
with OS/distribution maintenance: review `sudo apt-get update` and an explicit
targeted `sudo apt-get install --only-upgrade zsh git vim`. Native package
maintenance is distinct from Homebrew user-tool maintenance and from OS release
upgrades/reboots. Apple system Git/Zsh/Vim are owned by macOS/Command Line Tools
updates, not Homebrew. Manager updates do not inherently upgrade all installed
packages or language runtimes.

Shared Zsh enables Oh My Zsh's automatic updater (`mode auto`, upstream's normal
cadence); `omz update` also requests an update explicitly. It owns bundled
plugins/themes, **not** the Homebrew-packaged shell enhancements. Those follow
the standalone freshness policy on Linux too, rather than older distribution
plugin packages. See [interactive shell](interactive-shell.md) for loading order,
bindings, and learning references. The mixed-scope `up` alias is retired and
now refuses with guidance. Use the separate [user-tool and native maintenance
commands](maintenance.md) for deliberate updates, including whole-inventory
scope, cask/App Store exceptions, privileges, and runtime boundaries. No
scheduler is installed.

Start learning ripgrep with `rg --help` and
[ripgrep's guide](https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md).
[Learning issue #2](https://github.com/malchmih/dotfiles/issues/2) tracks trying it
in practice and reconsidering afterward; it does not block recovery.

## Curated optional inventory (manual, not provisioned)

These groups come from the inspected personal Homebrew inventory and shared
configuration references. Installation is evidence, not a requirement. Restore
only what you actually use. This is not a Brewfile, an exhaustive machine dump,
or automatic optional-application provisioning. Employer-specific inventory and
transitive libraries/codecs/certificates are intentionally omitted.

| Group | Candidates and ownership convention |
| --- | --- |
| Other CLI/developer utilities | `shellcheck`, `mas` (Mac App Store helper, macOS only), and `just` if its alias is useful. Homebrew for standalone utilities; `just` is a configuration reference, not observed as installed. |
| Media CLI | `ffmpeg`, `yt-dlp` through Homebrew; codec libraries are their dependencies, not recovery selections. |
| Containers | Podman or Docker only when needed; inspect existing engine/VM ownership first. A Homebrew Docker CLI alone is **not** a working daemon. Desktop/VM/WSL engine setup is separate and manual. Do not install both merely because aliases exist. |
| Language and Python tooling | Existing Deno, pipx, Homebrew Python, NVM, SDKMAN, and possible Gradle references are optional. Keep existing owners/data. The separate [opt-in toolchain workflow](toolchains.md) installs mise/uv, selects Node/Java, and retires active legacy selectors without deleting them. Prefer uv for future Python tooling without duplicating pipx-owned commands, and project Gradle Wrappers. No runtime installation in core setup. |
| API GUI | Bruno, installed/updated manually through Homebrew cask on macOS or its supported Linux distribution channel. Not needed for HTTPie. |
| Media GUI | VLC; Homebrew cask on macOS or native Linux package/application channel. |
| Desktop comfort | f.lux and Scroll Reverser; macOS casks. Not portable shell dependencies or Linux recovery requirements. |
| AI assistants and coding clients | Existing OpenCode, Claude Code, and Copilot CLI/desktop clients are optional independent tools. Retain their existing Homebrew/cask or upstream owner; do not install competing copies. Authentication/subscriptions and their configurations are separate. |
| IDEs | JetBrains/IdeaVim are optional as described in the README. Autosuggestions, fzf, and highlighting are core selections above, not IDE dependencies. |

Prefer one owner per executable. Use Homebrew formulae/casks for suitable macOS
optional tools, APT/native application channels where Linux integration matters,
and a documented specialist owner for runtimes or Python apps. Not every macOS
cask has a Linux counterpart. This list authorizes no removal, broad upgrade, or
automatic restoration of optional applications.
