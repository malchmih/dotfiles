# Personal dotfiles

Shared personal configuration and core recovery are declared natively with mise,
alongside optional personal toolchains and upstream Daily maintenance. Recovery
means becoming productive again, not cloning an entire workstation or exact
versions.
Machine-specific and private settings stay outside this checkout.

Targets: Apple Silicon macOS and Ubuntu/Debian desktop or WSL Linux on x86_64 or
ARM64. Intel Macs, native Windows, and Arch/Manjaro are not supported recovery
targets; package-manager support limits also apply.

## Quick start

First follow the [bootstrap prerequisites](docs/recovery.md#bootstrap-prerequisites)
and install standalone mise as described in the
[mise prerequisite](docs/toolchains.md#standalone-mise-prerequisite). Review the
checkout's `mise.toml` and the system/global mise configuration before trusting
the checkout. Then, as your ordinary account:

```sh
git clone https://github.com/malchmih/dotfiles.git
cd dotfiles
mise trust
mise config ls
mise bootstrap --only packages,repos,dotfiles --dry-run
mise bootstrap --only packages,repos,dotfiles
mise bootstrap status
mise dot status --verbose
```

Start a fresh terminal and use the native status commands to inspect declared
state. Try `zsh -l` if your terminal does not already start Zsh; changing the
account shell is a [separate, deliberate action](docs/recovery.md#choose-the-account-shell).

- **Recovery is phase-selected.** The documented mise command applies native core
  packages, the Oh My Zsh checkout, and shared links. It excludes optional tools,
  tasks, automatic shell activation, and account-shell changes. `--only` selects
  phases; it does not isolate this checkout from merged system/global config or
  hooks.
- **Review before trusting.** mise combines repository configuration with your
  normal global/system configuration; trust is not an isolation boundary. Check
  loaded files and applicable hooks before applying.
- **Conflicting regular files and directories are preserved.** Native apply
  reports conflicts; do not use `--force`. Write failures are not transactional.
- **Preview before applying.** The selected native bootstrap phases preview
  package, repository, and dotfile changes without installing or applying them.
- **Native package provisioning still needs Homebrew's CLI for existing workflows.**
  mise's built-in Homebrew backend does not invoke `brew`; keep the CLI on PATH
  for shell integrations, Topgrade's Homebrew step, and targeted package work.
  See [recovery](docs/recovery.md).
- **Startup does not install anything.** Missing optional integrations are
  skipped; shared configuration works without local files or Oh My Zsh.
- **Daily maintenance uses upstream Topgrade.** Core Recovery declares the
  `topgrade` package; invoke it directly with broad upstream detection and normal
  prompts. Its detected scope can include runtime and injected pipx-package
  updates and eligible integrations such as an Oh My Zsh update step. On
  supported Linux, the system step can add or remove packages;
  accepting the macOS update prompt can install every update Apple offers.
  Topgrade's explicit Cleanup stays off by default. Use manager-native commands
  for targeted work or occasional Cleanup; see [maintenance](docs/maintenance.md).
  `mise dot apply` deploys configuration only; it does not install or run Topgrade.

See [recovery and configuration deployment](docs/recovery.md) for trust/review,
preview, apply, status, repeat-run behavior, conflicts, and diagnostics.

## Repository checks

Run the explicitly invoked local check task from the checkout with
`mise run check`. It validates shared Zsh startup syntax and runs the isolated
shell regression tests. The repository-local development tools are optional
and are not part of Core recovery; see the
[check workflow](docs/maintenance.md#repository-checks) for prerequisites and
deliberate install/upgrade commands.

## Guides

| I want to… | Guide |
| --- | --- |
| Recover the core environment or apply shared configuration | [Recovery](docs/recovery.md) |
| Understand core package sources and choose optional applications | [Tools and ownership](docs/core-tools.md) |
| Use shell bindings, suggestions, fzf, highlighting, and history | [Interactive shell](docs/interactive-shell.md) |
| Add private settings or understand startup and PATH precedence | [Local configuration](docs/local-configuration.md) |
| Use fallback Vim or the independent IdeaVim preference | [Editors](docs/editors.md) |
| Restore global OpenCode instructions and terminal preferences | [OpenCode preferences](docs/opencode.md) |
| Opt into mise/uv, Node/Java/Python, and project runtime workflows | [Development toolchains](docs/toolchains.md) |
| Run Daily maintenance, targeted updates, or occasional Cleanup | [Maintenance](docs/maintenance.md) |

The [glossary](GLOSSARY.md) defines the repository's scope and terminology.
This repository retains the public-domain [license](LICENSE.md).
