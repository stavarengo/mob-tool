import click
from click import ClickException


class MobException(ClickException):
    pass

    def format_message(self) -> str:
        return click.style(self.message, fg="red")
