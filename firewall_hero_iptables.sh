#!/bin/bash

# Author : Tyler Boykin

# This script takes recently established connections as per
# Sam Bowne's Firewall Hero challenge, and applies iptable modifcations
# dynamically


`netstat -tupn | grep 'tcp' | awk '{print $4}' | cut -d':' -f2 > /ports_tmp`
FILE=/ports_tmp

while read p; do
`iptables -A INPUT -i eth0 -p tcp --dport ${p} -j ACCEPT`
`iptables -A INPUT -i tun0 -p tcp --dport ${p} -j ACCEPT`
done < $FILE

iptables -A INPUT -i eth0 -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -i tun0 -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -i eth0 -p tcp -j DROP
iptables -A INPUT -i tun0 -p tcp -j DROP
iptables-save
iptables-apply
