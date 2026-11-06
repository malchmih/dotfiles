"""Validate local mise vars, then let mise merge only the owned config keys."""

import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]


def run(*args, **kwargs):
    return subprocess.run(args, check=True, **kwargs)


def main():
    variables = json.loads(
        run("mise", "vars", "--json", cwd=ROOT, capture_output=True, text=True).stdout
    )
    pair = {}
    for name, pattern in (
        ("secondary_model", r"[A-Za-z0-9_.:-]+/[A-Za-z0-9_./:@+\-]+"),
        ("secondary_variant", r"[A-Za-z0-9_.\-]+"),
    ):
        value = variables.get(name)
        if not isinstance(value, str) or not re.fullmatch(pattern, value):
            raise ValueError(
                f"set a valid {name} in your user-local mise [vars] "
                "(secondary_model = provider/model; secondary_variant = variant)"
            )
        pair[name] = value

    config_home = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")
    if not config_home.is_absolute():
        raise ValueError("XDG_CONFIG_HOME must be an absolute path")
    opencode = config_home / "opencode"
    candidates = [opencode / "opencode.json", opencode / "opencode.jsonc"]
    existing = [path for path in candidates if path.exists() or path.is_symlink()]
    if len(existing) > 1:
        raise ValueError(
            "both opencode.json and opencode.jsonc exist; consolidate them before syncing"
        )
    targets = [
        existing[0] if existing else candidates[1],
        config_home / "implement-loop/config.toml",
    ]
    sources = [
        ROOT / "opencode/secondary-model.json.tera",
        ROOT / "implement-loop/secondary-model.toml.tera",
    ]

    # A separate manifest keeps these edits out of bootstrap and ordinary apply.
    # Literal absolute edit paths also honor non-default XDG_CONFIG_HOME values.
    temporary_root = "/tmp/opencode" if Path("/tmp/opencode").is_dir() else None
    with tempfile.TemporaryDirectory(
        prefix="secondary-model-", dir=temporary_root
    ) as directory:
        manifest = "[vars]\n" + "".join(
            f"{key} = {json.dumps(value)}\n" for key, value in pair.items()
        )
        manifest += f"opencode_new_config = {str(not existing).lower()}\n"
        manifest += "\n[dotfiles]\n"
        for target, source in zip(targets, sources):
            manifest += (
                f"{json.dumps(str(target) + '/secondary-model')} = "
                f"{{ source = {json.dumps(str(source))}, template = \"tera\", merge = true }}\n"
            )
        Path(directory, "mise.toml").write_text(manifest)
        arguments = [str(target) for target in targets]
        # Trust only our generated manifest, without persisting a trust record.
        environment = os.environ.copy()
        environment["MISE_TRUSTED_CONFIG_PATHS"] = os.pathsep.join(
            filter(None, [environment.get("MISE_TRUSTED_CONFIG_PATHS"), directory])
        )
        # Unlike apply --dry-run, diff renders and parses both merge templates.
        run("mise", "-C", directory, "dot", "diff", *arguments, env=environment)
        run("mise", "-C", directory, "dot", "apply", "--yes", *arguments, env=environment)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        if isinstance(error, subprocess.CalledProcessError) and error.stderr:
            print(error.stderr, file=sys.stderr, end="")
        print(f"sync-secondary-model: {error}", file=sys.stderr)
        sys.exit(1)
