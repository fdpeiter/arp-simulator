import netaddr

class RouterPort:
    def __init__(self, mac, ip_address, connected_devices):
        assert isinstance(mac, netaddr.EUI), "Invalid MAC Address"
        assert isinstance(ip_address, netaddr.IPNetwork), "Invalid IP/Prefix"
        self.mac = mac
        self.ip_address = ip_address
        self.connected_devices = connected_devices
