import copy
import json
from re import I
from uncertainties import ufloat
from hepi.input import Input, order_to_string, xsec_to_order
from hepi.util import LD2DL, DL2DF


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
    inpu.runner = dict["tool"]
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
                if "unc_pb" in dict["data"][k][l]:
                    dicd[order_to_string(inpu.order)] = ufloat(
                        dict["data"][k][l]["xsec_pb"],
                        dict["data"][k][l]["unc_pb"])
                elif "unc_down_pb" in dict["data"][k][l] and "unc_up_pb" in dict["data"][k][l]:
                    dicd[order_to_string(inpu.order)+ "_NOERR"] = dict["data"][k][l]["xsec_pb"]
                    dicd[order_to_string(inpu.order)+ "_COMBINED"] = ufloat(
                        dict["data"][k][l]["xsec_pb"] + (dict["data"][k][l]["unc_up_pb"] + dict["data"][k][l]["unc_down_pb"]) / 2,
                        (dict["data"][k][l]["unc_up_pb"] - dict["data"][k][l]["unc_down_pb"]) / 2)
                else:
                    raise ValueError("No uncertainty found in data.")
                dat.append(dicd)
    if dimensions == 1:
        for k in dict["data"]:
            dicd = copy.copy(inpu.__dict__)
            for p1 in params[0]:
                dicd[p1] = float(k)
            if "unc_pb" in dict["data"][k]:
                dicd[order_to_string(inpu.order)] = ufloat(
                    dict["data"][k]["xsec_pb"], dict["data"][k]["unc_pb"])
            elif "unc_down_pb" in dict["data"][k] and "unc_up_pb" in dict["data"][k]:
                dicd[order_to_string(inpu.order)+ "_NOERR"] = dict["data"][k]["xsec_pb"]
                dicd[order_to_string(inpu.order)+ "_COMBINED"] = ufloat(
                    dict["data"][k]["xsec_pb"] + (dict["data"][k]["unc_up_pb"] + dict["data"][k]["unc_down_pb"]) / 2,
                    (dict["data"][k]["unc_up_pb"] - dict["data"][k]["unc_down_pb"]) / 2)
            else:
                raise ValueError("No uncertainty found in data.")
            dat.append(dicd)
    return DL2DF(LD2DL(dat, actual_dict=True))
