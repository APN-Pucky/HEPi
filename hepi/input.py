from enum import IntEnum
#from math import dist
import numpy as np
from typing import List
import copy
from particle import PDGID
import pyslha
from .util import lhapdf_name_to_id
from particle import Particle
from particle.converters.bimap import DirectionalMaps
import lhapdf

in_dir = "./input/"
out_dir = "./output/"
pre = "nice -n 5"

PDG2LaTeXNameMap, LaTeX2PDGNameMap = DirectionalMaps(
    "PDGID", "LaTexName", converters=(PDGID, str))

PDG2Name2IDMap, PDGID2NameMap = DirectionalMaps(
    "PDGName", "PDGID", converters=(str, PDGID))


def get_name(id):
    global PDG2LaTeXNameMap
    pdgid = PDG2LaTeXNameMap[id]
    return pdgid


def get_LR_partner(id):
    n = PDGID2NameMap[id]
    if "L" in n:
        n = n.replace("L", "R")
        return -1, int(PDG2Name2IDMap[n])
    if "R" in n:
        n = n.replace("R", "L")
        return 1, int(PDG2Name2IDMap[n])


def get_input_dir():
    global in_dir
    return in_dir


def get_output_dir():
    global out_dir
    return out_dir


def set_input_dir(ind):
    global in_dir
    in_dir = ind


def set_output_dir(outd):
    global out_dir
    out_dir = outd


def set_pre(ppre):
    global pre
    pre = ppre


def get_pre():
    global pre
    return pre


class Order(IntEnum):
    LO = 0
    NLO = 1
    NLO_PLUS_NLL = 2


class Input:
    # TODO allow unspecified input? Maybe with kwargs + defaults
    def __init__(self, order: Order, energy, particle1: int, particle2: int, slha: str, pdf_lo: str, pdf_nlo: str, mu_f=1.0, mu_r=1.0, pdfset_lo=0, pdfset_nlo=0,precision=0.01,max_iters=50, id=""):
        self.order = order
        self.energy = energy
        self.energyhalf = energy/2.
        self.particle1 = particle1
        self.particle2 = particle2
        self.slha = slha
        self.pdf_lo = pdf_lo
        self.pdfset_lo = pdfset_lo
        self.pdf_nlo = pdf_nlo
        self.pdfset_nlo = pdfset_nlo
        self.pdf_lo_id = lhapdf_name_to_id(pdf_lo)
        self.pdf_nlo_id = lhapdf_name_to_id(pdf_nlo)
        self.mu_f = mu_f
        self.mu_r = mu_r
        self.precision = precision
        self.max_iters = max_iters
        self.id = id
        b = pyslha.read(get_input_dir() + slha)
        self.mu = (b.blocks["MASS"][abs(particle1)] +
                   b.blocks["MASS"][abs(particle2)])/2.


def mass_scan(l: List[Input], var: int, range, diff_L_R=None) -> List[Input]:
    ret = []
    for s in l:
        for r in range:
            d = None
            try:
                d = pyslha.read(s.slha)
            except:
                d = pyslha.read(get_input_dir() + s.slha)
            d.blocks["MASS"][var] = r
            if not (diff_L_R is None):
                is_L, v = get_LR_partner(var)
                d.blocks["MASS"][v] = r + is_L*diff_L_R

            newname = s.slha + "_" + str(var) + "_" + str(r)
            pyslha.write(get_input_dir()+newname, d)
            tmp = copy.copy(s)
            setattr(tmp, "mass_" + str(var), r)
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


def scale_scan(l: List[Input], range=3, distance=2.):
    ret = []
    for s in l:
        # not on error pdfs
        if s.pdfset_nlo == 0:
            tmp = scan([s], "mu_f", np.logspace(np.log10(1. /
                        distance), np.log10(distance), range))
            ret += scan(tmp, "mu_r", np.logspace(np.log10(1. /
                        distance), np.log10(distance), range))
        else:
            ret.append(s)

    return ret


def pdf_scan(l: List[Input]):
    ret = []
    for s in l:
        # only central scale
        if s.mu_f == 1.0 and s.mu_r == 1.0:
            set = lhapdf.getPDFSet(s.pdf_nlo)
            for r in range(set.size):
                tmp = copy.copy(s)
                setattr(tmp, "pdfset_nlo", r)
                ret.append(tmp)
        else:
            ret.append(s)
    return ret
