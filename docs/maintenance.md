# Maintenance and toolchains

[Recovery quickstart](../README.md#recover-the-core-environment)

## Daily maintenance

Run the upstream command directly:

```sh
topgrade
```

The root `mise.toml` declares Topgrade as a Homebrew Core package for supported
macOS and Linux. The selected package phase provisions it; shell startup and
`mise dot apply` do not install or run it. This repository adds no shared
Topgrade configuration, step allowlist, custom-command bridge, or blanket
approval. Existing Topgrade settings are left alone and may affect its
behavior.

Topgrade uses broad upstream detection and normal confirmations. Depending on
what is installed and configured, it may update package managers, runtimes,
eligible Git repositories and shell/editor/container integrations, and pipx
applications including injected packages. Detection and supported integrations
change upstream; check [Topgrade usage](https://github.com/topgrade-rs/topgrade#usage)
and its [current configuration reference](https://github.com/topgrade-rs/topgrade/blob/main/config.example.toml)
before relying on a particular step.

- On Ubuntu/Debian, the system step can use `dist-upgrade`, which may add or
  remove distribution packages.
- On macOS, accepting the system-update prompt can install **all** updates Apple
  offers, including a major macOS upgrade. Review the offered updates before
  accepting.
- Topgrade's explicit cleanup option stays at its upstream off-by-default setting.
  This does not disable native package-manager housekeeping during an update.
- Updates may require a later restart; this setup does not automate reboots.
- `topgrade --dry-run` may run detection probes and is not a frozen preview of
  every change a later update will make.

## Targeted updates

For a narrow package update, use its native manager:

```sh
brew update
brew upgrade <formula...>
sudo apt-get update
sudo apt-get install --only-upgrade <package...>
```

## Occasional Cleanup

First inspect proposed removals:

```sh
brew autoremove --dry-run
brew cleanup --dry-run
apt-get --simulate autoremove
```

On an existing machine, also review Homebrew's requested-install state
(`brew list --formula --no-installed-on-request`) or APT's automatic marks
(`apt-mark showauto`). mise declarations do not change these marks, and native
autoremove does not consult `mise.toml`; a manager can therefore consider a
declared package unused. Autoremove may remove dependencies you still need, so
review the proposed set and keep required packages marked/requested before
continuing.

If the removals are wanted, use the native commands and their normal prompts:

```sh
brew autoremove
brew cleanup
sudo apt-get autoremove
```

Homebrew cleanup removes old versions and cache files; APT autoremove removes
packages it considers automatically installed and no longer needed. Topgrade's
explicit cleanup option remains off by default, but that is not a promise of zero
native manager housekeeping during updates.

## Optional development toolchains

Personal runtime installation and Homebrew-owned `uv` are optional and separate
from Core Recovery. Standalone mise is the convention here; if another copy is
present, inspect `type -a mise` and choose ownership manually. Nothing in this
workflow replaces or migrates an existing manager or installation.

To select floating global requests from the user's home scope—not from an
arbitrary project—choose only the runtimes wanted:

```sh
cd "$HOME"
mise use --global --fuzzy node@latest java@latest python@latest
```

This may download and install runtimes. `latest` follows the newest stable
release, not necessarily an LTS release; the mise Python backend selects CPython.
Review existing global mise settings and `type -a node java python` first.
Projects can override these defaults with their own `mise.toml` or
`.tool-versions`.

Use Homebrew for [`uv`](https://docs.astral.sh/uv/), and update it there rather
than with `uv self update`:

```sh
brew install uv
brew upgrade uv
```

Before installing, inspect `type -a uv uvx` and resolve competing ownership
manually. Use `uv` for project environments, dependencies, and CLI applications;
existing pipx applications remain pipx-owned unless deliberately migrated.

Review a project's mise configuration before commands that may install its tools
or run its hooks. `mise exec -- <command>` uses project tools and `mise install`
installs declared versions. Prefer a project's Gradle Wrapper over a global
Gradle assumption. Shell runtime activation does not configure GUI IDE launchers.
See the [mise documentation](https://mise.jdx.dev/) for general usage.

## Repository checks

Checks are an explicit repository-development task, not part of Core Recovery,
shell startup, package provisioning, or Topgrade. From a reviewed checkout, run:

```sh
mise run check
```

The task requires `zsh` and `python` on `PATH` and fails if either is missing. It
checks shared Zsh startup syntax and runs the isolated shell regression tests.
The repository's Python selection is for this task only; if needed, install it
deliberately from the reviewed checkout with `mise install python`.
