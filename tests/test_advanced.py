# -*- coding: utf-8 -*-

from .context import simulator

import unittest


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def test_thoughts(self):
        simulator.hmm()


if __name__ == '__main__':
    unittest.main()