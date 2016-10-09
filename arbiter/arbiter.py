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
global ip_list
ip_list = [] # global list of randomly generated IPs
ttl = 300
ttl_map = {}

    
def gen_rand_ip():
    """generates an unused random ip in the public address space

    """
    rand_ip = "10.4.6." + ".".join(("%d" % random.randint(128, 255) for i in range(1)))
    while rand_ip in ip_list:
    	rand_ip = "10.4.6." + ".".join(("%d" % random.randint(128, 255) for i in range(1)))
    ip_list.append(rand_ip)
    return rand_ip

def update_ttl_rules():
    """determines if any of the rules need to be deleted

    """
    global ip_list
    t = int(time.time())
    for k, v in ttl_map.items():
    	if t - v > ttl:
	    delete_connection_rule(k[0], k[1], k[2])
	    ip_list = [x for x in ip_list if x != k[1]]
            del ttl_map[k]
            
def add_connection_rule(src_ip, public_addr, private_addr):
    """will execute the write iptable connection rule function as a insert

    """
    write_iptable_connection_rule(src_ip, public_addr, private_addr, '-I')

def delete_connection_rule(src_ip, public_addr, private_addr):
    """will execute the write iptable connection rule function as a delete

    """
    write_iptable_connection_rule(src_ip, public_addr, private_addr, '-D')

def write_iptable_connection_rule(src_ip, public_addr, private_addr, delete_add_mode):
    """executes an command line ip tables command to allow connection to the webserver

    src_ip {String} - where the packet came from
    public_ip {String} - where the packet thinks its going
    private_ip {String} - where the packet will be routed to
    delete_add_mode {String} - delete or insert
    """

    p = subprocess.Popen(["iptables", "-t", "nat", delete_add_mode, "PREROUTING", "-p", "tcp", "--dport", "80", "-s", src_ip, "-d", public_addr, "-j", "DNAT", "--to-destination", private_addr+":8080"], stdout=subprocess.PIPE)
    output , err = p.communicate()
    

def add_record_ttl_map(client_ip, public_ip, private_ip):
    ttl_map[(client_ip, public_ip, private_ip)] = time.time()

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
    ip.dst = pkt[IP].dst
   
    client_ip = pkt[IP].dst
    
    # build udp portion of packet (ports) #NOTE: flipflop
    udp.sport = pkt[UDP].sport
    udp.dport = pkt[UDP].dport

    # check if any ttls are up
    update_ttl_rules()

    # generate restricted rand ip (in public space)
    public_ip = gen_rand_ip()
    
    # getting details from packet
    qd = pkt[UDP].payload
    
    # creating DNS
    dns = DNS(id = qd.id, qr = 1, qdcount = 1, ancount = 1, arcount = 1, nscount = 1, rcode = 0)

    private_ip = honeypot_addr

    # check if the orig pkt has a DNS answer
    if pkt.getlayer(DNS).an is not None:
        qname = pkt.getlayer(DNS).qd.qname
        private_ip = pkt.getlayer(DNS).an.rdata
    else:
	# packet was not a DNS response
	packet.accept()
        return
    
    # write the connection rule: if from the source to the public route to the private
    if (client_ip, public_ip, private_ip) not in ttl_map:
	add_connection_rule(client_ip, public_ip, private_ip)

    # add the request to the map
    add_record_ttl_map(client_ip, public_ip, private_ip)
       
    # format dns response
    dns.qd = qd[DNSQR]
    dns.an = DNSRR(rrname = qname, ttl = ttl, rdata = public_ip)
    dns.ns = DNSRR(rrname = qname, ttl = ttl, rdata = public_ip)
    dns.ar = DNSRR(rrname = qname, ttl = ttl, rdata = public_ip)
         
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
    
