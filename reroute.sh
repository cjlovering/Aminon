
# !/sh/bin/bash
#tcpdump port 8080
#tcpdump -n dst portrange 6550-6556


#### To Reset NAT
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X

# Make sure ssh is not blocked
#iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -m state --state NEW -m tcp -p tcp --dport 22 -j ACCEPT


#************************* PORT FORWARDING WAS ENABLED ****************************************************************************************


# ***** Reroute DNS exceptions to CATSERVER@3:8080 *****                         Currently VB3
#iptables -t nat -A PREROUTING -p tcp --dport 80 -s 10.10.152.106 -j DNAT --to-destination 10.4.6.3:8080


# ***** Reroute ALL TCP/UDP to HONEY@2:8080 *****                                Currently VB2
iptables -t nat -A PREROUTING -p tcp --dport 1000:65500 -j DNAT --to-destination 10.4.6.2:8080
iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 10.4.6.2:8080
iptables -t nat -A PREROUTING -p tcp --dport 443 -j DNAT --to-destination 10.4.6.2:8080
iptables -t nat -A PREROUTING -p udp --dport 1000:65500 -j DNAT --to-destination 10.4.6.2:8080


# MASQ IS LIFE
iptables -t nat -A POSTROUTING -j MASQUERADE
