# Prefer user-installed commands and avoid duplicate PATH entries.
typeset -U path
path=("$HOME/.local/bin" $path)

# Optional machine-local environment, including noninteractive shells.
if [[ -r "${XDG_CONFIG_HOME:-$HOME/.config}/dotfiles/env.zsh" ]]; then
  source "${XDG_CONFIG_HOME:-$HOME/.config}/dotfiles/env.zsh"
fi
