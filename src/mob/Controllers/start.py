import json
import os

import click
from git import repo

from mob.GitCli.GitPython.GitCliWithGitPython import GitCliWithGitPython
from mob.MobSession.StartMobbing import StartMobbing
from mob.Services.BranchName import BranchName


@click.command(name='start')
@click.argument('branch_name')
@click.option(
    '--reset-members',
    '-m',
    help='Ask for the team members again, instead of using the last one.',
)
def start(branch_name: BranchName, reset_members: bool = False) -> None:
    """
    It will start a new mob session if BRANCH_NAME doesn't exit, or will continue a previous session if the BRANCH_NAME
    exists.
    """

    members = []
    last_team_filename = f'{repo.git_dir}/.mob.last_team.json'

    if not reset_members:
        if os.path.exists(last_team_filename):
            with open(last_team_filename, 'r') as f:
                members = json.loads(f.read())

    need_to_rewrite_last_team_file = False
    if not members or len(members) < 3:
        need_to_rewrite_last_team_file = True
        members = []
        while True:
            member = click.prompt('', prompt_suffix='', default='').strip()
            if not member:
                break
            members.append(member)

    if not members or len(members) < 3:
        click.echo('You must provide at least tree members.')
        return

    if need_to_rewrite_last_team_file:
        with open(last_team_filename, 'w') as f:
            f.write(json.dumps(members))

    git = GitCliWithGitPython(repo)
    StartMobbing(git).start(BranchName(branch_name), members)
