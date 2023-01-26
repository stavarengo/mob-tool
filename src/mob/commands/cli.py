import click

from mob.commands.done import done
from mob.commands.next import next
from mob.commands.start import start


@click.group()
def cli():
    pass


cli.add_command(start, 'start')
cli.add_command(next, 'next')
cli.add_command(done, 'done')
