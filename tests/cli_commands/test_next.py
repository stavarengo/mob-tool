import unittest

from click.testing import CliRunner

from mob.cli_commands import next


class TestStartCommand(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_done(self):
        result = self.runner.invoke(next)
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, 'next\n')
