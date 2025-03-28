# Friction_PD20s
This friction setup with PD20s instead of HX711. We decide to use PD20s transistor because with HX711 module we're getting too much noise.

Connect a 2.2K resistor to the signal leg of the proximity sensor

## Raspberry pi 7 inch screen keyboard is typing letters twice. To solve this problem, we follow the steps below:

1. Enter the following command into the terminal.

```sudo nano ~/.kivy/config.ini```
2. Then, comment the %(name)s = probesysfs line in the code that opens. Save the file.
#%(name)s = probesysfs

## To run the program directly on the opening screen, follow the steps below:
[Example web page](https://forums.raspberrypi.com/viewtopic.php?t=294014)

1. Enter the following commands into the terminal in order.

  ```sudo nano /etc/xdg/lxsession/LXDE-pi/autostart```

  ```mkdir /home/pi/.config/lxsession```

  ```mkdir /home/pi/.config/lxsession/LXDE-pi```

  ```cp /etc/xdg/lxsession/LXDE-pi/autostart /home/pi/.config/lxsession/LXDE-pi/autostart```

2. Enter the following command in the terminal, then enter the following value at the bottom of the opened code line and save the file.
@lxterminal -e python3 /home/pi/Cof-Tabs/main.py

3. To put a company logo on the start screen.
[Example web page](https://www.tomshardware.com/how-to/custom-raspberry-pi-splash-screen)

  ```cd /usr/share/plymouth/themes/pix/```

  ```sudo mv splash.png splash.png.bk```

  ```$ sudo cp /home/pi/Cof-Tabs/splash.png ./```
 
If you encounter more problems, say **R** and **A** and **N** and **A** 3 times and you can solve the problem.
