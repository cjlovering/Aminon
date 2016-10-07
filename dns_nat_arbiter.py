from netfilterqueue import NetfilterQueue
from time import time
import subprocess
import random

# ip_address --> ttl
interface = "enp0s3"
client_addr = "0.0.0.0"
honeypot_addr = "10.4.6.4"
honey_port = "8088"
webserver_addr = "2.2.2.2"
store = {}
ip_list = [] # global list of randomly generated IPs
    
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
	#print rand_ip
	#print ip_list

def approve_ip(private_addr, public_addr, ttl, interface):
    """
    executes an command line ip tables command to allow connection to the webserver
    """
    
    # TODO: generalize this for multiple comnads
    # TODO:? Needs to alter to allow with the allowed TTL and only allow to connect to the given random public IP as a destination ?
    """
    iptables -A INPUT -s "ip.to.allow.here" -j ALLOW
    """
    p = subprocess.Popen(["iptables", "-A", "INPUT", "-s", client_addr, "-j", "ALLOW"], stdout=subprocess.PIPE)
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
