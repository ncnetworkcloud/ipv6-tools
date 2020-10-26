#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Converts a list of MAC addresses into their IPv6 EUI-64
addresses. Prints the resulting EUI-64 addresses to stdout and creates
and Ansible YAML inventory for future configuration management.
"""

import sys
import ruamel.yaml


def main(v6_prefix):
    """
    Execution begins here.
    """

    # Load MAC addresses from file
    with open("macs.txt", "r") as handle:
        lines = handle.readlines()

    # Initialize Ansible YAML inventory dict
    ansible_inv = {"all": {"hosts": {}}}

    # Iterate over the lines read from file
    for line in lines:

        # Clean up the line; remove whitespace and delimeters
        mac = line.strip().lower()
        for delim in ["-", ":", "."]:
            mac = mac.replace(delim, "")

        # MAC address should be exactly 12 bytes and only hex digits
        assert len(mac) == 12
        assert int(mac, 16) > 0

        # Build the low-order 64 bits of the IPv6 address
        host_addr = f"{mac[:4]}:{mac[4:6]}ff:fe{mac[6:8]}:{mac[8:]}"

        # Flip the 7th bit of first byte (3rd bit of second nibble) using xor
        flip = hex(int(host_addr[1], 16) ^ 2)[-1]

        # Re-assemble host bits with flipped bit plus IPv6 prefix
        eui64_addr = f"{v6_prefix}{host_addr[:1]}{flip}{host_addr[2:]}"

        # Display MAC address and newly-computed EUI-64 IPv6 address
        print(mac, eui64_addr)

        # Update the Ansible inventory dict with new host. The MAC will
        # be the hostname and the host address will be the IPv6 address
        ansible_inv["all"]["hosts"][mac] = {"ansible_host": eui64_addr}

    # Dump the Ansible inventory to a new file for use later
    with open("hosts.yml", "w") as handle:
        ruamel.yaml.dump(
            ansible_inv, handle, default_flow_style=False, explicit_start=True
        )


if __name__ == "__main__":

    # If an IPv6 prefix isn't specified, use RFC3849 documentation prefix
    if len(sys.argv) < 2:
        main("2001:db8::")

    # IPv6 prefix was specified; extract and convert to lowercase
    else:
        main(sys.argv[1].lower())
