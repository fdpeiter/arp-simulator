# -*- coding: utf-8 -*-
from simulator.network.arp_packet import *
from simulator.network.echo_packet import *


class Node:
    def __init__(self, name, mac, ip_address, gateway):
        self.name = name
        self.mac = mac
        self.ip_address = ip_address
        self.gateway = gateway
        self.arp_table = {}

    def arp_request(self, destination):
        request = ArpRequest(self.name, self.ip_address.ip, destination)
        return request

    def arp_reply(self, destination):
        reply = ArpReply(self.name, destination, self.ip_address.ip, self.mac)
        return reply

    def arp_add_entry(self, reply):
        if reply.dst_host == self.name:
            self.arp_table[reply.src_address] = reply.src_mac

    def echo_request(self, dst_host, dst_address, ttl=8):
        result = []
        if dst_host not in self.arp_table:
            if dst_address not in self.ip_address:
                result.append(self.arp_request(self.gateway))
            else:
                result.append(self.arp_request(dst_address))
        if dst_address not in self.ip_address:
            result.append(EchoRequest(self.arp_table[self.gateway], self.name, dst_host,
                                      self.ip_address.ip, dst_address, ttl))
        else:
            result.append(EchoRequest(self.arp_table[dst_address], self.name, dst_host,
                                      self.ip_address.ip, dst_address, ttl))
        return result

    def echo_reply(self, dst_host, dst_address):
        reply = EchoReply(self.name, dst_host, self.ip_address.ip, dst_address, 8)
        return reply

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
    def mac(self):
        return self.__mac

    @mac.setter
    def mac(self, mac):
        if not isinstance(mac,netaddr.EUI):
            raise TypeError("Invalid MAC Address")
        else:
            self.__mac = mac

    @property
    def ip_address(self):
        return self.__ip_address

    @ip_address.setter
    def ip_address(self, ip_address):
        if not isinstance(ip_address, netaddr.IPNetwork):
            raise TypeError("Invalid IP/Prefix")
        else:
            self.__ip_address = ip_address

    @property
    def gateway(self):
        return self.__gateway

    @gateway.setter
    def gateway(self, gateway):
        if not isinstance(gateway, netaddr.IPAddress):
            raise TypeError("Invalid IP Address")
        else:
            self.__gateway = gateway
