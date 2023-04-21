from z3 import *


def opening_one_of_a_major(knowledge):
    if knowledge.opener is not None:
        return {}
    p = knowledge.current_player

    return {
        '1H': [And(p.hcp >= 13, p.h >= 5)],
        '1S': [And(p.hcp >= 13, p.h >= 5)]
    }


def opening_one_nt(knowledge):
    if knowledge.opener is not None:
        return {}
    p = knowledge.current_player

    return {
        '1NT': [And(p.hcp >= 15, p.hcp <= 17)]
    }


def default_pass(knowledge):
    return {
        'Pass': []
    }


rules = [
    opening_one_of_a_major,
    opening_one_nt,
    default_pass
]
