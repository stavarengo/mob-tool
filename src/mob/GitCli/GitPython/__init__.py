import logging
import os

os.environ["GIT_PYTHON_TRACE"] = "True"


def get_logger() -> logging.Logger:
    return logging.getLogger("git")


from mob.GitCli.GitPython.GitLogHandler import GitLogHandler

GitLogHandler.register(get_logger())
