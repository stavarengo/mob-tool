import logging
import sys


class LogHandler(logging.StreamHandler):
    def __init__(self):
        super().__init__(sys.stdout)

    def format(self, record: logging.LogRecord) -> str:
        msg = super().format(record)
        # write the log level in the beginning of the message
        msg = f"{record.levelname}: {msg}"
        return msg
