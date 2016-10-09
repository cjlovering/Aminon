# !/sh/bin/bash

#### To Reset NAT
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X

# Experimental IP table rule here

#### To all NAT and iptables cmds
iptables -L -t nat -n
