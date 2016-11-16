# -*- coding: utf-8 -*-
import sys
from simulator.file_parser import FileParser
from simulator.network.arp_packet import ArpReply, ArpRequest
from simulator.network.echo_packet import EchoReply, EchoRequest


class Simulator:
    def __init__(self, filename):
        parser = FileParser(self, filename)
        self.routers, self.mac_dict = parser.parse_file()

    def find_node(self, node_name):
        for router in self.routers:
            for port in router.ports:
                for connected in port.connected:
                    if connected.name == node_name:
                        return connected
        return None

    def connect(self, node_list):
        for i in range(0, len(node_list)-1):
            source = self.find_node(node_list[i])
            destination = self.find_node(node_list[i+1])
            if source is None:
                raise Exception("Node {name} not found".format(name=node_list[i]))
            if destination is None:
                raise Exception("Node {name} not found".format(name=node_list[i+1]))
            source.echo_request(destination.ip_address.ip)

    def parse_command(self, command):
        if isinstance(command, EchoRequest):
            if command.ttl == 0:
                exit(1)
        result = command.__str__().replace("src_host", self.mac_dict[command.src_mac])
        if command.dst_mac is not None:
            result = result.__str__().replace("dst_host", self.mac_dict[command.dst_mac])
        print(result)

sim = Simulator(sys.argv[1])
sim.connect(sys.argv[2:])







