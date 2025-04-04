---
Title: Setup Pimoroni OnOff SHIM using Device Tree Overlays
Date: 2024-03-30 00:00
Modified: 2024-03-30 00:00
Category: Hardware
Tags: raspberrypi, shim, onoff, bookworm
Slug: 2024-03-30-pimoroni-onoff-shim-dtoverlay
Authors: Stefan Jenkner
Summary: The OnOff SHIM by Pimoroni is a convenient power switch for the Raspberry Pi. The official guide suggests to install a daemon that initiates a clean shutdown on button press. A much simpler solution is to use device tree overlays and avoid 3rd-party tools.
---

The [OnOff SHIM by Pimoroni](https://shop.pimoroni.com/products/onoff-shim) is a convenient power switch for the Raspberry Pi.
The official guide suggests to install a daemon that initiates a clean shutdown on button press.
A much simpler solution is to use device tree overlays and avoid 3rd-party tools.
Furthermore, the "old" daemon solution does no longer work on Debian Bookworm based distributions and is a using sysv-based init script.

Given the [pin-out of the shim](https://pinout.xyz/pinout/onoff_shim), the solution is to watch PIN 17 and initiates a clean shutdown on press button (pulled low). And just before the Pi shuts down, PIN 4 gets pulled low to cut the power. Enabling is as easy as adding this to `/boot/firmware/config.txt` and reboot:

```
dtoverlay=gpio-shutdown,gpio_pin=17,active_low=1,gpio_pull=up
dtoverlay=gpio-poweroff,gpiopin=4,active_low=1
```

Please check <https://github.com/raspberrypi/firmware/blob/master/boot/overlays/README> for further details.
This solution works on Raspberry Pi OS 12 (Debian Bookworm based) and a Raspberry Pi Zero or later.
