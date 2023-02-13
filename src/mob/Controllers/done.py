import click

from mob.MobApp.EndMob import EndMob
from mob.di import di


@click.command()
def done():
    di.get(EndMob).end()
