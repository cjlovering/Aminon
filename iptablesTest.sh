# !/sh/bin/bash

#### To Reset NAT
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X

# Experimental IP table rule
#iptables -t nat -A PREROUTING --src 10.10.152.106 --dst 10.4.6.4 -p tcp --dport 1000:65500 -j REDIRECT --to-ports 8088
iptables -t nat -A PREROUTING --src 0/0 --dst 10.10.152.106 -p tcp --dport 80 -j REDIRECT --dst 10.4.6.4 --to-ports 8088
#### To all NAT and iptables cmds
iptables -L -t nat -n
