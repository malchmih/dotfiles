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

Start with Git, curl, internet access, and administrator privileges when prompted.

- **macOS:** install Apple's Command Line Tools (`xcode-select --install`) for
  bootstrap Git.
- **Ubuntu/Debian:** use the distribution's APT; see
  [Homebrew's Linux requirements](https://docs.brew.sh/Homebrew-on-Linux#requirements)
  if additional prerequisites are needed.

Install standalone mise using the
[official instructions](https://mise.jdx.dev/installing-mise.html#mise-run).
The standard installer command is:

```sh
curl -fsSL https://mise.run | sh
export PATH="$HOME/.local/bin:$PATH"
```

The export makes the newly installed mise available in this terminal before the
shared shell configuration is applied.

Clone the repository:

```sh
git clone https://github.com/malchmih/dotfiles.git
cd dotfiles
```

Trust the checkout and run Homebrew's official installer through mise:

```sh
mise trust
mise run install-homebrew
```

Follow the installer's `brew shellenv` instructions to make Homebrew available in
this terminal.

Preview and apply the Core environment:

```sh
mise bootstrap --only packages,repos,dotfiles --dry-run
mise bootstrap --only packages,repos,dotfiles
mise bootstrap status
mise dot status --verbose
```

These phases install Core packages, clone Oh My Zsh, and apply shared links. They
do not change the account's default shell. For repository maintenance, run
`mise run check`.

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
