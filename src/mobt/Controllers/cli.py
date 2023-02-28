import logging

import click

from mobt.Controllers.done import done
from mobt.Controllers.next import next
from mobt.Controllers.start import start
from mobt.Controllers.wip_commit import wip_commit


@click.group()
@click.version_option(package_name='mob-tool')
@click.option(
    '-v', '--verbose', count=True,
    help='Enables verbose mode. The more -v options, the more verbose, up to -vv'
)
@click.option(
    '-s', '--silent', count=True,
    help='Disable all output except errors. To disable errors, use -sss'
)
def cli(verbose, silent):
    log_level = logging.WARNING

    if silent == 1:
        log_level = logging.ERROR
    elif silent == 2:
        log_level = logging.CRITICAL
    elif silent >= 3:
        log_level = logging.CRITICAL + 1
    elif verbose == 0:
        # Default value set before the if
        pass
    elif verbose == 1:
        log_level = logging.INFO
    elif verbose == 2:
        log_level = logging.DEBUG

    from mobt.Controllers.boostrap_cli_app import bootstrap_cli_app

    bootstrap_cli_app(
        log_level=log_level,
        check_for_new_version=True,
    )


cli.add_command(start, 'start')
cli.add_command(next, 'next')
cli.add_command(done, 'done')
cli.add_command(wip_commit, 'commit')
