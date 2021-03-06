"""Results and postprocessing for the :mod:`hepi` package."""
from .util import DictData
import numpy as np
from uncertainties import unumpy
from smpl import plot
import lhapdf
import warnings

required_numerical_uncertainty_factor = 10
"""If the numerical uncertainty is :attr:`required_numerical_uncertainty_factor` times higher than the scale or pdf uncertainty a warning is shown."""


class Result(DictData):
    """
    General result class.

    Attributes:
        LO (:obj:`double`): Leading Order result. Defaults to None.
        NLO (:obj:`double`): Next-to-Leading Order result. Defaults to None.
        NLO_PLUS_NLL (:obj:`double`): Next-to-Leading Order plus Next-to-Leading Logarithm result. Defaults to None.
        K_LO (:obj:`double`): LO divided by LO.
        K_NLO (:obj:`double`): NLO divided by LO result.
        K_NLO_PLUS_NLL (:obj:`double`): NLO+NLL divided by LO.
        K_aNNLO_PLUS_NNLL (:obj:`double`): aNNLO+NNLL divided by LO.
        NLO_PLUS_NLL_OVER_NLO (:obj:`double`): NLO+NLL divided by NLO.
        aNNLO_PLUS_NNLL_OVER_NLO (:obj:`double`): aNNLO+NNLL divided by NLO.
    """

    def __init__(self,
                 lo=None,
                 nlo=None,
                 nlo_plus_nll=None,
                 annlo_plus_nnll=None):
        """
        Sets given and computes dependent ``Attributes``.

        Args:
            lo (:obj:`double`): corresponds to :attr:`LO`.
            nlo (:obj:`double`): corresponds to :attr:`NLO`.
            nlo_plus_nll (:obj:`double`): corresponds to :attr:`NLO_PLUS_NLL`.
            annlo_plus_nnll (:obj:`double`): corresponds to :attr:`aNNLO_PLUS_NNLL`.
        """
        self.LO = lo
        self.NLO = nlo
        self.NLO_PLUS_NLL = nlo_plus_nll
        self.aNNLO_PLUS_NNLL = annlo_plus_nnll
        if lo is not None and lo != 0:
            self.K_LO = lo / lo
        else:
            self.K_LO = None
        if nlo is not None and lo != 0:
            self.K_NLO = nlo / lo
        else:
            self.K_NLO = None
        if nlo_plus_nll is not None and lo != 0:
            self.K_NLO_PLUS_NLL = nlo_plus_nll / lo
        else:
            self.K_NLO_PLUS_NLL = None

        if nlo_plus_nll is not None and nlo != 0:
            self.NLO_PLUS_NLL_OVER_NLO = nlo_plus_nll / nlo
        else:
            self.NLO_PLUS_NLL_OVER_NLO = None

        if annlo_plus_nnll is not None and lo != 0:
            self.K_aNNLO_PLUS_NNLL = annlo_plus_nnll / lo
        else:
            self.K_aNNLO_PLUS_NNLL = None

        if annlo_plus_nnll is not None and nlo != 0:
            self.aNNLO_PLUS_NNLL_OVER_NLO = annlo_plus_nnll / nlo
        else:
            self.aNNLO_PLUS_NNLL_OVER_NLO = None


# TODO detect which errors also for scales
def pdf_errors(li,
               dl,
               ordernames=["LO", "NLO", "aNNLO_PLUS_NNLL"],
               confidence_level=90):
    """
    Just like `pdf_error` but over a list of ordernames.
    """
    r_dl = dl
    for o in ordernames:
        r_dl = pdf_error(li, r_dl, o, confidence_level=confidence_level)

    return r_dl


