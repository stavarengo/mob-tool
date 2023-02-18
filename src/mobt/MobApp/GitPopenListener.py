from mobt import echo
from mobt.MobApp import mob_app_logger
from mobt.PopenObserver.PopenListener import PopenListener


class GitPopenListener(PopenListener):

    def popen_executed(self, command: list, stdout: str, stderr: str) -> None:
        from git import remove_password_if_present
        command = remove_password_if_present(command)

        msg = f'{" ".join(command)}'

        if self._is_git_command(command) and not self._is_git_version_command(command):
            echo(msg, fg='bright_black')
        else:
            mob_app_logger().debug(msg)

    def _is_git_command(self, command: list) -> bool:
        return command and command[0] == 'git'

    def _is_git_version_command(self, command: list) -> bool:
        return command and command[0] == 'git' and command[1] == 'version'
