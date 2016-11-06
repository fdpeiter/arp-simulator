# -*- coding: utf-8 -*-
import netaddr
from simulator.network.router_table import RouterTable


class RouterPort:
    def __init__(self, mac, ip):
        self.mac = mac
        self.ip = ip

    @property
    def mac(self):
        return self.__mac

    @mac.setter
    def mac(self, mac):
        if not isinstance(mac, netaddr.EUI):
            raise TypeError("Invalid MAC Address")
        else:
            self.__mac = mac

    @property
    def ip(self):
        return self.__ip

    @ip.setter
    def ip(self, ip):
        if not isinstance(ip, netaddr.IPNetwork):
            raise TypeError("Invalid IP/Prefix, must be in the format IP_ADDRESS/CIDR")
        else:
            self.__ip = ip


class Router:
    def __init__(self, name, ports, router_table):
        self.name = name
        self.ports = ports
        self.router_table = router_table

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise TypeError("Name must be an string")
        else:
            self.__name = name

    @property
    def ports(self):
        return self.__ports

    @ports.setter
    def ports(self, ports):
        if not all (isinstance(port, RouterPort) for port in ports):
            raise TypeError("All ports must be in the correct format")
        else:
            self.__ports = ports

    @property
    def router_table(self):
        return self.__router_table

    @router_table.setter
    def router_table(self, router_table):
        if not all(isinstance(item, RouterTable) for item in router_table):
            raise TypeError("Router table must be an list of router_table items")
        elif not all(item > len(self.ports) for item in router_table):
            raise Exception("All ports must be an integer smaller than the router num_ports")
        else:
            self.__router_table = router_table