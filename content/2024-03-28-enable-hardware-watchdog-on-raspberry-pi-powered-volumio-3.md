Title: Enable hardware watchdog for Volumio 3 on Raspberry Pi
Date: 2024-03-28 00:00
Modified: 2024-03-28 00:00
Category: Audio
Tags: volumio, rapsberrypi, watchdog
Slug: 2024-03-28-enable-hardware-watchdog-on-raspberry-pi-powered-volumio-3
Authors: Stefan Jenkner
Summary: Enable hardware watchdog on Raspberry Pi powered Volumio 3

The Raspberry Pi features a built-in hardware watchdog timer that automatically resets the system if it becomes unresponsive or freezes.
If enabled, it expects the OS to reset the hardware watchdog every 15 seconds - otherwise the hardware watchdog will initiate a system reboot.
Given that [systemd provides support for hardware watchdogs](http://0pointer.de/blog/projects/watchdog.html),
there is no need to install additional userspace tools - at least not for basic hardware reset functionality.

As a prerequiste, [SSH must be enabled](https://developers.volumio.com/SSH%20Connection#how-to-enable-ssh) temporarily in Volumio.
After successful login, the Device Tree parameter for watchdog can be configured:

```bash
echo 'dtparam=watchdog=on' |sudo tee -a /boot/userconfig.txt
```

After reboot, the next step is to uncomment and change `RuntimeWatchdogSec` and `ShutdownWatchdogSec` in `/etc/systemd/system.conf`

```bash
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
