# Personal dotfiles

This checkout declares shared configuration and Core environment Recovery with
native mise. Recovery aims to make you productive, not clone a workstation or
reproduce exact software versions. Machine-specific and private settings remain
outside the shared configuration.

Supported Recovery targets are Apple Silicon macOS and Ubuntu/Debian desktop or
WSL Linux on x86_64 or ARM64. Intel Macs, native Windows, and Arch/Manjaro are not
supported targets; Homebrew support and bottle availability also apply. Run WSL
commands inside the Linux distribution, preferably WSL 2. Check Homebrew's current
[installation requirements](https://docs.brew.sh/Installation) and
[support tiers](https://docs.brew.sh/Support-Tiers) for changing platform limits.

## Recover the Core environment

Use an ordinary account with Git and working HTTPS access to GitHub and package
repositories.

- **macOS:** install Apple's Command Line Tools (`xcode-select --install`) for
  bootstrap Git, then install [Homebrew](https://brew.sh/) using its current
  instructions.
- **Ubuntu/Debian:** ask an administrator to install APT and Homebrew's Linux
  prerequisites, for example `git bash ca-certificates build-essential procps curl file sudo`;
  then install [Homebrew on Linux](https://docs.brew.sh/Homebrew-on-Linux) as your
  ordinary user.
- **Both:** expose the Homebrew CLI in the current shell using the `brew shellenv`
  command printed by its installer. Standard prefixes are `/opt/homebrew` on
  Apple Silicon and `/home/linuxbrew/.linuxbrew` on Linux. Do not run ordinary
  `brew` commands with `sudo`. mise's native Homebrew backend does not invoke the
  CLI; the CLI is still needed for shell integrations, Topgrade, and targeted
  package commands.

Install standalone mise using the
[official instructions](https://mise.jdx.dev/installing-mise.html#mise-run).
The standard installer command is:

```sh
curl -fsSL https://mise.run | sh
```

This executes downloaded code as your user; review and trust the official
installer before running it. Standalone mise installs under `$HOME/.local/bin`,
which shared Zsh startup adds for new shells. If `type -a mise` finds another
copy, choose ownership manually; Recovery does not replace or migrate it.

Before trusting this checkout, review its `mise.toml`, your applicable
system/global mise configuration, and any hooks those files enable. mise merges
configuration; `mise trust` is not an isolation boundary. Then, from the checkout:

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

The selected native phases preview/apply Core packages, the Oh My Zsh checkout,
and shared links. They exclude optional repository tools/tasks and do not change
shell activation or the account's default shell. `--only` selects phases; it does
not isolate the checkout from merged configuration or hooks. `mise config ls`
shows the configuration files loaded after trust.

Package provisioning installs missing selections; it does not upgrade installed
packages. Ordinary Recovery does not reset or update an existing Oh My Zsh
checkout. A dirty checkout or one with a different origin is a conflict; inspect
it rather than replacing it. Native status reports declared resources and links,
not command resolution or shell behavior.

For links alone, use `mise dot apply --dry-run`, then `mise dot apply` and
`mise dot status --verbose`. `mise dot apply` only manages declared links; it does
not provision packages, repositories, Topgrade, runtimes, or the repository check.
Regular-file and directory conflicts are preserved and reported: inspect them
and resolve deliberately rather than using `--force`. Native apply is not a
transaction; after a write failure, inspect status before retrying.

The links point into this checkout, so keep it available. If you move the
checkout, apply the links again from its new location. Open a fresh terminal to
load the shared shell; run `zsh -l` to try it without changing your account's
default shell. Recovery does not run `chsh` or install anything at shell startup.

## Shared configuration

The root `mise.toml` is the source of truth for selected packages and deployed
files; this overview is not a full machine inventory.

- **Shell:** Zsh with Oh My Zsh, the awesomepanda theme, useful bundled plugins,
  fzf, autosuggestions, and syntax highlighting. Optional enhancements are
  guarded so the base shell remains usable when they are absent. See
  [shell and Local configuration](docs/shell.md).
- **Editors:** Vim is a lightweight terminal fallback with a small built-in
  preference set. The optional IdeaVim preference shares only its `fd`
  insert-mode mapping; no IDE or plugin is installed for it.
- **OpenCode:** the declared links provide global agent instructions and small
  CLI/TUI preferences whether or not the optional client is installed. The
  client, credentials, provider choices, and model configuration remain local.
  OpenCode may write to linked preference sources; review `git diff` before
  committing changes.

These are live links into the checkout: editing a shared source affects new
sessions. Optional **Local configuration** is not versioned here. For Daily
maintenance, invoke `topgrade`; its broad scope and native package-manager
implications are in the [maintenance and toolchain reference](docs/maintenance.md).
Repository checks are separate from Core Recovery and are described there too.

## User guides

- [Shell and Local configuration](docs/shell.md)
- [Maintenance and toolchains](docs/maintenance.md)
- [Glossary](GLOSSARY.md)

This repository retains the public-domain [license](LICENSE.md).
