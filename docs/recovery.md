# Recovery and configuration deployment

[Documentation index](../README.md#guides)

Recovery restores a useful core environment, not identical versions or an entire
workstation. Installing tools, applying shared configuration, and choosing an
account shell are separate actions. Language runtimes, full IDE setup, desktop
customization, and private configuration backups remain outside core recovery.

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
  (normally via `sudo`). These packages provide cloning, Dotbot's Python, HTTPS
  trust, and Homebrew's native build prerequisites. Then install
  [Homebrew on Linux](https://docs.brew.sh/Homebrew-on-Linux) as your ordinary user.
  Core setup needs sudo only if APT-owned core packages are missing or existing
  core packages need to be marked as manually installed.
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
support, and 32-bit x86 is unsupported. Setup does not repair unsupported
Homebrew installations or enable distribution repositories for you.

## Recover the core environment

```sh
git clone https://github.com/malchmih/dotfiles.git
cd dotfiles
brew update                 # refresh Homebrew and definitions, not packages
./setup-core                # install missing core tools; clone Oh My Zsh if absent
./setup-core --check         # inspect ownership, PATH, and executable versions
./install --dry-run          # preview shared configuration; bootstrap can still fetch
./install                   # apply shared symlinks, not packages
```

The [tool inventory](core-tools.md) lists selected packages and their owners.
Bootstrap needs Git before setup can install the selected Git. Setup explicitly
lists all core packages even if they were once installed as dependencies. It
keeps installed selected packages, marks Homebrew core formulae as requested
and existing automatic APT core packages as manually installed (protecting both
from autoremove), installs only missing ones, and never runs a broad upgrade or
cleanup. APT refreshes indexes only when packages are missing; `--no-upgrade
--no-remove` protects already-installed packages from upgrades and removals.

Homebrew auto-refresh and installed-dependent checks are disabled for setup;
installing a missing formula may still install or upgrade a dependency required
by that formula. This is not a version lock or a package transaction. Failures
leave visible partial progress; fix the reported cause and rerun. `--check`
neither installs packages nor clones/updates Oh My Zsh.

Oh My Zsh is an explicit exception to package management: setup clones its
[upstream repository](https://github.com/ohmyzsh/ohmyzsh#manual-installation)
into `${ZSH:-$HOME/.oh-my-zsh}`. It does **not** invoke the upstream installer,
copy a `.zshrc` template, run Zsh, or call `chsh`. An existing readable installation
is kept without fetching or resetting it. An incomplete existing path, including
a broken symlink, is reported for inspection, never deleted/replaced. If using
a nondefault `ZSH`, export the same value during setup and in local `env.zsh`
before interactive startup.

After applying configuration, open a new terminal and repeat `./setup-core --check`.
Try `zsh -l` if the terminal does not already start Zsh. Optional next steps:

- [Scaffold local configuration](local-configuration.md#create-local-files) for
  incremental machine-specific additions; no local files are required.
- [Try the shell features](interactive-shell.md#try-it-in-a-fresh-terminal) and
  [fallback editor](editors.md).
- [Set up development toolchains](toolchains.md) only if wanted.
- Run `gh auth login` separately when wanted. Use existing credential mechanisms;
  do not commit credentials to shared files or examples.

## Apply shared configuration safely

The `install` bootstrap initializes the pinned Dotbot submodule and its nested
dependencies itself; a recursive clone is unnecessary. Dotbot links:

| Shared source | Home-directory link |
| --- | --- |
| `zshenv` | `~/.zshenv` |
| `zprofile` | `~/.zprofile` |
| `zshrc` | `~/.zshrc` |
| `vimrc` | `~/.vimrc` |
| `ideavimrc` | `~/.ideavimrc` |
| `update-tools` | `~/.local/bin/update-tools` |
| `update-system` | `~/.local/bin/update-system` |
| `opencode/AGENTS.md` | `${XDG_CONFIG_HOME:-$HOME/.config}/opencode/AGENTS.md` |
| `opencode/cli.json` | `${XDG_CONFIG_HOME:-$HOME/.config}/opencode/cli.json` |

The `install` wrapper supplies the default `XDG_CONFIG_HOME` for Dotbot; export
it before invoking `./install` to use a different config directory. OpenCode
links create their parent directories even if the optional client is absent.
See [OpenCode preferences](opencode.md) for scope and application-written edits.

The maintenance links also create their parent directory when needed. The shared
Zsh configuration puts `~/.local/bin` on PATH, making `update-tools` and
`update-system` available from any directory. Setup/recovery helpers remain
checkout-local; the checkout is not added wholesale to PATH (in particular,
`./install` must not shadow the system `install` command). Linking the maintenance
commands does not run them; see [maintenance](maintenance.md) before use.

Existing links can be relinked; conflicting regular files are **not** forcibly
replaced. Inspect and preserve their contents, moving them aside deliberately
if you want the shared links, then rerun `./install`. Application is best-effort:
a failed link does not prevent other links from being attempted, but Dotbot
reports failure overall. There is no custom preflight, transaction, or rollback.
The configured clean step removes broken links pointing into this checkout from
the home directory; it is not general home-directory cleanup.

`./install --dry-run` forwards Dotbot's upstream dry-run option. It is **not a
strict read-only wrapper**: bootstrap synchronizes/initializes submodules before
Dotbot runs, and arbitrary shell actions in a future config would need their own
care. `./install --help` lists upstream options, including opt-in
`--exit-on-failure`; ordinary application does not enable fail-fast behavior.

Links remain live into this checkout. Editing shared source files affects new
sessions without rerunning Dotbot. Keep the checkout in place; moving it requires
reapplying links from the new location. See [startup and PATH](local-configuration.md#startup-and-path)
for session coverage, local overrides, and refreshing an existing shell.

## Choose the account shell

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

## Diagnose an incomplete recovery

Setup checks the selected manager's package record, not just whether some copy
of a command exists. `./setup-core --check` then prints command paths and versions
and reports missing integration scripts or incomplete Oh My Zsh.

If a command is missing or resolves to another owner's executable, inspect
`type -a git` (or the reported command). Deliberately fix PATH/ownership; setup
never uninstalls or migrates competing copies. Apple system binaries remain
intact, but selected Homebrew tools should resolve first.

Setup does not edit its parent shell's PATH. Before shared links are applied,
use Homebrew's printed shellenv instructions. After application, check actual
fresh-shell resolution. For standard prefixes, custom prefixes, or noninteractive
access, see [PATH precedence and Homebrew](local-configuration.md#path-precedence-and-homebrew).
Startup never installs packages or audits missing commands; use diagnostics
deliberately. Feature-specific checks live in the [shell guide](interactive-shell.md#missing-components--deliberate-checks).

## Update Dotbot

Dotbot is pinned to **1.24.0** as a Git submodule. Ordinary `./install` uses the
repository's recorded submodule revision, not the latest remote version.
To intentionally advance it, start with clean repository/submodule worktrees
and review the chosen upstream release. From this checkout:

```sh
DOTBOT_TAG='vX.Y.Z' # replace with the reviewed upstream release tag
git -C dotbot fetch --tags origin
git -C dotbot checkout "$DOTBOT_TAG"
git -C dotbot submodule sync --recursive
git -C dotbot submodule update --init --recursive
git diff --submodule=log -- dotbot
git -C dotbot submodule status --recursive
git add dotbot
git commit -m "Update Dotbot to $DOTBOT_TAG"
# Only after recording the selection:
./install --dry-run
```

Replace `vX.Y.Z` with the reviewed tag before running the commands. Updating nested dependencies
means checking out the revisions recorded by that Dotbot release (including
PyYAML), not arbitrarily advancing them to remote heads. Review the resulting
dependency state as well as the Dotbot change. **Record the new gitlink before
ordinary bootstrap** so submodule initialization does not restore the previous
selection. Do not add another submodule-update action to `install.conf.yaml`:
the bootstrap already performs required initialization.

For routine dotfiles and package updates, see [maintenance](maintenance.md).
