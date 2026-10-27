# Personal Development Environment

The personal working environment shared across macOS, Linux desktop, and WSL machines, with employer-specific concerns kept separate.

## Language

**Core environment**:
The personal interactive shell, everyday command-line utilities, lightweight terminal editor, and their preferences. Project toolchains, full development-editor and IDE setups, and desktop customization are separate, optional parts of the working environment.
_Avoid_: Full machine setup, complete workstation

**Recovery**:
Restoring a usable personal working environment on a replacement machine. Recovery does not imply reproducing identical software versions or all previous machine state.
_Avoid_: Exact reproduction, machine cloning

**Shared configuration**:
Personal preferences intended to be versioned together and reused across supported machines, including selected preferences for optional tools. Sharing a tool's preferences does not make the tool a core dependency; credentials and employer-specific material remain non-public.
_Avoid_: All configuration

**Local configuration**:
Optional machine-specific or non-public additions outside the shared configuration. Its preservation is not part of the baseline recovery expectation.

**Checkup**:
An evidence-based assessment of the current machine's software and setup, covering correctness, improvement opportunities, core candidates, and cleanup candidates. Its outcome is advice, not changes to the environment.

**Daily maintenance**:
A user-initiated routine for reviewing and applying available updates to installed command-line tools, managed desktop applications, and native Linux packages. It includes awareness of available macOS updates, but not their installation, project dependency changes, or runtime selection.
_Avoid_: Update everything

**Cleanup**:
A separately initiated, reviewed removal of obsolete package caches, old package versions, and dependencies considered unused by the package manager. It does not include deleting application preferences or personal data.
