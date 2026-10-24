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
