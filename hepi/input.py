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
"""input directory"""
out_dir = "./output/"
"""output directory"""
pre = "nice -n 5"
"""run command prefix."""



def get_input_dir():
    """
    Get the input directory.
    """
    global in_dir
    return in_dir


def get_output_dir():
    """
    Get the input directory.
    """
    global out_dir
    return out_dir


def set_input_dir(ind):
    """
    Sets the input directory.
    """
    global in_dir
    in_dir = ind


def set_output_dir(outd):
    """
    Sets the output directory.
    """
    global out_dir
    out_dir = outd


def set_pre(ppre):
    """
    Sets the command prefix. 
    """
    global pre
    pre = ppre


def get_pre():
    """
    Gets the command prefix. 
    """
    global pre
    return pre


class Order(IntEnum):
    """
    Computation orders.
    """
    LO = 0
    NLO = 1
    NLO_PLUS_NLL = 2


class Input:
    """
    Input for computation.
    """
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
    """
    Updates dependent parameters in Input `i`.

    Mainly concerns the `mu` value used by `madgraph`.
    """
    b = pyslha.read(get_input_dir() + i.slha,ignorenomass=True)
    try:
        i.mu = (abs(b.blocks["MASS"][abs(i.particle1)]) +
                   abs(b.blocks["MASS"][abs(i.particle2)]))/2.
    except:
        pass
        





def scan(l: List[Input], var: str, range) -> List[Input]:
    """
    Scans a variable `var` over `range` in `l`.
    """
    ret = []
    for s in l:
        for r in range:
            tmp = copy.copy(s)
            setattr(tmp, var, r)
            ret.append(tmp)
    return ret


def scale_scan(l: List[Input], range=3, distance=2.):
    """
    Scans scale by varying `mu_f` and `mu_r`.
    They take `range` values from 1/`distance` to `distance` in lograthmic spacing.
    Only points with `mu_f`=`mu_r` or `mu_r/f`=1 or `mu_r/f`=`distance` or `mu_r/f`=1/`distance` are returned.
    """
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
    """
    Scans scale by varying `mu_f` and `mu_r` by factors of two excluding relative factors of 4.
    """
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
    """
    Scans NLO PDF sets. 

    The PDF sets are infered from `lhapdf.getPDFSet` with the argument of `pdfset_nlo`.
    """
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
    """
    Applies the values of `dicts` if the key value pairs in `kwargs` agree with a member of the list `l`.

    The changes only applied to the matching list members.
    """
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
    """
    Logarithmic `invariant_mass` scan close to the production threshold.
    """
    ret = []
    for s in l:
        for r in s.mu*2.+ low+ (np.logspace(np.log10(low),np.log10(1+low),points)-low) *diff:
            tmp = copy.copy(s)
            setattr(tmp, "invariant_mass", r)
            tmp.result = "m"
            ret.append(tmp)
    return ret

def mass_scan(l: List[Input], var: int, range, diff_L_R=None) -> List[Input]:
    """
    Scans the PDG identified mass `var` over `range` in the list `l`.
    `diff_L_R` allows to set a fixed difference between masses of left- and right-handed particles.
    """
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
    """
    Scan a generic 
    """
    return slha_scan_rel(l,lambda r,: [(block,var,r)],range)

def slha_scan_rel(l : List[Input],lambdas ,range : List) -> List[Input]:
    """
    Scan a generic slha variable.
    """
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