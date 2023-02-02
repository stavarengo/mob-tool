import unittest
from unittest.mock import MagicMock, patch

from mob.GitWrapper.GitWrapper import GitWrapper
from mob.GitWrapper.GitWrapperAbstract import WorkingDirectoryNotClean, LocalBranchIsAheadOfRemoteBranch
from mob.Services.BranchName import BranchName


class MagickMock:
    pass


class TestGitWrapperCheckout(unittest.TestCase):

    def test_checkout_clean_working_directory(self):
        with patch('git.Repo') as mock_repo:
            mock_repo.is_dirty.return_value = False
            git_wrapper = GitWrapper(mock_repo)
            git_wrapper.checkout(BranchName('branch'))
            mock_repo.assert_called_once()

    def test_checkout_working_directory_not_clean(self):
        with patch('git.Repo') as mock_repo:
            mock_repo.return_value.__is_dirty = MagicMock(return_value=True)
            git_wrapper = GitWrapper(mock_repo)
            with self.assertRaises(WorkingDirectoryNotClean):
                git_wrapper.checkout(BranchName('branch'))
            mock_repo.assert_called_once()

    def test_checkout_local_branch_ahead_of_remote(self):
        with patch('git.Repo') as mock_repo:
            mock_repo.return_value.__is_dirty = MagicMock(return_value=False)
            mock_repo.return_value.active_branch.is_ahead = MagicMock(return_value=True)
            git_wrapper = GitWrapper(mock_repo)
            with self.assertRaises(LocalBranchIsAheadOfRemoteBranch):
                git_wrapper.checkout(BranchName('branch'))
            mock_repo.assert_called_once()

    def test_checkout_local_branch_exists(self):
        with patch('git.Repo') as mock_repo:
            mock_repo.return_value.__is_dirty = MagicMock(return_value=False)
            mock_repo.return_value.active_branch.is_ahead = MagicMock(return_value=False)
            mock_repo.return_value.heads.__contains__ = MagicMock(return_value=True)
            git_wrapper = GitWrapper(mock_repo)
            with patch('builtins.open', mock_open(read_data='{"key": "value"}')) as mock_file:
                git_wrapper.checkout(BranchName('branch'))
                mock_file.assert_called_once_with('.mob.json', 'r')
                mock_repo.assert_called_once()

    def test_checkout_local_branch_does_not_exist(self):
        with patch('git.Repo') as mock_repo:
            mock_repo.return_value.__is_dirty = MagicMock(return_value=False)
            mock_repo.return_value.active_branch.is_ahead = MagicMock(return_value=False)
            mock_repo.return_value.heads.__contains__ = MagicMock(return_value=False)
            git_wrapper = GitWrapper(mock_repo)
            with patch('builtins.open', mock_open(read_data='{"key": "value"}')) as mock_file:
                git_wrapper.checkout(BranchName('branch'))
                mock_file.assert_not_called()
                mock_repo.assert_called_once()
