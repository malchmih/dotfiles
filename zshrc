# Interactive setup never belongs in noninteractive shells.
[[ -o interactive ]] || return

alias j=just
alias restart-podman='podman machine stop && podman machine start'

# Keep a usable base shell even without Oh My Zsh or its plugins.
bindkey -e
export ZSH="${ZSH:-$HOME/.oh-my-zsh}"

ZSH_THEME="awesomepanda"

# OMZ owns its bundled plugins/theme, not the separately packaged additions.
zstyle ':omz:update' mode auto

plugins=()
if [[ -r "$ZSH/oh-my-zsh.sh" ]]; then
  plugins=(common-aliases git)
  (( $+commands[brew] )) && plugins+=(brew)
  (( $+commands[gradle] )) && plugins+=(gradle)
  if [[ "$OSTYPE" == linux* ]] && [[ -r /etc/os-release ]] && grep -qE '^ID="?ubuntu"?$' /etc/os-release; then
    plugins+=(ubuntu)
  fi
  # One upstream fzf integration, after OMZ's completion and base keybindings.
  # Command-only `zsh -ic` has no terminal; upstream widget setup warns there.
  (( $+commands[fzf] )) && [[ -t 0 && -t 1 ]] && plugins+=(fzf)
  typeset -a _dotfiles_plugins
  _dotfiles_plugins=()
  for plugin in "${plugins[@]}"; do
    if [[ -r "${ZSH_CUSTOM:-$ZSH/custom}/plugins/$plugin/$plugin.plugin.zsh" ||
          -r "$ZSH/plugins/$plugin/$plugin.plugin.zsh" ]]; then
      _dotfiles_plugins+=("$plugin")
    fi
  done
  plugins=("${_dotfiles_plugins[@]}")
  unset plugin _dotfiles_plugins

  source "$ZSH/oh-my-zsh.sh"
fi

# Repository maintenance commands win over plugin aliases/functions.
# The later local preference phase can still override them deliberately.
unalias up cleanup 2>/dev/null
unfunction up cleanup 2>/dev/null

# mise selects the active Node/Java runtimes.
# No missing-runtime installation from activation, prompts, or command lookup.
if (( $+commands[mise] )); then
  export MISE_AUTO_INSTALL=false
  eval "$(mise activate zsh)"
fi

# Homebrew owns these on both platforms; no plugin clones or startup installs.
_dotfiles_brew_prefix=''
if (( $+commands[brew] )); then
  _dotfiles_brew_prefix="$(brew --prefix 2>/dev/null)"
fi
if [[ -n "$_dotfiles_brew_prefix" && -r "$_dotfiles_brew_prefix/share/zsh-autosuggestions/zsh-autosuggestions.zsh" ]]; then
  source "$_dotfiles_brew_prefix/share/zsh-autosuggestions/zsh-autosuggestions.zsh"
fi

# Last preference phase: local aliases, bindings, PATH, and plugin styles win.
if [[ -r "${XDG_CONFIG_HOME:-$HOME/.config}/dotfiles/interactive.zsh" ]]; then
  source "${XDG_CONFIG_HOME:-$HOME/.config}/dotfiles/interactive.zsh"
fi

# Finalize highlighting after all widget definitions, including local ones.
if [[ -n "$_dotfiles_brew_prefix" && -r "$_dotfiles_brew_prefix/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" ]]; then
  source "$_dotfiles_brew_prefix/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh"
fi
unset _dotfiles_brew_prefix
