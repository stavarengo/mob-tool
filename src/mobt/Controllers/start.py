import subprocess

import click

from mobt import echo, prompt
from mobt.GitCli.BranchName import BranchName
from mobt.LastTeamMembers.TeamMembers import TeamMembers
from mobt.MobApp.StartOrContinueMobSession import StartOrContinueMobSession


def __ask_for_new_members_name() -> TeamMembers:
    echo('Name of the team members. One per line. Minimum two.')

    members = []
    while True:
        member = prompt('Name (empty to stop asking)', default='').strip()
        if not member:
            break
        members.append(member)

    return TeamMembers(members)


def __fetch_member_names(reset_members: bool) -> TeamMembers:
    from mobt.LastTeamMembers.LastTeamMembersService import LastTeamMembersService
    from mobt.di import di
    last_team_members_service = di.get(LastTeamMembersService)

    new_members = None

    if not reset_members:
        new_members = last_team_members_service.get_last_team()

    if not new_members:
        new_members = __ask_for_new_members_name()

    return new_members


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
def start(
    branch_name: BranchName = None, members: str = None, reset_members: bool = False,
    force_if_non_mob_branch: bool = False
) -> None:
    """
    Start a mob session.

    The BRANCH_NAME is optional. If not passed, it will use the current branch of your repository.
    If the BRANCH_NAME exists, it will continue the mob session from that branch.
    If the BRANCH_NAME doesn't exist, it will create a new branch with that name and start a new mob session.
    """

    from mobt.LastTeamMembers.TeamMemberName import TeamMemberName
    from mobt.di import di

    if members:
        # Members were passed as a comma separated list.
        # We need to convert it to a list of TeamMemberName
        members = TeamMembers([TeamMemberName(n.strip()) for n in members.split(',') if n and n.strip()])

    start_or_continue = di.get(StartOrContinueMobSession)
    session_settings = start_or_continue.execute(
        branch_name=branch_name,
        team=members,
        force_if_non_mob_branch=force_if_non_mob_branch,
        fetch_members_name=lambda: __fetch_member_names(reset_members)
    )

    from mobt.LastTeamMembers.LastTeamMembersService import LastTeamMembersService
    last_team_members_service = di.get(LastTeamMembersService)
    last_team_members_service.save_last_team(session_settings.team)

    echo(f'Driver: {session_settings.team.driver}', fg='bright_green')
    echo(f'Navigator: {session_settings.team.navigator}', fg='bright_green')

    from mobt.Timer.TimerService import TimerService
    di.get(TimerService).start(session_settings.rotation.driverInMinutes)

    _final_announcements(session_settings)

    echo(f'Your driver round is over. Run `mobt next` to pass it to the next driver.', fg='bright_blue')


def _final_announcements(session_settings):
    from mobt.Controllers import controllers_logger
    msg_time_break = "Time for a break!"

    def _speak(msg):
        def _(text: str):
            import platform
            if platform.system() == 'Darwin':
                subprocess.call(['say', text])
            elif platform.system() == 'Linux':
                subprocess.call(['espeak', text])
            else:
                print("\a")

        try:
            _(msg)
        except Exception as e:
            controllers_logger().error(f'Error while trying to make it speak: {e}')

    def _show_gui(on_show: callable = None):
        try:
            import flet as ft
            from mobt.Gui.GuiService import GuiService
            from mobt.di import di

            msg = "Your driver round is over.\nNow you should run `mobt next`."
            if is_it_time_for_break:
                msg = msg_time_break

            di.get(GuiService).show_message(
                msg,
                color=ft.colors.RED_400 if is_it_time_for_break else ft.colors.GREEN_400,
                on_show=on_show,
            )
        except Exception as e:
            controllers_logger().error(f'Error while trying to show the GUI message: {e}')

    rotation = session_settings.rotation
    is_it_time_for_break = rotation.howManyRotationsSinceLastBreak == rotation.howManyRotationsBeforeBreak

    _show_gui(
        on_show=lambda: _speak(msg_time_break if is_it_time_for_break else "Mob Rotate!"),
    )

    if is_it_time_for_break:
        echo(msg_time_break, fg='bright_red')
