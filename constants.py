# -*- coding: utf-8 -*-
""" Monitor and flash LED strip as git to state transition
Description:

Todo:

"""
IDENTIFIER = "Warehouse/SecondPi"  # Location/Identifier of Pi, we could see it in mails

### definition of path of tracks to monitor  ###
NORMAL_TRACK_PATH = "/home/pi/Qt_projects/linux_honhwai_dinglei_new/1_en.mp3"
HOTFACE_TRACK_PATH = "/home/pi/Qt_projects/linux_honhwai_dinglei_new/2_en.mp3"
PHOTO_MONITOR_PATH = "/home/pi/Desktop/Savepic/Alarm"
### definition of path of tracks to monitor  ###

### definition of gmail credentials  ###
GMAILSENDER = "[sender mail address]"
GMAILAPPPASSWD = "app password in gmail account"
CUSTOMERMAIL = "[receiver mail addreess]"
### definition of gmail credentials  ###


### definition of LED colors ###
IDLE_COLOR = (127, 127, 127)  # Idle state color
NORMAL_COLOR = (0, 127, 0)  # Green color
HOTFACE_FLASH_ON_COLOR = (127, 0, 0)  # red
HOTFACE_FLASH_OFF_COLOR = (0, 0, 0)  # black
HOTFACE_FLASH_INTERVAL = 500  # ms unit, 500ms = 2Hz blinking rate
### definition of LED colors ###

SHUTDOWN_PIN = 17