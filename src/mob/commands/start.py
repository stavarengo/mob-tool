import click


@click.command()
@click.argument('branch_name')
def start(branch_name: str) -> None:
    """
    It will start a new mob session if BRANCH_NAME doesn't exit, or will continue a previous session if the BRANCH_NAME
    exists.
    """
    click.echo(f'Started: {branch_name}')
