import logging

# os.environ["GIT_PYTHON_TRACE"] = "True"

_logger = logging.getLogger(__name__)


def git_logger() -> logging.Logger:
    return _logger


_log_undoing_all_git_commands = False


def log_undoing_all_git_commands() -> None:
    global _log_undoing_all_git_commands
    if not _log_undoing_all_git_commands:
        _log_undoing_all_git_commands = True
        git_logger().warning("Undoing all Git commands")
