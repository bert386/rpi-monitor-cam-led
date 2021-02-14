# -*- coding: utf-8 -*-
""" Monitor and flash LED strip as git to state transition
Description:

Todo:

"""

import os
import sys

import json
import logging
import logging.config
import subprocess
import string
import threading
import datetime
import time

import pyinotify

from transitions import Machine, State
import board
import neopixel
import smtplib

# importing states
from playing1 import Playing1stState
from playing2 import Playing2ndState
from idle import IdleState

from constants import *
from mailer import sendmail_with_attached

from gpiozero import Button
from subprocess import check_call

logging.config.fileConfig(fname="logging.conf", disable_existing_loggers=False)

########################################################################################
state_controller = None
Terminate = False
state_machine = None
########################################################################################


wm = pyinotify.WatchManager()  # Watch Manager
mask = pyinotify.IN_CLOSE_NOWRITE | pyinotify.IN_ACCESS  # watched events
PhotoFileMask = pyinotify.IN_CLOSE_WRITE
# PhotoFileMask = pyinotify.ALL_EVENTS
pixels = neopixel.NeoPixel(board.D18, 144)


class StateController(object):
    def __init__(self):
        self.logic_stop = False
        self.access_01_time = int(time.time() * 1000)
        self.access_02_time = int(time.time() * 1000)

    def start(self):
        threading.Thread(target=self.loop).start()
        self.stateChangeTime = int(time.time() * 1000)

    def loop(self):
        chase_index = 0
        while not self.logic_stop:
            try:
                if self.is_playing_1st():
                    # playing track01
                    if int(time.time() * 1000) - self.access_01_time >= 750:
                        logging.warning("Stopped playing track01 ...")
                        self.reset()
                    else:
                        pixels.fill(NORMAL_COLOR)
                        pixels.show()

                elif self.is_playing_2nd():
                    # playing track02
                    if int(time.time() * 1000) - self.access_02_time >= 750:
                        logging.warning("Stopped playing track02 ...")
                        self.reset()
                    else:
                        elpased_time = self.timeInCurrState()
                        if (elpased_time % HOTFACE_FLASH_INTERVAL) < (
                            HOTFACE_FLASH_INTERVAL / 2
                        ):
                            pixels.fill(HOTFACE_FLASH_ON_COLOR)
                        else:
                            pixels.fill(HOTFACE_FLASH_OFF_COLOR)
                        pixels.show()
                else:
                    # idle state
                    pixels.fill(IDLE_COLOR)
                    pixels.show()

            except Exception as error:
                logging.error(error, exc_info=True)
                break
            time.sleep(0.1)

    def terminate(self):
        self.logic_stop = True

    def state_changed(self):
        self.stateChangeTime = int(time.time() * 1000)

    def timeInCurrState(self):
        return int(time.time() * 1000) - self.stateChangeTime


class EventHandler(pyinotify.ProcessEvent):
    def my_init(self, file_object=sys.stdout):
        """
        This is your constructor it is automatically called from
        ProcessEvent.__init__(), And extra arguments passed to __init__() would
        be delegated automatically to my_init().
        """
        self._file_object = file_object

    def process_IN_ACCESS(self, event):
        if event.pathname == NORMAL_TRACK_PATH:
            state_controller.access_01_time = int(time.time() * 1000)
            if not state_controller.is_playing_1st():
                state_controller.enter_1st_playing()

        if event.pathname == HOTFACE_TRACK_PATH:
            state_controller.access_02_time = int(time.time() * 1000)
            if not state_controller.is_playing_2nd():
                state_controller.enter_2nd_playing()

    def process_IN_CREATE(self, event):
        if not event.dir:
            logging.warning("Capturing new photo image: {}".format(event.pathname))

    def process_IN_CLOSE_WRITE(self, event):
        if not event.dir:
            logging.warning(
                "New photo image captured, [close_write]: {}".format(event.pathname)
            )
            sendmail_with_attached(
                GMAILSENDER, GMAILAPPPASSWD, CUSTOMERMAIL, event.pathname
            )

    def process_default(self, event):
        """
        Eventually, this method is called for all others types of events.
        This method can be useful when an action fits all events.
        """
        if not event.dir:
            print(event)


def shutdown_button_pressed():
    check_call(["sudo", "poweroff"])


if __name__ == "__main__":
    """  """
    try:

        shutdown_btn = Button(SHUTDOWN_PIN, hold_time=2)
        shutdown_btn.when_held = shutdown_button_pressed

        # log.setLevel(10)
        notifier = pyinotify.ThreadedNotifier(wm, EventHandler())
        notifier.start()

        wdd01 = wm.add_watch(NORMAL_TRACK_PATH, mask)
        wdd02 = wm.add_watch(HOTFACE_TRACK_PATH, mask)
        wdd03 = wm.add_watch(PHOTO_MONITOR_PATH, PhotoFileMask, rec=True, auto_add=True)

        state_controller = StateController()
        # initialize logic states
        idle_state = IdleState(state_controller)
        playing_1st_state = Playing1stState(state_controller)
        playing_2nd_state = Playing2ndState(state_controller)

        LogicStates = [
            State(name="dummy"),
            State(
                name="idle",
                on_enter=idle_state.on_entered,
                on_exit=idle_state.on_exited,
            ),
            State(
                name="playing_1st",
                on_enter=playing_1st_state.on_entered,
                on_exit=playing_1st_state.on_exited,
            ),
            State(
                name="playing_2nd",
                on_enter=playing_2nd_state.on_entered,
                on_exit=playing_2nd_state.on_exited,
            ),
        ]

        state_machine = Machine(
            model=state_controller,
            states=LogicStates,
            initial="dummy",
            before_state_change="state_changed",
        )
        state_machine.add_transition("dummy", LogicStates, "dummy")
        state_machine.add_transition("reset", LogicStates, "idle")
        state_machine.add_transition("enter_1st_playing", LogicStates, "playing_1st")
        state_machine.add_transition("enter_2nd_playing", LogicStates, "playing_2nd")

        #
        state_controller.start()
        #
        state_controller.reset()

        while True:
            time.sleep(1.0)

    except Exception as error:
        logging.error(error, exc_info=True)

    finally:
        # terminate_servcie = True
        notifier.stop()

        if state_controller != None:
            state_controller.terminate()

        time.sleep(2.0)
        logging.warning("Fully terminated?")
        raise