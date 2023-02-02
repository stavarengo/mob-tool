import logging
import os

os.environ["GIT_PYTHON_TRACE"] = "True"
gitpython_logger = logging.getLogger("git")
gitpython_logger.setLevel(logging.INFO)
gitpython_logger.addHandler(logging.StreamHandler())
