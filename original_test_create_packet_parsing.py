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
    """
    tests packet processing
    
    packet: a pkt from nfqueue, parse it and send mod dns response
    """
    pkt = IP(packet.get_payload()) #converts the raw packet to a scapy compatible string    
    ip = IP()
    udp = UDP()

    # building ip portion of packet
    ip.src = pkt[IP].dst
    ip.dst = pkt[IP].src
    
    # building udp portion of packet
    udp.sport = pkt[UDP].dport
    udp.dport = pkt[UDP].sport
        
    # TODO: here we get the new public ip address
    public_ip = "31.33.7.31"

    # getting details from packet
    qd = pkt[UDP].payload
    qname = pkt.getlayer(DNS).qd.qname

    # creating DNS 
    dns = DNS(id = qd.id, qr = 1, qdcount = 1, ancount = 1, arcount = 1, nscount = 1, rcode = 0)

    # TODO: confirm this works. current an is None typically, it should be priv address
    private_ip = honeypot_addr
    if pkt.getlayer(DNS).an is not None:
        private_ip = pkt.getlayer(DNS).an.rdata
    else:
        # CONFIRM: this packet should just be accepted
        packet.accept()
        return
        
    dns.qd = qd[DNSQR]
    dns.an = DNSRR(rrname = qname, ttl = 257540, rdlen = 4, rdata = public_ip)
    dns.ns = DNSRR(rrname = qname, ttl = 257540, rdlen = 4, rdata = public_ip)
    dns.ar = DNSRR(rrname = qname, ttl = 257540, rdlen = 4, rdata = public_ip)

    # TODO: write rule to NAT
    # os.system( "iptables command as a string" )
    # public_ip --> private_ip
    
    pkt[DNS].an.rdata = public_ip
    pkt[DNS].ns.rdata = public_ip
    pkt[DNS].ar.rdata = public_ip
    packet.set_payload(str(pkt))
    
    
    print "hello ", packet.get_payload()
    #send(ip/udp/dns)
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
