# -*- coding: utf-8 -*-
import netaddr


class RouterTable:
    def __init__(self, net_destination, next_hop, port):
        self.net_destination = net_destination
        self.next_hop = next_hop
        self.port = port

    @property
    def net_destination(self):
        return self.__net_destination

    @net_destination.setter
    def net_destination(self, net_destination):
        if not isinstance(net_destination, netaddr.IPNetwork):
            raise TypeError("Invalid NET_ADDRESS/Prefix, must be in the format NET_ADDRESS/CIDR")
        else:
            self.__net_destination = net_destination

    @property
    def next_hop(self):
        return self.__next_hop

    @next_hop.setter
    def next_hop(self, next_hop):
        if not isinstance(next_hop, netaddr.IPAddress):
            raise TypeError("The next_hop must be an valid IP_ADDRESS")
        else:
            self.__next_hop = next_hop

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, port):
        if not isinstance(port, int):
            raise TypeError("Port number must be an valid int")
        elif not port >= 0:
            raise Exception("Port number must be an positive int")
        else:
            self.__port = port
