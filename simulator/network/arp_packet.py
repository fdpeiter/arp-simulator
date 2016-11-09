# -*- coding: utf-8 -*-
import netaddr


class ArpRequest:
    def __init__(self, src_host, src_mac, src_address, dst_address):
        assert isinstance(src_host, str)
        assert isinstance(src_mac, netaddr.EUI)
        assert isinstance(src_address, netaddr.IPAddress)
        assert isinstance(dst_address, netaddr.IPAddress)
        self.src_host = src_host
        self.src_mac = src_mac
        self.src_address = src_address
        self.dst_address = dst_address

    def __str__(self):
        return "{host} box {host} : ARP - Who has {dst}? Tell {src};".format(host=self.src_host, src=self.src_address,
                                                                             dst=self.dst_address)


class ArpReply:
    def __init__(self, src_host, src_address, src_mac, dst_host, dst_address, dst_mac):
        assert isinstance(src_host, str)
        assert isinstance(dst_host, str)
        assert isinstance(src_address, netaddr.IPAddress)
        assert isinstance(src_mac, netaddr.EUI)
        assert isinstance(dst_address, netaddr.IPAddress)
        assert isinstance(dst_mac, netaddr.EUI)
        self.src_host = src_host
        self.dst_host = dst_host
        self.src_address = src_address
        self.src_mac = src_mac
        self.dst_address = dst_address
        self.dst_mac = dst_mac

    def __str__(self):
        return " {src_host} => {dst_host} : ARP - {ip} is at {mac};".format(src_host=self.src_host,
                                                                            dst_host=self.dst_host,
                                                                            ip=self.src_address,
                                                                            mac=self.src_mac)
