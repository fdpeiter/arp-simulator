# -*- coding: utf-8 -*-
import netaddr
from simulator.network.router_table import RouterTable


class Router:
    def __init__(self, name, num_ports, mac_ips, router_table):
        assert isinstance(name, str)
        assert isinstance(num_ports, int)
        assert len(mac_ips) == num_ports
        for mac, ip_addr in mac_ips:
            assert isinstance(mac, netaddr.EUI)
            assert isinstance(ip_addr, netaddr.IPNetwork)
        assert all(isinstance(item, RouterTable) for item in router_table)
        assert all(item.port > num_ports for item in router_table)
        self.name = name
        self.num_ports = num_ports
        self.mac_ips = mac_ips
        self.router_table = router_table