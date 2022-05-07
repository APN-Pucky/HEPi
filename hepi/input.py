from enum import IntEnum
import os
import shutil
import warnings
import copy

import numpy as np
from typing import Iterable, List

import pyslha
from .util import DictData, get_LR_partner, lhapdf_name_to_id

import lhapdf




in_dir = "./input/"
"""Input directory."""
out_dir = "./output/"
"""Output directory."""
pre = "nice -n 5"
"""Prefix for run commands."""



def get_input_dir():
    """
    Get the input directory.

    Returns:
        str: :attr:`in_dir`
    """
    global in_dir
    return in_dir


def get_output_dir():
    """
    Get the input directory.

    Returns:
        str: :attr:`out_dir`
    """
    global out_dir
    return out_dir


def get_pre():
    """
    Gets the command prefix. 

    Returns:
        str: :attr:`pre`
    """
    global pre
    return pre

def set_input_dir(ind):
    """
    Sets the input directory.

    Args:
        ind (str): new input directory.
    """
    global in_dir
    in_dir = ind


def set_output_dir(outd):
    """
    Sets the output directory.

    Args:
        outd (str): new output directory.
    """
    global out_dir
    out_dir = outd


def set_pre(ppre):
    """
    Sets the command prefix. 

    Args:
        ppre (str): new command prefix.
    """
    global pre
    pre = ppre


class Order(IntEnum):
    """
    Computation orders.
    """
    LO = 0
    """Leading Order"""
    NLO = 1
    """Next-to-Leading Order"""
    NLO_PLUS_NLL = 2
    """Next-to-Leading Order plus Next-to-Leading Logarithms"""
    aNNLO_PLUS_NNLL = 3
    """Approximate Next-to-next-to-Leading Order plus Next-to-next-to-Leading Logarithms"""

def order_to_string(o:Order):
    return ["LO","NLO","NLO_PLUS_NLL","aNNLO_PLUS_NNLL"][o]

class Input(DictData):
    """
    Input for computation and scans.

    Attributes:
        order (:class:`Order`): LO, NLO or NLO+NLL computation.
        energy (int): CMS energy in GeV.
        energyhalf (int): Halfed `energy`.
        particle1 (int): PDG identifier of the first final state particle.
        particle2 (int): PDG identifier of the second final state particle.
        slha (str): File path of for the base slha.
            Modified slha files will be used if a scan requires a change of the input.
        pdf_lo (str): LO PDF name.
        pdf_nlo (str): NLO PDF name.
        pdfset_lo (int): LO PDF member/set id.
        pdfset_nlo (int): NLO PDF member/set id.
        pdf_lo_id (int):  LO PDF first member/set id.
        pdf_nlo_id (int): NLO PDF first member/set id.
        mu (double): central scale factor.
        mu_f (double): Factorization scale factor.
        mu_r (double): Renormalization scale factor.
        precision (double): Desired numerical relative precision.
        max_iters (int): Upper limit on integration iterations.
        invariant_mass (str): Invariant mass mode 'auto = sqrt((p1+p2)^2)' else value.
        pt (str): Transverse Momentum mode 'auto' or value.
        result (str): Result type 'total'/'pt'/'ptj'/'m'.
        id (str): Set an id of this run. 
        model_path (str): Path for MadGraph model.
        update (bool): Update dependent `mu`.
    """
    # TODO allow unspecified input? Maybe with kwargs + defaults
    def __init__(self, order :Order, energy:float, particle1: int, particle2: int, slha: str, pdf_lo: str, pdf_nlo: str, mu_f=1.0, mu_r=1.0, pdfset_lo=0, pdfset_nlo=0,precision=0.01,max_iters=50, invariant_mass="auto",result="total",pt="auto",id="",model_path="/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO", update=True):
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
        if os.path.isfile(get_input_dir() + self.slha):
                shutil.copy(get_input_dir() + self.slha,get_output_dir() + self.slha)
        if update:
            update_slha(self)

    def has_gluino(self) -> bool:
        return is_gluino(self.particle1) or is_gluino(self.particle2)
    def has_neutralino(self) -> bool:
        return is_neutralino(self.particle1) or is_neutralino(self.particle2) 
    def has_charginos(self) -> bool:
        return is_chargino(self.particle1) or is_chargino(self.particle2) 
    def has_weakino(self) -> bool:
        return self.has_charginos() or self.has_neutralino()
    def has_squark(self) -> bool:
        return is_squark(self.particle1) or is_squark(self.particle2)
    def has_slepton(self) -> bool:
        return is_slepton(self.particle1) or is_slepton(self.particle2)

def is_gluino(id:int)->bool:
    return id == 1000021 

def is_neutralino(id:int) -> bool:
    neutralinos = [1000022,1000023,1000025,1000035]
    return abs(id) in neutralinos 

def is_chargino(id:int) -> bool:
    charginos= [1000024,1000037]
    return abs(id) in charginos

