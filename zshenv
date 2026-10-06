path+=("$HOME/.local/bin")

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
