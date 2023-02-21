import subprocess

import click

from mobt import echo, prompt
from mobt.GitCli.BranchName import BranchName
from mobt.LastTeamMembers.TeamMembers import TeamMembers


def __ask_for_new_members_name() -> TeamMembers:
    echo('Name of the team members. One per line. Minimum two.')

    members = []
    while True:
        member = prompt('Name (empty to stop asking)', default='').strip()
        if not member:
            break
        members.append(member)

    return TeamMembers(members)


@click.command()
@click.argument('branch_name', required=False)
@click.option(
    '--members',
    '-m',
    help='Optional. List of names separated by comma. If not passed, team members from the last session (if any) will '
         'be used. If there was no previous session, it will ask for the team members name interactively.',
)
@click.option(
    '--reset-members',
    '-r',
    is_flag=True,
    help='If passed, it will ignore the team members from the last session (if any) and ask for the team members again.',
)
@click.option(
    '--force-if-non-mob-branch',
    '-f',
    is_flag=True,
    help='Force start a mob session even if the branch already exists and is not a mob branch, turning it into a mob '
         'branch.',
)
def start(branch_name: BranchName = None, members: str = None, reset_members: bool = False,
          force_if_non_mob_branch: bool = False) -> None:
    """
    Start a mob session.

    The BRANCH_NAME is optional. If not passed, it will use the current branch of your repository.
    If the BRANCH_NAME exists, it will continue the mob session from that branch.
    If the BRANCH_NAME doesn't exist, it will create a new branch with that name and start a new mob session.
    """

    from mobt.LastTeamMembers.LastTeamMembersService import LastTeamMembersService
    from mobt.LastTeamMembers.TeamMemberName import TeamMemberName
    from mobt.MobApp.StartMobbing import StartMobbing
    from mobt.Gui.GuiService import GuiService
    from mobt.Timer.TimerService import TimerService
    from mobt.di import di
    last_team_members_service = di.get(LastTeamMembersService)
    if members:
        # Members were passed as a comma separated list.
        # We need to convert it to a list of TeamMemberName
        members = TeamMembers([TeamMemberName(n.strip()) for n in members.split(',') if n and n.strip()])

    if members is None:
        from mobt.SessionSettings.SessionSettingsService import SessionSettingsService
        session_settings_service: SessionSettingsService = di.get(SessionSettingsService)
        session_settings = session_settings_service.find()
        members = session_settings.team if session_settings else None

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

    session_settings = di.get(StartMobbing).start(branch_name=branch_name, team=members,
                                                  force_if_non_mob_branch=force_if_non_mob_branch)

    echo(f'Driver: {session_settings.team.driver}', fg='bright_green')
    echo(f'Navigator: {session_settings.team.navigator}', fg='bright_green')

    di.get(TimerService).start(session_settings.rotation.driverInMinutes)

    def _make_it_speak(text: str):
        import platform
        if platform.system() == 'Darwin':
            subprocess.call(['say', text])
        elif platform.system() == 'Linux':
            subprocess.call(['espeak', text])
        else:
            print("\a")

    from mobt.Controllers import controllers_logger

    rotation = session_settings.rotation
    time_for_break = rotation.howManyRotationsSinceLastBreak == rotation.howManyRotationsBeforeBreak

    try:
        _make_it_speak("Time for a break!" if time_for_break else "Mob Rotate!")
    except Exception as e:
        controllers_logger().error(f'Error while trying to make it speak: {e}')
    try:
        import flet as ft

        di.get(GuiService).show_message(
            "Time for a break!" if time_for_break else "Your driver round is over.\nNow you should run `mobt next`.",
            color=ft.colors.RED_400 if time_for_break else ft.colors.GREEN_400,
        )
    except Exception as e:
        controllers_logger().error(f'Error while trying to show the GUI message: {e}')

    echo(f'Your driver round is over. Now you should run `mobt next`.', fg='bright_blue')
