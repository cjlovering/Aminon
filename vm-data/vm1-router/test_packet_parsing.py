from netfilterqueue import NetfilterQueue
from time import time
import subprocess
import random
import pcapy
from pcapy import *
from struct import *
from scapy import *
from scapy.all import *
from scapy.layers.inet import IP, TCP
#from dpkt import *
#import dpkt
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


def test_packet_process(packet):
    """
    tests packet processing
    """
    pkt = IP(packet.get_payload()) #converts the raw packet to a scapy compatible string
    qname = "hello.io"
    
    ip = IP()
    udp = UDP()
    ip.src = pkt[IP].dst
    ip.dst = pkt[IP].src

    udp.sport = pkt[UDP].dport
    udp.dport = pkt[UDP].sport

    # here we get the new public ip address
    solved_ip = "31.33.7.31" # I'm lazy, reader you might create a function to generate random IP :))
    qd = pkt[UDP].payload
    dns = DNS(id = qd.id, qr = 1, qdcount = 1, ancount = 1, arcount = 1, nscount = 1, rcode = 0)
    dns.qd = qd[DNSQR]
    dns.an = DNSRR(rrname = qname, ttl = 257540, rdlen = 4, rdata = solved_ip)
    dns.ns = DNSRR(rrname = qname, ttl = 257540, rdlen = 4, rdata = solved_ip)
    dns.ar = DNSRR(rrname = qname, ttl = 257540, rdlen = 4, rdata = solved_ip)

    # write rule to NAT
    print "Sending the fake DNS reply to %s:%s" % (ip.dst, udp.dport)
    send(ip/udp/dns)

    
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
