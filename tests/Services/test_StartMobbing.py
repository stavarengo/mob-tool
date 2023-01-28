import unittest
from unittest.mock import MagicMock

from mob.GitWrapper.GitWrapper import GitWrapper
from mob.GitWrapper.GitWrapperAbstract import WorkingDirectoryNotClean
from mob.Services.StartMobbing import StartMobbing


class TestStartMobbing(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.git = MagicMock(spec=GitWrapper)
        self.git.is_dirty.return_value = False

        self.startMobbing = StartMobbing(self.git)

    def test_fail_if_repo_is_dirty(self):
        self.git.is_dirty.return_value = True
        with self.assertRaises(WorkingDirectoryNotClean):
            self.startMobbing.start()
