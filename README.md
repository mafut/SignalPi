# README #

This is simple project to control 6 LEDs with raspberry pi 3.
Raspberry pi 3 also expects to have 3.5" LCD connected to GPIO.

### Required hardwares ###

* Raspberry Pi 3
* [GPIO connected 3.5" LCD](http://www.raspberrypiwiki.com/index.php/3.5_inch_TFT_LCD_Touch_Screen_SKU:363295)
* [Pi Traffic Light](http://lowvoltagelabs.com/products/pi-traffic/)

### How do I get set up? ###

1. Flash raspbian-stretch 2017-09-07 to SD by Windows or Mac
1. Download apps and setup
	1. git clone https://bitbucket.org/mafut/signalpi.git
	1. chmod 755 signalpi/setup.sh
	1. ./signalpi/setup.sh
1. Enable 3.5" LCD
	1. chmod -R 755 LCD-show
	1. cd LCD-show/
	1. ./LCD35-show
	1. ./LDC-html if revert back
1. Enable Read-Only
	1. Add "fastboot noswap ro" at the end of line in /boot/cmdline.txt
	1. Move lock, run, spool
	rm -rf  /var/lock /var/run /var/spool
	ln -s /tmp /var/lock
	ln -s /tmp /var/run
	ln -s /tmp /var/spool
	1. Move dhcp
	rm -rf /var/lib/dhcp
	ln -s /tmp /var/lib/dhcp
	touch /tmp/dhcpcd.resolv.conf
	rm /etc/resolv.conf
	ln -s /tmp/dhcpcd.resolv.conf /etc/resolv.conf
	1. Remove startup
	insserv -r bootlogs
	insserv -r console-setup
	1. Update /etc/fstab to flag as read only
	/dev/mmcblk0p1    /boot    vfat    defaults,ro    0    2
	/dev/mmcblk0p2    /        ext4    defaults,ro    0    1
	1. Add the following to /etc/fstab
	tmpfs    /var/log    tmpfs    nosuid,nodev    0    0
	tmpfs    /var/tmp    tmpfs    nosuid,nodev    0    0

### More ###
* Calibrate (X) if needed
	1. DISPLAY=:0.0 xinput_calibrator
	1. Take memo calibration data
	1. nano /etc/X11/xorg.conf.d/99-calibration.conf
	1. reboot
