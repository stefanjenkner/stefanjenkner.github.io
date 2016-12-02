---
layout: post
title:  "Testing and patching Cubietruck for Dirty COW vulnerability"
date:   2016-12-02 22:53:13
categories: armbian docker arm security linux 
---

Recently, I stumbled across the [Fix Dirty COW on Raspberry Pi the Docker way][hypriot-blog] guide by [Hypriot][hypriot].
As it's related to RPis, this is how to test and fix a [Cubietruck][cubietruck] running [armbian][armbian] 
for that kind of [kernel security vulnerability][dirty-cow-explained].

Step 1. - Verify kernel version:

    $ uname -a
    Linux nepomuk 4.7.3-sunxi #26 SMP Wed Sep 14 19:50:18 CEST 2016 armv7l GNU/Linux
   
Step 2. - Test the kernel for Dirty COW vulnerability:

    $ docker run --rm hypriot/rpi-dirtycow
    Unable to find image 'hypriot/rpi-dirtycow:latest' locally
    latest: Pulling from hypriot/rpi-dirtycow
    38070c4d0c33: Pull complete 
    a3ed95caeb02: Pull complete 
    2d2e2d46b9b5: Pull complete 
    Digest: sha256:065d979dd3c48e6488044206ec782628ecf241ef02104610c076949d9881ad0d
    Status: Downloaded newer image for hypriot/rpi-dirtycow:latest
    
    Test for Dirty Cow:
      $ echo "You are SAFE!          " > foo
      $ chmod 404 foo
      $ ./dirtyc0w foo "You are VULNERABLE!!!" &
      $ sleep 2
      $ cat foo
    You are VULNERABLE!!!  
    
Step 3. - Upgrade the kernel:

    $ sudo apt-get update && sudo apt-get -u dist-upgrade
    ...
    Reading package lists... Done
    Building dependency tree       
    Reading state information... Done
    Calculating upgrade... Done
    The following packages will be upgraded:
      linux-dtb-next-sunxi linux-firmware-image-next-sunxi linux-headers-next-sunxi linux-image-next-sunxi linux-jessie-root-next-cubietruck
    5 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.
    Need to get 0 B/26.3 MB of archives.
    After this operation, 2,637 kB of additional disk space will be used.
    Do you want to continue? [Y/n]
    ...
    Processing triggers for systemd (215-17+deb8u5) ...
    Setting up linux-dtb-next-sunxi (5.23) ...
    Setting up linux-firmware-image-next-sunxi (5.23) ...
    Setting up linux-image-next-sunxi (5.23) ...
    Setting up linux-jessie-root-next-cubietruck (5.23) ...
    
Step 4. - Reboot the machine:

    $ sudo reboot
    
Step 5. - Test again:

    $ docker run --rm hypriot/rpi-dirtycow
    Test for Dirty Cow:
      $ echo "You are SAFE!          " > foo
      $ chmod 404 foo
      $ ./dirtyc0w foo "You are VULNERABLE!!!" &
      $ sleep 2
      $ cat foo
    You are SAFE!  

Step 6. - Verify the new kernel version:

    $ uname -a
    Linux nepomuk 4.8.4-sunxi #6 SMP Sun Oct 23 15:55:47 CEST 2016 armv7l GNU/Linux
    
The Cubietruck is now running Linux version 4.8.4.


[docker]: https://www.docker.com/
[dirty-cow-explained]: http://www.theregister.co.uk/2016/10/21/linux_privilege_escalation_hole/
[docker]: https://www.docker.com/
[cubietruck]: http://www.cubietruck.com
[hypriot]: http://blog.hypriot.com/downloads/
[hypriot-blog]: https://blog.hypriot.com/post/fix-dirty-cow-on-raspberry-pi/
[armbian]: http://www.armbian.com/
[docker-start-stop]: https://docs.docker.com/engine/admin/systemd/