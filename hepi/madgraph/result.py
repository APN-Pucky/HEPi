from hepi.input import Order
from .. import Input, Result, LD2DL, get_output_dir, get_input_dir
import re
from uncertainties import ufloat_fromstr


class MadgraphResult(Result):
    def __init__(self, lo, nlo):
        Result.__init__(self, lo, nlo, nlo)


def is_valid(file:str,p:Input,d):
    order = p.order
    res = parse_single(file)
    if res.LO is not None and order is Order.LO:
        return True
    if res.LO is not None and res.NLO is not None and order is Order.NLO:
        return True
    if res.LO is not None and res.NLO is not None and res.NLO_PLUS_NLL is not None and order is Order.NLO_PLUS_NLL:
        return True
    print("RESTART" ,res.LO, res.NLO,res.NLO_PLUS_NLL, file)
    return False

def parse_single(file) -> MadgraphResult:
    # TODO generalize units like RS
    lo_pattern = re.compile(r'^\s*Total cross section:\s*(.*) pb')

    lo_result = None
    with open(file) as output:
        for line in output:
            tmp = lo_pattern.search(line)
            if tmp is not None:
                lo_result = ufloat_fromstr(tmp.group(1).replace("+-", "+/-"))

    return MadgraphResult(lo_result, lo_result)
