v.1.0

Forked from
https://github.com/oliversteiner/Mopidy-oledScreen

****************************
Mopidy-oledScreen
****************************


Mopidy extension to display currently playing song to a small oled screen (currently only tested on ssd1306 via i2c)

It uses the LUMA oled screen driver: https://github.com/rm-hull/luma.oled
Also included are the bitstream vera fonts for display. 

Installation
============

First install the LUMA oled library: https://github.com/rm-hull/luma.oled, installation instructions: https://luma-oled.readthedocs.io/en/latest/install.html

Install by running::


Configuration
=============

Before starting Mopidy, you must add configuration for
Mopidy-oledScreen to your Mopidy configuration file::

    [oledScreen]
    enabled = true
    bus = 2
    address = 0x3c
    driver = ssd1306

The following configuration values are available:

- ``oledScreen/enabled``: if the screen should be used or not, defaults to true
- ``oledScreen/bus``: the i2c bus interface the oled screen is connected to (the bus number you use in i2cdetect -y busNumber), defaults to 2
- ``oledScreen/address``: the address the oled screen listens to (the output from i2cdetect -y busNumber) defaults to 0x3c
- ``oled/driver``: the luma oled driver name, valid values are: ssd1306 / ssd1322 / ssd1325 / ssd1331 / sh1106, currently only tested on ssd1306 via i2c, defaults to ssd1306

