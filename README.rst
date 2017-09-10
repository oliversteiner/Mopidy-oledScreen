****************************
Mopidy-oledScreen
****************************

.. image:: https://img.shields.io/pypi/v/Mopidy-oledScreen.svg?style=flat
    :target: https://pypi.python.org/pypi/Mopidy-oledScreen/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/travis/tulip85/mopidy_oledScreen/master.svg?style=flat
    :target: https://travis-ci.org/tulip85/mopidy_oledScreen
    :alt: Travis CI build status

.. image:: https://img.shields.io/coveralls/tulip85/mopidy_oledScreen/master.svg?style=flat
   :target: https://coveralls.io/r/tulip85/mopidy_oledScreen
   :alt: Test coverage

Mopidy extension to display currently playing song to a small oled screen (currently only tested on ssd1306 via i2c)

It uses the LUMA oled screen driver: https://github.com/rm-hull/luma.oled
Also included are the bitstream vera fonts for display. 

Installation
============

First install the LUMA oled library: https://github.com/rm-hull/luma.oled, installation instructions: https://luma-oled.readthedocs.io/en/latest/install.html

Install by running::

    sudo pip install Mopidy-oledScreen

Or, if available, install the Debian/Ubuntu package from `apt.mopidy.com
<http://apt.mopidy.com/>`_.


Configuration
=============

Before starting Mopidy, you must add configuration for
Mopidy-oledScreen to your Mopidy configuration file::

    [oledScreen]
    enabled = true
	bus = 2
	address = 0x3c
	driver = ssd1306

The following configuration values are avialble:
- oledScreen/enabled: if the screen should be used or not
- oledScreen/bus: the i2c bus interface the oled screen is connected to (the bus number you use in i2cdetect -y busNumber)
- oledScreen/address: the address the oled screen listens to (the output from i2cdetect -y busNumber)
- oled/driver: the luma oled driver name, valid values are: ssd1306 / ssd1322 / ssd1325 / ssd1331 / sh1106, currently only tested on ssd1306 via i2c

Project resources
=================

- `Source code <https://github.com/tulip85/mopidy-oledscreen>`_
- `Issue tracker <https://github.com/tulip85/mopidy-oledscreen/issues>`_


Changelog
=========

v0.1.0 (UNRELEASED)
----------------------------------------

- Initial release.