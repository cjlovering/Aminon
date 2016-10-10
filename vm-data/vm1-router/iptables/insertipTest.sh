# !/sh/bin/bash


# ***** Reroute DNS exceptions to CATSERVER@3:8080 *****                         Currently VB3
iptables -t nat -I PREROUTING -p tcp --dport 80 -s 10.4.6.4 -d 10.4.6.128 -j DNAT --to-destination 10.4.6.3:8080


#List our everything
iptables -L -t nat -nv
