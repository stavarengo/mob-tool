import logging


class Filter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.name != 'git.cmd'
