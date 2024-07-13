BLACK = '\033[0;30m'
RED = '\033[0;31m'
GREEN = '\033[0;32m'
BROWN = '\033[0;33m'
BLUE = '\033[0;34m'
PURPLE = '\033[0;35m'
CYAN = '\033[0;36m'
LIGHT_GRAY = '\033[0;37m'
DARK_GRAY = '\033[1;30m'
LIGHT_RED = '\033[1;31m'
LIGHT_GREEN = '\033[1;32m'
YELLOW = '\033[1;33m'
LIGHT_BLUE = '\033[1;34m'
LIGHT_PURPLE = '\033[1;35m'
LIGHT_CYAN = '\033[1;36m'
LIGHT_WHITE = '\033[1;37m'
BOLD = '\033[1m'
FAINT = '\033[2m'
ITALIC = '\033[3m'
UNDERLINE = '\033[4m'
BLINK = '\033[5m'
NEGATIVE = '\033[7m'
CROSSED = '\033[9m'
END = '\033[0m'


def color(text: str, color: str, justify: int = 0, just_type: str = 'right'):
    out_text = f'{color}{text}{END}'

    if not justify:
        return out_text

    just_amount = justify + len(color) + len(END)

    if just_type == 'right':
        out_text = f'{out_text:>{just_amount}}'
    elif just_type == 'left':
        out_text = f'{out_text:<{just_amount}}'

    return out_text


# THEME:
COLOR_CHARACTER = CYAN
COLOR_STATS = LIGHT_PURPLE

COLOR_BANK1 = LIGHT_PURPLE
