from collections import ChainMap, namedtuple

import z3

from bidding.utils import compute_range

NUM_PLAYERS = 4
SUIT_SIZE = 13
HAND_SIZE = 13
TOTAL_HCP = 40


class Player:
    Knowledge = namedtuple('PlayerKnowledge', 'hcp c d h s')

    def __init__(self, label):
        self.label = label

        self.hcp = z3.Int(f'hcp_{label}')
        self.c = z3.Int(f'c_{label}')
        self.d = z3.Int(f'd_{label}')
        self.h = z3.Int(f'h_{label}')
        self.s = z3.Int(f's_{label}')

    def __repr__(self):
        return f"<Player {self.label}>"

    @property
    def assertions(self):
        return [
            self.hcp >= 0,
            self.c >= 0,
            self.d >= 0,
            self.h >= 0,
            self.s >= 0,
            self.c + self.d + self.h + self.s == HAND_SIZE
        ]

    def compute_knowledge(self, opt):
        return Player.Knowledge(
            hcp=compute_range(opt, self.hcp),
            c=compute_range(opt, self.c),
            d=compute_range(opt, self.d),
            h=compute_range(opt, self.h),
            s=compute_range(opt, self.s)
        )


players = [Player(f'{i + 1}') for i in range(NUM_PLAYERS)]


class Bidding:
    Knowledge = namedtuple('BiddingKnowledge', 'players current_player opener responder')

    assertions = [
        z3.simplify(sum(p.hcp for p in players)) == TOTAL_HCP,
        z3.simplify(sum(p.c for p in players)) == SUIT_SIZE,
        z3.simplify(sum(p.d for p in players)) == SUIT_SIZE,
        z3.simplify(sum(p.h for p in players)) == SUIT_SIZE,
        z3.simplify(sum(p.s for p in players)) == SUIT_SIZE,
    ]

    def __init__(self, rules):
        self.rules = rules

        self.calls = []
        self.knowledge = None
        self.possible_calls = {}

        self._opt = z3.Optimize()
        self._opt.add(*Bidding.assertions)
        for player in players:
            self._opt.add(*player.assertions)
        self._compute()

    def push(self, call):
        self.calls.append(call)

        self._opt.push()
        self._opt.add(*self.possible_calls[call])
        self._compute()

    def pop(self):
        self.calls.pop()

        self._opt.pop()
        self._compute()

    def _compute(self):
        if self._opt.check() != z3.sat:
            raise RuntimeError("Assertions not satisfiable, check rules")

        opener_idx = next((i % NUM_PLAYERS for i, c in enumerate(self.calls) if c != 'Pass'), None)

        self.knowledge = Bidding.Knowledge(
            players={p: p.compute_knowledge(self._opt) for p in players},
            current_player=players[len(self.calls) % NUM_PLAYERS],
            opener=players[opener_idx] if opener_idx is not None else None,
            responder=players[(opener_idx + 2) % NUM_PLAYERS] if opener_idx is not None else None
        )

        self.possible_calls = dict(ChainMap(*(rule(self.knowledge) for rule in self.rules)))
