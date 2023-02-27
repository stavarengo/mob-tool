from dataclasses import dataclass
from typing import Optional

from git import GitError
from injector import inject

from mobt.EventSystem.EventManager import EventManager
from mobt.GitCli.BranchName import BranchName
from mobt.GitCli.GitCliWithAutoRollback import GitCliWithAutoRollback
from mobt.MobApp.ContinueMobSession import ContinueMobSession
from mobt.MobApp.MobAppRelevantOperationHappened import MobAppRelevantOperationHappened
from mobt.MobApp.StartNewMobSession import StartNewMobSession
from mobt.MobException import MobException
from mobt.SessionSettings import SessionSettings
from mobt.SessionSettings.SessionSettings import TeamMembers
from mobt.SessionSettings.SessionSettingsService import SessionSettingsService


@inject
@dataclass
class StartOrContinueMobSession:
    git: GitCliWithAutoRollback
    continue_mob_session: ContinueMobSession
    start_mob_session: StartNewMobSession
    session_settings_services: SessionSettingsService
    event_manager: EventManager

    def execute(
        self,
        branch_name: Optional[BranchName],
        team: Optional[TeamMembers],
        fetch_members_name: callable,
        force_if_non_mob_branch: bool = False,
    ) -> SessionSettings:

        try:
            self.git.fail_if_dirty()
            self.git.fetch_all()

            branch_name = branch_name or self.git.current_branch()

            if self.git.branch_exists(branch_name):
                human_log = f'Checking out branch "{branch_name}"'
                remote_branch = self.git.get_remote_branch(branch_name)
                if remote_branch:
                    human_log += f' (tracking "{remote_branch.name}"))'
                self.event_manager.dispatch_event(MobAppRelevantOperationHappened(human_log=f'{human_log}...'))
                self.git.checkout(branch_name)
                self.git.pull_with_rebase()
                if self.session_settings_services.find():
                    return self.continue_mob_session.go(
                        branch_name=branch_name,
                        team=team,
                        fetch_all=False,
                        fail_if_dirty=False
                    )

            if not team:
                team = fetch_members_name()

            return self.start_mob_session.start(
                branch_name=branch_name,
                team=team,
                fail_if_dirty=False,
                force_if_non_mob_branch=force_if_non_mob_branch,
                fetch_all=False,
            )
        except Exception as e:
            self.git.undo()

            if isinstance(e, GitError):
                e = MobException(str(e))

            raise e
