from netfilterqueue import NetfilterQueue
from time import time
import subprocess
import random

# ip_address --> ttl
interface = "eth0"
client_addr = "10.4.6.1"
honeypot_addr = "10.4.6.2"
honey_port = "8080"
webserver_addr = "10.4.6.3"
store = {}
ip_list = [] # global list of randomly generated IPs
ttl = 300
ttl_map = {}


def initial_configure():
    """
    generates list of public ips and stores it in store
    writes the pre-routing rule to send the honeypot
    """
    # creates a dict of ip addresses

    # this rule is needed to route dns resp to netfilter q
    # > sudo iptables -t nat -A PREROUTING -p udp --dport 53 -j NFQUEUE --queue-num 1
    # We don't need sudo as the script will run as sudo python script.py
    sp = subprocess.Popen(["iptables", "-t", "nat", "-A", "PREROUTING", "-p", "udp", "--dport", "53", "-j", "NFQUEUE" "--queue-num", "1"], stdout=subprocess.PIPE)
    
    
    
    # write the pre-routing rule to route everything to the honeypot unless otherwise specified
    """
    iptables -t mangle -A PREROUTING -i eth0 -j TTL --ttl-set 64
    
    iptables -A FORWARD -d 2.2.2.2 -i eth0 -p tcp -m tcp --dport 1000:65500 -j ACCEPT #forward tcp port range
    iptables -A FORWARD -d 2.2.2.2 -i eth0 -p udp -m udp --dport 1000:65500 -j ACCEPT #forward udp port range
    iptables -t nat -A PREROUTING -d 1.1.1.1 -p tcp -m tcp --dport 1000:65500 -j DNAT --to-destination 2.2.2.2  #tcp port range
    iptables -t nat -A PREROUTING -d 1.1.1.1 -p udp -m udp --dport 1000:65500 -j DNAT --to-destination 2.2.2.2  #udp port range
    iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
    
    ... general iptables ...
    -t nat/filter/mangle
    -A append to list -I insert
    -d destination adress
    -i input interface (where pkt recv)
    -o output interface (where pkt sent)
    route from IP:port to another IP:port
    iptables -t nat -A PREROUTING --src $SRC_IP_MASK --dst $DST_IP -p tcp --dport $portNumber -j REDIRECT --to-ports $rediectPort
    will attempt to update tomo
    """
    sp = subprocess.Popen(["iptables", "-t", "mangle", "-A", "PREROUTING", "-i", interface, "-j", "TTL", "--ttl-set", "64"], stdout=subprocess.PIPE)
    
    sp = subprocess.Popen(["iptables", "-A", "FORWARD", "-d", honeypot_addr, "-i", interface, "-p", "tcp", "-m", "tcp", "--dport", "1000:65500" , "-j", "ACCEPT"], stdout=subprocess.PIPE)
    sp = subprocess.Popen(["iptables", "-A", "FORWARD", "-d", honeypot_addr, "-i", interface, "-p", "udp", "-m", "udp", "--dport", "1000:65500" , "-j", "ACCEPT"], stdout=subprocess.PIPE)
    sp = subprocess.Popen(["iptables", "-t", "nat", "-A", "PREROUTING", "-d", client_addr, "-p", "tcp", "-m", "tcp", "--dport", "1000:65500" , "-j", "DNAT", "--to-destination", honeypot_addr], stdout=subprocess.PIPE)
    sp = subprocess.Popen(["iptables", "-t", "nat", "-A", "PREROUTING", "-d", client_addr, "-p", "udp", "-m", "udp", "--dport", "1000:65500" , "-j", "DNAT", "--to-destination", honeypot_addr], stdout=subprocess.PIPE)
    sp = subprocess.Popen(["iptables", "-t", "nat", "-A", "POSTROUTING", "-o", interface, "-j", "MASQUERADE"], stdout=subprocess.PIPE)
    output , err = sp.communicate()
    print output
    
def gen_rand_ip():
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
    t = int(time.time())
    for k, v in ttl_map:
    	if v - t > ttl:
	   delete_connection_rule(k[0], k[1], k[2])
    
def add_connection_rule(from_ip, private_addr, public_addr):
    write_iptable_connection_rule(from_ip, private_addr, public_addr, '-A')

def delete_connection_rule(from_ip, private_addr, public_addr):
    write_iptable_connection_rule(from_ip, private_addr, public_addr, '-D')

def write_iptable_connection_rule(from_ip, private_addr, public_addr, delete_add_mode):
    """
    executes an command line ip tables command to allow connection to the webserver
    """
 
    """
    iptables -A INPUT -s "ip.to.allow.here" -j ALLOW
    """
    # TODO: set this to the correct rule
    p = subprocess.Popen(["iptables", delete_add_mode, "INPUT", "-s", client_addr, "-j", "ALLOW"], stdout=subprocess.PIPE)
    output , err = p.communicate()
    print output
    
def dns_nat_arbiter(packet):
    """
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

    # TODO: here we get the new public ip address
    update_ttl_rules()
    public_ip = '66.66.66.66'  # gen_rand_ip();
    
    # getting details from packet
    qd = pkt[UDP].payload
    
    # creating DNS
    dns = DNS(id = qd.id, qr = 1, qdcount = 1, ancount = 1, arcount = 1, nscount = 1, rcode = 0)

    private_ip = honeypot_addr

    if pkt.getlayer(DNS).an is not None:
        qname = pkt.getlayer(DNS).qd.qname
        private_ip = pkt.getlayer(DNS).an.rdata
    else:
        packet.drop()
        return
    
    
    # TODO: write rule to NAT
    # add_connection_rule(ip.src, public_ip, private_ip)

    dns.qd = qd[DNSQR]
    dns.an = DNSRR(rrname = qname, ttl = ttl, rdata = public_ip)
    dns.ns = DNSRR(rrname = qname, ttl = ttl, rdata = public_ip)
    dns.ar = DNSRR(rrname = qname, ttl = ttl, rdata = public_ip)
         

    # save the file
    ttl_map[(ip.src, private_ip, public_ip)] = int(time.time())

    # drop orig packet, and send the new one
    packet.drop()
    send(ip/udp/dns) 

  

def main():
    initial_configure()
    nfqueue = NetfilterQueue()
    nfqueue.bind(1, dns_nat_arbiter)
    try:
        nfqueue.run()
    except KeyboardInterrupt:
        print('')
    nfqueue.unbind()
    
if __name__ == "__main__":
    main()
