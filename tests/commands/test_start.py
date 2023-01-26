import unittest

from click.testing import CliRunner

from mob.commands import start


class TestStartCommand(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_start_new_session(self):
        result = self.runner.invoke(start, ['new-session'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, 'Started: new-session\n')

    def test_branch_name_not_provided(self):
        result = self.runner.invoke(start, [])
        self.assertEqual(result.exit_code, 2)
        self.assertIn("Error: Missing argument 'BRANCH_NAME'.", result.output)
