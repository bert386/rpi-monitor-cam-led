# rpi-monitor-cam-led
 
- *Monitoring playing 2 wav tracks on the local filesystem*
- *As fit to playing track or idle state, showing/flashing LED strip*
- *Monitoring captured photo images from another application and mail image via Gmail service to specified address*

# Components

1) RPi 4B
2) 5V WS2812b led strip 144 led/m
3) SparkFun Logic Level Converter (BiDirectional)
4) 5V/10A DC power


# Installaion dependencies

```
 sudo apt update
 sudo apt-get install inotify-tools unzip -y
 sudo pip3 install pyinotify
 sudo pip3 install rpi_ws281x
 sudo apt-get install scons -y 
 sudo pip3 install adafruit-circuitpython-neopixel
 sudo pip3 install transitions
``` 
