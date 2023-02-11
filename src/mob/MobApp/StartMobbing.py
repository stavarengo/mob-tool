import platform
import subprocess
import sys
import time
from dataclasses import dataclass

import click
import colorama
from injector import inject

from mob.GitCli.BranchName import BranchName
from mob.GitCli.GitCliWithAutoRollback import GitCliWithAutoRollback
from mob.GitCli.GitPython import get_logger
from mob.MobApp.Exceptions import BranchAlreadyExistsAndIsNotMobBranch
from mob.SessionSettings.RotationSettings import RotationSettings
from mob.SessionSettings.SessionSettings import TeamMembers
from mob.SessionSettings.SessionSettingsService import SessionSettingsService


@inject
@dataclass
class StartMobbing:
    git: GitCliWithAutoRollback

    session_settings_services: SessionSettingsService

    def start(self, branch_name: BranchName, team: TeamMembers):
        try:
            if self.git.branch_exists(branch_name):
                self.git.checkout(branch_name)
                if not self.session_settings_services.find():
                    raise BranchAlreadyExistsAndIsNotMobBranch.create(branch_name)
            else:
                self.git.create_new_branch_from_main_and_checkout(branch_name)
                self.session_settings_services.create(team, RotationSettings())
                self.git.add_undo_callable(lambda: self.session_settings_services.delete())
                self.git.commit_and_push_everything("WIP: mob start", skip_hooks=True)

            session_settings = self.session_settings_services.get()
            print(click.style(f'Driver: {session_settings.team.driver}', fg='bright_green'))
            print(click.style(f'Navigator: {session_settings.team.navigator}', fg='bright_green'))
            self._print_timer(session_settings.rotation.driverInMinutes * 60)
        except Exception as e:
            if self.git.undo_commands.has_commands:
                get_logger().warning("Undoing all Git commands")
                self.git.undo()
            raise e

    def _print_timer(self, duration_in_seconds: int):
        sys.stdout.flush()

        border = "-" * 20
        hide_cursor = "\033[?25l"
        show_cursor = "\033[?25h"
        sys.stdout.write(hide_cursor)
        sys.stdout.write(f"+{border}+\n")
        try:
            for i in range(duration_in_seconds, -1, -1):
                minutes, seconds = divmod(i, 60)
                lines = [
                    "\r",
                    "|",
                    f"{minutes:02d}:{seconds:02d}".center(len(border), " "),
                    "|",
                    "\n",
                    f"+{border}+",
                ]
                sys.stdout.writelines(lines)
                sys.stdout.write(colorama.Cursor.UP(lines.count("\n")))
                sys.stdout.flush()
                time.sleep(1)
            print("")
            self.make_laptop_speak("Mob Rotate!")
        finally:
            sys.stdout.write(show_cursor)

    def make_laptop_speak(self, text: str):
        if platform.system() == 'Darwin':
            subprocess.call(['say', text])
        elif platform.system() == 'Linux':
            subprocess.call(['espeak', text])
        else:
            print("\a")
