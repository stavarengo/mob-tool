import click

from mobt.Controllers.common_params import common_params, AppContext, pass_state
from mobt.Controllers.done import done
from mobt.Controllers.next import next
from mobt.Controllers.start import start
from mobt.Controllers.wip_commit import wip_commit
from mobt.Controllers.squash import squash


@click.group()
@click.version_option(package_name='mob-tool')
@common_params
def cli():
    from mobt.Controllers.boostrap_cli_app import bootstrap_cli_app

    bootstrap_cli_app(
        check_for_new_version=True,
    )



cli.add_command(start, 'start')
cli.add_command(next, 'next')
cli.add_command(done, 'done')
cli.add_command(wip_commit, 'commit')
cli.add_command(squash, 'squash')
