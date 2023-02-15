import click

from mob.Controllers.boostrap_cli_app import bootstrap_cli_app
from mob.Controllers.done import done
from mob.Controllers.next import next
from mob.Controllers.start import start


@click.group()
@click.version_option()
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose mode')
@click.pass_context
def cli(ctx, verbose):
    bootstrap_cli_app(verbose)

    ctx.ensure_object(dict)

    ctx.obj['verbose'] = verbose


cli.add_command(start, 'start')
cli.add_command(next, 'next')
cli.add_command(done, 'done')
