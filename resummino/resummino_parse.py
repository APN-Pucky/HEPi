import re
from uncertainties import ufloat_fromstr
"""
Parse Resummino's output
"""



def parse(output):
    lo_pattern = re.compile(r'^LO = \((.*)\) pb')
    nlo_pattern = re.compile(r'^NLO = \((.*)\) pb')
    nll_pattern = re.compile(r'^NLO\+NLL = \((.*)\) pb')    

    lo_result = None
    nlo_result = None
    nll_result = None
    for line in output:
        tmp = lo_pattern.search(line)
        if tmp is not None:
            lo_result = ufloat_fromstr(tmp.group(1).replace("+-","+/-"))
        tmp = nlo_pattern.search(line)
        if tmp is not None:
            nlo_result = ufloat_fromstr(tmp.group(1).replace("+-","+/-"))
        tmp = nll_pattern.search(line)
        if tmp is not None:
            nll_result = ufloat_fromstr(tmp.group(1).replace("+-","+/-"))
        
    return {"lo":lo_result, "nlo":nlo_result , "nlo+nll":nll_result}


fn = "./output/mass_master_3000_2000002_1000022.in.out"
f = open(fn)
print(parse(f))
