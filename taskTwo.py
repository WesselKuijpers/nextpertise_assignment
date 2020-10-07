import struct
import socket
import ipaddress

class Network:
    def __init__(self, address):
        self.address = address

    def __str__(self):
        return self.address

    def __sub__(self, other):
        # get ranges
        ip_ranges = self.diff_ranges(other)

        networks = []

        # iterate over the ip_ranges, find to which subnet they belong and append it to the networks list
        for ip_range in ip_ranges:
            # i have been a little cheeky here and used the built-in ippaddress to find the subnets
            networks.extend(str(ipaddr) for ipaddr in ipaddress.summarize_address_range(ip_range[0], ip_range[-1]))

        return networks

    # method for getting the range of ip adresses in a subnet
    def get_range(self):
        # get the network prefix and mask by splitting the address on the '/'
        prefix, mask = self.address.split('/')
        mask = int(mask)
        # get the host bits, IPv4 addresses consist of 32 bits, so 32- the mask bits
        host_bits = 32 - mask
        
        # prefix string to integer
        # convert IPv4 string to binary format
        prefix_bin = socket.inet_aton(prefix)
        # unpack the binary prefix to integer 
        # i'm assuming the host system is little-endian, so i enforce big-endian
        # struct.unpack always returns a tuple, therefor i take the first element
        ip_integer = struct.unpack('>I', prefix_bin)[0]

        # define a start and end point for the range by clearing the host_bits (using the bitwise shift operators)
        start = (ip_integer >> host_bits) << host_bits
        end = start | ((1 << host_bits) - 1)
        end += 1

        ip_range = []
        # convert each address from binary back to string, create an ip_address object form it, append it to the range list
        for i in range(start, end):
            addr = ipaddress.ip_address(socket.inet_ntoa(struct.pack('>I',i)))
            ip_range.append(addr)

        # sort the range
        ip_range.sort()

        return ip_range

    # method that removes duplicate addresses from this network's range and returns the ranges that are left 
    def diff_ranges(self, other):
        # get ranges
        self_range = self.get_range()
        other_range = other.get_range()

        # find where the other_range is located in the self_range
        start_remove = self_range.index(other_range[0])
        end_remove = self_range.index(other_range[-1])

        ranges = []
        # remove the other_range from the self range, in some cases this gives one range back, sometimes two
        if start_remove != 0:
            ranges.append(self_range[:start_remove])
        ranges.append(self_range[end_remove + 1:])

        return ranges


a = Network('192.168.1.0/24')
b = Network('192.168.1.16/29')

print(a) # prints 192.168.1.0/24
print(b) # prints 192.168.1.16/29
print(a-b) # prints ['192.168.1.0/28', '192.168.1.24/29', '192.168.1.32/27', '192.168.1.64/26', '192.168.1.128/25']

