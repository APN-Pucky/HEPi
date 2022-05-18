import copy
import json
from re import I
from uncertainties import ufloat
from hepi.input import Input, order_to_string, xsec_to_order
from hepi.util import LD2DL


def load(f, dimensions=1):
    """
    Load xsec data from json in to something that works within hepi's plotting.

    Args:
        f : readable object, e.g. `open(filepath:str)`.
        dimensions (int) : 1 or 2 currently supported.
    """
    dict = json.load(f)

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
                    dicd[p1] = float(k)
                for p2 in params[1]:
                    dicd[p2] = float(l)
                dicd[order_to_string(inpu.order)] = ufloat(
                    dict["data"][k][l]["xsec_pb"],
                    dict["data"][k][l]["unc_pb"])
                dat.append(dicd)
    if dimensions == 1:
        for k in dict["data"]:
            dicd = copy.copy(inpu.__dict__)
            for p1 in params[0]:
                dicd[p1] = float(k)
            dicd[order_to_string(inpu.order)] = ufloat(
                dict["data"][k]["xsec_pb"], dict["data"][k]["unc_pb"])
            dat.append(dicd)
    return LD2DL(dat, actual_dict=True)