def is_weakino(id:int) -> bool:
    return is_chargino(id) or is_neutralino(id)

def is_squark(id:int) -> bool:
    l_squark= range(1000001,1000007)
    r_squark= range(2000001,2000007)
    return abs(id) in l_squark or abs(id) in r_squark

def is_slepton(id:int) -> bool:
    l_slepton= range(1000011,1000016)
    r_slepton= range(2000011,2000016)  # TODO remove righthandend snu's
    return abs(id) in l_slepton or abs(id) in r_slepton


def update_slha( i:Input ):
    """
    Updates dependent parameters in Input `i`.

    Mainly concerns the `mu` value used by `madgraph`.

    
    """
    b = pyslha.read(get_output_dir() + i.slha,ignorenomass=True)
    try:
        i.mu = (abs(b.blocks["MASS"][abs(i.particle1)]) +
                   abs(b.blocks["MASS"][abs(i.particle2)]))/2.
    except:
        warnings.warn("Could not set new central scale to average of masses.",RuntimeWarning)
        pass



def scan(l: List[Input], var: str , range :Iterable )  -> List[Input]:
    """
    Scans a variable `var` over `range` in `l`.

    Note:
        This function does not ensure that dependent vairables are updated (see `energyhalf` in Examples).

    Args:
        l (:obj:`list` of :class:`Input`): Input parameters that get scanned each.
        var (str): Scan variable name.
        range (Iterable): Range of `var` to be scanned.

    Returns:
        :obj:`list` of :class:`Input`: Modified list with scan runs added.

    Examples:
        >>> li = [Input(Order.LO, 13000,  1000022,1000022, "None", "CT14lo","CT14lo",update=False)]
        >>> li = scan(li,"energy",range(10000,13000,1000))
        >>> for e in li:
        ...     print(e)
        {'order': <Order.LO: 0>, 'energy': 10000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.LO: 0>, 'energy': 11000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.LO: 0>, 'energy': 12000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        >>> for e in scan(li,"order",[Order.LO,Order.NLO,Order.NLO_PLUS_NLL]):
        ...     print(e)
        {'order': <Order.LO: 0>, 'energy': 10000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 10000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO_PLUS_NLL: 2>, 'energy': 10000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.LO: 0>, 'energy': 11000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 11000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO_PLUS_NLL: 2>, 'energy': 11000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.LO: 0>, 'energy': 12000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 12000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO_PLUS_NLL: 2>, 'energy': 12000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
 
    """
    ret = []
    for s in l:
        for r in range:
            tmp = copy.copy(s)
            setattr(tmp, var, r)
            ret.append(tmp)
    return ret

def scan_multi(li: List[Input], **kwargs)  -> List[Input]:
    """
    Magically scans the variables passed to this function.

    Args:
        **kwargs: 

    Examples:
        >>> oli = [Input(Order.LO, 13000,  1000022,1000022, "None", "CT14lo","CT14lo",update=False)]
        >>> li = scan_multi(oli,energy=range(10000,13000,1000))
        >>> for e in li:
        ...     print(e)
        {'order': <Order.LO: 0>, 'energy': 10000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.LO: 0>, 'energy': 11000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.LO: 0>, 'energy': 12000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        >>> for e in scan_multi(oli,energy=range(10000,13000,1000),order=[Order.LO,Order.NLO,Order.NLO_PLUS_NLL]):
        ...     print(e)
        {'order': <Order.LO: 0>, 'energy': 10000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 10000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO_PLUS_NLL: 2>, 'energy': 10000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.LO: 0>, 'energy': 11000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 11000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO_PLUS_NLL: 2>, 'energy': 11000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.LO: 0>, 'energy': 12000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 12000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO_PLUS_NLL: 2>, 'energy': 12000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
 
    """
    for k,v in kwargs.items():
        li = scan(li,var=k,range=v)
    return li
multi_scan=scan_multi

