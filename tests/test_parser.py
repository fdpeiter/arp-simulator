# -*- coding: utf-8 -*-

from simulator.file_parser import FileParser
import unittest


class ParserTest(unittest.TestCase):

    def test_parse_size(self):
        nodes, routers = FileParser('test_entry.txt').parse_file()
        assert len(nodes) == 4
        assert len(routers) == 1


if __name__ == '__main__':
    unittest.main()