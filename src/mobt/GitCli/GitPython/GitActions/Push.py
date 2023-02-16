from dataclasses import dataclass
from typing import Optional

from git import GitCommandError, Repo

from mobt.GitCli.BranchName import BranchName
from mobt.GitCli.GitPython import git_logger
from mobt.GitCli.GitPython.GitActions.Exceptions import NonFastForwardPush
from mobt.GitCli.GitPython.GitActions.GitAction import GitAction


@dataclass(frozen=False)
class _PullRequestData:
    term: str
    create_url: str
    view_url: str

    def __str__(self):
        return f'Create new {self.term}: {self.create_url}'


@dataclass(frozen=False)
class _PushUndoContext:
    unset_upstream: bool = False
    delete_remote_branch: bool = False


@dataclass()
class Push(GitAction):
    repo: Repo
    branch_to_push: BranchName
    force: bool = False

    def __post_init__(self):
        self.__context: _PushUndoContext = _PushUndoContext()
        super().__post_init__()

    def _execute(self) -> None:
        branch = self.repo.branches[self.branch_to_push]
        if not branch.tracking_branch():
            self._create_upstream()
            self.__context.unset_upstream = True
            self.__context.delete_remote_branch = True
        else:
            self._push_existing_branch()

    def _undo(self):
        if self.__context.delete_remote_branch:
            self.repo.git.push("origin", "--delete", self.branch_to_push)

        if self.__context.unset_upstream:
            self.repo.git.branch("--unset-upstream", self.branch_to_push)

    def _push_existing_branch(self):
        try:
            if self.force:
                self.repo.git.push("origin", self.branch_to_push, "--force")
            else:
                self.repo.git.push("origin", self.branch_to_push)

            pull_request = self._pull_request_url(self.branch_to_push)
            if pull_request:
                git_logger().info(str(pull_request))
            else:
                git_logger().debug(f"I don't know how what's the PR URL for the server: {self.repo.remote().url}")
        except GitCommandError as e:
            if self._is_non_fast_forward_push(str(e)):
                raise NonFastForwardPush.create()
            raise e

    def _create_upstream(self):
        self.repo.git.push("origin", self.branch_to_push, "--set-upstream")

    @staticmethod
    def _is_non_fast_forward_push(error_message: str):
        return "failed to push some refs" in error_message and "non-fast-forward" in error_message

    def _pull_request_url(self, branch: BranchName) -> Optional[_PullRequestData]:
        remote_url = self.repo.remote().url

        # Get the name of the current branch and the remote branch it's tracking
        tracking_branch = self.repo.branches[branch].tracking_branch()

        # Extract the name of the remote branch
        remote_branch_name = tracking_branch.name.split("/")[1]

        # Construct the URL for the pull request/merge request
        if "github" in remote_url:
            return _PullRequestData(
                "Pull Request",
                f"{remote_url.replace('.git', '')}/pullS?q=is%3Apr+is%3Aopen+head%3A{branch}",
                ""
            )
        elif "gitlab" in remote_url:
            return _PullRequestData(
                "Merge Request",
                f"https://gitlab.molops.io/apps/mollie-platform/-/merge_requests/new?merge_request%5Bsource_branch%5D={branch}",
                ""
            )
        elif "bitbucket" in remote_url:
            return _PullRequestData(
                "Pull Request",
                f"{remote_url}/pull-requests?q=source={branch}+state=OPEN",
                ""
            )

        return None
