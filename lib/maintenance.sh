# shellcheck shell=bash
# Shared implementation for the explicit up/cleanup entry points (Bash 3.2+).
# No work is performed merely by sourcing this file.

maintenance_run() {
    local description=$1
    shift
    printf '\n%s\n' "$description"
    if "$@"; then
        return 0
    fi
    printf 'FAILED: %s\n' "$description" >&2
    failed=1
    return 1
}

maintenance_main() {
    set -uo pipefail
    local action=$1
    shift
    case "${1:-}" in
        --help|-h)
            [[ $# -eq 1 ]] || { printf 'Usage: %s [--help]\n' "$action" >&2; return 1; }
            if [[ $action == up ]]; then
                printf '%s\n' 'Usage: up [--help]' \
                    'Refresh, review native listings, then approve once to upgrade installed tools/apps.' \
                    'Includes Homebrew formulae/casks, uv tools, pipx apps, and Ubuntu/Debian APT packages.' \
                    'macOS updates are listed only. Normal cask app quits/restarts and built-in brew cleanup are allowed.' \
                    'Refresh may update Homebrew itself before approval. uv/pipx exact changes are unknown.'
            else
                printf '%s\n' 'Usage: cleanup [--help]' \
                    'Preview Homebrew autoremove/cleanup and Ubuntu/Debian APT autoremove, then approve once.' \
                    'No cask zap, application-preference deletion, or personal-data cleanup.'
            fi
            printf '%s\n' 'Run as your ordinary user; APT work validates sudo upfront; macOS installers may prompt as needed.' \
                'Independent failures are reported without rollback. No automatic reboot is requested.' \
                'Read docs/maintenance.md in the dotfiles checkout for scope and limitations.'
            return 0
            ;;
        '') [[ $# -eq 0 ]] || return 1 ;;
        *) printf 'Usage: %s [--help]\n' "$action" >&2; return 1 ;;
    esac
    if [[ $(id -u) == 0 ]]; then
        printf '%s: run as your ordinary user, not with sudo.\n' "$action" >&2
        return 1
    fi

    local platform failed=0 brew_ready=0 apt_ready=0 casks=0 uv_ready=0 pipx_ready=0
    local needs_sudo=0 installed_casks answer
    case "$(uname -s)" in
        Darwin) platform=macos ;;
        Linux)
            if [[ ! -r /etc/os-release ]]; then
                printf '%s: cannot identify Linux; expected Ubuntu or Debian.\n' "$action" >&2
                return 1
            fi
            local ID=''
            # shellcheck source=/dev/null
            . /etc/os-release
            case "$ID" in
                ubuntu|debian) platform=linux ;;
                *) printf '%s: only macOS and Ubuntu/Debian (including WSL) are supported.\n' "$action" >&2; return 1 ;;
            esac
            ;;
        *) printf '%s: only macOS and Ubuntu/Debian (including WSL) are supported.\n' "$action" >&2; return 1 ;;
    esac

    # Native listings must not trigger an implicit refresh or hide failures.
    export HOMEBREW_NO_AUTO_UPDATE=1
    # The daily workflow deliberately allows Homebrew's built-in cleanup.
    unset HOMEBREW_NO_INSTALL_CLEANUP
    if command -v brew >/dev/null; then
        brew_ready=1
        if [[ $action == up && $platform == macos ]]; then
            if installed_casks=$(brew list --cask); then
                if [[ -n $installed_casks ]]; then
                    casks=1
                fi
            else
                printf '%s\n' 'FAILED: Homebrew cask inventory; skipping cask upgrades.' >&2
                failed=1
            fi
        fi
    else
        printf '%s\n' 'SKIP: Homebrew not on PATH.'
    fi
    if [[ $platform == linux ]]; then
        if command -v apt-get >/dev/null; then
            apt_ready=1
            needs_sudo=1
        else
            printf '%s\n' 'FAILED: APT not on PATH on Ubuntu/Debian.' >&2
            failed=1
        fi
    fi
    if [[ $needs_sudo == 1 ]]; then
        if ! maintenance_run 'Validate sudo credentials before maintenance.' sudo -v; then
            apt_ready=0
            printf '%s\n' 'SKIP: privileged work after failed sudo validation; continuing independent work.'
        fi
    fi

    printf '\n%s\n' 'Review the following native listings. This is not a frozen transaction.'
    if [[ $action == up ]]; then
        if [[ $brew_ready == 1 ]]; then
            if ! maintenance_run 'Homebrew: refresh definitions and Homebrew itself (before approval).' brew update; then
                brew_ready=0
                printf '%s\n' 'SKIP: Homebrew upgrades after failed refresh.'
            elif ! maintenance_run 'Homebrew: available formula upgrades.' brew outdated --formula; then
                brew_ready=0
                printf '%s\n' 'SKIP: Homebrew upgrades after failed preview.'
            elif [[ $casks == 1 ]] && ! maintenance_run 'Homebrew: available cask upgrades (normal app quits/restarts allowed).' brew outdated --cask; then
                casks=0
            fi
        fi
        if [[ $apt_ready == 1 ]]; then
            # APT can return success for partially stale indexes unless error-mode is explicit.
            if ! maintenance_run 'APT: refresh indexes (before approval).' sudo apt-get -o APT::Update::Error-Mode=any update; then
                apt_ready=0
                printf '%s\n' 'SKIP: APT upgrades after failed refresh.'
            elif ! maintenance_run 'APT: simulated ordinary upgrade, without removals.' apt-get --simulate upgrade --no-remove; then
                apt_ready=0
            fi
        fi
        if command -v uv >/dev/null; then
            if maintenance_run 'uv: installed tools; exact upgrade changes UNKNOWN until execution.' uv tool list; then
                uv_ready=1
            fi
        else
            printf '%s\n' 'SKIP: optional uv not on PATH.'
        fi
        if command -v pipx >/dev/null; then
            if maintenance_run 'pipx: installed apps; exact upgrade changes UNKNOWN until execution.' pipx list; then
                pipx_ready=1
            fi
        else
            printf '%s\n' 'SKIP: optional pipx not on PATH.'
        fi
        if [[ $platform == macos ]]; then
            maintenance_run 'macOS: available updates, LIST ONLY; installation remains manual.' softwareupdate --list || :
        fi
    else
        if [[ $brew_ready == 1 ]]; then
            if ! maintenance_run 'Homebrew: unused dependencies proposed for removal.' brew autoremove --dry-run; then
                brew_ready=0
            elif ! maintenance_run 'Homebrew: old versions/caches proposed for cleanup.' brew cleanup --dry-run; then
                brew_ready=0
            fi
        fi
        if [[ $apt_ready == 1 ]]; then
            # Root preview sees the same APT configuration as the actual removal.
            if ! maintenance_run 'APT: unused dependencies proposed for removal.' sudo apt-get --simulate autoremove; then
                apt_ready=0
            fi
        fi
    fi

    if [[ $brew_ready == 0 && $apt_ready == 0 && $uv_ready == 0 && $pipx_ready == 0 ]]; then
        printf '\n%s\n' 'No eligible changes to approve.'
    else
        printf '\nApprove %s for the eligible inventories above? [Y/n] ' "$action"
        answer=''
        if ! IFS= read -r answer || [[ -n $answer && $answer != y && $answer != Y && $answer != yes && $answer != YES ]]; then
            printf '\n%s\n' 'Cancelled; no approved upgrades/removals were run. Prior refresh changes remain.'
            [[ $failed == 0 ]]
            return
        fi
        if [[ $action == up ]]; then
            if [[ $brew_ready == 1 ]]; then
                maintenance_run 'Homebrew: upgrade all eligible formulae (built-in cleanup allowed).' brew upgrade --formula --yes || :
                if [[ $casks == 1 ]]; then
                    maintenance_run 'Homebrew: upgrade all eligible casks (app disruption allowed).' brew upgrade --cask --yes || :
                fi
            fi
            [[ $uv_ready == 0 ]] || maintenance_run 'uv: upgrade all existing tool environments.' uv tool upgrade --all || :
            [[ $pipx_ready == 0 ]] || maintenance_run 'pipx: upgrade all existing apps.' pipx upgrade-all || :
            [[ $apt_ready == 0 ]] || maintenance_run 'APT: upgrade native packages without removals.' sudo apt-get upgrade --no-remove --yes || :
        else
            if [[ $brew_ready == 1 ]]; then
                maintenance_run 'Homebrew: remove unused dependencies.' brew autoremove || :
                maintenance_run 'Homebrew: clean old versions/caches.' brew cleanup || :
            fi
            [[ $apt_ready == 0 ]] || maintenance_run 'APT: remove unused dependencies.' sudo apt-get autoremove --yes || :
        fi
    fi
    if [[ $failed != 0 ]]; then
        printf '\n%s: incomplete; inspect FAILED messages before retrying. Earlier changes remain.\n' "$action" >&2
        return 1
    fi
    printf '\n%s: finished for eligible managers. No machine reboot was requested.\n' "$action"
}
