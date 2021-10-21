from enum import IntEnum
import numpy as np
from typing import List
import copy


class Order(IntEnum):
    LO = 0
    NLO = 1
    NLO_PLUS_NLL = 2


class Input:
    # TODO allow unspecified input? Maybe with kwargs + defaults
    def __init__(self, order: Order, energy, particle1: int, particle2: int, slha: str, pdf_lo: str, pdf_nlo: str, mu_f, mu_r):
        self.order = order
        self.energy = energy
        self.particle1 = particle1
        self.particle2 = particle2
        self.slha = slha
        self.pdf_lo = pdf_lo
        self.pdf_nlo = pdf_nlo
        self.mu_f = mu_f
        self.mu_r = mu_r


def scan(l: List[Input], var: str, range) -> List[Input]:
    ret = []
    for s in l:
        for r in range:
            tmp = copy.copy(s)
            setattr(tmp, var, r)
            ret.append(tmp)
    return ret
