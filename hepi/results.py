from .util import LD2DL
import numpy as np
from typing import List
from uncertainties import unumpy
import uncertainties as unc
from smpl import plot
import lhapdf

#numerical convergence should be better by a factor of 10 to avoid spoiling the scale/pdf uncertainties
required_numerical_uncertainty_factor = 10 

class Result:
    def __init__(self, lo, nlo, nlo_plus_nll):
        self.lo = lo
        self.nlo = nlo
        self.nlo_plus_nll = nlo_plus_nll
        if lo is not None and lo != 0:
            self.K_lo = lo/lo
        if nlo is not None and lo != 0:
            self.K_nlo = nlo/lo
        else:
            print("K_nlo is none")
        if nlo_plus_nll is not None and lo != 0:
            self.K_nlo_plus_nll = nlo_plus_nll/lo


class ResultWithError(Result):
    def __init__(self,
                 lo, lo_up_scale, lo_down_scale,
                 nlo,  nlo_up_scale, nlo_down_scale, nlo_up_pdf, nlo_down_pdf,
                 nlo_plus_nll, nlo_plus_nll_up_scale, nlo_plus_nll_down_scale, nlo_plus_nll_up_pdf, nlo_plus_nll_down_pdf,
                 ):
        Result.__init__(self, lo, nlo, nlo_plus_nll)


def pdf_error(li, dl):
    global required_numerical_uncertainty_factor
    example = li[0]
    members = [attr for attr in dir(example) if not callable(
        getattr(example, attr)) and not attr.startswith("__")]
    dl["nlo_pdf_central"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["nlo_pdf_errplus"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["nlo_pdf_errminus"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["nlo_pdf_errsym"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["nlo_plus_nll_pdf_central"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["nlo_plus_nll_pdf_errplus"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["nlo_plus_nll_pdf_errminus"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["nlo_plus_nll_pdf_errsym"] = np.array([None]*len(dl["pdfset_nlo"]))
    for i in range(len(dl["pdfset_nlo"])):
        if dl["pdfset_nlo"][i] == 0 and dl["mu_f"][i] == 1.0 and dl["mu_r"][i] == 1.0:
            set = lhapdf.getPDFSet(dl["pdf_nlo"][i])
            pdfs = [0.0] * set.size
            for j in range(len(dl["pdfset_nlo"])):
                same = True
                for s in members:
                    if not (dl[s][i] == dl[s][j]) and s != "pdfset_nlo":
                        same = False
                if same:
                    pdfs[dl["pdfset_nlo"][j]] = j

            # lo_unc = set.uncertainty(
            #    [plot.unv(dl["lo"][k]) for k in pdfs], -1)
            print(dl)
            print(members)
            print(pdfs)
            print("hi",dl["nlo"],[dl["nlo"][k] for k in pdfs],[plot.unv(dl["nlo"][k]) for k in pdfs])
            nlo_unc = set.uncertainty(
                [plot.unv(dl["nlo"][k]) for k in pdfs], -1)
            dl["nlo_pdf_central"][i] = nlo_unc.central
            dl["nlo_pdf_errplus"][i] = nlo_unc.errplus
            dl["nlo_pdf_errminus"][i] = -nlo_unc.errminus
            dl["nlo_pdf_errsym"][i] = nlo_unc.errsymm
            #TODO error sym to minus and plus
            if(plot.usd(dl["nlo"][i])*required_numerical_uncertainty_factor > dl["nlo_pdf_errplus"][i] or  plot.usd(dl["nlo"][i])*required_numerical_uncertainty_factor > -dl["nlo_pdf_errminus"][i]):
                print("WARNING: too low numerical nlo precision vs pdf")
            nlo_plus_nll_unc = set.uncertainty(
                [plot.unv(dl["nlo_plus_nll"][k]) for k in pdfs], -1)
            dl["nlo_plus_nll_pdf_central"][i] = nlo_plus_nll_unc.central
            dl["nlo_plus_nll_pdf_errplus"][i] = nlo_plus_nll_unc.errplus
            dl["nlo_plus_nll_pdf_errminus"][i] = -nlo_plus_nll_unc.errminus
            dl["nlo_plus_nll_pdf_errsym"][i] = nlo_plus_nll_unc.errsymm
            #TODO error sym to minus and plus
            if(plot.usd(dl["nlo_plus_nll"][i])*required_numerical_uncertainty_factor > dl["nlo_plus_nll_pdf_errplus"][i] or  plot.usd(dl["nlo_plus_nll"][i])*required_numerical_uncertainty_factor > -dl["nlo_plus_nll_pdf_errminus"][i]):
                print("WARNING: too low numerical nlo_plus_nll precision vs pdf")
    return dl


def scale_error(li, dl):
    global required_numerical_uncertainty_factor
    example = li[0]
    members = [attr for attr in dir(example) if not callable(
        getattr(example, attr)) and not attr.startswith("__")]
    dl["nlo_scale_errplus"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["nlo_scale_errminus"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["nlo_plus_nll_scale_errplus"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["nlo_plus_nll_scale_errminus"] = np.array([None]*len(dl["pdfset_nlo"]))
    for i in range(len(dl["pdfset_nlo"])):
        if dl["pdfset_nlo"][i] == 0 and dl["mu_f"][i] == 1.0 and dl["mu_r"][i] == 1.0:
            scales = []
            for j in range(len(dl["pdfset_nlo"])):
                same = True
                for s in members:
                    if not (dl[s][i] == dl[s][j]) and s != "mu_f" and s != "mu_r":
                        same = False
                if same:
                    scales.append(j)

            # lo_unc = set.uncertainty(
            #    [plot.unv(dl["lo"][k]) for k in pdfs], -1)
            dl["nlo_scale_errplus"][i] = np.max(
                [plot.unv(dl["nlo"][k]) for k in scales])-plot.unv(dl["nlo"][i])
            dl["nlo_scale_errminus"][i] = np.min(
                [plot.unv(dl["nlo"][k]) for k in scales])-plot.unv(dl["nlo"][i])
            if(plot.usd(dl["nlo"][i])*required_numerical_uncertainty_factor > dl["nlo_scale_errplus"][i] or  plot.usd(dl["nlo"][i])*required_numerical_uncertainty_factor > -dl["nlo_scale_errminus"][i]):
                print("WARNING: too low numerical nlo precision vs scale")
            dl["nlo_plus_nll_scale_errplus"][i] = np.max(
                [plot.unv(dl["nlo_plus_nll"][k]) for k in scales])-plot.unv(dl["nlo_plus_nll"][i])
            dl["nlo_plus_nll_scale_errminus"][i] = np.min(
                [plot.unv(dl["nlo_plus_nll"][k]) for k in scales])-plot.unv(dl["nlo_plus_nll"][i])
            if(plot.usd(dl["nlo_plus_nll"][i])*required_numerical_uncertainty_factor > dl["nlo_plus_nll_scale_errplus"][i] or  plot.usd(dl["nlo_plus_nll"][i])*required_numerical_uncertainty_factor > -dl["nlo_plus_nll_scale_errminus"][i]):
                print("WARNING: too low numerical nlo_plus_nll precision vs scale")

    return dl
