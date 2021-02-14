# -*- coding: utf-8 -*-
""" Base Logic State class  
Description:

Todo:

"""

import os
import sys
import logging
import time
import threading


class BaseState(object):
    """Base class for logic stage
    Args:
        state_controller: Class instance for main State_Controller
        in_state_callback:
    """

    def __init__(self, state_controller, in_state_callback=None):
        self._thread_stop = False
        self.in_state_callback = in_state_callback
        self.state_controller = state_controller

    @classmethod
    def decorator_enter(cls, func):
        def wrapper(self, *args, **kwargs):
            try:
                time.sleep(0.01)
                func(self, *args, **kwargs)
                logging.info(
                    "Started thread of logic state for {}... ".format(
                        self.state_controller.state
                    )
                )
                self._thread_stop = False
                self._thread_instance = threading.Thread(target=self.in_state_proc)
                if self.in_state_callback != None:
                    self._thread_instance.start()
                return
            except Exception as error:
                logging.error(repr(error), exc_info=True)

        return wrapper

    def in_state_proc(self):
        """ Instate thread procedure to call logic method of child class  """
        while self._thread_stop == False:
            try:
                if self.in_state_callback != None:
                    self.in_state_callback()
                time.sleep(0.05)
            except Exception as error:
                logging.error(repr(error), exc_info=True)
        logging.info("Finished thread of logic state ... ")

    @classmethod
    def decorator_exit(cls, func):
        def wrapper(self, *args, **kwargs):
            try:
                self._thread_stop = True
                time.sleep(0.05)
                func(self, *args, **kwargs)
                return
            except Exception as error:
                logging.error(repr(error), exc_info=True)

        return wrapper
