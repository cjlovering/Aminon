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
from dpkt import *
import dpkt
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
    ip.src = pkt[IP].dst
    ip.dst = pkt[IP].src

    udp.sport = pkt[UDP].dport
    udp.dport = pkt[UDP].sport

    # TODP: here we get the new public ip address
    public_ip = "31.33.7.31"
    
    qd = pkt[UDP].payload
    qname = pkt.getlayer(DNS).qd.qname
    
    dns = DNS(id = qd.id, qr = 1, qdcount = 1, ancount = 1, arcount = 1, nscount = 1, rcode = 0)

    # TODO: confirm this works. current an is None typically, it should be priv address
    private_ip = honeypot_addr
    if pkt.getlayer(DNS).an is not None:
        private_ip = pkt.getlayer(DNS).an.rdata
    
    dns.qd = qd[DNSQR]
    dns.an = DNSRR(rrname = qname, ttl = 257540, rdlen = 4, rdata = public_ip)
    dns.ns = DNSRR(rrname = qname, ttl = 257540, rdlen = 4, rdata = public_ip)
    dns.ar = DNSRR(rrname = qname, ttl = 257540, rdlen = 4, rdata = public_ip)

    # TODO: write rule to NAT
    # os.system( "iptables command as a string" )
    # public_ip --> private_ip
    send(ip/udp/dns)
    
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
