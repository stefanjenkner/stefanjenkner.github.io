Title: Setup Pimoroni OnOff SHIM using Device Tree Overlays
Date: 2024-03-30 00:00
Modified: 2024-03-30 00:00
Category: Hardware
Tags: rapsberrypi, shim, onoff, bookworm
Slug: 2024-03-30-pimoroni-onoff-shim-dtoverlay
Authors: Stefan Jenkner
Summary: The OnOff SHIM by Pimoroni is a convenient power switch for the Raspberry Pi. The official guide suggests to install a daemon to initiate a clean shutdown once the button is pressed. However, there is much simpler solution using device tree overlays avoiding additional 3rd party tools.

The [OnOff SHIM by Pimoroni](https://shop.pimoroni.com/products/onoff-shim) is a convenient power switch for the Raspberry Pi.
The official guide suggests to install a daemon to initiate a clean shutdown once the button is pressed.
However, there is much simpler solution using device tree overlays avoiding additional 3rd party tools.
Furthermore, the "old" daemon solution does no longer work on Debian Bookworm based distributions and is a using sysv-based init script.

Given the [pinout of the shim](https://pinout.xyz/pinout/onoff_shim), the solution is to watch PIN 17 and initiates a clean shutdown when the button is pressed (pulled low). And just before the the Pi shuts down, PIN 4 is pulled low to completely cut the power. Enabling it is as easy as adding this to `/boot/firmware/config.txt` and reboot:

```
dtoverlay=gpio-shutdown,gpio_pin=17,active_low=1,gpio_pull=up
dtoverlay=gpio-poweroff,gpiopin=4,active_low=1
```

Please check <https://github.com/raspberrypi/firmware/blob/master/boot/overlays/README> for further details.
This solution was tested with Raspberry Pi OS 12 (Debian Bookworm based) and a Raspberry Pi Zero.
