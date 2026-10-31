# Local configuration and shell startup

[Documentation index](../README.md#guides)

Shared configuration works without local files. Use the optional local layer
for machine-specific or non-public shell additions outside this checkout, not
copies of the shared configuration or named profiles.

## Create local files

From the repository checkout, run:

```sh
./scaffold-local
```

This copies harmless commented examples into
`${XDG_CONFIG_HOME:-$HOME/.config}/dotfiles/`:

- `env.zsh`: minimal environment additions for **every Zsh**, including scripts
  and `zsh -c`. Keep it quiet and fast; no interactive setup or credentials
  prompts. It runs after the shared environment defaults.
- `interactive.zsh`: interactive aliases, bindings, tool initialization, and
  overrides. It is the **last preference phase**, after shared aliases and
  integrations; syntax highlighting initializes afterward to see local widgets.

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

### PATH precedence and Homebrew

The shared environment prepends `$HOME/.local/bin`, followed by
`$HOME/.opencode/bin` if that directory exists, and deduplicates `path`/`PATH`
while keeping the first occurrence. This makes an existing standalone OpenCode
installation available in every Zsh without installing it. On Linux, it also
recognizes the standard
`/home/linuxbrew/.linuxbrew` prefix when its `bin/brew` is executable, putting
its bin/sbin after the user directories in every Zsh, including noninteractive
sessions.
`.zprofile` restores user-command precedence after
macOS's system login setup (`path_helper`) reorders PATH, with the selected
Homebrew tools next (recognizing `/opt/homebrew`, then `/usr/local`, when `brew`
exists there). Put general additional
directories in local `env.zsh`, usually with `path+=("/some/bin")`. A prepend there
can precede `.local/bin` in non-login shells, but login setup restores
`.local/bin` and the existing OpenCode directory first, in that order. Put final
interactive precedence overrides in local
`interactive.zsh`, using `path=("/some/bin" $path)`. Avoid repeatedly concatenating
raw PATH strings. Tool managers may also adjust PATH in the interactive phase.

For custom Homebrew prefixes or noninteractive macOS access, add Homebrew's
`bin` and `sbin` directories in local `env.zsh`. For example, on Apple Silicon:

```zsh
path=("$HOME/.local/bin" /opt/homebrew/bin /opt/homebrew/sbin $path)
```

Use the actual prefix on other platforms. Custom prefixes need deliberate local
PATH handling; the shared login setup only recognizes the standard prefixes.
Check `type -a brew git` in fresh shells rather than assuming setup changed its
parent shell. Before shared links are applied, use Homebrew's printed shellenv
instructions as described in [recovery prerequisites](recovery.md#bootstrap-prerequisites).

### Refresh a session

The installed files are live symlinks into this checkout: edits apply to **new**
sessions immediately, without rerunning Dotbot. Open a new shell or use
`exec zsh -l` to replace the current interactive shell (after saving work).
Existing processes keep their old environment; repeatedly sourcing `.zshrc`
can repeat third-party initialization and is not a full startup refresh.

For interactive feature loading order, see [the shell guide](interactive-shell.md#loading-and-local-ownership).
For explicit runtime access in scripts and IDEs, see [toolchains](toolchains.md#scripts-ides-and-gradle).
