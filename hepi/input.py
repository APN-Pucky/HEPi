from enum import IntEnum
import numpy as np
from typing import List
import copy
import pyslha
# TODO setters
in_dir = "./input/"
out_dir = "./output/"


def get_input_dir():
    global in_dir
    return in_dir


def get_output_dir():
    global out_dir
    return out_dir


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


def mass_scan(l: List[Input], var: int, range) -> List[Input]:
    ret = []
    for s in l:
        for r in range:
            d = pyslha.read(s.slha)
            d.blocks["MASS"][var] = r
            newname = s.slha + "_" + str(var) + "_" + str(r)
            pyslha.write(get_input_dir()+newname, d)
            tmp = copy.copy(s)
            setattr(tmp, "mass_" +str(var), r)
            setattr(tmp, "slha", newname)
            ret.append(tmp)
    return ret


def scan(l: List[Input], var: str, range) -> List[Input]:
    ret = []
    for s in l:
        for r in range:
            tmp = copy.copy(s)
            setattr(tmp, var, r)
            ret.append(tmp)
    return ret
