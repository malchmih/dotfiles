# Recovery and configuration deployment

[Documentation index](../README.md#guides)

Recovery restores a useful core environment, not identical versions or an entire
workstation. The root `mise.toml` declares core packages (including Topgrade), the
Oh My Zsh checkout, shared configuration links, and separate optional repository
tools/check task.
The documented recovery command selects only the core phases explicitly; the
repository check workflow, choosing an account shell, and selecting optional
runtimes are separate actions. Full IDE setup, desktop customization, and private
configuration backups remain outside core recovery.

## Bootstrap prerequisites

Use Apple Silicon macOS or a maintained Ubuntu/Debian desktop or WSL Linux on
x86_64 or ARM64, an ordinary user account with a writable home, and working HTTPS
access to GitHub and package repositories. Intel Macs, native Windows, and
Arch/Manjaro are outside the supported recovery boundary. WSL means running
these commands **inside the Linux distribution**, preferably WSL 2, not
PowerShell or Git Bash. Package-manager support tiers, distribution releases,
and Homebrew bottle availability still apply. The config has no custom strict
platform guard or Intel-Mac fallback: mise may report resources as skipped when
a package manager is unavailable. A skipped resource is not a complete recovery
on an unsupported machine.

Before cloning this repository:

- **macOS:** install Apple's Command Line Tools (`xcode-select --install`, then
  finish the dialog) to obtain bootstrap Git. Bash and Zsh ship with macOS.
  Install [Homebrew](https://brew.sh/) after reviewing its instructions. Do not
  run ordinary `brew` with sudo.
- **Ubuntu/Debian:** have an administrator install APT, bootstrap Git, HTTPS
  trust, and Homebrew's native build prerequisites, for example
  `git bash ca-certificates build-essential procps curl file sudo` (normally
  with `sudo apt-get`). Then install
  [Homebrew on Linux](https://docs.brew.sh/Homebrew-on-Linux) as your ordinary user.
- **Both:** put the Homebrew CLI on the current shell's PATH using the installer's
  printed `eval "$(.../bin/brew shellenv)"` command. The usual supported prefixes
  are `/opt/homebrew` (Apple Silicon) and `/home/linuxbrew/.linuxbrew` (Linux).
  The CLI remains required for shell integrations, Topgrade's Homebrew step, and
  targeted manager commands. mise's built-in Homebrew package backend installs
  into a compatible prefix without invoking `brew`; it does not replace this CLI
  prerequisite.

Install standalone mise before recovery, using the
[official installer instructions](toolchains.md#standalone-mise-prerequisite).
The repository does not install or update mise during bootstrap or shell startup.
Do not install Homebrew-owned mise alongside it. Existing Homebrew mise users
should follow the documented dependent-check and executable migration procedure
before removing the formula.

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
# Review mise.toml and the existing system/global mise config before trusting.
mise trust
mise config ls
mise bootstrap --only packages,repos,dotfiles --dry-run
mise bootstrap --only packages,repos,dotfiles
mise bootstrap status
mise dot status --verbose
```

The [tool inventory](core-tools.md) lists selected packages and their owners.
The core configuration declares latest Homebrew formulae on Apple Silicon macOS
and the existing APT/Homebrew split on supported Linux, including Topgrade.
Native `apply` installs missing packages while an installed version satisfies a
`latest` declaration; updates are run separately with Topgrade or targeted native
manager commands. Installing a missing formula can still resolve or install its
required dependencies. Package application is not a transaction, and failures
can leave earlier bootstrap phases applied; inspect native status and rerun after
resolving the reported issue.

The packages, repositories, and dotfiles phases are selected explicitly. This
excludes the repository's `[tools]` (ShellCheck and Python), its `check` task,
the `bootstrap` task, automatic shell activation, and account-shell changes. Core
recovery therefore neither installs the development tools nor runs their checks.
However, `--only` is not repository isolation: mise still merges the normal
system/global/project configuration and applicable hooks. Review the files listed
by `mise config ls` and any applicable hooks before applying. The command does not
pass `--update` or `--upgrade`: ordinary recovery does not broadly upgrade
packages or fast-forward the Oh My Zsh checkout.

The native repository declaration clones the unpinned
[Oh My Zsh upstream repository](https://github.com/ohmyzsh/ohmyzsh#manual-installation)
shallowly when missing. A clean existing checkout with the matching origin is
left at its current commit by ordinary apply; it is not reset or updated. A dirty
or untracked checkout, a different origin, or a non-Git path is a native conflict
that stops repository application before changes. Inspect such state yourself;
do not force or replace it. The upstream installer is not run, no `.zshrc`
template is copied, Zsh is not launched, and `chsh` is not called. By default the
checkout is `${ZSH:-$HOME/.oh-my-zsh}`; if using a custom absolute or `~/` `ZSH`
path, export the same value when running mise bootstrap and in local `env.zsh`
before interactive startup. The existing OMZ automatic updater policy remains
unchanged. Topgrade includes an Oh My Zsh update step, so running it can update
this checkout; review its current supported integrations before use. See
[maintenance](maintenance.md).

After recovery, open a new terminal and inspect native status if needed. Try
`zsh -l` if the terminal does not already start Zsh. Optional next steps:

- [Scaffold local configuration](local-configuration.md#create-local-files) for
  incremental machine-specific additions; no local files are required.
- [Try the shell features](interactive-shell.md#try-it-in-a-fresh-terminal) and
  [fallback editor](editors.md).
- [Set up development toolchains](toolchains.md) only if wanted.
- Run `gh auth login` separately when wanted. Use existing credential mechanisms;
  do not commit credentials to shared files or examples.

## Apply shared configuration safely

The repository-root `mise.toml` declares 7 individual symlinks. Each source path
is relative to that file, so sources continue to follow the checkout location:

| Shared source | Home-directory link |
| --- | --- |
| `zshenv` | `~/.zshenv` |
| `zprofile` | `~/.zprofile` |
| `zshrc` | `~/.zshrc` |
| `vimrc` | `~/.vimrc` |
| `ideavimrc` | `~/.ideavimrc` |
| `opencode/AGENTS.md` | `${XDG_CONFIG_HOME:-$HOME/.config}/opencode/AGENTS.md` |
| `opencode/cli.json` | `${XDG_CONFIG_HOME:-$HOME/.config}/opencode/cli.json` |

Before trusting a checkout, review its `mise.toml`. mise merges project
configuration with your existing global and system configuration; trust does
not isolate the repository. After trust, `mise config ls` lists the loaded
configuration files. This checkout also declares core packages, the Oh My Zsh
repository, and the optional local check tools/task. The documented recovery
command selects packages, repositories, and dotfiles only. Direct `mise dot apply`
still runs only the native dotfiles phase; it does not provision packages,
repositories, or development tools, run checks, select runtimes, run maintenance,
or change the account shell. Review applicable hooks and history reload commands
from merged configuration, since those remain native mise behavior. To apply
shared links alone from the checkout:

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
configuration (this repository declares the 7 links above). They do not
provision packages or tools, select runtimes, run maintenance or repository
checks, or change the account shell; they do not run package/repository/tool
bootstrap or task phases. Review
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
checkout available because preference links point into it. If you move the
checkout, run `mise dot apply` from the new location to repoint them. Topgrade is
a Homebrew Core package declared in `mise.toml`; only the selected package
bootstrap phase provisions it, and `mise dot apply` neither installs nor runs it.
See [maintenance](maintenance.md) before using it. The optional toolchain helper
remains checkout-local. See [OpenCode preferences](opencode.md) for scope and
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

`mise bootstrap status` reports declared bootstrap state, while
`mise dot status --verbose` reports declared links. Focused native checks are
`mise bootstrap packages status`, `mise bootstrap repos status`, and the dot
status command. Aggregate bootstrap status can include optional resources from
merged global configuration, and unavailable managers/resources may be reported
as skipped. Status does not check command ownership, PATH, executable versions,
shell integrations, or full shell correctness; skipped resources do not establish
complete recovery on an unsupported platform.

If a command is missing or resolves to another owner's executable, inspect
`type -a git` (or the reported command). Deliberately resolve PATH/ownership
conflicts; native bootstrap does not uninstall or migrate competing copies.
Apple system binaries remain intact, but selected Homebrew tools should resolve
first.

Recovery does not edit shell startup activation or its parent shell's PATH. Put
Homebrew on PATH with its printed shellenv instructions and check actual
fresh-shell resolution after applying links. For standard prefixes, custom
prefixes, or noninteractive access, see
[PATH precedence and Homebrew](local-configuration.md#path-precedence-and-homebrew).
Startup never installs packages or audits missing commands; use native status
and feature-specific checks from the [shell guide](interactive-shell.md#missing-components--deliberate-checks).

For routine dotfiles and package updates, see [maintenance](maintenance.md).
