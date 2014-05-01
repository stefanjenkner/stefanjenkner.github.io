---
layout: post
title: "Forwarding IPv6 Traffic from WAN to LAN with OpenWRT"
date: 2013-03-26 09:58
comments: true
categories: IPv6
published: true
---

We're starting from the premise that you already enabled IPv6. If not so, this will help you to switch it on:

* [Aiccu/Installing on OpenWRT](http://www.sixxs.net/wiki/Aiccu/Installing_on_OpenWRT)
* [IPv6 HowTo on Backfire and later](http://wiki.openwrt.org/doc/howto/ipv6)
 
OpenWRT Attitude Adjustment 2012.09 warning: There is an ongoing discussion regarding the AICCU init script. If you can, stay with OpenWRT Backfire 2010.3.

I'm using SixxS tunnels to enable IPv6. My `` /etc/config/network`` looks like this:


```
config interface 'lan'
	# ...
	option ip6addr '2001:my:subnet:prefix::1/64'

config 'interface' 'wan6'
	# ...
	option 'ip6addr' '2001:my:end:point::2'
```

To enable that your local server is reachable via SSH (port 22) add this rule to ``/etc/config/firewall`` straight after the standard IPv6 rules: 

```
config rule
       option 'src' 'wan6'
       option 'proto' 'tcp'
       option 'dest_port' '22'
       option 'dest_ip' '2001:your:servers:global:ipv6:address:####:####'
       option 'family' 'ipv6'
       option 'target' 'ACCEPT'
       option 'dest' 'lan' 
```

Also make sure that you installed the ``ip6tables`` Package,
then restart the firewall with ``/etc/init.d/firewall restart``
and test your setup.


