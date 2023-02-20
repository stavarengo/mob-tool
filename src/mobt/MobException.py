import typing as t

import click
from click import ClickException
from click._compat import get_text_stderr

from mobt import echo


class MobException(ClickException):

    def format_message(self) -> str:
        return click.style(self.message, fg="red")

    def show(self, file: t.Optional[t.IO] = None) -> None:
        if file is None:
            file = get_text_stderr()

        echo(message=self.format_message(), file=file)

