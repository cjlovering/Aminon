from netfilterqueue import NetfilterQueue
from time import time
#import subprocess import os
import random

from struct import *
from scapy.all import *

import socket

# ip_address --> ttl
honeypot_addr = "1.1.1.1"
store = {}

def initial_configure():
    """
    generates list of public ips and stores it in store
    writes the pre-routing rule to send the honeypot
    """
    # creates a dict of ip addresses
   
    # write the pre-routing rule
    pass

def process(packet):
    """ parses a packet for dns response, replacing priv ip with pub ip
    and creating a rule in the nat table.

    packet: a pkt from nfqueue, parse it and send mod dns response
    """
    pkt = IP(packet.get_payload()) #converts the raw packet to a scapy compatible string    
    ip = IP()
    udp = UDP()

    # delete checksums to force them to recompute
    del pkt[UDP].chksum
    del pkt[IP].chksum
    del pkt.chksum
    
    # TODO: here we get the new public ip address
    public_ip = "31.33.7.31"

    # getting details from packet
    qd = pkt[UDP].payload
    qname = pkt.getlayer(DNS).qd.qname
    
    # TODO: confirm this works. current an is None typically, it should be priv address
    private_ip = honeypot_addr
    if pkt.getlayer(DNS).an is not None:
        private_ip = pkt.getlayer(DNS).an.rdata
    else:
        # DESCISION:
        #   something is amiss, accept, drop or modify?
        packet.accept()
        return
        
    # TODO: write rule to NAT
    # os.system( "iptables command as a string" )
    # public_ip --> private_ip
    
    pkt[DNS].an.rdata = public_ip
    pkt[DNS].ns.rdata = public_ip
    pkt[DNS].ar.rdata = public_ip

    packet.set_payload(str(pkt))

    print packet.get_payload()
    packet.accept();

def main():
    print "starting script...."    
    initial_configure()
    nfqueue = NetfilterQueue()
    nfqueue.bind(1, process)
    try:
        nfqueue.run()
    except KeyboardInterrupt:
        print('')
    nfqueue.unbind()

if __name__ == "__main__":
    main()
