# -*- coding: utf-8 -*-
from simulator.network.arp_packet import *
from simulator.network.echo_packet import *
from simulator.network.router import Router


class Node:
    def __init__(self, name, mac, ip_address, gateway, gateway_port):
        assert isinstance(name, str), "Name must be an string"
        assert isinstance(mac, netaddr.EUI), "Invalid MAC Address"
        assert isinstance(ip_address, netaddr.IPNetwork), "Invalid IP/Prefix"
        assert isinstance(gateway, Router), "Gateway must be an valid Router object"
        assert isinstance(gateway_port, int), "Gateway port must be an int"
        self.name = name
        self.mac = mac
        self.ip_address = ip_address
        self.gateway = gateway
        self.gateway_port = gateway_port
        self.arp_table = {}

    def arp_request(self, destination):
        return ArpRequest(self.name, self.mac, self.ip_address, destination)

    def arp_reply(self, request):
        if request.dst_mac == self.mac:
            return ArpReply(self.name, self.mac, self.ip_address, request.src_host, request.src_mac, request.ip_address)
        else:
            return None

    def arp_add_entry(self, reply):
        if reply.dst_host == self.name:
            self.arp_table[reply.src_address] = reply.src_mac

    def echo_request(self, dst_host, dst_mac, dst_address, ttl=8):
        result = []
        if dst_mac not in self.arp_table:
            if dst_address not in self.ip_address:
                result.append(self.arp_request(self.gateway))
            else:
                result.append(self.arp_request(dst_address))
        if dst_address not in self.ip_address:
            result.append(EchoRequest(self.name, self.mac, self.ip_address.ip,
                                      self.gateway.name, self.gateway.ports[self.gateway_port].mac, dst_address,
                                      ttl))
        else:
            result.append(EchoRequest(self.name, self.mac, self.ip_address.ip,
                                      dst_host, dst_mac, dst_address,
                                      ttl))
        return result

    def echo_reply(self, dst_host, dst_address):
        reply = EchoReply(self.name, dst_host, self.ip_address.ip, dst_address, 8)
        return reply
