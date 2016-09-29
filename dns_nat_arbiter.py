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
