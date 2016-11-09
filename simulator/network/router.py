# -*- coding: utf-8 -*-
import netaddr

from simulator.network.arp_packet import ArpRequest, ArpReply
from simulator.network.echo_packet import EchoRequest, EchoReply
from simulator.network.router_table import RouterTable
from simulator.network.router_port import RouterPort


class Router:
    def __init__(self, name, ports, router_tables):
        assert isinstance(name, str), "Name must be an string"
        assert all (isinstance(port, RouterPort) for port in ports), "Each ports must be an valid RouterPort objects"
        assert all (isinstance(rt, RouterTable) for rt in router_tables), \
            "Each router table item must be an valid RouterTable object"
        self.name = name
        self.ports = ports
        self.router_tables = router_tables
        self.arp_table = {}

    def arp_request(self, destination):
        for table in self.router_tables:
            if destination in table.net_destination:
                if table.next_hop != netaddr.IPAddress('0.0.0.0'):
                    destination = table.next_hop
                request = ArpRequest(self.name, self.ports[table.port].ip_address.ip, destination)
                return request
        return None

    def arp_reply(self, src_ip, destination):
        for port in self.ports:
            if port.ip_address.ip == src_ip:
                return ArpReply(self.name, destination, port.ip_address.ip, port.mac)
        return None

    def arp_add_entry(self, reply):
        if reply.dst_host == self.name:
            self.arp_table[reply.src_address] = reply.src_mac

    def echo_request(self, src_address, dst_host, dst_address, ttl):
        result = []
        ttl -= 1
        if dst_host not in self.arp_table:
            result.append(self.arp_request(dst_address))
        result.append(EchoRequest(self.name, dst_host, src_address, dst_address, ttl))
        return result

    def echo_reply(self, src_address, dst_host, dst_address, ttl):
        ttl -= 1
        reply = EchoReply(self.name, dst_host, src_address, dst_address, ttl)
        return reply