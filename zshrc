# Interactive setup never belongs in noninteractive shells.
[[ -o interactive ]] || return

alias j=just
alias restart-podman='podman machine stop && podman machine start'

if [[ "$OSTYPE" == darwin* ]]; then
  alias up='bubu && mas upgrade && softwareupdate -i -a'
elif [[ "$OSTYPE" == linux* ]] && [[ -r /etc/os-release ]] && grep -qE '^ID="?ubuntu"?$' /etc/os-release; then
  alias up='bubu && aguu'
else
  alias up='echo "OS not supported"'
fi

# Keep a usable base shell even without Oh My Zsh or its plugins.
bindkey -v
export ZSH="${ZSH:-$HOME/.oh-my-zsh}"

ZSH_THEME="awesomepanda"

# Software installation and updates are explicit, never startup side effects.
zstyle ':omz:update' mode disabled

plugins=()
if [[ -r "$ZSH/oh-my-zsh.sh" ]]; then
  for plugin in brew common-aliases git vi-mode gradle ubuntu; do
    if [[ -r "${ZSH_CUSTOM:-$ZSH/custom}/plugins/$plugin/$plugin.plugin.zsh" ||
          -r "$ZSH/plugins/$plugin/$plugin.plugin.zsh" ]]; then
      plugins+=("$plugin")
    fi
  done
  unset plugin

  if [[ -d "${ZSH_CUSTOM:-$ZSH/custom}/plugins/zsh-completions/src" ]]; then
    fpath+=("${ZSH_CUSTOM:-$ZSH/custom}/plugins/zsh-completions/src")
  fi

  source "$ZSH/oh-my-zsh.sh"
fi

# One active Node/Java selector; legacy NVM/SDKMAN installations stay on disk.
# No missing-runtime installation from activation, prompts, or command lookup.
if (( $+commands[mise] )); then
  export MISE_AUTO_INSTALL=false
  eval "$(mise activate zsh)"
fi

# Last so local aliases, bindings, PATH, and other preferences can override shared ones.
if [[ -r "${XDG_CONFIG_HOME:-$HOME/.config}/dotfiles/interactive.zsh" ]]; then
  source "${XDG_CONFIG_HOME:-$HOME/.config}/dotfiles/interactive.zsh"
fi
