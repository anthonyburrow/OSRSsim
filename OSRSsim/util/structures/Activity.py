import time
import keyboard

from . import Player
from .. import Controller
from ..ticks import seconds_per_tick
from ..output import print_output
from ..commands import KEY_CANCEL
from ..misc import client_focused


class Activity:

    def __init__(self, controller: Controller, *args):
        self.player: Player = controller.player
        self.client_ID = controller.client_ID

        self.tick_count: int = 0
        self.in_standby = False

    def setup(self) -> dict:
        '''Check to see if requirements are met to perform activity.'''
        status = {
            'success': True,
            'status_msg': '',
        }

        if self.player.is_busy:
            status['success'] = False
            status['status_msg'] = \
                f'{self.player} is busy.'
            return status

        # Setup for inherited classes
        status = self.setup_inherited(status)

        return status

    def begin_loop(self):
        '''Begin activity loop.'''
        print_output(self.startup_text)

        while True:
            if keyboard.is_pressed(KEY_CANCEL) and client_focused(self.client_ID):
                self.finish()

                msg = f'{self.player} is returning from {self.description}...'
                print_output(msg)
                time.sleep(seconds_per_tick * 4.)
                break

            # TODO: async timing, ditch all the time subtract
            start = time.time()
            self.update()
            time_passed = time.time() - start

            time_to_wait = seconds_per_tick - time_passed
            if time_to_wait > 0:
                time.sleep(time_to_wait)

    def update(self):
        '''Processing during the tick.'''
        status = self.update_inherited()
        now_in_standby = status['status'] == 'standby'
        if now_in_standby != self.in_standby:
            self.in_standby = now_in_standby
            print_output(status['status_msg'])

        self.tick_count += 1

    def finish(self) -> str:
        # Return message, add loot to user, etc
        print_output(self.finish_text)

        self.finish_inherited()

        return ''