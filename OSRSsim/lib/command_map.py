from .activities.skilling import MiningActivity, WoodcuttingActivity

from .info.bank import bank_print
from .info.stats import stats_print

from .testing.skilling import testing_skilling


map_activity = {
    'mine': MiningActivity,
    'chop': WoodcuttingActivity,
}

map_info = {
    'bank': bank_print,
    'stats': stats_print,
}

map_testing = {
    'skilling': testing_skilling,
}
