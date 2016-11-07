# -*- coding: utf-8 -*-
import netaddr


class EchoRequest:
    def __init__(self, mac_dst, src_host, dst_host, src_address, dst_address, ttl=8):
        assert isinstance(mac_dst, netaddr.EUI), "Invalid MAC Address"
        assert isinstance(src_host, str), "Source host must be an string"
        assert isinstance(dst_host, str), "Destination host must be an string"
        assert isinstance(src_address, netaddr.IPAddress), "Source address must be an valid IPAddress"
        assert isinstance(dst_address, netaddr.IPAddress), "Destination address must be an valid IPAddress"
        assert isinstance(ttl, int) and 0 <= ttl <= 8, "TTL must be an valid integer between 0 and 8"
        self.mac_dst = mac_dst
        self.src_host = src_host
        self.dst_host = dst_host
        self.src_address = src_address
        self.dst_address = dst_address
        self.ttl = ttl

    def __str__(self):
        return "{src_host} => {dst_host} : ICMP - Echo request " \
               "(src={src_ip} dst={dst_ip} ttl={ttl});".format(src_host=self.src_host,
                                                               dst_host=self.dst_host,
                                                               src_ip=self.src_address,
                                                               dst_ip=self.dst_address,
                                                               ttl=self.ttl)


class EchoReply:
    def __init__(self, mac_dst, src_host, dst_host, src_address, dst_address, ttl=8):
        assert isinstance(mac_dst, netaddr.EUI), "Invalid MAC Address"
        assert isinstance(src_host, str), "Source host must be an string"
        assert isinstance(dst_host, str), "Destination host must be an string"
        assert isinstance(src_address, netaddr.IPAddress), "Source address must be an valid IPAddress"
        assert isinstance(dst_address, netaddr.IPAddress), "Destination address must be an valid IPAddress"
        assert isinstance(ttl, int) and 0 <= ttl <= 8, "TTL must be an valid integer between 0 and 8"
        self.mac_dst = mac_dst
        self.src_host = src_host
        self.dst_host = dst_host
        self.src_address = src_address
        self.dst_address = dst_address
        self.ttl = ttl

    def __str__(self):
        if self.ttl == 0:
            return "{src_host} => {dst_host} : ICMP - Time Exceeded;".format(src_host=self.src_host,
                                                                             dst_host=self.dst_host)
        else:
            return "{src_host} => {dst_host} : ICMP - Echo reply " \
                   "(src={src_ip} dst={dst_ip} ttl={ttl});".format(src_host=self.src_host,
                                                                   dst_host=self.dst_host,
                                                                   src_ip=self.src_address,
                                                                   dst_ip=self.dst_address,
                                                                   ttl=self.ttl)