"""Results and postprocessing for the :mod:`hepi` package."""
from .util import DictData
import numpy as np
from uncertainties import unumpy
from smpl import plot
import warnings
import tqdm
#from pqdm.processes import pqdm as ppqdm
from pqdm.threads import pqdm as tpqdm
import multiprocessing as mp
from smpl.parallel import par

#If the numerical uncertainty times :attr:`required_numerical_uncertainty_factor` is higher than the scale or pdf uncertainty a warning is shown.
required_numerical_uncertainty_factor = 5


def my_parallel(arr, f, n_jobs=None, desc=None):
    """
    Parallel execution of f on each element of args
    """
    n_jobs = n_jobs or mp.cpu_count()
    sa = np.array_split(np.array(arr), len(arr) / n_jobs)
    res = []
    for i in tqdm.tqdm(range(len(sa)), desc=desc):
        res += par(f, sa[i])
    return res


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
               ordernames=None,
               confidence_level=90,n_jobs=None):
    """
    Just like `pdf_error` but over a list of ordernames.
    """
    if ordernames is None:
        ordernames = ["LO", "NLO", "aNNLO_PLUS_NNLL"]
    r_dl = dl
    for o in ordernames:
        r_dl = pdf_error(li, r_dl, o, confidence_level=confidence_level,n_jobs=n_jobs)

    return r_dl


def _pdf_error_single(members, i, dl, ordername, confidence_level=90):  
    #import lhapdf
    if dl["pdfset_nlo"][i] == 0 and dl["mu_f"][i] == 1.0 and dl["mu_r"][
            i] == 1.0:
        pdfset = lhapdf.getPDFSet(dl["pdf_nlo"][i])
        pdfs = [0.0] * pdfset.size
        ddl = dl[members].drop(columns=["pdfset_nlo", "precision","max_iters"])
        bol = ddl.eq(ddl.iloc[i]).all(axis='columns')
        for j in range(len(dl["pdfset_nlo"])):
            if bol[j]:
                pdfs[dl["pdfset_nlo"][j]] = j

    # lo_unc = pdfset.uncertainty(
    #    [plot.unv(dl["LO"][k]) for k in pdfs], -1)
    #if ordername == "LO":
    #    dl.loc[i, "LO_PDF_CENTRAL"] = plot.unv(dl["LO"][i])
    #    dl.loc[i, "LO_PDF_ERRPLUS"] = 0.0
    #    dl.loc[i, "LO_PDF_ERRMINUS"] = 0.0
    #    dl.loc[i, "LO_PDF_ERRSYM"] = 0.0
    #else:
    #print([float(plot.unv(dl[ordername][k])) for k in pdfs])
        nlo_unc = pdfset.uncertainty(
            [float(plot.unv(dl[ordername][k])) for k in pdfs],
            confidence_level)

    return (i,nlo_unc)


def pdf_error(li, dl, ordername="LO", confidence_level=90, n_jobs=None):
    """
    Computes Parton Density Function (PDF) uncertainties through :func:`lhapdf.set.uncertainty`.

    Args:
        li (:obj:`list` of :class:`Input`): Input list.
        dl (:obj:`dict`): :class:`Result` dictionary with lists per entry.
        ordername (`str`): Name of the order.
        confidence_level (:obj:`double`): Confidence Level for PDF uncertainty

    Returns:
        :obj:`dict`: Modified `dl` with new `ordername_{PDF,PDF_CENTRAL,PDF_ERRPLUS,PDF_ERRMINUS,PDF_ERRSYM}` entries.
            - (`ordername`)_`PDF` contains a symmetrized :mod:`uncertainties` object.
    """
    global required_numerical_uncertainty_factor
    try:
        import lhapdf
    except ImportError:
        raise RuntimeError("LHAPDF with python bindings needed to compute PDF uncertainties. Make sure you set the PYTHONPATH correctly (i.e. correct python version).")
    if not lhapdf.availablePDFSets():
        raise RuntimeError("No PDF sets found. Make sure the environment variable LHAPDF_DATA_DIR points to the correct location (.../share/LHAPDF).")
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

    args = [{
        "members": members,
        "i": i,
        "dl": dl,
        "ordername": ordername,
        "confidence_level": confidence_level
    } for i in range(len(dl["pdfset_nlo"])) if dl["pdfset_nlo"][i] == 0
            and dl["mu_f"][i] == 1.0 and dl["mu_r"][i] == 1.0]
    ret = tpqdm(args,
                _pdf_error_single,
                n_jobs=n_jobs if n_jobs is not None else mp.cpu_count(),
                argument_type='kwargs',
                desc="PDF uncertainty @ " + ordername)
    for i, nlo_unc in ret:
        dl.loc[i, ordername + "_PDF_CENTRAL"] = nlo_unc.central
        dl.loc[i, ordername + "_PDF_ERRPLUS"] = nlo_unc.errplus
        dl.loc[i, ordername + "_PDF_ERRMINUS"] = -nlo_unc.errminus
        dl.loc[i, ordername + "_PDF_ERRSYM"] = nlo_unc.errsymm
        #TODO error sym to minus and plus
        #if :
        if (ordername != "LO" and
            (plot.usd(dl[ordername][i]) * required_numerical_uncertainty_factor
             > dl[ordername + "_PDF_ERRPLUS"][i] or
             plot.usd(dl[ordername][i]) * required_numerical_uncertainty_factor
             > -dl[ordername + "_PDF_ERRMINUS"][i])):
            rel = plot.unv(dl[ordername][i])
            warnings.warn(
                "too bad numerical precision vs pdf @ " + ordername +
                " num: " + str(plot.usd(dl[ordername][i]) / rel * 100.) +
                "% vs " + str(dl[ordername + "_PDF_ERRPLUS"][i] / rel * 100.) +
                "% to pdf: " +
                str(dl[ordername + "_PDF_ERRMINUS"][i] / rel * 100.) + "%",
                RuntimeWarning)

    mask = dl[ordername + "_PDF_CENTRAL"].notnull()
    dl.loc[mask, ordername + "_PDF"] = unumpy.uarray(
        plot.unv(dl[ordername + "_PDF_CENTRAL"][mask]) +
        dl[ordername + "_PDF_ERRPLUS"][mask] / 2. +
        dl[ordername + "_PDF_ERRMINUS"][mask] / 2.,
        (dl[ordername + "_PDF_ERRPLUS"][mask] -
         dl[ordername + "_PDF_ERRMINUS"][mask]) / 2.)

    return dl


