import os

os.environ["GIT_PYTHON_TRACE"] = "True"

import logging
import sys
from mob.GitCli.GitPython.GitLogHandler import FormatGroupItem


def git_logger() -> logging.Logger:
    return logging.getLogger("git")


from mob.GitCli.GitPython.GitLogHandler import GitLogHandler

handler = GitLogHandler(sys.stdout)
handler.setFormatter(FormatGroupItem())

logger = git_logger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)
