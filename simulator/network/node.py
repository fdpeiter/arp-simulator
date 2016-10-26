# -*- coding: utf-8 -*-
import netaddr


class Node:
    def __init__(self, name, mac, ip_address, gateway):
        self.name = name
        self.mac = mac
        self.ip_address = ip_address
        self.gateway = gateway

    @property
    def name(self):
        return self.name

    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise TypeError("Name must be an string")

    @property
    def mac(self):
        return self.mac

    @mac.setter
    def mac(self, mac):
        if not isinstance(mac, netaddr.EUI):
            raise TypeError("Invalid MAC Address")

    @property
    def ip_address(self):
        return self.ip_address

    @ip_address.setter
    def ip_address(self, ip_address):
        if not isinstance(ip_address, netaddr.IPNetwork):
            raise TypeError("Invalid IP/Prefix, must be in the format IP_ADDRESS/CIDR")

    @property
    def gateway(self):
        return self.gateway

    @gateway.setter
    def gateway(self, gateway):
        if not isinstance(gateway, netaddr.IPAddress):
            raise TypeError("Invalid IP Address")
