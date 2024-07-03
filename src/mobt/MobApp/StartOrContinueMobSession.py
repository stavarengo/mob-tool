import datetime
from dataclasses import dataclass
from typing import Optional

import click
from git import Repo
from injector import inject

from mobt.EventSystem.EventManager import EventManager
from mobt.GitCli.BranchName import BranchName
from mobt.GitCli.GitCliWithAutoRollback import GitCliWithAutoRollback
from mobt.MobApp.ContinueMobSession import ContinueMobSession
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
            stash_name = self.git.if_dirty_propose_stash_or_discard_or_abort()

            self.git.fail_if_dirty()
            self.git.fetch_all()

            branch_name = branch_name or self.git.current_branch()

            if self.git.branch_exists(branch_name):
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

            start_result = self.start_mob_session.start(branch_name=branch_name, team=team, fail_if_dirty=False,
                                                 force_if_non_mob_branch=force_if_non_mob_branch, fetch_all=False)


            if stash_name:
                user_choice = click.confirm(
                    'Do you want to apply the stashed changes?',
                    default=True,
                )
                if user_choice:
                    self.git.try_stash_pop(stash_name=stash_name)

            return start_result
        except Exception as e:
            self.git.undo()
            from git import GitError

            if isinstance(e, GitError):
                e = MobException(str(e))

            raise e
