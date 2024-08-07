from ....util.structures.Activity import Activity, Status
from ....util.structures.LootTable import LootTable
from ....util.structures.Bank import Bank
from ....lib.skilling.smithing import smithables, Smithable
from ....lib.skilling.woodcutting import logs


fire_effect = 'smithing fire'


class SmithingActivity(Activity):

    def __init__(self, *args):
        super().__init__(*args)

        argument = ' '.join(args[1:])
        if argument in smithables:
            self.smithable: Smithable = smithables[argument]
        else:
            self.smithable: Smithable = None

        self.description: str = 'smithing'

        self.loot_table: LootTable = None

    def setup_inherited(self, status: dict) -> dict:
        if self.smithable is None:
            status['success'] = False
            status['msg'] = \
                'A valid item was not given.'
            return status

        skill_level: int = self.player.get_level('smithing')
        if skill_level < self.smithable.level:
            status['success'] = False
            status['msg'] = \
                f'{self.player} must have Level {self.smithable.level} Smithing to smith a {self.smithable.name}.'
            return status

        if not self.player.has_effect(fire_effect):
            for log_key, log in logs.items():
                if self.player.has(log.name):
                    break
            else:
                status['success'] = False
                status['msg'] = \
                    f'{self.player} has no logs to fuel a furnace.'
                return status

        for item, quantity in self.smithable.items_required.items():
            if self.player.has(item, quantity):
                continue

            msg = f'{self.player} does not have {quantity}x {item}.'
            status['success'] = False
            status['msg'] = msg
            return status

        self._setup_loot_table()

        return status

    def update_inherited(self) -> dict:
        '''Processing during each tick.'''
        # Do checks
        ticks_per_action = self.smithable.ticks_per_action
        if self.tick_count % ticks_per_action:
            return {
                'status': Status.STANDBY,
                'msg': self.standby_text,
            }

        for item, quantity in self.smithable.items_required.items():
            if self.player.has(item, quantity):
                continue

            msg = f'{self.player} ran out of {item}.'
            return {
                'status': Status.EXIT,
                'msg': msg,
            }

        if not self.player.has_effect(fire_effect):
            for log_key, log in logs.items():
                if self.player.has(log.name):
                    self.player.remove(log.name, 1)
                    self.player.add_effect(fire_effect, log.ticks_per_fire)
                    break
            else:
                msg = f'{self.player} ran out of logs.'
                return {
                    'status': Status.EXIT,
                    'msg': msg,
                }

        # Process the item
        for item, quantity in self.smithable.items_required.items():
            self.player.remove(item, quantity)

        items: Bank = self.loot_table.roll()

        msg = f'Smithed a {self.smithable.name}!'

        return {
            'status': Status.ACTIVE,
            'msg': msg,
            'items': items,
            'XP': {
                'smithing': self.smithable.XP,
            },
        }

    def finish_inherited(self):
        pass

    def reset_on_levelup(self):
        self._setup_loot_table()

    @property
    def startup_text(self) -> str:
        return f'{self.player} is now smithing a {self.smithable.name}.'

    @property
    def standby_text(self) -> str:
        return 'Smithing...'

    @property
    def finish_text(self) -> str:
        return f'{self.player} finished {self.description}.'

    def _setup_loot_table(self):
        self.loot_table = LootTable()
        self.loot_table.every(
            self.smithable.name, 1
        )

        # Add more stuff (pets, etc)


def detailed_info():
    msg: list = []

    msg.append('Use cases:')
    msg.append('- smith [item]')

    msg.append('')

    msg.append('Available items:')
    for smithable in smithables:
        name = str(smithable).capitalize()
        msg.append(f'- {name}')

    return '\n'.join(msg)
