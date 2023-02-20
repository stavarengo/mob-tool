import click

from mobt import echo


@click.command()
@click.option(
    '--message',
    '-m',
    help='Optional. Message used for the last commit.',
)
@click.option(
    '--do-not-try-to-rebase',
    '-R',
    is_flag=True,
    help='Rebase all changes after squashing. If the rebase fails, the mob will be ended as usual, but the rebase '
         'will be aborted.',
)
@click.pass_context
def done(ctx, message: str = None, do_not_try_to_rebase: bool = False) -> None:
    """
        End the current mob session.

        It will remove the mob session file, squash all the commits and push all the changes to the remote.
        All git hooks will be executed for this final commit.
    """
    from mobt.di import di
    from mobt.MobApp.EndMob import EndMob
    di.get(EndMob).end(message=message, do_not_try_to_rebase=do_not_try_to_rebase)

    echo(f'Done!', fg='green')