def pdf_error(li, dl, ordername="LO", confidence_level=90):
    """
    Computes Parton Density Function (PDF) uncertainties through :func:`lhapdf.set.uncertainty`.

    Args:
        li (:obj:`list` of :class:`Input`): Input list.
        dl (:obj:`dict`): :class:`Result` dictionary with lists per entry.
        ordername (`str`): Name of the order.
        confidence_level (:obj:`double`): Confidence Level for PDF uncertainty

    Returns:
        :obj:`dict`: Modified `dl` with new `LO`/`NLO`/`NLO_PLUS_NLL` _ `PDF`/`PDF_CENTRAL`/`PDF_ERRPLUS`/`PDF_ERRMINUS`/`PDF_ERRSYM` entries.
            - `LO`/`NLO`/`NLO_PLUS_NLL` _ `PDF` contains a symmetrized :mod:`uncertainties` object.
    """
    global required_numerical_uncertainty_factor
    example = li[0]
    members = [
        attr for attr in dir(example)
        if not callable(getattr(example, attr)) and not attr.startswith("__")
    ]

    dl[ordername + "_PDF"] = np.array([None] * len(dl["pdfset_nlo"]))
    dl[ordername + "_PDF_CENTRAL"] = np.array([None] * len(dl["pdfset_nlo"]))
    dl[ordername + "_PDF_ERRPLUS"] = np.array([None] * len(dl["pdfset_nlo"]))
    dl[ordername + "_PDF_ERRMINUS"] = np.array([None] * len(dl["pdfset_nlo"]))
    dl[ordername + "_PDF_ERRSYM"] = np.array([None] * len(dl["pdfset_nlo"]))

    for i in range(len(dl["pdfset_nlo"])):
        if dl["pdfset_nlo"][i] == 0 and dl["mu_f"][i] == 1.0 and dl["mu_r"][
                i] == 1.0:
            pdfset = lhapdf.getPDFSet(dl["pdf_nlo"][i])
            pdfs = [0.0] * pdfset.size
            for j in range(len(dl["pdfset_nlo"])):
                same = True
                for s in members:
                    if not (
                            dl[s][i] == dl[s][j]
                    ) and s != "pdfset_nlo" and s != "precision" and s != "max_iters":
                        same = False
                if same:
                    pdfs[dl["pdfset_nlo"][j]] = j

        # lo_unc = pdfset.uncertainty(
        #    [plot.unv(dl["LO"][k]) for k in pdfs], -1)
        #if ordername == "LO":
        #    dl.loc[i, "LO_PDF_CENTRAL"] = plot.unv(dl["LO"][i])
        #    dl.loc[i, "LO_PDF_ERRPLUS"] = 0.0
        #    dl.loc[i, "LO_PDF_ERRMINUS"] = 0.0
        #    dl.loc[i, "LO_PDF_ERRSYM"] = 0.0
        #else:
            nlo_unc = pdfset.uncertainty(
                [plot.unv(dl[ordername][k]) for k in pdfs], confidence_level)
            dl.loc[i, ordername + "_PDF_CENTRAL"] = nlo_unc.central
            dl.loc[i, ordername + "_PDF_ERRPLUS"] = nlo_unc.errplus
            dl.loc[i, ordername + "_PDF_ERRMINUS"] = -nlo_unc.errminus
            dl.loc[i, ordername + "_PDF_ERRSYM"] = nlo_unc.errsymm
            #TODO error sym to minus and plus
            #if ordername != "LO":
            if (plot.usd(dl[ordername][i]) *
                    required_numerical_uncertainty_factor >
                    dl[ordername + "_PDF_ERRPLUS"][i]
                    or plot.usd(dl[ordername][i]) *
                    required_numerical_uncertainty_factor >
                    -dl[ordername + "_PDF_ERRMINUS"][i]):
                rel = plot.unv(dl[ordername][i])
                warnings.warn(
                    "too bad numerical precision vs pdf @ " + ordername +
                    " num: " + str(plot.usd(dl[ordername][i]) / rel * 100.) +
                    "% vs " +
                    str(dl[ordername + "_PDF_ERRPLUS"][i] / rel * 100.) +
                    "% to pdf: " +
                    str(dl[ordername + "_PDF_ERRMINUS"][i] / rel * 100.) + "%",
                    RuntimeWarning)

    mask = dl[ordername + "_PDF_CENTRAL"].notnull()
    dl.loc[mask, ordername + "_PDF"] = unumpy.uarray(
        plot.unv(dl[ordername + "_PDF_CENTRAL"][mask]) +
        dl[ordername + "_PDF_ERRPLUS"][mask] / 2. +
        dl[ordername + "_PDF_ERRMINUS"][mask] / 2.,
        (+dl[ordername + "_PDF_ERRPLUS"][mask] -
         dl[ordername + "_PDF_ERRMINUS"][mask]) / 2.)

    return dl


def scale_errors(li, dl, ordernames=["LO", "NLO", "aNNLO_PLUS_NNLL"]):
    """
    Just like `scale_error` but over a list of ordernames.
    """
    r_dl = dl
    for o in ordernames:
        r_dl = scale_error(li, r_dl, o)

    return r_dl


