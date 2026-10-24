# Personal dotfiles

Shared Zsh, Vim, and IdeaVim preferences, applied with
[Dotbot](https://github.com/anishathalye/dotbot). Machine-specific and private
settings belong outside this checkout.

## Fresh setup

Install Git, Zsh, Vim, and a Python version supported by Dotbot (Python 3
recommended) using your platform's package manager, then:

```sh
git clone https://github.com/malchmih/dotfiles.git
cd dotfiles
./install --dry-run
./install
```

The bootstrap initializes the pinned Dotbot submodule itself; a recursive clone
is unnecessary. Application is best-effort: a failed link does not prevent other
links from being attempted, but Dotbot reports failure overall. Existing links
can be relinked; conflicting regular files are **not** forcibly replaced. Inspect
and move those files yourself if you want the shared links instead.

`./install --dry-run` forwards Dotbot's upstream dry-run option. It is not a
strict read-only wrapper: the bootstrap still synchronizes/initializes the Git
submodule before Dotbot runs, and arbitrary shell actions in a future config
would need their own care. No custom preflight, transaction, or rollback layer is
provided. Use `./install --help` for upstream options (including opt-in
`--exit-on-failure`); ordinary application does not enable fail-fast behavior.

Shared configuration works without local files, Oh My Zsh, SDKMAN, or NVM. Those
integrations load only when already present. Startup does not install them,
automatically update Oh My Zsh, or audit missing commands. Some convenience
aliases still require their corresponding tools/plugins (`j` needs `just`,
`restart-podman` needs Podman, and `up` needs the relevant package-manager aliases
and tools). Installation and updates are separate, explicit operations.

## Editors

Terminal Vim is the lightweight fallback editor in the core environment, for
ordinary text and quick edits rather than a full development-editor setup.
`./install` links `vimrc` to `~/.vimrc`; no Vundle, downloaded plugins, or external
theme is required. The small built-in baseline enables filetype detection and
indentation, syntax highlighting, autoindent, backspace across indentation and
line boundaries, highlighted/incremental search, a status line, and line numbers.
There is no blanket two-space indentation policy; built-in filetype rules and
Vim defaults apply. Arrow keys and normal-mode navigation keep their defaults.

In insert mode, type **`fd`** to return to normal mode. This is the only custom
mapping, shared deliberately by Vim and IdeaVim.

Vim's default recovery policy is unchanged: swap files are enabled and writes
use the default temporary backup behavior (`writebackup`), not persistent backup
copies (`backup` is off by default). Swap-file warnings after an interrupted
session are not configuration errors. Use `vim -r path/to/file` to recover a
buffer, inspect and save the recovered text, and remove the stale swap file only
after recovery is complete and no other Vim session is using it. This is Vim's
standard recovery, not a separate backup system; see `:help recovery`.

IdeaVim is an **optional, independent** IDE preference. Dotbot links `ideavimrc`
to `~/.ideavimrc`, whose only customization is the same `fd` mapping; it does not
source terminal Vim settings or add Cursive actions, navigation, clipboard, or
join overrides. The link is harmless without an IDE. Install a compatible
JetBrains IDE and IdeaVim separately if wanted; neither IDE/plugin installation
nor a full development-editor setup is part of core recovery. Start a new Vim
session to load edits to `vimrc`; for IdeaVim, use `:source ~/.ideavimrc` or restart
the IDE. When migrating an already-running IdeaVim session from the legacy
configuration, restart the IDE to clear previously loaded mappings and options.

## Optional local configuration

```sh
./scaffold-local
```

This copies harmless commented examples into
`${XDG_CONFIG_HOME:-$HOME/.config}/dotfiles/`:

- `env.zsh`: minimal environment additions for **every Zsh**, including scripts
  and `zsh -c`. Keep it quiet and fast; no interactive setup or credentials
  prompts. It runs after the shared environment defaults.
- `interactive.zsh`: interactive aliases, bindings, tool initialization, and
  overrides. It runs **last**, after shared aliases and optional integrations.

Edit those external files incrementally; do not copy the shared startup files.
For example, uncomment `export EDITOR=vi` in `env.zsh` for all new Zsh sessions,
or `alias j='just --verbose'` in `interactive.zsh` for interactive sessions only.
The examples do nothing until edited. Set/export `XDG_CONFIG_HOME` in the
launching environment **before Zsh starts** to choose a different directory;
setting it inside a local file is too late to locate that file reliably.

Repeated scaffolding only creates missing directories/files, never overwrites
existing paths (including symlinks), and reports where to edit. New directories
are owner-only and new files are owner-readable/writable; existing permissions
and contents are unchanged. It installs no packages, collects no credentials,
changes no login shell, and activates no profiles. Neither scaffolding nor local
files are needed for `./install`.

Local configuration is **not versioned or backed up here**. Arrange its secure
backup separately if needed. Employer-specific settings and credentials must
never go into the shared files or committed examples. For an existing-machine
transition, preserve private exports in local `env.zsh` before removing their
shared declarations; verify them without printing their values.

## Startup and PATH

| Session | Shared startup coverage | Local coverage |
| --- | --- | --- |
| Noninteractive `zsh -c` / Zsh scripts | `.zshenv` | `env.zsh` |
| Noninteractive login `zsh -lc` | `.zshenv`, `.zprofile` | `env.zsh` |
| Interactive `zsh -ic` | `.zshenv`, `.zshrc` | both files |
| Interactive login `zsh -lic` | all three | both files |

This follows standard Zsh startup (not `zsh -f`, which skips user startup files).
Dotbot links these files into `$HOME`; if you deliberately use `ZDOTDIR`, arrange
the corresponding startup links there yourself. Bash and other shells do not
source these files. These files do **not** configure every GUI application's
environment automatically; GUI launchers may not start Zsh at all.

The shared environment prepends `$HOME/.local/bin` and deduplicates `path`/`PATH`
while keeping the first occurrence. `.zprofile` restores that precedence after
macOS's system login setup (`path_helper`) reorders PATH. Put general additional
directories in local `env.zsh`, usually with `path+=("/some/bin")`. A prepend there
can precede `.local/bin` in non-login shells, but login setup restores
`.local/bin` first. Put final interactive precedence overrides in local
`interactive.zsh`, using `path=("/some/bin" $path)`. Avoid repeatedly concatenating
raw PATH strings. Tool managers may also adjust PATH in the interactive phase.

The installed files are live symlinks into this checkout: edits apply to **new**
sessions immediately, without rerunning Dotbot. Open a new shell or use
`exec zsh -l` to replace the current interactive shell (after saving work).
Existing processes keep their old environment; repeatedly sourcing `.zshrc`
can repeat third-party initialization and is not a full startup refresh.

## Updating Dotbot

Dotbot is pinned to **1.24.0** as a Git submodule. Ordinary `./install` uses the
committed revision, not the latest remote version. To intentionally update it,
review an upstream release, fetch it inside `dotbot`, check out the chosen tag,
then commit the changed submodule pointer in this repository. Do not add another
submodule update action to `install.conf.yaml`: both bootstrap scripts already
perform the required initialization.

This repository retains the public-domain [license](LICENSE.md).
