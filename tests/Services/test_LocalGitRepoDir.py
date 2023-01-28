import unittest
from unittest.mock import patch

from mob.Services.LocalGitRepoDir import LocalGitRepoDir, InvalidGitRepoDir


class TestLocalGitRepoDir(unittest.TestCase):
    @patch('os.path.exists', return_value=True)
    def test_valid_path_with_dot_git_folder(self, mock_exists):
        path = '/tmp'
        local_git_repo_dir = LocalGitRepoDir(path)
        self.assertEqual(path, local_git_repo_dir.path)

    @patch('os.path.exists', side_effect=lambda p: not p.endswith('/.git'))
    def test_valid_path_but_no_dot_git_folder(self, mock_exists):
        path = '/local/repo'
        with self.assertRaisesRegex(InvalidGitRepoDir, str(InvalidGitRepoDir.create(path))):
            LocalGitRepoDir(path)

    @patch('os.path.exists', return_value=False)
    def test_invalid_path(self, mock_exists):
        path = '/not/a/real/path'
        with self.assertRaisesRegex(InvalidGitRepoDir, str(InvalidGitRepoDir.create(path))):
            LocalGitRepoDir(path)

    @patch('os.path.exists', return_value=True)
    def test_is_immutable(self, mock_exists):
        local_git_repo_dir = LocalGitRepoDir("/path/to/existing/folder")
        with self.assertRaises(AttributeError):
            # noinspection PyDataclass
            local_git_repo_dir.path = "/another/path"
