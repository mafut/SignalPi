#!/bin/bash

# Add apt to fix pointer issue for pygame
cat << EOF > /etc/apt/sources.list.d/wheezy.list
deb http://archive.raspbian.org/raspbian wheezy main
EOF
cat << EOF > /etc/apt/apt.conf.d/10defaultRelease
APT::Default-release "stable";
EOF
cat << EOF > /etc/apt/preferences.d/libsdl
echo "Package: libsdl1.2debian
Pin: release n=jessie
Pin-Priority: -10
Package: libsdl1.2debian
Pin: release n=wheezy
Pin-Priority: 900
EOF

# System Update
apt-get update -y --fix-missing
apt-get upgrade -y --fix-missing
apt-get install -y tslib libts-bin
apt-get install -y xinput-calibrator
apt-get install -y python-dev python-rpi.gpio
apt-get install -y busybox busybox-syslogd ntpdate
apt-get install -y --force-yes libsdl1.2debian/wheezy
apt-get remove -y --purge wolfram-engine triggerhappy anacron cron logrotate dbus fake-hwclock
apt-get autoremove -y --purge
rpi-update

# Replace log management
dpkg --purge rsyslog

# Disable Swap
dphys-swapfile swapoff
dphys-swapfile uninstall
update-rc.d dphys-swapfile disable
systemctl disable dphys-swapfile

# Get related apps
if [ ! -e /home/pi/LCD-show ]; then
    git clone https://github.com/goodtft/LCD-show.git
fi
if [ ! -e /home/pi/root-ro ]; then
    git clone https://github.com/josepsanzcamp/root-ro.git
fi

# Setup rc.local
cat << EOF > /etc/rc.local
#!/bin/sh -e
(/usr/sbin/ntpdate -b cz.pool.ntp.org)&
(/usr/bin/python /home/pi/signalpi/main.py)&
exit 0
EOF

# Setup Signalpi from X
mkdir -p /home/pi/.config/autostart/
cat << EOF > /home/pi/.config/autostart/signalpi.desktop
[Desktop Entry]
Type=Application
Name=signalpi
Exec=/usr/bin/python /home/pi/signalpi/main.py
Terminal=false
EOF
chown -R pi /home/pi/.config/autostart/
chgrp -R pi /home/pi/.config/autostart/
