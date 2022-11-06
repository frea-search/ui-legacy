import ipaddress
import requests
import threading
import sys

block_asn = [14061, 16509, 31898, 16550, 139190, 139070, 8074, 8075, 12076, 14061, 63949, 14618]
block_prefixes = []
ip = "192.168.0.1"

def  add_to_db(block_asns):
    for asn in block_asns:
        print(f"ASN: {asn}")
        get_asn_api_result = requests.get(f"https://stat.ripe.net/data/announced-prefixes/data.json?resource=AS{asn}")
        block_ips = get_asn_api_result.json()

        for prefix_data in block_ips["data"]["prefixes"]:
            prefix = prefix_data["prefix"]
            if ipaddress.ip_network(prefix).version == 4:
                print(f"PREFIX: {prefix}")
                block_prefixes.append(prefix)
            else:
                pass
                #for ip in ipaddress.IPv6Network(prefix):
                    #print(ip)


#add_to_db(block_asn)

def chk_ip(ip):
    for prefix in block_prefixes:
        if ipaddress.ip_address(ip) in ipaddress.IPv4Network(prefix):
            return True
        else:
            return False
