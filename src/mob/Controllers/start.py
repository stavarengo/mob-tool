import click

from mob.GitCli.BranchName import BranchName
from mob.LastTeamMembers.LastTeamMembersService import LastTeamMembersService
from mob.LastTeamMembers.TeamMemberName import TeamMemberName
from mob.LastTeamMembers.TeamMembers import TeamMembers
from mob.MobApp.StartMobbing import StartMobbing
from mob.di import di


def __ask_for_new_members_name() -> TeamMembers:
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
    is_flag=True,
    help='Force to ask for the team members again',
)
def start(branch_name: BranchName, members: str = None, reset_members: bool = False) -> None:
    """
    It will start a new mob session if BRANCH_NAME doesn't exit, or will continue a previous session if the BRANCH_NAME
    exists.
    """
    last_team_members_service = di.get(LastTeamMembersService)
    if members:
        # Members were passed as a comma separated list.
        # We need to convert it to a list of TeamMemberName
        members = [TeamMemberName(n.strip()) for n in members.split(',') if n and n.strip()]

    if members is None:
        # Members were not passed as a parameter, or it's an empty list. Load the last team members used.
        members = last_team_members_service.get_last_team()
    else:
        # Members were passed as a parameter. Save them as the last team members used.
        last_team_members_service.save_last_team(members)

    if reset_members:
        members = []

    if not members:
        # No members were passed, or no members were saved as the last team members used, or the user wants to reset the
        # team members. Ask for the team members name.
        members = __ask_for_new_members_name()
        last_team_members_service.save_last_team(members)

    di.get(StartMobbing).start(branch_name, members)
