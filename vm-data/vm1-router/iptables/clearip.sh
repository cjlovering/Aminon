#### To Reset NAT
       iptables -F
       iptables -X
       iptables -t nat -F
       iptables -t nat -X
       iptables -t mangle -F
       iptables -t mangle -X

#### To all NAT and iptables cmds
iptables -L -t nat -n

