from netfilterqueue import NetfilterQueue
from time import time
import subprocess
import random
import pcapy
from pcapy import *
from struct import *
from scapy import *
from scapy.layers.inet import IP, TCP
from dpkt import *
import socket

# ip_address --> ttl
honeypot_addr = "1.1.1.1"
store = {}
ip_list = {}

def initial_configure():
    """
    generates list of public ips and stores it in store
    writes the pre-routing rule to send the honeypot
    """
    # creates a dict of ip addresses
    genMatrix = 16**2
    # In case we want to keep the attempts within the rednet "10.44" begins class A&B sections
    rand_ipv4 = "10.44." + ".".join(("%d" % random.randint(0, genMatrix) for i in range(2)))
    #for ip in ip_list:
    # write the pre-routing rule
    pass

def test_packet_process(pkt):
    """
    tests packet processing
    """
    packet = pkt.get_payload()
    p = IP(packet)
    print p[IP].src

    pkt.set_payload(str(pkt))

    #script_start = time()
    pkt.accept()

def main():
    print "starting script...."
    initial_configure()
    nfqueue = NetfilterQueue()
    nfqueue.bind(1, test_packet_process)
    try:
        nfqueue.run()
    except KeyboardInterrupt:
        print('')
    nfqueue.unbind()

if __name__ == "__main__":
    main()
