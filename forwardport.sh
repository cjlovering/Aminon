#TEMPORARY#
sysctl -w net.ipv4.ip_forward=1
#PERMENANT#
# ed /etc/sysctl.conf:
        #net.ipv4.ip_forward = 1
        #sysctl -p /etc/sysctl.conf
        #/etc/init.d/procps.sh restart #may just be procps (not .sh)
        #if NOT deb/ubuntu#service network restart
