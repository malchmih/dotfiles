# Restore user-command precedence after macOS runs path_helper.
typeset -U path
path=("$HOME/.local/bin" $path)
