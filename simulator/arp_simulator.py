# -*- coding: utf-8 -*-
from simulator.file_parser import FileParser
from simulator.network.arp_packet import ArpReply, ArpRequest
from simulator.network.echo_packet import EchoReply, EchoRequest


class Simulator:
    def __init__(self, filename):
        self.nodes, self.routers = FileParser(filename).parse_file()

    def connect(self, node_list):
        for i in range(0, len(node_list)-1):
            source, destination = None, None
            for node in self.nodes:
                if node.name == node_list[i]:
                    source = node
                    break
            if source is None:
                raise Exception("Node {name} not found".format(name=node_list[i]))
            for node in self.nodes:
                if node.name == node_list[i+1]:
                    destination = node
                    break
            if destination is None:
                raise Exception("Node {name} not found".format(name=node_list[i+1]))
            commands = source.echo_request(destination.name, destination.ip_address.ip)
            while commands:
                command = commands.pop(0)
                if command is None: break
                print(command)
                if isinstance(command, ArpRequest):
                    commands.insert(0, self.parse_arp_request(command))
                elif isinstance(command, ArpReply):
                    self.parse_arp_reply(command)
                elif isinstance(command, EchoRequest):
                    commands.insert(0, self.parse_echo_request(command))
                elif isinstance(command, EchoReply):
                    commands.insert(0, self.parse_echo_reply(command))

    def parse_arp_request(self, command):
        for node in self.nodes:
            if node.ip_address.ip == command.dst_address:
                return node.arp_reply(command.host)
        for router in self.routers:
            for port in router.ports:
                if port.ip_address.ip == command.dst_address:
                    return router.arp_reply(command.dst_address, command.host)

    def parse_arp_reply(self, command):
        for node in self.nodes:
            if node.name == command.dst_host:
                node.add_arp_entry(command)

    def parse_echo_request(self, command):
        if command.ttl == 0:
            return None
        for node in self.nodes:
            if node.name == command.dst_host:
                return node.echo_reply(command.src_host, command.src_address)
        for router in self.routers:
            if router.name == command.dst_host:
                return router.echo_request(command.src_address, command.dst_host, command.dst_address, command.ttl)

    def parse_echo_reply(self, command):
        pass


sim = Simulator('/Users/Peiter/PycharmProjects/arp-simulator/tests/test_entry.txt')
sim.connect(['n1','n2','n3'])







