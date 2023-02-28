import logging

from mobt.Logging.color_by_log_level import color_by_log_level


class Formatter(logging.Formatter):

    def format(self, record: logging.LogRecord) -> str:
        import click

        if record.name == 'git.cmd' and record.args[0]:
            msg = " ".join(record.args[0])
        else:
            msg = super().format(record)

        return click.style(msg, fg=color_by_log_level(record))
