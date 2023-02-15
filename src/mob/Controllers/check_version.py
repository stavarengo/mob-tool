import click

from mob.AutoUpdate.AutoUpdatedService import AutoUpdateService
from mob.di import di


@click.command()
@click.option(
    '--force',
    '-f',
    is_flag=True,
    help='Force fetch the version from the server again',
)
def cache_available_version(force: bool = False) -> None:
    service = di.get(AutoUpdateService)
    if force:
        service.delete_cache_version()
    service.store_available_version()
    print(click.style(f'Done!', fg='bright_green'))
