# -*- coding: utf-8 -*-
import netaddr

from simulator.network.arp_packet import ArpRequest, ArpReply
from simulator.network.echo_packet import EchoRequest, EchoReply
from simulator.network.router_table import RouterTable


class RouterPort:
    def __init__(self, mac, ip_address):
        self.mac = mac
        self.ip_address = ip_address

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
    def ip_address(self):
        return self.__ip_address

    @ip_address.setter
    def ip_address(self, ip):
        if not isinstance(ip, netaddr.IPNetwork):
            raise TypeError("Invalid IP/Prefix, must be in the format IP_ADDRESS/CIDR")
        else:
            self.__ip_address = ip


class Router:
    def __init__(self, name, ports, router_table):
        self.name = name
        self.ports = ports
        self.router_table = router_table
        self.arp_table = {}

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