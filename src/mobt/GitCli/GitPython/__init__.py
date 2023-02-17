import logging
import os

os.environ["GIT_PYTHON_TRACE"] = "True"

_git_logger = logging.getLogger("git")


def git_logger() -> logging.Logger:
    return _git_logger
