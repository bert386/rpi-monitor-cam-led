# -*- coding: utf-8 -*-
"""   
Description:

Todo:

"""

import os
import sys
import logging
from collections import deque
from base_state import BaseState


class IdleState(BaseState):
    """"""

    def __init__(self, state_controller):
        super().__init__(state_controller, self.in_state)

    @BaseState.decorator_enter
    def on_entered(self):
        logging.warning("Idle state ...")

    def in_state(self):
        pass

    @BaseState.decorator_exit
    def on_exited(self):
        pass