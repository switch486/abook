# abook - the audio-book reader
A Raspberry Pi based audiobook reader.

# BOM
Consisting of:
- Raspberry pi - https://www.raspberrypi.com/products/raspberry-pi-3-model-b-plus/
- Button shield - https://shop.pimoroni.com/products/button-shim?variant=45854302218
- LCD shield - https://botland.com.pl/wyswietlacze-alfanumeryczne-i-graficzne/2640-wyswietlacz-lcd-4x20-znakow-niebieski-konwerter-i2c-lcm1602-5904422331061.html
- some soldering
- this software

# HW Setup - Wiring guide

TBD

# HW Setup - Bricks enclosure with button breakout

TBD

# Software Setup Guide

## SW installation

- RPI
- internet - WIFI
- SSH? i2c?
- python
- python libs
- service setup --- https://forums.raspberrypi.com/viewtopic.php?f=29&t=7192&p=828947#p828947
https://forums.raspberrypi.com/viewtopic.php?p=921354#p921354

$ sudo cp   abook.service  /etc/systemd/system/
$ sudo chmod u+rwx /etc/systemd/system/abook.service
$ sudo systemctl status abook
$ sudo systemctl start abook
$ sudo systemctl stop abook


## Testing the HW Setup

-- i2c debugging
-- venv python

# Preparation for operative work

## Folder structure in USB Memmory Stick

-- root
-- folders
-- files
-- abook files

# Supported Use Cases within abook

## select cast device - TBD
## folder structure jumping around - TBD
## select audiobook - TBD
## playback manipulations - TBD

TODO - 
-task - split mp3s based on chapters and Secondly by 5 minute parts
-TEST FIX - logs to outside 
-bug - usb hangs after a while
-bug - when navigate back from playing track, the http server stopps and hangs

