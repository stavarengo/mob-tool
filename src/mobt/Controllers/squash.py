import click

from mobt import echo
from mobt.Controllers.common_params import common_params
from mobt.GitCli.BranchName import BranchName


@click.command()
@click.argument('branch_name', required=False)
@click.option(
    '--push',
    '-p',
    is_flag=True,
    help='Force push the squashed commit to the remote.',
)
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
@common_params
def squash(branch_name: BranchName = None, push: bool = False, message: str = None, do_not_try_to_rebase: bool = False) -> None:
    """
        Squash all the commits.
        All git hooks will be executed for this final commit.

        Before squashing, it will try to rebase the changes on top of the main branch. This behavior
        can be changed with the `--do-not-try-to-rebase` option.
    """
    from mobt.di import di
    from mobt.MobApp.SquashBranch import SquashBranch
    di.get(SquashBranch).squash(branch_name=branch_name, message=message, do_not_try_to_rebase=do_not_try_to_rebase, push=push)

    echo(f'Done!', fg='green')
