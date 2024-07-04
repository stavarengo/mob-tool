import click

from mobt import echo
from mobt.Controllers.common_params import common_params


@click.command()
@common_params
def wip_commit():
    """
    Create a WIP commit with all the local changes and push it.

    This command is useful when you want to save your changes, but you don't want to pass it to the next driver.
    """
    from mobt.di import di
    from mobt.MobApp.MobWipCommit import MobWipCommit
    di.get(MobWipCommit).next()

    echo(f'WIP commit created', fg='bright_green')
