import logging

__setup_logging = False


def setup_logging():
    global __setup_logging
    if __setup_logging:
        return
    __setup_logging = True

    from mobt.Logging.LogHandler import LogHandler
    from mobt.Logging.Filter import Filter
    from mobt.Logging.Formatter import Formatter

    handler = LogHandler()
    handler.setFormatter(Formatter())
    handler.addFilter(Filter())

    # from mobt import mob_logger
    logging.getLogger().addHandler(handler)


def set_log_level(level: int):
    logging.getLogger().setLevel(level)


def get_log_level():
    return logging.getLogger().level
