# Optional development toolchains

[Documentation index](../README.md#guides)

Core recovery applies only the explicitly selected packages, repositories, and
dotfiles phases. It excludes the repository-local ShellCheck/Python tools and
`check` task, as well as the tools and bootstrap-task phases. Neither that
recovery command, direct `mise dot apply`, nor shell startup invokes
`./setup-toolchains` or installs the optional Node, Java, and CPython defaults.
The separate [`mise run check` workflow](maintenance.md#repository-checks) is
also explicit and is not runtime setup. Shell activation does not install or
upgrade tools merely because a directory is entered. No scheduler, blanket trust,
profile/context framework, global Gradle, or Python CLI application is added by
this workflow.

## Explicit opt-in

Use the ordinary account and the [core bootstrap prerequisites](recovery.md#bootstrap-prerequisites)
on supported macOS or Ubuntu/Debian desktop/WSL Linux, including Homebrew on PATH
and working HTTPS. This workflow supports Apple Silicon macOS and x86_64/ARM64
Ubuntu/Debian desktop or WSL Linux. Homebrew's platform support/bottle limits
still apply to `uv`. Native Windows and Arch/Manjaro are not targets. Setup needs
no sudo of its own.

## Standalone mise prerequisite

Install mise explicitly with the [official standalone installer](https://mise.jdx.dev/installing-mise.html#mise-run)
before applying shared configuration or opting into runtime setup:

```sh
curl -fsSL https://mise.run | sh
```

Leave `MISE_VERSION` unset: the official installer selects its current stable
release (with its release-age delay) and installs the executable at
`$HOME/.local/bin/mise`. Optional setup requires this default path and verifies
that regular executable (not a symlink) is the `mise` selected first on `PATH`;
do not override the install path for this workflow. This is an explicit install,
not an update policy; do not pin a mise executable in this repository, add a
downloader wrapper, or use Homebrew to install a second mise. The ordinary
installer endpoint above does not append shell activation. Do not use
`https://mise.run/zsh`: shared Zsh configuration already conditionally activates
mise, and the shell-specific installer can append another activation block.

Shared `.zshenv` prepends `$HOME/.local/bin` on new Zsh sessions. After applying
the shared links with mise, open a fresh shell; in the current shell, add that
directory to `PATH` if needed. Confirm `type -a mise` shows the intended standalone
executable first and check it with `mise --version`. Shell startup never
installs or updates mise.

## Transition from Homebrew-owned mise

If Homebrew currently owns mise, review the transition before removing that
formula:

1. Inspect installed dependents with `brew uses --installed mise`.
2. Install the standalone binary using the command above. Keep existing mise
   configuration, data, caches, state, plugins, and installed runtimes: by
   default these are separate from the executable (`${XDG_CONFIG_HOME:-$HOME/.config}/mise`,
   `~/.local/share/mise`, `~/.cache/mise` on Linux or `~/Library/Caches/mise` on
   macOS, and `~/.local/state/mise`; see [mise directories](https://mise.jdx.dev/directories.html).
   Custom `MISE_*_DIR`/`XDG_*` settings may move them. Do not run `mise implode`,
   reset mise, or delete those directories.
3. Before removing the formula, verify `"$HOME/.local/bin/mise" --version` and
   check `type -a mise`; fix PATH so the standalone binary is selected first.
4. Run `brew uninstall mise` without force or any bypass of Homebrew's dependency
   checks. If Homebrew refuses because installed formulae depend on mise, stop:
   that dependency is an unresolved ownership conflict. Review or deliberately
   replace those dependents, or leave the formula installed until that decision
   is made; do not silently force its removal.
5. Open a fresh shell and verify `command -v mise`, `type -a mise`, and
   `mise --version`. The selected command should resolve to the standalone
   executable (normally `$HOME/.local/bin/mise`). Check existing selections
   with `mise ls --current` and confirm your prior configuration is still present.

The executable transition does not require reinitializing mise or reinstalling
Node, Java, or Python. Finish any blocked Homebrew dependency migration separately
and deliberately.

Before setup, inspect `type -a mise uv uvx node java python python3` and existing
mise global/home configuration, if any (normally
`${XDG_CONFIG_HOME:-$HOME/.config}/mise/config.toml` and any home
`mise.toml`/`.tool-versions`). Setup uses your personal configuration, not an
isolated manager home; existing hooks, backend overrides, and settings remain
yours to review. Setup requires `$HOME/.local/bin/mise` to be executable and
selected first on `PATH`; it fails rather than falling back to a Homebrew copy.
Do not run setup from an unreviewed checkout.

```sh
brew update                  # explicit package-definition refresh, not upgrades
./setup-toolchains           # deliberately install/select optional tools
# From the reviewed dotfiles checkout; review mise.toml before trusting it.
mise trust
mise dot apply --dry-run
mise dot apply               # apply shared shell links if not already applied
# Open a new terminal (do not repeatedly source .zshrc).
mise ls --current
node --version
java -version
javac -version
python --version
uv --version
```

Setup requires the official standalone executable at `$HOME/.local/bin/mise` and
verifies that it wins PATH resolution; it never installs or marks mise with
Homebrew. It installs only missing Homebrew `uv`, marks `uv` as
explicitly requested (including if previously a dependency), and retains its
installed version. Homebrew auto-refresh, cleanup, and installed-dependent checks
are disabled for this `uv` install. Required dependencies may still be installed
or upgraded; this is not a lock or transaction. Visible partial progress is kept
on failure; fix the cause and rerun. There is no `--check`/dry-run mode for this
action: `--help` is informational; invoking setup is an installation/selection request.

Setup invokes the first `mise` found on `PATH`; inspect `type -a mise` and resolve
competing copies deliberately before running it. Visible competing `uv` or `uvx`
executables cause failure before Homebrew package installation, rather than
silent takeover. Setup does not uninstall, force-link, or migrate any existing
manager. Copies hidden later on `PATH` are not exhaustively audited. One manager
should own each command.

| Component | Selected source / update owner on both platforms |
| --- | --- |
| mise | [Official standalone installer](https://mise.jdx.dev/installing-mise.html#mise-run); Topgrade may update detected mise/runtime installations under upstream defaults—see [maintenance](maintenance.md#daily-maintenance) |
| uv / uvx | Supported [Homebrew formula](https://docs.astral.sh/uv/getting-started/installation/#homebrew); `brew upgrade uv`, not `uv self update` |
| Node / npm | mise's built-in Node backend; newest stable upstream Node release |
| Java / javac | mise's built-in Java backend; `java@latest` follows mise's default vendor (Temurin as of this writing) and default GA release type |
| Personal Python / `python`, `python3` | mise's built-in Python backend (CPython); selected as a floating personal default |
| Project environments, dependencies, and CLI apps | Homebrew-owned uv; compatible Python on PATH (including mise's selection) may be used, and uv's normal managed-Python fallback remains enabled |
| Existing pipx apps | pipx retains ownership, environments, and updates |

## Personal defaults versus project requirements

Setup runs `mise use --global --fuzzy node@latest java@latest python@latest`
from `$HOME`, not the caller's project directory. `--fuzzy` keeps each request
as `latest` even when the `pin` setting or `MISE_PIN=1` would otherwise write an
exact resolved version. Setup refreshes remote version lists and excludes
prereleases for this selection. `latest` means newest stable Node, **not** LTS;
Java follows mise's default shorthand vendor (Temurin as of this writing) and
default GA release type, **not** an LTS-only policy. Python is the built-in
CPython backend's newest stable release. Downloads depend on upstream
availability for the host architecture. The floating requests are written to
your personal mise config; existing unrelated settings and tool entries are
retained. No project declarations or lockfiles are edited.

Before selecting runtimes, setup removes only the three global settings that an
older version of this helper wrote as `false`: `auto_install`,
`not_found_system_fallback`, and `upgrade.auto_prune`. Unsetting them restores
mise's defaults (currently `true` for all three) instead of merely stopping new
false values from being written. Every other global setting is left alone.
Setup can be rerun to deliberately refresh the personal selections. It does not
uninstall existing mise, uv-managed, Homebrew-owned, or OS Python installations,
or rebuild existing environments.

**Rerunning setup intentionally reselects newest-stable personal defaults.** Old
runtime installations are not removed. A newest JDK may be too new to run an old
project's Gradle; select that project's supported JDK instead.

Project `mise.toml` or `.tool-versions` overrides personal defaults. Review a
project's runtime config, included files, hooks, tasks, environment/templates,
plugins, build scripts, and wrapper before trusting or executing it. Commands
such as `mise install`, `mise exec`, `mise run`, and `mise use` may trust config
and/or execute code; review **before** running them, not just before `mise trust`.
No wildcard trusted paths or auto-confirm-all setting is introduced here.

For a reviewed project that already declares tools:

```sh
cd /path/to/reviewed-project
mise config ls
mise install                 # explicit installation of declared versions
mise exec -- node --version
mise exec -- java -version
```

To intentionally add/change a declaration in a project you own, for example:

```sh
mise use --pin node@24 java@temurin-21
# Review and commit the resulting project declaration with the project.
```

The example is a project compatibility choice, not the personal freshness policy.
A broad request like `node@24`, `node@latest`, or `java@temurin` is a resolution
rule, not a background upgrade job. Pins/lockfiles improve reproducibility;
updating them is a separate project decision.

## Shell activation and missing-tool behavior

Shared interactive Zsh activates mise only when its executable is on PATH,
after Oh My Zsh and before local `interactive.zsh`; it does not override mise's
normal auto-install policy. The legacy shared `MISE_AUTO_INSTALL=false` export is
removed. With mise's default `auto_install = true`, a missing configured tool can
be installed by `mise exec`, `mise run`/a task that needs it, or enabled
shim/command-not-found handling. This is separate from selecting or upgrading an
already-installed runtime. Entering a directory updates the selected environment;
it does not by itself install or upgrade tools. This repository adds no install
hooks or lazy tool declarations.

Mise's default `not_found_system_fallback = true` lets a shim run a same-named
system executable if it cannot resolve the configured tool. Its default
`upgrade.auto_prune = true` schedules replaced mise-managed versions for removal
after the normal grace period, while versions still in use are retained. Auto-
install is not an update policy: no background runtime updates or update service
is enabled. If setup ran in a shell that inherited the old export, start a fresh
shell after applying the shared configuration.

To inspect effective defaults from outside this checkout, use:

```sh
cd "$HOME"
mise settings get auto_install
mise settings get not_found_system_fallback
mise settings get upgrade.auto_prune
```

Use `mise install` explicitly when you want to install a project's declared
versions ahead of use. For non-installing verification of an already completed
setup, command-scoped `MISE_AUTO_INSTALL=false mise exec -- ...` is appropriate;
it does not reintroduce a persistent shell override.

With no mise, shared startup skips activation quietly; system/user commands and
both optional local files still work.

Local interactive overrides run last and can override mise's PATH or `JAVA_HOME`.
Start a **fresh terminal** after changing shell configuration. Inspect
`type -a node java python python3`, `mise which node`, `mise which java`,
`mise which python`, and `print -r -- "$JAVA_HOME"`; compare inside/outside a
reviewed project. Existing shells keep their previous environment until replaced.

## Scripts, IDEs, and Gradle

Noninteractive Zsh does not activate mise, but `.zshenv` still puts the default
standalone executable directory (`$HOME/.local/bin`) on `PATH`. Put Homebrew's
bin directory on PATH too when a noninteractive shell needs `uv`, as described
in [PATH setup](local-configuration.md#path-precedence-and-homebrew).
From a reviewed project, prefer explicit execution, with installed tools:

```sh
mise exec -- node script.js
mise exec -- ./gradlew --version
mise exec -- ./gradlew build
```

Use the project's committed **Gradle Wrapper**, not a presumed global `gradle`.
Review wrapper scripts/JAR and distribution URL/checksum before execution; first
use can download the project's Gradle distribution. The wrapper selects Gradle,
**not a suitable JDK**: mise supplies Java/`JAVA_HOME`, and the project's Gradle
compatibility and Java toolchain declarations still govern the required JDK(s).
No project's wrapper or toolchain declarations are rewritten here. A standalone
Gradle install is optional for an explicit need such as authoring a new wrapper.

An IDE can use `mise exec -- <IDE-command>` from the reviewed project or be
configured explicitly with the JDK home printed by `mise where java` and the
Node binary printed by `mise which node`. Restart/reconfigure when those paths
change. For PATH-only tools, mise's [shims](https://mise.jdx.dev/dev-tools/shims.html)
are an alternative explicit launcher configuration (`mise activate zsh --shims`);
this repository does not add them to every Zsh. Shims set environment for their
child processes, **not** `JAVA_HOME` in the parent IDE. Configure the IDE JDK
directly or launch through `mise exec`. Terminal activation does not configure
all GUI launchers, services, schedulers, or other shells globally.

## Python, uv, and updates

The optional setup selects mise's floating personal CPython default; it does not
replace OS/bootstrap Python, existing Homebrew Python, uv-managed Python, or any
project environment. Homebrew continues to own the `uv` executable. Use uv for
project environments and dependencies (`uv init`, `uv add`, `uv run`), and for
CLI apps (`uv tool install <new-app>` or `uvx <new-app>`). When a mise-selected
Python is on PATH and satisfies a project's requirements, uv can discover and use
it; pass `--python "$(command -v python)"` when a project should explicitly use
that interpreter. Otherwise uv applies its normal interpreter preference and
project requirements. Its automatic managed-Python download fallback remains
available for a project-specific interpreter; do not add a global download
prohibition or set `python-downloads = "manual"` as part of this workflow. uv
commands may download runtimes/dependencies and execute code, so review project
and package sources first.

Keep existing Python CLI ownership: before installing a CLI, inspect `pipx list`,
`uv tool list`, and `type -a <command>`. Keep existing pipx apps with pipx
(including their existing executable links in `~/.local/bin`); no `uv tool
install --force`, alias takeover, or automatic reinstallation. An eventual
migration needs a separately intentional uninstall and reinstall, with its
settings/data considered. Core/bootstrap Python remains OS/Homebrew-owned; uv
does not replace the distribution's Python.

- Refresh Homebrew formula definitions with `brew update`; use `brew upgrade uv`
  for Homebrew-owned uv or `mise self-update` for standalone mise when targeting
  one manager. Topgrade's broad upstream detection may also update managers and
  runtimes; see [Daily maintenance](maintenance.md#daily-maintenance). Updating a
  manager is distinct from selecting new Node/Java/Python runtimes, upgrading
  uv-managed Python, project dependencies, or pipx/uv applications.
- Reselect newest-stable **personal runtimes**: rerun `./setup-toolchains`.
  This refreshes floating global requests, not project requirements, and retains
  old installations and environments. To upgrade the current global Node, Java,
  and Python selections without changing project requests, use the separate
  explicit action `mise upgrade --global node java python` after reviewing the
  global/system configuration it will apply to.
- For a reviewed project, `mise install` installs its declared versions;
  `mise outdated` inspects newer matches. `mise upgrade node java python`
  deliberately upgrades matching runtime requests in the current scope, not
  necessarily to a new major. Review `mise upgrade --help` before using `--bump`
  (declaration changes). Default automatic pruning applies to replaced
  mise-managed versions after their grace period.
- uv Python updates, `uv tool upgrade <app>`, project `uv lock --upgrade`/sync,
  and pipx-owned app upgrades are distinct deliberate operations, not manager
  updates. No scheduled/background upgrades are configured by this workflow.

For broad Daily maintenance, run [`topgrade`](maintenance.md#daily-maintenance).
It uses upstream detected steps, which can include installed package managers,
runtimes, and their managed tools. Use the manager-native commands above when you
intend a targeted update.
