import numpy as np

from ..colors import color, color_theme, skill_to_color
from . import Player


MAX_LEVEL: int = 126
MAX_XP: float = 2e8


def level_to_XP(level):
    prev_levels = np.arange(1, level)
    inner = np.floor(prev_levels + 300. * 2.**(prev_levels / 7.))
    XP = int(0.25 * inner.sum())
    return XP


XP_table = {lvl: level_to_XP(lvl) for lvl in range(1, MAX_LEVEL + 1)}


def level_up_msg(player: Player, skill_key: str):
    skill = player.get_skill(skill_key)

    level = skill.level
    if level >= 99:
        level = color(level, color_theme['skill_lvl99'])

    msg = f"{player}'s {skill} level has increased to Level {level}!"

    return msg


class Skill:

    def __init__(self, name: str, skill_type: str, XP: float = 0.):
        self.name: str = name
        self.skill_type: str = skill_type

        self.XP: float = 0.
        self.level: int = 1
        if XP > 0.:
            self.set_XP(XP)

    def add_XP(self, amount: float) -> dict:
        if self.XP >= MAX_XP:
            return

        new_XP = self.XP + amount
        if new_XP < MAX_XP:
            self.XP = new_XP
        else:
            self.XP = MAX_XP

        return self._adjust_level()

    def set_XP(self, value: float):
        if value > MAX_XP:
            value = MAX_XP
        self.XP = value

        self._adjust_level()

    def set_level(self, level: int):
        self.level = level
        self.XP = XP_table[level]

    def details(self) -> str:
        level = self.level
        if level >= 99:
            level = color(level, color_theme['skill_lvl99'])

        msg = f'{str(self)}: Lvl {level}'

        if level < MAX_LEVEL:
            xp_to_next = XP_table[level + 1] - self.XP
            msg = f'{msg} | {xp_to_next:.0f} EXP to next level'
        else:
            msg = f'{msg} | {self.XP:.0f} EXP'

        return msg

    def __str__(self):
        msg = color(self.name, skill_to_color(self.skill_type))

        return msg

    def _adjust_level(self) -> dict:
        current_lvl = self.level
        leveled_up = False
        for lvl in range(current_lvl + 1, MAX_LEVEL + 1):
            required_XP = XP_table[lvl]

            if self.XP < required_XP:
                break

            self.level = lvl

            leveled_up = True

        return {
            'leveled_up': leveled_up,
        }
