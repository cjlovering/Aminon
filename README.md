# Aminon
A lightweight DNS-based traffic gatekeeper filter simulation

## Design Document
https://www.overleaf.com/5973117gnxtwm#/19840886/

## Dependencies

Installing and Dependencies for NetfilterQueue
`
 # sudo apt-get install build-essential python-dev libnetfilter-queue-dev
 # pip install NetfilterQueue 
`
Install dpkt to parse dns response
`
 # pip install dpkt
`
Intsall scapy to parse packets from NetfilterQueue
`
 # pip install scapy
`