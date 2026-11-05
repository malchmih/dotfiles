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
PowerShell or Git Bash.

Before cloning this repository:

- **macOS:** install Apple's Command Line Tools (`xcode-select --install`, then
  finish the dialog) to obtain bootstrap Git. Bash and Zsh ship with macOS.
  Install [Homebrew](https://brew.sh/) after reviewing its instructions. Do not
  run ordinary `brew` or `./setup-core` with sudo.
- **Ubuntu/Debian:** have an administrator run `apt-get update` and
  `apt-get install git bash ca-certificates build-essential procps curl file sudo`
  (normally via `sudo`). These packages provide cloning, HTTPS trust, and
  Homebrew's native build prerequisites. Then install
  [Homebrew on Linux](https://docs.brew.sh/Homebrew-on-Linux) as your ordinary user.
  Core setup needs sudo only if APT-owned core packages are missing or existing
  core packages need to be marked as manually installed.
- **Both:** put Homebrew on the current shell's PATH using the installer's
  printed `eval "$(.../bin/brew shellenv)"` command. The usual prefixes are
  `/opt/homebrew` (Apple Silicon), `/usr/local` (Intel Mac), and
  `/home/linuxbrew/.linuxbrew` (Linux). Homebrew remains a separate prerequisite
  for the current core setup and maintenance commands; standalone mise does not
  replace the Homebrew CLI.

Install standalone mise before applying shared configuration, using the
[official installer instructions](toolchains.md#standalone-mise-prerequisite).
The repository does not install or update mise as a side effect of configuration
deployment. Existing Homebrew mise users should follow the documented
dependent-check and executable migration procedure before removing the formula.

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
# Review mise.toml before trusting this checkout.
mise trust
mise config ls               # inspect merged mise configuration
mise dot apply --dry-run    # preview shared links
mise dot apply              # apply shared links only
mise dot status --verbose   # inspect declared link state
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

The repository-root `mise.toml` declares 11 individual symlinks. Each source path
is relative to that file, so sources continue to follow the checkout location:

| Shared source | Home-directory link |
| --- | --- |
| `zshenv` | `~/.zshenv` |
| `zprofile` | `~/.zprofile` |
| `zshrc` | `~/.zshrc` |
| `vimrc` | `~/.vimrc` |
| `ideavimrc` | `~/.ideavimrc` |
| `update-tools` | `~/.local/bin/update-tools` |
| `update-system` | `~/.local/bin/update-system` |
| `up` | `~/.local/bin/up` |
| `cleanup` | `~/.local/bin/cleanup` |
| `opencode/AGENTS.md` | `${XDG_CONFIG_HOME:-$HOME/.config}/opencode/AGENTS.md` |
| `opencode/cli.json` | `${XDG_CONFIG_HOME:-$HOME/.config}/opencode/cli.json` |

Before trusting a checkout, review its `mise.toml`. mise merges project
configuration with your existing global and system configuration; trust does
not isolate the repository. After trust, `mise config ls` lists the loaded
configuration files. This checkout declares links only. `mise dot apply` runs
the native dotfiles phase, not package/repository/tool bootstrap or task phases.
It does not provision packages, select runtimes, run maintenance, or change the
account shell. Review any applicable `pre-dotfiles` or `post-dotfiles` hooks and
history reload commands from the merged configuration, since those remain
native mise behavior. From the checkout, the deployment workflow is:

```sh
mise trust
mise config ls
mise dot apply --dry-run
mise dot apply
mise dot status --verbose
```

If you are elsewhere, use `mise -C /path/to/dotfiles dot apply --dry-run`,
`mise -C /path/to/dotfiles dot apply`, and
`mise -C /path/to/dotfiles dot status --verbose`. The OpenCode destinations
follow mise's `xdg_config_home`: a nonempty `XDG_CONFIG_HOME`, or `$HOME/.config`
when the variable is unset or empty. Set it in the environment for each command
when using a custom location. Native apply creates missing target parent
directories.

The direct `mise dot` commands apply native dotfiles entries from the loaded
configuration (this repository declares the 11 links above). They do not
provision packages, select runtimes, run maintenance, or change the account shell;
they do not run package/repository/tool bootstrap or task phases. Review
applicable hooks and history reload commands from merged configuration as noted
above. Preview first; native
apply leaves already-matching links alone and
repoints a mismatched symlink to the declared source. A conflicting regular file
or directory is preserved and reported by native conflict preflight. Inspect
and move such data deliberately if you want the link; never use `--force`.
Failures while writing are not a transaction and can leave earlier links
applied; inspect `mise dot status --verbose` before retrying.

Only the declared targets are managed. There is no automatic stale broken-link
sweep or broad prune: inspect and remove obsolete links deliberately. Keep the
checkout available because links point into it. If you move the checkout, run
`mise dot apply` from the new location to repoint them. The maintenance links
also create their parent directory; Zsh puts `~/.local/bin` on PATH, so the
commands work from any directory and resolve their shared implementation through
the checkout symlink. Linking them does not run them; see
[maintenance](maintenance.md) before use. Setup/recovery helpers remain
checkout-local. See [OpenCode preferences](opencode.md) for scope and
application-written edits.

Links remain live into this checkout. Editing shared source files affects new
sessions without rerunning `mise dot apply`. See
[startup and PATH](local-configuration.md#startup-and-path) for session
coverage, local overrides, and refreshing an existing shell.

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
configure those deliberately. Neither package setup nor configuration deployment
changes the account shell.

## Diagnose an incomplete recovery

`mise dot status --verbose` reports the state of declared links; it is not a full
shell-correctness check. `./setup-core --check` separately inspects current core
package ownership, command paths and versions, integration scripts, and Oh My
Zsh.

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

For routine dotfiles and package updates, see [maintenance](maintenance.md).
