from itertools import combinations

from z3 import *


def exclude(possible_calls):
    return And(*(
        Not(And(*assertions))
        for assertions in possible_calls.values()
    ))


def balanced(player):
    no_voids_and_singletons = And(
        player.c >= 2, player.d >= 2, player.h >= 2, player.s >= 2)
    at_most_one_doubleton = And(*(
        Not(And(x == 2, y == 2))
        for x, y in combinations([player.c, player.d, player.h, player.s], 2)
    ))
    return And(no_voids_and_singletons, at_most_one_doubleton)


def opening_one_nt(knowledge):
    if knowledge.opener is not None:
        return {}
    p = knowledge.current_player

    return {
        '1NT': [
            balanced(p),
            And(p.hcp >= 15, p.hcp <= 17)
        ]
    }


def opening_one_of_a_major(knowledge):
    if knowledge.opener is not None:
        return {}
    p = knowledge.current_player

    return {
        '1H': [
            exclude(opening_one_nt(knowledge)),
            And(p.hcp >= 13, p.h >= 5)
        ],
        '1S': [
            exclude(opening_one_nt(knowledge)),
            And(p.hcp >= 13, p.s >= 5)
        ]
    }


def opening_one_of_a_minor(knowledge):
    if knowledge.opener is not None:
        return {}
    p = knowledge.current_player

    return {
        '1C': [
            exclude(opening_one_nt(knowledge)),
            exclude(opening_one_of_a_major(knowledge)),
            p.hcp >= 13,
            Or(p.c > p.d, And(p.c == p.d, p.c == 3))
        ],
        '1D': [
            exclude(opening_one_nt(knowledge)),
            exclude(opening_one_of_a_major(knowledge)),
            p.hcp >= 13,
            Or(p.d > p.c, And(p.d == p.c, p.d == 4))
        ]
    }


def opening_pass(knowledge):
    if knowledge.opener is not None:
        return {}

    return {
        'Pass': [exclude(opening_one_nt(knowledge)),
                 exclude(opening_one_of_a_major(knowledge)),
                 exclude(opening_one_of_a_minor(knowledge))]
    }


def default_pass(knowledge):
    return {
        'Pass': []
    }


rules = [
    opening_one_nt,
    opening_one_of_a_major,
    opening_one_of_a_minor,
    opening_pass,

    default_pass
]
