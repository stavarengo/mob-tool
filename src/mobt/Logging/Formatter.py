import logging

from mobt.Logging.color_by_log_level import color_by_log_level


class Formatter(logging.Formatter):

    def format(self, record: logging.LogRecord) -> str:
        import click

        return click.style(f"{super().format(record)}", fg=color_by_log_level(record))
