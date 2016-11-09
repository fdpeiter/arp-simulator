# -*- coding: utf-8 -*-
import os
import netaddr

from simulator.network.node import Node
from simulator.network.router import Router
from simulator.network.router import RouterPort
from simulator.network.router_table import RouterTable


class FileParser:
    def __init__(self, filename):
        assert isinstance(filename, str)
        assert os.path.isfile(filename)
        self.filename = filename
        self.nodes = []
        self.routers = []
        self.name_table = {}

    def parse_file(self):
        with open(self.filename, 'r') as f:
            data = f.read()
            if "#NODE" not in data:
                raise Exception("Missing node header")
            elif "#ROUTER" not in data:
                raise Exception("Missing router header")
            elif "#ROUTERTABLE" not in data:
                raise Exception("Missing router table header")
            else:
                nodes_str = data.split("#NODE\n")[1].split("#ROUTER\n")[0]
                routers_str = data.split("#ROUTER\n")[1].split("#ROUTERTABLE\n")[0]
                routing_tables_str = data.split("#ROUTERTABLE\n")[1]
                self.parse_nodes(nodes_str)
                self.parse_routers(routers_str)
                self.parse_routing_tables(routing_tables_str)
                return self.nodes, self.routers, self.name_table

    def parse_nodes(self, nodes_str):
        # Remove valores vazios da list
        nodes = list(filter(None, nodes_str.split("\n")))
        for node_line in nodes:
            node_info = node_line.split(",")
            node_name = node_info[0]
            node_mac = netaddr.EUI(node_info[1])
            self.name_table[node_mac] = node_name
            node_ip = netaddr.IPNetwork(node_info[2])
            node_gateway = netaddr.IPAddress(node_info[3])
            tmp_node = Node(node_name, node_mac, node_ip, node_gateway)
            self.nodes.append(tmp_node)

    def parse_routers(self, routers_str):
        # Remove valores vazios da lista
        routers = list(filter(None, routers_str.split("\n")))
        for router_line in routers:
            router_info = router_line.split(",")
            router_name = router_info[0]
            router_ports = []
            for i in range(2, len(router_info), 2):
                port = RouterPort(netaddr.EUI(router_info[i]), netaddr.IPNetwork(router_info[i+1]))
                self.name_table[router_info[i]] = router_name
                router_ports.append(port)
            tmp_router = Router(router_name, router_ports, [])
            self.routers.append(tmp_router)

    def parse_routing_tables(self, routing_tables_str):
        # Remove valores vazios da lista
        routing_tables = list(filter(None, routing_tables_str.split("\n")))
        for routing_table_line in routing_tables:
            table_info = routing_table_line.split(",")
            for router_entry in self.routers:
                if router_entry.name == table_info[0]:
                    tmp_router_table = RouterTable(netaddr.IPNetwork(table_info[1]),
                                                   netaddr.IPAddress(table_info[2]),
                                                   int(table_info[3]))
                    router_entry.router_table.append(tmp_router_table)
