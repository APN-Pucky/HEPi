import copy
import json
from re import I
from uncertainties import ufloat
from hepi.input import Input, order_to_string, xsec_to_order
from hepi.util import LD2DL, DL2DF

def load_json_with_metadata(file):

    """
    Load xsec data from json in to something that works within hepi's plotting.

    Args:
        f : readable object, e.g. `open(filepath:str)`.
        dimensions (int) : 1 or 2 currently supported.
    """
    dict = json.load(file)

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
    so = order_to_string(inpu.order)
    inpu.runner = dict["tool"]
    dat = []
    params = dict["parameters"]
    dimensions = len(params)
    if dimensions == 2:
        for k in dict["data"]:
            for l in dict["data"][k]:
                dicd = copy.copy(inpu.__dict__)
                for p1 in params[0]:
                    dicd[p1] = float(k)
                for p2 in params[1]:
                    dicd[p2] = float(l)
                if "unc_pb" in dict["data"][k][l]:
                    dicd[so] = ufloat(
                        dict["data"][k][l]["xsec_pb"],
                        dict["data"][k][l]["unc_pb"])
                elif "unc_down_pb" in dict["data"][k][l] and "unc_up_pb" in dict["data"][k][l]:
                    dicd[so+ "_NOERR"] = dict["data"][k][l]["xsec_pb"]
                    dicd[so+ "_COMBINED"] = ufloat(
                        dict["data"][k][l]["xsec_pb"] + (dict["data"][k][l]["unc_up_pb"] + dict["data"][k][l]["unc_down_pb"]) / 2,
                        (dict["data"][k][l]["unc_up_pb"] - dict["data"][k][l]["unc_down_pb"]) / 2)
                    if "unc_scale_up_pb" in dict["data"][k][l] and "unc_scale_down_pb" in dict["data"][k][l]:
                        dicd[so+ "_SCALE"] = ufloat(
                            dict["data"][k][l]["xsec_pb"] + (dict["data"][k][l]["unc_scale_up_pb"] + dict["data"][k][l]["unc_scale_down_pb"]) / 2,
                            (dict["data"][k][l]["unc_scale_up_pb"] - dict["data"][k][l]["unc_scale_down_pb"]) / 2 )
                    if "unc_pdf_up_pb" in dict["data"][k][l] and "unc_pdf_down_pb" in dict["data"][k][l]:
                        dicd[so+ "_PDF"] = ufloat(
                            dict["data"][k][l]["xsec_pb"] + (dict["data"][k][l]["unc_pdf_up_pb"] + dict["data"][k][l]["unc_pdf_down_pb"]) / 2,
                            (dict["data"][k][l]["unc_pdf_up_pb"] - dict["data"][k][l]["unc_pdf_down_pb"]) / 2 )
                else:
                    raise ValueError("No uncertainty found in data.")
                dat.append(dicd)
    if dimensions == 1:
        for k in dict["data"]:
            dicd = copy.copy(inpu.__dict__)
            for p1 in params[0]:
                dicd[p1] = float(k)
            if "unc_pb" in dict["data"][k]:
                dicd[so] = ufloat(
                    dict["data"][k]["xsec_pb"], dict["data"][k]["unc_pb"])
            elif "unc_down_pb" in dict["data"][k] and "unc_up_pb" in dict["data"][k]:
                dicd[so+ "_NOERR"] = dict["data"][k]["xsec_pb"]
                dicd[so+ "_COMBINED"] = ufloat(
                    dict["data"][k]["xsec_pb"] + (dict["data"][k]["unc_up_pb"] + dict["data"][k]["unc_down_pb"]) / 2,
                    (dict["data"][k]["unc_up_pb"] - dict["data"][k]["unc_down_pb"]) / 2)
                if "unc_scale_up_pb" in dict["data"][k] and "unc_scale_down_pb" in dict["data"][k]:
                    dicd[so+ "_SCALE"] = ufloat(
                        dict["data"][k]["xsec_pb"] + (dict["data"][k]["unc_scale_up_pb"] + dict["data"][k]["unc_scale_down_pb"]) / 2,
                        (dict["data"][k]["unc_scale_up_pb"] - dict["data"][k]["unc_scale_down_pb"]) / 2)
                if "unc_pdf_up_pb" in dict["data"][k] and "unc_pdf_down_pb" in dict["data"][k]:
                    dicd[so+ "_PDF"] = ufloat(
                        dict["data"][k]["xsec_pb"] + (dict["data"][k]["unc_pdf_up_pb"] + dict["data"][k]["unc_pdf_down_pb"]) / 2,
                        (dict["data"][k]["unc_pdf_up_pb"] - dict["data"][k]["unc_pdf_down_pb"]) / 2)
            else:
                raise ValueError("No uncertainty found in data.")
            dat.append(dicd)
    ddf = DL2DF(LD2DL(dat, actual_dict=True))
    # copy mass list to single masses
    for k in ddf.keys():
        if k.startswith("mass_"):
            for m in k[5:].split("_"): 
                ddf["mass_"+ m] = ddf[k]
    return ddf, params

def load_json(f,dimension=1):
    return load_json_with_metadata(f)[0]
load = load_json