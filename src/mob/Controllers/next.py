import click

from mob.MobApp.MobNext import MobNext
from mob.di import di


@click.command()
def next():
    di.get(MobNext).next()
