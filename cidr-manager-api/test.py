
import ipaddress
import sys

cird_ip = "83.0.0.0/8"

try:
    p = ipaddress.ip_network(cird_ip)
    print(p)
except ValueError:
    print(sys.exc_info())