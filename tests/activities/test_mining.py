from Pydle.util.structures.Player import Player
from Pydle.util.structures.Controller import Controller
from Pydle.util.input import parse_command

from Pydle.commands.activities.skilling import MiningActivity


def test_missing_pickaxe():
    # Setup
    player = Player(name='TestPlayer')

    player.set_level('mining', 99)
    controller = Controller(player)

    command = 'mine iron'
    command = parse_command(command)

    # Test no pickaxe
    activity = MiningActivity(controller, *command['args'])
    status = activity.setup()

    assert not status['success']

    # Test has pickaxe
    player.give('iron pickaxe')
    player.equip_tool('iron pickaxe')

    activity = MiningActivity(controller, *command['args'])
    status = activity.setup()

    assert status['success']


def test_misspelled_ore():
    # Setup
    player = Player(name='TestPlayer')

    player.set_level('mining', 99)
    controller = Controller(player)

    command = 'mine irn'
    command = parse_command(command)

    # Test misspelled command
    player.give('iron pickaxe')
    player.equip_tool('iron pickaxe')

    activity = MiningActivity(controller, *command['args'])
    status = activity.setup()

    assert not status['success']
