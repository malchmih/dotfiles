# Restore selected Homebrew tools after macOS runs path_helper. The system
# copies remain available by absolute path; no package installation happens here.
if [[ "$OSTYPE" == darwin* ]]; then
  if [[ -x /opt/homebrew/bin/brew ]]; then
    path=(/opt/homebrew/bin /opt/homebrew/sbin $path)
  elif [[ -x /usr/local/bin/brew ]]; then
    path=(/usr/local/bin /usr/local/sbin $path)
  fi
fi

# Keep user-command precedence above package-manager commands after login setup.
typeset -U path
if [[ -d "$HOME/.opencode/bin" ]]; then
  path=("$HOME/.opencode/bin" $path)
fi
path=("$HOME/.local/bin" $path)
