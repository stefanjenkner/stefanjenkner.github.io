---
layout: post
title:  "UniFi v5 Controller on Cubietruck"
date:   2018-03-27 23:13:54
categories: unifi ubiquiti cubietruck armbian systemd
---

This is about how to install the UniFi v5 Contoller on [armbian][armbian] -- a lightweight Linux distribution based on Debian Jessie (or Debian Stretch) supporting the [Cubietruck][cubietruck] (also know as Cubieboard 3). The UniFi Controller software is required for provisioning and management of UniFi Enterprise devices like the UAP-AC-PRO.

The following instructions are based on armbian Jessie and UniFi v5.7.20 which requieres Java 8.

## Install Java 8 on armbian Jessie

At this point in time, the JDK shipped with armbian Jessie is OpenJDK 7.
To download `oracle-java8-jdk` and install it along with its dependencies, run:

    wget "http://archive.raspberrypi.org/debian/pool/main/o/oracle-java8-jdk/oracle-java8-jdk_8u65_armhf.deb"
    sudo apt-get update
    sudo apt-get install --no-install-recommends libasound2 libgcc1 libx11-6 libxext6 libxi6 libxrender1 libxtst6
    sudo dpkg -i oracle-java8-jdk_8u65_armhf.deb

This packages provides `java8-runtime-headless`, a dependency of the Unifi Controller software.

## Install the UniFi v5 Controller software

There are multiarch packages available for the UniFi Controller software.
For version [5.7.20](https://community.ubnt.com/t5/UniFi-Updates-Blog/UniFi-5-7-20-Stable-has-been-released/ba-p/2271529) it's:

    wget "http://dl.ubnt.com/unifi/5.7.20/unifi_sysvinit_all.deb"
    apt-get install --no-install-recommends jsvc mongodb-server
    sudo systemctl disable mongodb
    sudo dpkg -i unifi_sysvinit_all.deb

Line 3 disables the mongodb service which is not needed since the UniFi Controller starts a dedicated process.
To verify it's working, please run:

    netstat -l -t |grep 8443

and check the output:

    tcp6       0      0 [::]:8443               [::]:*                  LISTEN

The controller will be available on port 8443 then:

    https://<ip-address>:8443/

## Troubleshooting

The log files can be found in the `/var/log/unifi` directory. View them with:

    sudo tail -f /var/log/unifi/{server,mongod}.log

The `unifi` service can be started/stopped with `sudo /etc/init.d/unifi {start|stop|restart|reload|force-reload}`.

## Further information

For the lastes version of the UniFi Controller software, please check out the
[UniFi-Updates-Blog](https://community.ubnt.com/t5/UniFi-Updates-Blog/bg-p/Blog_UniFi).

[cubietruck]: http://www.cubietruck.com
[armbian]: http://www.armbian.com/