def scale_error(li, dl, ordername="LO"):
    """
    Computes seven-point scale uncertainties from the results where the renormalization and factorization scales are varied by factors of 2 and  relative factors of four are excluded (cf. :meth:`seven_point_scan`).

    Args:
        li (:obj:`list` of :class:`Input`): Input list.
        dl (:obj:`dict`): :class:`Result` dictionary with lists per entry.

    Returns:
        :obj:`dict`: Modified `dl` with new `LO`/`NLO`/`NLO_PLUS_NLL` _ `SCALE`/`SCALE_ERRPLUS`/`SCALE_ERRMINUS`/`SCALE_ERRSYM` entries.
            - `LO`/`NLO`/`NLO_PLUS_NLL` _ `SCALE` contains a symmetrized :mod:`uncertainties` object.
    """
    global required_numerical_uncertainty_factor
    example = li[0]
    members = [
        attr for attr in dir(example)
        if not callable(getattr(example, attr)) and not attr.startswith("__")
    ]
    dl[ordername + "_SCALE"] = np.array([None] * len(dl["pdfset_nlo"]))
    dl[ordername + "_SCALE_ERRPLUS"] = np.array([None] * len(dl["pdfset_nlo"]))
    dl[ordername + "_SCALE_ERRMINUS"] = np.array([None] *
                                                 len(dl["pdfset_nlo"]))

    for i in range(len(dl["pdfset_nlo"])):
        if dl["pdfset_nlo"][i] == 0 and dl["mu_f"][i] == 1.0 and dl["mu_r"][
                i] == 1.0:
            scales = []
            for j in range(len(dl["pdfset_nlo"])):
                same = True
                for s in members:
                    if not (
                            dl[s][i] == dl[s][j]
                    ) and s != "mu_f" and s != "mu_r" and s != "precision" and s != "max_iters":
                        same = False
                if same:
                    scales.append(j)

            # lo_unc = pdfset.uncertainty(
            #    [plot.unv(dl["LO"][k]) for k in pdfs], -1)
            dl.loc[i, ordername + "_SCALE_ERRPLUS"] = np.max(
                [plot.unv(dl[ordername][k])
                 for k in scales]) - plot.unv(dl[ordername][i])
            dl.loc[i, ordername + "_SCALE_ERRMINUS"] = np.min(
                [plot.unv(dl[ordername][k])
                 for k in scales]) - plot.unv(dl[ordername][i])
            if (plot.usd(dl[ordername][i]) *
                    required_numerical_uncertainty_factor >
                    dl[ordername + "_SCALE_ERRPLUS"][i]
                    or plot.usd(dl[ordername][i]) *
                    required_numerical_uncertainty_factor >
                    -dl[ordername + "_SCALE_ERRMINUS"][i]):
                rel = plot.unv(dl[ordername][i])
                warnings.warn(
                    "too bad numerical precision vs scale @ num:" + ordername +
                    " " + str(plot.usd(dl[ordername][i]) / rel * 100.) +
                    "% vs scale:" +
                    str(dl[ordername + "_SCALE_ERRPLUS"][i] / rel * 100.) +
                    "% to " +
                    str(dl[ordername + "_SCALE_ERRMINUS"][i] / rel * 100.) +
                    "%", RuntimeWarning)

    mask = dl[ordername + "_SCALE_ERRPLUS"].notnull()
    dl.loc[mask, ordername + "_SCALE"] = unumpy.uarray(
        plot.unv(dl[ordername][mask]) +
        dl[ordername + "_SCALE_ERRPLUS"][mask] / 2. +
        dl[ordername + "_SCALE_ERRMINUS"][mask] / 2.,
        (+dl[ordername + "_SCALE_ERRPLUS"][mask] -
         dl[ordername + "_SCALE_ERRMINUS"][mask]) / 2.)

    return dl


def combine_errors(dl, ordernames=["LO", "NLO", "aNNLO_PLUS_NNLL"]):
    """
    Just like `combine_error` but over a list of ordernames.
    """
    r_dl = dl
    for o in ordernames:
        r_dl = combine_error(r_dl, o)

    return r_dl


def combine_error(dl: dict, ordername="LO"):
    """
    Combines seven-point scale uncertainties and pdf uncertainties from the results by Pythagorean addition.

    Note:
        Running :func:`scale_errors` and :func:`pdf_errors` before is necessary.

    Args:
        dl (:obj:`dict`): :class:`Result` dictionary with lists per entry.

    Returns:
        :obj:`dict`: Modified `dl` with new `LO`/`NLO`/`NLO_PLUS_NLL` _ `COMBINED`/`ERRPLUS`/`ERRMINUS` entries.
            - `LO`/`NLO`/`NLO_PLUS_NLL` _ `COMBINED` contains a symmetrized :mod:`uncertainties` object.
    """
    dl[ordername + "_NOERR"] = np.array([None] * len(dl["pdfset_nlo"]))
    dl[ordername + "_ERRPLUS"] = np.array([None] * len(dl["pdfset_nlo"]))
    dl[ordername + "_ERRMINUS"] = np.array([None] * len(dl["pdfset_nlo"]))
    dl[ordername + "_COMBINED"] = np.array([None] * len(dl["pdfset_nlo"]))

    mask = dl[ordername + "_PDF_CENTRAL"].notnull()
    dl.loc[mask, ordername + "_NOERR"] = plot.unv(dl[ordername +
                                                     ""][mask]).astype(float)
    dl.loc[mask, ordername + "_ERRPLUS"] = np.sqrt(
        dl[ordername + "_PDF_ERRPLUS"][mask].astype(float)**2 +
        dl[ordername + "_SCALE_ERRPLUS"][mask].astype(float)**2)
    dl.loc[mask, ordername + "_ERRMINUS"] = -np.sqrt(
        dl[ordername + "_PDF_ERRMINUS"][mask].astype(float)**2 +
        dl[ordername + "_SCALE_ERRMINUS"][mask].astype(float)**2)
    dl.loc[mask, ordername + "_COMBINED"] = unumpy.uarray(
        plot.unv(dl[ordername + ""][mask]) +
        dl[ordername + "_ERRPLUS"][mask] / 2. +
        dl[ordername + "_ERRMINUS"][mask] / 2.,
        +dl[ordername + "_ERRPLUS"][mask] - dl[ordername + "_ERRMINUS"][mask])

    return dl
