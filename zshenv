# Prefer user-installed commands and avoid duplicate PATH entries.
typeset -U path

# Standard Linuxbrew is also available to noninteractive shells/agent tools.
# Custom prefixes remain a local setting; do not initialize a runtime manager here.
if [[ "$OSTYPE" == linux* && -x /home/linuxbrew/.linuxbrew/bin/brew ]]; then
  path=(/home/linuxbrew/.linuxbrew/bin /home/linuxbrew/.linuxbrew/sbin $path)
fi
# Discover an existing standalone OpenCode installation without installing it.
if [[ -d "$HOME/.opencode/bin" ]]; then
  path=("$HOME/.opencode/bin" $path)
fi
path=("$HOME/.local/bin" $path)

# Optional machine-local environment, including noninteractive shells.
if [[ -r "${XDG_CONFIG_HOME:-$HOME/.config}/dotfiles/env.zsh" ]]; then
  source "${XDG_CONFIG_HOME:-$HOME/.config}/dotfiles/env.zsh"
fi
