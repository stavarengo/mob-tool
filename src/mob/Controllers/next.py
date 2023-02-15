import click

from mob.Controllers.boostrap_cli_app import bootstrap_cli_app
from mob.MobApp.MobNext import MobNext
from mob.di import di


@click.command()
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose mode')
def next(verbose: bool = False):
    bootstrap_cli_app(verbose)
    di.get(MobNext).next()
