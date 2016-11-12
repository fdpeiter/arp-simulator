# -*- coding: utf-8 -*-
from simulator.network.arp_packet import *
from simulator.network.echo_packet import *
from simulator.network.router import RouterPort


class Node:
    def __init__(self, name, mac, ip_address, gateway):
        assert isinstance(name, str), "Name must be an string"
        assert isinstance(mac,netaddr.EUI), "Invalid MAC Address"
        assert isinstance(ip_address, netaddr.IPNetwork), "Invalid IP/Prefix"
        isinstance(gateway, RouterPort), "Invalid IP Address"
        self.name = name
        self.mac = mac
        self.ip_address = ip_address
        self.gateway = gateway
        self.arp_table = {}

    def arp_request(self, dst_address):
        self.gateway.process_request(self, ArpRequest(self.mac, self.ip_address.ip, None, dst_address))

    def arp_reply(self, request):
        self.add_arp_table(request.src_address, request.src_mac)
        return ArpReply(self.mac, self.ip_address.ip, request.src_mac, request.src_address)

    def add_arp_table(self, address, mac):
        self.arp_table[address] = mac

    def echo_request(self, dst_address):
        if dst_address not in self.arp_table:
            if dst_address not in self.ip_address:
                self.gateway.process_request(self, self.arp_request(self.gateway.ip_address.ip))
            else:
                self.gateway.process_request(self, self.arp_request(dst_address))
        if dst_address not in self.ip_address:
            request = EchoRequest(self.mac, self.ip_address.ip,
                                 self.arp_table[self.gateway.ip_address.ip],
                                 dst_address, 8)
        else:
            request = EchoRequest(self.mac, self.ip_address.ip,
                                  self.arp_table[dst_address],
                                  dst_address, 8)
        self.gateway.process_request(self, request)


    def echo_reply(self, request):
        if request.src_address not in self.ip_address:
            request = EchoReply(self.mac, self.ip_address.ip,
                                self.arp_table[self.gateway.ip_address.ip],
                                request.src_address, 8)
        else:
            request = EchoReply(self.mac, self.ip_address.ip,
                                self.arp_table[request.src_address],
                                request.src_address, 8)
        self.gateway.process_request(self, request)