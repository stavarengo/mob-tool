import click

from mob.Controllers.boostrap_cli_app import bootstrap_cli_app
from mob.MobApp.EndMob import EndMob
from mob.di import di


@click.command()
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose mode')
def done(verbose: bool = False):
    bootstrap_cli_app(verbose)
    di.get(EndMob).end()