def scan_scale(l: List[Input], range=3, distance=2.):
    """
    Scans scale by varying `mu_f` and `mu_r`.

    They take `range` values from 1/`distance` to `distance` in lograthmic spacing.
    Only points with `mu_f`=`mu_r` or `mu_r/f`=1 or `mu_r/f`=`distance` or `mu_r/f`=1/`distance` are returned.

    Examples:
        >>> li = [Input(Order.LO, 13000,  1000022,1000022, "None", "CT14lo","CT14lo",update=False)]
        >>> for e in scan_scale(li):
        ...     print(e)
        {'order': <Order.LO: 0>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 0.5, 'mu_r': 0.5, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.LO: 0>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 0.5, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.LO: 0>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 0.5, 'mu_r': 2.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.LO: 0>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 0.5, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.LO: 0>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.LO: 0>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 2.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.LO: 0>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 2.0, 'mu_r': 0.5, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.LO: 0>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 2.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.LO: 0>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 2.0, 'mu_r': 2.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
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
scale_scan=scan_scale

def scan_seven_point(l: List[Input]):
    """
    Scans scale by varying `mu_f` and `mu_r` by factors of two excluding relative factors of 4.

    Examples:
        >>> li = [Input(Order.LO, 13000,  1000022,1000022, "None", "CT14lo","CT14lo",update=False)]
        >>> for e in scan_seven_point(li):
        ...     print(e)
        {'order': <Order.LO: 0>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 0.5, 'mu_r': 0.5, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.LO: 0>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 0.5, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.LO: 0>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 0.5, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.LO: 0>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.LO: 0>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 2.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.LO: 0>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 2.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.LO: 0>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 2.0, 'mu_r': 2.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
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
seven_point_scan=scan_seven_point



def change_where(l:List[Input], dicts : dict, **kwargs):
    """
    Applies the values of `dicts` if the key value pairs in `kwargs` agree with a member of the list `l`.

    The changes only applied to the matching list members.

    Examples:
        >>> li = scan_multi([Input(Order.LO, 13000,  1000022,1000022, "None", "CT14lo","CT14lo",update=False)],energy=range(10000,13000,1000))
        >>> for e in change_where(li,{'order':Order.NLO},energy=11000):
        ...     print(e)
        {'order': <Order.LO: 0>, 'energy': 10000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 11000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.LO: 0>, 'energy': 12000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        >>> li = scan_multi([Input(Order.LO, 13000,  1000022,1000022, "None", "CT14lo","CT14lo",update=False)],energy=range(10000,12000,1000),mu_f=range(1,3))
        >>> for e in change_where(li,{'order':Order.NLO},energy=11000,mu_f=1):
        ...     print(e)
        {'order': <Order.LO: 0>, 'energy': 10000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.LO: 0>, 'energy': 10000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 2, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 11000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 1, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.LO: 0>, 'energy': 11000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14lo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13200, 'mu_f': 2, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
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

def slha_write(newname,d):
    f = get_output_dir()+newname
    pyslha.write(f, d)
    with open(f) as reader, open(f, 'r+') as writer:
        for line in reader:
            if line.strip():
                writer.write(line)
            else:
                writer.write("#\n")
        writer.truncate()


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
                d = pyslha.read(get_output_dir() + s.slha)
            d.blocks["MASS"][abs(var)] = r
            if not (diff_L_R is None):
                is_L, v = get_LR_partner(abs(var))
                d.blocks["MASS"][abs(v)] = r + is_L*diff_L_R

            newname = s.slha + "_mass_" + str(var) + "_" + str(r)
            #pyslha.write(get_output_dir()+newname, d)
            slha_write(newname,d)

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
                d = pyslha.read(get_output_dir() + s.slha,ignorenomass=True)
            ls = lambdas(r)
            for b,v,res in ls:
                d.blocks[b][v] = res
                setattr(tmp, b+ "_" + str(v), res)
                newname = newname +  "_" +str(b) + "_" + str(v) + "_" + str(res)
            #pyslha.write(get_output_dir()+newname, d)
            slha_write(newname,d)

            setattr(tmp, "slha", newname)
            update_slha(tmp)
            ret.append(tmp)
    return ret

def scan_pdf(l: List[Input]):
    """
    Scans NLO PDF sets. 

    The PDF sets are infered from `lhapdf.getPDFSet` with the argument of `pdfset_nlo`.

    Examples:
        >>> li = [Input(Order.NLO, 13000,  1000022,1000022, "None", "CT14lo","CT14nlo",update=False)]
        >>> for e in scan_pdf(li):
        ...     print(e)
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 0, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 1, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 2, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 3, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 4, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 5, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 6, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 7, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 8, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 9, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 10, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 11, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 12, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 13, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 14, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 15, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 16, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 17, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 18, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 19, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 20, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 21, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 22, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 23, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 24, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 25, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 26, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 27, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 28, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 29, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 30, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 31, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 32, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 33, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 34, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 35, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 36, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 37, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 38, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 39, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 40, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 41, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 42, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 43, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 44, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 45, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 46, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 47, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 48, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 49, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 50, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 51, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 52, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 53, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 54, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 55, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
        {'order': <Order.NLO: 1>, 'energy': 13000, 'energyhalf': 6500.0, 'particle1': 1000022, 'particle2': 1000022, 'slha': 'None', 'pdf_lo': 'CT14lo', 'pdfset_lo': 0, 'pdf_nlo': 'CT14nlo', 'pdfset_nlo': 56, 'pdf_lo_id': 13200, 'pdf_nlo_id': 13100, 'mu_f': 1.0, 'mu_r': 1.0, 'precision': 0.01, 'max_iters': 50, 'invariant_mass': 'auto', 'pt': 'auto', 'result': 'total', 'id': '', 'model_path': '/opt/MG5_aMC_v2_7_0/models/MSSMatNLO_UFO'}
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
pdf_scan=scan_pdf