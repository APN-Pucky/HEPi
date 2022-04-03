from distutils.log import warn
from enum import IntEnum
#from math import dist
import copy
import warnings
import numpy as np
from typing import List

import pyslha
from .util import get_LR_partner, lhapdf_name_to_id, namehash

import lhapdf

in_dir = "./input/"
out_dir = "./output/"
pre = "nice -n 5"



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
    def __init__(self, order :Order, energy, particle1: int, particle2: int, slha: str, pdf_lo: str, pdf_nlo: str, mu_f=1.0, mu_r=1.0, pdfset_lo=0, pdfset_nlo=0,precision=0.01,max_iters=50, invariant_mass="auto",result="total",pt="auto",id="",model_path="/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO"):
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
        self.invariant_mass = invariant_mass
        self.pt = pt
        self.result = result
        self.id = id
        self.model_path = model_path
        update_slha(self)
def update_slha( i:Input ):
    b = pyslha.read(get_input_dir() + i.slha,ignorenomass=True)
    try:
        i.mu = (b.blocks["MASS"][abs(i.particle1)] +
                   b.blocks["MASS"][abs(i.particle2)])/2.
    except:
        pass
        





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
            tmp = scan(tmp, "mu_r", np.logspace(np.log10(1. /
                        distance), np.log10(distance), range))
            for t in tmp:
                if t.mu_f == 1.0 or t.mu_r == 1.0 or t.mu_f == t.mu_r or t.mu_f == distance or t.mu_f == 1./distance or t.mu_r == distance or t.mu_r == 1./distance:
                    ret.append(t)

        else:
            ret.append(s)

    return ret

def seven_point_scan(l: List[Input]):
    range=3
    distance=2.
    ret = []
    for s in l:
        # not on error pdfs
        if s.pdfset_nlo == 0 and s.mu_f == 1.0 and s.mu_r == 1.0:
            tmp = scan([s], "mu_f", np.logspace(np.log10(1. /
                        distance), np.log10(distance), range))
            tmp = scan(tmp, "mu_r", np.logspace(np.log10(1. /
                        distance), np.log10(distance), range))
            for t in tmp:
                if not ((t.mu_f == distance and  t.mu_r == 1./distance) or (t.mu_r == distance and  t.mu_f == 1./distance)):
                    ret.append(t)

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

def change_where(l:List[Input], dicts : dict, **kwargs):
    ret = []
    for s in l:
        ok = True
        for k,v in kwargs.items():
            if getattr(s,k) != v:
                ok = False
        if ok:
            tmp = copy.copy(s)
            for k,v in dicts.items():
                setattr(tmp, k, v)
            ret.append(tmp)
        else:
            ret.append(s)
            
    return ret

def scan_invariant_mass(l : List[Input],diff,points,low=0.001):
    ret = []
    for s in l:
        for r in s.mu*2.+ low+ (np.logspace(np.log10(low),np.log10(1+low),points)-low) *diff:
            tmp = copy.copy(s)
            setattr(tmp, "invariant_mass", r)
            tmp.result = "m"
            ret.append(tmp)
    return ret

def mass_scan(l: List[Input], var: int, range, diff_L_R=None) -> List[Input]:
    ret = []
    for s in l:
        for r in range:
            d = None
            try:
                d = pyslha.read(s.slha)
            except:
                d = pyslha.read(get_input_dir() + s.slha)
            d.blocks["MASS"][abs(var)] = r
            if not (diff_L_R is None):
                is_L, v = get_LR_partner(abs(var))
                d.blocks["MASS"][abs(v)] = r + is_L*diff_L_R

            newname = s.slha + "_mass_" + str(var) + "_" + str(r)
            pyslha.write(get_input_dir()+newname, d)

            tmp = copy.copy(s)
            setattr(tmp, "mass_" + str(var), r)
            setattr(tmp, "slha", newname)
            update_slha(tmp)
            ret.append(tmp)
    return ret

def slha_scan(l : List[Input],block,var,range : List) -> List[Input]:
    return slha_scan_rel(l,lambda r,: [(block,var,r)],range)

def slha_scan_rel(l : List[Input],lambdas ,range : List) -> List[Input]:
    ret = []
    for s in l:
        for r in range:
            d = None
            tmp = copy.copy(s)
            newname = s.slha
            try:
                d = pyslha.read(s.slha,ignorenomass=True)
            except:
                d = pyslha.read(get_input_dir() + s.slha,ignorenomass=True)
            ls = lambdas(r)
            for b,v,res in ls:
                d.blocks[b][v] = res
                setattr(tmp, b+ "_" + str(v), res)
                newname = newname +  "_" +str(b) + "_" + str(v) + "_" + str(res)
            pyslha.write(get_input_dir()+newname, d)

            setattr(tmp, "slha", newname)
            update_slha(tmp)
            ret.append(tmp)
    return ret