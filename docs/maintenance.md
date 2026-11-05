# Daily maintenance

[Documentation index](../README.md#guides)

## Daily command

Run the upstream command directly:

```sh
topgrade
```

The root `mise.toml` declares the Homebrew Core `topgrade` package for the
supported macOS and Linux targets. The selected package bootstrap phase
provisions it; shell startup and `mise dot apply` do not install or run it. This
repository adds no shared Topgrade configuration, step allowlist, custom-command
bridge, or automatic approval. Existing local Topgrade settings are left alone.

Topgrade uses broad upstream detection and normal confirmations. Depending on
what is installed, its steps can update runtime managers and runtimes, eligible
Git/shell/editor/container integrations (including an Oh My Zsh update step),
and pipx applications including injected packages. The detected steps and their
behavior can change upstream;
check [Topgrade usage](https://github.com/topgrade-rs/topgrade#usage) and the
[current configuration reference](https://github.com/topgrade-rs/topgrade/blob/main/config.example.toml)
before relying on a particular integration.

- On Linux, the system-update step can add or remove distribution packages.
- On macOS, accepting the system-update prompt can install **all** updates Apple
  offers, including a major macOS upgrade if one is offered. Review the versions
  before accepting.
- Topgrade's optional cleanup remains at its upstream off-by-default setting.
  This does not disable package-manager housekeeping that is part of an update.
- System updates can require a later restart; no reboot automation is added.
- `topgrade --dry-run` prints commands but can still run detection probes. It is
  not a guaranteed frozen summary of every change an update may make.

## Targeted updates

For a narrow package update, use that manager directly. For example:

```sh
brew update
brew upgrade <formula...>
sudo apt-get update
sudo apt-get install --only-upgrade <package...>
```

## Occasional Cleanup

Inspect the manager's proposed removals first:

```sh
brew autoremove --dry-run
brew cleanup --dry-run
apt-get --simulate autoremove
```

Then, if the proposed removals are wanted, use the native commands and their
normal prompts:

```sh
brew autoremove
brew cleanup
sudo apt-get autoremove
```

Autoremove can discard dependencies a manager considers unused; cache cleanup
removes local fallback files. Review each manager's output and retain anything
you still need. Topgrade's optional cleanup remains off by default.

## Repository checks

From the reviewed checkout, explicitly run:

```sh
mise run check
```

The task requires `zsh` and `python` on `PATH` and fails when either is missing.
It checks the shared Zsh startup syntax, then runs the isolated shell regression
tests. Python is a repository-development prerequisite, separate from optional
personal runtimes and Core Recovery; neither the task nor its tests are invoked by
startup, package provisioning, or Topgrade. If needed, install the declared
repository Python from the checkout with:

```sh
mise install python
```
