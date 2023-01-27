import unittest

from mob.services.branch_name import BranchName


class TestBranchName(unittest.TestCase):
    def test_branch_name(self):
        test_cases = [
            ("valid-branch-name", True),
            ("invalid branch name", False),
            ("branch_name", True),
            ("", False),
        ]

        for name, valid in test_cases:
            with self.subTest(name=name):
                if valid:
                    branch_name = BranchName(name)
                    self.assertEqual(name, branch_name.branch_name)
                else:
                    self.assertRaises(ValueError, BranchName, name)

    def test_comparison(self):
        test_cases = [
            ("branch_name", "branch_name", True),
            ("branch_NAME", "branch_name", False),
            ("branch_name", "diff-name", False),
        ]

        for name1, name2, is_eq in test_cases:
            with self.subTest(msg=f'{name1}={name2}'):
                if is_eq:
                    self.assertEqual(BranchName(name1), BranchName(name2))
                else:
                    self.assertNotEqual(BranchName(name1), BranchName(name2))
