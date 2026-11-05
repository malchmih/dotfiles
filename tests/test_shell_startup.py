"""Check shared Zsh startup in isolated homes; no tools are installed."""

from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
ZSH = shutil.which("zsh")


@unittest.skipUnless(ZSH, "zsh is not installed")
class ShellStartupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        for name in ("zshenv", "zprofile", "zshrc"):
            (self.home / f".{name}").symlink_to(ROOT / name)
        self.local = self.home / ".local/bin"
        self.opencode = self.home / ".opencode/bin"
        self.package = self.home / "package/bin"
        self.package.mkdir(parents=True)
        self.env = {
            "HOME": str(self.home),
            "ZDOTDIR": str(self.home),
            "XDG_CONFIG_HOME": str(self.home / "config"),
            "PATH": f"{self.package}:/usr/bin:/bin",
            "TERM": "dumb",
        }

    def run_shell(self, flags, script='print -rl -- $path'):
        return subprocess.run(
            [ZSH, flags, script], env=self.env, cwd=self.home,
            text=True, capture_output=True, check=True,
        )

    def test_existing_install_in_all_sessions_with_deduplicated_precedence(self):
        self.opencode.mkdir(parents=True)
        self.env["PATH"] += f":{self.opencode}:{self.opencode}"
        for flags in ("-c", "-lc", "-ic", "-lic"):
            with self.subTest(flags=flags):
                paths = self.run_shell(flags).stdout.splitlines()
                self.assertEqual(paths.count(str(self.opencode)), 1)
                self.assertLess(paths.index(str(self.local)), paths.index(str(self.opencode)))
                self.assertLess(paths.index(str(self.opencode)), paths.index(str(self.package)))

    def test_missing_install_is_not_added(self):
        for flags in ("-c", "-lc", "-ic", "-lic"):
            with self.subTest(flags=flags):
                self.assertNotIn(str(self.opencode), self.run_shell(flags).stdout.splitlines())

    def test_command_selection_prefers_local_then_standalone(self):
        self.local.mkdir(parents=True)
        self.opencode.mkdir(parents=True)
        for directory in (self.local, self.opencode, self.package):
            command = directory / "opencode"
            command.write_text("#!/bin/sh\n")
            command.chmod(0o755)
        self.assertEqual(self.run_shell("-lc", "command -v opencode").stdout.strip(),
                         str(self.local / "opencode"))
        (self.local / "opencode").unlink()
        self.assertEqual(self.run_shell("-lc", "command -v opencode").stdout.strip(),
                         str(self.opencode / "opencode"))

    def test_local_interactive_preference_can_override_shared_order(self):
        self.opencode.mkdir(parents=True)
        local_config = self.home / "config/dotfiles"
        local_config.mkdir(parents=True)
        (local_config / "interactive.zsh").write_text('path=("$HOME/override" $path)\n')
        paths = self.run_shell("-lic").stdout.splitlines()
        self.assertEqual(paths[0], str(self.home / "override"))

    def test_macos_login_restores_order_after_homebrew(self):
        self.opencode.mkdir(parents=True)
        brew = self.home / "homebrew/bin/brew"
        brew.parent.mkdir(parents=True)
        brew.touch(mode=0o755)
        profile = self.home / "darwin-profile"
        profile.write_text((ROOT / "zprofile").read_text().replace(
            "/opt/homebrew", str(self.home / "homebrew")
        ))
        script = (f'source "{ROOT / "zshenv"}"; OSTYPE=darwin; '
                  f'source "{profile}"; print -rl -- $path')
        paths = self.run_shell("-fc", script).stdout.splitlines()
        self.assertLess(paths.index(str(self.local)), paths.index(str(self.opencode)))
        self.assertLess(paths.index(str(self.opencode)), paths.index(str(brew.parent)))


if __name__ == "__main__":
    unittest.main()
