# Tools and ownership

[Documentation index](../README.md#guides)

`./setup-core` explicitly installs the core selections below. It is not run by
shell startup or `./install`; see [recovery](recovery.md) for prerequisites,
setup/repeat-run behavior, configuration deployment, and diagnostics. No task
runner, container engine, language toolchain, or GUI application is required.
Shell enhancements are core selections but remain optional at startup if not
yet installed.

Enhanced tools keep their own names: use `rg` and `http` explicitly. Nothing here
aliases them over `grep`, `find`, `cat`, or other familiar commands. Convenience
aliases still require their tools: `j` needs `just`, and `restart-podman` needs
Podman. Their presence does not make either tool a core dependency.

## Selected sources and update owners

Current releases are preferred; core packages are not version-pinned. Homebrew
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
| Dotbot (configuration application only) | Committed submodule **1.24.0**; [reviewed repository update](recovery.md#update-dotbot) | Same pinned submodule |

Refresh Homebrew itself and definitions deliberately with `brew update` before
targeted `brew upgrade <formula...>`; setup is not an update command. Keep
APT-owned tools with OS/distribution maintenance: review `sudo apt-get update`
and an explicit targeted `sudo apt-get install --only-upgrade zsh git vim`.
Native package maintenance is distinct from Homebrew user-tool maintenance and
from OS release upgrades/reboots. Apple system Git/Zsh/Vim are owned by
macOS/Command Line Tools updates, not Homebrew.

Oh My Zsh's automatic updater owns its checkout, bundled plugins, and themes,
**not** the Homebrew-packaged shell enhancements. See [the shell guide](interactive-shell.md)
for feature behavior and targeted updates. The separate [maintenance commands](maintenance.md)
cover deliberate whole-inventory user-tool and native updates. Manager updates
do not inherently upgrade language runtimes or every manager-owned application.

Start learning ripgrep with `rg --help` and
[ripgrep's guide](https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md).

## Curated optional inventory (manual, not provisioned)

Restore only what you actually use. This is a curated list of useful optional
applications, not a Brewfile, an exhaustive machine dump, or automatic optional
provisioning. Employer-specific inventory and transitive
libraries/codecs/certificates are intentionally omitted.

| Group | Candidates and ownership convention |
| --- | --- |
| Other CLI/developer utilities | `shellcheck`, `mas` (Mac App Store helper, macOS only), and `just` if its alias is useful. Homebrew for standalone utilities. |
| Media CLI | `ffmpeg`, `yt-dlp` through Homebrew; codec libraries are their dependencies, not recovery selections. |
| Containers | Podman or Docker only when needed; inspect existing engine/VM ownership first. A Homebrew Docker CLI alone is **not** a working daemon. Desktop/VM/WSL engine setup is separate and manual. Do not install both merely because aliases exist. |
| Language and Python tooling | Deno, pipx, Homebrew Python, NVM, SDKMAN, and standalone Gradle are optional. Keep existing owners/data. The separate [opt-in toolchain workflow](toolchains.md) installs mise/uv and selects Node/Java, without deleting legacy selectors/data. Prefer uv for future Python tooling without duplicating pipx-owned commands, and project Gradle Wrappers. |
| API GUI | Bruno, installed/updated manually through Homebrew cask on macOS or its supported Linux distribution channel. Not needed for HTTPie. |
| Media GUI | VLC; Homebrew cask on macOS or native Linux package/application channel. |
| Desktop comfort | f.lux and Scroll Reverser; macOS casks. Not portable shell dependencies or Linux recovery requirements. |
| AI assistants and coding clients | OpenCode, Claude Code, and Copilot CLI/desktop clients are optional independent tools. Retain their existing Homebrew/cask or upstream owner; do not install competing copies. Authentication/subscriptions and their configurations are separate. |
| IDEs | JetBrains/IdeaVim are optional; see [editors](editors.md). Autosuggestions, fzf, and highlighting are core shell selections, not IDE dependencies. |

Prefer one owner per executable. Use Homebrew formulae/casks for suitable macOS
optional tools, APT/native application channels where Linux integration matters,
and a documented specialist owner for runtimes or Python apps. Not every macOS
cask has a Linux counterpart. This list authorizes no removal, broad upgrade, or
automatic restoration of optional applications.
