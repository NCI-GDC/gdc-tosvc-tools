#!/usr/bin/env python

import tempfile
import unittest
from textwrap import dedent

from click.testing import CliRunner

from gdc_tosvc_tools.cli import extract_wig_size as MOD


@unittest.skip("Skip for now")
class ThisTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

        self.wig_data = dedent(
            """
            """
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_trim_wig_file(self):
        MOD.trim_wig_file()

    def test_trim_size_file(self):
        MOD.trim_size_file()

    def test_entrypoint(self):
        runner = CliRunner()
        runner.invoke(MOD.main)


if __name__ == "__main__":
    unittest.main()

# __END__
