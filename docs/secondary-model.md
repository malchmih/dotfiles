# Sync the secondary model

In `${XDG_CONFIG_HOME:-$HOME/.config}/mise/config.local.toml`, add both values
to your local `[vars]` table:

```toml
[vars]
secondary_model = "provider/model"
secondary_variant = "variant"
```

Choose an available OpenCode provider/model and variant, then run from this
checkout:

```sh
mise run sync-secondary-model
```

Run it again after changing either value. No activated mise shell is needed.
The task uses mise's Python runtime and native templated merges; it is never
part of bootstrap, ordinary `mise dot apply`, or shell startup.

Sync sets the user-level OpenCode `general` and `explore` model selections and
Implement Loop's OpenCode model/variant. It preserves unrelated settings and
comments, including the interactive model and Copilot settings. Native project
and CLI overrides still apply. Neither application needs mise at runtime.

Targets follow `XDG_CONFIG_HOME`. Sync updates an existing `opencode.json` or
`opencode.jsonc`, creating `opencode.jsonc` if neither exists, and updates or
creates `implement-loop/config.toml`. If both OpenCode files exist, consolidate
them first. Conflicting symlinks and malformed configs are refused, not replaced.

Missing or malformed values fail before writing; model availability is checked
by OpenCode at runtime. Both config merges are previewed and validated first,
but an I/O failure during apply can leave one updated. Inspect the output and
rerun after correcting the failure. Sync does not affect an already-running loop.
