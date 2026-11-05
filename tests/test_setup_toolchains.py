"""Exercise optional toolchain setup with fake managers and disposable homes."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]

MISE_STUB = r'''
import json
import os
from pathlib import Path
import re
import sys

args = sys.argv[1:]
event = {
    "args": args,
    "cwd": os.getcwd(),
    "auto_install": os.getenv("MISE_AUTO_INSTALL"),
    "pin": os.getenv("MISE_PIN"),
    "prereleases": os.getenv("MISE_PRERELEASES"),
    "fetch_remote_versions_cache": os.getenv("MISE_FETCH_REMOTE_VERSIONS_CACHE"),
}
with open(os.environ["MOCK_MISE_LOG"], "a") as log:
    log.write(json.dumps(event) + "\n")

config = Path(os.environ["MOCK_MISE_CONFIG"])
text = config.read_text()

if args[:2] == ["settings", "unset"]:
    key = args[2]
    text = re.sub(rf"(?m)^{re.escape(key)}\s*=.*\n?", "", text)
    config.write_text(text)
elif args[:2] == ["settings", "set"]:
    key, value = args[2:4]
    pattern = rf"(?m)^{re.escape(key)}\s*=.*$"
    if re.search(pattern, text):
        text = re.sub(pattern, f"{key} = {value}", text)
    else:
        text = text.replace("[settings]\n", f"[settings]\n{key} = {value}\n", 1)
    config.write_text(text)
elif args and args[0] == "use":
    exact_pin = (
        "--pin" in args
        or (os.getenv("MISE_PIN") == "1" and "--fuzzy" not in args)
    )
    resolved = {"node": "24.14.0", "java": "temurin-25.0.1+8", "python": "3.14.0"}
    tools_start = text.find("[tools]")
    tools_end = text.find("\n[", tools_start + 1)
    if tools_end < 0:
        tools_end = len(text)
    tools = text[tools_start:tools_end]
    for spec in (arg for arg in args if "@" in arg and not arg.startswith("-")):
        tool, requested = spec.split("@", 1)
        if tool not in resolved:
            continue
        version = resolved[tool] if exact_pin else requested
        tools, count = re.subn(
            rf"(?m)^{re.escape(tool)}\s*=.*$",
            f'{tool} = "{version}"',
            tools,
            count=1,
        )
        if count == 0:
            tools += f'\n{tool} = "{version}"'
    config.write_text(text[:tools_start] + tools + text[tools_end:])

if args and args[0] == "exec":
    print("mock exec " + " ".join(args[args.index("--") + 1:]))
'''

BREW_STUB = r'''
import json
import os
import sys

args = sys.argv[1:]
with open(os.environ["MOCK_BREW_LOG"], "a") as log:
    log.write(json.dumps(args) + "\n")
if args == ["--prefix"]:
    print(os.environ["MOCK_BREW_PREFIX"])
'''


class SetupToolchainsTests(unittest.TestCase):
    def setUp(self):
        if os.geteuid() == 0:
            self.skipTest("setup-toolchains intentionally refuses root")
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.mise_bin = self.home / ".local/bin"
        self.mise_bin.mkdir(parents=True)
        self.brew_prefix = self.home / "homebrew"
        self.brew_bin = self.brew_prefix / "bin"
        self.brew_bin.mkdir(parents=True)

        self.config = self.home / ".config/mise/config.toml"
        self.config.parent.mkdir(parents=True)
        self.config.write_text(
            '[settings]\n'
            'auto_install = false\n'
            'not_found_system_fallback = false\n'
            'upgrade.auto_prune = false\n'
            'pin = true\n'
            'jobs = 3\n'
            '\n'
            '[tools]\n'
            'node = "22.0.0"\n'
            'java = "temurin-21.0.0"\n'
            'python = "3.12.4"\n'
            'ruby = "3.4.3"\n'
        )
        self.local_config = self.home / ".config/dotfiles/interactive.zsh"
        self.local_config.parent.mkdir(parents=True)
        self.local_config.write_text("# machine-specific preference\n")

        self.project = self.home / "projects/example"
        self.project.mkdir(parents=True)
        self.project_config = self.project / "mise.toml"
        self.project_config.write_text('[tools]\npython = "3.11.9"\n')
        self.venv = self.project / ".venv/pyvenv.cfg"
        self.venv.parent.mkdir()
        self.venv.write_text("home = /existing/python\n")
        self.uv_python = self.home / ".local/share/uv/python/cpython-3.13.5/bin/python"
        self.uv_python.parent.mkdir(parents=True)
        self.uv_python.write_text("existing uv-managed interpreter\n")

        mise = self.mise_bin / "mise"
        mise.write_text(f"#!{sys.executable}\n" + MISE_STUB)
        mise.chmod(0o755)
        brew = self.brew_bin / "brew"
        brew.write_text(f"#!{sys.executable}\n" + BREW_STUB)
        brew.chmod(0o755)
        for name in ("uv", "uvx"):
            command = self.brew_bin / name
            command.write_text("#!/bin/sh\nprintf 'mock " + name + "\\n'\n")
            command.chmod(0o755)

        self.mise_log = self.home / "mise.jsonl"
        self.brew_log = self.home / "brew.jsonl"
        self.env = {
            "HOME": str(self.home),
            "PATH": f"{self.mise_bin}:{self.brew_bin}:/usr/bin:/bin",
            "MOCK_MISE_CONFIG": str(self.config),
            "MOCK_MISE_LOG": str(self.mise_log),
            "MOCK_BREW_PREFIX": str(self.brew_prefix),
            "MOCK_BREW_LOG": str(self.brew_log),
            # A user-level pin preference must not turn latest into exact pins.
            "MISE_PIN": "1",
        }

    def run_setup(self):
        return subprocess.run(
            [str(ROOT / "setup-toolchains")],
            cwd=self.project,
            env=self.env,
            text=True,
            capture_output=True,
        )

    def mise_events(self):
        return [json.loads(line) for line in self.mise_log.read_text().splitlines()]

    def test_setup_resets_legacy_settings_and_selects_floating_global_defaults(self):
        local_before = self.local_config.read_bytes()
        project_before = self.project_config.read_bytes()
        venv_before = self.venv.read_bytes()
        uv_python_before = self.uv_python.read_bytes()

        first = self.run_setup()

        self.assertEqual(first.returncode, 0, first.stderr)
        config = self.config.read_text()
        for obsolete in (
            "auto_install = false",
            "not_found_system_fallback = false",
            "upgrade.auto_prune = false",
        ):
            self.assertNotIn(obsolete, config)
        self.assertIn("pin = true", config)
        self.assertIn("jobs = 3", config)
        for request in ('node = "latest"', 'java = "latest"', 'python = "latest"'):
            self.assertIn(request, config)
        self.assertIn('ruby = "3.4.3"', config)

        events = self.mise_events()
        unset_keys = {
            event["args"][2]
            for event in events
            if event["args"][:2] == ["settings", "unset"]
        }
        self.assertEqual(
            unset_keys,
            {"auto_install", "not_found_system_fallback", "upgrade.auto_prune"},
        )
        use_event = next(event for event in events if event["args"][0] == "use")
        self.assertEqual(
            use_event["args"],
            ["use", "--global", "--fuzzy", "node@latest", "java@latest", "python@latest"],
        )
        self.assertEqual(use_event["cwd"], str(self.home.resolve()))
        self.assertEqual(use_event["pin"], "1")
        self.assertEqual(use_event["prereleases"], "false")
        self.assertEqual(use_event["fetch_remote_versions_cache"], "0s")
        verified = [
            event for event in events
            if event["args"][:2] == ["exec", "--"]
            or event["args"][:1] == ["exec"]
        ]
        self.assertEqual(
            [event["args"][event["args"].index("--") + 1:] for event in verified],
            [["node", "--version"], ["java", "-version"],
             ["javac", "-version"], ["python", "--version"]],
        )
        self.assertTrue(all(event["auto_install"] == "false" for event in verified))

        self.assertEqual(self.local_config.read_bytes(), local_before)
        self.assertEqual(self.project_config.read_bytes(), project_before)
        self.assertEqual(self.venv.read_bytes(), venv_before)
        self.assertEqual(self.uv_python.read_bytes(), uv_python_before)
        brew_calls = [json.loads(line) for line in self.brew_log.read_text().splitlines()]
        self.assertIn(["list", "--formula", "--versions", "uv"], brew_calls)
        self.assertIn(["tab", "--installed-on-request", "--formula", "uv"], brew_calls)
        self.assertNotIn(["install", "--formula", "uv"], brew_calls)

        config_after_first_run = self.config.read_bytes()
        second = self.run_setup()

        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(self.config.read_bytes(), config_after_first_run)
        self.assertEqual(
            len([event for event in self.mise_events() if event["args"][0] == "use"]),
            2,
        )


if __name__ == "__main__":
    unittest.main()
