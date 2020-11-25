[![Build Status](
https://travis-ci.com/nickrusso42518/ipv6-tools.svg?branch=master)](
https://travis-ci.com/nickrusso42518/ipv6-tools)

# IPv6 Tools
This repository contains a variety of IPv6 tools, most of which relate to
a DHCPv6 prefix delegation solution I designed for a customer.

> Contact information:\
> Email:    njrusmc@gmail.com\
> Twitter:  @nickrusso42518

  * [EUI64 Ansible Inventory Maker](#eui64-ansible-inventory-maker)
  * [Cisco EEM Boot Script](#cisco-eem-boot-script)
  * [Testing](#testing)

## EUI64 Ansible Inventory Maker
The `eui64.py` script takes a list of MAC addresses in a plain text file named
`macs.txt` with one MAC address per line. Any common format or mix of
delimeters is acceptable, including hyphens (`-`), colons (`:`),
or periods (`.`) between the hexadecimal characters.

There are two forms of output.
  1. Prints the original MAC addresses followed by the EUI64 IPv6 address
     derived from that MAC address on a singleline. This information is
     written to standard output as a quick visual check. Those that do not
     use Ansible may benefit from these quick conversions when applied to
     other use-cases.
  2. Generates a `hosts.yml` file which conforms to the Ansible YAML inventory
     standard. Each MAC address is represented by a new node which uses
     the EUI64 IPv6 address as the `ansible_host` parameter for connectivity.
     This repository supplied an example output inventory file named
     `sample_hosts.yml` to demonstrate what the output might look like.

You can optionally pass in the IPv6 prefix to the `eui64.py` script as a
command line argument. If no argument is supplied, the script uses the RFC3849
documentation prefix of `2001:db8::` in front of every EUI64 IPv6 address. The
prefix should be a plain string to be prepended to the EUI64 IPv6 address and
should *not* contain a prefix-length using `/` notation.

## Cisco EEM Boot Script
The `eem.txt` file is a reference configuration for Cisco IOS devices that
contains a relatively complex Embedded Event Manager (EEM) script. The
script performs two key tasks upon initial boot when necessary:
  1. Update the hostname to a unique string based on the device's serial number
  2. Update the Loopback0 IPv6 address to use /128 prefix-length while
     preserving the EUI64 IPv6 address already applied

Expressed in rough Python pseudo-code:

```
if not hostname.startswith("REMOTE-"):
    hostname = f"REMOTE-{device.sn}"
    loopback0.ipv6 = loopback0.ipv6.replace("64", "128")
```

### Testing
A GNU `Makefile` is used to automate testing with the following targets:
  * `lint`: Runs `yamllint` and `pylint` linters, and the `black` formatter
  * `run`: Performs test runs of all executable scripts in the repository
  * `clean`: Deletes any artifacts, such as `.pyc`, `.log`, and `output/` files
  * `all`: Default target that runs the sequence `clean lint unit dry`
