import click

from mob.LastTeamMembers.LastTeamMembersService import LastTeamMembersService
from mob.LastTeamMembers.TeamMemberName import TeamMemberName
from mob.LastTeamMembers.TeamMembers import TeamMembers
from mob.MobSession.StartMobbing import StartMobbing
from mob.Services.BranchName import BranchName
from mob.di import di


def __get_team_members() -> TeamMembers:
    click.echo('Name of the team members. One per line. Minimum two.')

    members = []
    while True:
        member = click.prompt('Name (empty to stop asking)', default='').strip()
        if not member:
            break
        members.append(member)

    return TeamMembers(members)


@click.command(name='start')
@click.argument('branch_name')
@click.option(
    '--members',
    '-m',
    help='List of names separated by comma',
)
@click.option(
    '--reset-members',
    '-r',
    help='Force to ask for the team members again',
)
def start(branch_name: BranchName, members: str = None, reset_members: bool = False) -> None:
    """
    It will start a new mob session if BRANCH_NAME doesn't exit, or will continue a previous session if the BRANCH_NAME
    exists.
    """
    last_team_members_service = di.get(LastTeamMembersService)
    if members:
        members = [TeamMemberName(n.strip()) for n in members.split(',') if n and n.strip()]

    if members is None:
        members = last_team_members_service.get_last_team()
    else:
        last_team_members_service.save_last_team(members)

    if reset_members:
        members = []

    if not members:
        members = __get_team_members()
        last_team_members_service.save_last_team(members)

    di.get(StartMobbing).start(branch_name, members)
