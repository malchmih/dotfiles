# Interactive shell

[Documentation index](../README.md#guides)

The shared shell keeps Zsh, Oh My Zsh (OMZ), **awesomepanda**, and ordinary local
history. `./setup-core` explicitly installs Homebrew `fzf`,
`zsh-autosuggestions`, and `zsh-syntax-highlighting` on macOS and Linux. This
uses the existing current-release policy, including on Ubuntu/Debian: APT still
owns Zsh there, while Homebrew owns the three enhancements. No new plugin
manager, custom widgets, special font, or history service is involved.

## Try it in a fresh terminal

| Feature | Stock behavior / keys |
| --- | --- |
| Emacs editing | `Ctrl-A` / `Ctrl-E`: start/end of line; `Ctrl-U`: kill the whole line; `Ctrl-K`: kill to end; `Ctrl-W`: kill previous word; `Ctrl-Y`: yank. No shell vi mode or `fd` escape chord. |
| Inline autosuggestions | Type the start of a command already in history; a dim suffix suggests a match. At end of input, Right Arrow or `Ctrl-F` accepts it. It does not execute until Enter. Default upstream history strategy, not an AI suggestion engine. |
| fzf history | `Ctrl-R` opens the history picker with current input as query; type to narrow, Enter inserts the selected command for editing, Escape cancels. Enter at the shell prompt executes it. `Ctrl-R` inside the picker toggles relevance/order. |
| fzf files | `Ctrl-T` inserts selected file/directory paths into the command line. Tab selects multiple entries, Enter accepts, Escape cancels. Test with `ls ` then `Ctrl-T`; insertion alone does not execute. |
| fzf directories | `Alt-C` selects a directory and changes into it immediately. On terminals that intercept Alt/Option, send Escape then `c` (or configure Option as Meta). |
| fzf completion | With a supported command, e.g. `cat **` then Tab, upstream fuzzy completion chooses paths. Ordinary Tab completion remains OMZ/Zsh's. |
| Syntax highlighting | As you type, known commands, unknown commands, quoting and shell constructs get upstream colors. This is editing feedback, **not** a security check, parser guarantee, or permission to execute pasted commands. |

For a harmless start, run `print -r -- shell-learning-example`, then type its
prefix to try a suggestion and `Ctrl-R` to find it. Try the file/directory
pickers in a small known directory. Default fzf walkers omit hidden paths;
searches and previews vary by widget. OMZ may set `FZF_DEFAULT_COMMAND` using
available `rg`/`fd`, but the stock `Ctrl-T`/`Alt-C` walkers have their own defaults.
No custom previews or recursive helper scripts are configured.

Use the upstream references below for further practice. No additional prompt
framework is installed or enabled.

## Loading and local ownership

Only interactive shells load these features; `.zshenv`/`.zprofile` do not start
them. Shared `.zshrc` proceeds in this order:

1. Base aliases, Emacs editing (`bindkey -e`), awesomepanda and OMZ update policy.
2. If present, OMZ initializes completion **once**, then bundled plugins.
   `common-aliases` and `git` are shared; `brew` and `gradle` require their
   commands; `ubuntu` requires actual Ubuntu (`/etc/os-release`, including WSL
   Ubuntu, not Debian/macOS). `fzf` requires the executable on PATH and terminal
   input/output; command-only `zsh -ic` probes skip its widget integration to
   avoid upstream ZLE-option warnings without a terminal.
3. **Only OMZ's `fzf` plugin** loads fzf's upstream completion/keybindings
   (`fzf --zsh` on current releases), after OMZ's base bindings. Thus fzf owns
   normal `Ctrl-R`. No `~/.fzf.zsh`, manual `eval "$(fzf --zsh)"`, second plugin
   manager, extra `compinit`, or old `zsh-completions` checkout is needed.
4. Optional mise activation, then Homebrew's autosuggestions script.
5. [Local `interactive.zsh`](local-configuration.md): the last
   **preference** phase, so local aliases, bindings, plugin settings and styles
   override shared choices. Do not initialize fzf or another highlighter here.
6. Homebrew syntax highlighting finalizes **after** local widget definitions,
   as upstream requires. It does not choose a keymap or replace local bindings.

Homebrew script paths are `<brew --prefix>/share/zsh-autosuggestions/` and
`<brew --prefix>/share/zsh-syntax-highlighting/`, so custom prefixes and Linux's
usual `/home/linuxbrew/.linuxbrew` work too. Ensure `brew` and `fzf` are on the
startup PATH (see [PATH setup](local-configuration.md#path-precedence-and-homebrew)); one prefix
lookup locates both scripts. Don't also add these as OMZ custom plugins.

Local preferences remain yours: preserve existing files and review old local
vi-mode/plugin initialization if it conflicts. Changes to the commented example
do not rewrite an existing local file. Use a new terminal or `exec zsh -l`
after saving work, not repeated `.zshrc` sourcing into an initialized session.

## Updates and history

OMZ's upstream updater is enabled with `zstyle ':omz:update' mode auto`. On its
normal cadence (upstream default: 13 days), eligible interactive terminal
startups can update the OMZ checkout, bundled plugins and awesomepanda. `omz
update` requests this manually. **OMZ does not update separately packaged
autosuggestions, fzf, or syntax highlighting.** Deliberately run:

```sh
brew update
brew upgrade fzf zsh-autosuggestions zsh-syntax-highlighting
```

Setup only installs missing packages; it does not upgrade these on repeat runs.
No broad OS/package upgrade is needed to try the features. See the
[source/update-owner table](core-tools.md#selected-sources-and-update-owners).
For deliberate whole-inventory user-tool upgrades, see the separate
[maintenance commands](maintenance.md).

With OMZ present, its normal history settings remain untouched: default
`~/.zsh_history`, minimum `HISTSIZE=50000` / `SAVEHIST=10000`, extended timestamps,
duplicate handling, leading-space exclusion, and `SHARE_HISTORY` between local
sessions. Local overrides can change these. Suggestions and `Ctrl-R` reuse that
history; nothing syncs commands across machines. Avoid secrets on command lines;
leading-space exclusion is convenience, not a security boundary.

## Missing components / deliberate checks

Startup never installs packages and does not print a continuous missing-tool
audit. If OMZ is absent, aliases, Emacs editing, local configuration and available
Homebrew suggestions/highlighting still load; the prompt/history/completion
follow base Zsh or local settings, and **fzf's OMZ integration is absent**. If
fzf is absent its plugin is skipped; `Ctrl-R` retains OMZ/base incremental history
search. Unreadable/missing packaged scripts are skipped independently. The shell
remains useful but is not claiming all enhancements are installed.

Use `./setup-core --check` deliberately: it reports missing packages, unreadable
integration scripts, selected executable paths/versions, and incomplete OMZ.
Resolve PATH or conflicting owners before rerunning `./setup-core`; no startup
installation or automatic takeover of another manager's package is performed.
In a fresh interactive shell, inspect:

```zsh
print -r -- $ZSH_THEME $plugins
bindkey -lL main                 # should link main to emacs
bindkey '^R'                    # fzf-history-widget (wrappers may decorate it)
bindkey '^T'                    # fzf-file-widget
bindkey '^[c'                   # fzf-cd-widget
whence -w _fzf_complete _zsh_autosuggest_start _zsh_highlight
zstyle -L ':omz:update'
print -r -- $HISTFILE $HISTSIZE $SAVEHIST
[[ -o share_history ]] && print SHARE_HISTORY
```

If bindings look correct but do not work in the terminal, try the keys above in
a fresh interactive terminal and check whether the terminal intercepts them.
For history-sharing problems, compare two same-machine sessions and inspect
local overrides of the history settings above.

Upstream references: [OMZ settings](https://github.com/ohmyzsh/ohmyzsh/wiki/Settings),
[OMZ fzf plugin](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/fzf),
[fzf shell integration](https://github.com/junegunn/fzf#key-bindings-for-command-line),
[autosuggestions](https://github.com/zsh-users/zsh-autosuggestions#usage),
[highlighting load order](https://github.com/zsh-users/zsh-syntax-highlighting#faq),
and [Zsh line editor](https://zsh.sourceforge.io/Doc/Release/Zsh-Line-Editor.html).
