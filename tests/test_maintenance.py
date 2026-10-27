"""Exercise maintenance with isolated, fake managers; never update the host.

Run with: python3 -m unittest discover -s tests -v
"""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
STUB = r'''
import json
import os
from pathlib import Path
import subprocess
import sys

name = Path(sys.argv[0]).name
args = sys.argv[1:]
config = json.loads(Path(os.environ["MOCK_CONFIG"]).read_text())
with open(os.environ["MOCK_LOG"], "a") as log:
    log.write(json.dumps({"command": [name] + args,
                          "auto_update": os.getenv("HOMEBREW_NO_AUTO_UPDATE"),
                          "no_cleanup": os.getenv("HOMEBREW_NO_INSTALL_CLEANUP")}) + "\n")
if [name] + args in config.get("fail", []):
    sys.exit(1)
if name == "id":
    print(config.get("uid", "1000"))
elif name == "uname":
    print(config.get("platform", "Darwin"))
elif name == "sudo":
    if args != ["-v"]:
        sys.exit(subprocess.run(args).returncode)
elif name == "brew" and args == ["list", "--cask"]:
    print(config.get("casks", "example-app"))
else:
    print("MOCK " + " ".join([name] + args))
'''


class MaintenanceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.bin = self.home / "bin"
        self.bin.mkdir()
        self.checkout = self.home / "checkout"
        (self.checkout / "lib").mkdir(parents=True)
        self.os_release = self.home / "os-release"
        self.os_release.write_text('ID=ubuntu\n')
        for name in ("up", "cleanup"):
            target = self.checkout / name
            shutil.copyfile(ROOT / name, target)
            target.chmod(0o755)
        library = (ROOT / "lib/maintenance.sh").read_text()
        # Substitute only the OS identity fixture; no production test-only API.
        (self.checkout / "lib/maintenance.sh").write_text(
            library.replace("/etc/os-release", str(self.os_release))
        )
        for name in ("bash", "dirname", "readlink"):
            (self.bin / name).symlink_to(shutil.which(name))
        self.config = self.home / "config.json"
        self.log = self.home / "calls.jsonl"
        self.env = {
            "PATH": str(self.bin),
            "HOME": str(self.home),
            "MOCK_CONFIG": str(self.config),
            "MOCK_LOG": str(self.log),
            # Assert the workflow overrides inherited cleanup suppression.
            "HOMEBREW_NO_INSTALL_CLEANUP": "1",
        }

    def run_command(self, command="up", answer="y\n", platform="Darwin",
                    managers=("brew", "uv", "pipx", "softwareupdate", "apt-get", "sudo"),
                    fail=(), casks="example-app", uid="1000", args=()):
        self.config.write_text(json.dumps({"platform": platform, "fail": fail,
                                           "casks": casks, "uid": uid}))
        for name in ("id", "uname") + managers:
            target = self.bin / name
            target.write_text(f"#!{sys.executable}\n" + STUB)
            target.chmod(0o755)
        result = subprocess.run(
            [str(self.checkout / command), *args], input=answer,
            text=True, capture_output=True, env=self.env, cwd=self.home,
        )
        self.events = [json.loads(line) for line in self.log.read_text().splitlines()] if self.log.exists() else []
        self.calls = [event["command"] for event in self.events]
        return result

    def test_macos_plan_approval_and_scope(self):
        result = self.run_command()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(any(c[0] == "sudo" for c in self.calls))
        self.assertLess(self.calls.index(["brew", "update"]), self.calls.index(["brew", "outdated", "--formula"]))
        self.assertLess(self.calls.index(["softwareupdate", "--list"]), self.calls.index(["brew", "upgrade", "--formula", "--yes"]))
        for call in (["brew", "upgrade", "--cask", "--yes"],
                     ["uv", "tool", "upgrade", "--all"], ["pipx", "upgrade-all"]):
            self.assertIn(call, self.calls)
        self.assertIn("UNKNOWN", result.stdout)
        self.assertEqual(result.stdout.count("Approve up"), 1)
        self.assertNotIn("--no-quit", str(self.calls))
        self.assertNotIn("--greedy", str(self.calls))
        self.assertFalse(any(c[0] == "apt-get" or "autoremove" in c or "cleanup" in c for c in self.calls))
        self.assertEqual([c for c in self.calls if c[0] == "softwareupdate"], [["softwareupdate", "--list"]])
        for event in self.events:
            if event["command"][0] == "brew":
                self.assertEqual(event["auto_update"], "1")
                self.assertIsNone(event["no_cleanup"])

    def test_no_casks_needs_no_sudo_on_mac(self):
        result = self.run_command(casks="")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(any(c[0] == "sudo" or "--cask" in c[1:] and c[1] != "list" for c in self.calls))

    def test_linux_sequence_and_scope(self):
        result = self.run_command(platform="Linux")
        self.assertEqual(result.returncode, 0, result.stderr)
        refresh = ["apt-get", "-o", "APT::Update::Error-Mode=any", "update"]
        preview = ["apt-get", "--simulate", "upgrade", "--no-remove"]
        upgrade = ["apt-get", "upgrade", "--no-remove", "--yes"]
        self.assertLess(self.calls.index(["sudo", "-v"]), self.calls.index(["brew", "update"]))
        self.assertLess(self.calls.index(refresh), self.calls.index(preview))
        self.assertLess(self.calls.index(preview), self.calls.index(upgrade))
        self.assertFalse(any(c[0] == "softwareupdate" or "--cask" in c for c in self.calls))

    def test_debian_is_supported(self):
        self.os_release.write_text('ID="debian"\n')
        self.assertEqual(self.run_command(platform="Linux").returncode, 0)

    def test_enter_and_explicit_yes_approve_both_commands(self):
        for command, actual in (("up", ["brew", "upgrade", "--formula", "--yes"]),
                                ("cleanup", ["brew", "cleanup"])):
            for answer in ("\n", "y\n", "Y\n", "yes\n", "YES\n"):
                with self.subTest(command=command, answer=answer):
                    self.log.unlink(missing_ok=True)
                    result = self.run_command(command=command, answer=answer,
                                              managers=("brew", "softwareupdate"))
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertIn("[Y/n]", result.stdout)
                    self.assertIn(actual, self.calls)

    def test_eof_no_and_unrecognized_answers_cancel_both_commands(self):
        for command in ("up", "cleanup"):
            for answer in ("", "n\n", "N\n", "no\n", "NO\n", "maybe\n", " \n"):
                with self.subTest(command=command, answer=answer):
                    self.log.unlink(missing_ok=True)
                    result = self.run_command(command=command, answer=answer,
                                              managers=("brew", "softwareupdate"))
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertIn("Cancelled", result.stdout)
                    self.assertFalse(any(c[:2] == ["brew", "upgrade"] for c in self.calls))
                    self.assertNotIn(["brew", "cleanup"], self.calls)
                    self.assertNotIn(["brew", "autoremove"], self.calls)

    def test_eof_prevents_upgrades_after_refresh(self):
        result = self.run_command(answer="")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(["brew", "update"], self.calls)
        self.assertFalse(any("upgrade" in c or "upgrade-all" in c for c in self.calls))
        self.assertIn("Cancelled", result.stdout)

    def test_brew_refresh_failure_skips_brew_but_not_other_managers(self):
        result = self.run_command(fail=[["brew", "update"]])
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(any(c[:2] == ["brew", "upgrade"] for c in self.calls))
        self.assertIn(["uv", "tool", "upgrade", "--all"], self.calls)
        self.assertIn("FAILED", result.stderr)

    def test_apt_refresh_failure_skips_apt_upgrade(self):
        result = self.run_command(platform="Linux", fail=[["apt-get", "-o", "APT::Update::Error-Mode=any", "update"]])
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn(["apt-get", "upgrade", "--no-remove", "--yes"], self.calls)
        self.assertIn(["brew", "upgrade", "--formula", "--yes"], self.calls)

    def test_failed_upgrade_does_not_stop_independent_managers(self):
        result = self.run_command(fail=[["brew", "upgrade", "--formula", "--yes"]])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(["pipx", "upgrade-all"], self.calls)

    def test_failed_preview_is_not_approved(self):
        result = self.run_command(fail=[["brew", "outdated", "--formula"], ["uv", "tool", "list"]])
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn(["brew", "upgrade", "--formula", "--yes"], self.calls)
        self.assertNotIn(["uv", "tool", "upgrade", "--all"], self.calls)
        self.assertIn(["pipx", "upgrade-all"], self.calls)

    def test_failed_sudo_skips_privileged_work(self):
        result = self.run_command(platform="Linux", fail=[["sudo", "-v"]])
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(any(c[0] == "apt-get" for c in self.calls))
        self.assertIn(["brew", "upgrade", "--formula", "--yes"], self.calls)

    def test_mac_casks_do_not_require_upfront_sudo(self):
        result = self.run_command(managers=("brew", "uv", "pipx", "softwareupdate"))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(any(c[0] == "sudo" for c in self.calls))
        self.assertIn(["brew", "outdated", "--cask"], self.calls)
        self.assertIn(["brew", "upgrade", "--cask", "--yes"], self.calls)
        self.assertIn(["brew", "upgrade", "--formula", "--yes"], self.calls)

    def test_failed_cask_upgrade_does_not_stop_independent_managers(self):
        result = self.run_command(fail=[["brew", "upgrade", "--cask", "--yes"]])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAILED: Homebrew: upgrade all eligible casks", result.stderr)
        self.assertIn(["uv", "tool", "upgrade", "--all"], self.calls)
        self.assertIn(["pipx", "upgrade-all"], self.calls)
        self.assertIn(["brew", "upgrade", "--formula", "--yes"], self.calls)

    def test_failed_cask_preview_skips_casks_only(self):
        result = self.run_command(fail=[["brew", "outdated", "--cask"]])
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn(["brew", "upgrade", "--cask", "--yes"], self.calls)
        self.assertIn(["brew", "upgrade", "--formula", "--yes"], self.calls)

    def test_failed_mac_scan_does_not_prevent_tool_upgrades(self):
        result = self.run_command(fail=[["softwareupdate", "--list"]])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(["brew", "upgrade", "--formula", "--yes"], self.calls)

    def test_missing_sudo_does_not_run_privileged_updates(self):
        result = self.run_command(platform="Linux", managers=("brew", "apt-get"))
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(any(c[0] == "apt-get" for c in self.calls))
        self.assertIn(["brew", "upgrade", "--formula", "--yes"], self.calls)

    def test_optional_managers_absent(self):
        result = self.run_command(managers=("softwareupdate",))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("No eligible changes", result.stdout)
        self.assertNotIn("Approve", result.stdout)

    def test_missing_native_manager_is_failure(self):
        result = self.run_command(platform="Linux", managers=())
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("APT not on PATH", result.stderr)

    def test_cleanup_previews_then_removes_brew_and_apt(self):
        result = self.run_command(command="cleanup", platform="Linux")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.count("Approve cleanup"), 1)
        for preview, actual in ((["brew", "autoremove", "--dry-run"], ["brew", "autoremove"]),
                                (["brew", "cleanup", "--dry-run"], ["brew", "cleanup"]),
                                (["apt-get", "--simulate", "autoremove"], ["apt-get", "autoremove", "--yes"])):
            self.assertLess(self.calls.index(preview), self.calls.index(actual))
        self.assertLess(self.calls.index(["apt-get", "--simulate", "autoremove"]), self.calls.index(["brew", "autoremove"]))
        self.assertFalse(any(c[0] in ("uv", "pipx", "softwareupdate") or "update" in c or "zap" in c for c in self.calls))

    def test_cleanup_cancellation(self):
        result = self.run_command(command="cleanup", answer="no\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(["brew", "cleanup", "--dry-run"], self.calls)
        self.assertNotIn(["brew", "cleanup"], self.calls)
        self.assertNotIn(["brew", "autoremove"], self.calls)
        self.assertFalse(any(c[0] == "sudo" for c in self.calls))

    def test_cleanup_failure_still_attempts_independent_removals(self):
        result = self.run_command(command="cleanup", platform="Linux", fail=[["brew", "autoremove"]])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(["brew", "cleanup"], self.calls)
        self.assertIn(["apt-get", "autoremove", "--yes"], self.calls)

    def test_failed_cleanup_preview_skips_brew_removals(self):
        result = self.run_command(command="cleanup", platform="Linux", fail=[["brew", "cleanup", "--dry-run"]])
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn(["brew", "autoremove"], self.calls)
        self.assertIn(["apt-get", "autoremove", "--yes"], self.calls)

    def test_symlink_entrypoint_from_unrelated_directory(self):
        (self.checkout / "linked-up").symlink_to("up")
        result = self.run_command(command="linked-up", args=("--help",))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Usage: up", result.stdout)
        self.assertEqual(self.calls, [])

    def test_absolute_installed_symlink(self):
        installed = self.home / "installed"
        installed.mkdir()
        (installed / "cleanup").symlink_to(self.checkout / "cleanup")
        result = subprocess.run(
            [str(installed / "cleanup"), "--help"], capture_output=True,
            text=True, env=self.env, cwd=self.home,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Usage: cleanup", result.stdout)

    @unittest.skipUnless((ROOT / "dotbot/bin/dotbot").exists(), "Dotbot submodule is not initialized")
    def test_dotbot_links_all_maintenance_commands_in_sandbox(self):
        env = dict(self.env, XDG_CONFIG_HOME=str(self.home / "config"))
        result = subprocess.run(
            [sys.executable, str(ROOT / "dotbot/bin/dotbot"),
             "-d", str(ROOT), "-c", str(ROOT / "install.conf.yaml")],
            capture_output=True, text=True, env=env, cwd=self.home,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for name in ("up", "cleanup", "update-tools", "update-system"):
            link = self.home / ".local/bin" / name
            self.assertTrue(link.is_symlink())
            self.assertEqual(link.resolve(), ROOT / name)
            self.assertTrue(os.access(link, os.X_OK))
        self.assertFalse(self.log.exists(), "Installing links must not run maintenance")

    @unittest.skipUnless(shutil.which("zsh"), "Zsh is not installed")
    def test_shell_removes_plugin_collisions_but_preserves_local_overrides(self):
        omz = self.home / "omz"
        (omz / "plugins/common-aliases").mkdir(parents=True)
        (omz / "plugins/common-aliases/common-aliases.plugin.zsh").touch()
        (omz / "oh-my-zsh.sh").write_text(
            "alias up='print plugin-up'\ncleanup() { print plugin-cleanup; }\n"
        )
        for name in ("up", "cleanup"):
            (self.bin / name).symlink_to(self.checkout / name)
        config = self.home / "config"
        (config / "dotfiles").mkdir(parents=True)
        env = dict(self.env, ZSH=str(omz), XDG_CONFIG_HOME=str(config))
        check = f'source "{ROOT / "zshrc"}"; whence -w up cleanup'
        result = subprocess.run([shutil.which("zsh"), "-dfi", "-c", check],
                                env=env, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("up: command", result.stdout)
        self.assertIn("cleanup: command", result.stdout)
        (config / "dotfiles/interactive.zsh").write_text("alias up='print local-up'\n")
        result = subprocess.run([shutil.which("zsh"), "-dfi", "-c", check],
                                env=env, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("up: alias", result.stdout)
        self.assertIn("cleanup: command", result.stdout)

    def test_root_is_rejected(self):
        result = self.run_command(uid="0")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.calls, [["id", "-u"]])

    def test_unsupported_platform_is_rejected(self):
        result = self.run_command(platform="Windows_NT")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(any(c[0] in ("sudo", "brew") for c in self.calls))

    def test_unsupported_linux_is_rejected(self):
        self.os_release.write_text('ID=arch\n')
        result = self.run_command(platform="Linux")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(any(c[0] in ("sudo", "brew", "apt-get") for c in self.calls))

    def test_help_and_invalid_arguments_do_no_work(self):
        result = self.run_command(args=("--help",))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.calls, [])
        result = self.run_command(args=("--yes",))
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.calls, [])


if __name__ == "__main__":
    unittest.main()
