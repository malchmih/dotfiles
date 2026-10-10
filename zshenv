path+=("$HOME/.local/bin")

# Make Linuxbrew tools available in non-interactive zsh shells (e.g. agent tools).
typeset -U path
path=(/home/linuxbrew/.linuxbrew/bin /home/linuxbrew/.linuxbrew/sbin $path)

# Make the NVM-selected Node.js version available in non-interactive zsh shells.
if [[ ! -o interactive ]]; then
  export NVM_DIR="$HOME/.nvm"
  [[ -s "$NVM_DIR/nvm.sh" ]] && . "$NVM_DIR/nvm.sh"
fi

if [[ "$OSTYPE" == darwin* ]]; then
  alias up='bubu && mas upgrade && softwareupdate -i -a'
elif [[ "$OSTYPE" == linux* ]] && [[ -r /etc/os-release ]] && grep -qE '^ID="?ubuntu"?$' /etc/os-release; then
  alias up='bubu && aguu'
else
  alias up='echo "OS not supported"'
fi

alias j=just

alias restart-podman='podman machine stop && podman machine start'

export UV_INDEX_ZALANDO_USERNAME=mmalchevskii
