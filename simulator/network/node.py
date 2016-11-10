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
        self.gateway.process_request(ArpRequest(self.mac, self.ip_address, None, dst_address))

    def arp_reply(self, request):
        self.add_arp_table(request.src_ip, request.src_mac)
        return ArpReply(self.mac, self.ip_address, request.src_mac, request.src_ip)

    def add_arp_table(self, address, mac):
        self.arp_table[address] = mac

    def echo_request(self, dst_address):
        if dst_address not in self.arp_table:
            self.gateway.process_request(self.arp_request(dst_address))
        self.gateway.process_request(EchoRequest(self.mac, self.ip_address,
                                                 self.arp_table[dst_address], dst_address, 8))

    def echo_reply(self, request):
        self.arp_table[request.src_address] = request.src_mac
        self.gateway.process_request(EchoReply(self.mac, self.ip_address,
                                               self.arp_table[request.src_address], request.src_address, 8))