# Issue #28: Current-machine mise migration

- **Completed:** 2026-11-05
- **Host:** Apple Silicon macOS (`Darwin arm64`), mise 2026.11.0

## Before

- Effective `auto_install`, `not_found_system_fallback`, and
  `upgrade.auto_prune` were all `false`, each from the global mise config.
- Global Node and Java requests were exact (`26.12.1` and
  `temurin-27.0.0+35`); there was no personal global Python request.
- The invoking process inherited `MISE_AUTO_INSTALL=false`, but no such export
  was present in shared or Local Zsh startup files, and `launchctl` had no value
  for it. Existing Python installations included Homebrew CPython 3.15.2,
  uv-managed CPython 3.13.5 and 3.11.17, and macOS Python 3.9.6. Existing uv
  tool and pipx environments were also inventoried.
- Homebrew-owned uv 0.13.7 was already explicitly requested. The root mise
  selections for ShellCheck and Python were already installed at latest.

## Migration and verification

- Reviewed `mise.toml`; all declared dotfile links, including the shared Zsh
  startup files, were already applied. No link replacement was needed.
- Ran the delivered `setup-toolchains` workflow with the inherited
  `MISE_AUTO_INSTALL` process variable removed. The global settings overrides
  were removed, and the personal global requests became floating `latest` for
  Node, Java, and Python. Node 26.13.0 and Java 27.0.1+1 (Temurin, mise's
  default vendor) were installed; CPython 3.15.2 was already installed and
  selected. Existing runtime versions were retained.
- A fresh interactive login Zsh outside the checkout reported
  `MISE_AUTO_INSTALL` unset and all three effective mise settings as `true`.
  `mise which node` returned
  `$HOME/.local/share/mise/installs/node/latest/bin/node`; `mise which java`
  returned `$HOME/.local/share/mise/installs/java/latest/bin/java`; and
  `mise which python` returned
  `$HOME/.local/share/mise/installs/python/latest/bin/python`. The selected
  versions were Node 26.13.0, Java 27.0.1, and Python 3.15.2. `JAVA_HOME`
  resolved to the mise-managed 27.0.1+1 install. `uv` resolved to
  `/opt/homebrew/bin/uv` and remained at 0.13.7.
- A fresh interactive login Zsh in the checkout resolved ShellCheck 0.11.0 and
  Python 3.15.2 from the repository's mise selections. `mise which shellcheck`
  returned `$HOME/.local/share/mise/installs/aqua-koalaman-shellcheck/latest/shellcheck-v0.11.0/shellcheck`;
  `mise which python` returned the mise-managed Python path above. Zsh remained
  outside mise and resolved to Homebrew Zsh 5.9.2 (with `/bin/zsh` also
  available).
- uv's `UV_PYTHON_DOWNLOADS` override and `python-downloads` configuration were
  absent, leaving its normal interpreter-download fallback available. Homebrew,
  uv-managed, OS, and existing mise Python/runtime installations remained
  present; uv tool and pipx inventories were unchanged.
- Before/after checks confirmed that unrelated global mise config entries,
  Local Zsh files, the repository mise config, and the Homebrew formula/version
  inventory were unchanged. No mise lockfile was added.

## Validation and limits

- `mise run check` **passed**: maintained Bash syntax, ShellCheck, Zsh syntax,
  and all 37 Python unit tests.
- The setup test `test_setup_resets_legacy_settings_and_selects_floating_global_defaults`
  passed, including its second execution against disposable fake manager state.
  The live setup was run once; the subsequent fresh-shell and preservation
  inspections were read-only.
- Live verification covered this Apple Silicon macOS machine only. Linux
  behavior was not live-tested.
