import click

from mobt import echo
from mobt.GitCli.BranchName import BranchName


@click.command()
@click.argument('branch_name', required=False)
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
def done(ctx, branch_name: BranchName = None, message: str = None, do_not_try_to_rebase: bool = False) -> None:
    """
        End the current mob session.

        The BRANCH_NAME is optional. If not passed, it will use the current branch of your repository.

        It will remove the mob session file, squash all the commits and push all the changes to the remote.
        All git hooks will be executed for this final commit.

        Before pushing, it will try to rebase the changes on top of the main branch, but if the rebase fails, it will
        not affect the end of the mob session. The rebase will just not be done automatically for you. This behavior
        can be changed with the `--do-not-try-to-rebase` option.
    """
    from mobt.di import di
    from mobt.MobApp.EndMob import EndMob
    di.get(EndMob).end(branch_name=branch_name, message=message, do_not_try_to_rebase=do_not_try_to_rebase)

    echo(f'Done!', fg='green')
