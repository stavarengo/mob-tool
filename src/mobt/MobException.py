import logging
import typing as t

import click
from click import ClickException
from click._compat import get_text_stderr

from mobt import echo
from mobt.Logging.color_by_log_level import color_by_log_level_int


class MobException(ClickException):

    def format_message(self) -> str:
        return click.style(self.message, fg=color_by_log_level_int(logging.ERROR))

    def show(self, file: t.Optional[t.IO] = None) -> None:
        if file is None:
            file = get_text_stderr()

        echo(message=self.format_message(), file=file)
        if self.extra_help():
            echo(message=click.style(f'{self.extra_help()}', fg='bright_blue'), file=file)

    def extra_help(self) -> str:
        return ""
