# -*- coding: utf-8 -*-
from simulator.file_parser import FileParser


class Simulator:
    def __init__(self, filename):
        self.routers, self.nodes = FileParser(filename).parse_file()

    def connect(self, node_list):
        for i in range(0, len(node_list)-1):
            node = node_list[i]




