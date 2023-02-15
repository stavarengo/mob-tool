import click

from mob.AutoUpdate.AutoUpdateService import AutoUpdateService
from mob.Controllers.boostrap_cli_app import bootstrap_cli_app
from mob.di import di


@click.command()
@click.option(
    '--force',
    '-f',
    is_flag=True,
    help='Force fetch the version from the server again',
)
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose mode')
def cache_available_version(force: bool = False, verbose: bool = False) -> None:
    bootstrap_cli_app(verbose, False)
    service = di.get(AutoUpdateService)
    if force:
        service.delete_cache_version()
    service.store_available_version()
    print(click.style(f'Done!', fg='bright_green'))
