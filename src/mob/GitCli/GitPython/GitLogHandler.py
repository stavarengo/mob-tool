import logging
import sys
from dataclasses import dataclass
from logging import LogRecord

import click

from mob.GitCli.GitPython import get_logger


@dataclass
class GroupContextManager:
    group: str
    logger: logging.Logger

    def __enter__(self):
        self.logger.info(self.group, extra={"start_group": self.group})

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger.info(self.group, extra={"end_group": self.group})


def _is_logging_git_command_execution(record: LogRecord) -> bool:
    return (record.module == 'cmd' and record.funcName == "execute" and record.msg.startswith(
        "git ")) or record.msg.startswith("git: ")


class FormatGroupItem(logging.Formatter):

    def format(self, record: LogRecord) -> str:
        pad = "   " * len(self._groups)
        if hasattr(record, "start_group") and record.start_group:
            self._groups.append(record.start_group)
            return click.style(f"{pad}> {record.msg}", fg="green")
        elif hasattr(record, "end_group") and record.end_group and record.end_group in self._groups:
            # Reverse the list to remove the last occurrence, remove it and reverse it back
            self._groups.reverse()
            self._groups.remove(record.end_group)
            self._groups.reverse()
            return ""

        record.msg = record.msg.replace('\n', '\\n')
        return click.style(f"{pad}{super().format(record)}", dim=True, fg=self._color_by_level(record))

    @property
    def _groups(self) -> list:
        if not hasattr(self, "_groups_"):
            self._groups_ = []
        return self._groups_

    def _color_by_level(self, record: LogRecord) -> str:
        if _is_logging_git_command_execution(record):
            return "bright_black"

        level = record.levelno

        if level == logging.DEBUG:
            return "bright_black"
        elif level == logging.INFO:
            return "bright_white"
        elif level == logging.WARNING:
            return "bright_yellow"
        elif level == logging.ERROR:
            return "bright_red"
        elif level == logging.CRITICAL:
            return "bright_red"
        else:
            return "bright_white"


class GitLogHandler(logging.StreamHandler):
    def acquire(self) -> None:
        super().acquire()

    def release(self) -> None:
        super().release()

    def filter(self, record: LogRecord) -> bool:
        if self.__is_git_command_that_can_be_ignored_becase_it_is_only_reading_data(record):
            return False
        return super().filter(record)

    def __is_git_command_that_can_be_ignored_becase_it_is_only_reading_data(self, record: LogRecord) -> bool:
        if not _is_logging_git_command_execution(record):
            return False

        return record.msg == "git version" or record.msg.startswith("git diff ") \
            or record.msg.startswith("git cat-file ")

    def handle(self, record: LogRecord) -> bool:
        return super().handle(record)

    def handleError(self, record: LogRecord) -> None:
        super().handleError(record)

    def emit(self, record: LogRecord) -> None:
        # check if the static function __format is set
        super().emit(record)

    @classmethod
    def log_group(cls, name: str) -> GroupContextManager:
        return GroupContextManager(name, get_logger())

    @classmethod
    def register(cls, logger: logging.Logger):
        handler = GitLogHandler(sys.stdout)
        handler.setFormatter(FormatGroupItem())

        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
