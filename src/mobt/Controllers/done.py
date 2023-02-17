import click

from mobt import echo


@click.command()
@click.pass_context
def done(ctx):
    """
        End the current mob session.

        It will remove the mob session file, squash all the commits and push all the changes to the remote.
        All git hooks will be executed for this final commit.
    """
    from mobt.di import di
    from mobt.MobApp.EndMob import EndMob
    di.get(EndMob).end()

    echo(f'Done!', fg='green')
