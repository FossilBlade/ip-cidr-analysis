import ipaddress


cird_ip = '192.0.0.1/24'

try:
    p = ipaddress.ip_network(cird_ip,False)
    print(list(p.hosts()))
except ValueError as e:
    print(e)