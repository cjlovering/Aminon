# Aminon
A lightweight DNS-based traffic gatekeeper filter simulation

## Dependencies

This system uses python2.7, bind9, and iptables on the machine for the dns/nat. Our setup is further described in the report. 


**Installing and Dependencies for NetfilterQueue**

```{bash}
 # sudo apt-get install build-essential python-dev libnetfilter-queue-dev
 # pip install NetfilterQueue 
```

**Install dpkt to parse dns response**

```{bash}
 # pip install dpkt
```

**Install scapy to parse packets from NetfilterQueue**

```{bash}
 # pip install scapy
```
