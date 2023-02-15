import click

from mob.Controllers.check_version import cache_available_version
from mob.Controllers.done import done
from mob.Controllers.next import next
from mob.Controllers.start import start


@click.group()
@click.version_option()
def cli():
    pass


cli.add_command(start)
cli.add_command(next, 'next')
cli.add_command(done, 'done')
cli.add_command(cache_available_version, 'cache-available-version')
