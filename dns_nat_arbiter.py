from netfilterqueue import NetfilterQueue
from time import time
import subprocess
import random

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
    """
    iptables -A FORWARD -d 2.2.2.2 -i eth0 -p tcp -m tcp --dport 1000:65500 -j ACCEPT #forward tcp port range
    iptables -A FORWARD -d 2.2.2.2 -i eth0 -p udp -m udp --dport 1000:65500 -j ACCEPT #forward udp port range
    iptables -t nat -A PREROUTING -d 1.1.1.1 -p tcp -m tcp --dport 1000:65500 -j DNAT --to-destination 2.2.2.2  #tcp port range
    iptables -t nat -A PREROUTING -d 1.1.1.1 -p udp -m udp --dport 1000:65500 -j DNAT --to-destination 2.2.2.2  #udp port range
    iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
    """
    sp = subprocess.Popen(["iptables", "-A", "FORWARD", "-d", "dest.ip.goes.here", "-i", "enp0s3", "-p", "tcp", "-m", "tcp", "--dport", "1000:65500" , "-j", "ACCEPT"], stdout=subprocess.PIPE)
    sp = subprocess.Popen(["iptables", "-A", "FORWARD", "-d", "dest.ip.goes.here", "-i", "enp0s3", "-p", "udp", "-m", "udp", "--dport", "1000:65500" , "-j", "ACCEPT"], stdout=subprocess.PIPE)
    sp = subprocess.Popen(["iptables", "-t", "nat", "-A", "PREROUTING", "-d", "src.ip.goes.here", "-p", "tcp", "-m", "tcp", "--dport", "1000:65500" , "-j", "DNAT", "--to-destination", "dest.ip.goes.here"], stdout=subprocess.PIPE)
    sp = subprocess.Popen(["iptables", "-t", "nat", "-A", "PREROUTING", "-d", "src.ip.goes.here", "-p", "udp", "-m", "udp", "--dport", "1000:65500" , "-j", "DNAT", "--to-destination", "dest.ip.goes.here"], stdout=subprocess.PIPE)
    sp = subprocess.Popen(["iptables", "-t", "nat", "-A", "POSTROUTING", "-o", "enp0s3", "-j", "MASQUERADE"], stdout=subprocess.PIPE)
    output , err = sp.communicate()
    print output
    pass
    

def iptables_call(private_addr, public_addr, ttl, interface):
    """
    executes an command line ip tables command
    """
    
    # TODO: generalize this for multiple comnads
    p = subprocess.Popen(["iptables", "-A", "INPUT", "-p", "tcp", "-m", "tcp", "--dport", "22" , "-j", "ACCEPT"], stdout=subprocess.PIPE)
    output , err = p.communicate()
    print output
    
def dns_nat_arbiter(pkt):
    """
    writes exception to ip tables
    gets the ttl and puts it into the dict
    """

    #script_start = time()
    print(pkt)
    pkt.accept()

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
