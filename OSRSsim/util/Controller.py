import sys

from .structures import Player, Activity
from .output import print_output
from .input import parse_command, flush_input


class Controller:

    def __init__(self, player: Player):
        self.player: Player = player

    def loop(self):
        while True:
            self.listen()

    def listen(self):
        flush_input()
        command: str = input('> ')
        command: dict = parse_command(command)

        if command['type'] == 'activity':
            self.control_activity(command)
        elif command['type'] == 'exit':
            sys.exit()
        else:
            print('Unknown command.')

    def control_activity(self, command: dict):
        _activity: Activity = command['activity']
        _activity_args: tuple = command['args']

        activity = _activity(self.player, *_activity_args)

        setup = activity.setup()
        if not setup['success']:
            print_output(setup['status_msg'])
            return

        activity.begin_loop()
