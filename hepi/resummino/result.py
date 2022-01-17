from hepi.input import Order
from .. import Input, Result, LD2DL, get_output_dir, get_input_dir
import re
from uncertainties import ufloat_fromstr
from string import Template
import pkgutil
import warnings

class ResumminoResult(Result):
    def __init__(self, lo, nlo, nlo_plus_nll, vnlo, p_plus_k, rnlog, rnloq):
        Result.__init__(self, lo, nlo, nlo_plus_nll)
        self.vnlo = vnlo
        self.p_plus_k = p_plus_k
        self.rnlog = rnlog
        self.rnloq = rnloq
        if not (vnlo is None or p_plus_k is None):
            self.vnlo_plus_p_plus_k = self.vnlo + self.p_plus_k
        else:
            self.vnlo_plus_p_plus_k = None
        if not (rnlog is None or rnloq is None):
            self.rnlo = rnlog+rnloq
        else:
            self.rnlo = None
        if not ( self.rnlo is None or self.vnlo_plus_p_plus_k is None):
            self.rnlo_plus_vnlo_plus_p_plus_k = self.rnlo + self.vnlo_plus_p_plus_k

def is_valid(file:str,p:Input,d):
    order = p.order
    data = pkgutil.get_data(__name__, "plot_template.in").decode(
                'utf-8')
    src = Template(data)
    result = src.substitute(d)
    sname = d['slha']
    with open(file,mode='r') as f:
        with open(get_input_dir() + sname, 'r') as sf:
            if not f.read().startswith(result + "\n\n" + sf.read()):
                warnings.warn("Possible hash collision in " + file,RuntimeWarning)
                exit(1)
                return False
    res = parse_single(file)
    if res.lo is not None and order is Order.LO:
        return True
    if res.lo is not None and res.nlo is not None and order is Order.NLO:
        return True
    if res.lo is not None and res.nlo is not None and res.nlo_plus_nll is not None and order is Order.NLO_PLUS_NLL:
        return True
    print("RESTART" ,res.lo, res.nlo,res.nlo_plus_nll, file)
    return False


def parse_single(file) -> ResumminoResult:
    # TODO generalize units like RS
    lo_pattern = re.compile(r'^LO = \((.*)\) pb')
    nlo_pattern = re.compile(r'^NLO = \((.*)\) pb')
    nll_pattern = re.compile(r'^NLO\+NLL = \((.*)\) pb')

    vnlo_pattern = re.compile(r'^vNLO = \((.*)\) pb')
    ppk_pattern = re.compile(r'^P\+K = \((.*)\) pb')
    rnlog_pattern = re.compile(r'^rNLOg = \((.*)\) pb')
    rnloq_pattern = re.compile(r'^rNLOq = \((.*)\) pb')

    lo_result = None
    nlo_result = None
    nll_result = None

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
    return ResumminoResult(lo_result, nlo_result, nll_result, vnlo_result, ppk_result, rnlog_result, rnloq_result)
