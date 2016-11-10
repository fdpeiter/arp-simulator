# -*- coding: utf-8 -*-
import netaddr

from simulator.network.arp_packet import ArpRequest, ArpReply
from simulator.network.echo_packet import EchoRequest, EchoReply
from simulator.network.router_table import RouterTable


class RouterPort:
    def __init__(self, router, mac, ip_address, connected):
        assert isinstance(router, Router), "Port router must be an valid Router object"
        assert isinstance(mac, netaddr.EUI), "Invalid MAC Address"
        assert isinstance(ip_address, netaddr.IPNetwork), "Invalid IP/Prefix, must be in the format IP_ADDRESS/CIDR"
        self.router = router
        self.mac = mac
        self.ip_address = ip_address
        self.connected = connected

    def arp_reply(self, request):
        return ArpReply(self.mac, self.ip_address, request.src_mac, request.src_ip)

    def process_request(self, node, request):
        return self.router.process_request(self, node, request)


class Router:
    def __init__(self, name, ports, router_table):
        assert isinstance(name, str), "Name must be an string"
        assert all(isinstance(port, RouterPort) for port in ports), "All ports must be in the correct format"
        assert all(isinstance(item, RouterTable) for item in router_table), "Router table must be an list of router_table items"
        assert all(item > len(self.ports) for item in router_table), "All ports must be an integer smaller than the router num_ports"
        self.name = name
        self.ports = ports
        self.router_table = router_table
        self.arp_table = {}

    def process_arp_request(self, port, node, request):
        commands = []
        if isinstance(request, ArpRequest):
            if request.dst_address == port.ip_address:
                commands.append(request.__str__().format(host=node.name))
                node.add_arp_table(port.ip_address, port.mac)
                commands.append(port.arp_reply(request).__str__().format(src_host=self.name,
                                                                  dst_host=node.name))

        if isinstance(request, ArpReply):

    def process_echo_request(self, port, node, request):
        pass

    def process_request(self, port, node, request):
        if isinstance(request, ArpReply) or isinstance(request, ArpRequest):
            self.process_arp_request(port, node, request)
        else:
            self.process_echo_request(port, node, request)

    def arp_request(self, destination):
        for table in self.router_table:
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