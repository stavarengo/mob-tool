from dataclasses import dataclass
from typing import Optional

from mobt.PopenObserver.PopenListener import PopenListener


@dataclass(frozen=False)
class PullRequestUrl:
    url: str
    term: str
    action: str


class GitPopenListener(PopenListener):

    def __init__(self) -> None:
        super().__init__()
        self._regex_to_find_url = None

    def popen_executed(self, command: list[str], stdout: str, stderr: str) -> None:
        from git import remove_password_if_present
        command = remove_password_if_present(command)

        msg = " ".join(command)
        from mobt.MobApp import mob_app_logger

        whole_output = ((stdout or "") + (stderr or "")).strip()
        if self._is_git_command(command):
            from mobt import echo

            if self._is_safe_command(command):
                mob_app_logger().debug(msg)
            else:
                mob_app_logger().info(msg)

            if self._is_git_push_command(command):
                pull_request_url = self._get_pul_request_url(whole_output)
                if pull_request_url:
                    echo(
                        f'To {pull_request_url.action} {pull_request_url.term}, visit:\n   {pull_request_url.url}',
                        fg='bright_blue'
                    )
        else:
            mob_app_logger().debug(msg)

        if whole_output:
            formatted_output = whole_output.replace("\n", "\n   > ")
            mob_app_logger().debug(f'   > {formatted_output}')

    def _is_safe_command(self, command: list) -> bool:
        safe_sub_commands = ['diff', 'fetch', 'version', 'merge-base']
        return any(self._is_git_command(command, sub_command) for sub_command in safe_sub_commands)

    def _get_pul_request_url(self, text: str) -> Optional[PullRequestUrl]:
        if not text or 'https://' not in text:
            return None

        if not self._regex_to_find_url:
            import re
            self._regex_to_find_url = re.compile(r'https?://\S+')

        all_urls = self._regex_to_find_url.findall(text)

        for url in all_urls:
            if '/merge_requests/' in url:
                if '/merge_requests/new?' in url:
                    return PullRequestUrl(url, 'MR', 'create')
                return PullRequestUrl(url, 'MR', 'view')
            elif '/pull/' in url:
                if '/pull/new' in url:
                    return PullRequestUrl(url, 'PR', 'create')
                return PullRequestUrl(url, 'PR', 'view')

        return None

    def _is_git_command(self, command: list, sub_command: str = None) -> bool:
        return command and command[0] == 'git' and (not sub_command or command[1] == sub_command)

    def _is_git_push_command(self, command: list) -> bool:
        return self._is_git_command(command, 'push')
