import copy
import json
from re import I
from uncertainties import ufloat
from hepi.input import Input, order_to_string, xsec_to_order


def load(f: str, dimensions=1):
    """
    Load xsec data from json in to something that works within hepi's plotting.

    Args:
        dimensions (int) : 1 or 2 currently supported.
    """
    dict = json.load(open(f))

    inpu = Input(
        xsec_to_order(dict["order"]),
        float(dict["Ecom [GeV]"]),
        -1,
        -1,
        slha=dict["process_latex"],
        pdf_lo=dict["PDF set"],
        pdf_nlo=dict["PDF set"],
        update=False,
    )
    dat = []
    params = dict["parameters"]
    if dimensions == 2:
        for k in dict["data"]:
            for l in dict["data"][k]:
                dicd = copy.copy(inpu.__dict__)
                for p1 in params[0]:
                    dicd[p1] = k
                for p2 in params[1]:
                    dicd[p2] = l
                dicd[order_to_string(inpu.order)] = ufloat(
                    dict["data"][k][l]["xsec_pb"],
                    dict["data"][k][l]["unc_pb"])
                print(dicd)
                dat.append(dicd)

            print(params[0], k, params[1], l, dict["data"][k][l])


#load("/home/apn/git/xsec/json/pp13_hinosplit_N2N1_NLO+NLL.json", 2)