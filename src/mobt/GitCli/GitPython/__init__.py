import logging

# os.environ["GIT_PYTHON_TRACE"] = "True"

_logger = logging.getLogger(__name__)


def git_logger() -> logging.Logger:
    return _logger
