# Tools and ownership

[Documentation index](../README.md#guides)

The repository-root `mise.toml` declares the core package selections and Oh My
Zsh checkout for native mise bootstrap. The documented recovery command applies
the packages, repositories, and dotfiles phases explicitly; shell startup and a
direct `mise dot apply` do not provision packages. See [recovery](recovery.md)
for prerequisites, preview/apply, repeat-run behavior, and diagnostics. No task
runner, container engine, language toolchain, or GUI application is required for
Core recovery. The repository-local Python tool and explicit
[`mise run check` workflow](maintenance.md#repository-checks) are optional and
remain outside the recovery phases. Shell enhancements remain optional at startup
if they are not yet installed.

Enhanced tools keep their own names: use `rg` and `http` explicitly. Nothing here
aliases them over `grep`, `find`, `cat`, or other familiar commands. Convenience
aliases still require their tools: `restart-podman` needs Podman. Its presence
does not make Podman a core dependency.

## Selected sources and update owners

The declarations use the unpinned `latest` package state. Native mise apply
installs missing packages and accepts any installed version; it does not broadly
upgrade installed selections. The built-in Homebrew backend installs into a
Homebrew-compatible prefix without invoking the `brew` CLI; installed formulae
remain visible to the CLI in that prefix. Keep the CLI on PATH for shell
integrations, Topgrade's Homebrew step, and targeted manager commands. On Linux,
APT is the deliberate native-packaging exception for the shell, foundational Git, and
fallback editor: distribution integration and support lifecycle outweigh
upstream freshness, so their versions follow the supported distribution.

| Core component / command | macOS provisioning / update | Ubuntu/Debian provisioning / update |
| --- | --- | --- |
| Topgrade / `topgrade` | mise `brew:topgrade`; Topgrade's detected Homebrew step or `brew upgrade topgrade` | mise `brew:topgrade`; Topgrade's detected Homebrew step or `brew upgrade topgrade` |
| Zsh / `zsh` | mise `brew:zsh`; Homebrew CLI `brew upgrade zsh` (Apple Zsh remains available) | mise `apt:zsh`; distribution package maintenance |
| Git / `git` | mise `brew:git`; Homebrew CLI `brew upgrade git` (Apple Git is bootstrap only) | mise `apt:git`; distribution package maintenance |
| GitHub CLI / `gh` | mise `brew:gh`; Homebrew CLI `brew upgrade gh` | mise `brew:gh`; Homebrew CLI `brew upgrade gh` |
| ripgrep / `rg` | mise `brew:ripgrep`; Homebrew CLI `brew upgrade ripgrep` | mise `brew:ripgrep`; Homebrew CLI `brew upgrade ripgrep` |
| HTTPie / `http`, `https` | mise `brew:httpie`; Homebrew CLI `brew upgrade httpie` | mise `brew:httpie`; Homebrew CLI `brew upgrade httpie` |
| fzf / `fzf` and OMZ integration | mise `brew:fzf`; Homebrew CLI `brew upgrade fzf` | mise `brew:fzf`; Homebrew CLI `brew upgrade fzf` |
| Inline autosuggestions | mise `brew:zsh-autosuggestions`; Homebrew CLI targeted upgrade | mise `brew:zsh-autosuggestions`; Homebrew CLI targeted upgrade |
| Syntax highlighting | mise `brew:zsh-syntax-highlighting`; Homebrew CLI targeted upgrade | mise `brew:zsh-syntax-highlighting`; Homebrew CLI targeted upgrade |
| Vim / `vim` | mise `brew:vim`; Homebrew CLI `brew upgrade vim` (Apple Vim remains available) | mise `apt:vim`; distribution package maintenance |
| Oh My Zsh | Unpinned shallow mise repository checkout; native updater and Topgrade step | Same checkout and steps |

Refresh Homebrew itself and definitions deliberately with `brew update` before
targeted `brew upgrade <formula...>`; mise apply is not an update command. Keep
APT-owned tools with OS/distribution maintenance. Topgrade is the Daily
maintenance command and follows upstream detection and prompt defaults; see
[maintenance](maintenance.md) for its scope and system-update implications.
Native package maintenance is distinct from OS release upgrades/reboots. Apple
system Git/Zsh/Vim are owned by macOS/Command Line Tools updates, not Homebrew.

Oh My Zsh retains its configured automatic updater for its checkout, bundled
plugins, and themes, **not** the Homebrew-packaged shell enhancements. Topgrade
also includes an Oh My Zsh update step, plus other eligible shell, editor,
runtime, and package-manager integrations beyond this core inventory. See
[the shell guide](interactive-shell.md) for shell behavior and
[maintenance](maintenance.md) for the current upstream scope; use native manager
commands for targeted updates.

Start learning ripgrep with `rg --help` and
[ripgrep's guide](https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md).

## Existing package ownership

The mise declarations do not continuously change package-manager ownership
metadata, and autoremove does not consult `mise.toml`. On an existing machine,
review current markings once before relying on autoremove. This is an optional,
manual migration, not part of recovery:

- **Homebrew:** inspect dependency-only formulae with
  `brew list --formula --no-installed-on-request`. For only the installed core
  formulae you have reviewed and want to retain, use Homebrew's native
  `brew tab --installed-on-request --formula <formula...>` command. Check
  `brew help tab` if the installed CLI does not provide that command; do not
  edit Homebrew receipts or force-reinstall packages to change their markings.
- **APT:** inspect `apt-mark showauto zsh git vim`; then run
  `sudo apt-mark manual <reviewed-auto-packages...>` for only the installed
  core packages that should be retained. Do not run `autoremove` as part of this
  migration.

These commands only change whether the package manager considers a package
requested; they do not upgrade or remove packages. Repeat the review on each
machine as appropriate. For occasional package housekeeping, see
[native Cleanup commands](maintenance.md#occasional-cleanup).

## Curated optional inventory (manual, not provisioned)

Restore only what you actually use. This is a curated list of useful optional
applications, not a Brewfile, an exhaustive machine dump, or automatic optional
provisioning. Employer-specific inventory and transitive
libraries/codecs/certificates are intentionally omitted.

| Group | Candidates and ownership convention |
| --- | --- |
| Other CLI/developer utilities | `mas` (Mac App Store helper, macOS only). Homebrew for standalone utilities. |
| Media CLI | `ffmpeg`, `yt-dlp` through Homebrew; codec libraries are their dependencies, not recovery selections. |
| Containers | Podman or Docker only when needed; inspect existing engine/VM ownership first. A Homebrew Docker CLI alone is **not** a working daemon. Desktop/VM/WSL engine setup is separate and manual. Do not install both merely because aliases exist. |
| Language and Python tooling | Deno, pipx, Homebrew Python, and standalone Gradle are optional. Keep existing owners/data. The [toolchain guide](toolchains.md) describes optional standalone-mise Node/Java/CPython defaults and Homebrew-owned uv for project environments, dependencies, and CLI applications. Prefer uv for project tooling without duplicating pipx-owned commands, and project Gradle Wrappers. |
| API GUI | Bruno, installed/updated manually through Homebrew cask on macOS or its supported Linux distribution channel. Not needed for HTTPie. |
| Media GUI | VLC; Homebrew cask on macOS or native Linux package/application channel. |
| Desktop comfort | f.lux and Scroll Reverser; macOS casks. Not portable shell dependencies or Linux recovery requirements. |
| AI assistants and coding clients | OpenCode, Claude Code, and Copilot CLI/desktop clients are optional independent tools. Retain their existing Homebrew/cask or upstream owner; do not install competing copies. Only selected [OpenCode preferences](opencode.md) are shared by mise; client installation, authentication/subscriptions, provider/model choices, and other client configurations remain separate. |
| IDEs | JetBrains/IdeaVim are optional; see [editors](editors.md). Autosuggestions, fzf, and highlighting are core shell selections, not IDE dependencies. |

Prefer one owner per executable. Use Homebrew formulae/casks for suitable macOS
optional tools, APT/native application channels where Linux integration matters,
and a documented specialist owner for runtimes or Python apps. Not every macOS
cask has a Linux counterpart. This list authorizes no removal, broad upgrade, or
automatic restoration of optional applications.
