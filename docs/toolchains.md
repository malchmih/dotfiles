# Optional development toolchains

[Documentation index](../README.md#guides)

Personal runtime installation/selection and Homebrew-owned `uv` are optional and
separate from Core recovery. Recovery, `mise dot apply`, and shell startup do not
run a repository-owned setup helper. The explicit repository check uses its own
Python development prerequisite; see
[maintenance](maintenance.md#repository-checks).

## Standalone mise prerequisite

Install mise with the
[official standalone installer](https://mise.jdx.dev/installing-mise.html#mise-run):

```sh
curl -fsSL https://mise.run | sh
```

It installs mise under `$HOME/.local/bin`; shared `.zshenv` adds that directory to
`PATH` for new Zsh sessions. Standalone mise is this repository's convention. If
another copy is already installed, inspect `type -a mise` and choose ownership
manually; do not automatically replace or migrate an existing manager.

## Homebrew-owned uv

Use Homebrew for the `uv` executable. If it is not already installed and Homebrew
is the intended owner:

```sh
brew install uv
```

Update it with `brew upgrade uv`, not `uv self update`. Before installing, inspect
`type -a uv uvx` and resolve any competing owner manually; this setup does not
remove or migrate existing installations. Use uv for project environments,
dependencies, and CLI applications. See the
[uv documentation](https://docs.astral.sh/uv/).

## Optional personal runtimes

Review your existing mise home/global configuration and inspect executable
ownership with `type -a node java python`; resolve conflicts manually. The
following optional command selects floating global requests from the user's home
scope, not an arbitrary project:

```sh
cd "$HOME"
mise use --global --fuzzy node@latest java@latest python@latest
```

`mise use` may download and install the requested runtimes; run it deliberately
and include only the runtimes you want.

Mise's Python backend selects CPython. `latest` follows the newest stable release;
these are **not LTS-only** selections, so Node or Java may advance to a non-LTS
release. The requests float rather than pinning the currently resolved versions.
Run only for the runtimes you want, and review ownership manually; this workflow
does not repair old settings, replace managers, or migrate installed runtimes.

Project `mise.toml` or `.tool-versions` declarations can override personal
defaults. Review a project's configuration before running commands that may
install tools or execute its hooks. These global selections do not edit project
declarations.

## Scripts, IDEs, and Gradle

From a reviewed project, `mise exec -- <command>` runs with that project's
declared tools. `mise install` installs declared versions; review the project
configuration first. Use the project's Gradle Wrapper instead of assuming a
global Gradle version: the wrapper selects Gradle, while the project still
determines its JDK requirements. Configure IDE runtimes explicitly or launch the
IDE through `mise exec` when appropriate; terminal activation does not configure
GUI launchers.

For project Python environments and dependencies, use Homebrew-owned uv. Existing
pipx applications remain pipx-owned unless you deliberately choose to migrate
them; no migration is performed here. See
[uv's project guide](https://docs.astral.sh/uv/guides/projects/) and the
[mise documentation](https://mise.jdx.dev/). For project environments, uv can
use a compatible Python on `PATH` or its normal managed-Python fallback.
