# -*- coding: utf-8 -*-
import netaddr


class Router:
    def __init__(self, name, num_ports, mac_ips):
        self.name = name
        self.num_ports = num_ports
        self.mac_ips = mac_ips

    @property
    def name(self):
        return self.name

    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise TypeError("Name must be an string")

    @property
    def num_ports(self):
        return self.num_ports

    @num_ports.setter
    def num_ports(self, num_ports):
        if not isinstance(num_ports, int):
            raise TypeError("Num ports must be an valid int")
        elif num_ports < 1:
            raise Exception("Num ports must be bigger than 0")

    @property
    def mac_ips(self):
        return self.mac_ips

    @mac_ips.setter
    def mac_ips(self, mac_ips):
        if not len(mac_ips) == self.num_ports:
            raise Exception("The number of MAC/IPs doesn't match the number of ports")
        else:
            for mac, ip_address in mac_ips:
                if not isinstance(mac, netaddr.EUI):
                    raise TypeError("Invalid MAC Address")
                elif not isinstance(ip_address, netaddr.IPNetwork):
                    raise TypeError("Invalid IP/Prefix, must be in the format IP_ADDRESS/CIDR")
