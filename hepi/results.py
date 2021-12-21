from .util import LD2DL
import numpy as np
from typing import List
from uncertainties import unumpy


class Result:
    def __init__(self, lo, nlo, nlo_plus_nll):
        self.lo = lo
        self.nlo = nlo
        self.nlo_plus_nll = nlo_plus_nll
        if lo is not None and lo != 0:
            self.K_lo = lo/lo
        if nlo is not None and nlo != 0:
            self.K_nlo = nlo/lo
        if nlo_plus_nll is not None and nlo_plus_nll != 0:
            self.K_nlo_plus_nll = nlo_plus_nll/lo
