import warnings
from hepi.input import Order
from .. import Input, Result, get_output_dir
import re
from uncertainties import ufloat_fromstr
from string import Template
import pkgutil
import os
import shutil


class ResumminoResult(Result):
    """
    Resummino Result Data.

    Attributes:
        VNLO (double): virtual NLO result.
        RNLO (double): real NLO result.
        P_PLUS_K (double): collineare remainders P+K NLO result.
        RNLOG (double): real NLO gluon result.
        RNLOQ (double): real NLO quark result.
        VNLO_PLUS_P_PLUS_K (double): VNLO+P+K result.
        RNLO_PLUS_VNLO_PLUS_P_PLUS_K (double): RNLO+VNLO+P+K result.
    """

    def __init__(self, lo, nlo, nlo_plus_nll, annlo_plus_nnll, vnlo, p_plus_k,
                 rnlog, rnloq):
        """
        Sets given and computes dependent ``Attributes``.

        Args:
            lo (:obj:`double`): corresponds to :attr:`LO`.
            nlo (:obj:`double`): corresponds to :attr:`NLO`.
            nlo_plus_nll (:obj:`double`): corresponds to :attr:`NLO_PLUS_NLL`.
            vnlo (:obj:`double`): corresponds to :attr:`VNLO`.
            p_plus_k (:obj:`double`): corresponds to :attr:`P_PLUS_K`.
            rnlog (:obj:`double`): corresponds to :attr:`RNLOG`.
            rnloq (:obj:`double`): corresponds to :attr:`RNLOQ`.
        """
        Result.__init__(self, lo, nlo, nlo_plus_nll, annlo_plus_nnll)
        self.VNLO = vnlo
        self.P_PLUS_K = p_plus_k
        self.RNLOG = rnlog
        self.RNLOQ = rnloq
        if not (vnlo is None or p_plus_k is None):
            self.VNLO_PLUS_P_PLUS_K = self.VNLO + self.P_PLUS_K
        else:
            self.VNLO_PLUS_P_PLUS_K = None
        if not (rnlog is None or rnloq is None):
            self.RNLO = rnlog + rnloq
        else:
            self.RNLO = None
        if not (self.RNLO is None or self.VNLO_PLUS_P_PLUS_K is None):
            self.RNLO_PLUS_VNLO_PLUS_P_PLUS_K = self.RNLO + self.VNLO_PLUS_P_PLUS_K
        else:
            self.RNLO_PLUS_VNLO_PLUS_P_PLUS_K = None


def is_valid(file: str, p: Input, d,**kwargs) -> bool:
    """
    Verifies that an file is a complete output.

    Args:
        file (str): File path to be parsed.
        p (:class:`hepi.Input`): Onput parameters.
        d (:obj:`dict`): Param dictionary.

    Returns:
        bool : True if `file` could be parsed.
    """
    order = p.order
    data = pkgutil.get_data(__name__, "plot_template.in").decode('utf-8')
    src = Template(data)
    result = src.substitute(d)
    sname = d['slha']
    with open(file, mode='r') as f:
        with open(get_output_dir() + sname, 'r') as sf:
            if not kwargs['ignore_error'] and not f.read().startswith(result + "\n\n" + sf.read()):
                warnings.warn(
                    "Possible hash collision in " + file + " -> moved to " +
                    file + ".old", RuntimeWarning)
                shutil.move(file, file + ".old")
                return False
    res = parse_single(file)
    if res.LO is not None and order is Order.LO:
        return True
    if res.LO is not None and res.NLO is not None and order is Order.NLO:
        return True
    if res.LO is not None and res.NLO is not None and res.NLO_PLUS_NLL is not None and order is Order.NLO_PLUS_NLL:
        return True
    if res.LO is not None and res.NLO is not None and res.aNNLO_PLUS_NNLL is not None and order is Order.aNNLO_PLUS_NNLL:
        return True
    print("RESTART", res.LO, res.NLO, res.NLO_PLUS_NLL, file)
    return False


def parse_single(file: str) -> ResumminoResult:
    """
    Extracts LO, NLO and NLO+NLL from Resummino output file.

    Args:
        file (str): File path to be parsed.

    Returns:
        :class:`ResumminoResult` : If a value is not found in the file None is used.

    """
    # TODO generalize units like RS
    lo_pattern = re.compile(r'^LO = \((.*)\) pb')
    nlo_pattern = re.compile(r'^NLO = \((.*)\) pb')
    nll_pattern = re.compile(r'^NLO\+NLL = \((.*)\) pb')
    nnll_pattern = re.compile(r'^aNNLO\+NNLL = \((.*)\) pb')

    vnlo_pattern = re.compile(r'^vNLO = \((.*)\) pb')
    ppk_pattern = re.compile(r'^P\+K = \((.*)\) pb')
    rnlog_pattern = re.compile(r'^rNLOg = \((.*)\) pb')
    rnloq_pattern = re.compile(r'^rNLOq = \((.*)\) pb')

    lo_result = None
    nlo_result = None
    nll_result = None
    nnll_result = None

    vnlo_result = None
    ppk_result = None
    rnlog_result = None
    rnloq_result = None
    with open(file) as output:
        for line in output:
            tmp = lo_pattern.search(line)
            if tmp is not None:
                lo_result = ufloat_fromstr(tmp.group(1).replace("+-", "+/-"))
            tmp = nlo_pattern.search(line)
            if tmp is not None:
                nlo_result = ufloat_fromstr(tmp.group(1).replace("+-", "+/-"))
            tmp = nll_pattern.search(line)
            if tmp is not None:
                nll_result = ufloat_fromstr(tmp.group(1).replace("+-", "+/-"))
            tmp = nnll_pattern.search(line)
            if tmp is not None:
                nnll_result = ufloat_fromstr(tmp.group(1).replace("+-", "+/-"))
            tmp = vnlo_pattern.search(line)
            if tmp is not None:
                vnlo_result = ufloat_fromstr(tmp.group(1).replace("+-", "+/-"))
            tmp = ppk_pattern.search(line)
            if tmp is not None:
                ppk_result = ufloat_fromstr(tmp.group(1).replace("+-", "+/-"))
            tmp = rnlog_pattern.search(line)
            if tmp is not None:
                rnlog_result = ufloat_fromstr(
                    tmp.group(1).replace("+-", "+/-"))
            tmp = rnloq_pattern.search(line)
            if tmp is not None:
                rnloq_result = ufloat_fromstr(
                    tmp.group(1).replace("+-", "+/-"))
    if lo_result < 0:
        warnings.warn("LO < 0")
    if nlo_result < 0:
        warnings.warn("NLO < 0")
    if nll_result < 0:
        warnings.warn("NLL < 0")
    if nnll_result < 0:
        warnings.warn("NNLL < 0")
    return ResumminoResult(lo_result, nlo_result, nll_result, nnll_result,
                           vnlo_result, ppk_result, rnlog_result, rnloq_result)
