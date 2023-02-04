import click

from mob.Controllers.done import done
from mob.Controllers.next import next
from mob.Controllers.start import start


@click.group()
def cli():
    pass


cli.add_command(start, 'start')
cli.add_command(next, 'next')
cli.add_command(done, 'done')
