# Optional development toolchains

Core recovery and the local shell layer work independently of runtimes. Neither
`./setup-core`, `./install`, nor shell startup invokes `./setup-toolchains` or
installs runtimes. No scheduler, blanket trust, profile/context framework, global
Gradle, Python runtime, or Python application is added by this workflow.

## Explicit opt-in

Use the ordinary account and the [core bootstrap prerequisites](core-tools.md#bootstrap-prerequisites)
on macOS or Ubuntu/Debian desktop/WSL Linux, including Homebrew on PATH and working
HTTPS. Homebrew's platform support/bottle limits still apply. Native Windows and
Arch/Manjaro are not targets. Setup needs no sudo of its own.

Before setup, inspect `type -a mise uv uvx node java` and existing mise global/home
configuration, if any (normally `${XDG_CONFIG_HOME:-$HOME/.config}/mise/config.toml`
and any home `mise.toml`/`.tool-versions`). Setup uses your personal configuration,
not an isolated manager home; existing hooks, backend overrides, and settings
remain yours to review. Do not run it from an unreviewed checkout.

```sh
brew update                  # explicit package-definition refresh, not upgrades
./setup-toolchains           # deliberately install/select optional tools
./install                    # apply shared shell links if not already applied
# Open a new terminal (do not repeatedly source .zshrc).
mise ls --current
node --version
java -version
javac -version
uv --version
```

Setup installs only missing Homebrew `mise` and `uv` formulae, marks both as
explicitly requested (including if previously dependencies), and retains installed
manager versions. Homebrew auto-refresh, cleanup, and installed-dependent checks
are disabled just as in core setup. Required dependencies may still be installed
or upgraded; this is not a lock or transaction. Visible partial progress is kept
on failure; fix the cause and rerun. There is no `--check`/dry-run mode for this
action: `--help` is informational; invoking setup is an installation/selection request.

Visible competing `mise`, `uv`, or `uvx` executables cause failure before package
installation, rather than silent takeover. Inspect `type -a` and the original
owner (standalone installer, pipx, Cargo, etc.). Resolve PATH/ownership deliberately;
setup does not uninstall, force-link, or migrate them. Copies hidden later on PATH
are not exhaustively audited. One manager should own each command.

| Component | Selected source / update owner on both platforms |
| --- | --- |
| mise | Supported [Homebrew formula](https://mise.jdx.dev/installing-mise.html); `brew upgrade mise`, not `mise self-update` |
| uv / uvx | Supported [Homebrew formula](https://docs.astral.sh/uv/getting-started/installation/#homebrew); `brew upgrade uv`, not `uv self update` |
| Node / npm | mise's built-in Node backend; upstream Node distributions |
| Java / javac | mise's built-in Java backend; Eclipse Temurin GA JDK distributions (not JRE-only) |
| Future Python runtimes/projects/CLI apps | uv, deliberately invoked; not provisioned by setup |
| Existing pipx apps | pipx retains ownership, environments, and updates |

## Personal defaults versus project requirements

Setup runs `mise use --global --pin node@latest java@temurin` from `$HOME`, not
the caller's project directory. It refreshes remote version lists and excludes
prereleases for this selection. `latest` means newest stable Node, **not** LTS;
`temurin` means newest stable/GA Temurin JDK of any major, **not** an LTS-only
policy. Downloads depend on upstream availability for the host architecture.
The resolved exact versions are written to your personal mise config. Existing
unrelated entries are retained. No project declarations or lockfiles are edited.

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
updating them is a separate project decision. Legacy `.nvmrc`, `.node-version`,
`.java-version`, or `.sdkmanrc` files are not automatically enabled by this setup.
Review their requirements and either declare them intentionally in project mise
config or opt into mise's documented idiomatic version-file support. Do not
assume a legacy file silently overrides the personal default.

## Shell transition and absent-manager fallback

Shared interactive Zsh activates mise only when its executable is on PATH,
after Oh My Zsh and before local `interactive.zsh`. It exports
`MISE_AUTO_INSTALL=false` so prompts, directory changes, and command-not-found
handling cannot provision missing runtimes. Setup also records `auto_install =
false` globally for noninteractive use, disables shim fallback to unrelated
system runtimes, and disables automatic pruning on later mise upgrades.
Use `mise install` explicitly for missing project versions. Do not add lazy
first-use declarations if you want installation to stay explicit.

With no mise, shared startup skips activation quietly; system/user commands and
both optional local files still work. It does **not** reactivate NVM or SDKMAN as
a fallback. Their old directories, installed versions, candidates, and caches
are preserved, but shared startup no longer sources `nvm.sh`, NVM completion,
or `sdkman-init.sh`. A global SDKMAN Gradle may therefore cease to be on PATH;
use the project wrapper instead. Nothing deletes or migrates its files.

Before switching, inspect local `env.zsh`/`interactive.zsh` and other launcher
configuration for NVM/SDKMAN initialization or fixed Node/Java PATH and
`JAVA_HOME` exports. Retire competing selector lines deliberately, preserving
unrelated/private settings. Local interactive overrides run last and can defeat
mise if they reactivate a legacy manager. Start a **fresh terminal from a clean
launcher environment**: replacing an already activated shell can inherit old
PATH/variables/functions. Inspect `type -a node java`, `mise which node`,
`mise which java`, and `print -r -- "$JAVA_HOME"`; compare inside/outside a
reviewed project. Existing shells keep their previous environment until replaced.
Do not delete old runtimes merely to tidy up this transition.

## Scripts, IDEs, and Gradle

Noninteractive Zsh does not activate mise. Put Homebrew's bin directory on PATH
in the launching environment or minimal local `env.zsh` as described in the core
docs. From a reviewed project, prefer explicit execution, with installed tools:

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

## Future Python tooling and updates

Prefer uv for new work: `uv python install 3.13` for an explicitly chosen Python,
`uv init`/`uv add`/`uv run` for projects, and `uv tool install <new-app>` or
`uvx <new-app>` for CLI tools. These are examples of deliberate separate actions,
not setup steps; uv run/uvx can download runtimes/dependencies and execute code.
Review project/package sources first. Do not use mise to install Python/uv or
duplicate a Python CLI already owned elsewhere.

Before installing a CLI, inspect `pipx list`, `uv tool list`, and `type -a
<command>`. Keep existing pipx apps with pipx (including their existing executable
links in `~/.local/bin`); no `uv tool install --force`, alias takeover, or automatic
reinstallation. An eventual migration needs a separately intentional uninstall
and reinstall, with its settings/data considered. Core bootstrap Python remains
OS/Homebrew-owned; uv does not replace the distribution's Python.

- Refresh formula definitions: `brew update`. Upgrade selected **managers**:
  `brew upgrade mise uv`. Neither inherently upgrades installed Node/JDKs,
  uv-managed Python, project dependencies, or pipx/uv applications.
- Reselect newest-stable **personal runtimes**: rerun `./setup-toolchains`.
  This changes personal pins, not project requirements, and retains old runtimes.
- For a reviewed project, `mise install` installs its declared versions;
  `mise outdated` inspects newer matches. `mise upgrade node java` deliberately
  upgrades matching runtime requests in the current scope, not necessarily to
  a new major. Review `mise upgrade --help` before using `--bump` (declaration
  changes). Automatic pruning is disabled by setup; no cleanup is required.
- uv Python updates, `uv tool upgrade <app>`, project `uv lock --upgrade`/sync,
  and pipx-owned app upgrades are distinct deliberate operations, not manager
  updates. No scheduled/background upgrades are configured by this workflow.

The separate [maintenance workflow](maintenance.md) provides `./update-tools
refresh|upgrade`: all installed Homebrew formulae (including managers), uv tool
environments, and pipx apps, not only the core inventory. It does not reselect
mise runtimes, upgrade uv-managed Python, rewrite project declarations, or revive
NVM/SDKMAN. Use the explicit runtime actions above when intended.

## Verification boundaries

Use `bash -n setup-toolchains`, `zsh -n zshrc`, setup's version checks, and
fresh interactive sessions. Verify personal selections outside projects, reviewed
project overrides, noninteractive `mise exec` and `JAVA_HOME`, absent-manager
startup, and unchanged legacy directories/pipx inventory. Use disposable homes
or projects for fallback/missing-version probes; no persistent tests are kept.
Current implementation results are recorded in #12; real Ubuntu/WSL integration
is handed off to #15, not implied by macOS or mocked checks. A working existing
Mac is not clean-machine provisioning or a Linux pass.
