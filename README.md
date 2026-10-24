# Personal dotfiles

Shared personal configuration, applied with
[Dotbot](https://github.com/anishathalye/dotbot), plus explicit setup and
maintenance commands for a recoverable **core environment**. Recovery means
becoming productive again, not cloning an entire workstation or exact versions.
Machine-specific and private settings stay outside this checkout.

Targets: macOS and Ubuntu/Debian desktop or WSL Linux. Native Windows and
Arch/Manjaro are not current targets; package-manager support limits also apply.

## Quick start

First follow the [bootstrap prerequisites](docs/recovery.md#bootstrap-prerequisites)
for Git, Bash, Python 3, and Homebrew. Then, as your ordinary account:

```sh
git clone https://github.com/malchmih/dotfiles.git
cd dotfiles
brew update                 # refresh Homebrew and definitions, not packages
./setup-core                # install missing core tools and Oh My Zsh
./setup-core --check         # inspect ownership, command paths, and versions
./install --dry-run          # preview; bootstrap can still fetch/change submodules
./install                   # apply shared configuration links
```

Open a fresh terminal and repeat `./setup-core --check`. Try `zsh -l` if your
terminal does not already start Zsh; changing the account shell is a
[separate, deliberate action](docs/recovery.md#choose-the-account-shell).

- **Setup installs tools; `install` applies configuration.** Neither changes the
  login shell. Optional runtime setup and broad upgrades are separate actions.
- **Conflicting regular files are not overwritten.** Inspect and move them
  deliberately if you want the shared links. Application is best-effort, not a
  transaction; failures can leave some links applied.
- **Dry-run is not strictly read-only:** bootstrap initializes the pinned Dotbot
  submodule before forwarding upstream options.
- **Startup does not install anything.** Missing optional integrations are
  skipped; shared configuration works without local files or Oh My Zsh.

See [recovery and configuration deployment](docs/recovery.md) for repeat-run
behavior, conflicts, diagnostics, and Dotbot updates.

## Guides

| I want to… | Guide |
| --- | --- |
| Recover the core environment or apply shared configuration | [Recovery](docs/recovery.md) |
| Understand core package sources and choose optional applications | [Tools and ownership](docs/core-tools.md) |
| Use shell bindings, suggestions, fzf, highlighting, and history | [Interactive shell](docs/interactive-shell.md) |
| Add private settings or understand startup and PATH precedence | [Local configuration](docs/local-configuration.md) |
| Use fallback Vim or the independent IdeaVim preference | [Editors](docs/editors.md) |
| Restore global OpenCode instructions and terminal preferences | [OpenCode preferences](docs/opencode.md) |
| Opt into mise/uv, Node/Java, and project runtime workflows | [Development toolchains](docs/toolchains.md) |
| Update user tools or native packages with explicit scopes | [Maintenance](docs/maintenance.md) |

The [glossary](GLOSSARY.md) defines the repository's scope and terminology.
This repository retains the public-domain [license](LICENSE.md).
