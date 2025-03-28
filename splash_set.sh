#!/bin/bash

sudo echo 'disable_splash=1' >> /boot/config.txt
sudo sed -i 's/^message_sprite/#&/' /usr/share/plymouth/themes/pix/pix.script
sudo sed -i 's/^Plymouth.SetUpdate/#&/' /usr/share/plymouth/themes/pix/pix.script
sudo sed -i 's/console=tty1/console=tty3/' /boot/cmdline.txt


if grep -q splash /boot/cmdline.txt
then
	echo ' '
else
	sed -i '$s/$/ splash/' /boot/cmdline.txt
fi

if grep -q quiet /boot/cmdline.txt
then
	echo ' '
else
	sed -i '$s/$/ quiet/' /boot/cmdline.txt
fi

if grep -q plymouth.ignore-serial-consoles /boot/cmdline.txt
then
	echo ' '
else
	sed -i '$s/$/ plymouth.ignore-serial-consoles/' /boot/cmdline.txt
fi

if grep -q logo.nologo /boot/cmdline.txt
then
	echo ' '
else
	sed -i '$s/$/ logo.nologo/' /boot/cmdline.txt
fi

if grep -q vt.global_cursor_default=0 /boot/cmdline.txt
then
	echo ' '
else
	sed -i '$s/$/ vt.global_cursor_default=0/' /boot/cmdline.txt
fi

sudo cp ./logo.png /usr/share/plymouth/themes/pix/splash.png

#pcmanfm --set-wallpaper="~/Cof-Tabs/logo.png"