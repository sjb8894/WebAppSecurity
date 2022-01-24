import requests
import sys
import ipaddress
from multiprocessing.dummy import Pool

# take in range of ip's, scan each looking for HTTP proxy

target = 'https://csec.rit.edu'
portList = [80, 8080]


def findProxy(address):
    addr = ipaddress.IPv4Address(address)
    for x in portList:
        try:
            resp = requests.get(target, proxies={'http': 'http://' + str(addr) + ':' + str(x)}, timeout=3)
            if resp.status_code == 200 and ("RIT" in resp.text):
                print("IP Address of Proxy: " + str(addr))

        except:
            pass


def main():
    if len(sys.argv) != 3:
        print("Incorrect input")
        return 1
    headIP = ipaddress.ip_address(sys.argv[1])
    tailIP = ipaddress.ip_address(sys.argv[2])
    threader = Pool(150)
    threader.map(findProxy, range(int(headIP), int(tailIP) + 1))
    threader.close()
    threader.join()

main()
