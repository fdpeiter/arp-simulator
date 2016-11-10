# -*- coding: utf-8 -*-
import netaddr


class RouterTable:
    def __init__(self, net_destination, next_hop, port):
        assert isinstance(net_destination, netaddr.IPNetwork),\
            "Invalid NET_ADDRESS/Prefix, must be in the format NET_ADDRESS/CIDR"
        assert isinstance(next_hop, netaddr.IPAddress), "The next_hop must be an valid IP_ADDRESS"
        assert isinstance(port, int), "Port number must be an valid int"
        assert port >= 0, "Port number must be an positive int"
        self.net_destination = net_destination
        self.next_hop = next_hop
        self.port = port