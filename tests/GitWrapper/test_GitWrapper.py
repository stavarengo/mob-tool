import unittest
from unittest.mock import MagicMock

from git import Repo

from mob.GitWrapper.GitWrapper import GitWrapper


class TestGitWrapper(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()

        self.repo = MagicMock(spec=Repo)
        self.git = GitWrapper(self.repo)

    def test_is_dirty_returns_false(self):
        self.repo.is_dirty.return_value = False
        self.assertFalse(self.git.is_dirty())
        self.repo.is_dirty.assert_called()

    def test_is_dirty_returns_true(self):
        self.repo.is_dirty.return_value = True
        self.assertTrue(self.git.is_dirty())
        self.repo.is_dirty.assert_called()
