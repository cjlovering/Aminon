#
# DISCLAIMER COMMANDS ARE DIFFERENT FROM asset/honeyp
#Run w/sudo 

# May potentially needs a netmask, this may work
#ip address add 10.4.6.128/25 netmask 255.255.255.0 dev eth0
ip address add 10.4.6.128/25 via 10.4.6.1
