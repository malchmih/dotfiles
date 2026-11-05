"""Check shared Zsh startup in isolated homes; no tools are installed."""

from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
ZSH = shutil.which("zsh")
if ZSH is None:
    raise RuntimeError("zsh is required to run the shell startup tests")


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
        self.linuxbrew = self.home / "linuxbrew/.linuxbrew"
        self.package.mkdir(parents=True)
        linux_zshenv = (ROOT / "zshenv").read_text().replace(
            "/home/linuxbrew/.linuxbrew", str(self.linuxbrew)
        )
        self.linux_zshenv = self.home / "zshenv-linux"
        self.linux_zshenv.write_text(linux_zshenv)
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

    def test_path_order_and_deduplication_across_session_types(self):
        flags_list = ("-c", "-lc", "-ic", "-lic")
        for opencode_present in (False, True):
            for linuxbrew_present in (False, True):
                with self.subTest(opencode=opencode_present, linuxbrew=linuxbrew_present):
                    if self.opencode.exists():
                        shutil.rmtree(self.opencode)
                    if self.linuxbrew.exists():
                        shutil.rmtree(self.linuxbrew)
                    self.env["PATH"] = f"{self.package}:/usr/bin:/bin"

                    if opencode_present:
                        self.opencode.mkdir(parents=True)
                        self.env["PATH"] += f":{self.opencode}:{self.opencode}"
                    if linuxbrew_present:
                        brew_bin = self.linuxbrew / "bin"
                        brew_bin.mkdir(parents=True)
                        (self.linuxbrew / "sbin").mkdir()
                        brew = brew_bin / "brew"
                        brew.write_text("#!/bin/sh\n")
                        brew.chmod(0o755)
                        self.env["PATH"] = f"{brew_bin}:{self.env['PATH']}:{brew_bin}"
                    else:
                        # A partial prefix without its CLI must remain optional.
                        (self.linuxbrew / "bin").mkdir(parents=True)

                    script = (
                        f'OSTYPE=linux-gnu; source "{self.linux_zshenv}"; '
                        "print -rl -- $path"
                    )
                    for flags in flags_list:
                        with self.subTest(flags=flags):
                            paths = self.run_shell(flags, script).stdout.splitlines()
                            self.assertEqual(len(paths), len(set(paths)))
                            self.assertEqual(paths.count(str(self.local)), 1)
                            self.assertIn(str(self.local), paths)
                            self.assertIn(str(self.package), paths)
                            self.assertLess(paths.index(str(self.local)),
                                            paths.index(str(self.package)))

                            if opencode_present:
                                self.assertEqual(paths.count(str(self.opencode)), 1)
                                self.assertLess(paths.index(str(self.local)),
                                                paths.index(str(self.opencode)))
                                self.assertLess(paths.index(str(self.opencode)),
                                                paths.index(str(self.package)))
                            else:
                                self.assertNotIn(str(self.opencode), paths)

                            brew_bin = self.linuxbrew / "bin"
                            brew_sbin = self.linuxbrew / "sbin"
                            if linuxbrew_present:
                                self.assertEqual(paths.count(str(brew_bin)), 1)
                                self.assertEqual(paths.count(str(brew_sbin)), 1)
                                user_prefix = self.opencode if opencode_present else self.local
                                self.assertLess(paths.index(str(user_prefix)),
                                                paths.index(str(brew_bin)))
                                self.assertLess(paths.index(str(brew_bin)),
                                                paths.index(str(brew_sbin)))
                                self.assertLess(paths.index(str(brew_sbin)),
                                                paths.index(str(self.package)))
                            else:
                                self.assertNotIn(str(brew_bin), paths)
                                self.assertNotIn(str(brew_sbin), paths)

    def test_local_interactive_preference_can_override_shared_order(self):
        self.opencode.mkdir(parents=True)
        local_config = self.home / "config/dotfiles"
        local_config.mkdir(parents=True)
        (local_config / "interactive.zsh").write_text(
            'export DOTFILES_LOCAL_INTERACTIVE=loaded\n'
            'path=("$HOME/override" $path)\n'
        )
        output = self.run_shell(
            "-lic", 'print -r -- "$DOTFILES_LOCAL_INTERACTIVE"; print -rl -- $path'
        ).stdout.splitlines()
        self.assertEqual(output[0], "loaded")
        self.assertEqual(output[1], str(self.home / "override"))

    def test_macos_login_restores_order_after_homebrew(self):
        self.opencode.mkdir(parents=True)
        brew = self.home / "homebrew/bin/brew"
        brew.parent.mkdir(parents=True)
        brew.write_text("#!/bin/sh\n")
        brew.chmod(0o755)
        profile = self.home / "darwin-profile"
        profile.write_text((ROOT / "zprofile").read_text().replace(
            "/opt/homebrew", str(self.home / "homebrew")
        ))
        script = (f'source "{ROOT / "zshenv"}"; path=(/usr/bin /bin $path); '
                  f'OSTYPE=darwin; '
                  f'source "{profile}"; print -rl -- $path')
        paths = self.run_shell("-fc", script).stdout.splitlines()
        self.assertLess(paths.index(str(self.local)), paths.index(str(self.opencode)))
        self.assertLess(paths.index(str(self.opencode)), paths.index(str(brew.parent)))
        self.assertLess(paths.index(str(brew.parent)), paths.index("/usr/bin"))


if __name__ == "__main__":
    unittest.main()
