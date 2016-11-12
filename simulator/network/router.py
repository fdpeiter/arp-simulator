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
        self.name = router.name
        self.mac = mac
        self.ip_address = ip_address
        self.connected = connected

    def arp_request(self, dst_address):
        request = ArpRequest(self.mac, self.ip_address.ip, None, dst_address)
        self.router.process_request(self, self.router, request)

    def arp_reply(self, request):
        self.router.add_arp_table(request.src_address, request.src_mac)
        reply = ArpReply(self.mac, self.ip_address.ip, request.src_mac, request.src_address)
        self.router.process_request(self, self.router, reply)

    def echo_request(self, dst_address, request):
        if dst_address not in self.router.arp_table:
            self.arp_request(dst_address)
        request.src_mac = self.mac
        request.dst_mac = self.router.arp_table[dst_address]
        request.ttl -= 1
        for connected in self.connected:
            if dst_address == connected.ip_address.ip:
                if isinstance(connected, RouterPort):
                    connected.router.process_request(connected, connected.router, request)
                else:
                    self.router.process_request(self, self.router, request)

    def echo_reply(self, dst_address, request):
        request.ttl -= 1
        request.src_mac = self.mac
        request.dst_mac = self.router.arp_table[dst_address]
        for connected in self.connected:
            if dst_address == connected.ip_address.ip:
                if isinstance(connected, RouterPort):
                    connected.router.process_request(connected, connected.router, request)
                else:
                    self.router.process_request(self, self.router, request)

    def process_request(self, source, request):
        return self.router.process_request(self, source, request)


class Router:
    def __init__(self, controller, name, ports, router_table):
        assert isinstance(name, str), "Name must be an string"
        assert all(isinstance(port, RouterPort) for port in ports), "All ports must be in the correct format"
        assert all(isinstance(item, RouterTable) for item in router_table), "Router table must be an list of router_table items"
        assert all(item > len(self.ports) for item in router_table), "All ports must be an integer smaller than the router num_ports"
        self.controller = controller
        self.name = name
        self.ports = ports
        self.router_table = router_table
        self.arp_table = {}

    def process_arp_packet(self, port, source, request):
        if isinstance(request, ArpRequest):
            if request.dst_address == port.ip_address.ip:
                source.add_arp_table(port.ip_address.ip, port.mac)
                self.process_request(port, self, port.arp_reply(request))
            else:
                for connected in port.connected:
                    if request.dst_address == connected.ip_address.ip:
                        source.add_arp_table(connected.ip_address.ip, connected.mac)
                        self.add_arp_table(connected.ip_address.ip, connected.mac)
                        reply = connected.arp_reply(request)
                        self.process_request(port, self, reply)
                        break

    def process_echo_packet(self, port, source, request):
        if isinstance(request, EchoRequest):
            if request.dst_address in port.ip_address:
                for connected in port.connected:
                    if connected.ip_address.ip == request.dst_address:
                        self.process_request(port, self, connected.echo_reply(request))
            else:
                for table in self.router_table:
                    if request.dst_address in table.net_destination:
                        port = self.ports[table.port]
                        if table.next_hop == netaddr.IPAddress('0.0.0.0'):
                            for connected in port.connected:
                                if connected.ip_address.ip == request.dst_address:
                                    port.echo_request(request.dst_address, request)
                                    return 1
                        else:
                            port.echo_request(table.next_hop, request)
                            break
        if isinstance(request, EchoReply):
            if request.dst_address in port.ip_address:
                for connected in port.connected:
                    if connected.ip_address.ip == request.dst_address:
                        return 1
            else:
                for table in self.router_table:
                    if request.dst_address in table.net_destination:
                        port = self.ports[table.port]
                        if table.next_hop == netaddr.IPAddress('0.0.0.0'):
                            for connected in port.connected:
                                if connected.ip_address.ip == request.dst_address:
                                    port.echo_reply(request.dst_address, request)
                                    return 1
                        else:
                            port.echo_reply(table.next_hop, request)
                            break

    def process_request(self, port, source, request):
        if request is None:
            return
        self.controller.parse_command(request)
        if isinstance(request, ArpReply) or isinstance(request, ArpRequest):
            self.process_arp_packet(port, source, request)
        else:
            self.process_echo_packet(port, source, request)

    def add_arp_table(self, address, mac):
        self.arp_table[address] = mac