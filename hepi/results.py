from .util import LD2DL
import numpy as np
from typing import List
from uncertainties import unumpy
import lhapdf


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


class ResultWithError(Result):
    def __init__(self,
                 lo, lo_up_scale, lo_down_scale,
                 nlo,  nlo_up_scale, nlo_down_scale, nlo_up_pdf, nlo_down_pdf,
                 nlo_plus_nll, nlo_plus_nll_up_scale, nlo_plus_nll_down_scale, nlo_plus_nll_up_pdf, nlo_plus_nll_down_pdf,
                 ):
        Result.__init__(self, lo, nlo, nlo_plus_nll)


def pdf_error(li, dl):
    example = li[0]
    members = [attr for attr in dir(example) if not callable(
        getattr(example, attr)) and not attr.startswith("__")]
    for i in range(len(dl["pdfset_nlo"])):
        if dl["pdfset_nlo"][i] == 0:
            set = lhapdf.getPDFSet(dl["pdf_nlo"][i])
            pdfs = [None] * set.size()
            for j in range(len(dl["pdfset_nlo"])):
                same = True
                for s in members:
                    if not (dl[s][i] == dl[s][j] and s != "pdfset_nlo"):
                        same = False
                if same:
                    pdfs[dl["pdfset_nlo"][j]] = j

            lo_unc = set.uncertainty([dl["lo"][k] for k in pdfs], -1)
            nlo_unc = set.uncertainty([dl["nlo"][k] for k in pdfs], -1)
            nlo_plus_nll_unc = set.uncertainty(
                [dl["nlo_plus_nll"][k] for k in pdfs], -1)
