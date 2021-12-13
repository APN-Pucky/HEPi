from .. import Input, Result, LD2DL, get_output_dir, get_input_dir
import re
from uncertainties import ufloat_fromstr


class MadgraphResult(Result):
    def __init__(self, lo, nlo):
        Result.__init__(self, lo, nlo, nlo)


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
