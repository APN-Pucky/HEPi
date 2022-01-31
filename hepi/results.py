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
        self.LO = lo
        self.NLO = nlo
        self.NLO_PLUS_NLL = nlo_plus_nll
        if lo is not None and lo != 0:
            self.K_LO = lo/lo
        else:
            self.K_LO = None
        #else:
        #    print("lo None or lo=",lo)
        if nlo is not None and lo != 0:
            self.K_NLO = nlo/lo
        else:
            self.K_NLO = None
        #else:
        #    print("nlo None or lo=",lo)
        if nlo_plus_nll is not None and lo != 0:
            self.K_NLO_PLUS_NLL = nlo_plus_nll/lo
        else:
            self.K_NLO_PLUS_NLL = None

        if nlo_plus_nll is not None and nlo != 0:
            self.NLO_PLUS_NLL_OVER_NLO = nlo_plus_nll/nlo
        else:
            self.NLO_PLUS_NLL_OVER_NLO  =None
        #else:
        #    print("nlo+nll None or lo=",lo)





def pdf_error(li, dl):
    global required_numerical_uncertainty_factor
    example = li[0]
    members = [attr for attr in dir(example) if not callable(
        getattr(example, attr)) and not attr.startswith("__")]
    dl["LO_PDF"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["LO_PDF_CENTRAL"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["LO_PDF_ERRPLUS"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["LO_PDF_ERRMINUS"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["LO_PDF_ERRSYM"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["NLO_PDF"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["NLO_PDF_CENTRAL"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["NLO_PDF_ERRPLUS"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["NLO_PDF_ERRMINUS"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["NLO_PDF_ERRSYM"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["NLO_PLUS_NLL_PDF"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["NLO_PLUS_NLL_PDF_CENTRAL"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["NLO_PLUS_NLL_PDF_ERRPLUS"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["NLO_PLUS_NLL_PDF_ERRMINUS"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["NLO_PLUS_NLL_PDF_ERRSYM"] = np.array([None]*len(dl["pdfset_nlo"]))
    for i in range(len(dl["pdfset_nlo"])):
        if dl["pdfset_nlo"][i] == 0 and dl["mu_f"][i] == 1.0 and dl["mu_r"][i] == 1.0:
            set = lhapdf.getPDFSet(dl["pdf_nlo"][i])
            pdfs = [0.0] * set.size
            for j in range(len(dl["pdfset_nlo"])):
                same = True
                for s in members:
                    if not (dl[s][i] == dl[s][j]) and s != "pdfset_nlo" and s != "precision" and s!="max_iters":
                        same = False
                if same:
                    pdfs[dl["pdfset_nlo"][j]] = j

            dl["LO_PDF_CENTRAL"][i] = plot.unv(dl["LO"][i])
            dl["LO_PDF_ERRPLUS"][i] = 0.0
            dl["LO_PDF_ERRMINUS"][i] = 0.0
            dl["LO_PDF_ERRSYM"][i] = 0.0
            # lo_unc = set.uncertainty(
            #    [plot.unv(dl["LO"][k]) for k in pdfs], -1)
            nlo_unc = set.uncertainty(
                [plot.unv(dl["NLO"][k]) for k in pdfs], -1)
            dl["NLO_PDF_CENTRAL"][i] = nlo_unc.central
            dl["NLO_PDF_ERRPLUS"][i] = nlo_unc.errplus
            dl["NLO_PDF_ERRMINUS"][i] = -nlo_unc.errminus
            dl["NLO_PDF_ERRSYM"][i] = nlo_unc.errsymm
            #TODO error sym to minus and plus
            if(plot.usd(dl["NLO"][i])*required_numerical_uncertainty_factor > dl["NLO_PDF_ERRPLUS"][i] or  plot.usd(dl["NLO"][i])*required_numerical_uncertainty_factor > -dl["NLO_PDF_ERRMINUS"][i]):
                warnings.warn("too low numerical nlo precision vs pdf", RuntimeWarning)

            nlo_plus_nll_unc = set.uncertainty(
                [plot.unv(dl["NLO_PLUS_NLL"][k]) for k in pdfs], -1)
            dl["NLO_PLUS_NLL_PDF_CENTRAL"][i] = nlo_plus_nll_unc.central
            dl["NLO_PLUS_NLL_PDF_ERRPLUS"][i] = nlo_plus_nll_unc.errplus
            dl["NLO_PLUS_NLL_PDF_ERRMINUS"][i] = -nlo_plus_nll_unc.errminus
            dl["NLO_PLUS_NLL_PDF_ERRSYM"][i] = nlo_plus_nll_unc.errsymm
            #TODO error sym to minus and plus
            if(plot.usd(dl["NLO_PLUS_NLL"][i])*required_numerical_uncertainty_factor > dl["NLO_PLUS_NLL_PDF_ERRPLUS"][i] or  plot.usd(dl["NLO_PLUS_NLL"][i])*required_numerical_uncertainty_factor > -dl["NLO_PLUS_NLL_PDF_ERRMINUS"][i]):
                warnings.warn("too low numerical nlo_plus_nll precision vs pdf", RuntimeWarning)


    mask = dl["LO_PDF_CENTRAL"]!= np.array(None)
    dl["LO_PDF"][mask] = unumpy.uarray(plot.unv(dl["LO"][mask])+dl["LO_PDF_ERRPLUS"][mask]/2.+dl["LO_PDF_ERRMINUS"][mask]/2.,
        (+dl["LO_PDF_ERRPLUS"][mask]-dl["LO_PDF_ERRMINUS"][mask])/2.)

    mask = dl["NLO_PDF_CENTRAL"]!= np.array(None)
    dl["NLO_PDF"][mask] = unumpy.uarray(plot.unv(dl["NLO"][mask])+dl["NLO_PDF_ERRPLUS"][mask]/2.+dl["NLO_PDF_ERRMINUS"][mask]/2.,
        (+dl["NLO_PDF_ERRPLUS"][mask]-dl["NLO_PDF_ERRMINUS"][mask])/2.)

    mask = dl["NLO_PLUS_NLL_PDF_CENTRAL"]!= np.array(None)
    dl["NLO_PLUS_NLL_PDF"][mask] = unumpy.uarray(plot.unv(dl["NLO_PLUS_NLL"][mask])+dl["NLO_PLUS_NLL_PDF_ERRPLUS"][mask]/2.+dl["NLO_PLUS_NLL_PDF_ERRMINUS"][mask]/2.,
        (+dl["NLO_PLUS_NLL_PDF_ERRPLUS"][mask]-dl["NLO_PLUS_NLL_PDF_ERRMINUS"][mask])/2.)
    return dl


def scale_error(li, dl):
    global required_numerical_uncertainty_factor
    example = li[0]
    members = [attr for attr in dir(example) if not callable(
        getattr(example, attr)) and not attr.startswith("__")]
    dl["LO_SCALE"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["LO_SCALE_ERRPLUS"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["LO_SCALE_ERRMINUS"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["NLO_SCALE"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["NLO_SCALE_ERRPLUS"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["NLO_SCALE_ERRMINUS"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["NLO_PLUS_NLL_SCALE"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["NLO_PLUS_NLL_SCALE_ERRPLUS"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["NLO_PLUS_NLL_SCALE_ERRMINUS"] = np.array([None]*len(dl["pdfset_nlo"]))
    for i in range(len(dl["pdfset_nlo"])):
        if dl["pdfset_nlo"][i] == 0 and dl["mu_f"][i] == 1.0 and dl["mu_r"][i] == 1.0:
            scales = []
            for j in range(len(dl["pdfset_nlo"])):
                same = True
                for s in members:
                    if not (dl[s][i] == dl[s][j]) and s != "mu_f" and s != "mu_r" and s != "precision" and s!="max_iters":
                        same = False
                if same:
                    scales.append(j)

            # lo_unc = set.uncertainty(
            #    [plot.unv(dl["LO"][k]) for k in pdfs], -1)
            dl["LO_SCALE_ERRPLUS"][i] = np.max(
                [plot.unv(dl["LO"][k]) for k in scales])-plot.unv(dl["LO"][i])
            dl["LO_SCALE_ERRMINUS"][i] = np.min(
                [plot.unv(dl["LO"][k]) for k in scales])-plot.unv(dl["LO"][i])
            if(plot.usd(dl["LO"][i])*required_numerical_uncertainty_factor > dl["LO_SCALE_ERRPLUS"][i] or  plot.usd(dl["LO"][i])*required_numerical_uncertainty_factor > -dl["LO_SCALE_ERRMINUS"][i]):
                warnings.warn("too low numerical lo precision vs scale", RuntimeWarning)

            dl["NLO_SCALE_ERRPLUS"][i] = np.max(
                [plot.unv(dl["NLO"][k]) for k in scales])-plot.unv(dl["NLO"][i])
            dl["NLO_SCALE_ERRMINUS"][i] = np.min(
                [plot.unv(dl["NLO"][k]) for k in scales])-plot.unv(dl["NLO"][i])
            if(plot.usd(dl["NLO"][i])*required_numerical_uncertainty_factor > dl["NLO_SCALE_ERRPLUS"][i] or  plot.usd(dl["NLO"][i])*required_numerical_uncertainty_factor > -dl["NLO_SCALE_ERRMINUS"][i]):
                warnings.warn("too low numerical nlo precision vs scale", RuntimeWarning)

            dl["NLO_PLUS_NLL_SCALE_ERRPLUS"][i] = np.max(
                [plot.unv(dl["NLO_PLUS_NLL"][k]) for k in scales])-plot.unv(dl["NLO_PLUS_NLL"][i])
            dl["NLO_PLUS_NLL_SCALE_ERRMINUS"][i] = np.min(
                [plot.unv(dl["NLO_PLUS_NLL"][k]) for k in scales])-plot.unv(dl["NLO_PLUS_NLL"][i])
            if(plot.usd(dl["NLO_PLUS_NLL"][i])*required_numerical_uncertainty_factor > dl["NLO_PLUS_NLL_SCALE_ERRPLUS"][i] or  plot.usd(dl["NLO_PLUS_NLL"][i])*required_numerical_uncertainty_factor > -dl["NLO_PLUS_NLL_SCALE_ERRMINUS"][i]):
                warnings.warn("too low numerical nlo_plus_nll precision vs scale", RuntimeWarning)

    mask = dl["LO_SCALE_ERRPLUS"]!= np.array(None)
    dl["LO_SCALE"][mask] = unumpy.uarray(plot.unv(dl["LO"][mask])+dl["LO_SCALE_ERRPLUS"][mask]/2.+dl["LO_SCALE_ERRMINUS"][mask]/2.,
        (+dl["LO_SCALE_ERRPLUS"][mask]-dl["LO_SCALE_ERRMINUS"][mask])/2.)

    mask = dl["NLO_SCALE_ERRPLUS"]!= np.array(None)
    dl["NLO_SCALE"][mask] = unumpy.uarray(plot.unv(dl["NLO"][mask])+dl["NLO_SCALE_ERRPLUS"][mask]/2.+dl["NLO_SCALE_ERRMINUS"][mask]/2.,
        (+dl["NLO_SCALE_ERRPLUS"][mask]-dl["NLO_SCALE_ERRMINUS"][mask])/2.)

    mask = dl["NLO_PLUS_NLL_SCALE_ERRPLUS"]!= np.array(None)
    dl["NLO_PLUS_NLL_SCALE"][mask] = unumpy.uarray(plot.unv(dl["NLO_PLUS_NLL"][mask])+dl["NLO_PLUS_NLL_SCALE_ERRPLUS"][mask]/2.+dl["NLO_PLUS_NLL_SCALE_ERRMINUS"][mask]/2.,
        (+dl["NLO_PLUS_NLL_SCALE_ERRPLUS"][mask]-dl["NLO_PLUS_NLL_SCALE_ERRMINUS"][mask])/2.)
    
    return dl

def combine_errors(dl):
    dl["LO_NOERR"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["LO_ERRPLUS"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["LO_ERRMINUS"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["LO_COMBINED"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["NLO_NOERR"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["NLO_ERRPLUS"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["NLO_ERRMINUS"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["NLO_COMBINED"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["NLO_PLUS_NLL_NOERR"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["NLO_PLUS_NLL_ERRPLUS"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["NLO_PLUS_NLL_ERRMINUS"] = np.array([None]*len(dl["pdfset_nlo"]))
    dl["NLO_PLUS_NLL_COMBINED"] = np.array([None]*len(dl["pdfset_nlo"]))


    mask = dl["LO_PDF_CENTRAL"]!= np.array(None)
    dl["LO_NOERR"][mask]= plot.unv(dl["LO"][mask]).astype(float)
    dl["LO_ERRPLUS"][mask]= np.sqrt(dl["LO_PDF_ERRPLUS"][mask].astype(float)**2+dl["LO_SCALE_ERRPLUS"][mask].astype(float)**2)
    dl["LO_ERRMINUS"][mask]= -np.sqrt(dl["LO_PDF_ERRMINUS"][mask].astype(float)**2+dl["LO_SCALE_ERRMINUS"][mask].astype(float)**2)
    dl["LO_COMBINED"][mask] = unumpy.uarray(plot.unv(dl["LO"][mask])+dl["LO_ERRPLUS"][mask]/2.+dl["LO_ERRMINUS"][mask]/2.,
        +dl["LO_ERRPLUS"][mask]-dl["LO_ERRMINUS"][mask])

    mask = dl["NLO_PDF_CENTRAL"]!= np.array(None)
    dl["NLO_NOERR"][mask]= plot.unv(dl["NLO"][mask]).astype(float)
    dl["NLO_ERRPLUS"][mask]= np.sqrt(dl["NLO_PDF_ERRPLUS"][mask].astype(float)**2+dl["NLO_SCALE_ERRPLUS"][mask].astype(float)**2)
    dl["NLO_ERRMINUS"][mask]= -np.sqrt(dl["NLO_PDF_ERRMINUS"][mask].astype(float)**2+dl["NLO_SCALE_ERRMINUS"][mask].astype(float)**2)
    dl["NLO_COMBINED"][mask] = unumpy.uarray(plot.unv(dl["NLO"][mask])+dl["NLO_ERRPLUS"][mask]/2.+dl["NLO_ERRMINUS"][mask]/2.,
        +dl["NLO_ERRPLUS"][mask]-dl["NLO_ERRMINUS"][mask])

    mask = dl["NLO_PLUS_NLL_PDF_CENTRAL"]!= np.array(None)
    dl["NLO_PLUS_NLL_NOERR"][mask]= plot.unv(dl["NLO_PLUS_NLL"][mask]).astype(float)
    dl["NLO_PLUS_NLL_ERRPLUS"][mask]= np.sqrt(dl["NLO_PLUS_NLL_PDF_ERRPLUS"][mask].astype(float)**2+dl["NLO_PLUS_NLL_SCALE_ERRPLUS"][mask].astype(float)**2)
    dl["NLO_PLUS_NLL_ERRMINUS"][mask]= -np.sqrt(dl["NLO_PLUS_NLL_PDF_ERRMINUS"][mask].astype(float)**2+dl["NLO_PLUS_NLL_SCALE_ERRMINUS"][mask].astype(float)**2)
    dl["NLO_PLUS_NLL_COMBINED"][mask] = unumpy.uarray(plot.unv(dl["NLO_PLUS_NLL"][mask])+dl["NLO_PLUS_NLL_ERRPLUS"][mask]/2.+dl["NLO_PLUS_NLL_ERRMINUS"][mask]/2.,
        +dl["NLO_PLUS_NLL_ERRPLUS"][mask]-dl["NLO_PLUS_NLL_ERRMINUS"][mask])

    return dl
