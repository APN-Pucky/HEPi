import json
from smpl import plot
import numpy as np

from .input import Order, order_to_string
from .util import LD2DF, get_name
from smpl import io

splot = plot


def write_latex(dict_list, key, fname, scale=True, pdf=True, yscale=1.):
    """
 Saves a `dict` of `list`s to `filename` as latex table.
 """
    dl = dict_list
    mask = dl["NLO_SCALE"] != np.array(None)
    lo = splot.unv(dl["LO"][mask])
    nlo = splot.unv(dl["NLO"][mask])
    nlo_plus_nll = splot.unv(dl["NLO_PLUS_NLL"][mask])
    with open(fname, 'w+') as f:
        for i in range(len(dl["LO"][mask])):
            f.write(
                "$" + io.gf(4).format(dl[key][mask][i]) + "$ \t&\t $" +
                "{:.3f}".format(lo[i] * yscale) + "^{+" +
                "{:.1f}".format(dl["LO_SCALE_ERRPLUS"][mask][i] / lo[i] *
                                100.) + "\\%}_{" +
                "{:.1f}".format(dl["LO_SCALE_ERRMINUS"][mask][i] / lo[i] *
                                100.) + "\\%}$ \t&\t $" +
                "{:.3f}".format(nlo[i] * yscale) + "^{+" +
                "{:.1f}".format(dl["NLO_SCALE_ERRPLUS"][mask][i] / nlo[i] *
                                100.) +
                ("\\%+" + "{:.1f}".format(dl["NLO_PDF_ERRPLUS"][mask][i] /
                                          nlo[i] * 100.) if pdf else "") +
                "\\%}_{" + "{:.1f}".format(dl["NLO_SCALE_ERRMINUS"][mask][i] /
                                           nlo[i] * 100.) +
                ("\\%" + "{:.1f}".format(dl["NLO_PDF_ERRMINUS"][mask][i] /
                                         nlo[i] * 100.) if pdf else "") +
                "\\%}$ \t&\t $" + "{:.3f}".format(nlo_plus_nll[i] * yscale) +
                "^{+" +
                "{:.1f}".format(dl["NLO_PLUS_NLL_SCALE_ERRPLUS"][mask][i] /
                                nlo_plus_nll[i] * 100.) +
                ("\\%+" +
                 "{:.1f}".format(dl["NLO_PLUS_NLL_PDF_ERRPLUS"][mask][i] /
                                 nlo_plus_nll[i] * 100.) if pdf else "") +
                "\\%}_{" +
                "{:.1f}".format(dl["NLO_PLUS_NLL_SCALE_ERRMINUS"][mask][i] /
                                nlo_plus_nll[i] * 100.) +
                ("\\%" +
                 "{:.1f}".format(dl["NLO_PLUS_NLL_PDF_ERRMINUS"][mask][i] /
                                 nlo_plus_nll[i] * 100.) if pdf else "") +
                "\\%}$ " + "\\\\\n")


tex_table = write_latex


def write_csv(dict_list: list, filename: str):
    """
 Saves a `dict` of `list`s to `filename` as csv table.
 """
    df = LD2DF(dict_list)
    df.to_csv(filename, index=False)


def write_json(dict_list: list,
               o: Order,
               parameter: str,
               filename: str,
               error_sym=False,
               error_asym=False):
    """
 Saves a `dict` of `list`s to `filename` as json.

 Cf. https://github.com/fuenfundachtzig/xsec
 """
    jd = {}
    jd["initial state"] = "pp"  # TODO add more such cases + filters, also in resummino
    if o == Order.LO:
        jd["order"] = "LO"
    elif o == Order.NLO:
        jd["order"] = "NLO"
    elif o == Order.NLO_PLUS_NLL:
        jd["order"] = "NLO+NLL"
    elif o == Order.aNNLO_PLUS_NNLL:
        jd["order"] = "NNLOapprox+NNLL"
    else:
        raise ValueError("Order not supported by write_json.")
    jd["source"] = "HEPi"
    jd["contact"] = "?"
    jd["tool"] = dict_list["code"][0]
    jd["process_latex"] = "$" + get_name(dict_list["particle1"][0]) + get_name(
        dict_list["particle2"][0]) + "$"
    jd["comment"] = dict_list["id"][0]
    jd["reference"] = "?"
    jd["Ecom [GeV]"] = str(dict_list["energy"][0])
    jd["process_id"] = "pp_" + str(dict_list["energy"][0]) + "_" + str(
        dict_list["particle1"][0]) + "_" + str(dict_list["particle2"][0])
    jd["PDF set"] = dict_list["pdf_nlo"][0]
    dat = {}
    for j in range(len(dict_list[parameter])):
        if error_asym:
            raise ValueError("asymmetric errors not supported by write_json.")
        elif error_sym:
            dat[str(dict_list[parameter][j])] = {
                "xsec_pb": float(plot.unv(dict_list[order_to_string(o)][j])),
                "unc_pb": float(plot.usd(dict_list[order_to_string(o)][j]))
            }
        else:
            dat[str(dict_list[parameter][j])] = {
                "xsec_pb": float(plot.unv(dict_list[order_to_string(o)][j]))
            }
    jd["data"] = dat
    jd["parameters"] = "?"
    with open(filename, 'w+') as f:
        f.write(json.dumps(jd))
