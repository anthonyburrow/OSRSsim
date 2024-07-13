import pickle

from .Bank import Bank
from .Stat import Stat
from ..colors import color, COLOR_CHARACTER
from ...lib import stats


class Player:

    def __init__(self, save_file: str):
        self.name: str = input('Character name?\n> ')
        self.save_file: str = save_file

        self._bank: Bank = Bank()

        self._stats = {}
        self._setup_stats()

    # Stats and Experience
    def add_XP(self, stat: str, XP: float):
        self._stats[stat].add_XP(XP)

    def set_XP(self, stat: str, XP: float):
        self._stats[stat].set_XP(XP)

    def set_level(self, stat: str, level: int):
        self._stats[stat].set_level(level)

    def get_stat(self, stat: str) -> Stat:
        return self._stats[stat]

    def _setup_stats(self):
        for stat, stat_name in stats.items():
            self._stats[stat] = Stat(stat_name)

    # Items
    def give(self, *args, **kwargs):
        self._bank.add(*args, **kwargs)

    def has(self, *args, **kwargs) -> bool:
        return self._bank.contains(*args, **kwargs)

    @property
    def bank(self) -> Bank:
        return self._bank

    # Management
    def save(self):
        with open(self.save_file, 'wb') as file:
            pickle.dump(self, file)

    # Misc
    def __str__(self):
        text: str = f'{self.name}'
        return color(text, COLOR_CHARACTER)

