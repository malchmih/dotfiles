# OpenCode preferences

[Documentation index](../README.md#guides)

OpenCode is an optional client, not a `setup-core` package. The native
`mise dot apply` command deploys two global preference files whether or not the
client is installed:

- `opencode/AGENTS.md`: the global interview preference for interactive questions.
- `opencode/cli.json`: terminal appearance, sessions, notifications, and diff preferences.

Destinations use `${XDG_CONFIG_HOME:-$HOME/.config}/opencode/`. mise resolves
`XDG_CONFIG_HOME` when nonempty and otherwise uses `$HOME/.config`, including
when the variable is empty. Export a custom value before running `mise dot apply`
and launch OpenCode with the same value. Native deployment creates missing parent
directories, links only these declared files, and leaves the rest of the OpenCode
directory alone. Existing regular files or directories remain conflicts; inspect
and move them aside deliberately before applying links. Do not use `--force`.

Use `mise dot status --verbose` to inspect these declared links. They are live
links into the checkout. OpenCode settings changes may write to
the shared source: review `git diff` before committing, especially if a future
client version adds settings. CLI preferences reload while the TUI is running;
they are separate from server/project configuration.

Keep `opencode.json(c)` local for provider-dependent model choices. Environment
substitution is a deferred option in [issue #16](https://github.com/malchmih/dotfiles/issues/16),
not a requirement of recovery. Custom themes, service state, credentials, provider
configuration, and all other AI-client configuration are outside this deployment.
Client installation and sign-in remain deliberate separate actions.
When `$HOME/.opencode/bin` exists, shared Zsh startup adds it to PATH after
`$HOME/.local/bin` and before package-manager commands. See
[shell startup](local-configuration.md#startup-and-path) for precedence and overrides.
