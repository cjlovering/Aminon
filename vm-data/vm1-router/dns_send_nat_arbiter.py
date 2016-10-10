from netfilterqueue import NetfilterQueue
from scapy.all import *
import time
import subprocess
import random

interface = "eth0"
client_addr = "10.4.6.4"
honeypot_addr = "10.4.6.2"
honey_port = "8080"
webserver_addr = "10.4.6.3"
ip_list = [] # global list of randomly generated IPs
ttl = 300
ttl_map = {}

    
def gen_rand_ip():
    """generates an unused random ip in the public address space

    """
    
    first_blk = random.randint(0, 255)
    while first_blk == 10 or first_blk == 192:
	first_blk = random.randint(0, 255)
    first_blk = str(first_blk) + "."
    # I believe we actually only have a class C liscense ie 10.4.6.5/24 to use as random public facing addresses
    rand_ip = first_blk + ".".join(("%d" % random.randint(0, 255) for i in range(3)))
    while rand_ip in ip_list:
	rand_ip = first_blk + ".".join(("%d" % random.randint(0, 255) for i in range(3)))
    ip_list.append(rand_ip)

def update_ttl_rules():
    """determines if any of the rules need to be deleted

    """
    
    t = int(time.time())
    for k, v in ttl_map.items():
    	if v - t > ttl:
	   delete_connection_rule(k[0], k[1], k[2])
           del ttl_map[k]
    
def add_connection_rule(src_ip, private_addr, public_addr):
    """will execute the write iptable connection rule function as a insert

    """
    write_iptable_connection_rule(src_ip, private_addr, public_addr, '-I')

def delete_connection_rule(src_ip, private_addr, public_addr):
    """will execute the write iptable connection rule function as a delete

    """
    write_iptable_connection_rule(src_ip, private_addr, public_addr, '-D')

def write_iptable_connection_rule(src_ip, private_addr, public_addr, delete_add_mode):
    """executes an command line ip tables command to allow connection to the webserver

    src_ip {String} - where the packet came from
    public_ip {String} - where the packet thinks its going
    private_ip {String} - where the packet will be routed to
    delete_add_mode {String} - delete or insert
    """

    p = subprocess.Popen(["iptables", "-t", "nat", delete_add_mode, "PREROUTING", "-p", "tcp", "--dport", "80", "-s", src_ip, "-d", public_addr, "-j", "DNAT", "--to-destination", private_addr+":8080"], stdout=subprocess.PIPE)
    output , err = p.communicate()
    
def dns_nat_arbiter(packet):
    """ the core of the capability functionality - parses each incoming packet
    determines if its a dns response
    writes exception to ip tables
    gets the ttl and puts it into the dict
    """
    pkt = IP(packet.get_payload())
    ip = IP()
    udp = UDP()
    
    # get ip src and dest of orig packet for building and iptbles
    ip.src = pkt[IP].src
    ip.dst = pkt[IP].src
    
    # build udp portion of packet (ports)
    udp.sport = pkt[UDP].dport
    udp.dport = pkt[UDP].sport

    # check if any ttls are up
    update_ttl_rules()

    # generate restricted rand ip (in public space)
    public_ip = '10.4.6.133'    # gen_rand_ip();
    
    # getting details from packet
    qd = pkt[UDP].payload
    
    # creating DNS
    dns = DNS(id = qd.id, qr = 1, qdcount = 1, ancount = 1, arcount = 1, nscount = 1, rcode = 0)

    private_ip = honeypot_addr


    print "DNS: ", pkt.getlayer(DNS)
    print "dns: ", dns
    print "ip.src: ", ip.src

    # check if the orig pkt has a DNS answer
    if pkt.getlayer(DNS).an is not None:
        qname = pkt.getlayer(DNS).qd.qname
        private_ip = pkt.getlayer(DNS).an.rdata
    else:
	# packet was not a DNS response
	packet.accept()
	print "PACCEPT"
        return
    
    # write the connection rule: if from the source to the public route to the private
    add_connection_rule(ip.src, private_ip, public_ip)

    # format dns response
    dns.qd = qd[DNSQR]
    dns.an = DNSRR(rrname = qname, ttl = ttl, rdata = public_ip)
    dns.ns = DNSRR(rrname = qname, ttl = ttl, rdata = public_ip)
    dns.ar = DNSRR(rrname = qname, ttl = ttl, rdata = public_ip)
         
    # add the request to the map
    print "adding to ttl map: ", ip.src, private_ip, public_ip
    ttl_map[(ip.src, private_ip, public_ip)] = int(time.time())

    # drop orig packet, and send the new one
    packet.drop()
    send(ip/udp/dns) 

def main():
    nfqueue = NetfilterQueue()
    nfqueue.bind(1, dns_nat_arbiter)
    try:
        nfqueue.run()
    except KeyboardInterrupt:
        print('')
    nfqueue.unbind()
    
if __name__ == "__main__":
    main()