def scale_errors(li, dl, ordernames=None,n_jobs=None):
    """
    Just like `scale_error` but over a list of ordernames.
    """
    if ordernames is None:
        ordernames = ["LO", "NLO", "aNNLO_PLUS_NNLL"]
    r_dl = dl
    for o in ordernames:
        r_dl = scale_error(li, r_dl, o, n_jobs=n_jobs)

    return r_dl

def _scale_error_single(members,i,dl,ordername="LO"):
    if dl["pdfset_nlo"][i] == 0 and dl["mu_f"][i] == 1.0 and dl["mu_r"][
        i] == 1.0:
        scales = []
        ddl = dl[members].drop(columns=["mu_f","mu_r", "precision","max_iters"])
        bol = ddl.eq(ddl.iloc[i]).all(axis='columns')
        for j in range(len(dl["pdfset_nlo"])):
            if bol[j]:
                scales.append(j)
    # index, errplus,errminus
    return (
        i,
        np.max( [plot.unv(dl[ordername][k]) for k in scales]) - plot.unv(dl[ordername][i]),
        np.min( [plot.unv(dl[ordername][k]) for k in scales]) - plot.unv(dl[ordername][i])
    )

def scale_error(li, dl, ordername="LO",n_jobs=None):
    """
    Computes seven-point scale uncertainties from the results where the renormalization and factorization scales are varied by factors of 2 and  relative factors of four are excluded (cf. :meth:`seven_point_scan`).

    Args:
        li (:obj:`list` of :class:`Input`): Input list.
        dl (:obj:`dict`): :class:`Result` dictionary with lists per entry.

    Returns:
        :obj:`dict`: Modified `dl` with new `ordername_{SCALE,SCALE_ERRPLUS,SCALE_ERRMINUS}` entries.
            - `ordername_SCALE` contains a symmetrized :mod:`uncertainties` object.
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


    args = [{
        "members": members,
        "i": i,
        "dl": dl,
        "ordername": ordername,
    } for i in range(len(dl["pdfset_nlo"])) if dl["pdfset_nlo"][i] == 0
            and dl["mu_f"][i] == 1.0 and dl["mu_r"][i] == 1.0]
    ret = tpqdm(args,
                _scale_error_single,
                n_jobs=n_jobs if n_jobs is not None else mp.cpu_count(),
                argument_type='kwargs',
                desc="Scale uncertainty @ " + ordername)
    for i,errplus,errminus in ret:
        # lo_unc = pdfset.uncertainty(
        #    [plot.unv(dl["LO"][k]) for k in pdfs], -1)
        dl.loc[i, ordername + "_SCALE_ERRPLUS"] = errplus
        dl.loc[i, ordername + "_SCALE_ERRMINUS"] = errminus
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


def combine_errors(dl, ordernames=None):
    """
    Just like `combine_error` but over a list of ordernames.
    """
    if ordernames is None:
        ordernames = ["LO", "NLO", "aNNLO_PLUS_NNLL"]
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
        :obj:`dict`: Modified `dl` with new `ordername_{COMBINED,ERRPLUS,ERRMINUS}` entries.
            - `ordername_COMBINED` contains a symmetrized :mod:`uncertainties` object.
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
        (+dl[ordername + "_ERRPLUS"][mask] - dl[ordername + "_ERRMINUS"][mask])
        / 2.)

    return dl
