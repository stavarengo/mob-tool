import click


@click.group()
def cli():
    pass


@click.command()
@click.argument('branch_name')
def start(branch_name: str) -> None:
    """
    It will start a new mob session if BRANCH_NAME doesn't exit, or will continue a previous session if the BRANCH_NAME
    exists.
    """
    click.echo('asdf')


@click.command()
def next():
    click.echo('next')


@click.command()
def done():
    click.echo('done')


cli.add_command(start)
cli.add_command(next)
cli.add_command(done)
