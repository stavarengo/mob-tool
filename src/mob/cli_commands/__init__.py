import click

from mob.cli_commands.done import done
from mob.cli_commands.next import next
from mob.cli_commands.start import start


@click.group()
def cli():
    pass


cli.add_command(start, 'start')
cli.add_command(next, 'next')
cli.add_command(done, 'done')
