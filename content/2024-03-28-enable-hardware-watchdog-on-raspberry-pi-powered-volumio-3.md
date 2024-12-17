---
Title: Enable hardware watchdog on Raspberry Pi-powered Volumio audio player
Date: 2024-03-28 00:00
Modified: 2024-03-29 00:00
Category: Audio
Tags: volumio, raspberrypi, watchdog
Slug: 2024-03-28-enable-hardware-watchdog-on-raspberry-pi-powered-volumio-3
Authors: Stefan Jenkner
Summary: The Raspberry Pi features a built-in hardware watchdog timer that automatically resets the system if it becomes unresponsive or freezes. This can be handy when used as an audio player like Volumio - especially if the hardware is not easy to access.
---

The Raspberry Pi features a built-in hardware watchdog timer that automatically resets the system if it becomes unresponsive or freezes.
If enabled, it expects the OS to reset the hardware watchdog every 15 seconds. Otherwise the hardware watchdog initiates a system reboot.
This can be handy when used as an audio player like [Volumio](https://volumio.com) especially if the hardware is not easy to access.

Given that [systemd provides support for hardware watchdogs](http://0pointer.de/blog/projects/watchdog.html),
there is no need to install userspace tools for basic hardware reset functionality.
The activation requires temporary [SSH access](https://developers.volumio.com/SSH%20Connection#how-to-enable-ssh) in Volumio.
After successful login, the Device Tree parameter for watchdog is ready for configuration:

```
echo 'dtparam=watchdog=on' |sudo tee -a /boot/userconfig.txt
```

After reboot, the next step is to comment out and change `RuntimeWatchdogSec` and `ShutdownWatchdogSec` in `/etc/systemd/system.conf`

```
sudo vi /etc/systemd/system.conf
```

```
RuntimeWatchdogSec=14
ShutdownWatchdogSec=2min
```

* `RuntimeWatchdogSec=14` - controls the keep-alive ping interval but systemd pings the hardware at half the specified interval (every 7 seconds)
* `ShutdownWatchdogSec=2min` - controls the watchdog interval to use during reboots

The changes can applied via `sudo systemctl daemon-reload` (or a reboot) and tested via
the classic [fork bomb](https://en.wikipedia.org/wiki/Fork_bomb)

```bash
:(){ :|:& };:
```

Once executed, the system will become unresponsive so the watchdog initiates a reboot.
