from .util import LD2DL
import numpy as np
from typing import List
from uncertainties import unumpy


class Result:
    def __init__(self, lo, nlo, nlo_plus_nll):
        self.lo = lo
        self.nlo = nlo
        self.nlo_plus_nll = nlo_plus_nll
        self.K_lo = lo/lo
        self.K_nlo = nlo/lo
        self.K_nlo_plus_nll = nlo_plus_nll/lo
