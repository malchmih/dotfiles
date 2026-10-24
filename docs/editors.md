# Vim and IdeaVim

[Documentation index](../README.md#guides)

## Terminal Vim

Terminal Vim is the lightweight fallback editor in the core environment, for
ordinary text and quick edits rather than a full development-editor setup.
[Core setup](recovery.md) installs Vim; `./install` links `vimrc` to `~/.vimrc`.
No Vundle, downloaded plugins, or external theme is required.

The small built-in baseline enables filetype detection and indentation, syntax
highlighting, autoindent, backspace across indentation and line boundaries,
highlighted/incremental search, a status line, and line numbers. There is no
blanket two-space indentation policy; built-in filetype rules and Vim defaults
apply. Arrow keys and normal-mode navigation keep their defaults.

In insert mode, type **`fd`** to return to normal mode. This is the only custom
mapping, shared deliberately by Vim and IdeaVim—not the interactive shell.
Start a new Vim session to load edits to `vimrc`.

### Recover an interrupted editing session

Vim's default recovery policy is unchanged: swap files are enabled and writes
use the default temporary backup behavior (`writebackup`), not persistent backup
copies (`backup` is off by default). Swap-file warnings after an interrupted
session are not configuration errors.

Use `vim -r path/to/file` to recover a buffer, inspect and save the recovered
text, and remove the stale swap file only after recovery is complete and no
other Vim session is using it. This is Vim's standard recovery, not a separate
backup system; see `:help recovery`.

## Optional IdeaVim

IdeaVim is an **optional, independent** IDE preference. Dotbot links `ideavimrc`
to `~/.ideavimrc`, whose only customization is the same `fd` mapping; it does not
source terminal Vim settings or add Cursive actions, navigation, clipboard, or
join overrides. The link is harmless without an IDE.

Install a compatible JetBrains IDE and IdeaVim separately if wanted; neither
IDE/plugin installation nor a full development-editor setup is part of core
recovery. To load changes, use `:source ~/.ideavimrc` or restart the IDE. When
moving from older configuration, restart the IDE to clear previously loaded
mappings and options.

See [toolchains](toolchains.md#scripts-ides-and-gradle) for explicit IDE runtime
configuration and [maintenance](maintenance.md#optional-nativegui-applications)
for GUI application update boundaries.
