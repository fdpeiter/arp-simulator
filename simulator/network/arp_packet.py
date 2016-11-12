# -*- coding: utf-8 -*-
import netaddr

class ArpPacket:
    def __init__(self, src_mac, src_address, dst_mac, dst_address):
        assert isinstance(src_mac, netaddr.EUI)
        assert isinstance(src_address, netaddr.IPAddress)
        assert isinstance(dst_mac, netaddr.EUI) or dst_mac is None
        assert isinstance(dst_address, netaddr.IPAddress)
        self.src_mac = src_mac
        self.src_address = src_address
        self.dst_mac = dst_mac
        self.dst_address = dst_address


class ArpRequest(ArpPacket):
    def __str__(self):
        return "src_host box src_host : ARP - Who has {dst}? Tell {src};".format(src=self.src_address,
                                                                                 dst=self.dst_address)


class ArpReply(ArpPacket):
    def __str__(self):
        return " src_host => dst_host : ARP - {src_ip} is at {src_mac};".format(src_ip=self.src_address,
                                                                               src_mac=self.src_mac)
