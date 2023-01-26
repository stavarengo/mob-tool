import unittest

from click.testing import CliRunner

from mob.commands.cli import cli


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_with_data(self):
        data = [
            (['start', 'branch_name'], 'Started: branch_name\n'),
            (['done'], 'done\n'),
            (['next'], 'next\n'),
        ]
        for cmd, expected_output in data:
            with self.subTest(cmd=cmd, expected_output=expected_output):
                result = self.runner.invoke(cli, cmd)
                self.assertEqual(result.exit_code, 0)
                self.assertEqual(result.output, expected_output)
