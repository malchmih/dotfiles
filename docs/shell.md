# Shell and Local configuration

[Recovery quickstart](../README.md#recover-the-core-environment)

Shared interactive Zsh uses Oh My Zsh (OMZ), the awesomepanda theme, OMZ's
selected bundled plugins, and Homebrew-packaged fzf, autosuggestions, and syntax
highlighting. These additions are optional at startup; the base shell remains
usable when they are absent.

## Use the shell

| Feature | Behavior |
| --- | --- |
| Emacs editing | `Ctrl-A` / `Ctrl-E` move to line start/end; `Ctrl-U` kills the line; `Ctrl-K` kills to the end; `Ctrl-W` kills the previous word; `Ctrl-Y` yanks. |
| Suggestions | A dim suffix suggests a command from local history. At the end of input, Right Arrow or `Ctrl-F` accepts it; Enter is still required to run it. |
| fzf history | `Ctrl-R` searches history; Enter inserts the selected command for editing, Escape cancels. |
| fzf files | `Ctrl-T` inserts paths; Tab selects multiple entries, Enter accepts, Escape cancels. |
| fzf directories and completion | `Alt-C` changes into a selected directory. With a supported command, `**` then Tab starts fuzzy path completion. Some terminals intercept Alt/Option; try Escape then `c`. |
| Syntax highlighting | Colors provide editing feedback, not a parser guarantee or security check. Review commands before executing them. |

`restart-podman` runs `podman machine stop && podman machine start` and requires
Podman. OMZ also retains its ordinary local history behavior; history is not
synced across machines. Avoid putting secrets on command lines.

## Loading and ownership

Only interactive shells load `.zshrc`; `.zshenv` and `.zprofile` do not start
interactive features. In shared `.zshrc`, the order is:

1. Base aliases and Emacs bindings, then awesomepanda and OMZ update settings.
2. If the OMZ initializer exists, OMZ loads `common-aliases` and `git`; `brew`
   and `gradle` are conditional on their commands, and `ubuntu` is conditional
   on Ubuntu. OMZ owns availability of its bundled plugin files.
3. OMZ's `fzf` plugin loads fzf's shell integration when fzf is present and the
   shell has a terminal. It owns the standard `Ctrl-R` binding; do not also
   source `~/.fzf.zsh` or run `eval "$(fzf --zsh)"`.
4. mise activation runs when mise is available, followed by Homebrew's
   autosuggestions script when readable.
5. Local `interactive.zsh` is the final preference phase for aliases, bindings,
   styles, and PATH.
6. Homebrew syntax highlighting loads last so it sees local widget definitions.

The OMZ automatic updater remains enabled. Topgrade can also update detected
shell integrations; Homebrew owns the separately packaged additions (see
[maintenance](maintenance.md#daily-maintenance)).

If OMZ is absent, base Zsh editing, aliases, and Local configuration still load.
If fzf or its terminal integration is unavailable, the OMZ fzf plugin is skipped;
`Ctrl-R` falls back to Zsh/OMZ history search. Available packaged suggestions and
highlighting can still load without OMZ; scripts are skipped when missing or
unreadable. Startup does not install, update, or continuously audit software. A
partial OMZ checkout may report its own missing bundled files.

## Startup sessions and PATH

| Session | Shared startup files | Local files |
| --- | --- | --- |
| `zsh -c` | `.zshenv` | `env.zsh` |
| `zsh -lc` | `.zshenv`, `.zprofile` | `env.zsh` |
| `zsh -ic` | `.zshenv`, `.zshrc` | both |
| `zsh -lic` | all three | both |

This is standard Zsh startup (not `zsh -f`). Bash and GUI applications do not
source these files. If you set `ZDOTDIR`, arrange the startup links there yourself.

PATH entries are deduplicated with the first occurrence kept. Every Zsh session
prefers `$HOME/.local/bin`, then an existing `$HOME/.opencode/bin`; Linux also
adds the standard Linuxbrew `bin`/`sbin` when its `brew` executable exists. On
macOS, `.zprofile` restores these user directories ahead of Homebrew after the
system login setup reorders PATH; recognized Homebrew commands then precede
Apple's system copies.

Use Local `env.zsh` to add paths for all Zsh sessions, usually with
`path+=("/some/bin")`. A prepend there can outrank `.local/bin` in non-login
shells; login setup restores `.local/bin` and the existing OpenCode directory
first. `interactive.zsh` runs after mise activation, so it can make final
interactive preference overrides, for example `path=("/some/bin" $path)`. Avoid
repeatedly concatenating raw `PATH` strings. For custom Homebrew prefixes, add
their `bin`/`sbin` paths locally; shared login setup recognizes only the standard
prefixes. Check `type -a brew git` in a fresh shell rather than assuming a parent
shell's PATH changed.

## Local configuration

Local files are optional and are not versioned here. Set `XDG_CONFIG_HOME` in the
environment **before Zsh starts** to change their directory. The defaults are
`${XDG_CONFIG_HOME:-$HOME/.config}/dotfiles/env.zsh` and
`${XDG_CONFIG_HOME:-$HOME/.config}/dotfiles/interactive.zsh`.

Create only missing files with restrictive permissions; existing files and
symlinks are kept:

```sh
local_dir="${XDG_CONFIG_HOME:-$HOME/.config}/dotfiles"
(
  set -eu
  umask 077
  mkdir -p "$local_dir"
  for name in env.zsh interactive.zsh; do
    file="$local_dir/$name"
    if [ -e "$file" ] || [ -L "$file" ]; then
      printf 'Kept existing path: %s\n' "$file"
    elif (set -C; : > "$file") 2>/dev/null; then
      printf 'Created: %s\n' "$file"
    else
      printf 'Could not safely create: %s\n' "$file" >&2
      exit 1
    fi
  done
)
```

New files use the owner-only `umask 077` (normally mode `600`; a newly created
directory is normally `700`). Existing permissions and contents are not changed.
Keep `env.zsh` quiet and fast for scripts and `zsh -c`; put interactive aliases,
bindings, and overrides in `interactive.zsh`. Do not copy shared startup files or
put credentials/employer-specific settings in the shared checkout. Arrange a
separate secure backup for Local configuration if needed.

Shared links remain live into this checkout, so edits affect new sessions without
reapplying links. Open a new terminal or use `exec zsh -l` after saving; repeatedly
sourcing `.zshrc` can repeat plugin initialization and is not a full shell refresh.

Upstream references: [OMZ settings](https://github.com/ohmyzsh/ohmyzsh/wiki/Settings),
[fzf integration](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/fzf),
[autosuggestions](https://github.com/zsh-users/zsh-autosuggestions#usage), and
[syntax-highlighting load order](https://github.com/zsh-users/zsh-syntax-highlighting#faq).
