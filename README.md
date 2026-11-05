# Personal dotfiles

Shared personal configuration, deployed natively with mise, plus explicit setup
and maintenance commands for a recoverable **core environment**. Recovery means
becoming productive again, not cloning an entire workstation or exact versions.
Machine-specific and private settings stay outside this checkout.

Targets: macOS and Ubuntu/Debian desktop or WSL Linux. Native Windows and
Arch/Manjaro are not current targets; package-manager support limits also apply.

## Quick start

First follow the [bootstrap prerequisites](docs/recovery.md#bootstrap-prerequisites)
and install standalone mise as described in the
[mise prerequisite](docs/toolchains.md#standalone-mise-prerequisite). Then, as
your ordinary account:

```sh
git clone https://github.com/malchmih/dotfiles.git
cd dotfiles
brew update                 # refresh Homebrew and definitions, not packages
./setup-core                # install missing core tools and Oh My Zsh
./setup-core --check         # inspect ownership, command paths, and versions
mise trust                  # after reviewing mise.toml
mise config ls               # inspect merged mise configuration
mise dot apply --dry-run    # preview shared configuration links
mise dot apply              # apply shared configuration links
mise dot status --verbose   # inspect declared link state
```

Open a fresh terminal and repeat `./setup-core --check`. Try `zsh -l` if your
terminal does not already start Zsh; changing the account shell is a
[separate, deliberate action](docs/recovery.md#choose-the-account-shell).

- **Setup and configuration are separate.** `./setup-core` installs core tools;
  this repository declares shared links in `mise.toml`. The direct `mise dot`
  commands do not provision packages, select runtimes, run maintenance, or
  change the login shell.
- **Review before trusting.** mise combines repository configuration with your
  normal global/system configuration; trust is not an isolation boundary. Check
  loaded files, applicable dotfiles hooks, and history reload commands too.
- **Conflicting regular files and directories are preserved.** Native apply
  reports conflicts; do not use `--force`. Write failures are not transactional.
- **Preview before applying.** `mise dot apply --dry-run` previews links without
  initializing submodules or running package setup.
- **Startup does not install anything.** Missing optional integrations are
  skipped; shared configuration works without local files or Oh My Zsh.
- **Maintenance commands work from any directory.** `mise dot apply` links
  `up`, `cleanup`, `update-tools`, and `update-system` into `~/.local/bin`, on the
  configured Zsh PATH. Use `up` for reviewed daily updates and `cleanup` for
  separately reviewed housekeeping. Setup/recovery helpers stay checkout-local;
  linking does not run updates. Keep the checkout available because the links
  point into it. See their [scopes](docs/maintenance.md) first.

See [recovery and configuration deployment](docs/recovery.md) for trust/review,
preview, apply, status, repeat-run behavior, conflicts, and diagnostics.

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
| Run daily updates, reviewed cleanup, or scoped maintenance | [Maintenance](docs/maintenance.md) |

The [glossary](GLOSSARY.md) defines the repository's scope and terminology.
This repository retains the public-domain [license](LICENSE.md).
