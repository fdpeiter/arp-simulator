# -*- coding: utf-8 -*-
import netaddr


class EchoPacket:
    def __init__(self, src_mac, src_address, dst_mac, dst_address, ttl=8):
        assert isinstance(src_mac, netaddr.EUI), "Invalid MAC Address"
        assert isinstance(dst_mac, netaddr.EUI), "Invalid MAC Address"
        assert isinstance(src_address, netaddr.IPAddress), "Source address must be an valid IPAddress"
        assert isinstance(dst_address, netaddr.IPAddress), "Destination address must be an valid IPAddress"
        assert isinstance(ttl, int) and 0 <= ttl <= 8, "TTL must be an valid integer between 0 and 8"
        self.src_mac = src_mac
        self.dst_mac = dst_mac
        self.src_address = src_address
        self.dst_address = dst_address
        self.ttl = ttl


class EchoRequest(EchoPacket):
    def __str__(self):
        return "src_host => dst_host : ICMP - Echo request " \
               "(src={src_ip} dst={dst_ip} ttl={ttl});".format(src_ip=self.src_address,
                                                               dst_ip=self.dst_address,
                                                               ttl=self.ttl)


class EchoReply(EchoPacket):
    def __str__(self):
        if self.ttl == 0:
            return "src_host => dst_host : ICMP - Time Exceeded;"
        else:
            return "src_host => dst_host : ICMP - Echo reply " \
                   "(src={src_ip} dst={dst_ip} ttl={ttl});".format(src_ip=self.src_address,
                                                                   dst_ip=self.dst_address,
                                                                   ttl=self.ttl)