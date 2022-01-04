from .util import LD2DL
import numpy as np
from typing import List
from uncertainties import unumpy
import uncertainties as unc
from smpl import plot
import lhapdf
import warnings

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
    dl["lo_pdf"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["lo_pdf_central"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["lo_pdf_errplus"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["lo_pdf_errminus"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["lo_pdf_errsym"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["nlo_pdf"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["nlo_pdf_central"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["nlo_pdf_errplus"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["nlo_pdf_errminus"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["nlo_pdf_errsym"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["nlo_plus_nll_pdf"] = np.array([None]*len(dl["pdfset_nlo"]))
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

            dl["lo_pdf_central"][i] = plot.unv(dl["lo"][i])
            dl["lo_pdf_errplus"][i] = 0.0
            dl["lo_pdf_errminus"][i] = 0.0
            dl["lo_pdf_errsym"][i] = 0.0
            # lo_unc = set.uncertainty(
            #    [plot.unv(dl["lo"][k]) for k in pdfs], -1)
            nlo_unc = set.uncertainty(
                [plot.unv(dl["nlo"][k]) for k in pdfs], -1)
            dl["nlo_pdf_central"][i] = nlo_unc.central
            dl["nlo_pdf_errplus"][i] = nlo_unc.errplus
            dl["nlo_pdf_errminus"][i] = -nlo_unc.errminus
            dl["nlo_pdf_errsym"][i] = nlo_unc.errsymm
            #TODO error sym to minus and plus
            if(plot.usd(dl["nlo"][i])*required_numerical_uncertainty_factor > dl["nlo_pdf_errplus"][i] or  plot.usd(dl["nlo"][i])*required_numerical_uncertainty_factor > -dl["nlo_pdf_errminus"][i]):
                warnings.warn("too low numerical nlo precision vs pdf", RuntimeWarning)

            nlo_plus_nll_unc = set.uncertainty(
                [plot.unv(dl["nlo_plus_nll"][k]) for k in pdfs], -1)
            dl["nlo_plus_nll_pdf_central"][i] = nlo_plus_nll_unc.central
            dl["nlo_plus_nll_pdf_errplus"][i] = nlo_plus_nll_unc.errplus
            dl["nlo_plus_nll_pdf_errminus"][i] = -nlo_plus_nll_unc.errminus
            dl["nlo_plus_nll_pdf_errsym"][i] = nlo_plus_nll_unc.errsymm
            #TODO error sym to minus and plus
            if(plot.usd(dl["nlo_plus_nll"][i])*required_numerical_uncertainty_factor > dl["nlo_plus_nll_pdf_errplus"][i] or  plot.usd(dl["nlo_plus_nll"][i])*required_numerical_uncertainty_factor > -dl["nlo_plus_nll_pdf_errminus"][i]):
                warnings.warn("too low numerical nlo_plus_nll precision vs pdf", RuntimeWarning)


    mask = dl["lo_pdf_central"]!= np.array(None)
    dl["lo_pdf"][mask] = unumpy.uarray(plot.unv(dl["lo"][mask])+dl["lo_pdf_errplus"][mask]/2.+dl["lo_pdf_errminus"][mask]/2.,
        +dl["lo_pdf_errplus"][mask]-dl["lo_pdf_errminus"][mask])

    mask = dl["nlo_pdf_central"]!= np.array(None)
    dl["nlo_pdf"][mask] = unumpy.uarray(plot.unv(dl["nlo"][mask])+dl["nlo_pdf_errplus"][mask]/2.+dl["nlo_pdf_errminus"][mask]/2.,
        +dl["nlo_pdf_errplus"][mask]-dl["nlo_pdf_errminus"][mask])

    mask = dl["nlo_plus_nll_pdf_central"]!= np.array(None)
    dl["nlo_plus_nll_pdf"][mask] = unumpy.uarray(plot.unv(dl["nlo_plus_nll"][mask])+dl["nlo_plus_nll_pdf_errplus"][mask]/2.+dl["nlo_plus_nll_pdf_errminus"][mask]/2.,
        +dl["nlo_plus_nll_pdf_errplus"][mask]-dl["nlo_plus_nll_pdf_errminus"][mask])
    return dl


def scale_error(li, dl):
    global required_numerical_uncertainty_factor
    example = li[0]
    members = [attr for attr in dir(example) if not callable(
        getattr(example, attr)) and not attr.startswith("__")]
    dl["lo_scale"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["lo_scale_errplus"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["lo_scale_errminus"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["nlo_scale"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["nlo_scale_errplus"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["nlo_scale_errminus"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["nlo_plus_nll_scale"] = np.array([None]*len(dl["pdfset_nlo"]))
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
            dl["lo_scale_errplus"][i] = np.max(
                [plot.unv(dl["lo"][k]) for k in scales])-plot.unv(dl["lo"][i])
            dl["lo_scale_errminus"][i] = np.min(
                [plot.unv(dl["lo"][k]) for k in scales])-plot.unv(dl["lo"][i])
            if(plot.usd(dl["lo"][i])*required_numerical_uncertainty_factor > dl["lo_scale_errplus"][i] or  plot.usd(dl["lo"][i])*required_numerical_uncertainty_factor > -dl["lo_scale_errminus"][i]):
                warnings.warn("too low numerical lo precision vs scale", RuntimeWarning)

            dl["nlo_scale_errplus"][i] = np.max(
                [plot.unv(dl["nlo"][k]) for k in scales])-plot.unv(dl["nlo"][i])
            dl["nlo_scale_errminus"][i] = np.min(
                [plot.unv(dl["nlo"][k]) for k in scales])-plot.unv(dl["nlo"][i])
            if(plot.usd(dl["nlo"][i])*required_numerical_uncertainty_factor > dl["nlo_scale_errplus"][i] or  plot.usd(dl["nlo"][i])*required_numerical_uncertainty_factor > -dl["nlo_scale_errminus"][i]):
                warnings.warn("too low numerical nlo precision vs scale", RuntimeWarning)

            dl["nlo_plus_nll_scale_errplus"][i] = np.max(
                [plot.unv(dl["nlo_plus_nll"][k]) for k in scales])-plot.unv(dl["nlo_plus_nll"][i])
            dl["nlo_plus_nll_scale_errminus"][i] = np.min(
                [plot.unv(dl["nlo_plus_nll"][k]) for k in scales])-plot.unv(dl["nlo_plus_nll"][i])
            if(plot.usd(dl["nlo_plus_nll"][i])*required_numerical_uncertainty_factor > dl["nlo_plus_nll_scale_errplus"][i] or  plot.usd(dl["nlo_plus_nll"][i])*required_numerical_uncertainty_factor > -dl["nlo_plus_nll_scale_errminus"][i]):
                warnings.warn("too low numerical nlo_plus_nll precision vs scale", RuntimeWarning)

    mask = dl["lo_scale_errplus"]!= np.array(None)
    dl["lo_scale"][mask] = unumpy.uarray(plot.unv(dl["lo"][mask])+dl["lo_scale_errplus"][mask]/2.+dl["lo_scale_errminus"][mask]/2.,
        +dl["lo_scale_errplus"][mask]-dl["lo_scale_errminus"][mask])

    mask = dl["nlo_scale_errplus"]!= np.array(None)
    dl["nlo_scale"][mask] = unumpy.uarray(plot.unv(dl["nlo"][mask])+dl["nlo_scale_errplus"][mask]/2.+dl["nlo_scale_errminus"][mask]/2.,
        +dl["nlo_scale_errplus"][mask]-dl["nlo_scale_errminus"][mask])

    mask = dl["nlo_plus_nll_scale_errplus"]!= np.array(None)
    dl["nlo_plus_nll_scale"][mask] = unumpy.uarray(plot.unv(dl["nlo_plus_nll"][mask])+dl["nlo_plus_nll_scale_errplus"][mask]/2.+dl["nlo_plus_nll_scale_errminus"][mask]/2.,
        +dl["nlo_plus_nll_scale_errplus"][mask]-dl["nlo_plus_nll_scale_errminus"][mask])
    
    return dl

def combine_errors(dl):
    dl["lo_errplus"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["lo_errminus"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["lo_combined"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["nlo_errplus"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["nlo_errminus"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["nlo_combined"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["nlo_plus_nll_errplus"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["nlo_plus_nll_errminus"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["nlo_plus_nll_combined"] = np.array([None]*len(dl["pdfset_nlo"]))


    mask = dl["lo_pdf_central"]!= np.array(None)
    dl["lo_errplus"][mask]= np.sqrt(dl["lo_pdf_errplus"][mask].astype(float)**2+dl["lo_scale_errplus"][mask].astype(float)**2)
    dl["lo_errminus"][mask]= -np.sqrt(dl["lo_pdf_errminus"][mask].astype(float)**2+dl["lo_scale_errminus"][mask].astype(float)**2)
    dl["lo_combined"][mask] = unumpy.uarray(plot.unv(dl["lo"][mask])+dl["lo_errplus"][mask]/2.+dl["lo_errminus"][mask]/2.,
        +dl["lo_errplus"][mask]-dl["lo_errminus"][mask])

    mask = dl["nlo_pdf_central"]!= np.array(None)
    dl["nlo_errplus"][mask]= np.sqrt(dl["nlo_pdf_errplus"][mask].astype(float)**2+dl["nlo_scale_errplus"][mask].astype(float)**2)
    dl["nlo_errminus"][mask]= -np.sqrt(dl["nlo_pdf_errminus"][mask].astype(float)**2+dl["nlo_scale_errminus"][mask].astype(float)**2)
    dl["nlo_combined"][mask] = unumpy.uarray(plot.unv(dl["nlo"][mask])+dl["nlo_errplus"][mask]/2.+dl["nlo_errminus"][mask]/2.,
        +dl["nlo_errplus"][mask]-dl["nlo_errminus"][mask])

    mask = dl["nlo_plus_nll_pdf_central"]!= np.array(None)
    dl["nlo_plus_nll_errplus"][mask]= np.sqrt(dl["nlo_plus_nll_pdf_errplus"][mask].astype(float)**2+dl["nlo_plus_nll_scale_errplus"][mask].astype(float)**2)
    dl["nlo_plus_nll_errminus"][mask]= -np.sqrt(dl["nlo_plus_nll_pdf_errminus"][mask].astype(float)**2+dl["nlo_plus_nll_scale_errminus"][mask].astype(float)**2)
    dl["nlo_plus_nll_combined"][mask] = unumpy.uarray(plot.unv(dl["nlo_plus_nll"][mask])+dl["nlo_plus_nll_errplus"][mask]/2.+dl["nlo_plus_nll_errminus"][mask]/2.,
        +dl["nlo_plus_nll_errplus"][mask]-dl["nlo_plus_nll_errminus"][mask])

    return dl