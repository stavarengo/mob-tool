import logging
import sys


class LogHandler(logging.StreamHandler):
    def __init__(self):
        super().__init__(sys.stdout)

    def format(self, record: logging.LogRecord) -> str:
        msg = super().format(record)
        return msg
