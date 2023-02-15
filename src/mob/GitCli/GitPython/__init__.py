import logging
import os

os.environ["GIT_PYTHON_TRACE"] = "True"


def git_logger() -> logging.Logger:
    return logging.getLogger("git")


from mob.GitCli.GitPython.GitLogHandler import GitLogHandler

GitLogHandler.register(git_logger())
