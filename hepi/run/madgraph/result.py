import warnings
from hepi.input import Order
from .. import Input, Result
import re
from uncertainties import ufloat_fromstr


class MadgraphResult(Result):
    """ MadGraph Result Data."""

    def __init__(self, lo, nlo):
        """Sets LO and NLO result. NLO+NLL is set to None."""
        Result.__init__(self, lo, nlo, None)


def is_valid(file: str, p: Input, d) -> bool:
    """
    Verifies that an file is a complete output.

    Args:
        file (str): File path to be parsed.
        p (:class:`hepi.Input`): Input parameters.
        d (:obj:`dict`): Param dictionary.

    Returns:
        bool : True if `file` could be parsed.
    """
    order = p.order
    res = parse_single(file)
    if order is not Order.NLO and order is not Order.LO:
        warnings.warn("MadGraph has only NLO and LO computation.")
    if res.LO is not None and order is Order.LO:
        return True
    if res.LO is not None and res.NLO is not None and order is Order.NLO:
        return True
    print("RESTART", res.LO, res.NLO, res.NLO_PLUS_NLL, file)
    return False


def parse_single(file) -> MadgraphResult:
    """
    Extracts Result from MadGraph output file.

    Note:
        This is only the result of one order. Therefore LO and NLO result in the return value are the same.


    Args:
        file (str): File path to be parsed.

    Returns:
        :class:`MadGraphResult` : If a value is not found in the file None is used.

    """
    # TODO generalize units like RS
    lo_pattern = re.compile(r'^\s*Total cross section:\s(\S+.*) pb')

    lo_result = None
    nlo_result = None
    with open(file) as output:
        for line in output:
            tmp = lo_pattern.search(line)
            if tmp is not None:
                if lo_result is None:
                    lo_result = ufloat_fromstr(
                        tmp.group(1).replace("+-", "+/-"))
                elif nlo_result is None:
                    nlo_result = ufloat_fromstr(
                        tmp.group(1).replace("+-", "+/-"))

    return MadgraphResult(lo_result, nlo_result)
