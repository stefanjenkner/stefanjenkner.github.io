---
layout: post
title:  "Docker on Cubietruck"
date:   2016-02-06 15:09:23
categories: docker cubietruck armbian systemd
---

To get started with [Docker][docker] on [Cubietruck][cubietruck] (also know as
Cubieboard 3), it's necessary to switch to a more recent Vanilla kernel.
My distribution of choice was [armbian][armbian] (a lightweight Linux
distribution based on Debian Wheezy, Jessie or Ubuntu Trusty).

## Get armbian

Prepare your SD-Card with Debian Jessie and the Vanilla kernel.
My setup runs: Armbian_4.5_Cubietruck_Debian_jessie_4.2.3.zip.
Get it from here: <http://www.armbian.com/cubietruck/>

## Enable systemd

[systemd][systemd] is disabled by default on Debian Jessie based
[armbian][armbian]. To enable it, remove the `ramlog` Package due to an
incompatibility with the `systemd` Package:

    apt-get remove --purge ramlog

To enable [systemd][systemd] run:

    apt-get update
    apt-get install --no-install-recommends systemd-sysv fake-hwclock

Then just reboot.

    reboot

There is no need to recompile boot scripts.

## Install Docker

Thanks to folks at [Hypriot][hypriot], it's quiet easy to get docker binaries
for the ARM architecture:

    wget "http://downloads.hypriot.com/docker-hypriot_1.10.0-1_armhf.deb"
    sudo dpkg -i docker-hypriot_1.10.0-1_armhf.deb

To start [Docker][docker] run:

    sudo systemctl start docker

To enable [Docker][docker] on [system boot][docker-start-stop]:

    sudo systemctl enable docker

Verify the result with:

    sudo docker info

Expected output should be like this:

    Containers: 0
     Running: 0
     Paused: 0
     Stopped: 0
    Images: 0
    Server Version: 1.10.0
    Storage Driver: overlay
     Backing Filesystem: extfs
    Execution Driver: native-0.2
    Logging Driver: json-file
    Plugins:
     Volume: local
     Network: null host bridge
    Kernel Version: 4.2.3-sunxi
    Operating System: Debian GNU/Linux 8 (jessie)
    OSType: linux
    Architecture: armv7l
    CPUs: 2
    Total Memory: 1.969 GiB
    Name: nepomuk
    ID: FZT4:I4JM:6PIG:BY55:KUOG:7P57:PV6U:QHAY:2PD5:XLZR:MOIF:W6B5
    Debug mode (server): true
     File Descriptors: 11
     Goroutines: 20
     System Time: 2016-02-06T01:57:59.080651972+01:00
     EventsListeners: 0
     Init SHA1: 357816754f63702bece2e1a3db651d7f2527a78c
     Init Path: /usr/lib/docker/dockerinit
     Docker Root Dir: /var/lib/docker

## Further information

For additional information regarding [Docker][docker] on ARM, check out the
[Hypriot Blog][hypriot-blog] and their
[Raspberry Pi compatible Docker Image](https://hub.docker.com/u/hypriot/)
on Docker Hub.

[docker]: https://www.docker.com/
[cubietruck]: http://www.cubietruck.com
[systemd]: https://wiki.freedesktop.org/www/Software/systemd/
[hypriot]: http://blog.hypriot.com/downloads/
[hypriot-blog]: http://blog.hypriot.com/getting-started-with-docker-on-your-arm-device/
[armbian]: http://www.armbian.com/
[docker-start-stop]: https://docs.docker.com/engine/admin/systemd/
