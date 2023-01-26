import unittest

from click.testing import CliRunner

from mob.commands import done


class TestStartCommand(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_done(self):
        result = self.runner.invoke(done)
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, 'done\n')
