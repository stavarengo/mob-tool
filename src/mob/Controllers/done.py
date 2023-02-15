import click

from mob.MobApp.EndMob import EndMob
from mob.di import di


@click.command()
@click.pass_context
def done(ctx):
    """
        End the current mob session.

        It will remove the mob session file, squash all the commits and push all the changes to the remote.
        All git hooks will be executed for this final commit.
    """
    di.get(EndMob).end()

    click.secho(f'Done!', fg='green')
